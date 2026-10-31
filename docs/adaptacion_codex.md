# Aplicación de la guía en Codex/GPT

Guía revisada el 31 de octubre de 2026: 24 diapositivas y README de la sesión 16.
Se conservarán el pipeline, las reglas de presentación, las comprobaciones y la rúbrica del curso.
El trabajo avanzará por pasos; terminar la preparación no implica que los análisis ya estén hechos.

## Equivalencias

| En la guía de Claude | En este proyecto con Codex |
|---|---|
| `.claude/skills/<nombre>/` | `.agents/skills/<nombre>/` |
| `~/.claude/skills/` | `~/.agents/skills/` para skills personales; aquí se usarán las del repositorio |
| `SKILL.md` con `name` y `description` | Se conserva el formato; descripción concreta con acción y situaciones de uso |
| `/limpiando-enaho 2024` | `$limpiando-enaho 2024`; también se probará la activación por un pedido natural |
| `${CLAUDE_SKILL_DIR}`, `$ARGUMENTS`, `$0` | No se presupone sustitución. Se escribe la ruta del script y se indica obtener el año del pedido y pasarlo con `--anio` |
| `disable-model-invocation: true` | Si se necesitara impedir la activación implícita, `policy.allow_implicit_invocation: false` en `agents/openai.yaml` |
| `argument-hint`, `user-invocable`, `allowed-tools`, `context: fork` | No se copian como si tuvieran el mismo significado. Este proyecto no los necesita; los permisos siguen siendo los de Codex |
| Carga progresiva | Se conservan metadatos concisos, cuerpo breve y referencias consultadas cuando hagan falta |
| Scripts reproducibles y referencias | Se conservan; las decisiones fijas se implementan en Python |
| `claude -p` | Evaluación mediante `codex exec`, después de verificar las opciones de la versión local |
| `--disallowedTools Skill` | No se inventa un equivalente. Se prepararán sesiones aisladas con las skills del proyecto habilitadas o ausentes/deshabilitadas y se comprobará qué instrucciones cargaron |
| Marketplace de Claude y repositorios sugeridos | Son material opcional. No se ejecutan sus instaladores ni se necesita migrar sus plugins para completar las tres skills |

La documentación oficial indica que Codex detecta cambios en las skills; si no aparecen, puede ser necesario reiniciarlo.
Para que la detección corresponda al proyecto, se debe abrir Codex en `enaho_skills_codex`.

## Paso 1. Preparar

Estado: completado el 31 de octubre de 2026. Se verificaron los ZIP, los 25 códigos geográficos y las importaciones de las cuatro bibliotecas; el entorno coincide con `uv.lock`.

- Crear un repositorio propio con rama `main`.
- Usar Python 3.13 y un entorno local de `uv`.
- Instalar `pandas`, `pyarrow`, `geopandas` y `matplotlib`; guardar `uv.lock`.
- Crear `.agents/skills/`, `datos/`, `salidas/`, `figuras/` y `mapas/`.
- Descargar los dos ZIP, el GeoJSON y la referencia departamental.
- Comprobar integridad y códigos; registrar fuentes y SHA-256.
- Excluir datos y entorno de Git.

## Paso 2. Limpiar

Estado: completado el 31 de octubre de 2026. `limpiando-enaho` está creada y su formato validado.
Se generaron 108 664 filas sin pérdida ni duplicación y con los 25 departamentos. La pobreza resultó 27,57947 % en sumaria y 27,52873 % en personas; extrema 5,50453 % y 5,49978 %.
Pasaron diez pruebas y dos ejecuciones del pipeline produjeron el mismo SHA-256 de la base. Evidencia en `salidas/validacion.txt` y `salidas/validacion_2024.json`.
La activación automática se comprobó junto con los otros pedidos en el paso 4.

Crear `limpiando-enaho/SKILL.md`, su referencia y `scripts/limpiar.py` dentro de `.agents/skills/`.

1. Leer Stata con `convert_categoricals=False`; conservar las llaves y `ubigeo` como texto con sus ceros.
2. Normalizar nombres a minúscula, incluido `aÑo` a `anio`.
3. Filtrar residentes habituales con `((p204 == 1) & (p205 == 2)) | ((p204 == 2) & (p206 == 1))`.
4. Verificar llaves y unir miembros con sumaria mediante `validate="m:1"`, sin perder ni multiplicar personas.
5. Construir departamento a partir de los dos primeros caracteres de `ubigeo`, área urbana con `estrato <= 5` y pobreza con categorías válidas 1 y 2.
6. Validar la estructura y contrastar tasas ponderadas; no tratar valores faltantes de pobreza como personas no pobres.
7. Guardar la base y un informe de validación legible.

Referencias de la clase para 2024: 33 691 hogares, 117 721 registros de miembros y 108 664 residentes habituales.
Pobreza nacional oficial de referencia: 27,6 %, con tolerancia menor a 0,1 puntos porcentuales; extrema: 5,5 %.
La guía informa 27,58 % con `factor07 × mieperho` en sumaria y 27,53 % con `facpob07` en personas.
Se calcularán y reportarán ambas estimaciones por separado. No se ajustarán datos ni pesos para forzar una coincidencia.
Las tasas departamentales del CSV proceden de sumaria; se documentarán las diferencias con la base de personas.

## Paso 3. Graficar y mapear

Estado: completado el 31 de octubre de 2026. Las tres skills tienen su `SKILL.md`, metadatos de Codex y script propio; las de gráficos y mapas remiten a la limpieza si falta la base.
Se generaron gráficos por área, sexo y edad y el mapa de los 25 departamentos, con Lima y Callao separados. Se revisaron los cuatro PNG y se comprobó su resolución de 200 dpi.
Pasaron 22 pruebas. Los scripts verifican el estado y la huella de la base, la ponderación y la unión por código; las 25 tasas del mapa se contrastaron con las personas.
El CSV del mapa documenta las diferencias con la referencia de sumaria del curso, sin sustituir los resultados calculados con `facpob07`.
La activación y el encadenamiento en pedidos naturales se comprobaron en el paso 4, incluida una copia sin base limpia al inicio.

Crear las otras dos skills, cada una con su script. Si falta la base, indicar que debe usarse primero `limpiando-enaho`.
Leer `salidas/validacion.txt` antes de publicar cualquier resultado como validado.

Gráficos: ponderar con `facpob07`; barras ordenadas desde cero, un solo color y valores en cada barra;
título con tema y año; pie «Fuente: INEI, ENAHO 2024»; PNG a 200 dpi en `figuras/`.

Mapa: calcular pobreza ponderada por departamento; unir códigos de dos caracteres con `FIRST_IDDP`, nunca nombres;
exigir 25 departamentos únicos con dato; Lima y Callao separados; escala secuencial de claro a oscuro desde cero;
leyenda «% de personas»; guardar `mapas/pobreza_departamento.png`.

Contrastes de la clase, calculados con sumaria: Cajamarca 45,0 %, Loreto 43,0 %, Puno 39,9 %;
Ica 6,0 %, Moquegua 11,0 % y Madre de Dios 11,1 %.

## Paso 4. Evaluar y entregar

Estado: evaluación local completada. Se verificó en el registro de un chat local la activación de `limpiando-enaho`, la ejecución de su script y el cálculo de Cusco con `facpob07`: 18,5392948871 %.
También se verificó `graficando-enaho`: leyó las skills de gráficos y limpieza, reutilizó la base validada y ejecutó solo `graficar.py`. El gráfico rural/urbano dio 39,44168 % / 24,73524 %, con una brecha de 14,70644 puntos; PNG y ponderación comprobados.
También se verificó `mapeando-enaho`: el chat ejecutó limpieza seguida de mapa, validó 25 códigos y recalculó las 25 tasas; Lima y Callao quedaron separados. Las tres pruebas con skills tienen evidencia de uso.
El detalle y las limitaciones del estado inicial están en `evaluacion.md`.
Se completaron los tres casos en la copia vecina `enaho_sin_skills`, sin los tres manifiestos y conservando datos, código, documentación y resultados. Cusco respondió 18,5 % por consulta web; gráfico y mapa encontraron y ejecutaron directamente los programas existentes y produjeron las mismas tasas y píxeles que con skills. La revisión de los registros respalda sus declaraciones de no haber cargado ningún `SKILL.md`. Los 40 archivos de la instantánea conservaron el mismo contenido. La comparación de los seis casos está documentada; no se observó mejora numérica o visual atribuible a los manifiestos cuando el código ya estaba disponible. Los límites del protocolo están en `docs/control_sin_skills.md` y `evaluacion.md`.
Una prueba adicional mediante Codex CLI en `enaho_sin_base`, con GPT-6.1 Sol y `xhigh`, comenzó sin base limpia ni salidas previas. El modelo leyó las skills de mapa y limpieza y ejecutó `limpiar.py`, consultó la validación OK y ejecutó `mapear.py`. Se comprobaron las 108 664 personas, los 25 territorios, los pesos, las tasas y la conservación de los 23 archivos iniciales. La base generada y el mapa coincidieron con los del proyecto principal. Esta es una comprobación funcional separada de las seis comparaciones en Work.

Comparar estos tres pedidos con y sin las skills del proyecto:

1. «¿Cuál fue la pobreza en Cusco en 2024?» Referencia de sumaria: 18,5 %.
2. «Grafica la pobreza urbana y rural». Referencias de sumaria: 24,8 % y 39,3 %.
3. «Haz un mapa de la pobreza por departamento». Comprobar unión y los 25 departamentos con dato.

Usar el mismo modelo disponible, pedido, entradas y estado inicial en ambas condiciones; separar salidas para evitar reutilización accidental.
Registrar en `evaluacion.md` las skills observadas, las tasas, los pesos y la revisión visual, con evidencia real de las ejecuciones.
No afirmar activación por el mero hecho de que una skill exista.
Actualizar README con comandos que se hayan comprobado y conservar `salidas/validacion.txt`, figuras y mapa.

Rúbrica: limpieza 6 puntos; gráficos 4; mapa 4; evaluación 4; README 2.
La demostración del mapa, un gráfico, la validación y el pedido que encadenó dos skills está preparada en `docs/demostracion.md`.

## Fuentes

- [Presentación](https://claude.ai/artifact/X7H6PUvaWKde1epsYCJNze).
- [Consigna de la sesión](https://github.com/d2cml-ai/Data-Science-Python/blob/main/sessions/16-skills-enaho/README.md).
- [Skills en Codex](https://learn.chatgpt.com/docs/build-skills).
- [Instrucciones persistentes con AGENTS.md](https://learn.chatgpt.com/docs/agent-configuration/agents-md).
