"""
Pruebas de conversiones y rechazo de argumentos inválidos.
"""

import pytest

from modelo_fisico.conversiones import (
    almacenamiento_a_humedad,
    humedad_a_almacenamiento,
)


@pytest.mark.parametrize(
    "theta,espesor,esperado",
    [
        (0.20, 0.20, 40.0),
        (0.20, 0.40, 80.0),
        (0.05, 0.20, 10.0),
        (0.25, 0.40, 100.0),
        (0.45, 0.20, 90.0),
        (0.0, 0.20, 0.0),
        (1.0, 0.20, 200.0),
    ],
)
def test_humedad_a_almacenamiento(theta, espesor, esperado):
    resultado = humedad_a_almacenamiento(theta, espesor)
    assert resultado == pytest.approx(
        esperado, rel=1e-12, abs=1e-12
    )


@pytest.mark.parametrize(
    "almacenamiento,espesor,esperado",
    [
        (40.0, 0.20, 0.20),
        (80.0, 0.40, 0.20),
        (10.0, 0.20, 0.05),
        (100.0, 0.40, 0.25),
        (90.0, 0.20, 0.45),
        (0.0, 0.20, 0.0),
        (200.0, 0.20, 1.0),
    ],
)
def test_almacenamiento_a_humedad(almacenamiento, espesor, esperado):
    resultado = almacenamiento_a_humedad(almacenamiento, espesor)
    assert resultado == pytest.approx(
        esperado, rel=1e-12, abs=1e-12
    )


@pytest.mark.parametrize("theta", [0.0, 0.05, 0.20, 0.45, 1.0])
@pytest.mark.parametrize("espesor", [0.10, 0.20, 0.40])
def test_conversion_de_ida_y_vuelta(theta, espesor):
    almacenamiento = humedad_a_almacenamiento(theta, espesor)
    recuperada = almacenamiento_a_humedad(almacenamiento, espesor)

    assert recuperada == pytest.approx(
        theta, rel=1e-12, abs=1e-12
    )


@pytest.mark.parametrize(
    "funcion,valor",
    [
        (humedad_a_almacenamiento, 0.20),
        (almacenamiento_a_humedad, 40.0),
    ],
)
@pytest.mark.parametrize(
    "espesor",
    [0.0, -0.2, float("nan"), float("inf"), "0.2", True],
)
def test_rechaza_espesores_invalidos(funcion, valor, espesor):
    with pytest.raises(ValueError):
        funcion(valor, espesor)


@pytest.mark.parametrize(
    "theta",
    [-0.01, 1.01, float("nan"), float("inf"), "0.2", True],
)
def test_rechaza_humedades_invalidas(theta):
    with pytest.raises(ValueError):
        humedad_a_almacenamiento(theta, 0.20)


@pytest.mark.parametrize(
    "almacenamiento",
    [-0.01, 200.01, float("nan"), float("inf"), "40", True],
)
def test_rechaza_almacenamientos_invalidos(almacenamiento):
    with pytest.raises(ValueError):
        almacenamiento_a_humedad(almacenamiento, 0.20)


@pytest.mark.parametrize(
    "funcion,valor",
    [
        (humedad_a_almacenamiento, 0.20),
        (almacenamiento_a_humedad, 40.0),
    ],
)
def test_rechaza_factor_de_conversion_no_finito(funcion, valor):
    with pytest.raises(ValueError):
        funcion(valor, 1e308)
