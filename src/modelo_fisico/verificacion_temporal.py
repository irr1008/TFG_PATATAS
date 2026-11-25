"""
Generación reproducible de las tablas de verificación temporal.

Reproduce los escenarios 11.1 y 11.2 del diseño v0.2 con
parámetros sintéticos y exporta tablas CSV.

Uso:
    python -m modelo_fisico.verificacion_temporal --salida resultados
"""

import argparse
import csv
import subprocess
from math import exp, fsum
from pathlib import Path

from .configuracion import Capa, ConfiguracionPerfil, OpcionesProcesos
from .ejecutor import ejecutar_serie
from .estados import EstadoPerfil
from .eventos import EventoTasas

PASOS_S = (300.0, 150.0, 75.0, 37.5)
DURACION_S = 86400.0


def crear_perfil():
    return ConfiguracionPerfil(
        capas=(
            Capa(0.0, 0.2, 0.05, 0.25, 0.45, 6.0),
            Capa(0.2, 0.6, 0.05, 0.25, 0.45, 12.0),
        ),
        f_max_mm_h=12.0,
        procesos=OpcionesProcesos(
            infiltracion=True,
            transferencias=True,
            drenaje_inferior=True,
        ),
    )


def crear_eventos_11_1():
    return (
        EventoTasas(
            inicio_s=0.0,
            fin_s=7200.0,
            precipitacion_mm_h=0.0,
            riego_mm_h=6.0,
            extracciones_mm_h=(0.0, 0.0),
        ),
        EventoTasas(
            inicio_s=7200.0,
            fin_s=DURACION_S,
            precipitacion_mm_h=0.0,
            riego_mm_h=0.0,
            extracciones_mm_h=(0.05, 0.10),
        ),
    )


def ejecutar_escenarios(perfil):
    definiciones = (
        ("11.1", (40.0, 80.0), crear_eventos_11_1()),
        ("11.2", (74.0, 124.0), ()),
    )
    ejecuciones = {}

    for escenario, almacenamientos, eventos in definiciones:
        for paso_s in PASOS_S:
            ejecuciones[(escenario, paso_s)] = ejecutar_serie(
                EstadoPerfil(perfil, almacenamientos),
                DURACION_S,
                paso_s,
                eventos=eventos,
            )

    return ejecuciones


def _fila_serie(tiempo_s, estado, ro_mm, dp_mm, perfil):
    s1, s2 = estado.almacenamientos_mm

    return {
        "tiempo_s": tiempo_s,
        "S1_mm": s1,
        "S2_mm": s2,
        "theta1": s1 / (1000.0 * perfil.capas[0].espesor_m),
        "theta2": s2 / (1000.0 * perfil.capas[1].espesor_m),
        "RO_acumulada_mm": ro_mm,
        "DP_acumulado_mm": dp_mm,
    }


def extraer_serie(resultado, perfil):
    filas = [
        _fila_serie(0.0, resultado.estado_inicial, 0.0, 0.0, perfil)
    ]
    salidas = []
    drenajes = []

    for registro in resultado.registros:
        salidas.append(registro.resultado.salida_superficial_mm)
        drenajes.append(registro.resultado.drenaje_inferior_mm)
        filas.append(
            _fila_serie(
                registro.intervalo.fin_s,
                registro.resultado.estado_final,
                fsum(salidas),
                fsum(drenajes),
                perfil,
            )
        )

    return filas


def tabla_resumen(ejecuciones):
    filas = []

    for (escenario, paso_s), resultado in ejecuciones.items():
        s1, s2 = resultado.estado_final.almacenamientos_mm

        filas.append({
            "escenario": escenario,
            "paso_s": paso_s,
            "numero_pasos": len(resultado.registros),
            "S1_final_mm": s1,
            "S2_final_mm": s2,
            "P_mm": resultado.precipitacion_mm,
            "I_mm": resultado.riego_mm,
            "infiltracion_mm": resultado.infiltracion_mm,
            "RO_mm": resultado.salida_superficial_mm,
            "DP_mm": resultado.drenaje_inferior_mm,
            "F12_mm": resultado.transferencias_mm[0],
            "U1_mm": resultado.extracciones_solicitadas_mm[0],
            "U2_mm": resultado.extracciones_solicitadas_mm[1],
            "X1_mm": resultado.extracciones_mm[0],
            "X2_mm": resultado.extracciones_mm[1],
            "U1_no_satisfecha_mm": (
                resultado.demandas_no_satisfechas_mm[0]
            ),
            "U2_no_satisfecha_mm": (
                resultado.demandas_no_satisfechas_mm[1]
            ),
            "residual_global_mm": resultado.residual_global_mm,
            "tolerancia_global_mm": resultado.tolerancia_global_mm,
            "suma_residuales_mm": resultado.suma_residuales_mm,
            "suma_absoluta_residuales_mm": (
                resultado.suma_absoluta_residuales_mm
            ),
        })

    return filas


def comparar_series(gruesa, fina):
    por_tiempo_gruesa = {fila["tiempo_s"]: fila for fila in gruesa}
    por_tiempo_fina = {fila["tiempo_s"]: fila for fila in fina}
    comunes = sorted(set(por_tiempo_gruesa) & set(por_tiempo_fina))

    def maximo(columna):
        return max(
            abs(
                por_tiempo_gruesa[t][columna]
                - por_tiempo_fina[t][columna]
            )
            for t in comunes
        )

    def final(columna):
        return abs(
            por_tiempo_gruesa[DURACION_S][columna]
            - por_tiempo_fina[DURACION_S][columna]
        )

    return {
        "numero_tiempos_comunes": len(comunes),
        "max_dtheta1": maximo("theta1"),
        "max_dtheta2": maximo("theta2"),
        "dS1_final_mm": final("S1_mm"),
        "dS2_final_mm": final("S2_mm"),
        "dRO_final_mm": final("RO_acumulada_mm"),
        "dDP_final_mm": final("DP_acumulado_mm"),
        "max_dRO_acumulada_mm": maximo("RO_acumulada_mm"),
        "max_dDP_acumulado_mm": maximo("DP_acumulado_mm"),
    }


def tabla_refinamiento_11_1(series):
    filas = []

    for grueso, fino in (
        (300.0, 150.0),
        (150.0, 75.0),
        (75.0, 37.5),
        (300.0, 37.5),
    ):
        comparacion = comparar_series(
            series[("11.1", grueso)], series[("11.1", fino)]
        )
        filas.append({
            "paso_grueso_s": grueso,
            "paso_fino_s": fino,
            **comparacion,
        })

    return filas


def tabla_criterios_11_1(refinamiento):
    fila = next(
        f for f in refinamiento
        if f["paso_grueso_s"] == 75.0 and f["paso_fino_s"] == 37.5
    )

    criterios = (
        (
            "Maxima diferencia de theta en tiempos comunes",
            max(fila["max_dtheta1"], fila["max_dtheta2"]),
            1e-4,
        ),
        ("Diferencia de RO total a las 24 h", fila["dRO_final_mm"], 0.01),
        ("Diferencia de DP total a las 24 h", fila["dDP_final_mm"], 0.01),
    )

    return [
        {
            "criterio": nombre,
            "valor": valor,
            "umbral": umbral,
            "cumple": valor <= umbral,
        }
        for nombre, valor, umbral in criterios
    ]


def referencia_11_2(tiempo_s):
    t_h = tiempo_s / 3600.0
    s1 = 50.0 + 24.0 * exp(-t_h / 6.0)
    s2 = (
        100.0
        + 72.0 * exp(-t_h / 12.0)
        - 48.0 * exp(-t_h / 6.0)
    )

    return s1, s2, 198.0 - s1 - s2


def tabla_errores_11_2(series, perfil):
    esp1 = 1000.0 * perfil.capas[0].espesor_m
    esp2 = 1000.0 * perfil.capas[1].espesor_m
    filas = []
    anterior = None

    for paso_s in PASOS_S:
        errores_s1 = []
        errores_s2 = []
        errores_dp = []

        for fila in series[("11.2", paso_s)]:
            s1, s2, dp = referencia_11_2(fila["tiempo_s"])
            errores_s1.append(fila["S1_mm"] - s1)
            errores_s2.append(fila["S2_mm"] - s2)
            errores_dp.append(fila["DP_acumulado_mm"] - dp)

        max_theta2 = max(abs(e) for e in errores_s2) / esp2

        filas.append({
            "paso_s": paso_s,
            "max_error_theta1": (
                max(abs(e) for e in errores_s1) / esp1
            ),
            "max_error_theta2": max_theta2,
            "error_S1_final_mm": errores_s1[-1],
            "error_S2_final_mm": errores_s2[-1],
            "error_theta1_final": errores_s1[-1] / esp1,
            "error_theta2_final": errores_s2[-1] / esp2,
            "error_DP_final_mm": errores_dp[-1],
            "max_error_DP_mm": max(abs(e) for e in errores_dp),
            "cociente_error_theta2": (
                "" if anterior is None else anterior / max_theta2
            ),
        })
        anterior = max_theta2

    return filas


def escribir_csv(ruta, filas):
    with ruta.open("w", newline="", encoding="utf-8") as archivo:
        escritor = csv.DictWriter(archivo, fieldnames=list(filas[0]))
        escritor.writeheader()
        escritor.writerows(filas)


def obtener_commit():
    try:
        return subprocess.run(
            ["git", "rev-parse", "HEAD"],
            capture_output=True,
            text=True,
            check=True,
        ).stdout.strip()
    except (OSError, subprocess.CalledProcessError):
        return "no disponible"


def generar_tablas(carpeta, commit=None):
    """Genera las tablas y devuelve las rutas escritas."""
    carpeta = Path(carpeta)
    carpeta.mkdir(parents=True, exist_ok=True)

    perfil = crear_perfil()
    ejecuciones = ejecutar_escenarios(perfil)
    series = {
        clave: extraer_serie(resultado, perfil)
        for clave, resultado in ejecuciones.items()
    }

    refinamiento = tabla_refinamiento_11_1(series)
    tablas = {
        "resumen_balances.csv": tabla_resumen(ejecuciones),
        "refinamiento_11_1.csv": refinamiento,
        "criterios_11_1.csv": tabla_criterios_11_1(refinamiento),
        "errores_analiticos_11_2.csv": tabla_errores_11_2(
            series, perfil
        ),
    }

    rutas = []

    for nombre, filas in tablas.items():
        ruta = carpeta / nombre
        escribir_csv(ruta, filas)
        rutas.append(ruta)

    for (escenario, paso_s), filas in series.items():
        ruta = carpeta / (
            f"serie_{escenario.replace('.', '_')}_paso_{paso_s:g}s.csv"
        )
        escribir_csv(ruta, filas)
        rutas.append(ruta)

    ruta_commit = carpeta / "commit.txt"
    ruta_commit.write_text(
        (commit if commit is not None else obtener_commit()) + "\n",
        encoding="utf-8",
    )
    rutas.append(ruta_commit)

    return rutas


def main(argumentos=None):
    parser = argparse.ArgumentParser(
        description="Genera las tablas de verificacion temporal."
    )
    parser.add_argument(
        "--salida",
        default="resultados_verificacion",
        help="Carpeta de salida.",
    )
    argumentos = parser.parse_args(argumentos)

    rutas = generar_tablas(argumentos.salida)
    print(f"Archivos generados: {len(rutas)}")
    print(f"Carpeta: {Path(argumentos.salida).resolve()}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
