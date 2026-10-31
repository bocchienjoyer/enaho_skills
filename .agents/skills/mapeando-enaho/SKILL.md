---
name: mapeando-enaho
description: Crea un mapa de pobreza monetaria por departamento del Perú con ENAHO 2024, pondera personas con facpob07 y une los 25 departamentos por código. Úsala cuando pidan un mapa departamental de pobreza o su distribución geográfica con ENAHO.
---

# Mapear pobreza de ENAHO 2024

1. Trabajar desde la raíz del repositorio. Si falta `salidas/personas_2024.parquet`, usar primero la skill [limpiando-enaho](../limpiando-enaho/SKILL.md). Exigir limpieza satisfactoria y leer `salidas/validacion.txt`. Usar 2024 si el pedido omite año y decirlo; otro año requiere una implementación y referencias propias.
2. Comprobar `datos/peru_departamental_simple.geojson`; si falta, ejecutar `uv run --frozen python scripts/preparar_datos.py` para obtener el archivo indicado en la guía.
3. Ejecutar el script de esta skill:

   ```powershell
   uv run --frozen python .agents/skills/mapeando-enaho/scripts/mapear.py --anio 2024
   ```

   Si `uv` no está en PATH, usar `.\.tools\bin\uv.exe run --frozen --cache-dir .uv-cache python` seguido de la misma ruta y argumentos.
4. El script comprueba el estado y SHA-256 de la base mediante `scripts/enaho_comun.py`, agrega con `facpob07` y une `departamento = ubigeo[:2]` con `FIRST_IDDP` como texto de dos caracteres. No unir nombres, rellenar tasas faltantes con cero ni disolver Lima `15` y Callao `07`.
5. Exigir 25 códigos únicos a ambos lados de la unión, correspondencia completa y ninguna tasa faltante. Si cualquier control falla, detenerse; si falla la validación de la base, resolver con `limpiando-enaho` antes de repetir. No presentar un mapa anterior como generado por la ejecución fallida.
6. Revisar `mapas/pobreza_departamento.png`: escala secuencial de azul claro a oscuro desde cero, leyenda «% de personas», título con año, fuente del INEI y detalle que permita distinguir Callao de Lima. El PNG se guarda a 200 dpi.
7. Responder con el mapa y las cifras del CSV adjunto, identificando residentes habituales y peso `facpob07`. El CSV conserva los códigos y, si está disponible la referencia de la sesión, añade su tasa de sumaria y la diferencia en puntos porcentuales. No reemplazar la estimación de personas por las cifras de sumaria para hacerlas coincidir. El JSON adjunto registra las huellas y los controles de la unión.

Para interpretar códigos o ampliar variables, consultar el [esquema de ENAHO](../limpiando-enaho/references/esquema_2024.md). Para barras por área, sexo o edad, usar `graficando-enaho`.
