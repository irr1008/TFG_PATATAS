# Análisis del histórico de sondas de humedad del suelo

Issue #9 · Sprint 3 · Fecha: 29/10/2026
Estado: versión completa, pendiente de contraste con los tutores en la revisión del 30/10/2026.
Fuentes: histórico de sondas facilitado por el personal que gestiona las sondas (no se incluye en el repositorio) y notebook `notebooks/04_analisis_historico_sondas.ipynb`. Las tablas completas y las figuras están en la carpeta privada de resultados en Drive.

## 1. Resumen

- El histórico contiene lecturas de 4 sondas, entre el 29/04/2026 y el 11/09/2026, con una lectura cada 4 horas de mediana.
- No cubre todo el periodo del estudio (01/04 a 01/11/2026): faltan abril y los 50 días desde el 12/09. Es todo el histórico facilitado.
- Las lecturas no incluyen unidad, profundidad ni parcela de cada sonda. La humedad está en % vol. y las sondas están a 25 cm. La parcela de cada sonda sigue pendiente.
- Hay huecos largos que coinciden en varias sondas a la vez, lo que apunta a una caída del sistema de captura y no a un fallo de cada sensor.
- Se han detectado 17 episodios candidatos de subida de humedad, 13 de ellos en una sola sonda, con un patrón regular cada 4 días en julio.

## 2. Estructura del histórico

| Aspecto | Resultado |
|---|---|
| Archivos leídos | 32 (CSV o Excel) |
| Filas y columnas totales | 3.152 filas y 17 columnas |
| Lecturas de sonda | 2.439 filas |
| Mensajes de conversación | 713 filas, que se descartan antes de analizar |
| Columnas de las lecturas | Fecha (texto, día/mes/año con hora), identificador de sonda (texto), temperatura (decimal), humedad (decimal) |
| Valores vacíos | Humedad, fecha e identificador: ninguno. Temperatura: 159 (6,5 %) |
| Unidad | % vol. |
| Profundidad | 25 cm |
| Parcela | No consta |
| Zona horaria de la fecha | No consta; hora local de España |

Los archivos mezclan dos tipos de registro: las lecturas de sonda y mensajes de una conversación que incluyen datos personales. Esos mensajes no se analizan ni se reproducen; las columnas personales se eliminan al cargar los datos.

## 3. Sondas e identificadores

El histórico trae 5 identificadores de sonda, pero son 4 sondas: uno de ellos es una extensión incorrecta del identificador de otra y aparece en una sola lectura (01/05/2026). Se fusionó con su sonda antes de analizar. Los identificadores se sustituyen por alias (sonda 1 a sonda 4) y la correspondencia solo existe en la carpeta privada. El histórico no indica a qué parcela corresponde cada sonda.

## 4. Frecuencia de lectura y huecos

Tras eliminar 186 filas que eran copias exactas de otras (131 pares con la misma sonda y fecha y valores idénticos, probablemente por el solape entre archivos), quedan 2.253 lecturas únicas.

| Sonda | Lecturas únicas | Primera lectura | Última lectura | Intervalo mínimo (h) | Percentil 5 (h) | Mediana (h) | Percentil 95 (h) | Máximo (h) |
|---|---:|---|---|---:|---:|---:|---:|---:|
| 1 | 564 | 29/04 | 11/09 | 0,25 | 1,01 | 4,0 | 22,99 | 100,99 |
| 2 | 559 | 29/04 | 11/09 | 0,50 | 1,00 | 4,0 | 23,00 | 156,26 |
| 3 | 569 | 29/04 | 11/09 | 0,24 | 1,00 | 4,0 | 23,00 | 100,99 |
| 4 | 561 | 29/04 | 11/09 | 0,25 | 1,00 | 4,0 | 23,00 | 155,99 |

La cadencia nominal es de una lectura cada 4 horas, pero los intervalos son irregulares: un 5 % es de una hora o menos y otro 5 % de unas 23 horas o más. Con el criterio provisional de más de 12 horas entre lecturas hay 188 huecos.

Los huecos más largos coinciden en varias sondas:

| Periodo | Duración aproximada | Sondas afectadas |
|---|---|---|
| 29/04 al 01/05 | 60 h | 1 y 3 |
| 29/04 al 05/05 | 156 h | 2 y 4 |
| 25/05 al 30/05 | 101 h | Las 4 |
| 30/05 al 01/06 | 47 h | 1, 3 y 4 |
| 01/06 al 04/06 | 70 h | 1, 3 y 4 |
| 01/06 al 05/06 | 95 h | 2 |

Que coincidan en varias sondas sugiere una caída común del sistema de captura o de transmisión. Es una hipótesis que debe confirmar quien gestiona las sondas.

## 5. Calidad de las lecturas

| Sonda | Lecturas | Imposibles (≤ 0 o > 100) | Saltos bruscos (> 10 puntos) | Sin temperatura |
|---|---:|---:|---:|---:|
| 1 | 564 | 0 | 2 | 41 |
| 2 | 559 | 3 | 1 | 41 |
| 3 | 569 | 3 | 1 | 41 |
| 4 | 561 | 2 | 2 | 36 |

Las 8 lecturas imposibles valen 0,0 y son las primeras de las sondas 2, 3 y 4 (29/04/2026). Parecen lecturas de arranque, anteriores a que la sonda midiera de verdad. Se excluyen del análisis, pero no se corrigen.

Los 6 saltos bruscos se marcan sin modificar:

| Sonda | Fecha | Humedad (% vol.) | Cambio (puntos) | Comentario |
|---|---|---:|---:|---|
| 1 | 30/05 | 29,4 | +24,2 | Posible riego o lluvia |
| 1 | 06/06 | 6,3 | −16,4 | Descenso brusco |
| 2 | 05/05 | 19,1 | +19,1 | Primera lectura válida tras los ceros de arranque |
| 3 | 25/06 | 25,6 | +21,6 | Posible riego o lluvia |
| 4 | 20/05 | 27,7 | +15,0 | Humedad alta durante cerca de un día |
| 4 | 21/05 | 5,9 | −21,6 | Caída brusca al final de ese tramo |

Humedad de las lecturas válidas (% vol.):

| Sonda | Lecturas válidas | Media | Mínimo | Percentil 25 | Mediana | Percentil 75 | Máximo |
|---|---:|---:|---:|---:|---:|---:|---:|
| 1 | 564 | 13,76 | 4,9 | 10,80 | 13,4 | 17,3 | 29,4 |
| 2 | 556 | 12,07 | 6,1 | 7,38 | 12,1 | 15,5 | 22,2 |
| 3 | 566 | 19,81 | 4,0 | 11,12 | 23,6 | 25,0 | 28,8 |
| 4 | 559 | 14,80 | 5,2 | 9,50 | 15,9 | 18,6 | 27,7 |

La sonda 3 tiene una distribución muy distinta: su mediana (23,6) está cerca del máximo, lo que indica que pasa gran parte del tiempo con la humedad alta. Aún no se aplica la regla del PMP, porque faltan los datos de textura (#13).

## 6. Solape con el periodo del estudio

El periodo provisional va del 01/04 al 01/11/2026 (214 días).

| Sonda | Días con datos válidos | Cobertura del periodo |
|---|---:|---:|
| 1 | 127 | 59,3 % |
| 2 | 121 | 56,5 % |
| 3 | 127 | 59,3 % |
| 4 | 122 | 57,0 % |

No hay lecturas del 01/04 al 28/04 ni del 12/09 al 31/10 (50 días). Dentro del tramo con datos (29/04 a 11/09, 136 días) la cobertura es del 89 al 93 %.

## 7. Episodios candidatos de subida de humedad

Criterio exploratorio: se marca una subida cuando la humedad aumenta al menos 2 puntos respecto al mínimo de las 12 horas anteriores. Las lecturas marcadas con menos de 12 horas de separación se agrupan en un episodio. Estos parámetros no son los de la calibración de la CC, que están pendientes.

| Sonda | Episodios | Amplitud (puntos) | Lecturas en la ventana de 24 a 48 h tras el pico |
|---|---:|---|---|
| 1 | 0 | — | — |
| 2 | 1 | 6,1 | 6 |
| 3 | 3 | 3,1 a 21,3 | 6 a 7 |
| 4 | 13 | 2,1 a 8,5 | 4 a 7 |

- Los 17 episodios tienen al menos 4 lecturas en la ventana posterior al pico, suficiente para plantear la calibración de la CC más adelante.
- En la sonda 4 los episodios se repiten cada 4 días exactos entre el 07/07 y el 27/07, y cada 4 o 5 días en agosto (05, 09, 13 y 18/08). Parece un turno de riego, pero es una hipótesis hasta cruzarlo con el registro de riegos.
- En la sonda 3, el episodio del 05 al 06/07 sube 21,3 puntos en unas 32 horas y es el más intenso.
- El método compara cada lectura con el mínimo de las 12 horas anteriores, así que probablemente no detecta subidas que ocurren tras un intervalo mayor. Tres de los saltos de la sección 5 (30/05 en la sonda 1, 25/06 en la 3 y 20/05 en la 4) no aparecen como episodio. Conviene revisar el método antes de usarlo en la calibración.
- Ningún episodio se confirma como riego o lluvia sin cruzarlo con el registro de riegos y la meteorología (#11 y #13).

## 8. Consecuencias para el proyecto

- Se usa el histórico tal como se entregó (29/04 a 11/09/2026), sin rellenar huecos ni corregir valores.
- Las lecturas con humedad menor o igual que 0 se excluyen y las copias exactas se eliminan.
- Frecuencia para el glosario de variables: una lectura cada 4 horas de mediana, con intervalos irregulares y huecos.
- Unidad: % vol. Profundidad: 25 cm, que coincide con la decisión de alcance del 26/10/2026.
- Fechas: hora local de España. Todo el histórico (29/04 a 11/09) está en horario de verano (UTC+2), sin cambio de hora. Al cruzarlo con datos meteorológicos en UTC hay que agrupar por día local.
- La cobertura parcial del periodo condiciona la calibración de la CC real y la validación del simulador: solo se podrán usar los 136 días con datos.

## 9. Preguntas abiertas

| Nº | Asunto | A quién |
|---|---|---|
| 1 | Parcela a la que corresponde cada sonda | Personal de las sondas |
| 2 | Causa de los huecos simultáneos (25 al 30/05, 01 al 05/06) | Personal de las sondas |
| 3 | Significado de los valores 0,0 del 29/04 | Personal de las sondas |
| 4 | Existencia de lecturas posteriores al 11/09 o anteriores al 29/04 | Personal de las sondas |
| 5 | Confirmar que el identificador con extensión incorrecta pertenece a la sonda con la que se fusionó | Personal de las sondas |
| 6 | Registro de riegos para contrastar los episodios candidatos | Tutores (#13) |
## 10. Reproducibilidad y privacidad

El notebook se ejecuta en Google Colab y lee el histórico de una carpeta privada de Drive. Las tablas y las figuras se guardan en otra carpeta privada. El repositorio no contiene datos de las explotaciones, ni identificadores de sondas, ni salidas del notebook.
