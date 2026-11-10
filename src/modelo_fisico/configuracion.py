"""
Configuración del perfil hidráulico.

Profundidades y espesores: m.
Humedades volumétricas: m³/m³.
Capacidad de infiltración: mm/h.
Escalas temporales de drenaje: h.

Este módulo no calcula flujos ni modifica estados.
"""

from dataclasses import dataclass, field
from math import isfinite
from numbers import Real


def _exigir_finito(nombre: str, valor: object) -> None:
    """Rechaza valores no numéricos, booleanos, NaN e infinitos."""
    if isinstance(valor, bool) or not isinstance(valor, Real):
        raise ValueError(f"{nombre} debe ser un número real finito.")
    if not isfinite(valor):
        raise ValueError(f"{nombre} debe ser finito.")


@dataclass(frozen=True)
class Capa:
    """
    Geometría y parámetros de una capa.

    tau_h=None permite omitir la escala si su drenaje está desactivado.
    Una escala proporcionada debe ser siempre positiva y finita.
    """

    z_superior_m: float
    z_inferior_m: float
    theta_min: float
    theta_fc: float
    theta_sat: float
    tau_h: float | None = None

    def __post_init__(self) -> None:
        for nombre in (
            "z_superior_m",
            "z_inferior_m",
            "theta_min",
            "theta_fc",
            "theta_sat",
        ):
            _exigir_finito(nombre, getattr(self, nombre))

        if self.z_superior_m < 0:
            raise ValueError("La profundidad superior no puede ser negativa.")

        if self.z_inferior_m <= self.z_superior_m:
            raise ValueError("El espesor de la capa debe ser positivo.")

        if not 0 <= self.theta_min <= self.theta_fc < self.theta_sat <= 1:
            raise ValueError(
                "Se exige 0 <= theta_min <= theta_fc < theta_sat <= 1."
            )

        if self.tau_h is not None:
            _exigir_finito("tau_h", self.tau_h)
            if self.tau_h <= 0:
                raise ValueError("tau_h debe ser positiva.")

    @property
    def espesor_m(self) -> float:
        return self.z_inferior_m - self.z_superior_m


@dataclass(frozen=True)
class OpcionesProcesos:
    """
    Activación independiente de los procesos del núcleo.
    """

    infiltracion: bool = True
    transferencias: bool = True
    drenaje_inferior: bool = True

    def __post_init__(self) -> None:
        for nombre in (
            "infiltracion",
            "transferencias",
            "drenaje_inferior",
        ):
            if not isinstance(getattr(self, nombre), bool):
                raise ValueError(f"{nombre} debe ser un booleano.")


@dataclass(frozen=True)
class ConfiguracionPerfil:
    """
    Perfil de una o más capas, ordenadas desde la superficie.

    Las capas se proporcionan como tupla.
    Sus interfaces deben coincidir exactamente: se recomienda reutilizar
    el mismo valor para cada límite compartido.

    Esta comprobación geométrica no utiliza la futura tolerancia de estados.
    """

    capas: tuple[Capa, ...]
    f_max_mm_h: float
    procesos: OpcionesProcesos = field(default_factory=OpcionesProcesos)

    def __post_init__(self) -> None:
        if not isinstance(self.capas, tuple) or not self.capas:
            raise ValueError("capas debe ser una tupla no vacía.")

        if not all(isinstance(capa, Capa) for capa in self.capas):
            raise ValueError("Cada elemento de capas debe ser una Capa.")

        if not isinstance(self.procesos, OpcionesProcesos):
            raise ValueError("procesos debe ser OpcionesProcesos.")

        _exigir_finito("f_max_mm_h", self.f_max_mm_h)
        if self.f_max_mm_h < 0:
            raise ValueError("f_max_mm_h no puede ser negativa.")

        if self.capas[0].z_superior_m != 0:
            raise ValueError("La primera capa debe empezar en la superficie.")

        for superior, inferior in zip(self.capas, self.capas[1:]):
            if superior.z_inferior_m != inferior.z_superior_m:
                raise ValueError("Las capas deben ser contiguas y ordenadas.")

        for indice, capa in enumerate(self.capas):
            es_ultima = indice == self.numero_capas - 1
            drenaje_activo = (
                self.procesos.drenaje_inferior
                if es_ultima
                else self.procesos.transferencias
            )
            if drenaje_activo and capa.tau_h is None:
                raise ValueError(
                    f"La capa {indice + 1} necesita tau_h para drenar."
                )

    @property
    def numero_capas(self) -> int:
        return len(self.capas)
