"""
Conversiones entre almacenamiento y humedad volumétrica.

Almacenamiento: mm.
Espesor: m.
Humedad volumétrica: m³/m³.

Estas funciones comprueban límites geométricos generales.
Los umbrales específicos de cada capa se comprobarán al validar el estado.
"""

from math import isfinite
from numbers import Real


def _validar_numero(nombre: str, valor: object) -> None:
    if isinstance(valor, bool) or not isinstance(valor, Real):
        raise ValueError(f"{nombre} debe ser un número real finito.")
    if not isfinite(valor):
        raise ValueError(f"{nombre} debe ser finito.")


def _validar_espesor(espesor_m: float) -> None:
    _validar_numero("espesor_m", espesor_m)
    if espesor_m <= 0:
        raise ValueError("espesor_m debe ser positivo.")


def humedad_a_almacenamiento(
    theta: float,
    espesor_m: float,
) -> float:
    """Convierte humedad volumétrica en almacenamiento de agua, en mm."""
    _validar_numero("theta", theta)
    _validar_espesor(espesor_m)

    if not 0 <= theta <= 1:
        raise ValueError("theta debe estar entre 0 y 1.")

    factor = 1000.0 * espesor_m
    if not isfinite(factor):
        raise ValueError("El espesor produce un factor no finito.")

    return factor * theta


def almacenamiento_a_humedad(
    almacenamiento_mm: float,
    espesor_m: float,
) -> float:
    """Convierte almacenamiento de agua, en mm, en humedad volumétrica."""
    _validar_numero("almacenamiento_mm", almacenamiento_mm)
    _validar_espesor(espesor_m)

    factor = 1000.0 * espesor_m
    if not isfinite(factor):
        raise ValueError("El espesor produce un factor no finito.")

    if not 0 <= almacenamiento_mm <= factor:
        raise ValueError(
            "El almacenamiento debe estar entre cero y "
            "el equivalente a theta=1."
        )

    return almacenamiento_mm / factor
