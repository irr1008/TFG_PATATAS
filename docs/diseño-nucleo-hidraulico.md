# Diseño del núcleo hidráulico

Versión: 0.1 · Fecha: 07/11/2026.
Estado: propuesta de implementación y protocolo de pruebas; no calibrado ni validado con parcelas.
Documento relacionado: `especificación-modelo-físico.md`.

## 1. Objetivo

Implementar y verificar un balance de agua por capas independiente de Agrobioma v14. Este incremento no es todavía el modelo meteorológico completo: no calcula evapotranspiración a partir de la atmósfera ni recomienda riego. Las extracciones prescritas son entradas de prueba, no estimaciones de demanda real.

## 2. Geometría y parámetros sintéticos

Todos los números de esta sección son valores elegidos para pruebas de software. No representan ninguna parcela, no proceden de los PDF privados y no deben usarse como parámetros calibrados.

| Parámetro | Capa 1 | Capa 2 | Unidad |
|---|---:|---:|---|
| Límite superior | 0,00 | 0,20 | m |
| Límite inferior | 0,20 | 0,60 | m |
| Espesor L | 0,20 | 0,40 | m |
| Humedad mínima de extracción theta_min | 0,05 | 0,05 | m³/m³ |
| Capacidad de campo theta_FC | 0,25 | 0,25 | m³/m³ |
| Saturación theta_sat | 0,45 | 0,45 | m³/m³ |
| Humedad inicial del caso base | 0,20 | 0,20 | m³/m³ |
| Escala de drenaje tau | 6 | 12 | h |

Parámetros globales: infiltración máxima f_max = 12 mm/h; paso nominal = 300 s. Cada proceso podrá desactivarse explícitamente para pruebas aisladas. No se usará tau = infinito ni tau = 0 para desactivarlo.

Los 25 cm quedan dentro de la capa 2. No se utiliza todavía esta geometría para comparar con sondas reales.

## 3. Estados y unidades

El estado interno es el almacenamiento S_j en mm:

S_j = 1000 L_j theta_j.

theta_j = S_j / (1000 L_j).

Para los parámetros sintéticos:

| Almacenamiento | Capa 1 | Capa 2 |
|---|---:|---:|
| S_min (mm) | 10 | 20 |
| S_FC (mm) | 50 | 100 |
| S_sat (mm) | 90 | 180 |
| S_inicial (mm) | 40 | 80 |

El almacenamiento inicial total es 120 mm. theta_min es un límite de extracción del experimento, no una identificación automática con PMP o humedad residual. El rango admisible de estados de este incremento es S_min <= S <= S_sat.

## 4. Entradas de un paso

- Duración dt en segundos, estrictamente positiva; dt_h = dt / 3600.
- P: precipitación que alcanza la superficie, mm por intervalo.
- I: riego que alcanza la superficie, mm por intervalo.
- U_j: extracción solicitada por capa, mm por intervalo.
- Estado inicial y parámetros por capa.

Se rechazan NaN, infinitos y aportes o demandas negativos. Datos ausentes no se convierten en cero. Las pruebas especifican explícitamente los ceros.

Si P e I llegan como tasas en mm/h, el adaptador las multiplica por dt_h. No se multiplica de nuevo un acumulado ya expresado en mm.

## 5. Drenaje

Para cada capa:

D_pot,j = max(0, S_j - S_FC,j) [1 - exp(-dt_h / tau_j)].

La ecuación es un cierre simplificado propuesto para este proyecto. No se atribuye a FAO ni a los tutores. tau_j debe ser positiva y finita cuando el proceso está activo.

Capa inferior: DP = D_pot,N; se resta del almacenamiento y se registra como salida del perfil.

Entre capas: F_j,j+1 = min(D_pot,j, max(0, S_sat,j+1 - S_j+1)). Se resta y suma el mismo valor. Si la receptora está llena, el agua permanece en la capa emisora.

Para N capas, recorrer de abajo arriba. Cada capa drena antes de recibir la transferencia de la superior; no se vuelve a drenar dentro del mismo subpaso. La ley no representa ascenso capilar, redistribución ascendente ni flujo por debajo de capacidad de campo.

La capacidad de campo no es el límite máximo de almacenamiento. No se elimina agua al superar S_FC.

## 6. Infiltración y salida superficial

A = P + I.

F_inf = min(A, f_max dt_h, max(0, S_sat,1 - S_1)).

RO = A - F_inf.

Se suma F_inf a la capa superior. No hay depósito superficial en este incremento. RO significa agua no infiltrada que abandona el dominio; no es una estimación detallada de la escorrentía de una parcela real.

f_max es una capacidad efectiva constante del modelo, no una conductividad hidráulica medida. No hay flujo preferencial ni interceptación; P e I son aportes a la superficie, no necesariamente lluvia sobre dosel o riego bruto.

## 7. Extracción prescrita

X_j = min(U_j, max(0, S_j - S_min,j)).

U_no_satisfecha,j = U_j - X_j.

Se resta únicamente X_j. La demanda no satisfecha no se interpreta aún como un índice fisiológico de estrés. No se reparten E y T en esta versión.

## 8. Orden del algoritmo

1. Validar geometría, parámetros, entradas y estados; guardar S_inicial.
2. Aplicar drenaje por el fondo.
3. Aplicar transferencias internas de abajo arriba.
4. Calcular e incorporar infiltración.
5. Registrar RO.
6. Aplicar extracciones prescritas.
7. Calcular theta_final y comprobar límites.
8. Calcular balances, residuales y diagnósticos.

Este orden es una separación numérica de procesos que físicamente pueden coexistir. El agua recién infiltrada no drena hasta el siguiente subpaso. No se interpreta ese retardo como tiempo de viaje físico. Se estudia su dependencia de dt.

## 9. Balance y tolerancias

Delta S = sum(S_final) - sum(S_inicial).

B = P + I - RO - DP - sum(X).

epsilon = Delta S - B.

Se guarda epsilon por paso, su suma firmada y la suma de sus valores absolutos. Esta última evita ocultar compensaciones de errores de distinto signo.

Tolerancia propuesta de masa por paso: abs(epsilon) <= 1e-9 mm + 1e-12 escala, donde escala = max(1 mm, sum(S_inicial), sum(S_final), P + I + RO + DP + sum(X)). Para una ejecución de n pasos se comprueba también el balance entre estados extremos y flujos acumulados, con umbral n*1e-9 mm + 1e-12 escala_global.

Las tolerancias son criterios de software propuestos, no precisión de los sensores. No se corrigen estados ni flujos para forzar el cierre del balance. Si falla, la prueba debe informar del residual.

## 10. Casos de prueba deterministas

Todos los casos son independientes. Se desactivan los procesos que no intervienen y se restablece el estado inicial antes de cada caso.

| Caso | Preparación y entradas | Resultado esperado |
|---|---|---|
| A. Reposo | Estado base; P=I=U=0 | S=(40,80) mm |
| B. Aporte pequeño | Estado base; drenaje desactivado; dt=300 s; P=0,5 mm | F_inf=0,5; RO=0; S=(40,5;80) mm |
| C. Capacidad de entrada | Estado base; drenaje desactivado; dt=300 s; P=3 mm | F_inf=1; RO=2; S=(41;80) mm |
| D. Saturación superior | S=(89,5;80); drenaje desactivado; dt=300 s; P=3 mm | F_inf=0,5; RO=2,5; S=(90;80) mm |
| E. Receptora llena | S=(74;180); salida inferior desactivada; P=I=U=0; transferencia activa | F_12=0; S sin cambios |
| F. Transferencia | S=(74;80); dt=300 s; salida inferior desactivada; sin aportes/extracción | F_12=24[1-exp(-1/72)] mm; misma pérdida y ganancia entre capas |
| G. Drenaje inferior | S=(40;124); dt=300 s; sin aportes/extracción | DP=24[1-exp(-1/144)] mm; S_2=124-DP |
| H. Extracción limitada | S=(10,5;20); drenaje desactivado; U=(2;0) mm | X=(0,5;0); no satisfecha=(1,5;0); S=(10;20) |
| I. Datos inválidos | Espesor negativo, theta_FC>theta_sat, tau<=0 activo, NaN o aporte negativo | Error explícito; no simulación silenciosa |

En el caso F, F_12 es aproximadamente 0,331029 mm. Se verifica con la expresión analítica, no solo con ese redondeo.

Para comparar números se usan tolerancias absolutas/relativas declaradas; no igualdad exacta de coma flotante.

## 11. Estudio temporal

Escenario sintético de 24 h, estado base:

- Riego a la superficie a tasa constante de 6 mm/h durante [0 h, 2 h): total 12 mm.
- P=0 en toda la ejecución.
- U=0 hasta la hora 2.
- Desde [2 h,24 h), demandas constantes U1=0,05 mm/h y U2=0,10 mm/h, convertidas a mm en cada paso.
- Drenaje e infiltración activos.

Ejecutar con dt=300, 150, 75 y 37,5 s, integrando cada aporte sobre su intervalo. Comparar almacenamientos finales y series en tiempos comunes; flujos acumulados y residuales. No aceptar la convergencia solo porque conserve masa.

Criterio inicial propuesto: la diferencia máxima de theta en tiempos comunes entre 75 y 37,5 s <= 1e-4 m³/m³, y diferencia de RO y DP acumulados <= 0,01 mm. Si falla, investigar discontinuidades y separación de procesos, reducir el paso o revisar el integrador. Estos umbrales no convierten un paso de 300 s automáticamente en aceptable: su error se informa por separado.

## 12. Estructura de implementación propuesta

- `src/modelo_fisico/`: configuración, estados, flujos e integrador, sin dependencia de Drive ni APIs.
- `tests/`: casos sintéticos, validación de entradas, balance y estudio temporal.
- `notebooks/`: demostración posterior que importe el núcleo.

Una función de paso recibirá estado, entradas, configuración y dt y devolverá nuevo estado, flujos y diagnósticos sin modificar silenciosamente los objetos de entrada. Un ejecutor de series manejará tiempos y acumulados.

## 13. Límites y siguiente incremento

No se calibra con las parcelas ni se fijan profundidades reales de sonda. Los parámetros sintéticos son únicamente fixtures de prueba. No se incorpora información privada al repositorio.

El siguiente incremento definirá demanda atmosférica, evaporación, transpiración y cultivo. Después se revisará qué parámetros son identificables y qué periodos permiten evaluar el modelo con datos reales.

Antes de implementar: revisar y aceptar este diseño, clasificar las peticiones antiguas y replanificar las issues. La especificación general 0.1 no necesita cambiar por la sola existencia de este documento complementario.
