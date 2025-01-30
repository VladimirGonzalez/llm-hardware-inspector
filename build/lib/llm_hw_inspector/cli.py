"""
CLI para LLM Hardware Inspector
-------------------------------
Provee una interfaz de línea de comandos para el proyecto, permitiendo:
- Mostrar la info en pantalla
- Guardar las sugerencias en un archivo
- Exportar en formato JSON
"""
import json
import argparse
from .hardware_checker import obtener_info_sistema, generar_prompt_sugerencias

def run_cli():
    parser = argparse.ArgumentParser(
        prog="llm-hardware-inspector",
        description="Herramienta CLI para inspeccionar hardware y sugerir configuracion de LLM."
    )
    parser.add_argument(
        "--output",
        choices=["text", "json"],
        default="text",
        help="Formato de salida: texto por defecto, o JSON para parsear programoticamente."
    )
    parser.add_argument(
        "--output-file",
        type=str,
        help="Si se especifica, la informacion (texto/JSON) se guardaro en este archivo."
    )
    parser.add_argument(
        "--prompt-file",
        type=str,
        default="sugerencias_llm.txt",
        help="Nombre del archivo donde se guardaron las sugerencias (texto)."
    )
    args = parser.parse_args()

    info = obtener_info_sistema()
    prompt = generar_prompt_sugerencias(info)

    if args.output == "json":
        data = {"hardware_info": info, "sugerencias": prompt}
        output_str = json.dumps(data, indent=4, ensure_ascii=False)
    else:
        output_str = _info_to_text(info) + "\n\n" + prompt

    print(output_str)

    if args.output_file:
        with open(args.output_file, "w", encoding="utf-8") as f:
            f.write(output_str)

    if prompt:
        with open(args.prompt_file, "w", encoding="utf-8") as f:
            f.write(prompt)

def _info_to_text(info: dict) -> str:
    lines = []
    lines.append("======================================== Informacion del Sistema ========================================")
    for key, value in info.items():
        if isinstance(value, list):
            lines.append(f"=== {key} ===")
            if not value:
                lines.append("    Sin datos")
            for idx, elem in enumerate(value, start=1):
                lines.append(f"  -- Elemento #{idx} --")
                if isinstance(elem, dict):
                    for subk, subv in elem.items():
                        lines.append(f"     {subk}: {subv}")
                else:
                    lines.append(f"     {elem}")
        else:
            lines.append(f"{key}: {value}")
    lines.append("=========================================================================================================")
    return "\n".join(lines)

def main():
    run_cli()

if __name__ == "__main__":
    main()
