# Notebooks del TFG

Los notebooks se ejecutan en Google Colab. Los datos (geometrías de parcelas,
CSV generados y resultados) se guardan en Google Drive y no forman parte de
este repositorio.

## Notebooks y estado en el repositorio

| Notebook | Función | Estado en el repositorio |
|---|---|---|
| `02_preparacion_parcelas_reales` | Genera el catálogo de parcelas y sus geometrías y comprueba su validez | Pendiente de publicar |
| `03_extraccion_sentinel2_parcelas_reales` | Extrae Sentinel-2 con Google Earth Engine y genera los CSV de índices, de calidad y el resumen semanal | Publicado, sin salidas |
| `01_Exploracion_inicial_datos_sentinel-2` | Parte 1: estructura de los CSV de las cuatro parcelas. Parte 2: ejemplo previo con maíz de 2018. Parte 3: evolución temporal de NDVI, NDMI y EVI | Publicado |

## Orden de ejecución

1. `02_preparacion_parcelas_reales`: crea el catálogo y las geometrías en Drive.
2. `03_extraccion_sentinel2_parcelas_reales`: lee el catálogo y genera los CSV.
3. `01_Exploracion_inicial_datos_sentinel-2`: analiza los CSV (Parte 1) y
   representa la evolución de los índices (Parte 3). La Parte 3 usa datos
   definidos en la Parte 1, por lo que se ejecuta después de ella. La Parte 2
   es independiente y requiere un CSV de maíz de 2018 en Drive.

## Cómo ejecutarlos

1. Abre el notebook en Colab y ejecuta las celdas en orden.
2. Autoriza el acceso a Drive cuando Colab lo pida. Los notebooks usan la
   carpeta de trabajo `TFG_PATATAS_TRABAJO` de tu Drive.
3. En el notebook 03, autoriza Google Earth Engine con tu cuenta. El
   identificador de tu proyecto de Earth Engine se lee del secreto
   `PROYECTO_EE` de Colab (icono de la llave, con acceso al notebook
   concedido) o se pide al ejecutar sin mostrarlo en pantalla. No se guarda
   en el notebook.
4. No pegues códigos de verificación, tokens ni identificadores de proyecto en
   las celdas ni en los comentarios.

## Dónde se guardan las salidas en Drive

| Salida | Carpeta |
|---|---|
| Catálogo y geometrías de las parcelas | `TFG_PATATAS_TRABAJO/parcelas` |
| CSV de índices, calidad y resumen semanal | `TFG_PATATAS_TRABAJO/resultados/sentinel2_lotes` |
| Tablas del análisis de estructura | `TFG_PATATAS_TRABAJO/resultados/analisis_estructura_csv` |
| Figuras de evolución temporal | `TFG_PATATAS_TRABAJO/resultados/graficas_evolucion_temporal` |

## Por qué falta el 02

El 02 contiene las coordenadas de las parcelas y sus salidas incluyen datos de
las explotaciones. Como el repositorio es público, se publicará una versión
saneada solo si los tutores autorizan publicar esos datos. El 03 se publica sin
salidas y sin el identificador del proyecto de Earth Engine.

## Requisitos

- Cuenta de Google con acceso a Drive y a Google Earth Engine.
- Dependencias en `requirements.txt`, probadas en Colab con Python 3.13.16. En
  Colab la mayoría ya están instaladas; los notebooks 02 y 03 instalan
  `shapely` y `earthengine-api` en su primera celda.
- No se almacenan credenciales ni tokens en este repositorio.
