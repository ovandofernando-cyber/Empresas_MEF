# Empresas MEF: composición societaria de las entidades vinculadas a Ueno Bank

Sistematización de la documentación remitida por el Ministerio de Economía y Finanzas (Nota MEF N° 1505, Memorándum DGPEJBF N° 175/2026, Informe CRA N° 385/2026) al Ministerio de Trabajo, Empleo y Seguridad Social, en respuesta a la Nota MTESS N° 656/2026, en el marco del procedimiento de resolución de **UENO BANK S.A.** (Exp. SIME N° 78.318/2026).

Objetivo: identificar con precisión a los empleadores, su conformación societaria y sus vínculos (posible conjunto o grupo económico) para resguardar los derechos laborales de los trabajadores afectados.

## Hallazgos principales

- **Hay un conjunto económico documentado.** Federico Miguel Vázquez Villasanti (CI 2.941.546) tiene ≈76 % del capital y ≈94 % de los votos de Grupo Vázquez S.A.E. y figura como beneficiario final por cadena en varias constancias.
- **Cadena de control de Ueno Bank (dato vigente):** U Holdings S.à r.l. (Luxemburgo, sin RUC; su composición no consta) → U Paraguay S.A. (97,99 %) → Ueno Bank (93,08 % del capital y 98,70 % de los votos). En marzo de 2024 el controlante directo era Grupo Vázquez.
- **Rama no financiera:** Grupo Vázquez → ITTI S.A.E.C.A. (77,46 %) → turismo, logística, tecnología y tercerización de personal (Kaitel, vía WOM77).
- **Reestructuraciones 2025-2026:** absorción de Ueno Holding por Grupo Vázquez (16/07/2025), siete sociedades vendidas a personas del entorno del grupo, aporte de ≈Gs. 877.000 M del banco en acciones preferidas de REDIPRO/REDISA y transferencias circulares en septiembre-octubre de 2026.
- **Clasificación laboral (matriz):** 25 entidades en nivel N1 (control común), 11 en N2, 7 en N3 y 8 en N4 (sin vínculo documentado). El plano laboral (quién empleaba a quién) todavía requiere prueba del IPS, del MTESS y del interventor.

Las cifras provienen de declaraciones juradas, registros manuscritos y OCR; ver advertencias en `analisis/metodologia_datos.md` y `datos/consolidado/calidad_datos.csv`.

## Estructura

| Carpeta / archivo | Contenido |
|---|---|
| `analisis/analisis_laboral.md` | Matriz laboral aplicada a las 51 entidades, perímetro del grupo, casos prioritarios, recomendaciones y modelo de requerimiento del MTESS |
| `analisis/marco_juridico_laboral.md` | Marco jurídico paraguayo (Código del Trabajo, Ley 2334/03, Ley 6446/19, IPS, inoponibilidad) y metodología de indicadores |
| `analisis/analisis_economico.md` | Estructura y lógica económica del grupo, cronología de reestructuraciones, señales de alerta e implicancias para los trabajadores |
| `analisis/red_societaria.md` | Diagramas de control (Mermaid), personas recurrentes, centralidad |
| `analisis/metodologia_datos.md` | Cómo se extrajo y normalizó la información, limitaciones |
| `fichas/` | Una ficha legible por entidad (`fichas/README.md` es el índice) |
| `datos/empresas_base.csv` | Las 51 entidades del Informe CRA 385/2026 con su RUC y carpeta |
| `datos/empresas/<id>.json` | Datos estructurados por entidad con fuente (archivo y página) de cada dato; esquema en `datos/ESQUEMA.md` |
| `datos/consolidado/` | Tablas: empresas, participaciones, control indirecto, autoridades, beneficiarios finales, personas, roles, vínculos, historial, declarantes, salidas del grupo, calidad de datos, matriz laboral, grafo (`grafo.graphml`) |
| `fuentes/inventario_documentos.csv` | Los 257 PDF recibidos, páginas y proporción de OCR |
| `fuentes/texto/` | Texto completo de cada documento (digital u OCR) para búsqueda |
| `scripts/` | Código que regenera el consolidado y los informes (`python3 scripts/correcciones_verificacion.py && python3 scripts/consolidar.py && python3 scripts/generar_informes.py`) |

Los PDF originales (≈400 MB) no se versionan; están en el zip del expediente.

## Aviso

Este material es un insumo técnico de trabajo, no un dictamen jurídico. Los datos personales provienen de registros administrativos remitidos al MTESS y deben tratarse con la reserva correspondiente.
