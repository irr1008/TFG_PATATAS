"""
Aplicación de la extracción prescrita y de la demanda no satisfecha.

Almacenamientos, demandas y flujos del intervalo: mm.
No aplica drenaje, transferencias ni infiltración.
"""

from dataclasses import dataclass
from math import fsum, isfinite
from numbers import Real

from .conversiones import humedad_a_almacenamiento
from .entradas import EntradasPaso
from .estados import (
    EstadoPerfil,
    TOLERANCIA_ESTADO_MM,
    comprobar_almacenamientos,
)


def _exigir_no_negativo(nombre: str, valor: object) -> None:
    if isinstance(valor, bool) or not isinstance(valor, Real):
        raise ValueError(f"{nombre} debe ser un número real finito.")
    if not isfinite(valor):
        raise ValueError(f"{nombre} debe ser finito.")
    if valor < 0:
        raise ValueError(f"{nombre} no puede ser negativo.")


def extraccion_efectiva_mm(
    demanda_mm: float,
    almacenamiento_mm: float,
    almacenamiento_minimo_mm: float,
) -> tuple[float, float]:
    """
    Calcula la extracción efectiva y la demanda no satisfecha, en mm.

    X = min(U, max(0, S - S_min)); no satisfecha = U - X.
    No modifica almacenamientos.
    """
    _exigir_no_negativo("demanda_mm", demanda_mm)
    _exigir_no_negativo("almacenamiento_mm", almacenamiento_mm)
    _exigir_no_negativo(
        "almacenamiento_minimo_mm", almacenamiento_minimo_mm
    )

    disponible_mm = max(0.0, almacenamiento_mm - almacenamiento_minimo_mm)
    extraccion_mm = min(demanda_mm, disponible_mm)

    return extraccion_mm, demanda_mm - extraccion_mm


@dataclass(frozen=True)
class ResultadoExtraccion:
    """
    Resultado de la fase de extracción, con flujos en mm por capa.
    """
    estado_final: EstadoPerfil
    extracciones_mm: tuple[float, ...]
    demandas_no_satisfechas_mm: tuple[float, ...]
    residual_masa_mm: float
    tolerancia_masa_mm: float


def aplicar_extraccion(
    estado: EstadoPerfil,
    entradas: EntradasPaso,
) -> ResultadoExtraccion:
    """
    Resta de cada capa su extracción efectiva.

    En el paso completo, estado debe ser el resultado de la fase
    de infiltración. Cada capa se limita por su propio almacenamiento
    disponible sobre S_min; la demanda no satisfecha no pasa a otra capa.

    No modifica los objetos recibidos.
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

    extracciones = []
    no_satisfechas = []
    finales = []

    for capa, almacenamiento, demanda in zip(
        configuracion.capas,
        iniciales,
        entradas.extracciones_solicitadas_mm,
    ):
        minimo_mm = humedad_a_almacenamiento(
            capa.theta_min, capa.espesor_m
        )
        extraccion_mm, no_satisfecha_mm = extraccion_efectiva_mm(
            demanda, almacenamiento, minimo_mm
        )
        extracciones.append(extraccion_mm)
        no_satisfechas.append(no_satisfecha_mm)
        finales.append(almacenamiento - extraccion_mm)

    finales = tuple(finales)

    comprobar_almacenamientos(
        configuracion,
        finales,
        tolerancia_mm=TOLERANCIA_ESTADO_MM,
    )

    total_inicial = fsum(iniciales)
    total_final = fsum(finales)
    total_extraido = fsum(extracciones)
    residual = fsum((total_final, -total_inicial, total_extraido))
    escala = max(
        1.0,
        total_inicial,
        total_final,
        total_extraido,
    )
    tolerancia = 1e-9 + 1e-12 * escala

    if (
        not isfinite(escala)
        or not isfinite(residual)
        or abs(residual) > tolerancia
    ):
        raise ValueError(
            "Balance de extracción fuera de tolerancia: "
            f"residual={residual} mm; tolerancia={tolerancia} mm."
        )

    return ResultadoExtraccion(
        estado_final=EstadoPerfil(
            configuracion=configuracion,
            almacenamientos_mm=finales,
        ),
        extracciones_mm=tuple(extracciones),
        demandas_no_satisfechas_mm=tuple(no_satisfechas),
        residual_masa_mm=residual,
        tolerancia_masa_mm=tolerancia,
    )
