from dataclasses import FrozenInstanceError, replace
from math import exp, fsum

import pytest

import modelo_fisico.ejecutor as modulo_ejecutor
from modelo_fisico.configuracion import (
    Capa,
    ConfiguracionPerfil,
    OpcionesProcesos,
)
from modelo_fisico.ejecutor import ejecutar_serie
from modelo_fisico.estados import EstadoPerfil
from modelo_fisico.eventos import EventoTasas
from modelo_fisico.paso import ejecutar_paso


def crear_estado(
    almacenamientos=(40.0, 80.0),
    *,
    infiltracion=True,
    transferencias=False,
    drenaje_inferior=False,
):
    perfil = ConfiguracionPerfil(
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
    return EstadoPerfil(perfil, almacenamientos)


def crear_evento(
    inicio=0.0,
    fin=3600.0,
    *,
    precipitacion=0.0,
    riego=6.0,
    demandas=(0.0, 0.0),
):
    return EventoTasas(
        inicio_s=inicio,
        fin_s=fin,
        precipitacion_mm_h=precipitacion,
        riego_mm_h=riego,
        extracciones_mm_h=demandas,
    )


def comprobar_balance(resultado):
    delta = (
        fsum(resultado.estado_final.almacenamientos_mm)
        - fsum(resultado.estado_inicial.almacenamientos_mm)
    )
    balance = fsum(
        (
            resultado.precipitacion_mm,
            resultado.riego_mm,
            -resultado.salida_superficial_mm,
            -resultado.drenaje_inferior_mm,
            -fsum(resultado.extracciones_mm),
        )
    )
    assert resultado.residual_global_mm == pytest.approx(
        delta - balance, rel=0.0, abs=1e-12
    )
    assert abs(resultado.residual_global_mm) <= (
        resultado.tolerancia_global_mm
    )

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

    for solicitada, efectiva, pendiente in zip(
        resultado.extracciones_solicitadas_mm,
        resultado.extracciones_mm,
        resultado.demandas_no_satisfechas_mm,
    ):
        assert solicitada == pytest.approx(
            efectiva + pendiente, rel=1e-12, abs=1e-12
        )


def test_reposo_y_ultimo_intervalo_corto():
    estado = crear_estado()
    resultado = ejecutar_serie(
        estado, 650.0, 300.0, eventos=()
    )

    assert tuple(
        registro.intervalo.dt_s
        for registro in resultado.registros
    ) == (300.0, 300.0, 50.0)
    assert resultado.estado_final.almacenamientos_mm == (
        40.0, 80.0
    )
    assert resultado.precipitacion_mm == 0.0
    assert resultado.riego_mm == 0.0
    assert resultado.tolerancia_global_mm == pytest.approx(
        3e-9 + 1e-12 * 120.0, rel=1e-12, abs=1e-18
    )
    comprobar_balance(resultado)


def test_riego_constante_y_encadenamiento_de_estados():
    estado = crear_estado()
    resultado = ejecutar_serie(
        estado,
        3600.0,
        300.0,
        eventos=(crear_evento(),),
    )

    assert resultado.riego_mm == pytest.approx(6.0)
    assert resultado.infiltracion_mm == pytest.approx(6.0)
    assert resultado.salida_superficial_mm == 0.0
    assert resultado.estado_final.almacenamientos_mm == (
        pytest.approx(46.0), pytest.approx(80.0)
    )

    anterior = estado
    for registro in resultado.registros:
        assert registro.estado_inicial is anterior
        esperado = ejecutar_paso(anterior, registro.entradas)
        assert registro.resultado == esperado
        anterior = registro.resultado.estado_final

    assert resultado.estado_final is anterior
    comprobar_balance(resultado)


def test_divide_cambios_no_alineados_sin_desplazar_malla():
    resultado = ejecutar_serie(
        crear_estado(),
        1000.0,
        300.0,
        eventos=(crear_evento(125.0, 725.0),),
    )

    assert tuple(
        (r.intervalo.inicio_s, r.intervalo.fin_s)
        for r in resultado.registros
    ) == (
        (0.0, 125.0),
        (125.0, 300.0),
        (300.0, 600.0),
        (600.0, 725.0),
        (725.0, 900.0),
        (900.0, 1000.0),
    )
    assert resultado.riego_mm == pytest.approx(1.0)
    assert resultado.estado_final.almacenamientos_mm == (
        pytest.approx(41.0), pytest.approx(80.0)
    )
    comprobar_balance(resultado)


@pytest.mark.parametrize("paso_s", [300.0, 150.0, 75.0, 37.5])
def test_aporte_no_alineado_con_distintos_pasos(paso_s):
    resultado = ejecutar_serie(
        crear_estado(),
        1000.0,
        paso_s,
        eventos=(crear_evento(125.0, 725.0),),
    )

    assert resultado.riego_mm == pytest.approx(
        1.0, rel=1e-12, abs=1e-12
    )
    assert resultado.estado_final.almacenamientos_mm == (
        pytest.approx(41.0), pytest.approx(80.0)
    )
    comprobar_balance(resultado)


def test_eventos_solapados_y_salida_por_capacidad_de_entrada():
    resultado = ejecutar_serie(
        crear_estado(),
        600.0,
        300.0,
        eventos=(
            crear_evento(0.0, 600.0, riego=12.0),
            crear_evento(
                0.0, 600.0, precipitacion=6.0, riego=0.0
            ),
        ),
    )

    assert resultado.precipitacion_mm == pytest.approx(1.0)
    assert resultado.riego_mm == pytest.approx(2.0)
    assert resultado.infiltracion_mm == pytest.approx(2.0)
    assert resultado.salida_superficial_mm == pytest.approx(1.0)
    assert resultado.estado_final.almacenamientos_mm == (
        pytest.approx(42.0), pytest.approx(80.0)
    )
    comprobar_balance(resultado)


def test_extraccion_limitada_y_demanda_no_satisfecha():
    resultado = ejecutar_serie(
        crear_estado((10.5, 20.0)),
        3600.0,
        300.0,
        eventos=(
            crear_evento(
                riego=0.0,
                demandas=(2.0, 1.0),
            ),
        ),
    )

    assert resultado.extracciones_solicitadas_mm == pytest.approx(
        (2.0, 1.0)
    )
    assert resultado.extracciones_mm == pytest.approx((0.5, 0.0))
    assert resultado.demandas_no_satisfechas_mm == pytest.approx(
        (1.5, 1.0)
    )
    assert resultado.estado_final.almacenamientos_mm == (
        pytest.approx(10.0), pytest.approx(20.0)
    )
    comprobar_balance(resultado)


def test_infiltracion_desactivada_contabiliza_salida():
    resultado = ejecutar_serie(
        crear_estado(infiltracion=False),
        3600.0,
        300.0,
        eventos=(crear_evento(),),
    )

    assert resultado.infiltracion_mm == 0.0
    assert resultado.salida_superficial_mm == pytest.approx(6.0)
    assert resultado.estado_final.almacenamientos_mm == (
        40.0, 80.0
    )
    comprobar_balance(resultado)


def test_drenaje_inferior_aislado_con_referencia_analitica():
    resultado = ejecutar_serie(
        crear_estado(
            (40.0, 124.0),
            infiltracion=False,
            drenaje_inferior=True,
        ),
        3600.0,
        300.0,
        eventos=(),
    )

    esperado = 100.0 + 24.0 * exp(-1.0 / 12.0)

    assert resultado.estado_final.almacenamientos_mm[1] == (
        pytest.approx(esperado, rel=1e-12, abs=1e-12)
    )
    assert resultado.drenaje_inferior_mm == pytest.approx(
        124.0 - esperado, rel=1e-12, abs=1e-12
    )
    comprobar_balance(resultado)


def test_transferencias_no_se_cuentan_como_salida_global():
    resultado = ejecutar_serie(
        crear_estado(
            (74.0, 80.0),
            infiltracion=False,
            transferencias=True,
        ),
        3600.0,
        300.0,
        eventos=(),
    )

    transferido = 24.0 * (1.0 - exp(-1.0 / 6.0))

    assert resultado.transferencias_mm == pytest.approx(
        (transferido,), rel=1e-12, abs=1e-12
    )
    assert resultado.estado_final.almacenamientos_mm == (
        pytest.approx(74.0 - transferido),
        pytest.approx(80.0 + transferido),
    )
    assert resultado.drenaje_inferior_mm == 0.0
    comprobar_balance(resultado)


@pytest.mark.parametrize("numero_capas", [1, 3])
def test_admite_distintos_numeros_de_capas(numero_capas):
    perfil = ConfiguracionPerfil(
        capas=tuple(
            Capa(i * 0.25, (i + 1) * 0.25, 0.0, 0.2, 0.4, 6.0)
            for i in range(numero_capas)
        ),
        f_max_mm_h=12.0,
    )
    estado = EstadoPerfil(perfil, (60.0,) * numero_capas)

    resultado = ejecutar_serie(
        estado, 600.0, 300.0, eventos=()
    )

    assert len(resultado.transferencias_mm) == numero_capas - 1
    assert len(resultado.extracciones_mm) == numero_capas
    comprobar_balance(resultado)


def test_eventos_que_superan_el_horizonte_se_integran_por_solape():
    resultado = ejecutar_serie(
        crear_estado(),
        600.0,
        300.0,
        eventos=(
            crear_evento(300.0, 900.0),
            crear_evento(900.0, 1200.0),
        ),
    )

    assert resultado.riego_mm == pytest.approx(0.5)
    assert len(resultado.registros) == 2
    comprobar_balance(resultado)


@pytest.mark.parametrize("eventos", [None, [], (None,)])
def test_rechaza_programacion_invalida(eventos):
    with pytest.raises(ValueError):
        ejecutar_serie(
            crear_estado(), 600.0, 300.0, eventos=eventos
        )


def test_valida_eventos_sin_solape_antes_del_primer_paso(monkeypatch):
    llamadas = []

    def paso_no_esperado(*args):
        llamadas.append(args)
        raise AssertionError("No debe ejecutarse ningún paso.")

    monkeypatch.setattr(
        modulo_ejecutor, "ejecutar_paso", paso_no_esperado
    )

    evento = crear_evento(
        900.0, 1200.0, demandas=(0.0,)
    )

    with pytest.raises(ValueError):
        ejecutar_serie(
            crear_estado(), 600.0, 300.0, eventos=(evento,)
        )

    assert llamadas == []


@pytest.mark.parametrize(
    "duracion,paso",
    [
        (0.0, 300.0),
        (-1.0, 300.0),
        (float("nan"), 300.0),
        (float("inf"), 300.0),
        (True, 300.0),
        ("600", 300.0),
        (600.0, 0.0),
        (600.0, -1.0),
        (600.0, float("nan")),
        (600.0, float("inf")),
        (600.0, True),
        (600.0, "300"),
    ],
)
def test_rechaza_tiempos_invalidos(duracion, paso):
    with pytest.raises(ValueError):
        ejecutar_serie(
            crear_estado(), duracion, paso, eventos=()
        )


def test_rechaza_estado_invalido():
    with pytest.raises(ValueError):
        ejecutar_serie(None, 600.0, 300.0, eventos=())


def test_balance_global_no_se_obtiene_sumando_residuales(monkeypatch):
    paso_real = modulo_ejecutor.ejecutar_paso
    residuales = iter((1e-10, -2e-10))

    def paso_con_diagnostico_modificado(estado, entradas):
        resultado = paso_real(estado, entradas)
        return replace(
            resultado,
            residual_masa_mm=next(residuales),
        )

    monkeypatch.setattr(
        modulo_ejecutor,
        "ejecutar_paso",
        paso_con_diagnostico_modificado,
    )

    resultado = ejecutar_serie(
        crear_estado(), 600.0, 300.0, eventos=()
    )

    assert resultado.residual_global_mm == 0.0
    assert resultado.suma_residuales_mm == pytest.approx(
        -1e-10, rel=0.0, abs=1e-20
    )
    assert resultado.suma_absoluta_residuales_mm == pytest.approx(
        3e-10, rel=0.0, abs=1e-20
    )


def test_rechaza_balance_global_incorrecto(monkeypatch):
    paso_real = modulo_ejecutor.ejecutar_paso

    def paso_con_flujo_incorrecto(estado, entradas):
        resultado = paso_real(estado, entradas)
        return replace(
            resultado,
            salida_superficial_mm=(
                resultado.salida_superficial_mm + 1.0
            ),
        )

    monkeypatch.setattr(
        modulo_ejecutor,
        "ejecutar_paso",
        paso_con_flujo_incorrecto,
    )

    with pytest.raises(ValueError, match="Balance global"):
        ejecutar_serie(
            crear_estado(), 600.0, 300.0, eventos=()
        )


def test_no_modifica_entradas_y_resultados_son_inmutables():
    estado = crear_estado()
    evento = crear_evento()
    eventos = (evento,)

    resultado = ejecutar_serie(
        estado, 600.0, 300.0, eventos=eventos
    )

    assert estado.almacenamientos_mm == (40.0, 80.0)
    assert evento.riego_mm_h == 6.0
    assert resultado.estado_inicial is estado
    assert isinstance(resultado.registros, tuple)

    with pytest.raises(FrozenInstanceError):
        resultado.riego_mm = 0.0

    with pytest.raises(FrozenInstanceError):
        resultado.registros[0].intervalo = None
