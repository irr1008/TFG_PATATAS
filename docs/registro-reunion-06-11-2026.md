# Registro de la reunión del 06/11/2026: cambio de enfoque

Fecha de la reunión: 06/11/2026.
Fecha de redacción: 07/11/2026.
Vinculación: issue #13 y seguimiento del sprint 3.
Estado: registro elaborado por el estudiante.

## 1. Resultado comunicado por el estudiante

La reunión se celebró. Los tutores recomendaron iniciar un modelo físico nuevo, sin seguir Agrobioma v14 como base de implementación. Se reutilizará el trabajo que resulte pertinente y el resto se conservará en el repositorio como antecedente, sin continuar su desarrollo.

Las solicitudes anteriores no se contestaron punto por punto. La celebración de la reunión no equivale a la validación de las fórmulas, constantes ni decisiones del enfoque anterior.

## 2. Orientaciones recogidas en las notas

- Comenzar con un modelo sencillo y un mínimo de entradas.
- Representar pocas capas al principio y explorar más capas y distintos espesores en versiones posteriores; 25 cm figura como profundidad de interés.
- Estudiar la evolución aproximadamente cada 5 minutos.
- Tratar el riego como entrada controlable.
- Considerar temperatura del aire, radiación solar, precipitación, humedad ambiental, viento, humedad y temperatura del suelo y propiedades del suelo; presión ambiental como posibilidad.
- Calcular el déficit de presión de vapor (VPD).
- Explorar la autocalibración y determinar qué entradas y parámetros son realmente necesarios.
- No suponer que los riegos comunicados a los agricultores fueron ejecutados (Datos aportados por la empresa).

Estas orientaciones no fijan todavía ecuaciones, espesores, parámetros calibrables ni un algoritmo numérico.

## 3. Aclaración posterior sobre las fuentes de datos

Las fichas de las parcelas están en PDF y que los CSV contienen registros de sondas e historial de mensajes. Los PDF originales son privados y no se incluyen en el repositorio.

La revisión documental posterior detecta diferencias entre la profundidad uniforme asumida anteriormente y las profundidades indicadas en las fichas. Se registra como discrepancia pendiente de aclaración, no como una nueva validación de los tutores. También se distinguen valores teóricos de la ficha, resultados calculados por el sistema previo y medidas independientes.

## 4. Consecuencias propuestas para el proyecto

- Conservar los análisis y entregables anteriores con su fecha y procedencia.
- Dejar de usar el v14 como especificación activa.
- Redactar una especificación nueva que distinga orientaciones de la reunión, propuestas técnicas e hipótesis pendientes.
- Revisar las issues #11 a #15 y la planificación antes de ejecutar el calendario anterior.
- Revisar cada petición antigua: sigue vigente, sustituida por el nuevo enfoque, o pendiente de respuesta. No marcar todas como contestadas.
- Mantener separados simulación, calibración y recomendación de riego.

## 5. Asuntos que quedan por resolver

- Profundidad efectiva y periodo de validez de cada instalación de sonda.
- Si el objetivo inicial comprende solo humedad o también temperatura del suelo.
- Disponibilidad de análisis de laboratorio completos y parámetros físicos medidos.
- Disponibilidad y fiabilidad de eventos de riego realmente aplicados.
- Horizonte temporal, resolución de entradas y criterios de evaluación de la primera versión.
- Qué parámetros se podrán estimar con los datos existentes.

## 6. Fuentes del registro

Documento `Modelo-fisico-basico.txt` redactado en la reunión que no se adjuntará al repositorio por privacidad. Las discrepancias de datos se detectaron después de la reunión al revisar cuatro exportaciones privadas de fichas de parcelas.
