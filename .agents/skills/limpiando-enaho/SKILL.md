---
name: limpiando-enaho
description: Limpia y une los módulos 34 y 02 de la ENAHO 2024 del INEI, valida la pobreza y genera una base de personas. Úsala al preparar o unir ENAHO 2024, calcular pobreza por región, sexo o edad, o cuando otra skill necesite la base limpia.
---

# Limpiar ENAHO 2024

1. Trabajar desde la raíz de este repositorio. Obtener el año del pedido; si no se indica, usar 2024 y decirlo. El script solo admite 2024; no reutilizar el código INEI 966 para otro año.
2. Comprobar `datos/966-Modulo34.zip` y `datos/966-Modulo02.zip`. Si faltan, ejecutar `uv run --frozen python scripts/preparar_datos.py`; si la descarga falla, informar qué archivo falta y su enlace del INEI indicado en el README.
3. Ejecutar el pipeline sin reescribir sus filtros ni pesos:

   ```powershell
   uv run --frozen python .agents/skills/limpiando-enaho/scripts/limpiar.py --anio 2024
   ```

   Sustituir el año solo por uno admitido por el script. En esta máquina, si `uv` no está en PATH, reemplazarlo por `.\.tools\bin\uv.exe` y añadir `--cache-dir .uv-cache` antes de `python`.
4. Leer `salidas/validacion.txt` y exigir `estado: OK` en `salidas/validacion_2024.json`. Si el proceso falla o cualquier control no pasa, detener el análisis y explicar el fallo; no presentar una base anterior como válida.
5. Usar `salidas/personas_2024.parquet` y ponderar las cifras de personas con `facpob07`. Identificar siempre el universo y el peso: las referencias del curso calculadas con sumaria usan `factor07 × mieperho` y pueden diferir de personas. No promediar códigos de pobreza ni forzar las tasas a los valores de referencia.
6. Antes de agregar variables, interpretar códigos o contrastar cifras, consultar [references/esquema_2024.md](references/esquema_2024.md). Para barras por área, sexo o edad, continuar con [graficando-enaho](../graficando-enaho/SKILL.md); para un mapa por departamento, con [mapeando-enaho](../mapeando-enaho/SKILL.md).

El año y la ruta del script son argumentos explícitos: no usar `$0`, `$ARGUMENTS` ni `${CLAUDE_SKILL_DIR}` como sustituciones automáticas de Codex.
