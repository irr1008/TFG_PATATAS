"""
Entradas de un intervalo del núcleo hidráulico.

Duración: s.
Precipitación, riego y extracciones solicitadas: mm por intervalo.

Los aportes y demandas ya son acumulados del intervalo, no tasas.
No se sustituyen datos ausentes por cero ni se calculan flujos.
"""

from dataclasses import dataclass
from math import isfinite
from numbers import Real

from .configuracion import ConfiguracionPerfil


def _exigir_finito(nombre: str, valor: object) -> None:
    if isinstance(valor, bool) or not isinstance(valor, Real):
        raise ValueError(f"{nombre} debe ser un número real finito.")
    if not isfinite(valor):
        raise ValueError(f"{nombre} debe ser finito.")


def _exigir_no_negativo(nombre: str, valor: object) -> None:
    _exigir_finito(nombre, valor)
    if valor < 0:
        raise ValueError(f"{nombre} no puede ser negativo.")


@dataclass(frozen=True)
class EntradasPaso:
    """
    Entradas prescritas para un perfil y un intervalo.

    Las extracciones se ordenan desde la capa superficial.
    Una demanda puede superar el almacenamiento disponible: su limitación
    a una extracción efectiva corresponde al futuro cálculo de flujos.
    """

    configuracion: ConfiguracionPerfil
    dt_s: float
    precipitacion_mm: float
    riego_mm: float
    extracciones_solicitadas_mm: tuple[float, ...]

    def __post_init__(self) -> None:
        if not isinstance(self.configuracion, ConfiguracionPerfil):
            raise ValueError("configuracion debe ser ConfiguracionPerfil.")

        _exigir_finito("dt_s", self.dt_s)
        if self.dt_s <= 0:
            raise ValueError("dt_s debe ser positivo.")

        if self.dt_s / 3600.0 == 0:
            raise ValueError(
                "dt_s es demasiado pequeño para representarlo en horas."
            )

        _exigir_no_negativo(
            "precipitacion_mm", self.precipitacion_mm
        )
        _exigir_no_negativo("riego_mm", self.riego_mm)

        if not isinstance(self.extracciones_solicitadas_mm, tuple):
            raise ValueError(
                "extracciones_solicitadas_mm debe ser una tupla."
            )

        if (
            len(self.extracciones_solicitadas_mm)
            != self.configuracion.numero_capas
        ):
            raise ValueError(
                "Debe existir una demanda de extracción por capa."
            )

        for indice, demanda in enumerate(
            self.extracciones_solicitadas_mm,
            start=1,
        ):
            _exigir_no_negativo(
                f"extracción solicitada de la capa {indice}",
                demanda,
            )

    @property
    def dt_h(self) -> float:
        """Duración del intervalo expresada en horas."""
        return self.dt_s / 3600.0
