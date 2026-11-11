"""
Pruebas de las entradas prescritas de un intervalo.
"""

from dataclasses import FrozenInstanceError

import pytest

from modelo_fisico.configuracion import (
    Capa,
    ConfiguracionPerfil,
    OpcionesProcesos,
)
from modelo_fisico.entradas import EntradasPaso


@pytest.fixture
def perfil():
    return ConfiguracionPerfil(
        capas=(
            Capa(0.0, 0.2, 0.05, 0.25, 0.45, 6.0),
            Capa(0.2, 0.6, 0.05, 0.25, 0.45, 12.0),
        ),
        f_max_mm_h=12.0,
    )


def crear_entradas(perfil, **cambios):
    parametros = {
        "configuracion": perfil,
        "dt_s": 300.0,
        "precipitacion_mm": 0.5,
        "riego_mm": 1.0,
        "extracciones_solicitadas_mm": (0.1, 0.2),
    }
    parametros.update(cambios)
    return EntradasPaso(**parametros)


def test_entradas_validas_y_duracion_en_horas(perfil):
    entradas = crear_entradas(perfil)

    assert entradas.dt_h == pytest.approx(1.0 / 12.0)
    assert entradas.precipitacion_mm == 0.5
    assert entradas.riego_mm == 1.0
    assert entradas.extracciones_solicitadas_mm == (0.1, 0.2)


def test_admite_ceros_explicitos(perfil):
    entradas = crear_entradas(
        perfil,
        precipitacion_mm=0.0,
        riego_mm=0.0,
        extracciones_solicitadas_mm=(0.0, 0.0),
    )

    assert entradas.precipitacion_mm == 0.0
    assert entradas.riego_mm == 0.0
    assert entradas.extracciones_solicitadas_mm == (0.0, 0.0)


@pytest.mark.parametrize("numero", [1, 2, 4])
def test_admite_una_demanda_por_capa(numero):
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

    entradas = EntradasPaso(
        configuracion=configuracion,
        dt_s=300.0,
        precipitacion_mm=0.0,
        riego_mm=0.0,
        extracciones_solicitadas_mm=(0.1,) * numero,
    )

    assert len(entradas.extracciones_solicitadas_mm) == numero


@pytest.mark.parametrize(
    "duracion",
    [
        0.0,
        -300.0,
        float("nan"),
        float("inf"),
        float("-inf"),
        "300",
        True,
        None,
        5e-324,
    ],
)
def test_rechaza_duracion_invalida(perfil, duracion):
    with pytest.raises(ValueError):
        crear_entradas(perfil, dt_s=duracion)


@pytest.mark.parametrize("duracion", [37.5, 300.0, 3600.0])
def test_convertir_duracion_no_modifica_acumulados(perfil, duracion):
    entradas = crear_entradas(perfil, dt_s=duracion)

    assert entradas.dt_h == pytest.approx(duracion / 3600.0)
    assert entradas.precipitacion_mm == 0.5
    assert entradas.riego_mm == 1.0
    assert entradas.extracciones_solicitadas_mm == (0.1, 0.2)


@pytest.mark.parametrize("campo", ["precipitacion_mm", "riego_mm"])
@pytest.mark.parametrize(
    "valor",
    [-0.1, float("nan"), float("inf"), float("-inf"), "1", True, None],
)
def test_rechaza_aportes_invalidos(perfil, campo, valor):
    with pytest.raises(ValueError):
        crear_entradas(perfil, **{campo: valor})


@pytest.mark.parametrize(
    "demandas",
    [
        (),
        (0.1,),
        (0.1, 0.2, 0.3),
        [0.1, 0.2],
        None,
    ],
)
def test_rechaza_dimensiones_o_contenedor_invalidos(perfil, demandas):
    with pytest.raises(ValueError):
        crear_entradas(
            perfil,
            extracciones_solicitadas_mm=demandas,
        )


@pytest.mark.parametrize("indice", [0, 1])
@pytest.mark.parametrize(
    "valor",
    [-0.1, float("nan"), float("inf"), float("-inf"), "1", True, None],
)
def test_rechaza_demanda_invalida_en_cualquier_capa(
    perfil, indice, valor
):
    demandas = [0.1, 0.2]
    demandas[indice] = valor

    with pytest.raises(ValueError):
        crear_entradas(
            perfil,
            extracciones_solicitadas_mm=tuple(demandas),
        )


def test_demanda_no_se_limita_al_almacenamiento(perfil):
    entradas = crear_entradas(
        perfil,
        extracciones_solicitadas_mm=(1000.0, 2000.0),
    )

    assert entradas.extracciones_solicitadas_mm == (1000.0, 2000.0)


def test_procesos_desactivados_no_borran_entradas(perfil):
    configuracion = ConfiguracionPerfil(
        capas=perfil.capas,
        f_max_mm_h=12.0,
        procesos=OpcionesProcesos(
            infiltracion=False,
            transferencias=False,
            drenaje_inferior=False,
        ),
    )

    entradas = crear_entradas(configuracion)

    assert entradas.precipitacion_mm == 0.5
    assert entradas.riego_mm == 1.0
    assert entradas.extracciones_solicitadas_mm == (0.1, 0.2)


def test_rechaza_configuracion_invalida(perfil):
    with pytest.raises(ValueError):
        crear_entradas(perfil, configuracion=None)


def test_campos_obligatorios_no_se_rellenan_con_ceros(perfil):
    with pytest.raises(TypeError):
        EntradasPaso(configuracion=perfil, dt_s=300.0)


def test_entradas_no_permiten_reasignacion(perfil):
    entradas = crear_entradas(perfil)

    with pytest.raises(FrozenInstanceError):
        entradas.riego_mm = 2.0
