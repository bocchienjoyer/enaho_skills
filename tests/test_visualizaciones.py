"""Ponderación, correspondencia geográfica y rechazo de bases sin validar."""

import importlib.util
import json
import sys
import tempfile
import unittest
from pathlib import Path

import geopandas as gpd
import pandas as pd
from shapely.geometry import box

RAIZ = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(RAIZ / "scripts"))
from enaho_comun import ErrorAnalisis, agrupar_pobreza, cargar_base_validada, huella


def cargar_script(nombre, ruta):
    spec = importlib.util.spec_from_file_location(nombre, RAIZ / ruta)
    modulo = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(modulo)
    return modulo


graficos = cargar_script("graficos", ".agents/skills/graficando-enaho/scripts/graficar.py")
mapas = cargar_script("mapas", ".agents/skills/mapeando-enaho/scripts/mapear.py")


class AgregacionTest(unittest.TestCase):
    def setUp(self):
        self.base = pd.DataFrame({"pobre": [True, False, True, False], "facpob07": [1.0, 9.0, 5.0, 5.0]})
        self.grupos = pd.Series(["Rural", "Rural", "Urbana", "Urbana"])

    def test_pondera_en_cada_grupo_y_conserva_personas(self):
        tabla = agrupar_pobreza(self.base, self.grupos).set_index("grupo")
        self.assertAlmostEqual(tabla.loc["Rural", "pobreza_pct"], 10.0)
        self.assertAlmostEqual(tabla.loc["Urbana", "pobreza_pct"], 50.0)
        self.assertEqual(tabla.n_personas.sum(), 4)
        self.assertAlmostEqual(tabla.poblacion_expandida.sum(), 20.0)

    def test_no_descarta_personas_sin_grupo(self):
        self.grupos.iloc[0] = None
        with self.assertRaisesRegex(ErrorAnalisis, "sin grupo"):
            agrupar_pobreza(self.base, self.grupos)

    def test_rechaza_peso_cero(self):
        self.base.loc[0, "facpob07"] = 0
        with self.assertRaisesRegex(ErrorAnalisis, "no positivos"):
            agrupar_pobreza(self.base, self.grupos)

    def test_edades_incluyen_cero_y_limites_sin_huecos(self):
        base = pd.DataFrame({"p208a": [0, 17, 18, 29, 30, 44, 45, 59, 60, 120]})
        grupos = graficos.crear_grupos(base, "edad")
        self.assertFalse(grupos.isna().any())
        self.assertEqual(grupos.value_counts().to_dict(), {grupo: 2 for grupo in graficos.EDADES})


class UnionMapaTest(unittest.TestCase):
    def setUp(self):
        codigos = [f"{i:02d}" for i in range(1, 26)]
        self.geo = gpd.GeoDataFrame(
            {"FIRST_IDDP": codigos[::-1], "NOMBDEP": ["Mismo nombre"] * 25},
            geometry=[box(i, 0, i + 0.5, 0.5) for i in range(25)], crs=4326,
        )
        self.tasas = pd.DataFrame({"departamento": codigos, "pobreza_pct": [float(i) for i in range(1, 26)]})

    def test_une_por_codigo_con_nombres_iguales_y_orden_distinto(self):
        resultado = mapas.unir_departamentos(self.geo, self.tasas).set_index("departamento")
        self.assertEqual(len(resultado), 25)
        self.assertEqual(resultado.loc["07", "pobreza_pct"], 7.0)
        self.assertEqual(resultado.loc["15", "pobreza_pct"], 15.0)
        self.assertFalse(resultado.pobreza_pct.isna().any())

    def test_rechaza_codigo_duplicado(self):
        self.geo.loc[0, "FIRST_IDDP"] = self.geo.loc[1, "FIRST_IDDP"]
        with self.assertRaisesRegex(ErrorAnalisis, "25 códigos únicos"):
            mapas.unir_departamentos(self.geo, self.tasas)

    def test_rechaza_departamento_sin_tasa(self):
        with self.assertRaisesRegex(ErrorAnalisis, "25 códigos únicos"):
            mapas.unir_departamentos(self.geo, self.tasas.iloc[:-1])
        self.tasas.loc[0, "pobreza_pct"] = float("nan")
        with self.assertRaisesRegex(ErrorAnalisis, "Tasas faltantes"):
            mapas.unir_departamentos(self.geo, self.tasas)

    def test_rechaza_codigo_que_perdio_el_cero(self):
        self.geo.loc[self.geo.FIRST_IDDP.eq("07"), "FIRST_IDDP"] = "7"
        with self.assertRaisesRegex(ErrorAnalisis, "dos caracteres"):
            mapas.unir_departamentos(self.geo, self.tasas)


class BaseValidadaTest(unittest.TestCase):
    def setUp(self):
        self.temporal = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporal.cleanup)
        self.raiz = Path(self.temporal.name)
        (self.raiz / "salidas").mkdir()
        self.ruta = self.raiz / "salidas/personas_2024.parquet"
        base = pd.DataFrame({
            "anio": [2024], "conglome": ["010001"], "vivienda": ["001"], "hogar": ["11"],
            "codperso": ["01"], "ubigeo": ["070101"], "estrato": [1], "departamento": ["07"],
            "urbano": [True], "pobreza": [2], "pobre": [True], "facpob07": [10.0], "p207": [1], "p208a": [0],
        })
        base.to_parquet(self.ruta, index=False)
        self.informe = self.raiz / "salidas/validacion_2024.json"
        self.informe.write_text(json.dumps({
            "estado": "OK", "anio": 2024, "filas": {"base": 1},
            "base": {"archivo": self.ruta.name, "sha256": huella(self.ruta)},
        }), encoding="utf-8")
        (self.raiz / "salidas/validacion.txt").write_text("Estado: OK\n", encoding="utf-8")

    def test_acepta_base_que_corresponde_al_informe(self):
        base, informe = cargar_base_validada(self.raiz, 2024)
        self.assertEqual(len(base), 1)
        self.assertEqual(informe["estado"], "OK")

    def test_rechaza_base_modificada(self):
        with self.ruta.open("ab") as archivo:
            archivo.write(b"modificada")
        with self.assertRaisesRegex(ErrorAnalisis, "SHA-256"):
            cargar_base_validada(self.raiz, 2024)

    def test_rechaza_informe_error_aunque_exista_base(self):
        informe = json.loads(self.informe.read_text(encoding="utf-8"))
        informe["estado"] = "ERROR"
        self.informe.write_text(json.dumps(informe), encoding="utf-8")
        with self.assertRaisesRegex(ErrorAnalisis, "validación OK"):
            cargar_base_validada(self.raiz, 2024)

    def test_si_falta_base_indica_skill_de_limpieza(self):
        with tempfile.TemporaryDirectory() as vacio:
            with self.assertRaisesRegex(FileNotFoundError, "limpiando-enaho"):
                cargar_base_validada(Path(vacio), 2024)


if __name__ == "__main__":
    unittest.main()
