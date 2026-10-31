"""Prepara una copia con skills y entradas, sin base limpia ni salidas previas."""

from __future__ import annotations

import hashlib
import json
import shutil
import subprocess
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[1]
SKILLS = ("limpiando-enaho", "graficando-enaho", "mapeando-enaho")
README = """# ENAHO 2024

Proyecto local de Python 3.13 con dependencias fijadas en `uv.lock`.

Entradas disponibles:

- `datos/966-Modulo34.zip`: módulo de sumaria de hogares del INEI.
- `datos/966-Modulo02.zip`: módulo de miembros del hogar del INEI.
- `datos/peru_departamental_simple.geojson`: límites territoriales del material del curso.
- `referencias/pobreza_departamento_2024.csv`: referencia de la sesión para contrastar resultados.

El entorno local está en `.venv`; `uv` está disponible en `.tools/bin/uv.exe`.
"""


def huella(ruta: Path) -> str:
    with ruta.open("rb") as archivo:
        return hashlib.file_digest(archivo, "sha256").hexdigest()


def main() -> None:
    destino = RAIZ.parent / "enaho_sin_base"
    if destino.exists():
        raise FileExistsError(f"Ya existe {destino}; no se sobrescribe ni se borra")
    for nombre in SKILLS:
        if not (RAIZ / ".agents/skills" / nombre / "SKILL.md").is_file():
            raise FileNotFoundError(f"Falta la skill {nombre} en el proyecto de origen")
    destino.mkdir()
    ignorar = shutil.ignore_patterns("__pycache__", "*.pyc")
    for carpeta in (".agents", "datos", "tests"):
        shutil.copytree(RAIZ / carpeta, destino / carpeta, ignore=ignorar)
    for nombre in (".gitignore", ".python-version", "pyproject.toml", "uv.lock"):
        shutil.copy2(RAIZ / nombre, destino / nombre)
    (destino / "scripts").mkdir()
    for nombre in ("enaho_comun.py", "preparar_datos.py"):
        shutil.copy2(RAIZ / "scripts" / nombre, destino / "scripts" / nombre)
    (destino / "referencias").mkdir()
    referencia = Path("referencias/pobreza_departamento_2024.csv")
    shutil.copy2(RAIZ / referencia, destino / referencia)
    for carpeta in ("salidas", "figuras", "mapas"):
        (destino / carpeta).mkdir()
    (destino / "README.md").write_text(README, encoding="utf-8")
    uv = destino / ".tools/bin/uv.exe"
    uv.parent.mkdir(parents=True)
    shutil.copy2(RAIZ / ".tools/bin/uv.exe", uv)
    subprocess.run(["git", "init", "--initial-branch=main", str(destino)], check=True, capture_output=True)

    registros = []
    for archivo in sorted(destino.rglob("*")):
        relativa = archivo.relative_to(destino)
        if not archivo.is_file() or any(parte in {".git", ".tools"} for parte in relativa.parts):
            continue
        sha = huella(archivo)
        if relativa.as_posix() != "README.md" and sha != huella(RAIZ / relativa):
            raise ValueError(f"La copia cambió {relativa}")
        registros.append({"archivo": relativa.as_posix(), "sha256": sha})
    manifiestos = list((destino / ".agents").rglob("SKILL.md"))
    if len(manifiestos) != 3:
        raise ValueError("La copia no contiene exactamente tres manifiestos")
    for carpeta in ("salidas", "figuras", "mapas"):
        if list((destino / carpeta).iterdir()):
            raise ValueError(f"La carpeta {carpeta} no está vacía")
    control = {
        "estado": "PREPARADO_SIN_BASE", "carpeta": destino.name,
        "condicion": "Tres skills y datos fuente presentes; sin base limpia, informes ni figuras previas",
        "manifiestos": [p.relative_to(destino).as_posix() for p in sorted(manifiestos)],
        "carpetas_vacias": ["salidas", "figuras", "mapas"],
        "documentacion": "README neutro sobre entradas y entorno; no se copiaron los informes de evaluación ni resultados previos",
        "referencia_de_entrada": referencia.as_posix(),
        "base_original_sha256": huella(RAIZ / "salidas/personas_2024.parquet"),
        "archivos_iniciales": registros,
        "ejecucion_del_pedido": "PENDIENTE",
    }
    ruta = RAIZ / "referencias/encadenamiento_sin_base_2024.json"
    ruta.write_text(json.dumps(control, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Copia preparada: {destino}")
    print(f"Tres skills y {len(registros)} archivos iniciales; salidas, figuras y mapas vacíos")


if __name__ == "__main__":
    main()
