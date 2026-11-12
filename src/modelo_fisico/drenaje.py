"""
Aplicación del drenaje inferior y las transferencias internas.

Almacenamientos y flujos acumulados del intervalo: mm.
Duración: h.

No aplica infiltración ni extracción.
"""

from dataclasses import dataclass
from math import fsum, isfinite
from numbers import Real

from .conversiones import humedad_a_almacenamiento
from .estados import (
    EstadoPerfil,
    TOLERANCIA_ESTADO_MM,
    comprobar_almacenamientos,
)
from .flujos import drenaje_potencial_mm


@dataclass(frozen=True)
class ResultadoDrenaje:
    """
    Resultado de la fase de drenaje.

    transferencias_mm[j] representa la transferencia de la capa j
    a la capa j+1, usando índices Python desde cero.
    La tupla está ordenada desde la interfaz superficial.
    """

    estado_final: EstadoPerfil
    drenaje_inferior_mm: float
    transferencias_mm: tuple[float, ...]
    residual_masa_mm: float
    tolerancia_masa_mm: float


def aplicar_drenaje(
    estado: EstadoPerfil,
    dt_h: float,
) -> ResultadoDrenaje:
    """
    Aplica fondo y después interfaces de abajo arriba.

    Cada capa evacua agua antes de recibirla de su superior.
    El estado recibido no se modifica.

    Las desviaciones numéricas no se corrigen recortando estados.
    El estado devuelto debe cumplir también el constructor estricto
    de EstadoPerfil.
    """
    if not isinstance(estado, EstadoPerfil):
        raise ValueError("estado debe ser EstadoPerfil.")

    if isinstance(dt_h, bool) or not isinstance(dt_h, Real):
        raise ValueError("dt_h debe ser un número real finito.")
    if not isfinite(dt_h) or dt_h <= 0:
        raise ValueError("dt_h debe ser positiva y finita.")

    configuracion = estado.configuracion
    iniciales = estado.almacenamientos_mm

    comprobar_almacenamientos(configuracion, iniciales)

    trabajo = list(iniciales)
    transferencias = [0.0] * (configuracion.numero_capas - 1)
    drenaje_inferior = 0.0

    capacidades_campo = tuple(
        humedad_a_almacenamiento(capa.theta_fc, capa.espesor_m)
        for capa in configuracion.capas
    )
    saturaciones = tuple(
        humedad_a_almacenamiento(capa.theta_sat, capa.espesor_m)
        for capa in configuracion.capas
    )

    if configuracion.procesos.drenaje_inferior:
        ultima = configuracion.numero_capas - 1
        tau_h = configuracion.capas[ultima].tau_h

        if tau_h is None:
            raise ValueError("Falta tau_h para el drenaje inferior.")

        drenaje_inferior = drenaje_potencial_mm(
            trabajo[ultima],
            capacidades_campo[ultima],
            dt_h,
            tau_h,
        )
        trabajo[ultima] -= drenaje_inferior

    if configuracion.procesos.transferencias:
        for emisora in range(configuracion.numero_capas - 2, -1, -1):
            receptora = emisora + 1
            tau_h = configuracion.capas[emisora].tau_h

            if tau_h is None:
                raise ValueError(
                    f"Falta tau_h para la capa {emisora + 1}."
                )

            potencial = drenaje_potencial_mm(
                trabajo[emisora],
                capacidades_campo[emisora],
                dt_h,
                tau_h,
            )
            capacidad_receptora = max(
                0.0,
                saturaciones[receptora] - trabajo[receptora],
            )
            flujo = min(potencial, capacidad_receptora)

            trabajo[emisora] -= flujo
            trabajo[receptora] += flujo
            transferencias[emisora] = flujo

    finales = tuple(trabajo)

    comprobar_almacenamientos(
        configuracion,
        finales,
        tolerancia_mm=TOLERANCIA_ESTADO_MM,
    )

    total_inicial = fsum(iniciales)
    total_final = fsum(finales)
    residual = fsum((total_final, -total_inicial, drenaje_inferior))
    escala = max(1.0, total_inicial, total_final, drenaje_inferior)
    tolerancia = 1e-9 + 1e-12 * escala

    if not isfinite(residual) or abs(residual) > tolerancia:
        raise ValueError(
            "Balance de drenaje fuera de tolerancia: "
            f"residual={residual} mm; tolerancia={tolerancia} mm."
        )

    estado_final = EstadoPerfil(
        configuracion=configuracion,
        almacenamientos_mm=finales,
    )

    return ResultadoDrenaje(
        estado_final=estado_final,
        drenaje_inferior_mm=drenaje_inferior,
        transferencias_mm=tuple(transferencias),
        residual_masa_mm=residual,
        tolerancia_masa_mm=tolerancia,
    )
