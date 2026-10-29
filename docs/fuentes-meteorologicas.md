# Fuentes de meteorología y radiación para la ETo

Issue #10 · Sprint 3 · Fecha: 30/10/2026
Estado: propuesta justificada, pendiente de contraste con los tutores en la revisión del 30/10/2026.
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
| Humedad relativa | hrMedia, hrMax y hrMin (%) | RH2M (%) | relative_humidity_2m_mean, máxima y mínima (%) |
| Viento | velmedia (m s⁻¹); altura de medida por confirmar | WS2M, ya a 2 m (m s⁻¹) | wind_speed_10m_mean y máxima, a 10 m (km h⁻¹ por defecto; admite m s⁻¹) |
| Radiación solar | No hay radiación diaria; sí horas de sol (sol) | ALLSKY_SFC_SW_DWN | shortwave_radiation_sum (MJ m⁻²) |
| Precipitación | prec (mm) | PRECTOTCORR (mm día⁻¹) | precipitation_sum (mm) |
| ETo ya calculada | No | No | et0_fao_evapotranspiration (mm), útil como contraste |
| Retraso | Unos 4 días en la climatología diaria | Casi tiempo real; datos de calidad climática tras 2 o 3 meses | ERA5 y ERA5-Land: 5 días. IFS: sin retraso |
| Clave | Sí, gratuita y sin caducidad | No | No (uso no comercial) |
| Límites | 40 peticiones por minuto y usuario | 20 parámetros por petición; no repetir peticiones a una resolución mayor que la de la malla | Uso gratuito no comercial: 10.000 llamadas al día, 600 por minuto, 5.000 por hora y 300.000 al mes |
| Licencia | Condiciones de la nota legal de AEMET | Datos abiertos de la NASA | CC BY 4.0, con atribución obligatoria |
| Zona horaria del día | Pendiente de confirmar con los metadatos | UTC u hora solar local (parámetro `time-standard`) | Parámetro `timezone` |

Los nombres de variables de AEMET y de NASA POWER proceden de la documentación y de ejemplos de terceros, y deben confirmarse con los metadatos de cada API antes de usarlos (apartado 8).

## 4. Radiación neta y viento a 2 m

Radiación neta (FAO-56):
- Si la fuente da R_s, se usa directamente. Si solo da horas de sol n (AEMET), R_s = (0,25 + 0,50 · n/N) · R_a, donde N son las horas de luz posibles y R_a la radiación extraterrestre, ambas a partir de la latitud y el día del año.
- Radiación neta de onda corta: R_ns = (1 − 0,23) · R_s.
- Radiación de cielo despejado: R_so = (0,75 + 2 · 10⁻⁵ · z) · R_a, con z la altitud en metros.
- Radiación neta de onda larga: R_nl = σ · (T_max,K⁴ + T_min,K⁴) / 2 · (0,34 − 0,14 · √e_a) · (1,35 · R_s/R_so − 0,35), con σ = 4,903 · 10⁻⁹ MJ K⁻⁴ m⁻² día⁻¹.
- Radiación neta: R_n = R_ns − R_nl.

Viento a 2 m: u_2 = u_z · 4,87 / ln(67,8 · z_u − 5,42). Para un viento medido a 10 m, u_2 = 0,748 · u_10. NASA POWER ya da el viento a 2 m y no necesita esta corrección.

Presión de vapor real: e_a se obtiene de la humedad relativa media y de las presiones de vapor de saturación a T_max y T_min, según FAO-56.

## 5. Conversiones de unidades

| Conversión | Factor |
|---|---|
| Viento de km h⁻¹ a m s⁻¹ | Dividir entre 3,6 |
| Radiación de kWh m⁻² día⁻¹ a MJ m⁻² día⁻¹ | Multiplicar por 3,6 |
| Radiación media diaria de W m⁻² a MJ m⁻² día⁻¹ | Multiplicar por 0,0864 |
| Horas de sol en segundos (Open-Meteo) a horas | Dividir entre 3.600 |
| Radiación neta de MJ m⁻² día⁻¹ a mm día⁻¹ de agua evaporada | Multiplicar por 0,408 |
| Viento de 10 m a 2 m | Multiplicar por 0,748 |

La radiación de NASA POWER depende de la comunidad solicitada: según una documentación de terceros, la comunidad agroclimatológica (AG) la sirve en MJ m⁻² día⁻¹ y la de energías renovables (RE) en kWh m⁻² día⁻¹, con valores 3,6 veces distintos. Hay que verificar la unidad en el metadato de la respuesta.

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
- Limitaciones: requiere clave, depende de la distancia a la estación más cercana, no da radiación (hay que estimarla con las horas de sol) y puede tener huecos.

NASA POWER no se propone como fuente principal por su resolución gruesa (0,5° × 0,625° en meteorología y 1° × 1° en radiación), aunque sirve para contrastar la radiación y el viento a 2 m.

La decisión definitiva depende de los tutores y de la distancia de cada parcela a las estaciones de AEMET, que se calcula con las coordenadas privadas y no se publica.

## 8. Verificaciones pendientes

| Nº | Qué verificar | Cómo |
|---|---|---|
| 1 | Nombres y unidades de las variables de AEMET y NASA POWER | Con los metadatos de cada API |
| 2 | Altura de medida del viento en AEMET (se espera 10 m, el estándar) | Con la documentación de AEMET o su soporte |
| 3 | Ventana de acumulación de la precipitación diaria de AEMET | Con los metadatos |
| 4 | Número máximo de días por petición en la climatología diaria de AEMET | Con la documentación de acceso para desarrolladores |
| 5 | Unidad de la radiación en NASA POWER según la comunidad | Con una petición de prueba |
| 6 | Zona horaria del día en AEMET | Con los metadatos |

## 9. Preguntas para los tutores

- ¿Se prefiere una fuente de observación (AEMET) o una de reanálisis (Open-Meteo) para la ETo?
- ¿A qué altura mide el viento la estación del v14 y en qué unidad?
- ¿Se puede publicar en el repositorio la ETo calculada, sin las coordenadas?

## 10. Privacidad

El repositorio no contiene claves de API ni coordenadas de las parcelas. Las peticiones a las APIs se harán desde un notebook con las coordenadas leídas del archivo privado de parcelas, y los datos descargados se guardarán en la carpeta privada de Drive.
