# Notebooks del TFG

Los notebooks se ejecutan en Google Colab. Los datos (geometrías de parcelas,
CSV generados y resultados) se guardan en Google Drive y no forman parte de
este repositorio.

## Notebooks y estado en el repositorio

| Notebook | Función | Estado en el repositorio |
|---|---|---|
| `02_preparacion_parcelas_reales` | Genera el catálogo de parcelas y sus geometrías y comprueba su validez. Lee las coordenadas, el municipio y la variedad de un archivo privado, `datos_parcelas_privados.py`, que no está en el repositorio | Publicado, sin salidas y sin datos privados |
| `03_extraccion_sentinel2_parcelas_reales` | Extrae Sentinel-2 con Google Earth Engine y genera los CSV de índices (NDVI, NDRE, NDMI, MSI, EVI y SAVI), de calidad y el resumen semanal. Combina en un mosaico las teselas de una misma fecha cuando la parcela cae en más de una, y descarta una imagen solo si la nube y la sombra de la propia parcela superan el 30 % | Publicado, sin salidas |
| `01_Exploracion_inicial_datos_sentinel-2` | Parte 1: estructura de los CSV de las cuatro parcelas. Parte 2: ejemplo previo con maíz de 2018. Parte 3: evolución temporal de NDVI, NDRE, NDMI y EVI | Publicado |
| `04_analisis_historico_sondas` | Analiza el histórico de sondas de humedad del suelo: estructura, frecuencia de lectura, huecos, calidad, solape con el periodo del estudio y episodios candidatos de subida. Lee el histórico de una carpeta privada de Drive y sustituye los identificadores de las sondas por alias | Publicado, sin salidas y sin identificadores |

## Orden de ejecución

1. `02_preparacion_parcelas_reales`: crea el catálogo y las geometrías en Drive a
   partir del archivo privado de datos de las parcelas.
2. `03_extraccion_sentinel2_parcelas_reales`: lee el catálogo y genera los CSV.
3. `01_Exploracion_inicial_datos_sentinel-2`: analiza los CSV (Parte 1) y
   representa la evolución de los índices (Parte 3). La Parte 3 usa datos
   definidos en la Parte 1, por lo que se ejecuta después de ella. La Parte 2
   es independiente y requiere un CSV de maíz de 2018 en Drive.
4. `04_analisis_historico_sondas`: independiente de los anteriores. Lee el
   histórico de sondas de `TFG_PATATAS_TRABAJO/privado/historico_sondas` y no
   usa los CSV de Sentinel-2.

## Cómo ejecutarlos

1. Abre el notebook en Colab y ejecuta las celdas en orden.
2. Autoriza el acceso a Drive cuando Colab lo pida. Los notebooks usan la
   carpeta de trabajo `TFG_PATATAS_TRABAJO` de tu Drive.
3. Antes de ejecutar el notebook 02, copia `datos_parcelas_privados_ejemplo.py`
   con el nombre `datos_parcelas_privados.py` en `TFG_PATATAS_TRABAJO/privado`
   de tu Drive y sustituye los valores ficticios por los reales (municipio,
   variedad y polígonos GeoJSON con el orden longitud, latitud). Este archivo
   no se sube al repositorio.
4. En el notebook 03, autoriza Google Earth Engine con tu cuenta. El
   identificador de tu proyecto de Earth Engine se lee del secreto
   `PROYECTO_EE` de Colab (icono de la llave, con acceso al notebook
   concedido) o se pide al ejecutar sin mostrarlo en pantalla. No se guarda
   en el notebook.
5. El periodo de extracción se define en `FECHA_INICIO` y `FECHA_FIN` del
   notebook 03 (hoy del 2026-04-01 al 2026-11-01, con fin excluido). Si el fin es
   posterior a la fecha de ejecución, solo se obtienen las imágenes ya
   disponibles. Al cambiar el periodo, el notebook 01 debe usar el mismo
   (`PERIODO`).
6. No pegues códigos de verificación, tokens ni identificadores de proyecto en
   las celdas ni en los comentarios.
7. Antes de publicar un notebook, borra sus salidas si contienen datos de las
   explotaciones (Editar → Borrar todos los resultados).

## Dónde se guardan las salidas en Drive

| Salida | Carpeta |
|---|---|
| Catálogo y geometrías de las parcelas | `TFG_PATATAS_TRABAJO/parcelas` |
| CSV de índices, calidad y resumen semanal (una carpeta por periodo) | `TFG_PATATAS_TRABAJO/resultados/sentinel2_lotes` |
| Tablas del análisis de estructura | `TFG_PATATAS_TRABAJO/resultados/analisis_estructura_csv` |
| Figuras de evolución temporal | `TFG_PATATAS_TRABAJO/resultados/graficas_evolucion_temporal` |
| Datos privados de las parcelas (coordenadas, municipio y variedad) | `TFG_PATATAS_TRABAJO/privado` (no se sube a GitHub) |
| Tablas y figuras del análisis del histórico de sondas | `TFG_PATATAS_TRABAJO/resultados/analisis_historico_sondas` |
| Histórico de sondas y correspondencia entre identificadores y alias | `TFG_PATATAS_TRABAJO/privado` (no se sube a GitHub) |

## Datos privados de las parcelas

El 02 necesita las coordenadas, el municipio y la variedad de las parcelas
reales. Como el repositorio es público, esos datos no están en el notebook: se
leen de `privado/datos_parcelas_privados.py` en Drive, un archivo excluido del
repositorio mediante `.gitignore`. La plantilla
`datos_parcelas_privados_ejemplo.py` muestra el formato con valores ficticios.

El 02 se publica sin salidas porque estas muestran el municipio y la variedad
de las parcelas. El 03 se publica sin salidas y sin el identificador del
proyecto de Earth Engine.

## Requisitos

- Cuenta de Google con acceso a Drive y a Google Earth Engine.
- Dependencias en `requirements.txt`, probadas en Colab con Python 3.13.16. En
  Colab la mayoría ya están instaladas; los notebooks 02 y 03 instalan
  `shapely` y `earthengine-api` en celdas propias.
- No se almacenan credenciales ni tokens en este repositorio.

## Documentación relacionada

- `docs/analisis-estructura-csv.md`: estructura de los CSV (Parte 1 del 01).
- `docs/evolucion-temporal-indices.md`: evolución temporal (Parte 3 del 01).
- `docs/preparacion-datos-simulador.md`: reglas y decisiones de preparación de
  los datos (notebook 03).
- `docs/analisis-historico-sondas.md`: análisis del histórico de sondas
  (notebook 04).
