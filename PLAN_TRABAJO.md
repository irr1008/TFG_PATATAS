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
- Notebooks 01, 02 y 03 y `requirements.txt` publicados, sin salidas en los notebooks 02 y 03.
- Las coordenadas, el municipio y la variedad de las parcelas no están en el repositorio: el notebook 02 los lee de un archivo privado, `datos_parcelas_privados.py`, y el repositorio incluye la plantilla `notebooks/datos_parcelas_privados_ejemplo.py` con valores ficticios.

Trabajo de análisis y transición realizado en el sprint 3:
- Motor de referencia analizado en `docs/analisis-motor-referencia.md`;
  se conserva como antecedente y no como especificación activa.
- Variables y unidades documentadas en `docs/variables-balance-hidrico.md`;
  su reutilización se revisará según el nuevo modelo.
- Histórico de sondas analizado en `docs/analisis-historico-sondas.md`.
- Fuentes meteorológicas comparadas en `docs/fuentes-meteorologicas.md`;
  la descarga y preparación siguen pendientes.
- Reunión del 06/11 y cambio de enfoque registrados en
  `docs/registro-reunion-06-11-2026.md`.
- Nuevo modelo descrito en `docs/especificación-modelo-físico.md`
  y `docs/diseño-nucleo-hidraulico.md`, sin implementación todavía.

Pendiente de la fase 1:
- Repetir la extracción para incorporar las imágenes posteriores al 22/10/2026 hasta el fin del periodo.
- Confirmar la campaña y las fechas agronómicas de las parcelas.
- Completar la auditoría y preparación de los datos reales en #16:
  el histórico de sondas ya fue analizado, pero siguen pendientes metadatos,
  discrepancias y confirmación de riegos aplicados.

La fase 2 se ha iniciado a nivel de especificación y diseño, sin implementación.

El sprint 3 se cierra anticipadamente el 08/11/2026 tras el cambio de enfoque
de la reunión del 06/11. El tiempo restante de su planificación deja de ser
necesario para el alcance vigente.

El siguiente incremento tendrá como objetivo implementar un núcleo hidráulico
independiente de Agrobioma v14 y verificarlo con datos sintéticos. Se prepara mediante 
las issues #17 a #22, con 52 horas estimadas en total. Se pretende iniciar el sprint 4 
el 09/11/2026; su calendario y milestone se definirán después de cerrar el sprint 3.

La auditoría de datos reales continúa en #16. La meteorología de #11 y la
ampliación Sentinel-2 de #12 permanecen en el backlog.

Las fases de aprendizaje automático, aprendizaje por refuerzo e interfaz
se mantienen como líneas futuras, no como trabajo iniciado ni como alcance
comprometido del próximo sprint.


## Riesgos y limitaciones iniciales
- Sentinel-2 no mide directamente la humedad del suelo.
- La frecuencia temporal de las observaciones no es diaria.
- Podrán ser necesarios datos meteorológicos externos o sintéticos.
- Los parámetros físicos del suelo pueden no estar disponibles.
- La complejidad final del modelo deberá ajustarse al tiempo y a los datos.
