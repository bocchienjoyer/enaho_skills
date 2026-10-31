"""Controles que evitan sesgos o multiplicación de personas en el pipeline."""

import importlib.util
from io import BytesIO
import json
import tempfile
import unittest
from pathlib import Path
from zipfile import ZipFile

import pandas as pd

RAIZ = Path(__file__).resolve().parents[1]
RUTA_SCRIPT = RAIZ / ".agents/skills/limpiando-enaho/scripts/limpiar.py"
spec = importlib.util.spec_from_file_location("limpieza", RUTA_SCRIPT)
limpieza = importlib.util.module_from_spec(spec)
spec.loader.exec_module(limpieza)


class LimpiezaTest(unittest.TestCase):
    def setUp(self):
        self.sumaria = pd.DataFrame([
            dict(aÑo="2024", conglome="010001", vivienda="001", hogar="11", ubigeo="010101", dominio=1, estrato=2, pobreza=1, factor07=2.0, mieperho=2),
            dict(aÑo="2024", conglome="010002", vivienda="002", hogar="11", ubigeo="070101", dominio=1, estrato=7, pobreza=3, factor07=6.0, mieperho=1),
        ])
        registros = []
        for hogar, codperso, p204, p205, p206, peso in [
            (0, "01", 1, 2, float("nan"), 2.0),
            (0, "02", 2, float("nan"), 1, 3.0),
            (1, "01", 1, 2, float("nan"), 5.0),
            (1, "02", 1, 1, float("nan"), 8.0),
        ]:
            original = self.sumaria.iloc[hogar]
            registros.append({
                **{c: original[c] for c in ["aÑo", *limpieza.LLAVES_HOGAR, *limpieza.GEOGRAFIA]},
                "mes": "01", "codperso": codperso, "p203": 1, "p204": p204, "p205": p205,
                "p206": p206, "p207": 1, "p208a": 0, "facpob07": peso,
            })
        self.personas = pd.DataFrame(registros)

    def construir(self):
        return limpieza.construir_base(self.personas, self.sumaria, 2024)

    def test_residencia_ponderacion_y_llaves(self):
        base, resumen = self.construir()
        self.assertEqual(len(base), 3)
        self.assertEqual(resumen["filas"]["excluidos"], 1)
        self.assertEqual(resumen["estimaciones"]["personas"]["pobreza_pct"], 50.0)
        self.assertEqual(resumen["estimaciones"]["sumaria"]["pobreza_pct"], 40.0)
        self.assertEqual(base.iloc[0].conglome, "010001")
        self.assertEqual(base.iloc[0].vivienda, "001")
        self.assertEqual(set(base.departamento), {"01", "07"})
        self.assertTrue(base.p208a.eq(0).all())
        self.assertNotIn("factor07", base.columns)
        self.assertNotIn("mieperho", base.columns)

    def test_rechaza_hogares_duplicados(self):
        self.sumaria = pd.concat([self.sumaria, self.sumaria.iloc[[0]]], ignore_index=True)
        with self.assertRaisesRegex(limpieza.ErrorValidacion, "llaves duplicadas"):
            self.construir()

    def test_rechaza_personas_duplicadas(self):
        self.personas = pd.concat([self.personas, self.personas.iloc[[0]]], ignore_index=True)
        with self.assertRaisesRegex(limpieza.ErrorValidacion, "llaves duplicadas"):
            self.construir()

    def test_rechaza_residente_sin_hogar(self):
        self.personas.loc[0, "hogar"] = "99"
        with self.assertRaisesRegex(limpieza.ErrorValidacion, "sin hogar"):
            self.construir()

    def test_rechaza_geografia_incompatible(self):
        self.personas.loc[0, "ubigeo"] = "080101"
        with self.assertRaisesRegex(limpieza.ErrorValidacion, "Geografía distinta"):
            self.construir()

    def test_rechaza_pobreza_invalida_o_faltante(self):
        for codigo in [None, 0, 4]:
            with self.subTest(codigo=codigo):
                self.sumaria.loc[0, "pobreza"] = codigo
                with self.assertRaisesRegex(limpieza.ErrorValidacion, "pobreza faltante"):
                    self.construir()

    def test_rechaza_pesos_invalidos(self):
        for peso in [0, -1, float("nan"), float("inf")]:
            with self.subTest(peso=peso):
                self.personas.loc[0, "facpob07"] = peso
                with self.assertRaisesRegex(limpieza.ErrorValidacion, "pesos nulos"):
                    self.construir()

    def test_rechaza_llaves_sin_ceros_y_anio_faltante(self):
        self.personas.loc[0, "conglome"] = "10001"
        with self.assertRaisesRegex(limpieza.ErrorValidacion, "formato incorrecto"):
            self.construir()
        self.personas.loc[0, "conglome"] = "010001"
        self.personas.loc[0, "aÑo"] = None
        with self.assertRaisesRegex(limpieza.ErrorValidacion, "año no es"):
            self.construir()

    def test_selecciona_dta_exacto_entre_varios(self):
        with tempfile.TemporaryDirectory() as carpeta:
            ruta = Path(carpeta) / "modulo.zip"
            esperado = pd.DataFrame({"identificador": [42]})
            with ZipFile(ruta, "w") as z:
                for nombre, tabla in [("sumaria-2024-12g.dta", pd.DataFrame({"identificador": [99]})), ("sumaria-2024.dta", esperado)]:
                    buffer = BytesIO()
                    tabla.to_stata(buffer, write_index=False)
                    z.writestr(f"modulo/{nombre}", buffer.getvalue())
            resultado = limpieza.leer_modulo(ruta, "sumaria-2024.dta")
            self.assertEqual(resultado.identificador.iloc[0], 42)

    def test_fallo_invalida_un_informe_previo(self):
        with tempfile.TemporaryDirectory() as carpeta:
            raiz = Path(carpeta)
            (raiz / "salidas").mkdir()
            informe = raiz / "salidas/validacion_2024.json"
            informe.write_text('{"estado": "OK"}', encoding="utf-8")
            with self.assertRaises(FileNotFoundError):
                limpieza.ejecutar(raiz, 2024)
            self.assertEqual(json.loads(informe.read_text(encoding="utf-8"))["estado"], "ERROR")
            self.assertIn("Estado: ERROR", (raiz / "salidas/validacion.txt").read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()
