# Especificación del modelo físico de humedad del suelo

Versión: 0.1 · Fecha: 07/11/2026.
Estado: propuesta técnica inicial; no aprobada aún como especificación final por los tutores.
Origen: cambio de enfoque comunicado tras la reunión del 06/11/2026.

## 1. Objetivo y alcance

Desarrollar un simulador independiente de Agrobioma v14 que represente la evolución del agua en un perfil de suelo ante meteorología y riego, conserve la masa y permita calibrar un conjunto reducido de parámetros.

Primera versión propuesta: balance hídrico unidimensional por capas y experimentos sintéticos reproducibles. La calibración con datos reales se incorpora después de verificar el núcleo. No incluye recomendaciones automáticas ni despliegue operativo. El acoplamiento térmico se reserva para una versión posterior, pendiente de confirmar el alcance con los tutores.

## 2. Procedencia de los requisitos

| Categoría | Contenido |
|---|---|
| Orientación de la reunión según notas | Modelo simple, pocas entradas y capas, profundidad de interés de 25 cm, evolución aproximada cada 5 min, VPD y autocalibración |
| Propuesta de implementación | Depósitos por capas, balances conservativos, configuración externa y pruebas sintéticas antes de calibrar |
| Pendiente | Geometría final, leyes de flujos, demanda evaporativa y transpirativa, fronteras, parámetros y tolerancias |

No se trasladan constantes del v14 sin justificación independiente.

## 3. Datos disponibles y límites

- CSV: lecturas de sonda y mensajes; los mensajes no demuestran la ejecución del riego.
- PDF: fichas exportadas de parcelas con clases texturales y algunos parámetros. No equivalen a informes completos de laboratorio.
- Meteorología: estudio previo reutilizable; fuente y resolución que se usarán en el modelo pendientes de cerrar.
- Sentinel-2: infraestructura reutilizable; integración aplazada hasta justificar su aportación.
- Algunas fichas contienen estimaciones de capacidad de campo con un método automático y un indicador de confianza. No se consideran mediciones independientes de referencia ni valores validados para evaluar el nuevo modelo.
- Los campos de arena y arcilla aparecen vacíos en las fichas inspeccionadas. No se dispone de porosidad medida en ellas. No se deducen porcentajes granulométricos únicos de una clase textural.
- Las profundidades de las fichas discrepan de la hipótesis anterior de 25 cm para todas las parcelas. No se fijará esa profundidad como valor real universal.
- Los registros vinculados de octubre en los PDF no aportan por sí solos una serie numérica completa ni amplían automáticamente el histórico CSV analizado.

## 4. Estados, geometría y observación

Perfil de N capas configurables, con límites z_superior y z_inferior en m y espesor L_j en m.

Estado principal: humedad volumétrica theta_j en m³/m³. Almacenamiento equivalente: S_j = 1000 · L_j · theta_j, en mm.

La observación en % vol. se convierte mediante theta_obs = humedad_pct / 100. No se confunde la profundidad de una sonda con el espesor de la capa ni con la profundidad radicular.

Se propone empezar con dos capas; número y límites aún por decidir. El operador de observación H(theta, z_sonda) indicará qué valor del modelo se compara con la sonda y qué hipótesis de representatividad utiliza. Si la sonda cae en una interfaz se definirá una convención explícita, sin elegirla implícitamente.

## 5. Balance y unidades

Durante cada intervalo:

S_j(n+1) = S_j(n) + F_entrada,j − F_salida,j − E_j − T_j.

Todos los términos de flujo de esta ecuación son láminas acumuladas durante el intervalo, en mm; no tasas. Los intercambios internos deben restarse de una capa y sumarse a la siguiente con idéntico valor.

Balance global, sin ascenso capilar ni flujo lateral en la primera versión:

Delta S_perfil = P + I_superficie − RO − DP − E − T.

P e I_superficie son el agua que alcanza la superficie modelada. Si se parte de riego bruto o lluvia sobre dosel, las pérdidas de aplicación e interceptación se representarán o se declararán omitidas. Nunca se descontarán dos veces.

Si hay almacenamiento superficial, se incluirá en el estado y en Delta S_total. Sin ese almacenamiento, el agua que no infiltra debe contabilizarse explícitamente como escorrentía o salida superficial.

Residual: epsilon = Delta S_total − (P + I_superficie − RO − DP − E − T). Se registrará por paso y acumulado.

## 6. Procesos y cierres pendientes

| Proceso | Requisito de especificación antes de implementar |
|---|---|
| Infiltración | Ley, capacidad de entrada, unidades y tratamiento del exceso |
| Transferencia y drenaje | Ley dependiente del estado, parámetros y límites de transferencia |
| Evaporación | Demanda atmosférica y limitación por agua disponible |
| Transpiración | Representación del cultivo, distribución de extracción y estrés |
| Frontera inferior | Drenaje libre u otra condición justificada |
| Inicialización | Perfil inicial, incertidumbre y eventual calentamiento del modelo |

Una posibilidad a evaluar es drenaje dependiente del exceso sobre capacidad de campo, con una escala temporal explícita. No se establece aquí como ley aprobada. La capacidad de campo no es el máximo físico de almacenamiento: se permite agua por encima de ella hasta el límite de saturación definido.

El modelo de depósitos no pretende resolver Richards ni reproducir todos los procesos de flujo no saturado. Sus simplificaciones deben documentarse.

## 7. Entradas y variables derivadas

Meteorología candidata: temperatura del aire (°C), humedad relativa (%), radiación solar (W/m² con intervalo conocido, o energía por intervalo), viento (m/s con altura), precipitación (mm por intervalo).

Riego: inicio, fin o duración, lámina o volumen, área de referencia y estado de confirmación. Conversión de volumen: I_mm = volumen_L / area_m2. Si se usa caudal, se necesita además la duración y el área realmente regada.

VPD instantáneo propuesto:

e_s(T) = 0,6108 · exp(17,27 · T / (T + 237,3)) [kPa].
VPD = e_s(T) · (1 − HR/100) [kPa].

Se validarán T y HR. El VPD no sustituye a una ley de evapotranspiración. FAO-56 es una referencia candidata para demanda atmosférica; no se trasladará una ETo diaria directamente a tasas de 5 min sin una hipótesis documentada. La evapotranspiración de referencia no se identifica automáticamente con la evapotranspiración real del cultivo.

Color del suelo, temperatura del suelo y presión ambiental solo se incorporarán cuando exista una relación definida con un proceso o una necesidad de evaluación. No todas las variables de las notas serán entradas independientes.

## 8. Tiempo

Paso nominal propuesto: 300 s (equivalente a 5 minutos), configurable. Frecuencia de integración, salida, observación y forzantes se registran por separado.

Tiempo interno en UTC; hora local con zona IANA explícita para interpretación y agregación. Los intervalos indicarán si el sello temporal corresponde al inicio o al final.

Los datos horarios no se convierten en observaciones de 5 min. Si se mantienen constantes o se reparten dentro de la hora, se documentará como supuesto. Los acumulados deben conservarse. Un dato desconocido no se transforma en cero.

Se estudiará convergencia temporal y, si es necesario, subpasos para evitar extraer más agua de la disponible o transferir más de la que admite la capa receptora.

## 9. Parámetros y calibración

Clasificación: medidos, procedentes de ficha, estimados bibliográficamente, calibrados y no identificables. Todos tendrán unidades, fuente, límites y versión.

La autocalibración significa ajuste automático de un conjunto pequeño de parámetros dentro de límites físicos, no identificación garantizada de todos los parámetros ni del tipo exacto de suelo.

Primera fase: verificar el núcleo con parámetros sintéticos conocidos. Segunda: ajustar solo parámetros con evidencia y comprobar sensibilidad y posibles compensaciones. Separar periodos de calibración y evaluación y no usar estimaciones del sistema anterior como verdad de referencia.

No ajustar simultáneamente riego desconocido y todos los parámetros del suelo como si el resultado fuera único. Clasificar los eventos: recomendado, declarado, aplicado confirmado y desconocido. Los escenarios sin información de riego se identificarán como tales.

## 10. Pruebas de aceptación

- Sin entradas ni salidas: almacenamiento constante.
- Aporte conocido sin pérdidas: aumento equivalente de almacenamiento.
- Transferencia interna: conservación del total del perfil.
- Saturación: exceso contabilizado; no desaparición de agua al recortar estados.
- Secado: extracción limitada al agua disponible según la ley especificada.
- Conversiones de volumen y unidades comprobadas.
- Geometría y parámetros inválidos rechazados con errores claros.
- Residual de masa por paso y acumulado bajo tolerancia numérica documentada, absoluta y relativa.
- Convergencia al reducir el paso temporal sobre escenarios definidos.
- Calibración sintética y evaluación temporal separada antes de interpretar resultados reales.

Las tolerancias y métricas finales se fijarán en el protocolo de pruebas, no después de observar los resultados.

## 11. Arquitectura y entregables propuestos

- Núcleo Python independiente de Drive, APIs y notebooks.
- Adaptadores de datos separados del integrador.
- Configuración de capas y parámetros externa.
- Pruebas automatizadas con datos sintéticos públicos.
- Notebook de demostración sin salidas privadas.
- Inventario privado de datos y discrepancias con procedencia.

## 12. Decisiones por cerrar antes de programar

1. Dos capas iniciales y límites del perfil.
2. Profundidad y periodo de instalación real de cada sonda.
3. Leyes de infiltración, drenaje y evapotranspiración y sus parámetros mínimos.
4. Frontera inferior y tratamiento del cultivo.
5. Disponibilidad real de datos meteorológicos y eventos de riego.
6. Parámetros ajustables y criterios de evaluación.

## 13. Fuentes

- Notas de la reunión del 06/11/2026 y aclaraciones del 07/11/2026.
- Cuatro exportaciones privadas de fichas de parcelas; no se publican ni se copian sus identificadores, coordenadas ni datos personales.
- Allen et al. (1998), FAO Irrigation and Drainage Paper 56: https://www.fao.org/4/X0490E/x0490e00.htm ; balance: https://www.fao.org/4/X0490E/x0490e0e.htm ; meteorología y presiones de vapor: https://www.fao.org/4/x0490e/x0490e07.htm.
