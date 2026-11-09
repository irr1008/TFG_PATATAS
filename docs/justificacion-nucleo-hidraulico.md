# Justificación de las leyes y limitaciones del núcleo hidráulico

Issue #17 · Sprint 4 · Fecha: 09/11/2026.
Estado: revisión documental completada para la #17; pendiente de implementación y verificación numérica.
Base: `especificación-modelo-físico.md`, versión 0.1, y
`diseño-nucleo-hidraulico.md`, versión 0.2.

## 1. Objetivo

Justificar las hipótesis y las leyes del primer núcleo hidráulico,
distinguiendo principios de conservación, cierres simplificados y
elecciones del experimento.

Esta justificación no constituye verificación del código, calibración
de parámetros ni validación con parcelas reales.

No se trasladan automáticamente reglas ni constantes de Agrobioma v14.

## 2. Alcance de las fuentes

| Fuente | Qué aporta | Qué no justifica |
|---|---|---|
| Allen et al. (1998), FAO-56, capítulo 8 | Balance de agua, unidades y concepto de capacidad de campo | Nuestro drenaje subdiario, geometría, parámetros sintéticos y orden de cálculo |
| DSSAT, Modular Approach, apartado SW.FOR | Ejemplo didáctico de modularidad, almacenamiento, drenaje proporcional al exceso y balance acumulado | Exactitud física de nuestro núcleo ni sus ecuaciones particulares |

FAO-56 utiliza un procedimiento diario que supone la pérdida del exceso
sobre capacidad de campo dentro del día. El núcleo propuesto mantiene
el exceso y lo drena progresivamente mediante una ley de relajación.

El ejemplo modular de DSSAT declara que sus algoritmos están deliberadamente
simplificados y no deben utilizarse para simular con exactitud condiciones
físicas reales. Se cita como antecedente metodológico, no como validación
del núcleo.

## 3. Conservación del agua y unidades

### 3.1. Almacenamiento de una capa

Para una capa de espesor fijo L_j, expresado en metros, y humedad volumétrica
media theta_j, expresada en m³/m³:

S_j = 1000 · L_j · theta_j.

S_j es el almacenamiento equivalente de agua, en mm, referido a una unidad
de superficie horizontal.

La relación inversa es:

theta_j = S_j / (1000 · L_j).

Esta conversión es geométrica. No implica que la medida puntual de una sonda
sea igual a la humedad media de toda la capa.

### 3.2. Balance por capa

Durante cada intervalo:

Delta S_j = F_entrada,j - F_salida,j - X_j.

Todos los flujos de esta expresión son láminas acumuladas durante el
intervalo, en mm. No son tasas.

Cada transferencia interna se resta de una capa y se suma a la siguiente
con exactamente el mismo valor.

### 3.3. Balance del perfil

Al sumar las capas, las transferencias internas se cancelan:

Delta S_total = P + I - RO - DP - sum(X_j).

Donde:
- P: precipitación que alcanza la superficie modelada.
- I: riego que alcanza la superficie modelada.
- RO: agua no infiltrada que abandona el dominio.
- DP: drenaje que sale por el fondo.
- X_j: extracción efectiva de cada capa.

El núcleo supone una superficie de referencia común y espesores fijos.

No se modelan ascenso capilar, flujo lateral, interceptación ni almacenamiento
superficial. Su omisión es una hipótesis de este incremento, no una afirmación
sobre su ausencia en las parcelas.

### 3.4. Diferencia respecto al balance de FAO-56

FAO-56 emplea riego neto infiltrado en su balance diario de la zona radicular.
En nuestro núcleo, I representa agua que llega a la superficie y todavía
puede contribuir a RO.

Las formulaciones comparten el principio de conservación, pero sus símbolos
no deben intercambiarse sin revisar las definiciones.

## 4. Derivación y alcance del drenaje exponencial

### 4.1. Hipótesis de partida

Se define el exceso sobre capacidad de campo:

x = S - S_FC.

Para una capa aislada con x > 0 se propone:

dx/dt = -x/tau.

Esta ley supone:
- Una escala temporal tau positiva y constante.
- Capacidad de campo constante durante el intervalo.
- Ausencia de aportes y extracciones durante el subproblema de drenaje.
- Ausencia de una restricción de capacidad en la capa receptora.

El tiempo t y tau deben expresarse en la misma unidad.

La ecuación es un cierre simplificado propuesto para este proyecto.
No se atribuye a FAO-56 ni a los tutores.

### 4.2. Solución del subproblema aislado

Separando variables:

dx/x = -dt/tau.

Integrando entre el inicio y el final de un intervalo:

ln(x_final/x_inicial) = -Delta t/tau.

Por tanto:

x_final = x_inicial · exp(-Delta t/tau).

El agua drenada es la disminución de ese exceso:

D = x_inicial - x_final.

D = x_inicial · [1 - exp(-Delta t/tau)].

La extensión empleada en el núcleo es:

D_pot,j = max(0, S_j - S_FC,j)
          · [1 - exp(-Delta t_h/tau_j)].

### 4.3. Comprobación dimensional y límites

- S_j y S_FC,j se expresan en mm.
- Delta t_h y tau_j se expresan en horas.
- El cociente Delta t_h/tau_j es adimensional.
- D_pot,j se expresa en mm acumulados durante el intervalo.

Para Delta t > 0 y tau > 0:

0 < 1 - exp(-Delta t/tau) < 1.

Por tanto, el drenaje potencial no supera el exceso inicial.

Si S_j <= S_FC,j, el drenaje potencial se fija en cero.

Cuando Delta t tiende a cero, el drenaje del intervalo tiende a cero.
Cuando Delta t/tau aumenta, la fracción drenada se aproxima a uno.

### 4.4. Interpretación de tau

tau es una escala temporal de relajación del exceso.

En el subproblema aislado, tras un tiempo tau queda una fracción exp(-1)
del exceso inicial. No significa que toda el agua excedente haya drenado.

tau no se identifica directamente con una conductividad hidráulica medida.
Su utilización con datos reales requerirá estimación, calibración y
evaluación de su identificabilidad.

### 4.5. Límites de la exactitud

La expresión exponencial es exacta para la ecuación de relajación aislada
y bajo las hipótesis anteriores.

No hace exacta la actualización completa del perfil, porque los procesos
se aplican secuencialmente y pueden intervenir restricciones de capacidad,
infiltración y extracción.

La ley no representa toda la física del flujo no saturado. En particular,
no describe gradientes hidráulicos ni redistribución ascendente.

## 5. Umbrales de almacenamiento y extracción

### 5.1. Definiciones

Para cada capa se distinguen:

- theta_sat,j: humedad volumétrica de saturación.
- theta_FC,j: humedad volumétrica a capacidad de campo.
- theta_min,j: límite inferior de la extracción representada en el núcleo.

Sus almacenamientos equivalentes son:

S_sat,j = 1000 · L_j · theta_sat,j.

S_FC,j = 1000 · L_j · theta_FC,j.

S_min,j = 1000 · L_j · theta_min,j.

Para este núcleo se exige:

0 <= theta_min,j <= theta_FC,j < theta_sat,j <= 1.

Estos límites son condiciones de coherencia de la configuración.
No demuestran que los parámetros describan un suelo real.

### 5.2. Función de cada umbral

La saturación limita el almacenamiento admitido por la capa.

La capacidad de campo determina el umbral a partir del cual se activa
el drenaje gravitacional simplificado.

El límite inferior de extracción determina hasta dónde puede retirar
agua el término X_j.

Por tanto, capacidad de campo no equivale a saturación y el almacenamiento
puede superar temporalmente S_FC,j sin incumplir el modelo.

### 5.3. Alcance del límite inferior

theta_min,j es un parámetro operativo del modelo.

Solo se interpretará como humedad en el punto de marchitez si esa
identificación se declara y justifica.

No se utiliza como límite universal de la evaporación del suelo ni como
demostración de que no existe agua por debajo de ese umbral.

### 5.4. Prohibición de correcciones sin balance

No se corregirá un exceso de almacenamiento mediante un recorte que
elimine agua sin contabilizarla.

Tampoco se elevará artificialmente el almacenamiento hasta S_min,j
para corregir una extracción excesiva.

Las restricciones deben aplicarse a los flujos antes de actualizar
el almacenamiento.

## 6. Transferencias internas y drenaje de fondo

### 6.1. Drenaje potencial y transferencia efectiva

El drenaje potencial de una capa se calcula mediante la ley exponencial
del apartado 4.

Para una capa que tiene otra inmediatamente debajo:

C_receptora = max(0, S_sat,j+1 - S_j+1).

T_j = min(D_pot,j, C_receptora).

C_receptora y T_j se expresan en mm.

Las transferencias se recorren de abajo arriba, después de aplicar
el drenaje de fondo.

La capacidad receptora se calcula con el estado de trabajo actualizado:
la capa receptora ya ha tenido oportunidad de evacuar agua hacia la capa
inferior o fuera del perfil.

Cada capa evacua agua antes de recibir la transferencia de la superior.
No vuelve a drenar después de recibirla dentro del mismo paso.

### 6.2. Actualización conservativa

La misma transferencia se utiliza en ambas capas:

S_j,nuevo = S_j - T_j.

S_j+1,nuevo = S_j+1 + T_j.

No se calcula por separado una salida y una entrada que puedan diferir.

Si la capa receptora no dispone de capacidad suficiente, la parte no
transferida permanece en la capa donante.

### 6.3. Condición de contorno inferior

Para la última capa:

DP = D_pot,N.

DP abandona el dominio y se registra como drenaje de fondo.

Esta condición supone una salida inferior sin restricción adicional.
No representa una capa impermeable, una capa freática ni un flujo
ascendente desde el exterior.

### 6.4. Limitaciones

La restricción por capacidad receptora evita superar la saturación
en el esquema de depósitos.

No reproduce explícitamente gradientes de potencial hidráulico,
presiones de agua ni flujo preferencial.

El bloqueo de una transferencia no implica que el modelo represente
correctamente los procesos físicos de un perfil encharcado.

## 7. Entrada superficial e infiltración

### 7.1. Agua disponible

El agua que llega a la superficie durante el intervalo es:

W = P + I.

P e I son láminas acumuladas durante el intervalo, en mm.

No incluyen agua interceptada antes de alcanzar la superficie modelada.

### 7.2. Restricciones de entrada

Se define una capacidad máxima de infiltración constante f_max,
expresada en mm/h.

Para un intervalo Delta t_h:

F_tasa = f_max · Delta t_h.

El espacio disponible en la primera capa es:

C_1 = max(0, S_sat,1 - S_1).

La infiltración efectiva es:

F = min(W, F_tasa, C_1).

El almacenamiento de la primera capa se incrementa en F.

### 7.3. Agua no infiltrada

RO = W - F.

Como el núcleo no representa almacenamiento superficial, toda el agua
no infiltrada abandona el dominio durante ese intervalo.

RO se interpreta como salida superficial agregada. No permite distinguir
entre escorrentía por limitación de infiltración y por saturación.

### 7.4. Limitaciones

f_max es un parámetro efectivo y constante de este incremento.

No representa la evolución de la infiltración con el frente de humectación,
el estado de la superficie, el encostramiento o la estructura del suelo.

La entrada también depende del momento del intervalo en que se evalúa
el espacio disponible en la primera capa.

Una salida superficial alta puede deberse a esta simplificación temporal,
no únicamente a una propiedad física del suelo.

## 8. Extracción prescrita y extracción efectiva

### 8.1. Demanda de entrada

La demanda X_dem,j se proporciona externamente para cada capa y cada
intervalo, en mm.

X_dem,j corresponde a U_j en `diseño-nucleo-hidraulico.md`.
Ambos símbolos representan la misma extracción solicitada por capa
y por intervalo; no son dos entradas diferentes.

Debe ser no negativa.

El núcleo no determina por sí mismo la demanda atmosférica, el reparto
radicular ni los coeficientes de cultivo.

### 8.2. Restricción por disponibilidad

En el momento de aplicar la extracción:

A_j = max(0, S_j - S_min,j).

X_j = min(X_dem,j, A_j).

La actualización es:

S_j,nuevo = S_j - X_j.

La demanda no satisfecha se registra como:

X_no_satisfecha,j = X_dem,j - X_j.

La demanda no satisfecha no es una salida de agua del dominio.

### 8.3. Alcance

Esta regla evita extraer agua por debajo del umbral configurado.

No representa una reducción progresiva por estrés hídrico antes de
alcanzar ese umbral.

No se redistribuye automáticamente la demanda no satisfecha entre capas.
Una redistribución futura requerirá una regla explícita y pruebas propias.

Si se desea representar evaporación del suelo y transpiración con
umbrales diferentes, deberán separarse ambos procesos.

## 9. Orden secuencial y dependencia temporal

### 9.1. Secuencia del diseño

En cada intervalo:

1. Validar configuración, entradas y estados, y guardar el estado inicial.
2. Aplicar el drenaje de fondo a la última capa.
3. Aplicar las transferencias internas de abajo arriba.
4. Calcular e incorporar la infiltración con el estado resultante.
5. Registrar como RO el aporte superficial no infiltrado.
6. Aplicar las extracciones prescritas.
7. Comprobar los estados y calcular el balance y sus diagnósticos.

Cada flujo se calcula con el estado de trabajo inmediatamente anterior
a su aplicación. No se calculan todos los flujos a partir del estado
inicial del intervalo.

Para una sola capa se aplican drenaje de fondo, infiltración y extracción.
No existen transferencias internas.

### 9.2. Consecuencias del orden elegido

La capa inferior drena antes de recibir agua de la superior.

En las transferencias internas, cada capa evacua agua antes de recibir
la transferencia de la capa situada encima.

La capacidad liberada por esas salidas puede utilizarse al calcular
las entradas posteriores.

El agua recién infiltrada no participa en el drenaje de ese mismo paso.
Sí puede quedar disponible para la extracción, que se aplica después.

El retardo introducido por esta secuencia no se interpreta como un
tiempo de viaje físico del agua.

### 9.3. Alcance de la discretización

El orden constituye una separación numérica de procesos que físicamente
pueden coexistir.

La solución exponencial del drenaje aislado no elimina el error temporal
del acoplamiento entre capas y procesos.

No se afirmará independencia respecto al paso temporal.

La sensibilidad se evaluará mediante refinamiento del paso y mediante
el caso acoplado con solución analítica definido en el diseño.

Las comparaciones conservarán las condiciones iniciales, los parámetros
y los aportes y demandas acumulados sobre los mismos periodos.

El paso nominal de 300 s es una elección de trabajo pendiente de evaluación.
Su aceptación dependerá de los errores medidos, no solo del cierre de masa.

## 10. Criterios de revisión de esta justificación

La revisión documental se ha realizado con los siguientes criterios:

- Cada símbolo tiene una definición y una unidad.
- Se distinguen tasas de flujo y láminas acumuladas por intervalo.
- La derivación exponencial declara sus hipótesis de validez.
- Se distingue saturación de capacidad de campo.
- theta_min se presenta como límite operativo de extracción.
- Las transferencias internas utilizan la misma salida y entrada.
- El agua no infiltrada y el drenaje de fondo quedan contabilizados.
- La demanda no satisfecha no se contabiliza como salida de agua.
- El orden de procesos coincide con el diseño del núcleo.
- Los parámetros sintéticos no se presentan como datos de parcelas.
- Las fuentes se citan solo para las afirmaciones que respaldan.
- Se distinguen justificación matemática, verificación numérica, calibración y evaluación con datos reales.

La revisión documental no sustituye la ejecución de las pruebas previstas
para las tareas de implementación y evaluación.

## 11. Notación y correspondencia con el diseño

El índice j identifica una capa, numerada desde la superficie.
N es el número total de capas.

| Símbolo | Significado | Unidad |
|---|---|---|
| L_j | Espesor fijo de la capa | m |
| theta_j | Humedad volumétrica media de la capa | m³/m³ |
| theta_min,j | Límite inferior operativo de extracción | m³/m³ |
| theta_FC,j | Humedad a capacidad de campo | m³/m³ |
| theta_sat,j | Humedad de saturación | m³/m³ |
| S_j | Almacenamiento de agua de la capa | mm |
| S_min,j, S_FC,j, S_sat,j | Almacenamientos asociados a los umbrales | mm |
| P, I | Aportes que alcanzan la superficie durante el intervalo | mm |
| W | Aporte superficial total, P + I; denominado A en el diseño | mm |
| f_max | Capacidad efectiva máxima de infiltración | mm/h |
| F_tasa | Límite de infiltración debido a f_max durante el intervalo | mm |
| C_1 | Espacio disponible en la primera capa al evaluar la infiltración | mm |
| F | Infiltración efectiva; denominada F_inf en el diseño | mm |
| RO | Agua no infiltrada que abandona el dominio | mm |
| x | Exceso de almacenamiento sobre capacidad de campo en la derivación | mm |
| tau_j | Escala temporal de relajación del drenaje | h |
| D_pot,j | Drenaje potencial de la capa durante el intervalo | mm |
| C_receptora | Espacio disponible en la capa receptora | mm |
| T_j | Transferencia de j a j+1; denominada F_j,j+1 en el diseño | mm |
| DP | Drenaje que abandona el fondo del perfil | mm |
| X_dem,j | Extracción solicitada; denominada U_j en el diseño | mm |
| A_j | Agua disponible para la extracción por encima de S_min,j | mm |
| X_j | Extracción efectiva | mm |
| X_no_satisfecha,j | Demanda no satisfecha; denominada U_no_satisfecha,j en el diseño | mm |
| Delta t_h | Duración del intervalo | h |
| t | Tiempo de la derivación, expresado en la misma unidad que tau | h |
| Delta S_j | Diferencia entre almacenamiento final e inicial de la capa | mm |

F_entrada,j y F_salida,j son los totales de entradas y salidas hidráulicas
de la capa durante el intervalo, en mm. La extracción X_j se contabiliza
por separado.

Todos los aportes, transferencias y extracciones de las ecuaciones
discretas son acumulados del intervalo, no tasas.

## 12. Limitaciones y posibles revisiones

| Decisión de este incremento | Qué deja fuera | Posible revisión futura |
|---|---|---|
| Capas con humedad media uniforme | Variabilidad dentro de cada capa y alrededor de una sonda | Revisar la discretización vertical y la correspondencia entre observaciones y estados |
| Drenaje exponencial solo por encima de capacidad de campo | Flujo por debajo de ese umbral y dependencia explícita de gradientes hidráulicos | Evaluar un cierre hidráulico más detallado si los datos y el objetivo lo requieren |
| Transferencias exclusivamente descendentes | Redistribución ascendente y ascenso capilar | Incorporar flujos bidireccionales y condiciones de contorno apropiadas |
| Infiltración con capacidad constante | Evolución de la capacidad de entrada durante la humectación | Evaluar una ley dependiente del estado y del evento |
| Ausencia de depósito superficial | Retención temporal y reinfiltración posterior | Incorporar almacenamiento superficial con su propio balance |
| Salida inferior sin restricción adicional | Capa impermeable, nivel freático y contrapresión | Revisar la condición de contorno inferior |
| Extracción prescrita por capa | Demanda atmosférica, reparto radicular y respuesta progresiva al estrés | Incorporar módulos de demanda y extracción con hipótesis explícitas |
| Separación secuencial de procesos | Simultaneidad de los procesos y respuesta independiente del orden | Medir el error temporal y revisar el acoplamiento si resulta necesario |
| Parámetros sintéticos | Representación demostrada de una parcela concreta | Estimar y evaluar parámetros con datos adecuados y periodos independientes |

Estas alternativas no se implementan ni se seleccionan en esta tarea.

El criterio de este incremento es disponer de un núcleo pequeño,
conservativo y verificable, con supuestos explícitos.

Una mayor complejidad no se considerará una mejora demostrada sin evaluar
su necesidad, sus datos de entrada y sus resultados.

## 13. Alcance de la justificación y comprobaciones posteriores

Esta tarea documenta la coherencia matemática de las leyes propuestas,
sus unidades, sus hipótesis y sus límites de interpretación.

Se distinguen cuatro actividades:

- Justificación matemática y documental: explicar las ecuaciones elegidas
  y el alcance de sus fuentes.
- Verificación numérica: comprobar que el programa implementa las reglas
  previstas mediante pruebas, balances y referencias analíticas.
- Calibración: estimar o ajustar parámetros con datos.
- Evaluación con datos independientes: estudiar el comportamiento del
  modelo frente a observaciones no utilizadas para ajustar los parámetros.

La derivación exponencial justifica la solución del subproblema de
relajación aislado. No demuestra la adecuación física de ese cierre
para una parcela.

La revisión del orden secuencial no sustituye el estudio de sensibilidad
al paso temporal.

La conservación de masa es necesaria para este núcleo, pero no demuestra
por sí sola exactitud temporal ni capacidad de reproducir observaciones.

Las pruebas de implementación y evaluación se realizarán en las tareas
posteriores. Este documento no declara que hayan sido ejecutadas.

## 14. Referencias bibliográficas y trazabilidad

### 14.1. FAO-56

Allen, R. G., Pereira, L. S., Raes, D. y Smith, M. (1998).
Crop evapotranspiration: Guidelines for computing crop water requirements.
FAO Irrigation and Drainage Paper 56. Roma: FAO.

Capítulo 8: ETc under soil water stress conditions.
https://www.fao.org/4/X0490E/x0490e0e.htm

Apartados utilizados:
- Soil water availability: capacidad de campo y punto de marchitez.
- Soil water balance, ecuación 85: contabilidad diaria del agua.
- Deep percolation, ecuación 88: pérdida del exceso sobre capacidad
  de campo dentro del procedimiento diario simplificado.

No se atribuyen a esta fuente la ley exponencial subdiaria, el orden
secuencial ni los parámetros sintéticos del núcleo.

### 14.2. Ejemplo modular de DSSAT

DSSAT (s. f.). Modular Approach.
https://dssat.net/development/model-development/

Apartados utilizados:
- Module Definition and Structure: separación y comunicación entre módulos.
- Soil Water Balance Module (SW.FOR), Rate calculations:
  drenaje proporcional al exceso sobre capacidad de campo.
- Soil Water Balance Module (SW.FOR), Close:
  comprobación del balance acumulado.

El ejemplo declara su finalidad didáctica y no está destinado a simular
con exactitud condiciones físicas reales.

La consulta de este ejemplo no implica que el proyecto utilice el
software DSSAT ni que reproduzca sus algoritmos.

### 14.3. Decisiones propias del proyecto

La ecuación exponencial se deriva en el apartado 4.

El orden de procesos, las restricciones de transferencia y las reglas
de infiltración y extracción corresponden al diseño del núcleo.

Las capas, los parámetros sintéticos y las tolerancias pertenecen al
experimento de software. No se presentan como valores obtenidos de
las referencias anteriores.

Fuentes web consultadas el 09/11/2026.

## 15. Conclusión sobre la suficiencia del diseño

La revisión documental considera que el diseño v0.2 es suficientemente
explícito para iniciar la implementación y la verificación sintética
del primer núcleo hidráulico.

Esta conclusión se limita a disponer de:

- Estados, entradas, parámetros y unidades definidos.
- Ecuaciones de almacenamiento y reglas de transferencia explícitas.
- Un orden secuencial reproducible.
- Restricciones de almacenamiento y extracción.
- Un balance de agua con diagnósticos y tolerancias propuestas.
- Casos deterministas y un protocolo de estudio temporal.
- Una referencia analítica para un escenario de drenaje acoplado.

Se mantienen para este incremento el drenaje exponencial, la infiltración
con capacidad constante, las transferencias exclusivamente descendentes,
la ausencia de almacenamiento superficial y la extracción prescrita.

Se mantienen como simplificaciones de trabajo verificables, no como
descripciones ya contrastadas de una parcela.

El núcleo es un modelo de depósitos por capas. No se presenta como una
solución de la ecuación de Richards.

La revisión no identifica una razón técnica que obligue a modificar
las ecuaciones o el orden del diseño v0.2 antes de implementar.
Su comportamiento deberá comprobarse mediante las pruebas previstas.

La suficiencia documental no significa que el programa esté implementado,
que las pruebas hayan sido superadas ni que el paso nominal de 300 s
haya sido aceptado.

La adecuación de las simplificaciones a condiciones reales, la estimación
de parámetros y la evaluación con observaciones quedan pendientes de
trabajos posteriores.
