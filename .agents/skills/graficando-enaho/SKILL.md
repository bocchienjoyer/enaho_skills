---
name: graficando-enaho
description: Genera gráficos de barras de pobreza monetaria de ENAHO 2024 por área urbana y rural, sexo o grupos de edad, ponderados con facpob07. Úsala cuando pidan graficar o comparar visualmente esas categorías de la ENAHO.
---

# Graficar pobreza de ENAHO 2024

1. Trabajar desde la raíz del repositorio. Si falta `salidas/personas_2024.parquet`, usar primero la skill [limpiando-enaho](../limpiando-enaho/SKILL.md). Exigir limpieza satisfactoria y leer `salidas/validacion.txt`.
2. Usar 2024 si no se indica otro año y decirlo. Solo está implementado ese año. Elegir `--por area`, `--por sexo` o `--por edad` según el pedido; si es un pedido genérico de gráfico de pobreza, usar área urbana y rural e indicar la elección.
3. Ejecutar el script correspondiente sin cambiar los pesos:

   ```powershell
   uv run --frozen python .agents/skills/graficando-enaho/scripts/graficar.py --anio 2024 --por area
   ```

   Si `uv` no está en PATH, usar `.\.tools\bin\uv.exe run --frozen --cache-dir .uv-cache python` seguido de la misma ruta y argumentos.
4. El script comprueba el estado y SHA-256 de la base mediante `scripts/enaho_comun.py`. Si falla, detenerse y resolver la validación con `limpiando-enaho`; no reutilizar una figura anterior como resultado nuevo.
5. Revisar el PNG y el CSV de `figuras/pobreza_<por>_2024.*`. Deben tener barras desde cero, ordenadas por tasa de mayor a menor, un solo color y valores escritos en cada barra. El título indica qué y cuándo; el pie dice «Fuente: INEI, ENAHO 2024». La salida es PNG a 200 dpi.
6. Informar que el universo son residentes habituales y el peso `facpob07`. No sustituir las tasas por los redondeos de sumaria del curso. Para edad se usan grupos 0–17, 18–29, 30–44, 45–59 y 60 años o más; identificarlos al responder. El JSON adjunto registra la base, el peso y los parámetros usados.

Para categorías o variables distintas de las implementadas, consultar el [esquema de ENAHO](../limpiando-enaho/references/esquema_2024.md) antes de ampliar el script. No llamar a esta skill para mapas departamentales: usar `mapeando-enaho`.
