# Variables y unidades del balance hídrico

Issue #8 · Sprint 3 · Fecha: 27/10/2026
Estado: borrador. Suelo y decisión elaborados y revisados; cultivo, atmósfera, entradas de agua y comprobación de fórmulas pendientes.
Fuentes: documento de especificación técnica del motor mejorado, motor de referencia v14 (análisis en `docs/analisis-motor-referencia.md`) y artículo de Saxton y Rawls (2006). Los documentos del profesorado no se incluyen en el repositorio.

## 1. Convenciones

- Humedad del suelo: porcentaje volumétrico (% vol.), medido por una única sonda a 25 cm.
- Profundidades: cm. Láminas de agua: mm (1 mm equivale a 1 L/m²).
- Con la sonda a 25 cm, un punto de humedad volumétrica equivale a 2,5 mm de lámina de agua.
- Las ecuaciones de Saxton y Rawls dan la humedad como fracción decimal (por ejemplo 0,25). Para expresarla en % vol. se multiplica por 100.
- Tipos de variable: observada (medida), derivada (calculada), pendiente (sin dato todavía) y sintética (generada artificialmente; ninguna por ahora).
- No se asigna ningún valor a un parámetro sin una fuente. Los rangos y definiciones proceden del documento del tutor o de la bibliografía (issue #14); si no hay fuente, figura como pendiente.

## 2. Variables del suelo (módulo 1)

| Variable | Símbolo | Unidad | Rango o definición | Fuente | Tipo | Estado |
|---|---|---|---|---|---|---|
| Humedad volumétrica medida | θ | % vol. | Entre el PMP y la CC_real en régimen normal; por encima de la CC_real, perfil saturado; por debajo del PMP, posible error de la sonda | Sonda única a 25 cm | Observada | Histórico pendiente de analizar (#9) |
| Profundidad de la sonda | z_s | cm | 25, igual para todas las parcelas | Decisión de alcance del 26/10/2026 | Observada | Fijada por decisión; confirmación de los tutores pendiente |
| Punto de marchitez permanente | PMP | % vol. | Humedad a 1500 kPa (15 bar) | Saxton y Rawls a partir de la textura, o ficha de la parcela como en el v14 | Derivada | Pendiente de textura (#13) y de decidir la fuente |
| Capacidad de campo teórica | CC_teórica | % vol. | Humedad a 33 kPa | Saxton y Rawls a partir de la textura | Derivada | Pendiente de textura (#13) |
| Capacidad de campo real | CC_real | % vol. | Pendiente | Calibración con la sonda tras un riego o una lluvia: ventana de 24 a 48 h tras el pico de humedad y punto de inflexión de la derivada | Derivada | Pendiente de los umbrales de detección |
| Arena, limo y arcilla | S, Si, C | % en peso | Suman 100 | Textura del suelo | Pendiente | Pendiente de los tutores (#13) |
| Materia orgánica | MO | % en peso | Hasta 8 (límite de las ecuaciones) | Textura del suelo | Pendiente | Pendiente de los tutores (#13) |
| Ajustes opcionales de densidad, grava y salinidad | DF, grava, CE | Factor, %, dS/m | DF entre 0,9 y 1,3 | Saxton y Rawls | Pendiente | Opcionales; no se usarán sin datos |
| Umbrales de humedad de la ficha (mínima, objetivo, máxima) | θ_min, θ_obj, θ_max | % vol. | Pendiente | Ficha de la parcela del v14 | Pendiente | Conciliación con el umbral de MAD por decidir |

## 3. Variables de decisión (módulo 4)

| Variable | Símbolo | Unidad | Rango o definición | Fuente | Tipo | Estado |
|---|---|---|---|---|---|---|
| Humedad del perfil | θ_pond | % vol. | Igual que θ | Con una única sonda, θ_pond equivale a θ | Derivada | Confirmación pendiente |
| Profundidad radicular efectiva | Z_r | cm | Pendiente: el v14 la tabula por estadio y la especificación no da un máximo | Especificación del tutor (dinámica con DTE o GDD) | Derivada | Método pendiente. Los tramos de 15 y 35 cm solo definen la matriz de pesos, que no se aplica con una única sonda |
| Agotamiento mínimo admisible | MAD | Adimensional | Entre 0,35 y 0,50 según el estadio | Especificación del tutor | Pendiente | Tabla por estadio pendiente |
| Agua fácilmente disponible | AFD | mm | Pendiente | Especificación del tutor | Derivada | Definición y unidad pendientes (factor 1 − MAD y factor ×10) |
| Umbral de recarga | θ_rec | % vol. | Entre PMP y CC_real | CC_real − (CC_real − PMP) × MAD | Derivada | Depende de CC_real y MAD |
| Lámina de riego | L_r | mm | Mayor o igual que 0 | (CC_real − θ_pond) / 100 × Z_r × 10 | Derivada | Profundidad de cálculo por decidir (Z_r o z_s) |
| Alerta de riego | A | Sí o no | Dos valores | Se activa cuando θ_pond es menor o igual que θ_rec | Derivada | Salida del motor |

La lámina óptima que devuelve el motor mejorado es L_r.

## 4. Decisiones de definición

- 27/10/2026: la humedad se expresa en % volumétrico, como el motor v14 y los datos de los tutores.
- 27/10/2026: una lectura de la sonda por debajo del PMP se trata como posible error. El v14 la interpreta como perfil agotado, por lo que la diferencia se contrastará con los tutores.
- 27/10/2026: la sonda está a 25 cm de profundidad en todas las parcelas.
- 27/10/2026: la CC_real es la referencia superior de la humedad por el momento; no se usa la humedad de saturación.

## 5. Pendiente

- Cultivo: Kc, a y b de la relación con NDVI, días tras emergencia y GDD.
- Atmósfera: temperatura, viento a 2 m, radiación neta, flujo de calor del suelo, déficit de presión de vapor, pendiente de la curva, constante psicrométrica y ETo.
- Entradas de agua: lluvia, lluvia efectiva y riego.
- Comprobación dimensional de AFD, umbral de recarga y lámina de riego.
- Clasificación final de cada variable y registro de discrepancias.
