# LLM Hardware Inspector

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

Este proyecto **open source** recopila y muestra información detallada del sistema (CPU, GPU, memoria, disco, versiones de Python/Frameworks, etc.) con el objetivo de **estimar la capacidad** para ejecutar modelos de **IA/LLM** localmente. Además, genera **sugerencias** para guiar al usuario sobre qué tipo de modelo o configuración puede ser adecuada según su hardware.

## Características Principales

- Detección de CPU (núcleos, frecuencia, flags como AVX/AVX2, etc.).
- Información de **GPU** (NVIDIA/AMD) mediante:
  - [GPUtil](https://pypi.org/project/GPUtil/)
  - [pynvml](https://pypi.org/project/pynvml/) (para Compute Capability y versión del driver NVIDIA).
- Verificación de **versiones de frameworks** (PyTorch, TensorFlow).
- Espacio en disco (para estimar almacenamiento disponible).
- Generación de **recomendaciones** para ejecutar LLMs, en base a la VRAM y RAM.
- **CLI** amigable con opciones para exportar como JSON o como texto.
- Compatible con Linux, Windows y macOS (dentro de las limitaciones de las herramientas instaladas).

## Instalación

### Requisitos

- Python 3.7 o superior
- pip para instalar dependencias

### Pasos de Instalación

```bash
git clone https://github.com/VladimirGonzalez/llm-hardware-inspector.git
cd llm-hardware-inspector

# Instalar dependencias (si usas pip):
pip install -r requirements.txt

# (opcional) Instalar localmente como paquete:
pip install .



¡Claro! A continuación encontrarás una propuesta de proyecto open source con licencia MIT, enfocado en recopilar información del sistema para evaluar la factibilidad de correr modelos de IA (en particular, modelos de lenguaje - LLM) de forma local. La estructura incluye:

Un directorio principal con nombre sugerido (llm-hardware-inspector).
Un archivo de licencia MIT.
Un archivo README.md con una descripción clara, instrucciones de instalación y uso.
Un archivo de requirements (o pyproject.toml) para manejo de dependencias.
Un módulo Python con el corazón de la lógica (hardware_checker.py).
Un módulo CLI (cli.py) que hace fácil la ejecución desde la terminal.
Un flujo de GitHub Actions (opcional) para pruebas automáticas.
Estructura de Archivos
graphql
Copiar
Editar
llm-hardware-inspector/
├── .github/
│   └── workflows/
│       └── test.yml            # (Opcional) Flujo de GitHub Actions para pruebas
├── LICENSE                     # Licencia MIT
├── README.md                   # Descripción e instrucciones de uso
├── pyproject.toml              # (o requirements.txt) Para gestionar dependencias
├── llm_hw_inspector/
│   ├── __init__.py
│   ├── hardware_checker.py     # Lógica principal de obtención de info
│   └── cli.py                  # CLI con argparse
└── setup.py                    # (Opcional) Para instalación con pip
A continuación, se muestra un ejemplo detallado de implementación. La idea es que, si subes este repo a tu GitHub con la estructura mostrada, cualquier persona podrá clonar el proyecto, instalarlo y usarlo para obtener un reporte avanzado sobre el hardware y software disponible para IA, junto con recomendaciones.

1. Archivo de Licencia (MIT)
LICENSE:

plaintext
Copiar
Editar
MIT License

Copyright (c) 2023 [TU-NOMBRE]

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

[... resto de la MIT License ...]
Recuerda reemplazar [TU-NOMBRE] con tu nombre (o el de tu organización).

2. Archivo README.md
markdown
Copiar
Editar
# LLM Hardware Inspector

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

Este proyecto **open source** recopila y muestra información detallada del sistema (CPU, GPU, memoria, disco, versiones de Python/Frameworks, etc.) con el objetivo de **estimar la capacidad** para ejecutar modelos de **IA/LLM** localmente. Además, genera **sugerencias** para guiar al usuario sobre qué tipo de modelo o configuración puede ser adecuada según su hardware.

## Características Principales

- Detección de CPU (núcleos, frecuencia, flags como AVX/AVX2, etc.).
- Información de **GPU** (NVIDIA/AMD) mediante:
  - [GPUtil](https://pypi.org/project/GPUtil/)
  - [pynvml](https://pypi.org/project/pynvml/) (para Compute Capability y versión del driver NVIDIA).
- Verificación de **versiones de frameworks** (PyTorch, TensorFlow).
- Espacio en disco (para estimar almacenamiento disponible).
- Generación de **recomendaciones** para ejecutar LLMs, en base a la VRAM y RAM.
- **CLI** amigable con opciones para exportar como JSON o como texto.
- Compatible con Linux, Windows y macOS (dentro de las limitaciones de las herramientas instaladas).

## Instalación

### Requisitos

- Python 3.7 o superior
- pip para instalar dependencias

### Pasos de Instalación

```bash
git clone https://github.com/[TU-USUARIO]/llm-hardware-inspector.git
cd llm-hardware-inspector

# Instalar dependencias (si usas pip):
pip install -r requirements.txt

# (opcional) Instalar localmente como paquete:
pip install .
Uso
Modo básico (Texto)
bash
Copiar
Editar
python -m llm_hw_inspector.cli
Generará un reporte en pantalla y guardará un archivo de sugerencias (sugerencias_llm.txt).

Modo JSON
bash
Copiar
Editar
python -m llm_hw_inspector.cli --output json
Muestra la información en formato JSON por la salida estándar (y también genera sugerencias).

Opciones de ayuda
bash
Copiar
Editar
python -m llm_hw_inspector.cli --help
Despliega todas las opciones disponibles.

Licencia
Este proyecto está licenciado bajo la Licencia MIT. ¡Siéntete libre de usarlo, mejorarlo y compartirlo!

makefile
Copiar
Editar

---

## 3. `pyproject.toml` (o `requirements.txt`)

Como ejemplo, podemos usar `pyproject.toml` para definir el proyecto y dependencias:

```toml
[build-system]
requires = ["setuptools>=42", "wheel"]
build-backend = "setuptools.build_meta"

[project]
name = "llm-hardware-inspector"
version = "0.1.0"
description = "Herramienta para inspeccionar hardware/sofware y sugerir configuración de LLM."
authors = [
  { name = "Tu nombre", email = "tu-email@example.com" }
]
license = "MIT"
readme = "README.md"
requires-python = ">=3.7"

[project.urls]
"Source Code" = "https://github.com/TU-USUARIO/llm-hardware-inspector"
"Bug Tracker" = "https://github.com/TU-USUARIO/llm-hardware-inspector/issues"

[project.dependencies]
psutil = "*"
GPUtil = "*"
cpuinfo = {optional = true}    # Permite flags CPU
pynvml = {optional = true}     # Permite compute capability y driver info
torch = {optional = true}      # Para detección de PyTorch
tensorflow = {optional = true} # Para detección de TensorFlow
Si prefieres un requirements.txt, podrías usar algo así:

Copiar
Editar
psutil
GPUtil
py-cpuinfo
pynvml
torch
tensorflow