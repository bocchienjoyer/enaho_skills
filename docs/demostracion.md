# Demostración de ENAHO con Codex

Recorrido de unos tres minutos para mostrar el trabajo de la sesión 16, adaptado a Codex/GPT.

## 1. Mostrar las tres skills

Abrir `.agents/skills/`: `limpiando-enaho`, `graficando-enaho` y `mapeando-enaho`.
Cada una tiene instrucciones en `SKILL.md` y un programa de Python. Las instrucciones permiten al modelo elegir el flujo; los programas fijan filtros, pesos y controles.

## 2. Mostrar la validación

Abrir [salidas/validacion.txt](../salidas/validacion.txt): estado **OK**, 33 691 hogares y **108 664 residentes habituales**, sin pérdidas ni multiplicaciones de personas.
La pobreza nacional es **27,52873 %** con personas y `facpob07`; la comprobación de sumaria da **27,57947 %** con `factor07 × mieperho`. Ambas están a menos de 0,1 puntos de la referencia de 27,6 %.

## 3. Mostrar el gráfico y el mapa

Abrir [el gráfico urbano y rural](../figuras/pobreza_area_2024.png): **24,7 % urbana** y **39,4 % rural**, brecha de **14,7 puntos porcentuales**.

Abrir [el mapa](../mapas/pobreza_departamento.png): 24 departamentos y Callao, unidos por códigos de dos caracteres. Destacar la leyenda desde cero y el detalle de Lima y Callao, con **26,9 %** y **33,8 %** por separado.
Todos estos resultados usan residentes habituales y `facpob07`.

## 4. Explicar el pedido que encadenó dos skills

Pedido: «Haz un mapa de la pobreza por departamento del Perú con la ENAHO 2024».

La prueba adicional comenzó en `enaho_sin_base`, con los ZIP y las tres skills, sin base limpia ni figuras previas. El registro confirma esta secuencia:

1. Lectura de `mapeando-enaho` y `limpiando-enaho`.
2. Ejecución de `limpiar.py --anio 2024`.
3. Lectura de los informes de validación: **OK**.
4. Ejecución de `mapear.py --anio 2024`.

Mostrar el resumen en [evaluacion.md](../evaluacion.md#prueba-adicional--encadenamiento-sin-base-limpia) y el [registro de comprobación](../referencias/encadenamiento_sin_base_2024.json).
Se realizó con Codex CLI, GPT-6.1 Sol y razonamiento `xhigh`; las seis comparaciones anteriores se hicieron en Work.

## 5. Explicar la comparación con y sin manifiestos

En los seis casos documentados, las cifras redondeadas coincidieron. Sin los tres `SKILL.md`, el modelo consultó una fuente publicada para Cusco y ejecutó los programas conservados para el gráfico y el mapa. Estos dos resultados tuvieron las mismas tasas y los mismos píxeles.

La comparación muestra dos formas de llegar al resultado: seguir instrucciones de skills o encontrar directamente el código disponible. No establece una mejora causal de exactitud o apariencia. Los límites y las acciones observadas están documentados en [evaluacion.md](../evaluacion.md) y [docs/control_sin_skills.md](control_sin_skills.md).
