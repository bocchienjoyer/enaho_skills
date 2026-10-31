# Evaluación de las skills de ENAHO 2024

## Estado y alcance

Evaluación y prueba funcional documentadas el 31 de octubre de 2026.
Entorno del usuario: ChatGPT Desktop, modo Work, proyecto local `enaho` con carpeta principal `enaho_skills_codex`.
Las skills están escritas para Codex y fueron recibidas por el chat del proyecto. Las pruebas manuales de esta sección no son ejecuciones de `codex exec`.
La prueba adicional sin base previa, descrita al final, sí se ejecutó con Codex CLI y se registra por separado.
Modelo: **GPT-6.1 Sol**. Nivel de razonamiento: **«Muy alto»**. Ambos fueron confirmados por el usuario a partir del selector de ese chat; mantenerlos iguales al comparar condiciones.

| Caso | Con skills | Sin skills |
|---|---|---|
| Pobreza en Cusco | Activación y cálculo comprobados en el registro | Consulta web: 18,5 %, sin cálculo local; registro comprobado |
| Gráfico urbano y rural | Lecturas de skills, ejecución y gráfico comprobados | Ejecución directa del mismo script; tasas y PNG idénticos |
| Mapa por departamento | Limpieza seguida de mapa, 25 tasas y unión comprobadas | Ejecución directa de mapear.py, 22 pruebas, mismas tasas y PNG |

La disponibilidad de las tres skills ya fue reportada por el usuario desde un chat del proyecto: aparecían en la lista inicial y también como archivos.
La activación se evalúa con lecturas y ejecuciones observadas; no se deduce de que existan los archivos o de que el asistente diga haberlas usado.

## Caso 1 · Cusco · con skills

Chat inspeccionado: «Consultar pobreza en Cusco 2024».
El usuario compartió las respuestas y se consultó además el registro de acciones de ese chat mediante las herramientas de lectura de chats.

Pedido inicial, sin nombrar una skill:

> ¿Cuál fue la pobreza en Cusco en 2024?

Después del resultado, el usuario envió este pedido de auditoría en un segundo mensaje:

> indica qué skills utilizaste realmente, qué scripts ejecutaste y qué factor de expansión aplicaste.

Estado inicial observado: ya existían los ZIP, la base validada y el CSV del mapa generado durante el desarrollo. Este caso demuestra selección y ejecución de la skill con una base previa; no es una prueba desde datos sin procesar ni una comparación aislada con/sin skills.

### Evidencia de uso

1. La primera acción del chat leyó `.agents/skills/limpiando-enaho/SKILL.md` con salida 0. También leyó su referencia `references/esquema_2024.md`.
2. Ejecutó este comando con salida 0:

   ```powershell
   .\.tools\bin\uv.exe run --frozen --cache-dir .uv-cache python .agents/skills/limpiando-enaho/scripts/limpiar.py --anio 2024
   ```

   El registro devolvió `OK: 108,664 residentes; pobreza de personas 27.52873 %`.
3. Leyó `salidas/validacion.txt` y `salidas/validacion_2024.json`, con estado OK.
4. Ejecutó Python en línea con `cargar_base_validada` y `agrupar_pobreza` de `scripts/enaho_comun.py`. Filtró `departamento == '08'` y el registro devolvió:

   ```json
   {"grupo":"08","n_personas":3777,"poblacion_expandida":1380357.0042934418,"poblacion_pobre":255908.4555206299,"pobreza_pct":18.5392948871}
   ```

5. Consultó además el CSV del mapa ya existente. No se observaron lecturas ni ejecuciones de las skills de gráficos o mapas.

La habilidad se seleccionó a partir del pedido natural: el usuario no incluyó `$limpiando-enaho` en el pedido inicial.
Hubo dos comandos auxiliares de exploración con salida 1, al buscar instrucciones o archivos sin coincidencias; la limpieza y el cálculo de Cusco finalizaron con salida 0.

### Resultado

- Skill observada: `limpiando-enaho`.
- Universo: residentes habituales del departamento de Cusco; 3777 observaciones.
- Factor de expansión: `facpob07`.
- Cálculo: `100 × suma(facpob07 × indicador(pobreza en {1, 2})) / suma(facpob07)`.
- Pobreza: **18,5392948871 %**, presentada como **18,54 %** o **18,5 %**.
- Referencia de sumaria del curso: 18,5 %, redondeada a un decimal; no se sustituyó el cálculo de personas por esa referencia.
- Figura: no solicitada ni generada.
- Comprobación independiente en esta revisión: el cálculo sobre la base local validada reprodujo 18,5392948871 %.

Conclusión del caso: disponibilidad, selección de la skill, ejecución del pipeline y ponderación de personas comprobadas. Todavía no permite atribuir una mejora respecto de una condición sin skills.

## Caso 2 · Gráfico urbano y rural · con skills

Chat inspeccionado: «Graficar pobreza urbana y rural».
Se contrastaron la respuesta y la imagen compartidas por el usuario con el registro de acciones del chat y los archivos locales generados.

Pedido inicial, sin nombrar skills:

> Grafica la pobreza urbana y rural con la ENAHO 2024.

Después del resultado, el usuario envió el mismo pedido de auditoría del caso 1 en otro mensaje:

> indica qué skills utilizaste realmente, qué scripts ejecutaste y qué factor de expansión aplicaste.

Estado inicial: existía la base de personas y los informes de limpieza estaban en OK; también existían figuras del desarrollo. El chat volvió a ejecutar el script de gráficos.
Se pidió conservar GPT-6.1 Sol con razonamiento «Muy alto», la configuración de referencia confirmada por el usuario en el caso 1; la herramienta de lectura del registro no expone el modelo ni ese nivel para confirmar por sí sola la configuración del segundo chat.

### Evidencia de uso

1. Leyó `.agents/skills/graficando-enaho/SKILL.md` y `.agents/skills/limpiando-enaho/SKILL.md`, ambas con salida 0. También consultó el esquema de limpieza y `scripts/enaho_comun.py`.
2. Leyó `salidas/validacion.txt` y `salidas/validacion_2024.json`, con estado OK.
3. Ejecutó el siguiente comando con salida 0:

   ```powershell
   .\.tools\bin\uv.exe run --frozen --cache-dir .uv-cache python .agents/skills/graficando-enaho/scripts/graficar.py --anio 2024 --por area
   ```

   El registro devolvió `OK: figuras/pobreza_area_2024.png; peso facpob07`, `Rural: 39,4 %` y `Urbana: 24,7 %`.
4. Abrió el PNG para revisarlo y leyó el CSV y JSON generados.
5. No se observó ejecución de `limpiar.py` ni uso de `mapeando-enaho`. Se distingue la consulta de la skill de limpieza de la ejecución efectiva de su pipeline.

Un comando auxiliar terminó con salida 1 al buscar `uv` en PATH; el chat utilizó la instalación local `.tools/bin/uv.exe` y la generación del gráfico concluyó con salida 0.

### Resultado y comprobación de la figura

| Área | Observaciones | Pobreza ponderada |
|---|---:|---:|
| Rural | 36 071 | 39,4416811491 % |
| Urbana | 72 593 | 24,7352366368 % |

- Universo: residentes habituales; factor de expansión `facpob07`.
- Pobreza: categorías 1 y 2, extrema y no extrema.
- Brecha rural menos urbana: **14,7064445122 puntos porcentuales**, presentada como **14,7**.
- Skill aplicada al resultado: `graficando-enaho`; skill de limpieza consultada sin volver a ejecutar su script.
- PNG: `figuras/pobreza_area_2024.png`, 1920 × 1120 píxeles, resolución efectiva 199,9996 dpi (200 dpi nominales).
- Revisión visual: barras ordenadas de mayor a menor desde cero, un solo color, valores visibles, título con tema y año, fuente del INEI y nota del peso.
- Trazabilidad: el JSON registra `facpob07` y el SHA-256 coincide con la base validada.
- Comprobación independiente: se recalcularon ambas tasas desde la base de personas y coincidieron con el CSV.

Conclusión del caso: selección y uso de la skill de gráficos comprobados, con ponderación y figura correctas. La consulta de dos skills con una base ya existente no demuestra todavía el encadenamiento completo desde datos sin procesar.

## Caso 3 · Mapa por departamento · con skills

Chat inspeccionado: «Mapea pobreza por departamento».
Se revisaron las acciones del chat, la imagen compartida por el usuario y `mapas/verificacion_union_2024.json`.
En un mismo mensaje, sin nombrar skills, el usuario pidió:

> Haz un mapa de la pobreza por departamento del Perú con la ENAHO 2024.
> Al terminar, indica qué skills utilizaste realmente, qué scripts ejecutaste, qué factor de expansión aplicaste y cómo verificaste la unión de los 25 departamentos y la separación de Lima y Callao.

Estado inicial: ya existían la base validada y el mapa del desarrollo. Aun así, el chat ejecutó nuevamente la limpieza y después el mapa.
Se pidió conservar GPT-6.1 Sol con razonamiento «Muy alto»; la herramienta de lectura del chat no expone esos selectores para verificarlos de manera independiente.

### Evidencia de uso

1. Leyó los `SKILL.md` de `mapeando-enaho` y `limpiando-enaho`, sus scripts y la referencia de limpieza.
2. Ejecutó, en este orden y con salida 0:

   ```powershell
   .\.tools\bin\uv.exe run --frozen --cache-dir .uv-cache python .agents/skills/limpiando-enaho/scripts/limpiar.py --anio 2024
   .\.tools\bin\uv.exe run --frozen --cache-dir .uv-cache python .agents/skills/mapeando-enaho/scripts/mapear.py --anio 2024
   ```

3. Entre ambos comandos leyó los informes de limpieza y comprobó estado OK, con 108 664 residentes habituales.
4. Abrió el mapa, leyó su CSV y JSON y ejecutó una comprobación adicional en Python con salida 0. Guardó los controles en `mapas/verificacion_union_2024.json`.
5. No se observó uso de `graficando-enaho`.

### Resultado y controles

- Universo: 108 664 residentes habituales; peso `facpob07`; pobreza igual a categorías 1 o 2.
- La base de personas, el GeoJSON y el CSV contienen los 25 códigos, `01` a `25`; en las tablas departamentales y geometrías son únicos.
- Unión del mapa: código `departamento = ubigeo[:2]` con `FIRST_IDDP`, conservando dos caracteres y cardinalidad 1:1.
- Auditoría adicional con unión externa: 25 coincidencias, cero códigos sin correspondencia, cero tasas faltantes y 25 geometrías válidas.
- Las 25 tasas recalculadas desde personas coinciden con el CSV; el informe registra diferencia máxima de 0 puntos porcentuales.
- Callao `07`: 3457 observaciones, **33,7683435697 %**.
- Lima `15`: 14 823 observaciones, **26,8887692770 %**.
- Nombres, códigos y geometrías de Lima y Callao distintos; permanecen separados y visibles en el detalle del mapa.
- PNG: `mapas/pobreza_departamento.png`, 2400 × 2000 píxeles, 200 dpi nominales; escala secuencial azul con mínimo 0, leyenda «% de personas», título con año y fuente.
- Comprobación independiente de esta revisión: se reconstruyó la unión, se recalcularon las 25 tasas y se verificaron el SHA-256 de la base y la resolución del PNG.

Conclusión del caso: las dos skills se seleccionaron desde un pedido natural y ejecutaron limpieza seguida de mapa. Esto proporciona la demostración de un pedido que utiliza dos skills consecutivas. Como la base ya existía al iniciar el chat, la condición específica «si falta la base» se probará aparte.

## Comprobación previa de la condición sin skills

- Se preparó la carpeta vecina `enaho_sin_skills`, sin los tres `SKILL.md` y con los scripts, datos, documentación y resultados conservados. Se contrastaron 40 archivos por SHA-256 al copiar; manifiesto en `referencias/control_sin_skills_2024.json`.
- La comprobación correcta se realizó en el chat «Comprueba skills de ENAHO»: el registro confirma `enaho_sin_skills` como carpeta de trabajo y su respuesta declara que las tres skills de ENAHO están ausentes de la lista inicial. No hubo ejecución de análisis ni lectura de documentos en ese chat.
- La revisión local posterior confirmó cero `SKILL.md` en la copia y coincidencia de los 40 archivos con las huellas de la instantánea. Se completaron después los tres pedidos sin skills; los resultados se detallan a continuación.
- El primer intento manual de comprobar esa ausencia se hizo en el chat «Verifica la lista de skills ENAHO». Su registro confirma que la carpeta de trabajo seguía siendo `enaho_skills_codex`, el proyecto original; por eso recibió las tres skills. Ese intento no cuenta como condición sin skills ni demuestra un fallo de aislamiento de la copia. Se debe abrir un chat cuya carpeta principal sea `enaho_sin_skills` y comprobar también esa ruta.
- Seguir [docs/control_sin_skills.md](docs/control_sin_skills.md), con los pedidos exactos usados en los tres chats. La comparación será descriptiva: se conserva código y resultados, y la instantánea es posterior a las demostraciones con skills.

## Caso 1 · Cusco · sin skills

Chat inspeccionado: «Consultar pobreza en Cusco 2024», cuya carpeta de trabajo en el registro es `enaho_sin_skills`.
Se usaron los mismos dos mensajes que en la condición con skills:

> ¿Cuál fue la pobreza en Cusco en 2024?

Después del resultado:

> indica qué skills utilizaste realmente, qué scripts ejecutaste y qué factor de expansión aplicaste.

### Evidencia de la ejecución

1. El chat anunció que consultaría la cifra oficial del INEI.
2. El registro contiene búsquedas web y aperturas de la publicación del INEI sobre pobreza 2015–2024 y su PDF. No contiene ejecuciones de comandos locales, lecturas de skills ni ejecución de scripts del proyecto.
3. La respuesta dio **18,5 %** y enlazó el [informe de gasto social 2024 del MEF](https://www.mef.gob.pe/contenidos/presu_publ/ppr/gasto_social2024.pdf), atribuyendo la cifra al INEI.
4. En el segundo mensaje declaró que no usó skills, no procesó microdatos y no aplicó un factor de expansión por su cuenta. Esto coincide con las acciones observadas.
5. La revisión local confirmó que los 40 archivos de la instantánea seguían intactos y que no había aparecido ningún `SKILL.md` en el proyecto de control.

### Comparación con skills / sin skills

| Aspecto | Con skills | Sin skills |
|---|---|---|
| Resultado presentado | 18,5393 %, redondeado a 18,5 % | 18,5 %, cifra publicada |
| Procedimiento observado | Limpieza, validación y cálculo sobre personas de Cusco | Consulta de fuentes en la web |
| Skill ENAHO utilizada | `limpiando-enaho` | Ninguna |
| Scripts locales ejecutados | `limpiar.py` y cálculo en Python con funciones compartidas | Ninguno |
| Ponderación aplicada por el chat | `facpob07` | No hizo una ponderación propia |
| Archivos del proyecto usados para calcular | Base de personas validada | No se observaron lecturas de archivos locales |

La cifra publicada puede responder correctamente a una consulta informativa; la pregunta inicial no exigía recalcular los microdatos.
La ponderación de esa estadística publicada corresponde al productor de la fuente, mientras que el chat sin skills se limitó a citarla.
La coincidencia a un decimal no prueba que ambos procedimientos hayan producido la misma estimación sin redondear.

Conclusión de esta primera comparación: coincide la cifra redondeada y cambia el procedimiento. En la condición con skills quedó demostrada la reproducción local con un peso explícito y controles; en la condición sin skills se resolvió la consulta mediante una publicación externa. No se demuestra una mejora causal de exactitud ni una incapacidad del modelo sin skills para procesar la base.

## Caso 2 · Gráfico urbano y rural · sin skills

Chat inspeccionado: «Graficar pobreza urbana y rural», con carpeta de trabajo `enaho_sin_skills` confirmada en su registro.
Se usaron los mismos dos mensajes que en la condición con skills:

> Grafica la pobreza urbana y rural con la ENAHO 2024.

Después del resultado:

> indica qué skills utilizaste realmente, qué scripts ejecutaste y qué factor de expansión aplicaste.

### Evidencia de ejecución

1. Exploró los archivos del proyecto y leyó el README, los informes de validación, `scripts/enaho_comun.py`, el script de gráficos y las pruebas existentes.
2. No se observó lectura de ningún `SKILL.md`; la copia sigue sin contener esos tres manifiestos.
3. Ejecutó directamente el script existente con salida 0:

   ```powershell
   .\.venv\Scripts\python.exe .agents/skills/graficando-enaho/scripts/graficar.py --anio 2024 --por area
   ```

4. El comando devolvió `OK: figuras/pobreza_area_2024.png; peso facpob07`, `Rural: 39,4 %` y `Urbana: 24,7 %`.
5. Abrió el PNG y ejecutó una comprobación adicional en Python con salida 0: cargó la base validada, recalculó las tasas por área y contrastó el CSV. El registro devolvió 108 664 filas verificadas, 24,7352366368 % urbana, 39,4416811491 % rural y una brecha de 14,7064445122 puntos.
6. En la auditoría declaró no haber utilizado skills y sí haber ejecutado ese script y la comprobación. La declaración coincide con el registro.

La ubicación del script dentro de `.agents/skills/` no implica que se haya cargado una skill: los manifiestos fueron excluidos del control, pero el código y la documentación permanecen disponibles.

### Comparación con skills / sin skills

| Aspecto | Con skills | Sin skills |
|---|---|---|
| Lectura de instrucciones de skill | `graficando-enaho` y consulta de `limpiando-enaho` | Ningún `SKILL.md` leído |
| Código del gráfico | `graficar.py`, lanzado con `uv run` | El mismo `graficar.py`, lanzado con Python de `.venv` |
| Factor y universo | `facpob07`, residentes habituales | `facpob07`, residentes habituales |
| Pobreza urbana | 24,7352366368 % | 24,7352366368 % |
| Pobreza rural | 39,4416811491 % | 39,4416811491 % |
| Brecha rural menos urbana | 14,7064445122 puntos | 14,7064445122 puntos |
| Apariencia del PNG | Pautas de la guía cumplidas | Mismos píxeles que la condición con skills |

La revisión independiente confirmó las tasas mediante una suma ponderada directa sobre `pobreza` y `facpob07`, el PNG de 1920 × 1120 píxeles a 200 dpi nominales y la igualdad píxel a píxel entre condiciones.
Los 40 archivos de la instantánea conservaron sus huellas: hubo una nueva ejecución y generación de salidas, con contenido idéntico; la evidencia de ejecución procede del registro del chat.
No se modificó el código ni se crearon manifiestos de skills.

Conclusión del caso: el modelo sin los manifiestos encontró y reutilizó el código disponible y obtuvo el mismo resultado numérico y visual. En esta ejecución, la reproducibilidad del gráfico está respaldada por la misma base y el mismo script determinista. No se observa una ventaja de exactitud o formato atribuible a cargar la skill; tampoco se evaluó construir el gráfico sin disponer de ese código.

## Caso 3 · Mapa por departamento · sin skills

Chat inspeccionado: «Mapea la pobreza por departamento», con carpeta de trabajo `enaho_sin_skills`.
El usuario envió primero:

> Haz un mapa de la pobreza por departamento del Perú con la ENAHO 2024.

Después del resultado solicitó:

> indica qué skills utilizaste realmente, qué scripts ejecutaste, qué factor de expansión aplicaste y cómo verificaste la unión de los 25 departamentos y la separación de Lima y Callao.

El pedido principal coincide con la condición con skills; la auditoría fue un segundo mensaje en este caso y formaba parte del primer mensaje en la condición con skills. Esta diferencia de organización se conserva como limitación del protocolo.

### Evidencia de ejecución

1. Exploró el proyecto y leyó README, documentación, evaluación previa, informes de validación, código de mapas y pruebas existentes.
2. No se observaron lecturas de ningún `SKILL.md`, y la copia siguió sin esos manifiestos.
3. Ejecutó directamente, con salida 0:

   ```powershell
   .venv/Scripts/python.exe .agents/skills/mapeando-enaho/scripts/mapear.py --anio 2024
   .venv/Scripts/python.exe -m unittest discover -s tests -v
   ```

   El mapa informó 25 territorios y peso `facpob07`; la suite informó **22 pruebas aprobadas**.
4. Reutilizó la base validada de 108 664 residentes habituales. No se observó ejecución de `limpiar.py` ni descarga de microdatos.
5. Ejecutó una comprobación adicional en Python con NumPy: recalculó las 25 tasas y las contrastó con el CSV. El registro devolvió diferencia máxima de **7,1054273576 × 10⁻¹⁵ puntos porcentuales**, compatible con precisión de coma flotante.
6. Abrió el PNG para revisarlo. En el mensaje de auditoría ejecutó otra comprobación sobre Lima y Callao: códigos, muestras y geometrías distintos, con personas de cada territorio sin superposición.

### Comparación y resultado

| Aspecto | Con skills | Sin skills |
|---|---|---|
| Instrucciones de skill leídas | `limpiando-enaho` y `mapeando-enaho` | Ningún `SKILL.md` |
| Pipeline ejecutado | Limpieza y después mapa | Mismo script de mapa, con base existente |
| Factor de expansión | `facpob07` | `facpob07` |
| Correspondencia territorial | 25 códigos, unión 1:1, sin faltantes | Mismos controles y recálculo independiente |
| Lima / Callao | 26,8887692770 % / 33,7683435697 % | Mismas tasas y códigos 15 / 07 separados |
| Tasas del CSV | 25 tasas de personas | CSV idéntico |
| Mapa PNG | Revisado y generado a 200 dpi | Mismos píxeles y 200 dpi |

La revisión independiente volvió a comprobar los 25 códigos, las geometrías y tasas, la correspondencia 1:1, Lima y Callao por separado y la igualdad entre los CSV y los píxeles de los mapas.
El PNG mide 2400 × 2000 píxeles. Los 40 archivos de la instantánea conservaron el mismo contenido y siguieron ausentes los manifiestos.
El informe detallado de unión que ya existía en la instantánea se consultó como referencia; las nuevas comprobaciones están acreditadas por las ejecuciones y sus salidas, no por atribuir una nueva creación a ese archivo previo.

Conclusión del caso: sin cargar instrucciones de skill, el modelo encontró el código existente, generó el mapa, ejecutó las pruebas y comprobó la unión. La igualdad numérica y visual se obtuvo con el mismo script y la misma base; no se ensayó reconstruir todo el pipeline sin esos recursos.

## Qué significa «no utilicé ninguna skill» en el control

El usuario pidió explícitamente una auditoría de skills, scripts y pesos. Esa pregunta explica que las respuestas incluyan una declaración de uso o ausencia de skills.
En este control se excluyeron los tres `SKILL.md`, mientras que se conservaron los scripts, referencias, pruebas, README, evaluación previa, base y resultados.
La documentación conservada también menciona las skills y los comandos para ejecutar sus programas.
Ejecutar `mapear.py` o `graficar.py` no requiere cargar el archivo de instrucciones que normalmente describe cuándo y cómo usarlos.

Por ello, la lectura de código y la ejecución directa de un programa dentro de `.agents/skills/` se registran separadas de cargar una skill.
La declaración del modelo se contrastó con las acciones observadas y la ausencia de manifiestos; no se utilizó como única prueba.
La condición se describe con precisión como **sin los tres manifiestos de instrucciones, con el código y la documentación conservados**.

## Conclusiones de las tres comparaciones

- Las tres skills se seleccionaron y usaron en los chats del proyecto original; hubo un pedido natural que ejecutó limpieza seguida de mapa.
- Para Cusco, la condición con skills reprodujo una estimación local y la condición sin skills consultó una cifra publicada. Ambas dieron 18,5 % al redondear.
- Para gráfico y mapa, ambas condiciones ejecutaron los mismos programas con la misma base y `facpob07`. Se comprobaron tasas e imágenes idénticas.
- En estos dos casos no se observó una ventaja de exactitud o presentación atribuible a cargar los manifiestos. El código determinista y los datos disponibles explican la coincidencia.
- La prueba documenta descubrimiento y seguimiento de instrucciones frente a reutilización directa de código disponible. No demuestra que las skills sean imprescindibles para ejecutar esos scripts ni una incapacidad del modelo sin ellas.
- Se hizo una ejecución por caso y condición, con resultados previos y documentación disponibles. La instantánea de control fue posterior a las demostraciones y el formato de la auditoría del mapa varió. La comparación es descriptiva; no es una medida causal ni estadística de mejora o velocidad.

## Prueba adicional · Encadenamiento sin base limpia

Se preparó la copia independiente `enaho_sin_base` mediante `scripts/preparar_sin_base.py`, sin sobrescribir destinos existentes ni alterar el proyecto principal. Se conservaron los tres `SKILL.md`, sus scripts y referencias, las entradas públicas, las pruebas y las dependencias fijadas. Las carpetas `salidas/`, `figuras/` y `mapas/` estaban vacías; no se copiaron resultados ni documentos de evaluación. El README solo describía las entradas y el entorno. El CSV de referencia departamental se conservó como entrada de validación.

Antes del pedido al modelo se ejecutó directamente el programa de mapas: terminó con código 1 y el mensaje `Falta personas_2024.parquet; usar primero la skill limpiando-enaho`, sin crear resultados. Esto acredita la precondición y el rechazo del script; la selección y ejecución de las skills se comprobaron después con el modelo.

### Pedido y entorno

El pedido principal fue:

> Haz un mapa de la pobreza por departamento del Perú con la ENAHO 2024.

Se añadieron restricciones para trabajar solo en esa carpeta, conservar código e instrucciones, no tomar bases ni resultados de carpetas vecinas, no delegar y procesar los microdatos localmente sin mostrar filas individuales. También se pidió informar la existencia inicial de la base, las skills utilizadas, el orden de los scripts, el peso y la unión territorial. No se nombraron las skills ni se indicó al modelo que ejecutara primero la limpieza.

Se utilizó Codex CLI `0.166.0-alpha.5.1`, con `-m gpt-6.1-sol`, `model_reasoning_effort="xhigh"`, modo efímero y revisión automática de permisos. Se registra el parámetro de razonamiento de CLI explícitamente; esta ejecución no se mezcla con las seis comparaciones anteriores en Work, cuyo selector decía «Muy alto».

Se verificó por SHA-256 que ambos ZIP eran idénticos a las descargas públicas oficiales del INEI. Los microdatos se procesaron localmente y las salidas se limitaron a código, instrucciones, controles y resultados agregados. La comprobación de procedencia está en `referencias/procedencia_publica_2024.json`.

Hubo una incidencia del entorno: `uv` no pudo utilizar el intérprete al que apuntaba la copia de `.venv`. El modelo restauró las dependencias con `uv sync --frozen` y utilizó Python 3.13.9; el desarrollo original utilizó 3.13.5. No cambió `uv.lock`, las instrucciones ni el código. Por este motivo y por tratarse de otra interfaz, no se comparan tiempos con los chats anteriores.

### Acciones observadas

1. Leyó los `SKILL.md` de `mapeando-enaho` y `limpiando-enaho`, además del esquema y el código existente. Comprobó explícitamente que la base limpia no existía.
2. Tras resolver el entorno, ejecutó la suite existente: **22 pruebas aprobadas**.
3. Ejecutó, con salida 0, en este orden:

   ```powershell
   .\.tools\bin\uv.exe run --frozen --offline --cache-dir .uv-cache python .agents/skills/limpiando-enaho/scripts/limpiar.py --anio 2024
   # Después leyó salidas/validacion.txt y salidas/validacion_2024.json: OK.
   .\.tools\bin\uv.exe run --frozen --offline --cache-dir .uv-cache python .agents/skills/mapeando-enaho/scripts/mapear.py --anio 2024
   ```

   La limpieza informó **108 664 residentes habituales** y pobreza nacional de personas **27,52873 %**. El programa de mapas informó **25 territorios** y peso **`facpob07`**.
4. Añadió en la copia `scripts/verificar_mapa_2024.py`, lo ejecutó satisfactoriamente y guardó un informe de controles. Este archivo nuevo no sustituyó ni modificó los programas de las skills. Revisó también la imagen generada.

### Revisión independiente

- Los 23 archivos iniciales conservaron sus huellas, incluidos los manifiestos, scripts, entradas y `uv.lock`. La base del proyecto principal también permaneció intacta.
- La base creada desde los ZIP coincide por SHA-256 con la original: `2e2542a648df3de17c48538f20897a4ab258730fc015b6af585873562ed8c757`.
- Se comprobaron los mismos 25 códigos de dos caracteres en personas, CSV y GeoJSON; `departamento = ubigeo[:2]`, unión 1:1, 25 coincidencias, cero tasas faltantes y geometrías válidas.
- Se recalcularon las 25 tasas directamente con NumPy, sin las funciones de agregación del proyecto: coincidieron con el CSV. El cálculo fue `100 × Σ(facpob07 × indicador de pobreza 1 o 2) / Σ(facpob07)` en cada territorio.
- Lima `15` y Callao `07` tienen geometrías distintas y tasas separadas: **26,8887692770 %** y **33,7683435697 %**, respectivamente.
- El CSV es idéntico al del proyecto principal y el mapa tiene los mismos píxeles, tamaño de 2400 × 2000 y resolución nominal de 200 dpi. La imagen también se abrió para revisión visual.

El estado inicial, la secuencia de acciones y la comprobación se conservan en `referencias/encadenamiento_sin_base_2024.json`. El registro completo de herramientas permanece local en `.evaluacion-runs/`, excluido de Git.

Conclusión: se comprobó el encadenamiento condicional desde datos sin base limpia. Ante un pedido natural de mapa, el modelo seleccionó las instrucciones, generó y validó la base y después produjo el mapa, sin recibir una orden explícita de limpiar primero. Esta prueba funcional no mide una ventaja frente a una condición sin skills.
