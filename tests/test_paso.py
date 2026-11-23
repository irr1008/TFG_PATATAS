from dataclasses import FrozenInstanceError, replace
from math import expm1, fsum

import pytest

from modelo_fisico.configuracion import (
    Capa,
    ConfiguracionPerfil,
    OpcionesProcesos,
)
from modelo_fisico.conversiones import humedad_a_almacenamiento
from modelo_fisico.entradas import EntradasPaso
from modelo_fisico.estados import EstadoPerfil
from modelo_fisico.paso import ejecutar_paso


def crear_perfil(
    *, infiltracion=True, transferencias=True, drenaje_inferior=True
):
    return ConfiguracionPerfil(
        capas=(
            Capa(0.0, 0.2, 0.05, 0.25, 0.45, 6.0),
            Capa(0.2, 0.6, 0.05, 0.25, 0.45, 12.0),
        ),
        f_max_mm_h=12.0,
        procesos=OpcionesProcesos(
            infiltracion=infiltracion,
            transferencias=transferencias,
            drenaje_inferior=drenaje_inferior,
        ),
    )


def crear_entradas(
    perfil,
    *,
    precipitacion_mm=0.0,
    riego_mm=0.0,
    demandas=None,
    dt_s=300.0,
):
    if demandas is None:
        demandas = (0.0,) * perfil.numero_capas
    return EntradasPaso(
        configuracion=perfil,
        dt_s=dt_s,
        precipitacion_mm=precipitacion_mm,
        riego_mm=riego_mm,
        extracciones_solicitadas_mm=demandas,
    )


def comprobar_balance_independiente(estado, resultado):
    delta = fsum(resultado.estado_final.almacenamientos_mm) - fsum(
        estado.almacenamientos_mm
    )
    balance = fsum(
        (
            resultado.aporte_mm,
            -resultado.salida_superficial_mm,
            -resultado.drenaje_inferior_mm,
            -fsum(resultado.extracciones_mm),
        )
    )
    residual = delta - balance

    assert residual == pytest.approx(
        0.0, rel=0.0, abs=resultado.tolerancia_masa_mm
    )
    assert resultado.residual_masa_mm == pytest.approx(
        residual, rel=0.0, abs=1e-12
    )
    assert resultado.aporte_mm == pytest.approx(
        resultado.infiltracion_mm + resultado.salida_superficial_mm,
        rel=1e-12,
        abs=1e-12,
    )


def test_caso_a_reposo():
    perfil = crear_perfil()
    estado = EstadoPerfil(perfil, (40.0, 80.0))

    resultado = ejecutar_paso(estado, crear_entradas(perfil))

    assert resultado.estado_final.almacenamientos_mm == (40.0, 80.0)
    assert resultado.drenaje_inferior_mm == 0.0
    assert resultado.transferencias_mm == (0.0,)
    assert resultado.extracciones_mm == (0.0, 0.0)
    comprobar_balance_independiente(estado, resultado)


def test_caso_c_capacidad_de_entrada_en_el_paso_completo():
    perfil = crear_perfil(transferencias=False, drenaje_inferior=False)
    estado = EstadoPerfil(perfil, (40.0, 80.0))

    resultado = ejecutar_paso(
        estado, crear_entradas(perfil, precipitacion_mm=3.0)
    )

    assert resultado.infiltracion_mm == pytest.approx(1.0)
    assert resultado.salida_superficial_mm == pytest.approx(2.0)
    assert resultado.estado_final.almacenamientos_mm == pytest.approx(
        (41.0, 80.0)
    )
    comprobar_balance_independiente(estado, resultado)


def test_caso_f_transferencia_analitica_en_el_paso_completo():
    perfil = crear_perfil(drenaje_inferior=False, infiltracion=False)
    estado = EstadoPerfil(perfil, (74.0, 80.0))

    resultado = ejecutar_paso(estado, crear_entradas(perfil))

    esperado = 24.0 * -expm1(-1.0 / 72.0)
    assert resultado.transferencias_mm[0] == pytest.approx(
        esperado, rel=1e-12, abs=1e-12
    )
    assert resultado.estado_final.almacenamientos_mm == pytest.approx(
        (74.0 - esperado, 80.0 + esperado), rel=1e-12, abs=1e-12
    )
    comprobar_balance_independiente(estado, resultado)


def test_caso_g_drenaje_inferior_analitico_en_el_paso_completo():
    perfil = crear_perfil(transferencias=False, infiltracion=False)
    estado = EstadoPerfil(perfil, (40.0, 124.0))

    resultado = ejecutar_paso(estado, crear_entradas(perfil))

    esperado = 24.0 * -expm1(-1.0 / 144.0)
    assert resultado.drenaje_inferior_mm == pytest.approx(
        esperado, rel=1e-12, abs=1e-12
    )
    assert resultado.estado_final.almacenamientos_mm == pytest.approx(
        (40.0, 124.0 - esperado), rel=1e-12, abs=1e-12
    )
    comprobar_balance_independiente(estado, resultado)


def test_caso_h_extraccion_limitada_en_el_paso_completo():
    perfil = crear_perfil(
        infiltracion=False,
        transferencias=False,
        drenaje_inferior=False,
    )
    estado = EstadoPerfil(perfil, (10.5, 20.0))

    resultado = ejecutar_paso(
        estado, crear_entradas(perfil, demandas=(2.0, 0.0))
    )

    assert resultado.extracciones_mm == pytest.approx((0.5, 0.0))
    assert resultado.demandas_no_satisfechas_mm == pytest.approx(
        (1.5, 0.0)
    )
    assert resultado.estado_final.almacenamientos_mm == pytest.approx(
        (10.0, 20.0), rel=1e-12, abs=1e-12
    )
    comprobar_balance_independiente(estado, resultado)


def test_orden_el_drenaje_libera_hueco_antes_de_infiltrar():
    perfil = ConfiguracionPerfil(
        capas=(Capa(0.0, 0.25, 0.0, 0.2, 0.4, 1.0),),
        f_max_mm_h=12.0,
    )
    estado = EstadoPerfil(perfil, (100.0,))

    resultado = ejecutar_paso(
        estado, crear_entradas(perfil, precipitacion_mm=0.5)
    )

    assert resultado.drenaje_inferior_mm > 0.5
    assert resultado.infiltracion_mm == pytest.approx(0.5)
    assert resultado.salida_superficial_mm == 0.0
    comprobar_balance_independiente(estado, resultado)


def test_orden_el_agua_infiltrada_no_drena_en_el_mismo_paso():
    perfil = crear_perfil()
    capacidades = tuple(
        humedad_a_almacenamiento(capa.theta_fc, capa.espesor_m)
        for capa in perfil.capas
    )
    estado = EstadoPerfil(perfil, capacidades)

    resultado = ejecutar_paso(
        estado, crear_entradas(perfil, precipitacion_mm=1.0)
    )

    assert resultado.infiltracion_mm == pytest.approx(1.0)
    assert resultado.drenaje_inferior_mm == 0.0
    assert resultado.transferencias_mm == (0.0,)
    assert resultado.estado_final.almacenamientos_mm == pytest.approx(
        (capacidades[0] + 1.0, capacidades[1]), rel=1e-12, abs=1e-12
    )
    comprobar_balance_independiente(estado, resultado)


def test_orden_la_extraccion_usa_el_estado_posterior_a_la_infiltracion():
    perfil = crear_perfil(
        transferencias=False, drenaje_inferior=False
    )
    estado = EstadoPerfil(perfil, (10.0, 80.0))

    resultado = ejecutar_paso(
        estado,
        crear_entradas(
            perfil, precipitacion_mm=1.0, demandas=(1.0, 0.0)
        ),
    )

    assert resultado.infiltracion_mm == pytest.approx(1.0)
    assert resultado.extracciones_mm == pytest.approx((1.0, 0.0))
    assert resultado.demandas_no_satisfechas_mm == pytest.approx(
        (0.0, 0.0)
    )
    assert resultado.estado_final.almacenamientos_mm == pytest.approx(
        (10.0, 80.0), rel=1e-12, abs=1e-12
    )
    comprobar_balance_independiente(estado, resultado)


def test_orden_completo_con_todos_los_procesos_y_tres_capas():
    perfil = ConfiguracionPerfil(
        capas=(
            Capa(0.0, 0.2, 0.05, 0.25, 0.45, 6.0),
            Capa(0.2, 0.4, 0.05, 0.25, 0.45, 9.0),
            Capa(0.4, 0.6, 0.05, 0.25, 0.45, 12.0),
        ),
        f_max_mm_h=12.0,
    )
    estado = EstadoPerfil(perfil, (74.0, 70.0, 74.0))
    entradas = crear_entradas(
        perfil,
        precipitacion_mm=0.5,
        riego_mm=0.5,
        demandas=(0.2, 0.1, 0.05),
    )

    resultado = ejecutar_paso(estado, entradas)

    assert resultado.drenaje_inferior_mm > 0.0
    assert all(f > 0.0 for f in resultado.transferencias_mm)
    assert resultado.infiltracion_mm == pytest.approx(1.0)
    assert resultado.extracciones_mm == pytest.approx((0.2, 0.1, 0.05))
    comprobar_balance_independiente(estado, resultado)


def test_residuales_de_las_fases_se_registran_en_orden():
    perfil = crear_perfil()
    estado = EstadoPerfil(perfil, (74.0, 124.0))

    resultado = ejecutar_paso(
        estado,
        crear_entradas(
            perfil, precipitacion_mm=0.5, demandas=(0.1, 0.1)
        ),
    )

    assert len(resultado.residuales_fases_mm) == 3
    for residual in resultado.residuales_fases_mm:
        assert residual == pytest.approx(0.0, rel=0.0, abs=1e-9)


@pytest.mark.parametrize("numero_capas", [1, 3])
def test_admite_una_y_mas_de_dos_capas(numero_capas):
    perfil = ConfiguracionPerfil(
        capas=tuple(
            Capa(i * 0.25, (i + 1) * 0.25, 0.0, 0.2, 0.4, 6.0)
            for i in range(numero_capas)
        ),
        f_max_mm_h=12.0,
    )
    estado = EstadoPerfil(perfil, (60.0,) * numero_capas)
    entradas = crear_entradas(
        perfil,
        precipitacion_mm=0.5,
        demandas=(0.1,) * numero_capas,
    )

    resultado = ejecutar_paso(estado, entradas)

    assert len(resultado.transferencias_mm) == numero_capas - 1
    assert len(resultado.extracciones_mm) == numero_capas
    comprobar_balance_independiente(estado, resultado)


def test_no_modifica_objetos_y_resultado_es_inmutable():
    perfil = crear_perfil()
    estado = EstadoPerfil(perfil, (74.0, 124.0))
    entradas = crear_entradas(
        perfil, precipitacion_mm=0.5, demandas=(0.1, 0.2)
    )

    resultado = ejecutar_paso(estado, entradas)

    assert estado.almacenamientos_mm == (74.0, 124.0)
    assert entradas.extracciones_solicitadas_mm == (0.1, 0.2)
    assert entradas.precipitacion_mm == 0.5
    assert resultado.estado_final is not estado

    with pytest.raises(FrozenInstanceError):
        resultado.infiltracion_mm = 0.0


def test_procesos_desactivados_dejan_solo_la_extraccion():
    perfil = crear_perfil(
        infiltracion=False,
        transferencias=False,
        drenaje_inferior=False,
    )
    estado = EstadoPerfil(perfil, (74.0, 124.0))
    entradas = crear_entradas(
        perfil, precipitacion_mm=2.0, demandas=(1.0, 1.0)
    )

    resultado = ejecutar_paso(estado, entradas)

    assert resultado.infiltracion_mm == 0.0
    assert resultado.salida_superficial_mm == pytest.approx(2.0)
    assert resultado.drenaje_inferior_mm == 0.0
    assert resultado.transferencias_mm == (0.0,)
    assert resultado.estado_final.almacenamientos_mm == pytest.approx(
        (73.0, 123.0)
    )
    comprobar_balance_independiente(estado, resultado)


def test_rechaza_configuraciones_distintas():
    perfil = crear_perfil()
    otro_perfil = replace(perfil, f_max_mm_h=6.0)
    estado = EstadoPerfil(perfil, (40.0, 80.0))

    with pytest.raises(ValueError):
        ejecutar_paso(estado, crear_entradas(otro_perfil))


def test_rechaza_estado_de_tipo_incorrecto():
    with pytest.raises(ValueError):
        ejecutar_paso(None, crear_entradas(crear_perfil()))


def test_rechaza_entradas_de_tipo_incorrecto():
    estado = EstadoPerfil(crear_perfil(), (40.0, 80.0))

    with pytest.raises(ValueError):
        ejecutar_paso(estado, None)
