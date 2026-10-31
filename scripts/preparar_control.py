"""Crea una copia vecina del proyecto sin los tres manifiestos SKILL.md."""

from __future__ import annotations

import hashlib
import json
import shutil
import subprocess
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[1]
CARPETAS = (".agents", "datos", "salidas", "figuras", "mapas", "referencias", "scripts", "tests", "docs")
ARCHIVOS = (".gitignore", ".python-version", "pyproject.toml", "uv.lock", "README.md", "evaluacion.md")
SKILLS = ("limpiando-enaho", "graficando-enaho", "mapeando-enaho")


def huella(ruta: Path) -> str:
    with ruta.open("rb") as archivo:
        return hashlib.file_digest(archivo, "sha256").hexdigest()


def main() -> None:
    destino = RAIZ.parent / "enaho_sin_skills"
    if destino.exists():
        raise FileExistsError(f"Ya existe {destino}; no se sobrescribe ni se borra")
    manifiestos = [Path(".agents/skills") / nombre / "SKILL.md" for nombre in SKILLS]
    if not all((RAIZ / relativa).is_file() for relativa in manifiestos):
        raise ValueError("El proyecto de origen no contiene los tres manifiestos esperados")
    destino.mkdir()
    ignorar = shutil.ignore_patterns("SKILL.md", "__pycache__", "*.pyc", "control_sin_skills_2024.json")
    for carpeta in CARPETAS:
        shutil.copytree(RAIZ / carpeta, destino / carpeta, ignore=ignorar)
    for archivo in ARCHIVOS:
        shutil.copy2(RAIZ / archivo, destino / archivo)
    uv = destino / ".tools/bin/uv.exe"
    uv.parent.mkdir(parents=True)
    shutil.copy2(RAIZ / ".tools/bin/uv.exe", uv)
    subprocess.run(["git", "init", "--initial-branch=main", str(destino)], check=True, capture_output=True)

    registros = []
    for carpeta in CARPETAS:
        for archivo in sorted((destino / carpeta).rglob("*")):
            if archivo.is_file():
                relativa = archivo.relative_to(destino)
                sha = huella(archivo)
                if sha != huella(RAIZ / relativa):
                    raise ValueError(f"La copia cambió {relativa}")
                registros.append({"archivo": relativa.as_posix(), "sha256": sha, "bytes": archivo.stat().st_size})
    for nombre in ARCHIVOS:
        archivo = destino / nombre
        sha = huella(archivo)
        if sha != huella(RAIZ / nombre):
            raise ValueError(f"La copia cambió {nombre}")
        registros.append({"archivo": nombre, "sha256": sha, "bytes": archivo.stat().st_size})
    if list((destino / ".agents").rglob("SKILL.md")):
        raise ValueError("Quedó un manifiesto de skill en la copia de control")
    control = {
        "estado": "PREPARADO", "carpeta_control": destino.name,
        "condicion": "Sin los tres manifiestos SKILL.md; se conservan scripts, referencias, datos, documentación y resultados existentes",
        "manifiestos_excluidos": [ruta.as_posix() for ruta in manifiestos],
        "nota": "Comprobar en un chat nuevo que las tres skills no figuran en su lista inicial. Las skills del sistema no se desactivan.",
        "limite_comparacion": "Instantánea posterior a las tres demostraciones con skills. Conserva resultados y documentación con cifras; la comparación será descriptiva, no una prueba desde datos sin procesar ni una medida causal de mejora.",
        "archivos_identicos_al_preparar": registros,
    }
    ruta_control = RAIZ / "referencias/control_sin_skills_2024.json"
    ruta_control.write_text(json.dumps(control, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Copia preparada: {destino}")
    print(f"{len(registros)} archivos contrastados con el origen; tres manifiestos ausentes")
    print("Antes de probar, abrir un chat nuevo en el proyecto de control y comprobar la lista de skills.")


if __name__ == "__main__":
    main()
