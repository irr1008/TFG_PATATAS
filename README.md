# Sistema Inteligente de Recomendación de Riego para Patata
Trabajo de Fin de Grado del Grado en Ingeniería Informática.

## Descripción
Este proyecto desarrolla un prototipo de sistema inteligente para recomendar
el riego de un cultivo de patata mediante la combinación de:

- Datos de observación terrestre obtenidos mediante Sentinel-2 (proporcionado por el profesorado).
- Variables meteorológicas.
- Modelado físico del balance hídrico.
- Técnicas de Machine Learning.
- Simulación del cultivo.
- Aprendizaje por refuerzo.
- Visualización de resultados mediante un dashboard.

## Objetivo principal
Diseñar e implementar un sistema capaz de estimar el estado hídrico del cultivo
de patata y recomendar acciones de riego que reduzcan el consumo de agua 
sin modificar la calidad de la producción.

## Objetivos específicos
1. Analizar datos históricos de la parcela obtenidos mediante Sentinel-2.
2. Construir una serie temporal procesada de índices espectrales.
3. Integrar variables meteorológicas y agronómicas.
4. Implementar un modelo físico de balance hídrico.
5. Desarrollar un simulador del cultivo.
6. Evaluar modelos de Machine Learning.
7. Crear un entorno de aprendizaje por refuerzo.
8. Comparar diferentes políticas de riego.
9. Desarrollar una interfaz de visualización de resultados.

## Arquitectura prevista
Sentinel-2 + meteorología + sensores
                |
                v
       Preprocesamiento de datos
                |
                v
       Modelo físico e hídrico
                |
                v
          Simulador de cultivo
                |
                v
        Entorno de aprendizaje
                |
                v
        Recomendación de riego
                |
                v
            Dashboard

## Estructura prevista
data/          Datos de entrada y datos procesados
notebooks/     Experimentos realizados en Google Colab
src/           Código fuente reutilizable
tests/         Pruebas automáticas
models/        Modelos entrenados
results/       Gráficos y métricas
docs/          Documentación técnica y seguimiento

## Tecnologías previstas
- Python
- Google Colab
- pandas
- Google Earth Engine
- GitHub
- (por el momento, iremos añadiendo más en el caso de que sean utilizadas)

## Reproducibilidad
No se almacenarán en el repositorio credenciales, tokens, claves privadas ni
datos sensibles. Los datos pesados se documentarán y se conservarán fuera del
repositorio cuando sea necesario.

## Autor
Iván Ramírez Rodríguez (irr1008@alu.ubu.es)

## Tutores
- Rubén Ruíz González
- Antonia Maiara Marques Do Nascimiento

