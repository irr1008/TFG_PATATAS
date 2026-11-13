"""
Aplicación de infiltración y salida superficial.

Almacenamientos, aportes y flujos del intervalo: mm.
No aplica drenaje ni extracción.
"""

from dataclasses import dataclass
from math import fsum, isfinite

from .conversiones import humedad_a_almacenamiento
from .entradas import EntradasPaso
from .estados import (
    EstadoPerfil,
    TOLERANCIA_ESTADO_MM,
    comprobar_almacenamientos,
)
from .flujos import infiltracion_y_salida_mm


@dataclass(frozen=True)
class ResultadoInfiltracion:
    """Resultado de la fase de infiltración, con flujos en mm."""

    estado_final: EstadoPerfil
    infiltracion_mm: float
    salida_superficial_mm: float
    residual_masa_mm: float
    tolerancia_masa_mm: float


def aplicar_infiltracion(
    estado: EstadoPerfil,
    entradas: EntradasPaso,
) -> ResultadoInfiltracion:
    """
    Incorpora el agua infiltrada únicamente a la capa superior.

    En el paso completo, estado debe ser el resultado de la fase
    de drenaje y transferencias.

    No modifica los objetos recibidos.
    No aplica las demandas de extracción de entradas.
    No corrige almacenamientos para forzar límites o balances.
    """
    if not isinstance(estado, EstadoPerfil):
        raise ValueError("estado debe ser EstadoPerfil.")

    if not isinstance(entradas, EntradasPaso):
        raise ValueError("entradas debe ser EntradasPaso.")

    configuracion = estado.configuracion

    if entradas.configuracion != configuracion:
        raise ValueError(
            "El estado y las entradas deben corresponder "
            "a configuraciones equivalentes."
        )

    iniciales = estado.almacenamientos_mm
    comprobar_almacenamientos(configuracion, iniciales)

    aporte_mm = entradas.precipitacion_mm + entradas.riego_mm
    if not isfinite(aporte_mm):
        raise ValueError("El aporte superficial total debe ser finito.")

    capa_superior = configuracion.capas[0]
    saturacion_mm = humedad_a_almacenamiento(
        capa_superior.theta_sat,
        capa_superior.espesor_m,
    )
    hueco_mm = max(0.0, saturacion_mm - iniciales[0])

    infiltracion_mm, salida_mm = infiltracion_y_salida_mm(
        aporte_mm=aporte_mm,
        f_max_mm_h=configuracion.f_max_mm_h,
        dt_h=entradas.dt_h,
        capacidad_disponible_mm=hueco_mm,
        activa=configuracion.procesos.infiltracion,
    )

    trabajo = list(iniciales)
    trabajo[0] += infiltracion_mm
    finales = tuple(trabajo)

    comprobar_almacenamientos(
        configuracion,
        finales,
        tolerancia_mm=TOLERANCIA_ESTADO_MM,
    )

    total_inicial = fsum(iniciales)
    total_final = fsum(finales)
    residual = fsum(
        (total_final, -total_inicial, -aporte_mm, salida_mm)
    )
    escala = max(
        1.0,
        total_inicial,
        total_final,
        aporte_mm + salida_mm,
    )
    tolerancia = 1e-9 + 1e-12 * escala

    if (
        not isfinite(escala)
        or not isfinite(residual)
        or abs(residual) > tolerancia
    ):
        raise ValueError(
            "Balance de infiltración fuera de tolerancia: "
            f"residual={residual} mm; tolerancia={tolerancia} mm."
        )

    estado_final = EstadoPerfil(
        configuracion=configuracion,
        almacenamientos_mm=finales,
    )

    return ResultadoInfiltracion(
        estado_final=estado_final,
        infiltracion_mm=infiltracion_mm,
        salida_superficial_mm=salida_mm,
        residual_masa_mm=residual,
        tolerancia_masa_mm=tolerancia,
    )
