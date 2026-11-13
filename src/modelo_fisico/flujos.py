"""
Cálculos de flujos del núcleo hidráulico.

Almacenamientos y drenaje potencial: mm.
Duración y escala temporal: h.

Estas funciones no modifican estados ni aplican transferencias al perfil.
"""

from math import expm1, isfinite
from numbers import Real


def _exigir_finito(nombre: str, valor: object) -> None:
    if isinstance(valor, bool) or not isinstance(valor, Real):
        raise ValueError(f"{nombre} debe ser un número real finito.")
    if not isfinite(valor):
        raise ValueError(f"{nombre} debe ser finito.")


def drenaje_potencial_mm(
    almacenamiento_mm: float,
    capacidad_campo_mm: float,
    dt_h: float,
    tau_h: float,
) -> float:
    """
    Calcula el drenaje potencial por relajación del exceso sobre FC.

    No comprueba los límites particulares de una capa ni aplica el flujo.
    La configuración y el estado deben validarse antes de actualizar
    un perfil.

    tau_h debe ser positiva y finita. Un proceso desactivado no debe
    invocar esta función con una escala ausente o artificial.

    La expresión corresponde a una relajación aislada, no a la solución
    exacta de un perfil acoplado evaluado secuencialmente.
    """
    for nombre, valor in (
        ("almacenamiento_mm", almacenamiento_mm),
        ("capacidad_campo_mm", capacidad_campo_mm),
        ("dt_h", dt_h),
        ("tau_h", tau_h),
    ):
        _exigir_finito(nombre, valor)

    if almacenamiento_mm < 0:
        raise ValueError("almacenamiento_mm no puede ser negativo.")

    if capacidad_campo_mm < 0:
        raise ValueError("capacidad_campo_mm no puede ser negativa.")

    if dt_h <= 0:
        raise ValueError("dt_h debe ser positiva.")

    if tau_h <= 0:
        raise ValueError("tau_h debe ser positiva.")

    exceso_mm = max(0.0, almacenamiento_mm - capacidad_campo_mm)
    fraccion = -expm1(-dt_h / tau_h)

    return exceso_mm * fraccion

def infiltracion_y_salida_mm(
    aporte_mm: float,
    f_max_mm_h: float,
    dt_h: float,
    capacidad_disponible_mm: float,
    *,
    activa: bool,
) -> tuple[float, float]:
    """
    Calcula infiltración y salida superficial del intervalo, en mm.

    aporte_mm es un acumulado, no una tasa.
    capacidad_disponible_mm es el hueco de la capa superior
    después del drenaje y las transferencias.

    No modifica almacenamientos ni mantiene un depósito superficial.
    Con infiltración desactivada, todo el aporte sale del dominio.
    """
    for nombre, valor in (
        ("aporte_mm", aporte_mm),
        ("f_max_mm_h", f_max_mm_h),
        ("dt_h", dt_h),
        ("capacidad_disponible_mm", capacidad_disponible_mm),
    ):
        _exigir_finito(nombre, valor)

    if aporte_mm < 0:
        raise ValueError("aporte_mm no puede ser negativo.")

    if f_max_mm_h < 0:
        raise ValueError("f_max_mm_h no puede ser negativa.")

    if dt_h <= 0:
        raise ValueError("dt_h debe ser positiva.")

    if capacidad_disponible_mm < 0:
        raise ValueError(
            "capacidad_disponible_mm no puede ser negativa."
        )

    if not isinstance(activa, bool):
        raise ValueError("activa debe ser un booleano.")

    if not activa:
        return 0.0, aporte_mm

    infiltracion_mm = min(
        aporte_mm,
        f_max_mm_h * dt_h,
        capacidad_disponible_mm,
    )
    salida_superficial_mm = aporte_mm - infiltracion_mm

    return infiltracion_mm, salida_superficial_mm
