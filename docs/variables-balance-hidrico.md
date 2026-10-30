# Variables y unidades del balance hídrico

Issue #8 · Sprint 3 · Fecha: 27, 28 y 29/10/2026
Estado: versión completa, pendiente de contraste con los tutores en la revisión del 06/11/2026.
Fuentes: documento de especificación técnica del motor mejorado, motor de referencia v14 (análisis en `docs/analisis-motor-referencia.md`), artículo de Saxton y Rawls (2006) y guía FAO-56 ([Allen et al., 1998](https://www.fao.org/4/X0490E/x0490e00.htm)). Los documentos del profesorado no se incluyen en el repositorio.

## 1. Convenciones

- Humedad del suelo: porcentaje volumétrico (% vol.), medido por una única sonda a 25 cm.
- Profundidades: cm. Láminas de agua: mm (1 mm equivale a 1 L/m² y a 10 m³/ha).
- Con la sonda a 25 cm, un punto de humedad volumétrica equivale a 2,5 mm de lámina de agua.
- Las ecuaciones de Saxton y Rawls dan la humedad como fracción decimal (por ejemplo 0,25). Para expresarla en % vol. se multiplica por 100.
- Tipos de variable: observada (medida y con datos ya disponibles en el proyecto), derivada (calculada), pendiente (sin dato todavía, aunque sea medible) y sintética (generada artificialmente; ninguna por ahora).
- No se asigna ningún valor a un parámetro sin una fuente. Los rangos y definiciones proceden del documento del tutor, de FAO-56 o de la bibliografía (issue #14); si no hay fuente, figura como pendiente.

## 2. Variables del suelo (módulo 1)

| Variable | Símbolo | Unidad | Rango o definición | Fuente | Frecuencia | Tipo | Estado |
|---|---|---|---|---|---|---|---|
| Humedad volumétrica medida | θ | % vol. | Entre el PMP y la CC_real en régimen normal; por encima de la CC_real, perfil saturado; por debajo del PMP, posible error de la sonda | Sonda a 25 cm | Una lectura cada 4 h de mediana, con intervalos irregulares y huecos (#9) | Observada | Histórico analizado (29/04 a 11/09/2026); unidad (% vol.) |
| Profundidad de la sonda | z_s | cm | 25, igual para todas las parcelas | Decisión de alcance del 26/10/2026 | Constante | Observada | Fijada por el dirigente de las sondas |
| Punto de marchitez permanente | PMP | % vol. | Humedad a 1500 kPa (15 bar) | Saxton y Rawls a partir de la textura, o ficha de la parcela como en el v14 | Constante por parcela | Derivada | Pendiente de textura (#13) y de decidir la fuente |
| Capacidad de campo teórica | CC_teórica | % vol. | Humedad a 33 kPa | Saxton y Rawls a partir de la textura | Constante por parcela | Derivada | Pendiente de textura (#13) |
| Capacidad de campo real | CC_real | % vol. | Pendiente | Calibración con la sonda tras un riego o una lluvia: ventana de 24 a 48 h tras el pico de humedad y punto de inflexión de la derivada | Se actualiza al detectar un evento de riego o lluvia | Derivada | Pendiente de los umbrales de detección |
| Arena, limo y arcilla | S, Si, C | % en peso | Suman 100 | Textura del suelo | Constante por parcela | Pendiente | Pendiente de los tutores (#13) |
| Materia orgánica | MO | % en peso | Hasta 8 (límite de las ecuaciones) | Textura del suelo | Constante por parcela | Pendiente | Pendiente de los tutores (#13) |
| Ajustes opcionales de densidad, grava y salinidad | DF, grava, CE | Factor, %, dS/m | DF entre 0,9 y 1,3 | Saxton y Rawls | Constante por parcela | Pendiente | Opcionales; no se usarán sin datos |
| Umbrales de humedad de la ficha (mínima, objetivo, máxima) | θ_min, θ_obj, θ_max | % vol. | Pendiente | Ficha de la parcela del v14 | Constante por parcela | Pendiente | Conciliación con el umbral de MAD por decidir |

## 3. Variables del cultivo (módulo 2)

| Variable | Símbolo | Unidad | Rango o definición | Fuente | Frecuencia | Tipo | Estado |
|---|---|---|---|---|---|---|---|
| Fecha de siembra | F_siem | Fecha | Fecha del calendario | Tutores | Una por campaña | Pendiente | Pendiente de los tutores (#13) |
| Fecha de emergencia | F_em | Fecha | Posterior a la siembra | Tutores | Una por campaña | Pendiente | Pendiente de los tutores (#13) |
| Días tras emergencia | DTE | Días | Entero mayor o igual que 0: fecha del día menos F_em | Fecha de emergencia | Diaria | Derivada | Pendiente de F_em |
| Temperatura base | T_base | °C | Pendiente | Tutores o bibliografía (#14) | Constante | Pendiente | La especificación no la da |
| Grados día acumulados | GDD | °C·día | Suma diaria desde la emergencia; fórmula exacta pendiente | Temperatura diaria y T_base | Diaria | Derivada | Fórmula y T_base pendientes |
| Estadio fenológico | — | Categoría | Lista de estadios del v14, de siembra a recolección | Ficha de la parcela en el v14; en el motor mejorado, DTE o GDD | Diaria | Pendiente | Cómo se determina el estadio, por decidir |
| Índice de vegetación | NDVI | Adimensional | Entre −1 y 1 | Sentinel-2 (extracción del sprint 2) | Mediana de 4 o 5 días entre imágenes, con huecos | Observada | Disponible hasta el 22/10/2026; ampliación en la #12 |
| Parámetros de la relación Kc–NDVI | a, b | Adimensional | Pendiente | Tutores (calibrados por cultivo según la especificación) | Constantes | Pendiente | Pendiente de los tutores (#13) |
| Coeficiente de cultivo | Kc | Adimensional | Pendiente | a·NDVI + b, o tablas por GDD; el v14 usa un valor fijo de la ficha | Diaria | Derivada | Pendiente de a y b |

La profundidad radicular efectiva Z_r y el MAD se definen en el apartado de decisión.

## 4. Variables de la atmósfera y de la ETo (módulo 3)

| Variable | Símbolo | Unidad | Rango o definición | Fuente | Frecuencia | Tipo | Estado |
|---|---|---|---|---|---|---|---|
| Temperatura máxima y mínima del aire | T_max, T_min | °C | Pendiente | Fuente meteorológica por decidir (#10) | Diaria | Pendiente | Pendiente de la fuente y de la descarga (#11) |
| Temperatura media diaria del aire a 2 m | T | °C | (T_max + T_min) / 2 | Derivada de T_max y T_min | Diaria | Derivada | Depende de la fuente |
| Humedad relativa | HR | % | Entre 0 y 100 | Fuente meteorológica por decidir (#10) | Diaria | Pendiente | Necesaria para la presión de vapor real |
| Velocidad del viento medida y altura de medida | u_z, z_u | m s⁻¹ y m | Pendiente | Fuente meteorológica (el v14 no indica la unidad) | Diaria | Pendiente | Unidad y altura de medida por confirmar |
| Velocidad del viento a 2 m | u_2 | m s⁻¹ | Corrección logarítmica de u_z a 2 m | FAO-56 | Diaria | Derivada | Depende de u_z y z_u |
| Radiación solar incidente | R_s | MJ m⁻² día⁻¹ | Pendiente | Fuente meteorológica por decidir (#10); el v14 solo usa el índice UV | Diaria | Pendiente | Si la fuente la da en kWh m⁻² día⁻¹, se multiplica por 3,6 |
| Radiación neta | R_n | MJ m⁻² día⁻¹ | R_ns − R_nl (onda corta menos onda larga) | FAO-56, a partir de R_s, temperatura y presión de vapor | Diaria | Derivada | Depende de R_s |
| Flujo de calor del suelo | G | MJ m⁻² día⁻¹ | Aproximadamente 0 en paso diario | Especificación del tutor y FAO-56 | Diaria | Derivada | Aproximación aceptada |
| Presión de vapor de saturación, real y su déficit | e_s, e_a, e_s − e_a | kPa | e_s a partir de T; e_a a partir de HR | FAO-56 | Diaria | Derivada | Depende de T y HR |
| Pendiente de la curva de presión de vapor | Δ | kPa °C⁻¹ | Función de T | FAO-56 | Diaria | Derivada | Depende de T |
| Altitud de la parcela | z | m | Pendiente | Ubicación de la parcela (dato privado) | Constante | Pendiente | Se obtiene del archivo privado de parcelas |
| Presión atmosférica | P | kPa | Función de la altitud | FAO-56 | Constante por parcela | Derivada | Depende de z |
| Constante psicrométrica | γ | kPa °C⁻¹ | Función de P | FAO-56 | Constante por parcela | Derivada | Depende de P |
| Evapotranspiración de referencia | ETo | mm día⁻¹ | Penman-Monteith FAO-56 | Especificación del tutor y FAO-56 | Diaria | Derivada | Depende de todas las anteriores |
| Evapotranspiración del cultivo | ETc | mm día⁻¹ | Kc × ETo | FAO-56 | Diaria | Derivada | La especificación no indica cómo se usa en la decisión |

## 5. Entradas de agua

| Variable | Símbolo | Unidad | Rango o definición | Fuente | Frecuencia | Tipo | Estado |
|---|---|---|---|---|---|---|---|
| Precipitación diaria | P_d | mm día⁻¹ | Mayor o igual que 0 | Fuente meteorológica por decidir (#10) | Diaria | Pendiente | Pendiente de la fuente y de la descarga (#11) |
| Precipitación acumulada en 48 h | P_48 | mm | Suma de dos días de P_d | Derivada de P_d | Diaria | Derivada | Entrada del v14; su uso en el motor mejorado está por decidir |
| Lluvia efectiva | P_ef | mm | P_48 por una eficiencia que depende de la textura en el v14 | v14 | Diaria | Derivada | El motor mejorado no la define |
| Alerta de lavado | — | Sí o no | Dos valores | v14 (previsión meteorológica) | Diaria | Pendiente | Uso en el motor mejorado por decidir |
| Riego aplicado | I | mm | Mayor o igual que 0 | Registro de riegos de los tutores | Por evento | Pendiente | Pendiente de los tutores (#13) |

## 6. Variables de decisión (módulo 4)

| Variable | Símbolo | Unidad | Rango o definición | Fuente | Frecuencia | Tipo | Estado |
|---|---|---|---|---|---|---|---|
| Humedad del perfil | θ_pond | % vol. | Igual que θ | Con una única sonda, θ_pond equivale a θ | Diaria | Derivada | Confirmación pendiente |
| Profundidad radicular efectiva | Z_r | cm | Pendiente: el v14 la tabula por estadio y la especificación no da un máximo | Especificación del tutor (dinámica con DTE o GDD) | Diaria | Derivada | Método pendiente. Los tramos de 15 y 35 cm solo definen la matriz de pesos, que no se aplica con una única sonda |
| Agotamiento mínimo admisible | MAD | Adimensional | Entre 0,35 y 0,50 según el estadio | Especificación del tutor | Por estadio | Pendiente | Tabla por estadio pendiente |
| Agua fácilmente disponible | AFD | mm | Pendiente | Especificación del tutor | Diaria | Derivada | Definición y unidad pendientes (apartado 8) |
| Umbral de recarga | θ_rec | % vol. | Entre PMP y CC_real | CC_real − (CC_real − PMP) × MAD | Diaria | Derivada | Depende de CC_real y MAD |
| Lámina de riego | L_r | mm | Mayor o igual que 0 | (CC_real − θ_pond) / 100 × Z_r × 10 | Diaria | Derivada | Profundidad de cálculo por decidir (Z_r o z_s) |
| Alerta de riego | A | Sí o no | Dos valores | Se activa cuando θ_pond es menor o igual que θ_rec | Diaria | Derivada | Salida del motor |

La lámina óptima que devuelve el motor mejorado es L_r.

## 7. Comprobación dimensional de las fórmulas

| Fórmula | Comprobación | Resultado |
|---|---|---|
| ETo (Penman-Monteith) | Las unidades de la tabla de variables dan mm día⁻¹; el factor 0,408 convierte MJ m⁻² día⁻¹ en mm día⁻¹ | Coherente con FAO-56 |
| ETc = Kc × ETo | Adimensional por mm día⁻¹ | mm día⁻¹ |
| θ_rec = CC_real − (CC_real − PMP) × MAD | % vol. por una resta y un producto con un factor adimensional | % vol. |
| L_r = (CC_real − θ_pond) / 100 × Z_r × 10 | (% vol. / 100) por cm por 10 | mm. Con 5 puntos de déficit y Z_r = 25 cm da 12,5 mm |
| Conversión del v14 | Un punto de VWC equivale a z_s / 10 mm | Con z_s = 25 cm, 2,5 mm por punto; coincide con L_r para la misma profundidad |
| AFD según el texto del tutor | (CC_real − PMP) / 100 × Z_r × (1 − MAD) | Con Z_r en cm queda en cm: falta el factor ×10. Además, con (1 − MAD) no coincide con FAO-56 (RAW = p × TAW) si MAD es la fracción agotable |
| Saxton y Rawls | Fracción decimal por 100 | % vol. |
| Radiación | 1 kWh equivale a 3,6 MJ | R_s en MJ m⁻² día⁻¹ si la fuente da kWh m⁻² día⁻¹ |
| Dosis | 1 mm equivale a 10 m³/ha | Coherente con el v14 |

## 8. Discrepancias y asuntos abiertos

| Nº | Asunto | Estado |
|---|---|---|
| 1 | AFD: factor (1 − MAD) frente al MAD del umbral de recarga, y falta del factor ×10 con Z_r en cm | Consultado a los tutores |
| 2 | Profundidad de cálculo de L_r y del AFD: Z_r (especificación) o z_s (v14) | Consultado a los tutores |
| 3 | Lectura por debajo del PMP: posible error (decisión de este proyecto) frente a perfil agotado (v14) | Consultado a los tutores |
| 4 | Umbrales de humedad de la ficha frente al umbral basado en MAD | Consultado a los tutores |
| 5 | Matriz de pesos por profundidad frente a la sonda única | Resuelto por decisión de alcance; eliminada |
| 6 | Kc diario frente a NDVI cada unos 5 días, sin interpolar | Por decidir con los tutores |
| 7 | Unidad y altura de medida del viento en el v14 | Consultado a los tutores |
| 8 | El v14 solo dispone del índice UV; Penman-Monteith necesita radiación neta | Por resolver en la #10 |
| 9 | La ETo del v14 es empírica (ETc dividida entre Kc), no comparable con Penman-Monteith | Se sustituye |
| 10 | La especificación no indica cómo se usan Kc y ETc en la decisión (el diagrama menciona la demanda del cultivo) | Por consultar |
| 11 | Fórmula de GDD, temperatura base y método para determinar el estadio fenológico | Por consultar |

## 9. Decisiones de definición

- 27/10/2026: la humedad se expresa en % volumétrico, como el motor v14 y los datos de los tutores.
- 27/10/2026: una lectura de la sonda por debajo del PMP se trata como posible error. El v14 la interpreta como perfil agotado, por lo que la diferencia se contrastará con los tutores.
- 27/10/2026: la sonda está a 25 cm de profundidad en todas las parcelas.
- 27/10/2026: la CC_real es la referencia superior de la humedad por el momento; no se usa la humedad de saturación.

## 10. Resumen de la clasificación

| Bloque | Variables | Observadas | Derivadas | Pendientes |
|---|---:|---:|---:|---:|
| Suelo | 9 | 2 | 3 | 4 |
| Cultivo | 9 | 1 | 3 | 5 |
| Atmósfera y ETo | 15 | 0 | 10 | 5 |
| Entradas de agua | 5 | 0 | 2 | 3 |
| Decisión | 7 | 0 | 6 | 1 |
| Total | 45 | 3 | 24 | 18 |

No hay variables sintéticas. Los datos pendientes dependen de los tutores (#13), de la elección de la fuente meteorológica (#10) y de la descarga de datos (#11).
