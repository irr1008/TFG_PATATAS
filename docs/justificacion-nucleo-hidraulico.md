# Justificación de las leyes y limitaciones del núcleo hidráulico

Issue #17 · Sprint 4 · Fecha: 09/11/2026.
Estado: en elaboración.
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
