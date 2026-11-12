from math import exp

import pytest

from modelo_fisico.flujos import drenaje_potencial_mm


@pytest.mark.parametrize("almacenamiento_mm", [0.0, 40.0, 50.0])
def test_no_drena_sin_exceso_sobre_capacidad_de_campo(
    almacenamiento_mm,
):
    resultado = drenaje_potencial_mm(
        almacenamiento_mm,
        capacidad_campo_mm=50.0,
        dt_h=300.0 / 3600.0,
        tau_h=6.0,
    )

    assert resultado == 0.0


def test_referencia_analitica_del_caso_f():
    resultado = drenaje_potencial_mm(
        almacenamiento_mm=74.0,
        capacidad_campo_mm=50.0,
        dt_h=300.0 / 3600.0,
        tau_h=6.0,
    )

    esperado = 24.0 * (1.0 - exp(-1.0 / 72.0))

    assert resultado == pytest.approx(
        esperado, rel=1e-12, abs=1e-12
    )


def test_referencia_analitica_del_caso_g():
    resultado = drenaje_potencial_mm(
        almacenamiento_mm=124.0,
        capacidad_campo_mm=100.0,
        dt_h=300.0 / 3600.0,
        tau_h=12.0,
    )

    esperado = 24.0 * (1.0 - exp(-1.0 / 144.0))

    assert resultado == pytest.approx(
        esperado, rel=1e-12, abs=1e-12
    )


@pytest.mark.parametrize("dt_h", [1e-12, 1.0, 1000.0])
def test_drenaje_no_supera_el_exceso(dt_h):
    resultado = drenaje_potencial_mm(
        almacenamiento_mm=74.0,
        capacidad_campo_mm=50.0,
        dt_h=dt_h,
        tau_h=6.0,
    )

    assert 0.0 <= resultado <= 24.0


def test_intervalo_pequeno_conserva_un_drenaje_positivo():
    resultado = drenaje_potencial_mm(
        almacenamiento_mm=74.0,
        capacidad_campo_mm=50.0,
        dt_h=1e-16,
        tau_h=6.0,
    )

    referencia_lineal = 24.0 * (1e-16 / 6.0)

    assert resultado > 0.0
    assert resultado == pytest.approx(
        referencia_lineal, rel=1e-12, abs=0.0
    )


@pytest.mark.parametrize(
    "campo",
    [
        "almacenamiento_mm",
        "capacidad_campo_mm",
        "dt_h",
        "tau_h",
    ],
)
@pytest.mark.parametrize(
    "valor",
    [float("nan"), float("inf"), float("-inf"), True, "1", None],
)
def test_rechaza_argumentos_no_admitidos(campo, valor):
    argumentos = {
        "almacenamiento_mm": 74.0,
        "capacidad_campo_mm": 50.0,
        "dt_h": 300.0 / 3600.0,
        "tau_h": 6.0,
    }
    argumentos[campo] = valor

    with pytest.raises(ValueError):
        drenaje_potencial_mm(**argumentos)


@pytest.mark.parametrize(
    ("campo", "valor"),
    [
        ("almacenamiento_mm", -1.0),
        ("capacidad_campo_mm", -1.0),
        ("dt_h", 0.0),
        ("dt_h", -1.0),
        ("tau_h", 0.0),
        ("tau_h", -1.0),
    ],
)
def test_rechaza_argumentos_fuera_de_rango(campo, valor):
    argumentos = {
        "almacenamiento_mm": 74.0,
        "capacidad_campo_mm": 50.0,
        "dt_h": 300.0 / 3600.0,
        "tau_h": 6.0,
    }
    argumentos[campo] = valor

    with pytest.raises(ValueError):
        drenaje_potencial_mm(**argumentos)
