from dataclasses import FrozenInstanceError
from math import fsum

import pytest

from modelo_fisico.tiempos import (
    IntervaloTemporal,
    construir_intervalos,
)


def extremos(intervalos):
    return tuple(
        (intervalo.inicio_s, intervalo.fin_s)
        for intervalo in intervalos
    )


def test_malla_nominal_exacta():
    intervalos = construir_intervalos(
        900.0, 300.0, cambios_s=()
    )

    assert extremos(intervalos) == (
        (0.0, 300.0),
        (300.0, 600.0),
        (600.0, 900.0),
    )


def test_ultimo_intervalo_mas_corto():
    intervalos = construir_intervalos(
        700.0, 300.0, cambios_s=()
    )

    assert extremos(intervalos) == (
        (0.0, 300.0),
        (300.0, 600.0),
        (600.0, 700.0),
    )
    assert intervalos[-1].dt_s == 100.0


def test_cambio_no_alineado_no_desplaza_la_malla():
    intervalos = construir_intervalos(
        700.0, 300.0, cambios_s=(450.0,)
    )

    assert extremos(intervalos) == (
        (0.0, 300.0),
        (300.0, 450.0),
        (450.0, 600.0),
        (600.0, 700.0),
    )


def test_cambios_repetidos_y_desordenados():
    intervalos = construir_intervalos(
        700.0,
        300.0,
        cambios_s=(450.0, 300.0, 450.0, 0.0, 700.0),
    )

    assert extremos(intervalos) == (
        (0.0, 300.0),
        (300.0, 450.0),
        (450.0, 600.0),
        (600.0, 700.0),
    )


def test_duracion_menor_que_el_paso_nominal():
    intervalos = construir_intervalos(
        100.0, 300.0, cambios_s=()
    )

    assert extremos(intervalos) == ((0.0, 100.0),)


def test_paso_fraccionario():
    intervalos = construir_intervalos(
        100.0, 37.5, cambios_s=()
    )

    assert extremos(intervalos) == (
        (0.0, 37.5),
        (37.5, 75.0),
        (75.0, 100.0),
    )


def test_cubre_la_duracion_sin_huecos():
    intervalos = construir_intervalos(
        1000.0,
        300.0,
        cambios_s=(125.0, 450.0, 925.0),
    )

    assert intervalos[0].inicio_s == 0.0
    assert intervalos[-1].fin_s == 1000.0

    for anterior, siguiente in zip(intervalos, intervalos[1:]):
        assert anterior.fin_s == siguiente.inicio_s

    assert all(intervalo.dt_s > 0 for intervalo in intervalos)
    assert fsum(i.dt_s for i in intervalos) == pytest.approx(
        1000.0, rel=0.0, abs=1e-12
    )


@pytest.mark.parametrize(
    "valor",
    [0.0, -1.0, float("nan"), float("inf"), True, "300", None],
)
def test_rechaza_duracion_invalida(valor):
    with pytest.raises(ValueError):
        construir_intervalos(valor, 300.0, cambios_s=())


@pytest.mark.parametrize(
    "valor",
    [0.0, -1.0, float("nan"), float("inf"), True, "300", None],
)
def test_rechaza_paso_invalido(valor):
    with pytest.raises(ValueError):
        construir_intervalos(900.0, valor, cambios_s=())


@pytest.mark.parametrize(
    "cambios",
    [
        (-1.0,),
        (901.0,),
        (float("nan"),),
        (float("inf"),),
        (True,),
        ("450",),
        (None,),
        [450.0],
        None,
    ],
)
def test_rechaza_cambios_invalidos(cambios):
    with pytest.raises(ValueError):
        construir_intervalos(
            900.0, 300.0, cambios_s=cambios
        )


@pytest.mark.parametrize(
    "inicio, fin",
    [
        (-1.0, 10.0),
        (10.0, 10.0),
        (20.0, 10.0),
        (0.0, float("inf")),
        (float("nan"), 10.0),
        (True, 10.0),
        (0.0, 5e-324),
    ],
)
def test_rechaza_intervalos_invalidos(inicio, fin):
    with pytest.raises(ValueError):
        IntervaloTemporal(inicio, fin)


def test_intervalo_inmutable():
    intervalo = IntervaloTemporal(0.0, 300.0)

    with pytest.raises(FrozenInstanceError):
        intervalo.fin_s = 600.0
