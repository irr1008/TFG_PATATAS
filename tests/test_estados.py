"""
Pruebas de estados, dimensiones y tolerancias explícitas.
"""

from dataclasses import FrozenInstanceError

import pytest

from modelo_fisico.configuracion import Capa, ConfiguracionPerfil
from modelo_fisico.estados import (
    EstadoPerfil,
    TOLERANCIA_ESTADO_MM,
    comprobar_almacenamientos,
)


@pytest.fixture
def perfil():
    return ConfiguracionPerfil(
        capas=(
            Capa(0.0, 0.2, 0.05, 0.25, 0.45, 6.0),
            Capa(0.2, 0.6, 0.05, 0.25, 0.45, 12.0),
        ),
        f_max_mm_h=12.0,
    )


def test_estado_base_y_conversiones(perfil):
    estado = EstadoPerfil(perfil, (40.0, 80.0))

    assert estado.almacenamientos_mm == (40.0, 80.0)
    assert estado.humedades == pytest.approx(
        (0.20, 0.20), rel=1e-12, abs=1e-12
    )
    assert estado.almacenamiento_total_mm == pytest.approx(120.0)


@pytest.mark.parametrize("numero", [1, 2, 4])
def test_estado_admite_distintos_numeros_de_capas(numero):
    limites = tuple(indice * 0.2 for indice in range(numero + 1))
    capas = tuple(
        Capa(
            limites[indice],
            limites[indice + 1],
            0.05,
            0.25,
            0.45,
            6.0,
        )
        for indice in range(numero)
    )
    configuracion = ConfiguracionPerfil(capas, 12.0)
    almacenamientos = tuple(
        1000.0 * capa.espesor_m * 0.20
        for capa in capas
    )

    estado = EstadoPerfil(configuracion, almacenamientos)

    assert len(estado.humedades) == numero
    assert estado.humedades == pytest.approx((0.20,) * numero)


@pytest.mark.parametrize("atributo", ["theta_min", "theta_sat"])
def test_admite_limites_exactos(perfil, atributo):
    almacenamientos = tuple(
        1000.0 * capa.espesor_m * getattr(capa, atributo)
        for capa in perfil.capas
    )

    estado = EstadoPerfil(perfil, almacenamientos)

    assert estado.almacenamientos_mm == almacenamientos


@pytest.mark.parametrize(
    "almacenamientos",
    [
        (),
        (40.0,),
        (40.0, 80.0, 40.0),
        [40.0, 80.0],
        None,
    ],
)
def test_rechaza_dimensiones_o_contenedor_invalidos(
    perfil, almacenamientos
):
    with pytest.raises(ValueError):
        EstadoPerfil(perfil, almacenamientos)


@pytest.mark.parametrize(
    "valor",
    [float("nan"), float("inf"), float("-inf"), "40", True, None],
)
def test_rechaza_valores_invalidos(perfil, valor):
    with pytest.raises(ValueError):
        EstadoPerfil(perfil, (valor, 80.0))


@pytest.mark.parametrize(
    "almacenamientos",
    [
        (9.0, 80.0),
        (91.0, 80.0),
        (40.0, 19.0),
        (40.0, 181.0),
    ],
)
def test_rechaza_estados_fuera_de_rango(perfil, almacenamientos):
    with pytest.raises(ValueError):
        EstadoPerfil(perfil, almacenamientos)


def test_constructor_no_admite_desviacion_pequena(perfil):
    almacenamientos = (10.0 - 0.5 * TOLERANCIA_ESTADO_MM, 80.0)

    with pytest.raises(ValueError):
        EstadoPerfil(perfil, almacenamientos)


@pytest.mark.parametrize("limite", ["inferior", "superior"])
def test_tolerancia_explicita_no_modifica_valores(perfil, limite):
    if limite == "inferior":
        valor = 10.0 - 0.5 * TOLERANCIA_ESTADO_MM
    else:
        valor = 90.0 + 0.5 * TOLERANCIA_ESTADO_MM

    almacenamientos = (valor, 80.0)

    comprobar_almacenamientos(
        perfil,
        almacenamientos,
        tolerancia_mm=TOLERANCIA_ESTADO_MM,
    )

    assert almacenamientos == (valor, 80.0)


@pytest.mark.parametrize("limite", ["inferior", "superior"])
def test_rechaza_desviacion_superior_a_tolerancia(perfil, limite):
    if limite == "inferior":
        valor = 10.0 - 2.0 * TOLERANCIA_ESTADO_MM
    else:
        valor = 90.0 + 2.0 * TOLERANCIA_ESTADO_MM

    with pytest.raises(ValueError):
        comprobar_almacenamientos(
            perfil,
            (valor, 80.0),
            tolerancia_mm=TOLERANCIA_ESTADO_MM,
        )


@pytest.mark.parametrize(
    "tolerancia",
    [-1.0, float("nan"), float("inf"), True, "0.001"],
)
def test_rechaza_tolerancia_invalida(perfil, tolerancia):
    with pytest.raises(ValueError):
        comprobar_almacenamientos(
            perfil, (40.0, 80.0), tolerancia_mm=tolerancia
        )


def test_rechaza_configuracion_invalida():
    with pytest.raises(ValueError):
        EstadoPerfil(None, (40.0,))


def test_estado_no_permite_reasignacion(perfil):
    estado = EstadoPerfil(perfil, (40.0, 80.0))

    with pytest.raises(FrozenInstanceError):
        estado.almacenamientos_mm = (41.0, 80.0)
