# LLM Hardware Inspector

Este proyecto **open source** permite obtener información detallada del hardware (CPU, GPU, RAM, almacenamiento, etc.) para estimar la capacidad de ejecutar modelos de **IA/LLM** localmente. También genera **sugerencias** sobre qué modelos o configuraciones podrían ser adecuadas según el hardware disponible.

## Características

- Información sobre **CPU** y **GPU** (NVIDIA/AMD).
- Verificación de versiones de **frameworks** como PyTorch y TensorFlow.
- Recomendaciones basadas en VRAM y RAM.
- **CLI** para exportar datos en formato texto o JSON.

## Instalación

Requisitos:
- Python 3.7 o superior

Pasos:
```bash
git clone https://github.com/[TU-USUARIO]/llm-hardware-inspector.git
cd llm-hardware-inspector
pip install -r requirements.txt

## Uso

Modo básico (Texto):
```bash
python -m llm_hw_inspector.cli

Modo JSON:
```bash
python -m llm_hw_inspector.cli --output json
