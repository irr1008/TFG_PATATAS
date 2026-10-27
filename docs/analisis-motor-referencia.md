# Análisis del motor de referencia Agrobioma v14

Issue #7 · Sprint 3 · Fecha: 26 y 27/10/2026
Estado: versión final (27/10/2026).
Fuentes: código del motor de decisión (versión 14.0) y documento de especificación técnica del motor mejorado, ambos proporcionados por el profesorado y no incluidos en el repositorio.

## 1. Alcance

Este documento describe, a nivel funcional, qué entradas, parámetros y reglas usa el motor v14 y en qué se diferencia del motor especificado por el tutor. No reproduce código ni datos de explotaciones. Los valores numéricos exactos de las constantes del motor se conservan fuera del repositorio hasta que los tutores autoricen su publicación (issue #13). No se modifica ni se ejecuta el motor.

## 2. Estructura del motor v14

El motor es un script de decisión de un flujo de automatización que se ejecuta por parcela y día. Sus bloques son, en orden:

1. Captura de datos de la ficha de la parcela, de la sonda, de la meteorología y de los índices satelitales.
2. Lectura de parámetros hidrológicos y profundidades.
3. Lectura actual de la sonda y del clima, con respaldo en el histórico.
4. Modelo hídrico y agua disponible.
5. Demanda evaporativa (ETc), tendencia y tasa de secado.
6. Lluvia efectiva.
7. Modelo térmico del suelo.
8. Análisis satelital.
9. Estado del perfil, dosis y reglas de decisión.
10. Fraccionamiento del riego, alertas, interpretación y mensajes de salida.

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
| Previsión: temperatura máxima y mínima de hoy, temperatura máxima de mañana y de pasado mañana; lluvia prevista; lluvia de 48 h; alerta de lavado | AEMET | °C, mm | |
| Estación: temperatura, humedad relativa, viento, índice UV, lluvia | Estación meteorológica | °C, %, sin unidad indicada, índice, mm | La unidad del viento no consta en el código |
| Índices satelitales: NDVI, MSI, NDWI, RECI, fecha de imagen, nubosidad | Proveedor externo | Adimensional, % | Solo se usa el último registro. La decisión usa MSI y NDWI; NDVI y RECI se leen y se devuelven en la salida |

La variedad, el sistema de riego y la superficie se leen y se muestran en los mensajes, pero no intervienen en las reglas de decisión.

## 4. Parámetros y convenciones

- Humedad del suelo: porcentaje volumétrico (VWC) medido por una sola sonda. La decisión usa solo esa lectura.
- Conversión a lámina: un punto de VWC equivale a una lámina de mm igual a la profundidad de la sonda en cm dividida entre 10. Es dimensionalmente equivalente a la lámina Lr de la especificación cuando la profundidad es la misma.
- Agua disponible (%): (humedad − PMP) / (CC − PMP) × 100. Internamente puede ser negativa; en los mensajes se limita a 0.
- Profundidad radicular: tabla por estadio fenológico. Se usa para interpretar fase y prioridad y para una estimación informativa del horizonte radicular, con incertidumbre explícita. No interviene en la lámina de decisión.
- Estados del perfil: saturado, completo, alto, óptimo, moderado, bajo y crítico. Saturado y completo dependen de la CC; el resto, del déficit respecto al objetivo en puntos de VWC.
- Prioridad fenológica: baja, media, alta, crítica o controlada según el estadio.
- Dosis: mm (equivale a L/m²). Para m³/ha se multiplica por 10.
- Límites operativos: dosis mínima técnica, mínimo eficaz del pivote, máximo por riego y fraccionamiento en un máximo de dos ciclos con techo por ciclo según textura.

## 5. Lógica de decisión

1. Se valida la lectura de la sonda: si falta o es antigua, se usa el último registro del histórico en modo degradado; si tampoco hay, se usan valores por defecto.
2. La demanda evaporativa (ETc) es una expresión empírica lineal en la temperatura media prevista, el índice UV y el viento, multiplicada por Kc, con correcciones por humedad relativa y por riesgo térmico del suelo. La ETo se obtiene dividiendo entre Kc.
3. La tendencia y la tasa de secado se calculan comparando la lectura actual con la más cercana a 24 h antes.
4. La lluvia efectiva es la lluvia de 48 h por una eficiencia que depende de la textura y se reduce con alerta de lavado. Solo se descuenta de la dosis si supera un umbral mínimo.
5. Un modelo térmico estima la temperatura del caballón y activa, si procede, un riego refrigerante.
6. La señal satelital indica estrés hídrico cuando MSI y NDWI superan umbrales, y estrés foliar cuando solo lo supera MSI. Solo se usa en fases con cobertura vegetal.
7. La dosis se calcula según el estado del perfil. Desde el estado moderado, el déficit medido es la base de la dosis y la ETc la corrige de forma acotada. En estado óptimo, la ETc es el criterio principal. Intervienen factores de textura, fase, temperatura y estrés.
8. La decisión sigue un orden de prioridad: bloqueos por lluvia o saturación, perfil agotado o crítico, déficit bajo, ola de calor, refrigeración, anti-costra en nascencia y reposición diaria.
9. Dos filtros finales evitan regar en vano: la dosis mínima eficaz en senescencia y la espera tras una humectación reciente.
10. Se aplican límites de seguridad y se fracciona la dosis. Las salidas son decisión, prioridad, dosis, ciclos, tipo de pase, alertas, interpretación y mensajes.

## 6. Comparación con el motor especificado

| Módulo | Motor v14 | Especificación del tutor | Acción prevista |
|---|---|---|---|
| 1. Hidrofísica del suelo | CC y PMP tomados de la ficha, sin calibración | PMP estático y CC teórica por Saxton y Rawls a partir de textura; CC real calibrada tras riego o lluvia | Sustituir. Faltan datos de textura (#13) y análisis de las sondas (#9) |
| 2. Crecimiento del cultivo | Profundidad radicular por tabla de estadios (informativa); Kc constante de la ficha | Zr dinámica con días tras emergencia o GDD; Kc lineal con NDVI o tablas por GDD. La matriz de pesos de sondas no se aplica con una única sonda a 25 cm | Sustituir. Faltan fechas de emergencia y parámetros a y b |
| 3. ETo | Fórmula empírica con temperatura, UV y viento | Penman-Monteith FAO-56 | Sustituir. Fuentes en #10 |
| 4. Decisión | Déficit frente a objetivo de ficha, siete estados y dosis por estado | Humedad del perfil (con una única sonda, la lectura de esa sonda), umbral de recarga con MAD, AFD y lámina Lr | Sustituir el núcleo. Hay que decidir qué reglas operativas se conservan y qué profundidad se usa en la lámina |

Diagrama de flujo de la especificación: el motor recibe entradas estáticas (la textura del suelo, con la que Saxton y Rawls dan el PMP inicial y la CC teórica) y entradas dinámicas (sondas de humedad, que alimentan la autocalibración de la CC a partir de picos y drenaje; datos satelitales o fenológicos, que dan el Kc dinámico y la profundidad radicular Zr; y datos agrometeorológicos diarios, con los que se calcula la ETo por Penman-Monteith). El motor de decisión pondera por Zr, aplica el balance hídrico con MAD y evalúa la demanda del cultivo. Las salidas son una alerta (sí o no) y la lámina óptima en mm. El diagrama figura con el título «Módulo 1» aunque recoge el flujo de los cuatro módulos, y muestra sondas a 10, 30 y 40 cm, que no se aplican por la decisión de usar una única sonda a 25 cm.

Salidas: el v14 devuelve decisión, prioridad, dosis en mm y m³/ha, ciclos, tipo de pase, alertas y mensajes. La especificación prevé como salidas una alerta (sí o no) y la lámina óptima en mm.

Estructura de código requerida por la especificación: modelos de datos para el perfil de suelo, el estado del cultivo y los datos meteorológicos, y funciones independientes para detectar la capacidad de campo, calcular los pesos de las sondas, calcular la ETo con Penman-Monteith y evaluar el riego. Con una única sonda, la función de pesos no se aplica.

Funcionalidades solo presentes en el v14, sin equivalente en la especificación: modelo térmico del caballón, riego refrigerante, anti-costra, ola de calor, lluvia efectiva y lavado, mínimo eficaz y acumulación de déficit, espera tras humectación, tratamiento de senescencia, señal satelital con MSI y NDWI, modo degradado de sonda, alertas y mensajería.

## 7. Huecos, ambigüedades y preguntas

1. El agua fácilmente disponible se expresa con (1 − MAD) y el umbral de recarga con MAD. Además, en el texto de la especificación el AFD en mm no incluye el factor ×10 que sí tiene la lámina Lr, por lo que con Zr en cm quedaría en cm. ¿Cuál es la definición correcta y en qué unidad?
2. El proyecto utilizará una única sonda a 25 cm y la matriz de pesos por profundidad no se aplica. ¿Se confirma que la humedad ponderada equivale a la lectura de esa sonda?
3. Si Zr se mantiene, ¿se calcula con la tabla de estadios del v14 o de forma dinámica con GDD o días tras emergencia? ¿Existen las fechas de emergencia?
4. ¿Qué valores de a y b se usan en Kc = a·NDVI + b? ¿Se mantiene el Kc de la ficha como respaldo?
5. ¿Qué prevalece para CC y PMP: la ficha o Saxton y Rawls? ¿Qué valores se usan para el umbral de detección de la CC real?
6. ¿Cómo varía el MAD entre 0,35 y 0,50 según el estadio? ¿Existe una tabla por estadio?
7. ¿Se conserva la ETc empírica como respaldo cuando falta la radiación neta? ¿De dónde sale?
8. ¿Se conservan las reglas operativas propias del v14 en el motor mejorado?
9. ¿Se mantiene la señal MSI y NDWI, dado que la extracción actual no incluye NDWI ni RECI?
10. ¿Cómo se concilian los umbrales de humedad de la ficha (mínima, objetivo, máxima) con el umbral basado en MAD?
11. ¿En qué unidad llega el viento?
12. ¿Se autoriza publicar las constantes del motor en el repositorio?
13. Con una única sonda a 25 cm, ¿la lámina Lr y el AFD se calculan con Zr (especificación) o con la profundidad de la sonda (v14)?
14. La autocalibración de la CC real se alimenta de las sondas. Con una única sonda a 25 cm, ¿se calibra solo con esa sonda? ¿Qué umbrales de subida de humedad y de drenaje se consideran para detectar los eventos?

Observaciones a verificar, sin modificar el motor:
- Un comentario del código cita un mínimo de humedad del 8 %, mientras el valor por defecto es el 7 %.
- La ETo que se devuelve se calcula antes del ajuste térmico posterior de la ETc, por lo que ETo por Kc no coincide con la ETc final.
- La búsqueda por subcadena de «emergencia» hace que «pre-emergencia» active también el riego refrigerante y el uso de la señal satelital.
- El formateador de mensajes usa una fórmula distinta para la ETc cuando no recibe el dato.
- La prioridad fenológica se calcula pero no interviene en la decisión; solo se usa la bandera de senescencia, aunque un comentario del código indica lo contrario.
- El contador de estrés combinado se inicializa a 0 y nunca se incrementa, por lo que su alerta no puede activarse.
- Los umbrales de humedad se convierten a agua disponible, pero esa conversión solo se escribe en el registro y no interviene en la decisión.

## 8. Conclusiones

Los cuatro módulos de la especificación sustituyen al núcleo del v14. Se conservan como candidatas las reglas operativas del v14 hasta que los tutores indiquen cuáles forman parte del motor mejorado. Los datos que bloquean la sustitución son la textura del suelo, las fechas de emergencia, MAD, a y b de Kc y la radiación neta.

La variedad, la superficie y el sistema de riego no intervienen en las reglas de decisión, y de los índices satelitales solo MSI y NDWI lo hacen. Esto simplifica la lista de variables del balance hídrico (issue #8).

Decisión de alcance (26/10/2026): el proyecto utilizará una única sonda de humedad a 25 cm de profundidad, como el v14. La matriz de pesos por profundidad de la especificación no se aplica. La decisión se contrastará con los tutores en la revisión intermedia del 30/10.

## 9. Limitaciones

- El análisis se basa en la lectura del código y del documento; no se ha ejecutado el motor.
- Los valores numéricos de las constantes no se publican (anexo privado).

## 10. Evidencias

- Issue #7 del repositorio.
- Código del motor y documento de especificación del profesorado, guardados fuera del repositorio.
