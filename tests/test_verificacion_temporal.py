import csv

import pytest

from modelo_fisico.verificacion_temporal import (
    generar_tablas,
    main,
)


@pytest.fixture(scope="module")
def carpeta(tmp_path_factory):
    destino = tmp_path_factory.mktemp("verificacion")
    generar_tablas(destino, commit="commit-de-prueba")
    return destino


def leer(carpeta, nombre):
    with (carpeta / nombre).open(encoding="utf-8") as archivo:
        return list(csv.DictReader(archivo))


def test_genera_todos_los_archivos(carpeta):
    nombres = {ruta.name for ruta in carpeta.iterdir()}

    assert len(nombres) == 13
    assert {
        "resumen_balances.csv",
        "refinamiento_11_1.csv",
        "criterios_11_1.csv",
        "errores_analiticos_11_2.csv",
        "commit.txt",
    } <= nombres
    assert (carpeta / "commit.txt").read_text(
        encoding="utf-8"
    ).strip() == "commit-de-prueba"

    series = [n for n in nombres if n.startswith("serie_")]
    assert len(series) == 8


def test_resumen_cierra_balance(carpeta):
    filas = leer(carpeta, "resumen_balances.csv")

    assert len(filas) == 8

    for fila in filas:
        assert abs(float(fila["residual_global_mm"])) <= float(
            fila["tolerancia_global_mm"]
        )

    for fila in filas:
        if fila["escenario"] == "11.1":
            assert float(fila["I_mm"]) == pytest.approx(12.0)
            assert float(fila["U1_mm"]) == pytest.approx(1.1)
            assert float(fila["U2_mm"]) == pytest.approx(2.2)


def test_criterios_11_1(carpeta):
    filas = leer(carpeta, "criterios_11_1.csv")

    assert len(filas) == 3
    assert all(fila["cumple"] == "True" for fila in filas)


def test_errores_analiticos_11_2(carpeta):
    filas = leer(carpeta, "errores_analiticos_11_2.csv")
    errores = [float(f["max_error_theta2"]) for f in filas]

    assert [float(f["paso_s"]) for f in filas] == [
        300.0, 150.0, 75.0, 37.5
    ]
    assert all(fino < grueso for grueso, fino in zip(errores, errores[1:]))
    assert errores[0] == pytest.approx(1.05e-4, rel=0.02)

    for fila in filas[1:]:
        assert 1.99 < float(fila["cociente_error_theta2"]) < 2.01


def test_main_escribe_resultados(tmp_path):
    salida = tmp_path / "resultados"

    assert main(["--salida", str(salida)]) == 0
    assert (salida / "resumen_balances.csv").exists()
    assert (salida / "commit.txt").exists()
