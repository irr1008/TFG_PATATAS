"""
Eventos sintéticos con tasas constantes.

Tiempos: segundos desde el inicio de la ejecución.
Tasas: mm/h.
Acumulados generados: mm por intervalo.

Una programación completa se representa mediante una tupla de eventos.
Fuera de los eventos las tasas son cero por definición.
Los eventos solapados se suman. No se admiten datos ausentes.
"""

from dataclasses import dataclass
from math import fsum, isfinite
from numbers import Real

from .configuracion import ConfiguracionPerfil
from .entradas import EntradasPaso
from .tiempos import IntervaloTemporal


def _exigir_no_negativo(nombre: str, valor: object) -> None:
    if isinstance(valor, bool) or not isinstance(valor, Real):
        raise ValueError(f"{nombre} debe ser un número real finito.")

    if not isfinite(valor) or valor < 0:
        raise ValueError(f"{nombre} debe ser finito y no negativo.")


@dataclass(frozen=True)
class EventoTasas:
    """
    Tasas constantes durante [inicio_s, fin_s).
    """

    inicio_s: float
    fin_s: float
    precipitacion_mm_h: float
    riego_mm_h: float
    extracciones_mm_h: tuple[float, ...]

    def __post_init__(self) -> None:
        IntervaloTemporal(self.inicio_s, self.fin_s)

        _exigir_no_negativo(
            "precipitacion_mm_h", self.precipitacion_mm_h
        )
        _exigir_no_negativo("riego_mm_h", self.riego_mm_h)

        if (
            not isinstance(self.extracciones_mm_h, tuple)
            or not self.extracciones_mm_h
        ):
            raise ValueError(
                "extracciones_mm_h debe ser una tupla no vacía."
            )

        for tasa in self.extracciones_mm_h:
            _exigir_no_negativo("tasa de extracción", tasa)


def integrar_eventos(
    configuracion: ConfiguracionPerfil,
    intervalo: IntervaloTemporal,
    eventos: tuple[EventoTasas, ...],
) -> EntradasPaso:
    """
    Integra las tasas por solape y devuelve acumulados del intervalo.

    Esta función puede integrar un intervalo que atraviese eventos.
    El ejecutor deberá dividir su malla en los cambios de entrada
    antes de aplicar el paso hidráulico.
    """
    if not isinstance(configuracion, ConfiguracionPerfil):
        raise ValueError("configuracion debe ser ConfiguracionPerfil.")

    if not isinstance(intervalo, IntervaloTemporal):
        raise ValueError("intervalo debe ser IntervaloTemporal.")

    if not isinstance(eventos, tuple):
        raise ValueError("eventos debe ser una tupla.")

    precipitaciones = []
    riegos = []
    demandas = [
        [] for _ in range(configuracion.numero_capas)
    ]

    for evento in eventos:
        if not isinstance(evento, EventoTasas):
            raise ValueError("Cada evento debe ser EventoTasas.")

        if (
            len(evento.extracciones_mm_h)
            != configuracion.numero_capas
        ):
            raise ValueError(
                "Debe existir una tasa de extracción por capa."
            )

        solape_s = max(
            0.0,
            min(intervalo.fin_s, evento.fin_s)
            - max(intervalo.inicio_s, evento.inicio_s),
        )

        if solape_s == 0.0:
            continue

        solape_h = solape_s / 3600.0
        if solape_h == 0.0:
            raise ValueError(
                "El solape es demasiado pequeño para expresarlo en horas."
            )

        precipitaciones.append(
            evento.precipitacion_mm_h * solape_h
        )
        riegos.append(evento.riego_mm_h * solape_h)

        for acumulados, tasa in zip(
            demandas, evento.extracciones_mm_h
        ):
            acumulados.append(tasa * solape_h)

    return EntradasPaso(
        configuracion=configuracion,
        dt_s=intervalo.dt_s,
        precipitacion_mm=fsum(precipitaciones),
        riego_mm=fsum(riegos),
        extracciones_solicitadas_mm=tuple(
            fsum(acumulados) for acumulados in demandas
        ),
    )
