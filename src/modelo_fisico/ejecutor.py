"""
Ejecución temporal del núcleo hidráulico.

Tiempos: segundos.
Almacenamientos y flujos acumulados: mm.

El residual global se calcula con los estados extremos y los
flujos acumulados, no a partir de los residuales por paso.
"""

from dataclasses import dataclass
from math import fsum, isfinite

from .entradas import EntradasPaso
from .estados import EstadoPerfil
from .eventos import EventoTasas, integrar_eventos
from .paso import ResultadoPaso, ejecutar_paso
from .tiempos import IntervaloTemporal, construir_intervalos


@dataclass(frozen=True)
class RegistroPaso:
    intervalo: IntervaloTemporal
    estado_inicial: EstadoPerfil
    entradas: EntradasPaso
    resultado: ResultadoPaso


@dataclass(frozen=True)
class ResultadoEjecucion:
    estado_inicial: EstadoPerfil
    estado_final: EstadoPerfil
    registros: tuple[RegistroPaso, ...]
    precipitacion_mm: float
    riego_mm: float
    infiltracion_mm: float
    salida_superficial_mm: float
    drenaje_inferior_mm: float
    transferencias_mm: tuple[float, ...]
    extracciones_solicitadas_mm: tuple[float, ...]
    extracciones_mm: tuple[float, ...]
    demandas_no_satisfechas_mm: tuple[float, ...]
    residual_global_mm: float
    tolerancia_global_mm: float
    suma_residuales_mm: float
    suma_absoluta_residuales_mm: float


def ejecutar_serie(
    estado_inicial: EstadoPerfil,
    duracion_s: float,
    paso_nominal_s: float,
    *,
    eventos: tuple[EventoTasas, ...],
) -> ResultadoEjecucion:
    """
    Ejecuta una programación sintética desde cero hasta duracion_s.

    Las fronteras de los eventos dividen la malla nominal.
    Los eventos pueden prolongarse más allá de duracion_s:
    únicamente se integra su solape con la ejecución.

    Toda la programación se valida antes del primer paso.
    No se corrigen estados ni flujos para cerrar el balance.
    """
    if not isinstance(estado_inicial, EstadoPerfil):
        raise ValueError("estado_inicial debe ser EstadoPerfil.")

    if not isinstance(eventos, tuple):
        raise ValueError("eventos debe ser una tupla.")

    configuracion = estado_inicial.configuracion
    numero_capas = configuracion.numero_capas

    for evento in eventos:
        if not isinstance(evento, EventoTasas):
            raise ValueError("Cada evento debe ser EventoTasas.")

        if len(evento.extracciones_mm_h) != numero_capas:
            raise ValueError(
                "Debe existir una tasa de extracción por capa."
            )

    # Valida duración y paso antes de filtrar las fronteras.
    IntervaloTemporal(0.0, duracion_s)

    cambios = tuple(
        instante
        for evento in eventos
        for instante in (evento.inicio_s, evento.fin_s)
        if 0.0 < instante < duracion_s
    )

    intervalos = construir_intervalos(
        duracion_s,
        paso_nominal_s,
        cambios_s=cambios,
    )

    registros_lista = []
    estado = estado_inicial

    for intervalo in intervalos:
        entradas = integrar_eventos(
            configuracion,
            intervalo,
            eventos,
        )
        resultado = ejecutar_paso(estado, entradas)

        registros_lista.append(
            RegistroPaso(
                intervalo=intervalo,
                estado_inicial=estado,
                entradas=entradas,
                resultado=resultado,
            )
        )
        estado = resultado.estado_final

    registros = tuple(registros_lista)

    precipitacion = fsum(
        registro.entradas.precipitacion_mm
        for registro in registros
    )
    riego = fsum(
        registro.entradas.riego_mm
        for registro in registros
    )
    infiltracion = fsum(
        registro.resultado.infiltracion_mm
        for registro in registros
    )
    salida = fsum(
        registro.resultado.salida_superficial_mm
        for registro in registros
    )
    drenaje = fsum(
        registro.resultado.drenaje_inferior_mm
        for registro in registros
    )

    transferencias = tuple(
        fsum(
            registro.resultado.transferencias_mm[j]
            for registro in registros
        )
