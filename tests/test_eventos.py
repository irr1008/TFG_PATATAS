from dataclasses import FrozenInstanceError, replace
from math import fsum

import pytest

from modelo_fisico.configuracion import (
    Capa,
    ConfiguracionPerfil,
    OpcionesProcesos,
)
from modelo_fisico.eventos import EventoTasas, integrar_eventos
from modelo_fisico.tiempos import (
    IntervaloTemporal,
    construir_intervalos,
)


def crear_perfil():
    return ConfiguracionPerfil(
        capas=(
            Capa(0.0, 0.2, 0.05, 0.25, 0.45),
            Capa(0.2, 0.6, 0.05, 0.25, 0.45),
        ),
        f_max_mm_h=12.0,
        procesos=OpcionesProcesos(
            infiltracion=True,
            transferencias=False,
            drenaje_inferior=False,
        ),
    )


def crear_evento():
    return EventoTasas(
        inicio_s=0.0,
        fin_s=7200.0,
        precipitacion_mm_h=0.0,
        riego_mm_h=6.0,
        extracciones_mm_h=(0.0, 0.0),
    )


def test_convierte_tasas_una_sola_vez():
    entradas = integrar_eventos(
        crear_perfil(),
        IntervaloTemporal(0.0, 300.0),
        (crear_evento(),),
    )

    assert entradas.dt_s == 300.0
    assert entradas.riego_mm == pytest.approx(
        0.5, rel=1e-12, abs=1e-12
    )
    assert entradas.precipitacion_mm == 0.0
    assert entradas.extracciones_solicitadas_mm == (0.0, 0.0)


def test_solape_parcial():
    evento = replace(
        crear_evento(), inicio_s=150.0, fin_s=450.0
    )

    entradas = integrar_eventos(
        crear_perfil(),
        IntervaloTemporal(0.0, 300.0),
        (evento,),
    )

    assert entradas.riego_mm == pytest.approx(
        0.25, rel=1e-12, abs=1e-12
    )


def test_evento_que_termina_al_inicio_no_aporta():
    evento = replace(crear_evento(), fin_s=300.0)

    entradas = integrar_eventos(
        crear_perfil(),
        IntervaloTemporal(300.0, 600.0),
        (evento,),
    )

    assert entradas.riego_mm == 0.0


def test_evento_que_empieza_al_final_no_aporta():
    evento = replace(
        crear_evento(), inicio_s=300.0, fin_s=600.0
    )

    entradas = integrar_eventos(
        crear_perfil(),
        IntervaloTemporal(0.0, 300.0),
        (evento,),
    )

    assert entradas.riego_mm == 0.0


def test_suma_eventos_solapados():
    evento = crear_evento()
    adicional = replace(
        evento,
        precipitacion_mm_h=3.0,
        riego_mm_h=0.0,
        extracciones_mm_h=(0.6, 1.2),
    )

    entradas = integrar_eventos(
        crear_perfil(),
        IntervaloTemporal(0.0, 600.0),
        (evento, adicional),
    )

    assert entradas.precipitacion_mm == pytest.approx(0.5)
    assert entradas.riego_mm == pytest.approx(1.0)
    assert entradas.extracciones_solicitadas_mm == pytest.approx(
        (0.1, 0.2), rel=1e-12, abs=1e-12
    )


def test_programacion_vacia_define_tasas_cero():
    entradas = integrar_eventos(
        crear_perfil(),
        IntervaloTemporal(0.0, 300.0),
        (),
    )

    assert entradas.precipitacion_mm == 0.0
    assert entradas.riego_mm == 0.0
    assert entradas.extracciones_solicitadas_mm == (0.0, 0.0)


@pytest.mark.parametrize("paso_s", [300.0, 150.0, 75.0, 37.5])
def test_conserva_el_total_del_evento_con_distintos_pasos(paso_s):
    perfil = crear_perfil()
    evento = replace(
        crear_evento(), inicio_s=125.0, fin_s=725.0
    )
    intervalos = construir_intervalos(
        1000.0,
        paso_s,
        cambios_s=(evento.inicio_s, evento.fin_s),
    )

    entradas = tuple(
        integrar_eventos(perfil, intervalo, (evento,))
        for intervalo in intervalos
    )

    assert fsum(e.riego_mm for e in entradas) == pytest.approx(
        1.0, rel=1e-12, abs=1e-12
    )


def test_acumulados_prescritos_del_escenario_11_1():
    perfil = crear_perfil()
    eventos = (
        crear_evento(),
        EventoTasas(
            inicio_s=7200.0,
            fin_s=86400.0,
            precipitacion_mm_h=0.0,
            riego_mm_h=0.0,
            extracciones_mm_h=(0.05, 0.10),
        ),
    )
    intervalos = construir_intervalos(
        86400.0,
        300.0,
        cambios_s=(0.0, 7200.0, 86400.0),
    )
    entradas = tuple(
        integrar_eventos(perfil, intervalo, eventos)
        for intervalo in intervalos
    )

    assert fsum(e.riego_mm for e in entradas) == pytest.approx(
        12.0, rel=1e-12, abs=1e-12
    )
    assert fsum(
        e.extracciones_solicitadas_mm[0] for e in entradas
    ) == pytest.approx(1.1, rel=1e-12, abs=1e-12)
    assert fsum(
        e.extracciones_solicitadas_mm[1] for e in entradas
    ) == pytest.approx(2.2, rel=1e-12, abs=1e-12)


@pytest.mark.parametrize(
    "cambios",
    [
        {"inicio_s": -1.0},
        {"fin_s": 0.0},
        {"fin_s": float("inf")},
        {"precipitacion_mm_h": -1.0},
        {"riego_mm_h": float("nan")},
        {"riego_mm_h": True},
        {"extracciones_mm_h": (0.0, -1.0)},
        {"extracciones_mm_h": (None, 0.0)},
        {"extracciones_mm_h": [0.0, 0.0]},
        {"extracciones_mm_h": ()},
    ],
)
def test_rechaza_eventos_invalidos(cambios):
    with pytest.raises(ValueError):
        replace(crear_evento(), **cambios)


def test_rechaza_numero_de_demandas_incorrecto_sin_solape():
    evento = replace(
        crear_evento(),
        inicio_s=600.0,
        extracciones_mm_h=(0.0,),
    )

    with pytest.raises(ValueError):
        integrar_eventos(
            crear_perfil(),
            IntervaloTemporal(0.0, 300.0),
            (evento,),
        )


@pytest.mark.parametrize("eventos", [None, [], (None,)])
def test_rechaza_programacion_invalida(eventos):
    with pytest.raises(ValueError):
        integrar_eventos(
            crear_perfil(),
            IntervaloTemporal(0.0, 300.0),
            eventos,
        )


def test_no_modifica_evento_y_es_inmutable():
    evento = crear_evento()

    integrar_eventos(
        crear_perfil(),
        IntervaloTemporal(0.0, 300.0),
        (evento,),
    )

    assert evento.riego_mm_h == 6.0
    assert evento.fin_s == 7200.0

    with pytest.raises(FrozenInstanceError):
        evento.riego_mm_h = 0.0
