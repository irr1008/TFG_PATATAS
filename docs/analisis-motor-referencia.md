# Análisis del motor de referencia Agrobioma v14

Issue #7 · Sprint 3 · Fecha: 26/10/2026
Estado: parcial. Cubre las entradas y los parámetros del motor; la lógica de decisión y la comparación con la especificación están pendientes.
Fuentes: código del motor de decisión (versión 14.0) y documento de especificación técnica del motor mejorado, ambos proporcionados por el profesorado y no incluidos en el repositorio.

## 1. Alcance

Este documento describe, a nivel funcional, qué entradas y parámetros usa el motor v14. No reproduce código ni datos de explotaciones. Los valores numéricos exactos de las constantes del motor se conservan fuera del repositorio hasta que los tutores autoricen su publicación (issue #13). No se modifica ni se ejecuta el motor.

## 2. Estructura del motor v14

El motor es un script de decisión de un flujo de automatización que se ejecuta por parcela y día. Sus bloques son, en orden: captura de datos, parámetros hidrológicos y profundidades, lectura de la sonda y del clima, modelo hídrico, demanda evaporativa y tendencia, lluvia efectiva, modelo térmico, análisis satelital, estado del perfil y decisión, y fraccionamiento, alertas y mensajes.

## 3. Entradas

| Entrada | Origen | Unidad | Observaciones |
|---|---|---|---|
| Datos de la parcela: nombre, municipio, variedad, sistema de riego, tipo de suelo dominante, superficie, estadio fenológico, identificador de sonda | Ficha de la parcela | Texto y ha (hectárea) | Datos de explotación: no se publican |
| CC y PMP | Ficha | % volumétrico | Tienen valor por defecto si faltan |
| Kc | Ficha | Adimensional | Constante por parcela |
| Umbrales de humedad mínima, objetivo y máxima | Ficha | % volumétrico | Calibrados por parcela |
| Profundidad de la sonda y profundidad radicular | Ficha | cm | La sonda tiene 25 cm por defecto |
| Lectura de sonda: humedad, temperatura del suelo, fecha | Sonda | % vol., °C | Una sola profundidad |
| Histórico de sondas | Base de datos | % vol., °C | Respaldo y cálculo de tendencia |
| Previsión: temperatura máxima y mínima de hoy, mañana y pasado; lluvia prevista; lluvia de 48 h; alerta de lavado | AEMET | °C, mm | |
| Estación: temperatura, humedad relativa, viento, índice UV, lluvia | Estación meteorológica | °C, %, sin unidad indicada, índice, mm | La unidad del viento no consta en el código |
| Índices satelitales: NDVI, MSI, NDWI, RECI, fecha de imagen, nubosidad | Proveedor externo | Adimensional, % | Solo se usa el último registro |

## 4. Parámetros y convenciones

- Humedad del suelo: porcentaje volumétrico (VWC) medido por una sola sonda. La decisión usa solo esa lectura.
- Conversión a lámina: un punto de VWC equivale a una lámina de mm igual a la profundidad de la sonda en cm dividida entre 10.
- Agua disponible (%): (humedad − PMP) / (CC − PMP) × 100. Internamente puede ser negativa; en los mensajes se limita a 0.
- Profundidad radicular: tabla por estadio fenológico. Se usa para interpretar fase y prioridad y para una estimación informativa del horizonte radicular, con incertidumbre explícita. No interviene en la lámina de decisión.
- Estados del perfil: saturado, completo, alto, óptimo, moderado, bajo y crítico, según el déficit respecto al objetivo en puntos de VWC.
- Prioridad fenológica: baja, media, alta, crítica o controlada según el estadio.
- Dosis: mm (equivale a L/m²). Para m³/ha se multiplica por 10.
- Límites operativos: dosis mínima técnica, mínimo eficaz del pivote, máximo por riego y fraccionamiento en un máximo de dos ciclos con techo por ciclo según textura.

## 5. Decisión de alcance

Decisión (26/10/2026): el proyecto utilizará una única sonda de humedad a 25 cm de profundidad, como el v14. La matriz de pesos por profundidad de la especificación del tutor no se aplica y la humedad del perfil es la lectura de esa sonda. Se contrastará con los tutores en la revisión intermedia del 30/10.

## 6. Observaciones y preguntas provisionales

Observaciones a verificar, sin modificar el motor:
- La unidad del viento no consta en el código.
- Un comentario del código cita un mínimo de humedad del 8 %, mientras el valor por defecto es el 7 %.

Preguntas para los tutores:
1. ¿En qué unidad llega el viento?
2. ¿Se confirma que la humedad ponderada equivale a la lectura de la sonda única a 25 cm?
3. Con una única sonda a 25 cm, ¿la lámina de riego y el AFD se calculan con la profundidad radicular de la especificación o con la profundidad de la sonda, como hace el v14?
4. ¿Se autoriza publicar las constantes del motor en el repositorio?

## 7. Pendiente

- Lógica de decisión del motor.
- Comparación con los cuatro módulos de la especificación del tutor.
- Huecos, ambigüedades y preguntas restantes.
- Conclusiones y limitaciones.

## 8. Evidencias

- Issue #7 del repositorio.
- Código del motor y documento de especificación del profesorado, guardados fuera del repositorio.
