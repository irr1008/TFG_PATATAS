# Uso y pruebas del núcleo hidráulico

## 1. Alcance

El paquete `modelo_fisico` contiene la configuración, los estados,
las entradas y las conversiones del núcleo hidráulico.

Este incremento no calcula flujos, no ejecuta series temporales
y no calibra parámetros.

El núcleo no necesita Drive, APIs, credenciales ni datos privados.

## 2. Instalación y pruebas

Requisito declarado: Python 3.11 o posterior.

Entorno utilizado durante el desarrollo de la #18:
Python 3.13.18 y pytest 8.4.2 en Google Colab.

Esto no constituye una comprobación de todas las versiones de Python
admitidas por la configuración del paquete.

Desde la raíz del repositorio:

```bash
python -m pip install -e ".[test]"
python -m pytest -v
```

`requirements.txt` contiene las dependencias de los notebooks.
No es necesario instalarlo para ejecutar estas pruebas del núcleo.

En una celda de Colab, la instalación equivalente es:

```python
%pip install -e ".[test]"
```

Para ejecutar las pruebas desde el mismo intérprete del cuaderno:

```python
import subprocess
import sys

resultado = subprocess.run(
    [sys.executable, "-m", "pytest", "-v"],
    capture_output=True,
    text=True,
    check=False,
)

print(resultado.stdout)
if resultado.stderr:
    print(resultado.stderr)

print("Código de salida:", resultado.returncode)
assert resultado.returncode == 0
```

La carpeta de trabajo debe ser la raíz de la copia del repositorio.

## 3. Ejemplo mínimo

Los parámetros de este ejemplo son sintéticos.

```python
from modelo_fisico.configuracion import Capa, ConfiguracionPerfil
from modelo_fisico.estados import EstadoPerfil
from modelo_fisico.entradas import EntradasPaso

perfil = ConfiguracionPerfil(
    capas=(
        Capa(0.0, 0.2, 0.05, 0.25, 0.45, 6.0),
        Capa(0.2, 0.6, 0.05, 0.25, 0.45, 12.0),
    ),
    f_max_mm_h=12.0,
)

estado = EstadoPerfil(
    configuracion=perfil,
    almacenamientos_mm=(40.0, 80.0),
)

entradas = EntradasPaso(
    configuracion=perfil,
    dt_s=300.0,
    precipitacion_mm=0.5,
    riego_mm=0.0,
    extracciones_solicitadas_mm=(0.1, 0.2),
)

print(estado.humedades)
print(estado.almacenamiento_total_mm)
print(entradas.dt_h)
```

Este ejemplo construye y consulta objetos.
No aplica las entradas al estado ni simula un paso hidráulico.

## 4. Campos y unidades

### Configuración

- `z_superior_m`, `z_inferior_m`: profundidades en m.
- `espesor_m`: diferencia entre las profundidades, en m.
- `theta_min`: límite operativo inferior de extracción, en m³/m³.
- `theta_fc`: capacidad de campo, en m³/m³.
- `theta_sat`: saturación, en m³/m³.
- `tau_h`: escala temporal de drenaje, en h.
- `f_max_mm_h`: capacidad efectiva máxima de infiltración, en mm/h.

Las capas se proporcionan como una tupla ordenada desde la superficie.
Los límites compartidos deben coincidir exactamente.

Las opciones `infiltracion`, `transferencias` y `drenaje_inferior`
son booleanas e independientes.

`tau_h=None` solo se admite cuando no es necesaria para la salida activa
de esa capa. Cualquier escala proporcionada debe ser positiva y finita.

### Estado

- `almacenamientos_mm`: tupla con un almacenamiento por capa, en mm.
- `humedades`: humedades volumétricas calculadas, en m³/m³.
- `almacenamiento_total_mm`: suma de almacenamientos, en mm.

### Entradas

- `dt_s`: duración positiva del intervalo, en s.
- `dt_h`: duración calculada en h.
- `precipitacion_mm`: precipitación que alcanza la superficie, en mm.
- `riego_mm`: riego que alcanza la superficie, en mm.
- `extracciones_solicitadas_mm`: demanda por capa, en mm.

Los aportes y las demandas son acumulados del intervalo, no tasas.
No se multiplican de nuevo por la duración.

Los campos son obligatorios y los ceros deben indicarse explícitamente.
Las demandas no se limitan aquí al almacenamiento disponible.

## 5. Conversiones

Las funciones de `modelo_fisico.conversiones` implementan:

S = 1000 · L · theta.

theta = S / (1000 · L).

Comprueban el rango geométrico general y el espesor.
Los límites particulares de cada capa se comprueban al validar el estado.

## 6. Estados y tolerancias

`EstadoPerfil` comprueba estrictamente los límites al construirse.
No admite estados iniciales fuera de rango ni los corrige.

`comprobar_almacenamientos` utiliza tolerancia cero por defecto.
Para comprobaciones numéricas posteriores puede proporcionarse
explícitamente una tolerancia absoluta en mm.

Se propone `TOLERANCIA_ESTADO_MM = 1e-9` mm.

Una comparación tolerante no modifica el almacenamiento ni convierte
automáticamente ese valor en un EstadoPerfil válido.

La tolerancia es un criterio de software, no una precisión de sensores.
No sustituye las tolerancias del balance de masa ni las comparaciones
de refinamiento temporal del diseño.

## 7. Tratamiento de errores

Se rechazan tipos no admitidos, booleanos usados como números,
valores no finitos, geometrías inválidas, umbrales incoherentes,
dimensiones incompatibles y estados fuera de rango.

No se sustituyen datos ausentes por cero.
No se recortan valores para ocultar errores.

## 8. Evidencia de ejecución

La evidencia debe identificar:
- El commit probado.
- Las versiones de Python y pytest.
- El resumen de pruebas.
- El código de salida.

Los resultados corresponden a los casos ejecutados y no demuestran
calibración ni validación con parcelas.
