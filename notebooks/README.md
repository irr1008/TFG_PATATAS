# Notebooks del TFG

Los notebooks se ejecutan en Google Colab. Los datos (geometrías de parcelas,
CSV generados y resultados) se guardan en Google Drive y no forman parte de
este repositorio.

## Notebooks y estado en el repositorio

| Notebook | Función | Estado en el repositorio |
|---|---|---|
| `02_preparacion_parcelas_reales` | Genera el catálogo de parcelas y sus geometrías y comprueba su validez | Pendiente de publicar |
| `03_extraccion_sentinel2_parcelas_reales` | Extrae Sentinel-2 con Google Earth Engine y genera los CSV de índices, de calidad y el resumen semanal | Pendiente de publicar |
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
3. En el notebook 03, autoriza Google Earth Engine con tu cuenta e indica tu
   propio proyecto de Earth Engine en la configuración.
4. No pegues códigos de verificación ni tokens en las celdas ni en los
   comentarios.

## Dónde se guardan las salidas en Drive

| Salida | Carpeta |
|---|---|
| Catálogo y geometrías de las parcelas | `TFG_PATATAS_TRABAJO/parcelas` |
| CSV de índices, calidad y resumen semanal | `TFG_PATATAS_TRABAJO/resultados/sentinel2_lotes` |
| Tablas del análisis de estructura | `TFG_PATATAS_TRABAJO/resultados/analisis_estructura_csv` |
| Figuras de evolución temporal | `TFG_PATATAS_TRABAJO/resultados/graficas_evolucion_temporal` |

## Por qué faltan el 02 y el 03

El 02 contiene las coordenadas de las parcelas y ambos notebooks incluyen
salidas con datos de las explotaciones. Como el repositorio es público, se
publicarán versiones saneadas tras revisar los permisos sobre los datos
(issue #4).

## Requisitos

- Cuenta de Google con acceso a Drive y a Google Earth Engine.
- Dependencias en `requirements.txt`, probadas en Colab con Python 3.13.16. En
  Colab la mayoría ya están instaladas; los notebooks 02 y 03 instalan
  `shapely` y `earthengine-api` en su primera celda.
- No se almacenan credenciales ni tokens en este repositorio.
