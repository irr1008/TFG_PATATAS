"""
Estados de almacenamiento y comprobación de límites.

Almacenamientos y tolerancias absolutas: mm.
Humedades volumétricas: m³/m³.

La construcción de EstadoPerfil valida estrictamente el estado.
La función comprobar_almacenamientos permite una tolerancia explícita
para comprobaciones posteriores, sin modificar los valores recibidos.
"""

from dataclasses import dataclass
from math import isfinite
from numbers import Real

from .configuracion import ConfiguracionPerfil
from .conversiones import (
    almacenamiento_a_humedad,
    humedad_a_almacenamiento,
)


TOLERANCIA_ESTADO_MM = 1e-9


def _exigir_finito(nombre: str, valor: object) -> None:
    if isinstance(valor, bool) or not isinstance(valor, Real):
        raise ValueError(f"{nombre} debe ser un número real finito.")
    if not isfinite(valor):
        raise ValueError(f"{nombre} debe ser finito.")


def comprobar_almacenamientos(
    configuracion: ConfiguracionPerfil,
    almacenamientos_mm: tuple[float, ...],
    *,
    tolerancia_mm: float = 0.0,
) -> None:
    """
    Comprueba dimensiones y límites sin corregir los almacenamientos.

    tolerancia_mm amplía únicamente la comparación de los límites:
    S_min - tolerancia_mm <= S <= S_sat + tolerancia_mm.

    El valor por defecto es cero: comprobación estricta.
    """
    if not isinstance(configuracion, ConfiguracionPerfil):
        raise ValueError("configuracion debe ser ConfiguracionPerfil.")

    _exigir_finito("tolerancia_mm", tolerancia_mm)
    if tolerancia_mm < 0:
        raise ValueError("tolerancia_mm no puede ser negativa.")

    if not isinstance(almacenamientos_mm, tuple):
        raise ValueError("almacenamientos_mm debe ser una tupla.")

    if len(almacenamientos_mm) != configuracion.numero_capas:
        raise ValueError("Debe existir un almacenamiento por capa.")

    for indice, (capa, almacenamiento) in enumerate(
        zip(configuracion.capas, almacenamientos_mm),
        start=1,
    ):
        _exigir_finito(
            f"almacenamiento de la capa {indice}",
            almacenamiento,
        )

        minimo = humedad_a_almacenamiento(
            capa.theta_min, capa.espesor_m
        )
        maximo = humedad_a_almacenamiento(
            capa.theta_sat, capa.espesor_m
        )

        if almacenamiento < minimo:
            desviacion = minimo - almacenamiento
        elif almacenamiento > maximo:
            desviacion = almacenamiento - maximo
        else:
            desviacion = 0.0

        if desviacion > tolerancia_mm:
            raise ValueError(
                f"Almacenamiento fuera de rango en la capa {indice}: "
                f"{almacenamiento} mm; límites [{minimo}, {maximo}] mm; "
                f"tolerancia {tolerancia_mm} mm."
            )


@dataclass(frozen=True)
class EstadoPerfil:
    """
    Estado estrictamente válido asociado a una configuración.

    Los almacenamientos se ordenan desde la capa superficial.
    No se calculan flujos ni se actualiza el estado en este módulo.
    """

    configuracion: ConfiguracionPerfil
    almacenamientos_mm: tuple[float, ...]

    def __post_init__(self) -> None:
        comprobar_almacenamientos(
            self.configuracion,
            self.almacenamientos_mm,
        )

    @property
    def humedades(self) -> tuple[float, ...]:
        """Devuelve la humedad volumétrica media de cada capa."""
        return tuple(
            almacenamiento_a_humedad(
                almacenamiento, capa.espesor_m
            )
            for capa, almacenamiento in zip(
                self.configuracion.capas,
                self.almacenamientos_mm,
            )
        )

    @property
    def almacenamiento_total_mm(self) -> float:
        """Suma los almacenamientos sin modificar el estado."""
        return sum(self.almacenamientos_mm)
