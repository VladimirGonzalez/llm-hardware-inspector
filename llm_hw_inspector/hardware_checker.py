"""
MIT License

Herramienta principal para obtener información de hardware y software
relevante para ejecutar IA (especialmente LLM) de forma local.
"""

import platform
import psutil
import GPUtil
import subprocess

try:
    import cpuinfo
    CPUINFO_AVAILABLE = True
except ImportError:
    CPUINFO_AVAILABLE = False

try:
    from pynvml import (
        nvmlInit, nvmlDeviceGetHandleByIndex, nvmlDeviceGetComputeCapability,
        nvmlShutdown, nvmlDeviceGetName, nvmlSystemGetDriverVersion
    )
    PYNVML_AVAILABLE = True
except ImportError:
    PYNVML_AVAILABLE = False


def obtener_info_sistema() -> dict:
    info = {}
    info_os = platform.uname()
    info["Sistema Operativo"] = info_os.system
    info["Nombre del Nodo"] = info_os.node
    info["Versión OS"] = info_os.version
    info["Arquitectura"] = info_os.machine
    info["Procesador (raw)"] = info_os.processor
    info["Versión de Python"] = platform.python_version()

    cpu_freq = psutil.cpu_freq()
    if cpu_freq:
        info["Frecuencia Máxima (MHz)"] = cpu_freq.max
        info["Frecuencia Mínima (MHz)"] = cpu_freq.min
        info["Frecuencia Actual (MHz)"] = cpu_freq.current
    else:
        info["Frecuencia Máxima (MHz)"] = None
        info["Frecuencia Mínima (MHz)"] = None
        info["Frecuencia Actual (MHz)"] = None

    info["Núcleos Físicos"] = psutil.cpu_count(logical=False)
    info["Núcleos Totales (lógicos)"] = psutil.cpu_count(logical=True)
    info["Uso de CPU por Núcleo (%)"] = psutil.cpu_percent(percpu=True)
    info["Uso Total de CPU (%)"] = psutil.cpu_percent()

    if CPUINFO_AVAILABLE:
        cpu_inf = cpuinfo.get_cpu_info()
        flags = cpu_inf.get("flags", [])
        info["CPU Flags"] = flags
        info["Marca/Modelo CPU"] = cpu_inf.get("brand_raw", "Desconocido")
    else:
        info["CPU Flags"] = "py-cpuinfo no instalado"
        info["Marca/Modelo CPU"] = "Desconocido (py-cpuinfo no disponible)"

    memoria = psutil.virtual_memory()
    info["Memoria Total (GB)"] = round(memoria.total / (1024**3), 2)
    info["Memoria Disponible (GB)"] = round(memoria.available / (1024**3), 2)
    info["Memoria Usada (GB)"] = round(memoria.used / (1024**3), 2)
    info["Porcentaje de Memoria Usada (%)"] = memoria.percent

    disco = psutil.disk_usage('/')
    info["Almacenamiento Total (GB)"] = round(disco.total / (1024**3), 2)
    info["Almacenamiento Usado (GB)"] = round(disco.used / (1024**3), 2)
    info["Almacenamiento Libre (GB)"] = round(disco.free / (1024**3), 2)
    info["Porcentaje Disco Usado (%)"] = disco.percent

    gpu_data = []
    try:
        gpus = GPUtil.getGPUs()
        for gpu in gpus:
            gpu_info = {
                "Nombre": gpu.name,
                "Memoria Total (GB)": round(gpu.memoryTotal / 1024, 2),
                "Memoria Usada (GB)": round(gpu.memoryUsed / 1024, 2),
                "Memoria Libre (GB)": round(gpu.memoryFree / 1024, 2),
                "Carga de la GPU (%)": round(gpu.load * 100, 2),
                "Temperatura (°C)": gpu.temperature
            }
            gpu_data.append(gpu_info)
    except Exception as e:
        gpu_data.append({"Error": f"No se pudo obtener información de la GPU vía GPUtil: {e}"})
    info["GPUs (GPUtil)"] = gpu_data

    gpu_extra_info = []
    if PYNVML_AVAILABLE:
        try:
            nvmlInit()
            for index in range(len(gpu_data)):
                handle = nvmlDeviceGetHandleByIndex(index)
                gpu_name_nvml = nvmlDeviceGetName(handle).decode("utf-8")
                major_cc, minor_cc = nvmlDeviceGetComputeCapability(handle)
                driver_version = nvmlSystemGetDriverVersion().decode("utf-8")
                extra_info = {
                    "Nombre (NVML)": gpu_name_nvml,
                    "Compute Capability": f"{major_cc}.{minor_cc}",
                    "Driver Version": driver_version
                }
                gpu_extra_info.append(extra_info)
            nvmlShutdown()
        except Exception as e:
            gpu_extra_info.append({"Error": f"No se pudo obtener info de compute capability o driver: {e}"})
    else:
        gpu_extra_info.append({"Info": "pynvml no instalado, no se pudo obtener versión de driver ni compute capability"})
    info["GPUs (NVML Extra)"] = gpu_extra_info

    try:
        salida = subprocess.check_output(
            ["nvidia-smi", "--query-gpu=driver_version", "--format=csv,noheader"],
            stderr=subprocess.STDOUT
        ).decode("utf-8").strip()
        info["Driver NVIDIA (nvidia-smi)"] = salida
    except Exception:
        info["Driver NVIDIA (nvidia-smi)"] = "No disponible o no se pudo ejecutar"

    try:
        import torch
        info["PyTorch Version"] = torch.__version__
        info["PyTorch CUDA disponible"] = torch.cuda.is_available()
    except ImportError:
        info["PyTorch Version"] = "No instalado"

    try:
        import tensorflow as tf
        info["TensorFlow Version"] = tf.__version__
        info["TensorFlow GPU disponible"] = len(tf.config.list_physical_devices('GPU')) > 0
    except ImportError:
        info["TensorFlow Version"] = "No instalado"

    return info


def generar_prompt_sugerencias(info: dict) -> str:
    gpus = info.get("GPUs (GPUtil)", [])
    total_vram_gb = 0
    for g in gpus:
        maybe_vram = g.get("Memoria Total (GB)")
        if maybe_vram and maybe_vram > total_vram_gb:
            total_vram_gb = maybe_vram

    total_ram_gb = info.get("Memoria Total (GB)", 0)
    sugerencias = []

    if total_vram_gb >= 24:
        sugerencias.append("Puedes considerar modelos de 13B-30B en FP16 o int8.")
    elif total_vram_gb >= 16:
        sugerencias.append("Puedes considerar modelos LLM de 7B-13B en FP16 o int8 en GPU.")
    elif total_vram_gb >= 8:
        sugerencias.append("Podrías usar modelos 7B con técnicas de cuantización (4 bits/8 bits).")
    elif total_vram_gb > 0:
        sugerencias.append("Quizá sólo modelos muy pequeños o fuertemente cuantizados en GPU.")
    else:
        sugerencias.append("No se detectó una GPU potente. Probablemente debas ejecutar en CPU.")

    if total_ram_gb < 8:
        sugerencias.append("La RAM es limitada; considera modelos muy pequeños o cuantización agresiva.")
    elif total_ram_gb < 16:
        sugerencias.append("Podrías manejar modelos 7B con librerías optimizadas y/o swap si es imprescindible.")
    else:
        sugerencias.append("Tienes suficiente RAM para modelos medianos o múltiples procesos.")

    return (
        "=== Sugerencias para ejecutar LLM localmente ===\n"
        f"GPU con mayor VRAM detectada: {total_vram_gb} GB\n"
        f"Memoria RAM total: {total_ram_gb} GB\n"
        "Recomendaciones:\n" +
        "\n".join(f"- {s}" for s in sugerencias)
    )
