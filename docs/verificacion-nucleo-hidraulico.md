# Verificación del núcleo hidráulico

Fecha de comprobación: 25/11/2026.

Estado: verificación numérica con escenarios sintéticos.
No constituye calibración ni validación con parcelas reales.

## 1. Objetivo y alcance

Comprobar por separado:

- La conservación de masa.
- La integración temporal de las entradas prescritas.
- La dependencia de los resultados respecto al paso temporal.
- El error frente a una solución analítica de drenaje acoplado.

El estudio utiliza el diseño del núcleo hidráulico v0.2,
especialmente sus secciones 9, 11.1 y 11.2.

Los parámetros son sintéticos. No proceden de parcelas,
sondas ni datos privados.

## 2. Versión y entorno comprobados

- Commit del código verificado:
  581c8bfcbf70e2e948585d1c23799dbd392df416.
- Python: 3.13.18.
- pytest: 8.4.2.
- Entorno de ejecución: Google Colab.
- Suite completa: 443 pruebas superadas.
- Código de salida: 0.
- Tiempo observado de pytest: 8,96 s.
- Generación de tablas: dos escenarios y cuatro resoluciones,
  mediante el módulo modelo_fisico.verificacion_temporal.
- Archivos comprobados: doce CSV no vacíos y commit.txt.
- El commit registrado en los resultados coincide con
  el commit del repositorio.

El tiempo de ejecución es una observación de esta sesión,
no un criterio de aceptación.

La evidencia revisada es el notebook
Pruebas_nucleo_hidraulico_issue20-14.ipynb,
con sus salidas guardadas tras reiniciar la sesión y ejecutar
las celdas en orden.

El notebook comprueba la preparación del repositorio,
la instalación, la suite, la generación de resultados,
los criterios del escenario 11.1, los balances de las ocho
ejecuciones y la disminución del error de theta2 al refinar
en el escenario 11.2.

No sustituye a la demostración reproducible prevista en la #21.
## 3. Configuración sintética

| Parámetro | Capa 1 | Capa 2 |
|---|---:|---:|
| Profundidad superior (m) | 0,00 | 0,20 |
| Profundidad inferior (m) | 0,20 | 0,60 |
| Espesor (m) | 0,20 | 0,40 |
| Humedad mínima (m³/m³) | 0,05 | 0,05 |
| Capacidad de campo (m³/m³) | 0,25 | 0,25 |
| Saturación (m³/m³) | 0,45 | 0,45 |
| Escala de drenaje (h) | 6 | 12 |

Capacidad máxima de infiltración: 12 mm/h.

Se mantienen activos la infiltración, las transferencias
internas y el drenaje inferior.

Duración de cada ejecución: 24 h.

Pasos nominales: 300, 150, 75 y 37,5 s.

El algoritmo aplica, en este orden:

1. Drenaje inferior.
2. Transferencias internas de abajo arriba.
3. Infiltración y salida superficial.
4. Extracción prescrita.
5. Comprobaciones y balance.

El agua infiltrada no drena hasta el siguiente paso.
Este retardo pertenece a la separación numérica de procesos;
no representa un tiempo de viaje físico.

## 4. Tiempos, eventos y acumulados

Los tiempos se expresan en segundos desde el inicio.
Las tasas de entrada se expresan en mm/h.

Cada evento se interpreta sobre el intervalo [inicio, fin).
Su aporte a un intervalo es la tasa multiplicada por
la duración de solape en horas.

Los eventos solapados se suman.
Fuera de los eventos, las tasas son cero por definición
de la programación sintética completa.

El ejecutor incorpora los inicios y finales de eventos
a la malla antes de aplicar los pasos hidráulicos.
Los cambios no desplazan la malla nominal restante.

Las pruebas del ejecutor incluyen cambios no alineados,
último intervalo corto y conservación de los aportes.

## 5. Balance independiente

Para cada ejecución:

Delta S = suma(S_final) - suma(S_inicial).

B = P + I - RO - DP - suma(X).

Residual global = Delta S - B.

X representa la extracción efectiva, no la solicitada.
Las transferencias internas no son salidas del perfil.

El residual global se obtiene con estados extremos
y flujos acumulados, independientemente de la suma
de residuales por paso.

También se registran:

- Suma firmada de residuales por paso.
- Suma de sus valores absolutos.

La tolerancia global sigue el diseño:

tolerancia = n * 1e-9 mm + 1e-12 * escala_global,

donde n es el número de pasos y:

escala_global = max(
  1 mm,
  almacenamiento inicial total,
  almacenamiento final total,
  P + I + RO + DP + suma(X)
).

No se corrigen estados ni flujos para forzar el cierre.

En las ocho ejecuciones, el valor absoluto del residual
global es inferior a 3,1e-12 mm.

Las tolerancias globales se sitúan aproximadamente
entre 2,88e-7 y 2,30e-6 mm.

Todas las ejecuciones cumplen su tolerancia.
Este resultado comprueba la contabilidad del agua,
no la precisión temporal ni la validez física.

## 6. Escenario 11.1: aportes y extracción

Estado inicial: S1 = 40 mm; S2 = 80 mm.

Entradas:

- Riego de 6 mm/h durante [0 h, 2 h).
- Precipitación cero durante toda la ejecución.
- Extracción solicitada cero hasta las 2 h.
- Desde las 2 hasta las 24 h:
  0,05 mm/h en la capa 1 y 0,10 mm/h en la capa 2.

Acumulados comprobados en las cuatro resoluciones:

- Riego: 12 mm.
- Infiltración: 12 mm.
- Demanda solicitada: 1,1 y 2,2 mm.
- Extracción efectiva: 1,1 y 2,2 mm.
- Demanda no satisfecha: cero.
- Salida superficial: cero.
- Drenaje inferior: cero.

### 6.1. Estados finales

| Paso (s) | Pasos efectivos | S1 final (mm) | S2 final (mm) |
|---:|---:|---:|---:|
| 300 | 288 | 49,503863 | 79,196137 |
| 150 | 576 | 49,503864 | 79,196136 |
| 75 | 1152 | 49,503864 | 79,196136 |
| 37,5 | 2304 | 49,503865 | 79,196135 |

Existe transferencia interna de aproximadamente 1,396 mm.
No debe confundirse con drenaje por el fondo.

### 6.2. Comparación entre 75 y 37,5 s

Se comparan 1153 tiempos comunes, incluido el inicial,
sin interpolación.

| Magnitud | Valor aproximado | Umbral | Resultado |
|---|---:|---:|---|
| Máxima diferencia de humedad | 8e-6 m³/m³ | 1e-4 m³/m³ | Cumple |
| Diferencia de RO total | 0 mm | 0,01 mm | Cumple |
| Diferencia de DP total | 0 mm | 0,01 mm | Cumple |

La diferencia final de almacenamiento es aproximadamente
2,62e-7 mm por capa.

Las comparaciones de RO y DP son limitadas en este escenario:
ambos flujos son cero en todas las resoluciones.
La evaluación del drenaje inferior se complementa
con el escenario 11.2.

### 6.3. Paso nominal de 300 s

Frente a 37,5 s, las diferencias máximas de humedad
en tiempos comunes son aproximadamente:

- Capa 1: 5,9e-5 m³/m³.
- Capa 2: 3,0e-5 m³/m³.

La diferencia final de almacenamiento es aproximadamente
1,84e-6 mm por capa.

La coincidencia casi completa al final no sustituye
la comparación de toda la serie.

## 7. Escenario 11.2: drenaje acoplado

Estado inicial: S1 = 74 mm; S2 = 124 mm.

Precipitación, riego y demandas de extracción: cero.

Se mantienen activas las transferencias y el drenaje inferior.

### 7.1. Referencia analítica

Con t expresado en horas:

S1(t) = 50 + 24 exp(-t/6).

S2(t) = 100 + 72 exp(-t/12) - 48 exp(-t/6).

DP(t) = 198 - S1(t) - S2(t).

La referencia representa el sistema continuo de drenaje
acoplado del diseño. No reproduce el algoritmo secuencial.

Cada resolución se compara con esta referencia en todos
sus tiempos de salida, incluido el inicial.

### 7.2. Resultados

Los errores finales son numérico menos analítico.
Los errores máximos son valores absolutos.

| Paso (s) | Máximo error de theta2 (m³/m³) | Error final de S2 (mm) | Error final de DP (mm) | Máximo error de DP en la serie (mm) |
|---:|---:|---:|---:|---:|
| 300 | 0,000105 | +0,019571 | -0,019571 | 0,041812 |
| 150 | 0,000052 | +0,009769 | -0,009769 | 0,020870 |
| 75 | 0,000026 | +0,004880 | -0,004880 | 0,010426 |
| 37,5 | 0,000013 | +0,002439 | -0,002439 | 0,005211 |

El máximo error de humedad de la capa 1 es inferior
a 5e-16 m³/m³ en estas ejecuciones.

La capa inferior conserva algo más de agua que la referencia
continua, mientras el drenaje acumulado queda por debajo.

### 7.3. Refinamiento

Los cocientes entre errores máximos de theta2 de resoluciones
consecutivas son aproximadamente:

- 300/150 s: 2,003478.
- 150/75 s: 2,001735.
- 75/37,5 s: 2,000868.

El error disminuye aproximadamente a la mitad
al dividir el paso por dos.

La tendencia observada es compatible con primer orden
temporal del acoplamiento en este escenario.
No constituye una demostración general del orden
para cualquier configuración o evento.

No se exige coincidencia exacta con la solución continua
para un paso finito.

## 8. Uso del paso nominal de 300 s

Se mantiene 300 s como resolución nominal de trabajo
para demostraciones sintéticas y exploración del núcleo,
siempre acompañada de estos errores medidos.

No se acepta como resolución universal ni como garantía
de una precisión determinada.

En el escenario 11.2, su error máximo de humedad
en la capa inferior es aproximadamente 1,05e-4 m³/m³
y el máximo error de drenaje acumulado es 0,041812 mm.

Si una aplicación exige errores menores, deberá emplear
una resolución más fina y comprobar su adecuación.

El umbral de humedad establecido para comparar 75 y 37,5 s
en el escenario 11.1 no se traslada automáticamente
como criterio de aceptación del escenario 11.2.

El cierre de masa no basta para aceptar un paso temporal.

## 9. Pruebas automatizadas

El archivo tests/test_escenarios_temporales.py añade
diez casos contando las parametrizaciones:

- Acumulados, balance y límites del escenario 11.1
  en las cuatro resoluciones.
- Criterios entre 75 y 37,5 s del escenario 11.1.
- Balance, límites y referencia de la capa superior
  del escenario 11.2 en las cuatro resoluciones.
- Reducción del error máximo de humedad de la capa 2
  y del error final de drenaje al refinar.

El archivo tests/test_verificacion_temporal.py añade
cinco pruebas del generador:

- Generación del conjunto de archivos.
- Cierre del balance en el resumen.
- Cumplimiento de los criterios del escenario 11.1.
- Comprobación de los errores analíticos del escenario 11.2.
- Escritura de resultados mediante el punto de entrada main.

Los cinco casos se superan dentro de la suite completa.

Las tablas generadas complementan estas aserciones:
no todas sus cifras están fijadas como valores de regresión.

## 10. Reproducción y trazabilidad

Desde la raíz del repositorio, con Python y pip disponibles:

```bash
python -m pip install -e ".[test]"
python -m pytest -v
python -m modelo_fisico.verificacion_temporal --salida resultados_verificacion
```

Para reproducir la versión comprobada, el repositorio debe
situarse previamente en el commit indicado en la sección 2.

Para ejecutar únicamente las pruebas de escenarios:

```bash
python -m pytest tests/test_escenarios_temporales.py -v
```

Para ejecutar únicamente las pruebas del generador:

```bash
python -m pytest tests/test_verificacion_temporal.py -v
```

La suite comprueba las aserciones automatizadas.
El comando del generador exporta las tablas del estudio.

El generador ejecuta los escenarios 11.1 y 11.2 con pasos
nominales de 300, 150, 75 y 37,5 s y escribe:

- resumen_balances.csv.
- refinamiento_11_1.csv.
- criterios_11_1.csv.
- errores_analiticos_11_2.csv.
- Ocho series temporales en CSV.
- commit.txt.

En la ejecución revisada se comprobaron doce CSV no vacíos
y la coincidencia entre commit.txt y el commit del repositorio.

Las comprobaciones adicionales del notebook verifican:

- Los tres criterios del escenario 11.1.
- El cierre del balance global en las ocho ejecuciones.
- La disminución del máximo error de theta2 al refinar
  en el escenario 11.2.

La generación desde el repositorio se ejecutó sobre el commit
indicado en la sección 2. Sus resultados son coherentes con
las cifras recogidas en este informe.

El notebook de evidencia se conserva con sus salidas.
No se presupone su publicación en el repositorio.

## 11. Limitaciones

- Parámetros, estados y entradas sintéticos.
- Sin calibración ni comparación con parcelas reales.
- Flujo exclusivamente descendente.
- Sin redistribución por debajo de capacidad de campo.
- Sin depósito superficial.
- Infiltración máxima constante.
- Extracciones prescritas, no demanda atmosférica calculada.
- Dependencia temporal de la separación de procesos.
- Dos escenarios temporales no cubren todas las configuraciones.

Las pruebas deterministas de saturación y capacidad receptora
siguen siendo necesarias: el escenario 11.1 no las sustituye.

## 12. Estado del trabajo

Completado y comprobado:

- Ejecutor temporal.
- Eventos y acumulados.
- Registro de estados, flujos y residuales.
- Balance global independiente.
- Escenarios 11.1 y 11.2.
- Comparación de cuatro resoluciones.
- Pruebas automatizadas de escenarios.

Pendiente antes del cierre:

- Publicar el procedimiento reproducible de generación
  de las tablas desde el repositorio.
- Revisar la coherencia de código, pruebas, informe y evidencias.
- Actualizar el seguimiento de la issue y del sprint.
