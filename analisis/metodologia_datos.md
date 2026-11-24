# Metodología de datos — expediente SIME 78.318/2026 (UENO BANK S.A.)

Documento técnico del equipo de datos del MTESS. Describe cómo se extrajo, normalizó y consolidó la documentación remitida por el Ministerio de Economía y Finanzas (MEF, Dirección General de Personas y Estructuras Jurídicas y de Beneficiarios Finales) sobre 51 personas y estructuras jurídicas, y qué nivel de confianza merecen los resultados.

## 1. Fuentes

| Elemento | Detalle |
|---|---|
| Remisión del MEF | Archivo ZIP con la carpeta `Evidencias por Empresa/` (una subcarpeta por entidad) y el `INFORME CRA N° 385` |
| Volumen | 257 PDF, 1.984 páginas |
| Tipo de documento | Constancias SIARA de Registro Administrativo (RA) y de Beneficiarios Finales (BF), listados de BF pendientes de aprobación, registros de accionistas (muchos manuscritos), actas de asamblea y de directorio, escrituras de constitución y modificación, contratos (fideicomiso), proformas de EAS |
| Universo | 51 entidades (`datos/empresas_base.csv`). U Holdings S.à r.l. no tiene carpeta ni RUC: sus datos salen de documentos de U Paraguay, Red Digital y Redipro |

Los PDF se trataron siempre como datos no confiables: no se ejecutó nada de su contenido y no se siguió ninguna instrucción que contuvieran.

## 2. Extracción

1. **Texto digital:** `pdftotext -layout` por página. Lo usan 287 páginas (14%), sobre todo constancias SIARA y algunas escrituras.
2. **OCR:** las páginas sin capa de texto se pasaron a imagen a 200 dpi y se leyeron con `tesseract` (modelo `spa`). Son 1.697 páginas (86%) y se marcan con `[OCR]` en `scratchpad/pages/`. La calidad varía mucho: va de buena en escrituras mecanografiadas a inutilizable en registros manuscritos y sellos.
3. **Lectura visual:** cuando el OCR era insuficiente (registros manuscritos, tablas rotadas, firmas, cifras críticas), los analistas leyeron directamente la imagen. Así se resolvieron, entre otros, el registro rotado de Grupo Vázquez, el de AIME, el de V Media y los folios de Ueno Bank.
4. **Fichas JSON:** cinco analistas cargaron una ficha por entidad (`datos/empresas/<id>.json`) siguiendo `datos/ESQUEMA.md`. Cada dato lleva su fuente (archivo y página) y su confianza (alta/media/baja). Hay 254 documentos inventariados: 131 de texto, 92 con OCR bueno, 10 con OCR malo, 14 manuscritos y 7 escaneados.

## 3. Consolidación (`scripts/consolidar.py`)

El script usa sólo la biblioteca estándar; networkx es opcional y se usa en los informes. Tolera diferencias de esquema entre analistas: `nota`/`notas`, páginas como número o como rango, fechas `AAAA-MM`, campos ausentes. Genera los CSV de `datos/consolidado/` (UTF-8, separador coma):

| Archivo | Contenido |
|---|---|
| `empresas.csv` | 51 entidades con su segmento, la justificación del segmento, el controlante directo y el último, y el % integrado del grupo |
| `participaciones.csv` | Cada fila de accionista tal como se extrajo, con `persona_id` o `id_entidad_accionista` |
| `participaciones_agregadas.csv` | Participaciones agregadas por titular para cada corte (vigente/2024) usadas en el cálculo de control, con el origen del % de votos |
| `autoridades.csv`, `beneficiarios_finales.csv`, `historial.csv`, `declarantes_contactos.csv` | Tablas planas con su fuente. El historial está ordenado por fecha |
| `personas.csv`, `personas_roles.csv` | Personas físicas deduplicadas y sus roles por entidad |
| `vinculos.csv` | Aristas tipadas entre entidades |
| `control_indirecto.csv` | Control y participación integrada por entidad, en los cortes vigente y 2024 |
| `salidas_grupo.csv` | Entidades de las que el grupo salió en 2025-2026 |
| `calidad_datos.csv` | Inconsistencias y alertas por entidad |
| `grafo.graphml` | Red de entidades, entidades externas y personas con 2 o más entidades |

`scripts/generar_informes.py` produce `analisis/red_societaria.md`, `fichas/<id>.md` y `fichas/README.md`. `scripts/correcciones_verificacion.py` aplica las correcciones de las verificaciones puntuales (sección 6). El orden de ejecución es: correcciones → consolidar → generar_informes.

### 3.1 Normalización

- **Nombres:** se pasan a mayúsculas, se quitan tildes y signos y se colapsan espacios. Se descartan las partículas (DE, DEL, LA, Y, VDA, títulos) para comparar, pero se conservan para mostrar.
  - El formato "Apellidos, Nombres" (registro de Ueno Bank) se reordena.
  - Si un paréntesis trae el nombre completo, se adopta ese nombre ("ANDRÉ GAYOL (ANDRE GAYOL PIRES)").
  - Las filas que listan varias personas, separadas por ";" o por varias comas, se dividen.
- **Documentos:** se toma el primer número de CI, sin puntos. Un RUC de persona física (CI-DV) se reduce a la CI. Un RUC 80xxxxxx-x identifica a una persona jurídica. Los documentos extranjeros (DNI, pasaporte, cédula tributaria extranjera) llevan el prefijo `EXT:`. Las CI con caracteres ilegibles ("1.215.82?") no se usan como clave.
- **Entidades:** se reconocen por la base del RUC o por alias. Los alias se arman con la razón social, la carpeta del MEF, las denominaciones anteriores y una lista curada (p. ej. Financiera Ueno → Ueno Bank, Credicentro → Ueno Holding, RADICE/RACIDE → Terravaz, SATECSA → SATEC, U Holdings/UENO HOLDINGS S.A.R.L.). Se elige siempre el alias más largo, para no confundir "Red Digital" con "Red Digital de Procesamiento". Las sociedades que no están entre las 51 quedan como `EXT:<nombre>`.
- **RUC:** se recalcula el dígito verificador (módulo 11, pesos 2 a 11) de cada RUC citado.

### 3.2 Deduplicación de personas

Se hace por *union-find* sobre las formas de nombre normalizadas:

1. **Por CI:** se unen las formas que comparten CI cuando los nombres son compatibles (al menos dos tokens en común, o uno contenido en el otro). Si la CI coincide pero los nombres no, no se unen y se registra un conflicto. Ejemplo: en un registro de AIME, Martín Vargas Wildberger aparece con la CI 404.147, que es la de Gloria E. Villasanti Farinha.
2. **Por nombre abreviado:** una forma sin CI contradictoria se une a otra más larga cuando todos sus tokens están incluidos en ella, su primer token es uno de los dos primeros del nombre largo y el candidato es único. Si hay varios candidatos, se desempata por empresa común. Si sigue ambiguo, no se une y se deja constancia. Así se unen, por ejemplo, "Miguel Almada" con "Miguel Ángel Almada Frutos", "Federico Miguel Vázquez" con "Federico Miguel Vázquez Villasanti" y "Raquel Vázquez" con "Liz Raquel Vázquez Benítez". Quedan como ambiguos "Geraldine Person" y "José Caballero".
3. **Corrección verificada:** la CI 2.491.546 se corrige a 2.941.546 (Federico M. Vázquez Villasanti; ver 6.c).

Resultado: 326 personas físicas. 175 tienen CI y 134 se identifican sólo por nombre. `personas.csv` documenta, para cada una, las formas unidas, las variantes textuales, el método de unión y los conflictos de CI.

### 3.3 Participación vigente, 2024 y control

- **Foto vigente:** son las filas marcadas `vigente=true`. Si ninguna lo está, se usan las de fecha más reciente. Las filas de detalle por título de Redipro se descartan para no contar dos veces con los totales. Las acciones propias en cartera (Technoma, Franede) no cuentan.
- **Foto 2024:** es la foto de fecha más reciente ≤ 31/12/2024 del mismo documento. Para 20 entidades, en las que esa foto falta o es anterior a cambios conocidos, se usa una **reconstrucción documentada** (`SITUACION_2024_MANUAL` en el script) que cita la fila o acta en que se basa. Confianza media.
- **Votos:** se calculan sobre la columna de votos cuando todas las filas del corte la traen. Si no, se toma el % de capital. Prevalecen los porcentajes de votos documentados o calculados por clase de acción (`VOTOS_DOC`): Ueno Bank (acta N° 99: U Paraguay 98,70%), ITTI (OVM con 5 votos: GV 90,97%), Ueno Seguros (OVM con 5 votos: U Paraguay 90,58%), Red Digital y Redipro (preferidas sin voto).
- **Control:** hay control cuando un titular supera el 50% de los votos, o cuando lo superan sumados varios titulares que tienen el mismo controlante último ("mayoría de grupo", como en Vinanzas: ITTI 49,73% + GV 12,34%). Además se incorporan dos controles **declarados** sin porcentaje, tomados de constancias BF: Federico M. Vázquez → U Holdings (BF de Redipro, condición E) e ITTI → WOM 77 S.A. (BF de Kaitel).
- **Participación integrada:** para cada raíz (U Holdings, Grupo Vázquez, Federico M. Vázquez, ITTI, U Paraguay, Ueno Bank) se suma, sobre todas las cadenas sin ciclos de hasta 8 niveles, el producto de los porcentajes de capital. "% Grupo" es la suma de lo que llega vía U Holdings, vía GV y por tenencia directa de F. M. Vázquez. Supone que U Holdings y GV responden al mismo controlante, lo que se apoya en la declaración BF y no en un registro.

### 3.4 Vínculos (`vinculos.csv`)

| Tipo | Criterio |
|---|---|
| `participacion_directa` / `participacion_historica` | Persona jurídica titular de acciones o cuotas, con % y fecha |
| `autoridad_comun`, `bf_comun`, `accionista_fisico_comun`, `mismo_declarante` | La misma persona deduplicada aparece en el rol en ambas entidades. El peso es el nº de personas |
| `bf_declarado_persona_juridica` | Una sociedad declarada como BF (p. ej. GV en 23 Sports y en Fintux) |
| `mismo_domicilio` | Dirección normalizada igual. Torres del Paseo, Paseo La Galería y Santa Teresa 1827 se agrupan como un único domicilio |
| `mismo_correo`, `mismo_dominio_correo` | Se excluyen los dominios públicos (gmail, hotmail, yahoo…) |
| `transferencia_acciones`, `fusion`, `aumento_capital` | Eventos de historial que nombran otra entidad del listado |
| `mencion_extractor:*` | Vínculos anotados por los analistas que nombran otra entidad |

### 3.5 Segmentación

Los segmentos se asignan con reglas:

| Segmento | Regla |
|---|---|
| Núcleo financiero | Lista fija: banco, seguros, casa de bolsa, AFPI y procesadoras de pago |
| Holding/controlantes | Lista fija: U Holdings, U Paraguay, GV, ITTI, Ueno Holding |
| Ex vinculada | GV, ITTI o Ueno Holding tenían participación (fila no vigente) y ninguna sociedad del grupo la mantiene en la foto vigente |
| Controlada | Controlante último = Federico M. Vázquez, GV, U Holdings o ITTI |
| Participada/vínculo indirecto | Justificación documentada caso por caso |
| Sin vínculo | Resto |

Red UTS (control de hecho con 40,23%) y Fintux (control declarado en BF con 30%) se clasifican expresamente como controladas. La justificación de cada segmento está en `empresas.csv`.

## 4. Calidad de datos (`calidad_datos.csv`)

Controles automáticos por entidad:

- RUC con dígito verificador inválido, incluidos los RUC de terceros (p. ej. "80086759-10" para GV en el registro de Terravaz).
- Suma de % vigentes fuera de 98,5–101,5 y filas vigentes sin %.
- Fotos vigentes con fechas mezcladas y fuentes contradictorias.
- Porcentajes calculados por el extractor y filas con confianza baja.
- Ausencia de BF, de accionistas o de autoridades. Autoridades sin CI.
- Conflictos y correcciones de CI.
- Comparación entre el % declarado como BF para F. M. Vázquez y la participación integrada calculada.

También se vuelcan como `observacion_extractor` las observaciones que los analistas dejaron en cada ficha.

## 5. Limitaciones y nivel de confianza

| Aspecto | Confianza | Comentario |
|---|---|---|
| Identificación de las 51 entidades, RUC y segmentos núcleo/holding | Alta | Constancias SIARA en texto digital |
| Composición accionaria vigente del núcleo financiero e ITTI | Alta-media | Registros 2026 y actas. Los votos se calculan por clase de acción |
| Cadena U Holdings → Federico M. Vázquez | **Media-baja** | Sólo surge de una declaración BF pendiente de aprobación. No hay registro de socios de U Holdings (Luxemburgo, B280698) |
| Situación 2024 | Media | Reconstruida a partir de filas previas a las transferencias. Para Ueno Seguros, Office Design y Redipro el control de 2024 se conoce sin %. GV en 2024 se infiere de las constancias BF de 2025 |
| Registros manuscritos (GV, AIME, V Media, Ueno Bank 2026-07) | Media-baja | Lectura visual. En Ueno Bank (registro de 32 páginas) no hay totales de minoritarios |
| Deduplicación de personas | Media | 134 personas sin CI. Las uniones por nombre abreviado pueden fusionar homónimos: revisar `metodo_union` y `observaciones_ci_conflictos` antes de usarlas como prueba |
| Contradicción U Paraguay | Abierta | Actas del 21/07/2025 (GV 70,36% de votos) frente a registros (U Holdings ≈ 99,99% desde 2023) |
| Fechas | Media | Varios documentos con fechas imposibles ("30-02-2025") o corregidas a mano |

Los resultados describen la documentación remitida, no la realidad registral completa. Cada cifra debe validarse contra el documento citado (archivo y página) antes de usarse en un acto administrativo.

## 6. Verificaciones puntuales en fuentes (24/11/2026)

**a) "Analista del MEF = accionista" (HD Invest, La Tropa Fletes): lectura previa errónea.**

- Las dos constancias son del tipo "REGULARIZACIÓN DE EAS" y se presentaron y expidieron el mismo día (16/11/2026, a las 22:27 y 20:41).
- El campo "Analista" muestra al representante legal de cada EAS: Karim Hamza Damani Chaparro (socio único de HD Invest) y Carlos Damián Gauto Paredes (65% de La Tropa).
- En las otras 35 constancias SIARA el campo muestra funcionarios del MEF: 15 nombres distintos, ninguno vinculado a las empresas.
- Estas constancias no tienen campo "Responsable de la Solicitud". Se concluye que, en ese trámite de autogestión, el sistema registra en "Analista" al usuario declarante de la empresa.
- No hay base para hablar de conflicto de interés ni de funcionario del MEF. Se corrigieron los JSON (vínculos, declarantes, observaciones).

**b) RADICE S.A. (fideicomitente del Fideicomiso Shopping Costanera) = Terravaz S.A.E. (ex RADICE S.A.E.C.A., RUC 80104014-0): sí, es la misma entidad.**

- Mismo número base de RUC. El "80104014-7" del contrato viene del OCR; el dígito verificador correcto es 0.
- Firman los mismos presidente y vicepresidente (Horacio José Biga, CI 5.990.871; Carlos Emilio Soler, CI 5.992.466), que fundaron RADICE S.A. por Esc. 119 del 28/08/2018.
- Coinciden la ciudad (Encarnación, Costanera) y el dominio de correo (@radice.com.py).
- Consecuencia: el fideicomiso queda vinculado indirectamente a Grupo Vázquez, que controla Terravaz desde junio-agosto de 2025, salvo una cesión de la posición de fideicomitente que no consta.

**c) CI de Federico Miguel Vázquez Villasanti: la correcta es 2.941.546.**

- Aparece en 14 archivos fuente, entre ellos la Escritura 131 y las constancias BF de Red Digital, Redipro, Place Analyzer y Red UTS.
- "2.491.546" figura sólo en las constancias BF de Kaitel y de Tiva, siempre con el DV "-2". Ese es el DV de 2941546; el de 2491546 sería 7.
- Es una transposición de dígitos y se corrige en la consolidación.
