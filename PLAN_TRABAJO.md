# Plan de trabajo del TFG
## Título
Sistema Inteligente de Recomendación de Riego para el Cultivo de Patata.

## Objetivo general
Diseñar e implementar un prototipo de sistema inteligente capaz de analizar
datos del cultivo, estimar su estado hídrico y recomendar acciones de riego.

## Fases previstas
### Fase 1: preparación y datos
- Documentar el problema.
- Analizar los datos de Sentinel-2.
- Identificar las variables disponibles y ausentes.
- Preparar los datos para el simulador.

### Fase 2: modelo físico

### Fase 3: simulador

### Fase 4: Machine Learning

### Fase 5: aprendizaje por refuerzo

### Fase 6: interfaz

## Estado actual
Fase 1 (preparación y datos), trabajada en el sprint 2:
- Alcance y arquitectura documentados en `docs/alcance-y-arquitectura.md`.
- Estructura de los CSV de Sentinel-2 analizada en `docs/analisis-estructura-csv.md`.
- Evolución temporal de NDVI, NDRE, NDMI y EVI representada en `docs/evolucion-temporal-indices.md`.
- Datos Sentinel-2 preparados para el simulador, descritos en `docs/preparacion-datos-simulador.md`:
  - Periodo provisional del 01/04/2026 al 01/11/2026, con imágenes hasta el 22/10/2026.
  - Teselas de una misma fecha combinadas cuando la parcela cae en más de una.
  - Imágenes descartadas solo si más del 30 % de la parcela es nube o sombra.
  - Resumen semanal sin interpolación, con las semanas posteriores a la última imagen marcadas como aún no disponibles.
- Notebooks 01 y 03 y `requirements.txt` publicados; el notebook 03 sin salidas. El notebook 02 no está publicado hasta que los tutores autoricen publicar las coordenadas, el municipio y la variedad de las parcelas.

Pendiente de la fase 1:
- Repetir la extracción para incorporar las imágenes posteriores al 22/10/2026 hasta el fin del periodo.
- Confirmar la campaña y las fechas agronómicas de las parcelas.
- Incorporar los históricos de sensores y riego.

Las fases 2 a 6 aún no se han iniciado.

El siguiente paso es completar la revisión del sprint 2 (issue #6).

## Riesgos y limitaciones iniciales
- Sentinel-2 no mide directamente la humedad del suelo.
- La frecuencia temporal de las observaciones no es diaria.
- Podrán ser necesarios datos meteorológicos externos o sintéticos.
- Los parámetros físicos del suelo pueden no estar disponibles.
- La complejidad final del modelo deberá ajustarse al tiempo y a los datos.
