# Fuentes de meteorología y radiación para la ETo

Issue #10 · Sprint 3 · Fecha: 30/10/2026
Estado: propuesta justificada, pendiente de contraste con los tutores en la revisión del 06/11/2026.
Fuentes: variables del glosario (`docs/variables-balance-hidrico.md`), análisis del motor de referencia v14, guía FAO-56 ([Allen et al., 1998](https://www.fao.org/4/X0490E/x0490e00.htm), [capítulo 3](https://www.fao.org/4/x0490e/x0490e07.htm)) y la documentación de [AEMET OpenData](https://opendata.aemet.es/), [NASA POWER](https://power.larc.nasa.gov/docs/services/api/temporal/daily/) y [Open-Meteo](https://open-meteo.com/en/docs/historical-weather-api). Este documento no contiene claves de API ni coordenadas.

## 1. Resumen

- La ETo con Penman-Monteith FAO-56 necesita temperatura máxima y mínima, humedad relativa, viento, radiación solar y, además, la latitud y la altitud de cada parcela.
- El v14 no dispone de radiación (solo del índice UV), por lo que no puede calcular la ETo con Penman-Monteith.
- Se propone Open-Meteo (API de datos históricos) como fuente principal y AEMET OpenData como alternativa y contraste. NASA POWER queda como comprobación adicional por su resolución gruesa.
- La decisión definitiva queda pendiente de los tutores.
- Hay tres cuestiones prácticas que afectan a la issue #11: el retraso de los últimos días, la zona horaria de los días y la altura del viento.

## 2. Variables necesarias

| Variable | Símbolo | Unidad de cálculo | Uso en el v14 |
|---|---|---|---|
| Temperatura máxima y mínima del aire | T_max, T_min | °C | Sí: previsión de AEMET |
| Humedad relativa | HR | % | Sí: estación local |
| Velocidad del viento y altura de medida | u_z, z_u | m s⁻¹ y m | Sí: estación local, sin unidad ni altura indicadas |
| Radiación solar incidente | R_s | MJ m⁻² día⁻¹ | No: solo el índice UV |
| Precipitación diaria | P_d | mm día⁻¹ | Sí: lluvia acumulada en 48 h |
| Latitud y altitud de la parcela | φ, z | ° y m | No aplica: datos privados de las parcelas |

El resto de las variables de la ETo (temperatura media, presiones de vapor, pendiente de la curva, presión atmosférica, constante psicrométrica, radiación neta y viento a 2 m) se derivan de estas, como recoge el glosario. El flujo de calor del suelo se toma como 0 en paso diario.

## 3. Comparación de fuentes

| Aspecto | AEMET OpenData | NASA POWER | Open-Meteo (datos históricos) |
|---|---|---|---|
| Tipo de dato | Observaciones de estaciones | Reanálisis y satélite (MERRA-2 y CERES) | Reanálisis (ERA5, ERA5-Land) y modelo IFS |
| Resolución | Puntual, por estación | Meteorología 0,5° × 0,625° y radiación 1° × 1° | ERA5 0,25°, ERA5-Land 0,1° e IFS 9 km |
| Temperatura máxima y mínima | tmax y tmin (°C) | T2M_MAX y T2M_MIN (°C) | temperature_2m_max y temperature_2m_min (°C) |
| Humedad relativa | hrMedia, hrMax y hrMin (%) | RH2M (%) | relative_humidity_2m_mean (%; verificado). Máxima y mínima por verificar |
| Viento | velmedia (m s⁻¹; verificado en los metadatos). La API no indica la altura de medida; se espera 10 m | WS2M, ya a 2 m (m s⁻¹; verificado) | wind_speed_10m_mean, a 10 m (m s⁻¹ con `wind_speed_unit=ms`; verificado) |
| Radiación solar | No hay radiación diaria. Insolación (sol, en horas; verificado), que no todas las estaciones registran | ALLSKY_SFC_SW_DWN (MJ m⁻² día⁻¹ en la comunidad AG; verificado) | shortwave_radiation_sum (MJ m⁻²; verificado) |
| Precipitación | prec (mm) | PRECTOTCORR (mm día⁻¹) | precipitation_sum (mm) |
| ETo ya calculada | No | No | et0_fao_evapotranspiration (mm), útil como contraste |
| Retraso | Unos 4 días en la climatología diaria | Casi tiempo real; datos de calidad climática tras 2 o 3 meses | ERA5 y ERA5-Land: 5 días. IFS: sin retraso |
| Clave | Sí, gratuita. Las claves nuevas caducan a los 3 meses | No | No (uso no comercial) |
| Límites | 50 peticiones por minuto (según datos.gob.es) | 20 parámetros por petición; no repetir peticiones a una resolución mayor que la de la malla | Uso gratuito no comercial: 10.000 llamadas al día, 600 por minuto, 5.000 por hora y 300.000 al mes |
| Licencia | Uso autorizado citando a AEMET (verificado en los metadatos) | Datos abiertos de la NASA | CC BY 4.0, con atribución obligatoria |
| Zona horaria del día | Precipitación de 07 a 07; las horas de los extremos van en UTC (verificado en los metadatos) | UTC u hora solar local (parámetro `time-standard`) | Parámetro `timezone` |

Los nombres y unidades de Open-Meteo y NASA POWER se verificaron el 30/10/2026 con una petición de prueba. Los de AEMET se verificaron en los metadatos oficiales de la climatología diaria; no se probó la API porque no se pudo obtener la clave.

## 4. Radiación neta y viento a 2 m

Radiación neta (FAO-56):
- Si la fuente da R_s, se usa directamente. Si solo da horas de sol n (AEMET), R_s = (0,25 + 0,50 · n/N) · R_a, donde N son las horas de luz posibles y R_a la radiación extraterrestre, ambas a partir de la latitud y el día del año.
- Radiación neta de onda corta: R_ns = (1 − 0,23) · R_s.
- Radiación de cielo despejado: R_so = (0,75 + 2 · 10⁻⁵ · z) · R_a, con z la altitud en metros.
- Radiación neta de onda larga: R_nl = σ · (T_max,K⁴ + T_min,K⁴) / 2 · (0,34 − 0,14 · √e_a) · (1,35 · R_s/R_so − 0,35), con σ = 4,903 · 10⁻⁹ MJ K⁻⁴ m⁻² día⁻¹.
- Radiación neta: R_n = R_ns − R_nl.

Viento a 2 m: u_2 = u_z · 4,87 / ln(67,8 · z_u − 5,42). Para un viento medido a 10 m, u_2 = 0,748 · u_10. NASA POWER ya da el viento a 2 m y no necesita esta corrección.

Presión de vapor real: con la humedad relativa máxima y mínima, e_a = [e°(T_min) · HR_max/100 + e°(T_max) · HR_min/100] / 2 (ecuación 17 de FAO-56, preferible). Si solo se dispone de la media, e_a = e_s · HR_media/100 (ecuación 19, menos recomendable), con e_s la media de las presiones de vapor de saturación a T_max y T_min.

Comprobación con una petición de prueba. Con los datos de Open-Meteo del 1 al 3 de junio de 2026 para un punto genérico y una altitud supuesta (el resultado apenas cambia entre 600 y 700 m), y con la humedad media (ecuación 19), el cálculo FAO-56 de este documento da una ETo de 7,8, 7,2 y 6,6 mm día⁻¹, entre un 3 % y un 4 % por debajo de la ETo que devuelve Open-Meteo (8,1, 7,4 y 6,8). Con los datos de NASA POWER para el mismo punto da 7,2, 6,7 y 6,4 mm día⁻¹. Las dos fuentes difieren en humedad relativa (31-37 % frente a 43-47 %) y en temperatura mínima (entre 3 y 5 °C), lo que explica parte de la diferencia. La prueba sirve para comprobar las fórmulas y las unidades, no para validar la ETo frente a medidas reales.

## 5. Conversiones de unidades

| Conversión | Factor |
|---|---|
| Viento de km h⁻¹ a m s⁻¹ | Dividir entre 3,6 |
| Radiación de kWh m⁻² día⁻¹ a MJ m⁻² día⁻¹ | Multiplicar por 3,6 |
| Radiación media diaria de W m⁻² a MJ m⁻² día⁻¹ | Multiplicar por 0,0864 |
| Horas de sol en segundos (Open-Meteo) a horas | Dividir entre 3.600 |
| Radiación neta de MJ m⁻² día⁻¹ a mm día⁻¹ de agua evaporada | Multiplicar por 0,408 |
| Viento de 10 m a 2 m | Multiplicar por 0,748 |

La radiación de NASA POWER depende de la comunidad solicitada. Verificado el 30/10/2026: la comunidad agroclimatológica (AG) la entrega en MJ m⁻² día⁻¹ y la de energías renovables (RE) en kWh m⁻² día⁻¹, que es 3,6 veces menor (por ejemplo, 7,78 kWh equivalen a 28,01 MJ). Se usará la comunidad AG.

## 6. Zona horaria y retraso de los datos

- Las lecturas de las sondas están en hora local de España, y todo el histórico (29/04 a 11/09/2026) está en horario de verano (UTC+2).
- Open-Meteo calcula los límites del día con el desfase horario vigente en el momento de la petición y no cambia ese desfase si hay un cambio de hora dentro del rango. Una petición hecha tras el 25/10/2026 con `timezone=Europe/Madrid` usaría UTC+1 para todos los días del 01/04 al 01/11, aunque en verano la hora local fuera UTC+2. La solución es pedir datos horarios, convertirlos a hora local con las reglas del cambio de hora y agregarlos por día en el notebook.
- NASA POWER entrega por defecto la hora solar local, que no coincide con la hora civil de España. Si se usa, conviene pedir UTC y agregar por día local.
- El retraso afecta a la issue #11. Los últimos días del periodo (hasta el 31/10) no estarán disponibles en ERA5 (5 días de retraso) ni en la climatología diaria de AEMET (unos 4 días) hasta principios de noviembre. Los datos de esos días, si se obtienen con IFS u otro modelo sin retraso, deben marcarse como provisionales.

## 7. Propuesta

Fuente principal: Open-Meteo, con un modelo fijo (ERA5-Seamless, que combina ERA5-Land y ERA5) para toda la serie.
- Aporta directamente todas las entradas de Penman-Monteith, incluida la radiación, sin necesitar clave.
- La serie es continua y su resolución (0,1° a 0,25°) es mejor que la de NASA POWER.
- Incluye una ETo calculada con FAO-56, que sirve para comprobar nuestro cálculo.
- Limitaciones: es reanálisis y no observación directa, el viento es a 10 m, el uso gratuito es solo no comercial y exige atribución.

Alternativa y contraste: AEMET OpenData.
- Son observaciones reales y el v14 ya usa AEMET para la previsión.
- Limitaciones: requiere clave (las claves nuevas caducan a los 3 meses y la solicitud exige captcha), depende de la distancia a la estación más cercana, no da radiación (hay que estimarla con la insolación, que no todas las estaciones registran). La solicitud de la clave de la API no se completó el 30/10/2026.

NASA POWER no se propone como fuente principal por su resolución gruesa (0,5° × 0,625° en meteorología y 1° × 1° en radiación), aunque sirve para contrastar la radiación y el viento a 2 m.

La decisión definitiva depende de los tutores y de la distancia de cada parcela a las estaciones de AEMET, que se calcula con las coordenadas privadas y no se publica.

## 8. Verificaciones pendientes

| Nº | Qué verificar | Cómo |
|---|---|---|
| 1 | Altura de medida del viento en AEMET (se espera 10 m; la API no la indica) | Con la documentación de AEMET o su soporte |
| 2 | Número máximo de días por petición en la climatología diaria | Con la documentación de acceso para desarrolladores o una petición con clave |
| 3 | Qué estaciones cercanas a las parcelas registran la insolación | Con una consulta a la API cuando se obtenga la clave |
| 4 | Zona horaria de la ventana de 07 a 07 de la precipitación | Con la documentación de AEMET o su soporte |
| 5 | Respuesta real de la API con clave (nombres y unidades) | Con una petición de prueba, cuando se obtenga la clave |

Verificado el 30/10/2026: nombres y unidades de Open-Meteo y NASA POWER, y la unidad de la radiación de NASA POWER según la comunidad. En los metadatos oficiales de AEMET: nombres y unidades de las variables, precipitación de 07 a 07, insolación en horas, horas en UTC y retardo de 4 días.

## 9. Preguntas para los tutores

- ¿Podéis indicar qué estación de referencia usa el v14?
- ¿A qué altura mide el viento la estación del v14 y en qué unidad?
- ¿Se puede publicar en el repositorio la ETo calculada, sin las coordenadas?
- ¿Se ha renovado la clave de AEMET del v14? AEMET está retirando progresivamente, desde el 15/10/2026, las claves sin caducidad.

## 10. Privacidad

El repositorio no contiene claves de API ni coordenadas de las parcelas. Las peticiones a las APIs se harán desde un notebook con las coordenadas leídas del archivo privado de parcelas, y los datos descargados se guardarán en la carpeta privada de Drive.
