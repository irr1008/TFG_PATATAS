"""
Paso hidráulico completo del núcleo.

Almacenamientos y flujos acumulados del intervalo: mm.
Duración: s (se convierte a h dentro de EntradasPaso).

Orden de evaluación (diseño v0.2, sección 8):
drenaje inferior -> transferencias de abajo arriba -> infiltración
y salida superficial -> extracción prescrita -> balance.
"""

from dataclasses import dataclass
from math import fsum, isfinite

from .drenaje import aplicar_drenaje
from .entradas import EntradasPaso
from .estados import EstadoPerfil
from .extraccion import aplicar_extraccion
from .infiltracion import aplicar_infiltracion


@dataclass(frozen=True)
class ResultadoPaso:
    """
    Resultado de un paso hidráulico completo.

    transferencias_mm[j] es la transferencia de la capa j a la j+1.
    residual_masa_mm es el residual independiente del paso:
    epsilon = Delta S - B, con B = P + I - RO - DP - sum(X).
    residuales_fases_mm contiene, en orden, los residuales de
    drenaje, infiltración y extracción, para diagnóstico.
    """

    estado_final: EstadoPerfil
    aporte_mm: float
    infiltracion_mm: float
    salida_superficial_mm: float
    drenaje_inferior_mm: float
    transferencias_mm: tuple[float, ...]
    extracciones_mm: tuple[float, ...]
    demandas_no_satisfechas_mm: tuple[float, ...]
    residual_masa_mm: float
    tolerancia_masa_mm: float
    residuales_fases_mm: tuple[float, float, float]


def ejecutar_paso(
    estado: EstadoPerfil,
    entradas: EntradasPaso,
) -> ResultadoPaso:
    """
    Aplica un intervalo completo al perfil sin modificar las entradas.

    Cada fase recibe el estado de trabajo que deja la anterior.
    El agua infiltrada no drena en el mismo paso y la extracción
    utiliza el estado posterior a la infiltración.

    No corrige estados ni flujos para cerrar el balance: si el
    residual supera la tolerancia, lanza ValueError.
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

    drenaje = aplicar_drenaje(estado, entradas.dt_h)
    infiltracion = aplicar_infiltracion(drenaje.estado_final, entradas)
    extraccion = aplicar_extraccion(infiltracion.estado_final, entradas)

    estado_final = extraccion.estado_final

    aporte_mm = entradas.precipitacion_mm + entradas.riego_mm
    drenaje_inferior_mm = drenaje.drenaje_inferior_mm
    salida_mm = infiltracion.salida_superficial_mm
    extraido_mm = fsum(extraccion.extracciones_mm)

    total_inicial = fsum(estado.almacenamientos_mm)
    total_final = fsum(estado_final.almacenamientos_mm)

    delta_almacenamiento = total_final - total_inicial
    balance_flujos = fsum(
        (aporte_mm, -salida_mm, -drenaje_inferior_mm, -extraido_mm)
    )
    residual = delta_almacenamiento - balance_flujos

    escala = max(
        1.0,
        total_inicial,
        total_final,
        aporte_mm + salida_mm + drenaje_inferior_mm + extraido_mm,
    )
    tolerancia = 1e-9 + 1e-12 * escala

    if (
        not isfinite(escala)
        or not isfinite(residual)
        or abs(residual) > tolerancia
    ):
        raise ValueError(
            "Balance del paso fuera de tolerancia: "
            f"residual={residual} mm; tolerancia={tolerancia} mm."
        )

    return ResultadoPaso(
        estado_final=estado_final,
        aporte_mm=aporte_mm,
        infiltracion_mm=infiltracion.infiltracion_mm,
        salida_superficial_mm=salida_mm,
        drenaje_inferior_mm=drenaje_inferior_mm,
        transferencias_mm=drenaje.transferencias_mm,
        extracciones_mm=extraccion.extracciones_mm,
        demandas_no_satisfechas_mm=extraccion.demandas_no_satisfechas_mm,
        residual_masa_mm=residual,
        tolerancia_masa_mm=tolerancia,
        residuales_fases_mm=(
            drenaje.residual_masa_mm,
            infiltracion.residual_masa_mm,
            extraccion.residual_masa_mm,
        ),
    )
