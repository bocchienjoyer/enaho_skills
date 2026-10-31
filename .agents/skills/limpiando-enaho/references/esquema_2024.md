# Esquema y decisiones de ENAHO 2024

## Entradas y llaves

- Sumaria: seleccionar exactamente `sumaria-2024.dta` dentro de `966-Modulo34.zip`. El mismo ZIP incluye `sumaria-2024-12g.dta`; no elegir el primer archivo `.dta`.
- Miembros: seleccionar exactamente `enaho01-2024-200.dta` dentro de `966-Modulo02.zip`; también hay tablas auxiliares.
- Leer con `pandas.read_stata(convert_categoricals=False)`. Los códigos no deben convertirse a etiquetas.
- Normalizar nombres en minúscula; `aÑo` se convierte en `anio`.
- Hogar: `conglome` (6 caracteres), `vivienda` (3), `hogar` (2). Persona: agregar `codperso` (2).
- `ubigeo`: 6 caracteres; los primeros dos identifican departamento. Mantener texto y ceros en todas las llaves.
- No deduplicar silenciosamente ni completar una llave perdida: detenerse si las llaves faltan, tienen formato incorrecto o se repiten.

## Universo y variables

Residente habitual: `((p204 == 1) & (p205 == 2)) | ((p204 == 2) & (p206 == 1))`.
Los nulos en las preguntas de residencia pueden corresponder a saltos del cuestionario: no rellenarlos antes de evaluar el filtro.

| Variable | Significado / uso |
|---|---|
| `p203` | Parentesco; 1 identifica al jefe o jefa del hogar |
| `p204` | Miembro del hogar: 1 sí, 2 no |
| `p205` | Ausente del hogar 30 días o más: 1 sí, 2 no |
| `p206` | Presente en el hogar 30 días o más: 1 sí, 2 no |
| `p207` | Sexo: 1 hombre, 2 mujer |
| `p208a` | Edad en años cumplidos; cero es una edad válida |
| `pobreza` | 1 pobre extremo, 2 pobre no extremo, 3 no pobre |
| `pobre`, `pobre_extremo` | Indicadores booleanos: códigos 1 o 2, y código 1, respectivamente |
| `urbano` | `estrato <= 5`; los estratos 6–8 corresponden al área rural |
| `facpob07` | Factor de expansión de personas; único peso para las tasas sobre la base de personas |
| `factor07`, `mieperho` | Factor del hogar y miembros: su producto es el peso poblacional usado con sumaria |
| `departamento` | Código de dos caracteres; Lima `15` y Callao `07` separados |

La base final conserva `facpob07` y las variables anteriores de personas, geografía y pobreza.
`factor07` y `mieperho` se usan en la validación de sumaria y no se incluyen como pesos alternativos en la base de personas.
Las tasas se calculan como `100 × suma(indicador × peso) / suma(peso)`, con pesos positivos y finitos y sin datos faltantes en pobreza.
Son estimaciones puntuales; este pipeline no calcula errores estándar ni intervalos de confianza del diseño muestral.

## Controles y referencias

Para 2024: 33 691 hogares, 117 721 miembros registrados y 108 664 residentes habituales.
La unión se hace de personas a hogares con `how="left"`, `validate="m:1"` y comprobación de correspondencia completa.
`ubigeo`, `dominio` y `estrato` deben coincidir entre ambos módulos.
Los 25 códigos departamentales deben estar presentes en la base resultante.

La referencia nacional de la guía es 27,6 % de pobreza monetaria y 5,5 % de extrema.
Se admite una diferencia estrictamente menor que 0,1 puntos porcentuales en cada estimación nacional.
Los archivos descargados producen aproximadamente:

| Universo y peso | Pobreza | Extrema | Urbano / rural |
|---|---:|---:|---:|
| Sumaria, `factor07 × mieperho` | 27,57947 % | 5,50453 % | 24,80699 % / 39,30279 % |
| Residentes, `facpob07` | 27,52873 % | 5,49978 % | 24,73524 % / 39,44168 % |

La tabla del curso para Cusco (18,5 %), urbano/rural (24,8 %/39,3 %) y departamentos procede de sumaria.
Al evaluar los gráficos y el mapa de personas, reportar cualquier diferencia y su universo; no modificar los pesos para reproducir esos redondeos.
El conteo de residentes por hogar no coincide siempre con `mieperho`; no imponer esa igualdad ni usarla para cambiar el filtro.

## Salidas y fallo

- `salidas/personas_2024.parquet`: una fila por residente; orden estable por llave de persona.
- `salidas/validacion.txt`: controles, estimaciones y explicación de universos.
- `salidas/validacion_2024.json`: estado, controles, fuentes y SHA-256 de la base para comprobar que corresponde a esa validación.

Un fallo deja el informe en estado ERROR y el proceso termina con código distinto de cero.
Si existe una base de una ejecución anterior, el informe ERROR impide considerarla validada.

Fuentes: [consigna y referencias de la sesión](https://github.com/d2cml-ai/Data-Science-Python/tree/main/sessions/16-skills-enaho), etiquetas de los archivos Stata descargados y [lectura Stata en pandas](https://pandas.pydata.org/docs/reference/api/pandas.read_stata.html).
