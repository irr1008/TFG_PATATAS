# Alcance y arquitectura inicial del sistema

Estado: validado por los tutores. Versión del
sprint 2 (issue #1).

## 1. Contexto y problema

Existe un motor de decisión de riego para patata (Agrobioma v14) que
combina la lectura de una sonda de humedad, datos meteorológicos e
índices satelitales para emitir una recomendación diaria. Los documentos
del tutor especifican una versión mejorada. El TFG contribuye a esa
mejora.

## 2. Sistema de referencia

Motor actual (v14): sonda única a 25 cm, CC y PMP tomados de la ficha de
cada parcela, ETc estimada por una fórmula empírica y recomendación en
dosis (mm) con fraccionamiento.

Motor especificado por el tutor: cuatro módulos.

| Módulo | Función | Entradas principales |
|---|---|---|
| 1. Hidrofísica del suelo | PMP y CC (teórica y calibrada) | Textura, humedad de sondas |
| 2. Crecimiento del cultivo | Zr y Kc dinámicos | DTE o GDD, NDVI |
| 3. ETo | Penman-Monteith FAO-56 | T, viento, Rn, DPV |
| 4. Decisión | Humedad ponderada, umbral, AFD, lámina Lr | Salidas de 1–3 y sondas |

## 3. Componentes que se pretende mejorar

Componentes confirmados con los tutores. Ninguno se implementa en este
sprint.
- Sustituir la ETc empírica por ETo de Penman-Monteith.
- Incorporar sondas a varias profundidades con pesos según Zr.
- Estimar Kc a partir de NDVI de Sentinel-2.
- Calibrar CC real a partir de episodios de riego o lluvia.

## 4. Entradas

| Entrada | Estado | Observaciones |
|---|---|---|
| Índices Sentinel-2 de cuatro parcelas | Disponible | Periodo provisional 01/04/2026–01/11/2026 (imágenes hasta el 22/10/2026); NDVI, NDRE, NDMI, MSI, EVI, SAVI |
| Catálogo de parcelas | Disponible | Nombre, municipio, variedad |
| Histórico de sondas | Disponible | Proporcionado por el profesorado |
| Riegos aplicados | Pendiente | |
| Meteorología (T, viento, Rn, DPV) | Pendiente | Posible uso de datos externos o sintéticos |
| Textura del suelo | Pendiente | Necesaria para Saxton & Rawls |
| Fechas agronómicas (siembra, emergencia) | Pendiente | Sin confirmar el cultivo en el periodo |
| Datos sintéticos | Sin definir | Se identificarán como tales si se usan |

## 5. Salidas previstas

Salidas del prototipo del TFG en esta fase: series satelitales
analizadas y datos preparados para un simulador. No se emiten
recomendaciones operativas de riego.

## 6. Encaje del procesamiento Sentinel-2

Sentinel-2 aporta índices por parcela y semana. NDVI alimenta la
estimación de Kc (módulo 2); esta relación está especificada pero no
implementada en este sprint. Los índices no miden humedad del suelo y
no sustituyen a las sondas.

## 7. Limitaciones y fuera de alcance

- Periodo de extracción provisional; cultivo no confirmado.
- Semanas sin observaciones conservan valores ausentes.
- No se implementa el motor completo ni se entrenan modelos.
- Faltan por incorporar riegos, meteorología, textura del suelo y
  fechas agronómicas.
