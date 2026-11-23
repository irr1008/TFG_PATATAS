from dataclasses import FrozenInstanceError, replace
from math import fsum

import pytest

from modelo_fisico.configuracion import (
    Capa,
    ConfiguracionPerfil,
    OpcionesProcesos,
)
from modelo_fisico.entradas import EntradasPaso
from modelo_fisico.estados import EstadoPerfil
from modelo_fisico.extraccion import (
    aplicar_extraccion,
    extraccion_efectiva_mm,
)


def crear_perfil():
    return ConfiguracionPerfil(
        capas=(
            Capa(0.0, 0.2, 0.05, 0.25, 0.45, 6.0),
            Capa(0.2, 0.6, 0.05, 0.25, 0.45, 12.0),
        ),
        f_max_mm_h=12.0,
        procesos=OpcionesProcesos(
            infiltracion=False,
            transferencias=False,
            drenaje_inferior=False,
        ),
    )


def crear_entradas(perfil, demandas):
    return EntradasPaso(
        configuracion=perfil,
        dt_s=300.0,
        precipitacion_mm=0.0,
        riego_mm=0.0,
        extracciones_solicitadas_mm=demandas,
    )


def comprobar_balance(estado, resultado):
    residual = fsum(
        (
            fsum(resultado.estado_final.almacenamientos_mm),
            -fsum(estado.almacenamientos_mm),
            fsum(resultado.extracciones_mm),
        )
    )

    assert residual == pytest.approx(
        0.0, rel=0.0, abs=resultado.tolerancia_masa_mm
    )
    assert resultado.residual_masa_mm == pytest.approx(
        residual, rel=0.0, abs=1e-12
    )


def test_caso_h_extraccion_limitada():
    perfil = crear_perfil()
    estado = EstadoPerfil(perfil, (10.5, 20.0))
    entradas = crear_entradas(perfil, (2.0, 0.0))

    resultado = aplicar_extraccion(estado, entradas)

    assert resultado.extracciones_mm == pytest.approx((0.5, 0.0))
    assert resultado.demandas_no_satisfechas_mm == pytest.approx(
        (1.5, 0.0)
    )
    assert resultado.estado_final.almacenamientos_mm == pytest.approx(
        (10.0, 20.0), rel=1e-12, abs=1e-12
    )
    comprobar_balance(estado, resultado)


def test_demanda_cubierta_completamente():
    perfil = crear_perfil()
    estado = EstadoPerfil(perfil, (40.0, 80.0))
    entradas = crear_entradas(perfil, (2.0, 3.0))

    resultado = aplicar_extraccion(estado, entradas)

    assert resultado.extracciones_mm == (2.0, 3.0)
    assert resultado.demandas_no_satisfechas_mm == (0.0, 0.0)
    assert resultado.estado_final.almacenamientos_mm == (38.0, 77.0)
    comprobar_balance(estado, resultado)


def test_sin_demanda_no_modifica_el_estado():
    perfil = crear_perfil()
    estado = EstadoPerfil(perfil, (40.0, 80.0))
    entradas = crear_entradas(perfil, (0.0, 0.0))

    resultado = aplicar_extraccion(estado, entradas)

    assert resultado.extracciones_mm == (0.0, 0.0)
    assert resultado.demandas_no_satisfechas_mm == (0.0, 0.0)
    assert (
        resultado.estado_final.almacenamientos_mm
        == estado.almacenamientos_mm
    )
    comprobar_balance(estado, resultado)


def test_capa_en_el_minimo_no_aporta_agua():
    perfil = crear_perfil()
    estado = EstadoPerfil(perfil, (10.0, 20.0))
    entradas = crear_entradas(perfil, (1.0, 2.0))

    resultado = aplicar_extraccion(estado, entradas)

    assert resultado.extracciones_mm == (0.0, 0.0)
    assert resultado.demandas_no_satisfechas_mm == (1.0, 2.0)
    assert (
        resultado.estado_final.almacenamientos_mm
        == estado.almacenamientos_mm
    )
    comprobar_balance(estado, resultado)


def test_la_demanda_no_satisfecha_no_pasa_a_otra_capa():
    perfil = crear_perfil()
    estado = EstadoPerfil(perfil, (10.5, 80.0))
    entradas = crear_entradas(perfil, (2.0, 0.0))

    resultado = aplicar_extraccion(estado, entradas)

    assert resultado.extracciones_mm == pytest.approx((0.5, 0.0))
    assert resultado.estado_final.almacenamientos_mm == pytest.approx(
        (10.0, 80.0), rel=1e-12, abs=1e-12
    )
    comprobar_balance(estado, resultado)


def test_extrae_cada_capa_con_su_propio_limite():
    perfil = crear_perfil()
    estado = EstadoPerfil(perfil, (10.5, 21.0))
    entradas = crear_entradas(perfil, (2.0, 0.4))

    resultado = aplicar_extraccion(estado, entradas)

    assert resultado.extracciones_mm == pytest.approx((0.5, 0.4))
    assert resultado.demandas_no_satisfechas_mm == pytest.approx(
        (1.5, 0.0)
    )
    comprobar_balance(estado, resultado)


@pytest.mark.parametrize("numero_capas", [1, 3])
def test_admite_una_y_mas_de_dos_capas(numero_capas):
    perfil = ConfiguracionPerfil(
        capas=tuple(
            Capa(i * 0.25, (i + 1) * 0.25, 0.0, 0.2, 0.4)
            for i in range(numero_capas)
        ),
        f_max_mm_h=12.0,
        procesos=OpcionesProcesos(
            infiltracion=False,
            transferencias=False,
            drenaje_inferior=False,
        ),
    )
    estado = EstadoPerfil(perfil, (40.0,) * numero_capas)
    entradas = crear_entradas(perfil, (1.0,) * numero_capas)

    resultado = aplicar_extraccion(estado, entradas)

    assert resultado.estado_final.almacenamientos_mm == (
        (39.0,) * numero_capas
    )
    assert len(resultado.extracciones_mm) == numero_capas
    assert resultado.demandas_no_satisfechas_mm == (0.0,) * numero_capas
    comprobar_balance(estado, resultado)


def test_no_aplica_aportes_de_las_entradas():
    perfil = crear_perfil()
    estado = EstadoPerfil(perfil, (40.0, 80.0))
    entradas = replace(
        crear_entradas(perfil, (1.0, 0.0)),
        precipitacion_mm=5.0,
        riego_mm=2.0,
    )

    resultado = aplicar_extraccion(estado, entradas)

    assert resultado.estado_final.almacenamientos_mm == (39.0, 80.0)


def test_no_modifica_objetos_y_resultado_es_inmutable():
    perfil = crear_perfil()
    estado = EstadoPerfil(perfil, (40.0, 80.0))
    entradas = crear_entradas(perfil, (2.0, 3.0))

    resultado = aplicar_extraccion(estado, entradas)

    assert estado.almacenamientos_mm == (40.0, 80.0)
    assert entradas.extracciones_solicitadas_mm == (2.0, 3.0)
    assert resultado.estado_final is not estado

    with pytest.raises(FrozenInstanceError):
        resultado.extracciones_mm = (0.0, 0.0)


@pytest.mark.parametrize(
    ("demanda", "almacenamiento", "minimo", "esperado"),
    [
        (2.0, 10.5, 10.0, (0.5, 1.5)),
        (0.3, 10.5, 10.0, (0.3, 0.0)),
        (1.0, 10.0, 10.0, (0.0, 1.0)),
        (0.0, 40.0, 10.0, (0.0, 0.0)),
    ],
)
def test_funcion_de_extraccion_efectiva(
    demanda, almacenamiento, minimo, esperado
):
    assert extraccion_efectiva_mm(
        demanda, almacenamiento, minimo
    ) == pytest.approx(esperado, rel=1e-12, abs=1e-12)


@pytest.mark.parametrize(
    "argumentos",
    [
        (-0.1, 40.0, 10.0),
        (float("nan"), 40.0, 10.0),
        (float("inf"), 40.0, 10.0),
        (True, 40.0, 10.0),
        (None, 40.0, 10.0),
        (1.0, -1.0, 10.0),
        (1.0, 40.0, float("nan")),
        (1.0, 40.0, -1.0),
    ],
)
def test_funcion_de_extraccion_rechaza_argumentos_invalidos(argumentos):
    with pytest.raises(ValueError):
        extraccion_efectiva_mm(*argumentos)


def test_rechaza_configuraciones_distintas():
    perfil = crear_perfil()
    otro_perfil = replace(perfil, f_max_mm_h=6.0)
    estado = EstadoPerfil(perfil, (40.0, 80.0))
    entradas = crear_entradas(otro_perfil, (0.0, 0.0))

    with pytest.raises(ValueError):
        aplicar_extraccion(estado, entradas)


def test_rechaza_estado_de_tipo_incorrecto():
    entradas = crear_entradas(crear_perfil(), (0.0, 0.0))

    with pytest.raises(ValueError):
        aplicar_extraccion(None, entradas)


def test_rechaza_entradas_de_tipo_incorrecto():
    estado = EstadoPerfil(crear_perfil(), (40.0, 80.0))

    with pytest.raises(ValueError):
        aplicar_extraccion(estado, None)
