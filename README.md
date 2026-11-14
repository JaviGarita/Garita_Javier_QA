# Prueba Técnica — Pasantía QA Automation Mobile (ShopGo)

Este repositorio contiene la resolución de la prueba técnica de QA Automation Mobile para la aplicación **ShopGo**.

## Estructura del Proyecto

```text
Garita_Javier_QA/
|-- README.md                 # Instrucciones de instalación y ejecución
|-- NOTAS.md                  # Suposiciones, registro de uso de IA y tiempo invertido
|-- requirements.txt          # Dependencias del proyecto (pytest, Appium-Python-Client)
|-- parte1_casos/
|   `-- casos_login.md        # Parte 1: Casos de prueba para inicio de sesión
|-- shopgo/
|   |-- __init__.py
|   `-- validaciones.py       # Parte 2: Funciones validar_password y calcular_envio
|-- pages/
|   |-- __init__.py
|   `-- login_page.py         # Parte 3: Page Object de la pantalla de inicio de sesión
|-- tests/
|   |-- conftest.py           # Parte 3: Fixture del driver de Appium
|   |-- test_validaciones.py  # Parte 2: Pruebas unitarias con pytest
|   `-- test_login.py         # Parte 3: Pruebas de UI mobile con Appium
`-- parte4_bug/
    `-- reporte_bug.md        # Parte 4: Reporte de bug del carrito al rotar pantalla
```

## Requisitos Previos

- **Python 3.10** o superior.

## Configuración y Ejecución

### 1. Crear y activar el entorno virtual

En **Windows (PowerShell)**:
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

En **Windows (CMD)**:
```cmd
python -m venv .venv
.venv\Scripts\activate.bat
```

En **macOS / Linux**:
```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 2. Instalar las dependencias

```bash
pip install -r requirements.txt
```

### 3. Ejecutar las pruebas automatizadas (Parte 2)

Para ejecutar la suite de pruebas unitarias de validaciones y cálculo de envío:

```bash
pytest tests/test_validaciones.py -v
```

> **Nota sobre la Parte 3 (`tests/test_login.py`):** De acuerdo con las instrucciones de la prueba, el script de UI mobile con Appium está diseñado para demostrar el patrón Page Object, locators, fixtures y esperas explícitas, y no requiere contar con un servidor Appium ni un emulador activo para su revisión.
