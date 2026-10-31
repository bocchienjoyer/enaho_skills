# Comparación sin los manifiestos de las skills de ENAHO

## Copia preparada

La carpeta vecina `enaho_sin_skills` es una instantánea independiente del proyecto, preparada después de las tres demostraciones con skills.
Se creó mediante `scripts/preparar_control.py`, que no sobrescribe destinos existentes.
Se contrastaron 40 archivos con el origen al copiar; sus huellas están en `referencias/control_sin_skills_2024.json`.

Se conservan los datos, la base validada, los scripts, las referencias, la documentación y los resultados ya existentes.
Se excluyen únicamente estos manifiestos de instrucciones:

- `.agents/skills/limpiando-enaho/SKILL.md`
- `.agents/skills/graficando-enaho/SKILL.md`
- `.agents/skills/mapeando-enaho/SKILL.md`

Por tanto, los scripts dentro de `.agents/skills/` siguen disponibles para una ejecución directa, aunque esas carpetas ya no constituyen skills descubribles sin su archivo obligatorio.
Las demás skills personales o del sistema conservan su disponibilidad habitual.
El proyecto original mantiene sus tres skills.

## Verificar antes de analizar

1. Crear otro proyecto local con `enaho_sin_skills` como carpeta principal.
2. Abrir un chat nuevo en ese proyecto, en el mismo modo Work usado antes.
3. Elegir GPT-6.1 Sol con razonamiento «Muy alto».
4. Pedir que indique primero su carpeta de trabajo actual: debe terminar en `enaho_sin_skills`. Después comprobar si las tres skills de ENAHO figuran en la lista recibida al iniciar el chat. Distinguir la lista de skills de las menciones en el README o de los scripts que aún existen.
5. Continuar solo cuando las tres estén ausentes de la lista. Si aparece alguna, revisar su ruta y la carpeta principal antes de considerar válida la condición sin skills.

Esta comprobación debe hacerse en la interfaz de Work; una inspección local preliminar con `codex debug prompt-input` no permitió confirmar la lista.
Un chat nuevo abierto dentro de `enaho` sigue usando la carpeta original `enaho_skills_codex`. Para la condición de control se necesita un proyecto separado que tenga `enaho_sin_skills` como carpeta principal; se confirmó que el primer intento de comprobación se hizo todavía en la carpeta original y se descartó de la evaluación sin skills.

La comprobación posterior sí se realizó en la carpeta correcta: el registro del chat «Comprueba skills de ENAHO» confirma `enaho_sin_skills`, y la respuesta declara ausentes las tres skills en su lista inicial. Se comprobaron cero manifiestos y la integridad de los 40 archivos de la instantánea. Los tres casos sin skills ya están completados: Cusco respondió 18,5 % con una fuente web; gráfico y mapa ejecutaron directamente el código conservado, sin leer ningún `SKILL.md`, y obtuvieron las mismas tasas e imágenes. El registro del mapa confirma además 22 pruebas aprobadas y una comprobación independiente de las 25 tasas.

## Pedidos para la comparación

Usar chats nuevos y mantener el modelo y nivel. Antes de cada caso, comprobar que no se hayan añadido manifiestos de ENAHO ni cambiado los datos o scripts de control.
Registrar las acciones reales y los resultados en el proyecto original, en `evaluacion.md`.

### Caso 1

Primer mensaje:

> ¿Cuál fue la pobreza en Cusco en 2024?

Después del resultado, segundo mensaje:

> indica qué skills utilizaste realmente, qué scripts ejecutaste y qué factor de expansión aplicaste.

### Caso 2

Primer mensaje:

> Grafica la pobreza urbana y rural con la ENAHO 2024.

Después del resultado, enviar el mismo segundo mensaje del caso 1.

### Caso 3

Enviar en un solo mensaje:

> Haz un mapa de la pobreza por departamento del Perú con la ENAHO 2024.
> Al terminar, indica qué skills utilizaste realmente, qué scripts ejecutaste, qué factor de expansión aplicaste y cómo verificaste la unión de los 25 departamentos y la separación de Lima y Callao.

## Qué permite concluir

La frase «no utilicé ninguna skill» responde a la auditoría solicitada por el usuario. Los registros confirman la ausencia de lecturas de `SKILL.md`; los scripts y documentos siguieron disponibles y permitieron reproducir las salidas.

Esta condición compara el comportamiento con y sin los tres manifiestos y su descubrimiento automático, manteniendo disponibles los scripts y resultados.
Puede obtener cifras y figuras correctas mediante ejecución directa o consulta de salidas existentes: no se debe esperar ni forzar un fallo.
Es una comparación descriptiva, con una instantánea posterior a las pruebas con skills. No mantiene idéntica toda la documentación previa de cada chat ni demuestra por sí sola una mejora causal, independencia de los scripts o capacidad de reconstruir el análisis desde datos sin procesar.

La demostración condicional de encadenamiento sin base previa se completó en otra copia, `enaho_sin_base`, que conservó los tres manifiestos. Codex CLI seleccionó las skills de mapa y limpieza, generó y validó la base y después ejecutó el mapa. No se alteró la base del proyecto principal. Esta comprobación funcional es adicional a la comparación de seis casos; está documentada en `evaluacion.md` y `referencias/encadenamiento_sin_base_2024.json`.

Fuente sobre el requisito de `SKILL.md` y el descubrimiento de skills locales: [documentación oficial de Codex](https://learn.chatgpt.com/docs/build-skills).
