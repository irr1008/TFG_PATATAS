"""
Pruebas de configuración sin estados ni cálculos de flujo.
"""

from dataclasses import FrozenInstanceError

import pytest

from modelo_fisico.configuracion import (
    Capa,
    ConfiguracionPerfil,
    OpcionesProcesos,
)


def crear_capa(superior=0.0, inferior=0.2, **cambios):
    parametros = {
        "z_superior_m": superior,
        "z_inferior_m": inferior,
        "theta_min": 0.05,
        "theta_fc": 0.25,
        "theta_sat": 0.45,
        "tau_h": 6.0,
    }
    parametros.update(cambios)
    return Capa(**parametros)


@pytest.mark.parametrize("numero", [1, 2, 4])
def test_admite_distintos_numeros_de_capas(numero):
    limites = [indice * 0.2 for indice in range(numero + 1)]
    capas = tuple(
        crear_capa(limites[indice], limites[indice + 1])
        for indice in range(numero)
    )

    perfil = ConfiguracionPerfil(capas=capas, f_max_mm_h=12.0)

    assert perfil.numero_capas == numero
    assert perfil.capas[0].espesor_m == pytest.approx(0.2)


@pytest.mark.parametrize(
    "cambios",
    [
        {"z_superior_m": -0.1},
        {"z_inferior_m": 0.0},
        {"z_inferior_m": -0.1},
        {"theta_min": -0.01},
        {"theta_min": 0.30},
        {"theta_fc": 0.45},
        {"theta_sat": 1.1},
        {"tau_h": 0.0},
        {"tau_h": -1.0},
        {"theta_fc": float("nan")},
        {"z_inferior_m": float("inf")},
        {"tau_h": float("inf")},
        {"theta_fc": "0.25"},
        {"theta_fc": True},
    ],
)
def test_rechaza_parametros_de_capa_invalidos(cambios):
    with pytest.raises(ValueError):
        crear_capa(**cambios)


def test_admite_theta_min_igual_a_capacidad_de_campo():
    capa = crear_capa(theta_min=0.25)
    assert capa.theta_min == capa.theta_fc


@pytest.mark.parametrize(
    "capas",
    [
        (),
        [crear_capa()],
        ("no es una capa",),
        (crear_capa(0.1, 0.3),),
        (crear_capa(), crear_capa(0.3, 0.6)),
        (crear_capa(), crear_capa(0.1, 0.6)),
    ],
)
def test_rechaza_perfiles_invalidos(capas):
    with pytest.raises(ValueError):
        ConfiguracionPerfil(capas=capas, f_max_mm_h=12.0)


@pytest.mark.parametrize(
    "valor", [-1.0, float("nan"), float("inf"), "12", True]
)
def test_rechaza_capacidad_de_infiltracion_invalida(valor):
    with pytest.raises(ValueError):
        ConfiguracionPerfil(capas=(crear_capa(),), f_max_mm_h=valor)


def test_admite_capacidad_de_infiltracion_cero():
    perfil = ConfiguracionPerfil(
        capas=(crear_capa(),),
        f_max_mm_h=0.0,
    )
    assert perfil.f_max_mm_h == 0.0


@pytest.mark.parametrize(
    "nombre", ["infiltracion", "transferencias", "drenaje_inferior"]
)
def test_opciones_exigen_booleanos(nombre):
    with pytest.raises(ValueError):
        OpcionesProcesos(**{nombre: 1})


@pytest.mark.parametrize(
    "transferencias,drenaje_inferior",
    [(False, False), (False, True), (True, False), (True, True)],
)
def test_activacion_independiente_de_salidas(
    transferencias, drenaje_inferior
):
    capas = (
        crear_capa(tau_h=6.0 if transferencias else None),
        crear_capa(0.2, 0.6, tau_h=12.0 if drenaje_inferior else None),
    )
    opciones = OpcionesProcesos(
        infiltracion=False,
        transferencias=transferencias,
        drenaje_inferior=drenaje_inferior,
    )

    perfil = ConfiguracionPerfil(
        capas=capas,
        f_max_mm_h=12.0,
        procesos=opciones,
    )

    assert perfil.procesos == opciones


@pytest.mark.parametrize("capa_sin_tau", [0, 1])
def test_drenaje_activo_exige_escala(capa_sin_tau):
    capas = [
        crear_capa(),
        crear_capa(0.2, 0.6, tau_h=12.0),
    ]
    if capa_sin_tau == 0:
        capas[0] = crear_capa(tau_h=None)
    else:
        capas[1] = crear_capa(0.2, 0.6, tau_h=None)

    with pytest.raises(ValueError):
        ConfiguracionPerfil(capas=tuple(capas), f_max_mm_h=12.0)


def test_una_capa_no_necesita_tau_para_transferencias_inexistentes():
    perfil = ConfiguracionPerfil(
        capas=(crear_capa(tau_h=None),),
        f_max_mm_h=12.0,
        procesos=OpcionesProcesos(
            transferencias=True,
            drenaje_inferior=False,
        ),
    )
    assert perfil.numero_capas == 1


def test_rechaza_objeto_de_opciones_invalido():
    with pytest.raises(ValueError):
        ConfiguracionPerfil(
            capas=(crear_capa(),),
            f_max_mm_h=12.0,
            procesos=None,
        )


def test_configuracion_no_permite_reasignacion():
    perfil = ConfiguracionPerfil(
        capas=(crear_capa(),),
        f_max_mm_h=12.0,
    )

    with pytest.raises(FrozenInstanceError):
        perfil.f_max_mm_h = 20.0
