"""
Construcción de la malla temporal del ejecutor.

Tiempos y duraciones: segundos desde el inicio de la ejecución.

La malla nominal está anclada en cero. Los cambios de entrada
dividen los intervalos nominales sin desplazar la malla restante.
Los intervalos se interpretan como [inicio_s, fin_s).
"""

from dataclasses import dataclass
from math import isfinite
from numbers import Real


def _exigir_finito(nombre: str, valor: object) -> None:
    if isinstance(valor, bool) or not isinstance(valor, Real):
        raise ValueError(f"{nombre} debe ser un número real finito.")

    if not isfinite(valor):
        raise ValueError(f"{nombre} debe ser finito.")


@dataclass(frozen=True)
class IntervaloTemporal:
    """
    Intervalo de integración, con extremos expresados en segundos.
    """

    inicio_s: float
    fin_s: float

    def __post_init__(self) -> None:
        _exigir_finito("inicio_s", self.inicio_s)
        _exigir_finito("fin_s", self.fin_s)

        if self.inicio_s < 0:
            raise ValueError("inicio_s no puede ser negativo.")

        if self.fin_s <= self.inicio_s:
            raise ValueError("fin_s debe ser mayor que inicio_s.")

        if not isfinite(self.dt_s) or self.dt_s / 3600.0 == 0:
            raise ValueError(
                "La duración debe ser finita y representable en horas."
            )

    @property
    def dt_s(self) -> float:
        """Duración efectiva del intervalo."""
        return self.fin_s - self.inicio_s


def construir_intervalos(
    duracion_s: float,
    paso_nominal_s: float,
    *,
    cambios_s: tuple[float, ...],
) -> tuple[IntervaloTemporal, ...]:
    """
    Construye intervalos contiguos entre cero y duracion_s.

    cambios_s contiene instantes de cambio de las entradas.
    Deben estar dentro de [0, duracion_s]. Se admiten instantes
    repetidos y desordenados; cada frontera se incorpora una vez.

    Los cambios no reinician la malla nominal.
    No se fusionan fronteras próximas mediante tolerancias:
    si una duración no es representable, se rechaza explícitamente.

    Para entradas constantes se debe proporcionar cambios_s=().
    """
    _exigir_finito("duracion_s", duracion_s)
    _exigir_finito("paso_nominal_s", paso_nominal_s)

    if duracion_s <= 0:
        raise ValueError("duracion_s debe ser positiva.")

    if paso_nominal_s <= 0:
        raise ValueError("paso_nominal_s debe ser positivo.")

    if not isinstance(cambios_s, tuple):
        raise ValueError("cambios_s debe ser una tupla.")

    fronteras = {0.0, duracion_s}

    for cambio in cambios_s:
        _exigir_finito("instante de cambio", cambio)

        if not 0 <= cambio <= duracion_s:
            raise ValueError(
                "Cada cambio debe estar dentro de [0, duracion_s]."
            )

        fronteras.add(cambio)

    indice = 1
    anterior = 0.0

    while True:
        frontera = indice * paso_nominal_s

        if frontera >= duracion_s:
            break

        if not isfinite(frontera) or frontera <= anterior:
            raise ValueError(
                "No se puede avanzar en la malla temporal."
            )

        fronteras.add(frontera)
        anterior = frontera
        indice += 1

    ordenadas = sorted(fronteras)

    return tuple(
        IntervaloTemporal(inicio, fin)
        for inicio, fin in zip(ordenadas, ordenadas[1:])
    )
