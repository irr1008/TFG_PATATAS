# Plan de trabajo del TFG
## Título
Sistema Inteligente de Recomendación de Riego para el Cultivo de Patata.

## Objetivo general
Diseñar e implementar un prototipo de sistema inteligente capaz de analizar
datos del cultivo, estimar su estado hídrico y recomendar acciones de riego.

## Fases previstas
### Fase 1: preparación y datos
- Documentar el problema.
- Analizar los datos de Sentinel-2.
- Identificar las variables disponibles y ausentes.
- Preparar los datos para el simulador.

### Fase 2: modelo físico

### Fase 3: simulador

### Fase 4: Machine Learning

### Fase 5: aprendizaje por refuerzo

### Fase 6: interfaz

## Estado actual
Se han creado los archivos iniciales del repositorio:
- README.md
- .gitignore
- requirements.txt
El siguiente objetivo es analizar el CSV generado por Sentinel-2 y documentar
sus características.

## Riesgos y limitaciones iniciales
- Sentinel-2 no mide directamente la humedad del suelo.
- La frecuencia temporal de las observaciones no es diaria.
- Podrán ser necesarios datos meteorológicos externos o sintéticos.
- Los parámetros físicos del suelo pueden no estar disponibles.
- La complejidad final del modelo deberá ajustarse al tiempo y a los datos.
