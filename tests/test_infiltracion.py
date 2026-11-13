from dataclasses import FrozenInstanceError, replace
from math import fsum

import pytest

from modelo_fisico.configuracion import (
    Capa,
    ConfiguracionPerfil,
    OpcionesProcesos,
)
from modelo_fisico.conversiones import humedad_a_almacenamiento
from modelo_fisico.drenaje import aplicar_drenaje
from modelo_fisico.entradas import EntradasPaso
from modelo_fisico.estados import EstadoPerfil
from modelo_fisico.infiltracion import aplicar_infiltracion


def crear_perfil(*, infiltracion=True):
    return ConfiguracionPerfil(
        capas=(
            Capa(0.0, 0.2, 0.05, 0.25, 0.45, 6.0),
            Capa(0.2, 0.6, 0.05, 0.25, 0.45, 12.0),
        ),
        f_max_mm_h=12.0,
        procesos=OpcionesProcesos(
            infiltracion=infiltracion,
            transferencias=False,
            drenaje_inferior=False,
        ),
    )


def crear_entradas(
    perfil,
    *,
    precipitacion_mm=0.0,
    riego_mm=0.0,
):
    return EntradasPaso(
        configuracion=perfil,
        dt_s=300.0,
        precipitacion_mm=precipitacion_mm,
        riego_mm=riego_mm,
        extracciones_solicitadas_mm=(0.0,) * perfil.numero_capas,
    )


def comprobar_balance(estado, entradas, resultado):
    residual = fsum(
        (
            fsum(resultado.estado_final.almacenamientos_mm),
            -fsum(estado.almacenamientos_mm),
            -entradas.precipitacion_mm,
            -entradas.riego_mm,
            resultado.salida_superficial_mm,
        )
    )

    assert residual == pytest.approx(
        0.0, rel=0.0, abs=resultado.tolerancia_masa_mm
    )
    assert resultado.residual_masa_mm == pytest.approx(
        residual, rel=0.0, abs=1e-12
    )


@pytest.mark.parametrize(
    ("superior_mm", "aporte_mm", "infiltracion_mm", "salida_mm"),
    [
        (40.0, 0.0, 0.0, 0.0),
        (40.0, 0.5, 0.5, 0.0),
        (40.0, 3.0, 1.0, 2.0),
        (89.5, 3.0, 0.5, 2.5),
    ],
)
def test_casos_sin_aporte_y_b_c_d(
    superior_mm, aporte_mm, infiltracion_mm, salida_mm
):
    perfil = crear_perfil()
    estado = EstadoPerfil(perfil, (superior_mm, 80.0))
    entradas = crear_entradas(perfil, precipitacion_mm=aporte_mm)

    resultado = aplicar_infiltracion(estado, entradas)

    assert resultado.infiltracion_mm == pytest.approx(
        infiltracion_mm, rel=1e-12, abs=1e-12
    )
    assert resultado.salida_superficial_mm == pytest.approx(
        salida_mm, rel=1e-12, abs=1e-12
    )
    assert resultado.estado_final.almacenamientos_mm == pytest.approx(
        (superior_mm + infiltracion_mm, 80.0),
        rel=1e-12,
        abs=1e-12,
    )
    comprobar_balance(estado, entradas, resultado)


def test_suma_precipitacion_y_riego_sin_reconvertir_acumulados():
    perfil = crear_perfil()
    estado = EstadoPerfil(perfil, (40.0, 80.0))
    entradas = crear_entradas(
        perfil, precipitacion_mm=0.2, riego_mm=0.3
    )

    resultado = aplicar_infiltracion(estado, entradas)

    assert resultado.infiltracion_mm == pytest.approx(0.5)
    assert resultado.salida_superficial_mm == 0.0
    assert resultado.estado_final.almacenamientos_mm == (40.5, 80.0)
    comprobar_balance(estado, entradas, resultado)


def test_infiltracion_desactivada_no_modifica_almacenamientos():
    perfil = crear_perfil(infiltracion=False)
    estado = EstadoPerfil(perfil, (40.0, 80.0))
    entradas = crear_entradas(perfil, precipitacion_mm=3.0)

    resultado = aplicar_infiltracion(estado, entradas)

    assert resultado.infiltracion_mm == 0.0
    assert resultado.salida_superficial_mm == 3.0
    assert resultado.estado_final.almacenamientos_mm == (40.0, 80.0)
    comprobar_balance(estado, entradas, resultado)


def test_capa_superior_saturada_no_admite_agua():
    perfil = crear_perfil()
    capa = perfil.capas[0]
    saturacion = humedad_a_almacenamiento(
        capa.theta_sat, capa.espesor_m
    )
    estado = EstadoPerfil(perfil, (saturacion, 80.0))
    entradas = crear_entradas(perfil, precipitacion_mm=3.0)

    resultado = aplicar_infiltracion(estado, entradas)

    assert resultado.infiltracion_mm == 0.0
    assert resultado.salida_superficial_mm == 3.0
    assert (
        resultado.estado_final.almacenamientos_mm
        == estado.almacenamientos_mm
    )
    comprobar_balance(estado, entradas, resultado)


@pytest.mark.parametrize("numero_capas", [1, 3])
def test_admite_una_y_mas_de_dos_capas(numero_capas):
    perfil = ConfiguracionPerfil(
        capas=tuple(
            Capa(i * 0.25, (i + 1) * 0.25, 0.0, 0.2, 0.4)
            for i in range(numero_capas)
        ),
        f_max_mm_h=12.0,
        procesos=OpcionesProcesos(
            infiltracion=True,
            transferencias=False,
            drenaje_inferior=False,
        ),
    )
    estado = EstadoPerfil(perfil, (40.0,) * numero_capas)
    entradas = crear_entradas(perfil, precipitacion_mm=0.5)

    resultado = aplicar_infiltracion(estado, entradas)

    assert resultado.estado_final.almacenamientos_mm == (
        (40.5,) + (40.0,) * (numero_capas - 1)
    )
    comprobar_balance(estado, entradas, resultado)


def test_utiliza_el_hueco_posterior_al_drenaje():
    perfil = ConfiguracionPerfil(
        capas=(Capa(0.0, 0.25, 0.0, 0.2, 0.4, 1.0),),
        f_max_mm_h=12.0,
    )
    estado = EstadoPerfil(perfil, (100.0,))
    entradas = crear_entradas(perfil, precipitacion_mm=0.5)

    drenaje = aplicar_drenaje(estado, entradas.dt_h)
    resultado = aplicar_infiltracion(drenaje.estado_final, entradas)

    assert drenaje.drenaje_inferior_mm > 0.5
    assert resultado.infiltracion_mm == pytest.approx(0.5)
    assert resultado.salida_superficial_mm == 0.0
    assert resultado.estado_final.almacenamientos_mm == pytest.approx(
        (100.0 - drenaje.drenaje_inferior_mm + 0.5,),
        rel=1e-12,
        abs=1e-12,
    )
    comprobar_balance(drenaje.estado_final, entradas, resultado)


def test_no_modifica_objetos_ni_aplica_extracciones():
    perfil = crear_perfil()
    estado = EstadoPerfil(perfil, (40.0, 80.0))
    entradas = replace(
        crear_entradas(perfil, precipitacion_mm=0.5),
        extracciones_solicitadas_mm=(2.0, 3.0),
    )

    resultado = aplicar_infiltracion(estado, entradas)

    assert estado.almacenamientos_mm == (40.0, 80.0)
    assert entradas.extracciones_solicitadas_mm == (2.0, 3.0)
    assert resultado.estado_final is not estado
    assert resultado.estado_final.almacenamientos_mm == (40.5, 80.0)

    with pytest.raises(FrozenInstanceError):
        resultado.infiltracion_mm = 0.0


def test_rechaza_configuraciones_distintas():
    perfil = crear_perfil()
    otro_perfil = replace(perfil, f_max_mm_h=6.0)
    estado = EstadoPerfil(perfil, (40.0, 80.0))
    entradas = crear_entradas(otro_perfil)

    with pytest.raises(ValueError):
        aplicar_infiltracion(estado, entradas)


def test_admite_configuraciones_equivalentes():
    perfil = crear_perfil()
    otro_perfil = crear_perfil()
    estado = EstadoPerfil(perfil, (40.0, 80.0))
    entradas = crear_entradas(otro_perfil, precipitacion_mm=0.5)

    resultado = aplicar_infiltracion(estado, entradas)

    assert resultado.estado_final.almacenamientos_mm == (40.5, 80.0)


def test_rechaza_estado_de_tipo_incorrecto():
    entradas = crear_entradas(crear_perfil())

    with pytest.raises(ValueError):
        aplicar_infiltracion(None, entradas)


def test_rechaza_entradas_de_tipo_incorrecto():
    estado = EstadoPerfil(crear_perfil(), (40.0, 80.0))

    with pytest.raises(ValueError):
        aplicar_infiltracion(estado, None)
