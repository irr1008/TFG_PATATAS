from dataclasses import FrozenInstanceError
from math import exp, fsum
from modelo_fisico.conversiones import humedad_a_almacenamiento

import pytest

from modelo_fisico.configuracion import (
    Capa,
    ConfiguracionPerfil,
    OpcionesProcesos,
)
from modelo_fisico.drenaje import aplicar_drenaje
from modelo_fisico.estados import EstadoPerfil


ABS_MM = 1e-12
REL = 1e-12


def perfil_base(*, transferencias=True, drenaje_inferior=True):
    return ConfiguracionPerfil(
        capas=(
            Capa(0.0, 0.2, 0.05, 0.25, 0.45, 6.0),
            Capa(0.2, 0.6, 0.05, 0.25, 0.45, 12.0),
        ),
        f_max_mm_h=12.0,
        procesos=OpcionesProcesos(
            infiltracion=False,
            transferencias=transferencias,
            drenaje_inferior=drenaje_inferior,
        ),
    )


def comprobar_balance(estado, resultado):
    residual_independiente = (
        fsum(resultado.estado_final.almacenamientos_mm)
        - fsum(estado.almacenamientos_mm)
        + resultado.drenaje_inferior_mm
    )

    assert residual_independiente == pytest.approx(
        0.0, rel=0.0, abs=resultado.tolerancia_masa_mm
    )
    assert resultado.residual_masa_mm == pytest.approx(
        residual_independiente, rel=0.0, abs=ABS_MM
    )


def test_caso_g_drenaje_inferior():
    estado = EstadoPerfil(
        perfil_base(transferencias=False),
        (40.0, 124.0),
    )

    resultado = aplicar_drenaje(estado, 300.0 / 3600.0)
    esperado = 24.0 * (1.0 - exp(-1.0 / 144.0))

    assert resultado.drenaje_inferior_mm == pytest.approx(
        esperado, rel=REL, abs=ABS_MM
    )
    assert resultado.transferencias_mm == (0.0,)
    assert resultado.estado_final.almacenamientos_mm == pytest.approx(
        (40.0, 124.0 - esperado), rel=REL, abs=ABS_MM
    )
    comprobar_balance(estado, resultado)


def test_caso_f_transferencia_conservativa():
    estado = EstadoPerfil(
        perfil_base(drenaje_inferior=False),
        (74.0, 80.0),
    )

    resultado = aplicar_drenaje(estado, 300.0 / 3600.0)
    esperado = 24.0 * (1.0 - exp(-1.0 / 72.0))

    assert resultado.transferencias_mm == pytest.approx(
        (esperado,), rel=REL, abs=ABS_MM
    )
    assert resultado.drenaje_inferior_mm == 0.0
    assert resultado.estado_final.almacenamientos_mm == pytest.approx(
        (74.0 - esperado, 80.0 + esperado),
        rel=REL,
        abs=ABS_MM,
    )
    comprobar_balance(estado, resultado)


def test_caso_e_receptora_llena():
    perfil = perfil_base(drenaje_inferior=False)
    capa_inferior = perfil.capas[1]
    saturacion_inferior = humedad_a_almacenamiento(
        capa_inferior.theta_sat,
        capa_inferior.espesor_m,
    )
    estado = EstadoPerfil(perfil, (74.0, saturacion_inferior))

    resultado = aplicar_drenaje(estado, 300.0 / 3600.0)

    assert resultado.transferencias_mm == (0.0,)
    assert resultado.drenaje_inferior_mm == 0.0
    assert (
        resultado.estado_final.almacenamientos_mm
        == estado.almacenamientos_mm
    )
    comprobar_balance(estado, resultado)


def test_transferencia_limitada_por_hueco_receptor():
    estado = EstadoPerfil(
        perfil_base(drenaje_inferior=False),
        (74.0, 179.9),
    )

    resultado = aplicar_drenaje(estado, 300.0 / 3600.0)
    hueco = (
        1000.0
        * estado.configuracion.capas[1].espesor_m
        * estado.configuracion.capas[1].theta_sat
        - 179.9
    )

    assert resultado.transferencias_mm == pytest.approx(
        (hueco,), rel=REL, abs=ABS_MM
    )
    assert resultado.estado_final.almacenamientos_mm == pytest.approx(
        (74.0 - hueco, 180.0), rel=REL, abs=ABS_MM
    )
    comprobar_balance(estado, resultado)


def test_fondo_libera_hueco_antes_de_transferir():
    perfil = perfil_base()
    capa_inferior = perfil.capas[1]

    saturacion_inferior = humedad_a_almacenamiento(
        capa_inferior.theta_sat,
        capa_inferior.espesor_m,
    )
    capacidad_campo_inferior = humedad_a_almacenamiento(
        capa_inferior.theta_fc,
        capa_inferior.espesor_m,
    )
    estado = EstadoPerfil(perfil, (74.0, saturacion_inferior))

    resultado = aplicar_drenaje(estado, 300.0 / 3600.0)

    exceso_inferior = (
        saturacion_inferior - capacidad_campo_inferior
    )
    dp = exceso_inferior * (1.0 - exp(-1.0 / 144.0))
    transferencia = 24.0 * (1.0 - exp(-1.0 / 72.0))

    assert resultado.drenaje_inferior_mm == pytest.approx(
        dp, rel=REL, abs=ABS_MM
    )
    assert resultado.transferencias_mm == pytest.approx(
        (transferencia,), rel=REL, abs=ABS_MM
    )
    assert resultado.estado_final.almacenamientos_mm == pytest.approx(
        (
            74.0 - transferencia,
            saturacion_inferior - dp + transferencia,
        ),
        rel=REL,
        abs=ABS_MM,
    )
    comprobar_balance(estado, resultado)


def test_tres_capas_recorrido_abajo_arriba():
    perfil = ConfiguracionPerfil(
        capas=(
            Capa(0.0, 0.25, 0.0, 0.2, 0.4, 1.0),
            Capa(0.25, 0.5, 0.0, 0.2, 0.4, 1.0),
            Capa(0.5, 0.75, 0.0, 0.2, 0.4, None),
        ),
        f_max_mm_h=0.0,
        procesos=OpcionesProcesos(
            infiltracion=False,
            transferencias=True,
            drenaje_inferior=False,
        ),
    )
    estado = EstadoPerfil(perfil, (90.0, 100.0, 90.0))

    resultado = aplicar_drenaje(estado, 1.0)

    # La capa intermedia libera 10 mm antes de recibir agua.
    assert resultado.transferencias_mm == pytest.approx(
        (10.0, 10.0), rel=REL, abs=ABS_MM
    )
    assert resultado.estado_final.almacenamientos_mm == pytest.approx(
        (80.0, 100.0, 100.0), rel=REL, abs=ABS_MM
    )
    comprobar_balance(estado, resultado)


def test_agua_recibida_no_vuelve_a_drenar_en_la_misma_fase():
    perfil = perfil_base()
    capa_inferior = perfil.capas[1]
    capacidad_campo_inferior = humedad_a_almacenamiento(
        capa_inferior.theta_fc,
        capa_inferior.espesor_m,
    )
    estado = EstadoPerfil(
        perfil,
        (74.0, capacidad_campo_inferior),
    )

    resultado = aplicar_drenaje(estado, 300.0 / 3600.0)

    assert resultado.drenaje_inferior_mm == 0.0
    assert resultado.transferencias_mm[0] > 0.0
    assert (
        resultado.estado_final.almacenamientos_mm[1]
        > capacidad_campo_inferior
    )
    comprobar_balance(estado, resultado)


def test_una_capa_sin_interfaces():
    perfil = ConfiguracionPerfil(
        capas=(Capa(0.0, 0.25, 0.0, 0.2, 0.4, 1.0),),
        f_max_mm_h=0.0,
    )
    estado = EstadoPerfil(perfil, (90.0,))

    resultado = aplicar_drenaje(estado, 1.0)
    esperado = 40.0 * (1.0 - exp(-1.0))

    assert resultado.transferencias_mm == ()
    assert resultado.drenaje_inferior_mm == pytest.approx(
        esperado, rel=REL, abs=ABS_MM
    )
    assert resultado.estado_final.almacenamientos_mm == pytest.approx(
        (90.0 - esperado,), rel=REL, abs=ABS_MM
    )
    comprobar_balance(estado, resultado)


def test_salidas_desactivadas_admiten_tau_ausente():
    perfil = ConfiguracionPerfil(
        capas=(
            Capa(0.0, 0.25, 0.0, 0.2, 0.4, None),
            Capa(0.25, 0.5, 0.0, 0.2, 0.4, None),
        ),
        f_max_mm_h=0.0,
        procesos=OpcionesProcesos(
            infiltracion=False,
            transferencias=False,
            drenaje_inferior=False,
        ),
    )
    estado = EstadoPerfil(perfil, (90.0, 90.0))

    resultado = aplicar_drenaje(estado, 1.0)

    assert resultado.estado_final.almacenamientos_mm == (90.0, 90.0)
    assert resultado.transferencias_mm == (0.0,)
    assert resultado.drenaje_inferior_mm == 0.0
    comprobar_balance(estado, resultado)


def test_no_modifica_estado_y_resultado_es_inmutable():
    estado = EstadoPerfil(perfil_base(), (74.0, 124.0))
    originales = estado.almacenamientos_mm

    resultado = aplicar_drenaje(estado, 1.0)

    assert estado.almacenamientos_mm == originales
    assert resultado.estado_final is not estado
    assert resultado.estado_final.configuracion is estado.configuracion

    with pytest.raises(FrozenInstanceError):
        resultado.drenaje_inferior_mm = 0.0


@pytest.mark.parametrize(
    "dt_h",
    [0.0, -1.0, float("nan"), float("inf"), True, "1", None],
)
def test_rechaza_duracion_invalida(dt_h):
    estado = EstadoPerfil(perfil_base(), (40.0, 80.0))

    with pytest.raises(ValueError):
        aplicar_drenaje(estado, dt_h)


def test_rechaza_estado_de_tipo_incorrecto():
    with pytest.raises(ValueError):
        aplicar_drenaje(None, 1.0)
