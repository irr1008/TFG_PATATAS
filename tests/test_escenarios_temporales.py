"""
Verificación de los escenarios temporales del diseño v0.2.
"""

from math import exp, fsum, isfinite

import pytest

from modelo_fisico.configuracion import (
    Capa,
    ConfiguracionPerfil,
    OpcionesProcesos,
)
from modelo_fisico.ejecutor import ejecutar_serie
from modelo_fisico.estados import EstadoPerfil
from modelo_fisico.eventos import EventoTasas


PASOS_S = (300.0, 150.0, 75.0, 37.5)
DURACION_S = 86400.0


@pytest.fixture(scope="module")
def ejecuciones():
    perfil = ConfiguracionPerfil(
        capas=(
            Capa(0.0, 0.2, 0.05, 0.25, 0.45, 6.0),
            Capa(0.2, 0.6, 0.05, 0.25, 0.45, 12.0),
        ),
        f_max_mm_h=12.0,
        procesos=OpcionesProcesos(
            infiltracion=True,
            transferencias=True,
            drenaje_inferior=True,
        ),
    )

    eventos = (
        EventoTasas(
            inicio_s=0.0,
            fin_s=7200.0,
            precipitacion_mm_h=0.0,
            riego_mm_h=6.0,
            extracciones_mm_h=(0.0, 0.0),
        ),
        EventoTasas(
            inicio_s=7200.0,
            fin_s=DURACION_S,
            precipitacion_mm_h=0.0,
            riego_mm_h=0.0,
            extracciones_mm_h=(0.05, 0.10),
        ),
    )

    resultados = {}

    for escenario, almacenamientos, programacion in (
        ("11.1", (40.0, 80.0), eventos),
        ("11.2", (74.0, 124.0), ()),
    ):
        for paso_s in PASOS_S:
            resultados[(escenario, paso_s)] = ejecutar_serie(
                EstadoPerfil(perfil, almacenamientos),
                DURACION_S,
                paso_s,
                eventos=programacion,
            )

    return resultados


def estados_por_tiempo(resultado):
    estados = {0.0: resultado.estado_inicial}

    for registro in resultado.registros:
        estados[registro.intervalo.fin_s] = (
            registro.resultado.estado_final
        )

    return estados


def comprobar_balance_y_limites(resultado):
    inicial = fsum(resultado.estado_inicial.almacenamientos_mm)
    final = fsum(resultado.estado_final.almacenamientos_mm)

    flujos = fsum((
        resultado.precipitacion_mm,
        resultado.riego_mm,
        -resultado.salida_superficial_mm,
        -resultado.drenaje_inferior_mm,
        -fsum(resultado.extracciones_mm),
    ))
    residual = final - inicial - flujos

    assert isfinite(residual)
    assert resultado.residual_global_mm == pytest.approx(
        residual, rel=0.0, abs=1e-12
    )
    assert abs(residual) <= resultado.tolerancia_global_mm

    residuales = tuple(
        registro.resultado.residual_masa_mm
        for registro in resultado.registros
    )
    assert resultado.suma_residuales_mm == pytest.approx(
        fsum(residuales), rel=0.0, abs=1e-12
    )
    assert resultado.suma_absoluta_residuales_mm == pytest.approx(
        fsum(abs(valor) for valor in residuales),
        rel=0.0,
        abs=1e-12,
    )

    for estado in estados_por_tiempo(resultado).values():
        for almacenamiento, capa in zip(
            estado.almacenamientos_mm,
            estado.configuracion.capas,
        ):
            minimo = 1000.0 * capa.espesor_m * capa.theta_min
            maximo = 1000.0 * capa.espesor_m * capa.theta_sat

            assert isfinite(almacenamiento)
            assert minimo - 1e-9 <= almacenamiento <= maximo + 1e-9


@pytest.mark.parametrize("paso_s", PASOS_S)
def test_escenario_11_1_acumulados_balance_y_limites(
    ejecuciones, paso_s
):
    resultado = ejecuciones[("11.1", paso_s)]

    assert len(resultado.registros) == int(DURACION_S / paso_s)
    assert resultado.registros[-1].intervalo.fin_s == DURACION_S

    assert resultado.precipitacion_mm == 0.0
    assert resultado.riego_mm == pytest.approx(
        12.0, rel=1e-12, abs=1e-12
    )
    assert resultado.infiltracion_mm == pytest.approx(
        12.0, rel=1e-12, abs=1e-12
    )
    assert resultado.extracciones_solicitadas_mm == pytest.approx(
        (1.1, 2.2), rel=1e-12, abs=1e-12
    )
    assert resultado.extracciones_mm == pytest.approx(
        (1.1, 2.2), rel=1e-12, abs=1e-12
    )
    assert resultado.demandas_no_satisfechas_mm == pytest.approx(
        (0.0, 0.0), rel=0.0, abs=1e-12
    )
    assert resultado.salida_superficial_mm == pytest.approx(
        0.0, rel=0.0, abs=1e-12
    )
    assert resultado.drenaje_inferior_mm == pytest.approx(
        0.0, rel=0.0, abs=1e-12
    )

    comprobar_balance_y_limites(resultado)


def test_escenario_11_1_criterios_75_y_37_5_s(ejecuciones):
    gruesa = ejecuciones[("11.1", 75.0)]
    fina = ejecuciones[("11.1", 37.5)]

    estados_gruesos = estados_por_tiempo(gruesa)
    estados_finos = estados_por_tiempo(fina)

    assert set(estados_gruesos).issubset(estados_finos)
    assert len(estados_gruesos) == 1153

    diferencias = []

    for tiempo, estado_grueso in estados_gruesos.items():
        estado_fino = estados_finos[tiempo]

        for j, capa in enumerate(
            estado_grueso.configuracion.capas
        ):
            diferencia_theta = abs(
                estado_grueso.almacenamientos_mm[j]
                - estado_fino.almacenamientos_mm[j]
            ) / (1000.0 * capa.espesor_m)

            diferencias.append(diferencia_theta)

    assert max(diferencias) <= 1e-4
    assert abs(
        gruesa.salida_superficial_mm
        - fina.salida_superficial_mm
    ) <= 0.01
    assert abs(
        gruesa.drenaje_inferior_mm
        - fina.drenaje_inferior_mm
    ) <= 0.01


def referencia_11_2(tiempo_s):
    tiempo_h = tiempo_s / 3600.0

    s1 = 50.0 + 24.0 * exp(-tiempo_h / 6.0)
    s2 = (
        100.0
        + 72.0 * exp(-tiempo_h / 12.0)
        - 48.0 * exp(-tiempo_h / 6.0)
    )

    return s1, s2, 198.0 - s1 - s2


@pytest.mark.parametrize("paso_s", PASOS_S)
def test_escenario_11_2_balance_limites_y_capa_superior(
    ejecuciones, paso_s
):
    resultado = ejecuciones[("11.2", paso_s)]

    comprobar_balance_y_limites(resultado)

    assert resultado.precipitacion_mm == 0.0
    assert resultado.riego_mm == 0.0
    assert resultado.extracciones_mm == (0.0, 0.0)
    assert resultado.drenaje_inferior_mm > 0.0

    for tiempo, estado in estados_por_tiempo(resultado).items():
        s1_exacta, _, _ = referencia_11_2(tiempo)

        assert estado.almacenamientos_mm[0] == pytest.approx(
            s1_exacta, rel=1e-12, abs=1e-12
        )


def test_escenario_11_2_error_disminuye_al_refinar(ejecuciones):
    errores_maximos_theta2 = []
    errores_finales_dp = []

    for paso_s in PASOS_S:
        resultado = ejecuciones[("11.2", paso_s)]
        errores_theta2 = []

        for tiempo, estado in estados_por_tiempo(
            resultado
        ).items():
            _, s2_exacta, _ = referencia_11_2(tiempo)
            espesor = estado.configuracion.capas[1].espesor_m

            errores_theta2.append(
                abs(estado.almacenamientos_mm[1] - s2_exacta)
                / (1000.0 * espesor)
            )

        _, _, dp_exacta = referencia_11_2(DURACION_S)

        errores_maximos_theta2.append(max(errores_theta2))
        errores_finales_dp.append(
            abs(resultado.drenaje_inferior_mm - dp_exacta)
        )

    for errores in (
        errores_maximos_theta2,
        errores_finales_dp,
    ):
        assert all(isfinite(error) for error in errores)
        assert all(
            fino < grueso
            for grueso, fino in zip(errores, errores[1:])
        )
