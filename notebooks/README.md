# Notebooks del TFG

Los notebooks se ejecutan en Google Colab. Los datos (geometrías de parcelas,
CSV generados y resultados) se guardan en Google Drive y no forman parte de
este repositorio.

## Orden de ejecución

| Notebook | Función | Estado en el repositorio |
|---|---|---|
| `01_Exploracion_inicial_datos_sentinel-2.ipynb` | Parte 1: análisis de la estructura de los CSV de las cuatro parcelas (2026). Parte 2: ejemplo previo con un CSV de maíz de 2018 | Publicado |
| `02_preparacion_parcelas_reales` | Catálogo y validación de las geometrías de las parcelas | Pendiente de publicar |
| `03_extraccion_sentinel2_parcelas_reales` | Extracción de índices Sentinel-2 con Google Earth Engine | Pendiente de publicar |

## Por qué faltan el 02 y el 03

El 02 contiene las coordenadas de las parcelas y ambos notebooks incluyen
salidas con datos de las explotaciones. Como el repositorio es público, se
publicarán versiones saneadas tras revisar los permisos sobre los datos
(issue #4).

## Requisitos

- Cuenta de Google con acceso a Drive y a Google Earth Engine.
- Las dependencias se instalan dentro de cada notebook o están en
  `requirements.txt`.
- No se almacenan credenciales ni tokens en este repositorio.
