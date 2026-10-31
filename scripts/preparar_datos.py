"""Descarga y verifica las entradas públicas de la sesión ENAHO 2024."""

from __future__ import annotations

import csv
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from urllib.request import Request, urlopen
from zipfile import ZipFile

RAIZ = Path(__file__).resolve().parents[1]
FUENTES = (
    (
        "datos/966-Modulo34.zip",
        "https://proyectos.inei.gob.pe/iinei/srienaho/descarga/STATA/966-Modulo34.zip",
    ),
    (
        "datos/966-Modulo02.zip",
        "https://proyectos.inei.gob.pe/iinei/srienaho/descarga/STATA/966-Modulo02.zip",
    ),
    (
        "datos/peru_departamental_simple.geojson",
        "https://raw.githubusercontent.com/d2cml-ai/Data-Science-Python/main/"
        "sessions/06-geoespacial/lab/Data/peru_departamental_simple.geojson",
    ),
    (
        "referencias/pobreza_departamento_2024.csv",
        "https://raw.githubusercontent.com/d2cml-ai/Data-Science-Python/main/"
        "sessions/16-skills-enaho/referencias/pobreza_departamento_2024.csv",
    ),
)


def verificar(ruta: Path, nombre_final: Path | None = None) -> dict:
    nombre = nombre_final or ruta
    if nombre.suffix == ".zip":
        esperado = (
            "sumaria-2024.dta"
            if "Modulo34" in nombre.name
            else "enaho01-2024-200.dta"
        )
        with ZipFile(ruta) as archivo:
            incorrecto = archivo.testzip()
            if incorrecto:
                raise ValueError(f"ZIP dañado: {incorrecto}")
            nombres = archivo.namelist()
            if not any(Path(nombre).name.lower() == esperado for nombre in nombres):
                raise ValueError(f"No se encontró {esperado} en {ruta.name}")
        return {"archivo_stata": esperado, "entradas_zip": len(nombres)}
    if nombre.suffix == ".geojson":
        contenido = json.loads(ruta.read_text(encoding="utf-8"))
        entidades = contenido["features"]
        codigos = [str(f["properties"]["FIRST_IDDP"]).zfill(2) for f in entidades]
        if len(entidades) != 25 or set(codigos) != {f"{i:02d}" for i in range(1, 26)}:
            raise ValueError("El GeoJSON no contiene los 25 códigos departamentales únicos")
        return {"departamentos": len(entidades), "campo_union": "FIRST_IDDP"}
    with ruta.open(encoding="utf-8-sig", newline="") as archivo:
        filas = list(csv.DictReader(archivo))
    if len(filas) != 25 or {f["ccdd"] for f in filas} != {f"{i:02d}" for i in range(1, 26)}:
        raise ValueError("La referencia no contiene los 25 códigos departamentales")
    return {"departamentos": len(filas), "origen": "Referencia de la sesión, no cálculo propio"}


def main() -> None:
    registros = []
    for relativa, url in FUENTES:
        ruta = RAIZ / relativa
        ruta.parent.mkdir(parents=True, exist_ok=True)
        if not ruta.exists():
            temporal = ruta.with_suffix(ruta.suffix + ".part")
            peticion = Request(url, headers={"User-Agent": "ENAHO-skills-Codex/1.0"})
            with urlopen(peticion, timeout=60) as respuesta, temporal.open("wb") as archivo:
                while bloque := respuesta.read(1024 * 1024):
                    archivo.write(bloque)
            verificar(temporal, ruta)
            temporal.replace(ruta)
        resultado = verificar(ruta)
        with ruta.open("rb") as archivo:
            sha256 = hashlib.file_digest(archivo, "sha256").hexdigest()
        registro = {
            "archivo": relativa,
            "url": url,
            "bytes": ruta.stat().st_size,
            "sha256": sha256,
            "verificacion": resultado,
        }
        registros.append(registro)
        print(f"OK {relativa}: {registro['bytes']:,} bytes", flush=True)
    manifiesto = {
        "anio": 2024,
        "verificado_utc": datetime.now(timezone.utc).isoformat(),
        "nota": "Integridad y estructura de entradas; aún no se ha validado la limpieza.",
        "fuentes": registros,
    }
    destino = RAIZ / "referencias" / "fuentes_2024.json"
    destino.write_text(json.dumps(manifiesto, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
