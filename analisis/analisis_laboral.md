# Análisis laboral de las 51 entidades
## Caso UENO BANK S.A. (RUC 80026157-7) – Expediente SIME 78.318/2026

**Destinatario:** Ministerio de Trabajo, Empleo y Seguridad Social (MTESS) – Viceministerio de Trabajo, Dirección de Trabajo y Dirección General de Inspección y Fiscalización.
**Fecha:** 24 de noviembre de 2026.
**Fase:** 2. Aplicación de la matriz de `analisis/marco_juridico_laboral.md` (§7) a las 51 entidades informadas por el MEF (Nota MEF 1505, Informe CRA 385/2026).
**Insumos:** fichas `datos/empresas/<id>.json` (extracción de la carpeta de cada entidad remitida por el MEF), tablas `datos/consolidado/` (control indirecto, salidas del grupo, vínculos), `analisis/analisis_economico.md` y `analisis/marco_juridico_laboral.md`.
**Producto anexo:** `datos/consolidado/matriz_laboral.csv` (misma matriz, en formato de datos).
**Carácter:** documento técnico de trabajo. **No es un dictamen vinculante.** Las calificaciones de responsabilidad (empleador real, solidaridad, inoponibilidad) **corresponden a la justicia**; aquí se ordenan indicios y se proponen actuaciones administrativas.

### Cómo leer este documento

| Marca | Significado |
|---|---|
| **[MEF: carpeta › archivo]** | Hecho que consta en un documento remitido por el MEF. Se cita la carpeta de la entidad y el archivo. |
| **[PÚBLICO]** | Dato de prensa o publicación pública (ver `analisis_economico.md` §6, con URL). **No verificado** con documentos oficiales. |
| **[INFERENCIA]** | Lectura del analista. Es hipótesis de trabajo, **no hecho probado**. No debe transcribirse en un acta como hecho constatado. |
| **(h)** después de una etiqueta IMP | Hipótesis de imputación: hay base societaria o pública, **pero falta la prueba laboral** (planillas, contratos, inspección) que exige la matriz. |

---

## Índice

1. [Resumen ejecutivo](#1-resumen-ejecutivo)
2. [Ajustes metodológicos al aplicar la matriz](#2-ajustes-metodológicos-al-aplicar-la-matriz)
3. [Matriz completa de las 51 entidades](#3-matriz-completa-de-las-51-entidades)
4. [Fichas por entidad, agrupadas por nivel](#4-fichas-por-entidad-agrupadas-por-nivel)
5. [Conclusiones: existencia y perímetro del conjunto económico](#5-conclusiones-existencia-y-perímetro-del-conjunto-económico)
6. [Casos prioritarios](#6-casos-prioritarios)
7. [Recomendaciones concretas al MTESS](#7-recomendaciones-concretas-al-mtess)
8. [Modelo de requerimiento de información](#8-modelo-de-requerimiento-de-información)
9. [Limitaciones](#9-limitaciones)

---

## 1. Resumen ejecutivo

1. **Existe un conjunto económico bajo control común, documentado en los registros del MEF.** 25 de las 51 entidades (nivel **N1**) están bajo control directo o indirecto de **Grupo Vázquez S.A.E.** y, en último término, de **Federico Miguel Vázquez Villasanti** (CI 2.941.546). Este figura como **beneficiario final declarado** en REDIPRO, REDISA, Kaitel, Tiva, Place Analyzer y Red UTS [MEF], y controla ≈94 % de los votos de GV [MEF: GRUPO VAZQUEZ SAE › Libro de registro de accionistas.pdf]. La cadena es GV → (U Holdings S.à r.l.) → U Paraguay → **Ueno Bank**. En paralelo, GV → ITTI → empresas de tecnología, turismo, logística y **Kaitel**.
2. **11 entidades (N2)** tienen vínculo relevante sin control vigente acreditado. Seis de ellas **salieron del grupo en 2025–2026** hacia personas del entorno: MOWI, Grupo M, Grupo Hendy, Franede, TUIU y V Media. Una séptima salida, Office Design, queda en N3 [MEF; `salidas_grupo.csv`]. **7 entidades (N3)** tienen vínculo débil y **8 (N4)** no tienen vínculo societario documentado. Estas últimas son, según la prensa, **deudoras del banco** y no sociedades del grupo [PÚBLICO].
3. **Pertenecer al grupo no basta para extender la responsabilidad laboral** (marco §3.1). La matriz muestra que **el plano societario está bien documentado (PS alto) y el plano laboral está casi vacío (PL ≈ 0, "s/d")**. Por eso casi todas las etiquetas son **hipótesis (h)**. La tarea inmediata del MTESS es **producir la prueba laboral**: planillas IPS y MTESS, contratos intragrupo, inspecciones.
4. **Vías más sólidas por caso:**
   - **Kaitel S.R.L.** (≈1.200 trabajadores [PÚBLICO]): outsourcing de personal con capital de **Gs. 50 millones** [MEF], gerenciada por un **director de Ueno Bank** (Impagliatelli) y por el **síndico de Ueno Bank** (Almada) [MEF]. Es el caso típico de **intermediación (CT art. 25)** y de contratista sin autonomía (art. 26 a contrario).
   - **ITTI** (≈1.600 [PÚBLICO]): la hipótesis es **empleador real o coempleador** (arts. 22 y 24) del personal asignado al banco. ITTI es además controlante indirecta de Kaitel.
   - **REDIPRO, REDISA y U Paraguay**: el banco aportó **≈Gs. 877.000 millones en acciones preferidas sin voto**, y un mes antes de la resolución salieron del banco **263.339 preferidas de REDIPRO** hacia U Paraguay, en parte por una **cadena circular de un día** [MEF]. Son el principal objetivo de **preservación patrimonial** (vía de inoponibilidad o fraude, CC art. 372).
   - **Grupo Vázquez**: es **sucesora universal de Ueno Holding S.A.E.C.A.** por fusión [MEF: Escritura 131, 16/07/2025]. Ese es un hecho documentado que traslada a GV las obligaciones laborales de Ueno Holding.
5. **Urgencias:** no se puede embargar a Ueno Bank mientras dure la resolución (Ley 2334/03 art. 25). La prescripción laboral es breve. Varias sociedades del entorno cambian de manos o tienen cautelas penales. El MTESS debe (i) requerir información hoy, (ii) inspeccionar Kaitel, ITTI, REDISA/REDIPRO e IDL, (iii) convocar a mediación a la cadena Kaitel–WOM77–ITTI–GV junto con el interventor, y (iv) orientar a los trabajadores para que pidan **cautelas laborales** contra las sociedades con patrimonio.

---

## 2. Ajustes metodológicos al aplicar la matriz

Al aplicar la matriz del marco (§7) a datos reales se hicieron estos ajustes, que se explicitan para que la puntuación sea replicable:

1. **S1 redefinido según la estructura hallada.** El marco definía S1 como participación directa de Ueno Bank, Ueno Holding o Ueno Holdings S.à r.l. Los datos muestran que la cúspide es **Grupo Vázquez**, con holdings intermedios (U Paraguay, ITTI, U Holdings, WOM77). S1 se puntúa entonces como **participación directa de cualquier sociedad del núcleo de control** (GV, U Holdings, U Paraguay, ITTI, Ueno Bank, Ueno Holding, WOM77 y sus controladas). Para las controlantes (GV, U Holdings, U Paraguay) S1 = 3 refleja su posición de controlante.
2. **Sociedades salidas del grupo (ex-grupo).** Rige la regla del marco §7.5.1 (fecha de los hechos laborales). S1 = **2** si la salida ocurrió dentro de los 12 meses previos a la resolución (02/11/2026), y S1 = **1** si ocurrió entre 12 y 24 meses antes. El **nivel N1 se reserva al control vigente**. Por eso V Media (salida 23/03/2026) queda en **N2 por decisión expresa**, aunque la regla automática le daría N1.
3. **Fintux E.A.S.** queda en **N2 por decisión expresa**: ITTI tiene solo el 30 %, y la constancia de beneficiarios finales declara a "Grupo Vázquez S.A.E." (una persona jurídica) como BF. Eso es un indicio de control, no una prueba.
4. **L5 no duplica S5.** El uso de correos de otra sociedad del grupo por los **declarantes** SIARA se computa en S5. L5 se reserva a indicios de **operación** común: directivos que trabajan con correo de otra sociedad, o función legal prestada por otra sociedad.
5. **Datos de prensa.** Valen como máximo **1** (indicio) en L y F. Los hechos documentados en el MEF pueden valer 2 o 3.
6. **"s/d" (sin datos)** no suma ni resta. La columna `s/d` cuenta los indicadores sin datos. Un número alto indica **falta de prueba, no ausencia de vínculo**.
7. **Ueno Bank** se puntúa como entidad de referencia (empleador formal en resolución), con la etiqueta **REF**.

**Escala** (marco §7.2): 0 sin evidencia; 1 indicio débil; 2 indicio relevante (documental); 3 prueba fuerte. **Niveles:** N1 control común (S1 o S2 ≥ 2, y además S3 o S4 ≥ 2); N2 vinculación relevante (PS ≥ 6 o algún S = 3); N3 débil (PS 1–5); N4 sin vínculo acreditado. **Etiquetas:** IMP-A empleador real o coempleador; IMP-B intermediación o contratista no autónomo; IMP-C sustitución o sucesión; IMP-D inoponibilidad por fraude; IMP-E seguridad social (patrón principal); IMP-0 sin base de imputación por ahora.

**Recordatorio de indicadores.** S1 participación directa del núcleo; S2 control indirecto; S3 beneficiario final común; S4 directores o representantes comunes; S5 mismo declarante o dominio; S6 mismo domicilio; S7 marca común. L1 servicios intragrupo; L2 dependencia económica; L3 trabajadores compartidos; L4 dirección o poder disciplinario común; L5 infraestructura común; L6 discordancia de registros IPS/MTESS; L7 pagos cruzados; L8 contratista sin autonomía. F1 caja común o financiamiento intragrupo; F2 movimientos previos a la resolución; F3 cambios societarios recientes o irregulares; F4 subcapitalización o sociedad "satélite".

---

## 3. Matriz completa de las 51 entidades

PS = puntaje societario (máx. 21); PL = laboral (máx. 24); PF = fraude (máx. 12); s/d = sin datos. La fuente de cada puntaje está en las fichas (§4).

| # | Entidad | S1 | S2 | S3 | S4 | S5 | S6 | S7 | **PS** | L1 | L2 | L3 | L4 | L5 | L6 | L7 | L8 | **PL** | F1 | F2 | F3 | F4 | **PF** | s/d | **Nivel** | **Etiqueta** |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | 23 Sports Marketing S.A. | 3 | 3 | 1 | 2 | 1 | 0 | 1 | **11** | s/d | s/d | s/d | s/d | s/d | s/d | s/d | s/d | **0** | s/d | s/d | 1 | s/d | **1** | 11 | **N1** | IMP-0 |
| 2 | AIME S.A. Corredores de Seguros | 0 | 0 | 1 | 1 | 3 | 3 | 0 | **8** | s/d | s/d | s/d | s/d | s/d | s/d | s/d | s/d | **0** | 1 | s/d | s/d | s/d | **1** | 11 | **N2** | IMP-0 |
| 3 | BIC S.A. (Buró de Información Comercial) | 1 | 1 | s/d | 0 | 0 | 0 | 0 | **2** | s/d | s/d | s/d | s/d | s/d | s/d | s/d | s/d | **0** | s/d | s/d | s/d | s/d | **0** | 13 | **N3** | IMP-0 |
| 4 | CBS S.A. | 0 | 0 | 0 | 1 | 0 | 0 | 0 | **1** | s/d | s/d | s/d | s/d | s/d | s/d | s/d | s/d | **0** | s/d | s/d | s/d | s/d | **0** | 12 | **N3** | IMP-0 |
| 5 | Compañía de Desarrollo Turístico S.R.L. (COMDETUR) | 3 | 3 | s/d | 3 | 2 | 1 | 0 | **12** | s/d | s/d | s/d | s/d | s/d | s/d | s/d | s/d | **0** | s/d | s/d | s/d | s/d | **0** | 13 | **N1** | IMP-0 |
| 6 | Condominio Estancia Don Miguel | 0 | 0 | 0 | 0 | 0 | 0 | 0 | **0** | s/d | s/d | s/d | s/d | s/d | s/d | s/d | s/d | **0** | s/d | s/d | s/d | s/d | **0** | 12 | **N4** | IMP-0 |
| 7 | Discover Paraguay S.A. | 3 | 3 | s/d | 3 | 1 | 1 | 0 | **11** | s/d | s/d | s/d | s/d | s/d | s/d | s/d | s/d | **0** | s/d | s/d | s/d | s/d | **0** | 13 | **N1** | IMP-0 |
| 8 | Factopar S.A. | 0 | 0 | 0 | 0 | 0 | 0 | 0 | **0** | s/d | s/d | s/d | s/d | s/d | s/d | s/d | s/d | **0** | 1 | s/d | s/d | s/d | **1** | 11 | **N4** | IMP-0 |
| 9 | Fideicomiso Shopping Costanera | 0 | 1 | 0 | 0 | 0 | 0 | 0 | **1** | s/d | s/d | s/d | s/d | s/d | s/d | s/d | s/d | **0** | s/d | s/d | s/d | s/d | **0** | 12 | **N3** | IMP-0 |
| 10 | Fintux E.A.S. | 2 | 2 | 2 | 0 | 0 | 0 | 0 | **6** | s/d | s/d | s/d | s/d | s/d | s/d | s/d | s/d | **0** | s/d | s/d | s/d | s/d | **0** | 12 | **N2** | IMP-0 |
| 11 | Franede S.A. | 1 | 0 | 1 | 1 | 3 | 1 | 0 | **7** | s/d | s/d | s/d | s/d | s/d | s/d | s/d | s/d | **0** | 1 | 2 | 2 | s/d | **5** | 9 | **N2** | IMP-0 |
| 12 | Galadriel S.A. | 0 | 0 | 0 | 0 | 0 | 0 | 0 | **0** | s/d | s/d | s/d | s/d | s/d | s/d | s/d | s/d | **0** | s/d | s/d | s/d | s/d | **0** | 12 | **N4** | IMP-0 |
| 13 | Grupo Berilo S.A. | 0 | 0 | s/d | 0 | 0 | 2 | 0 | **2** | s/d | s/d | s/d | s/d | s/d | s/d | s/d | s/d | **0** | s/d | s/d | s/d | s/d | **0** | 13 | **N3** | IMP-0 |
| 14 | Grupo Hendy S.A. | 1 | 0 | s/d | 2 | 2 | 3 | 0 | **8** | s/d | s/d | s/d | s/d | s/d | s/d | s/d | s/d | **0** | 1 | 2 | 2 | 1 | **6** | 9 | **N2** | IMP-0 |
| 15 | Grupo M S.A. | 1 | 0 | s/d | 2 | 2 | 3 | 0 | **8** | s/d | s/d | s/d | s/d | s/d | s/d | s/d | s/d | **0** | 1 | 2 | 2 | s/d | **5** | 10 | **N2** | IMP-0 |
| 16 | Grupo Vázquez S.A.E. | 3 | 3 | 3 | 3 | 2 | 3 | 1 | **18** | s/d | s/d | s/d | s/d | s/d | s/d | s/d | s/d | **0** | 1 | 2 | 2 | s/d | **5** | 9 | **N1** | IMP-C (sucesora de Ueno Holding); IMP-D(h) |
| 17 | GSR E.A.S. | 0 | 0 | 1 | 0 | 0 | 0 | 0 | **1** | s/d | s/d | s/d | s/d | s/d | s/d | s/d | s/d | **0** | s/d | s/d | s/d | s/d | **0** | 12 | **N3** | IMP-0 |
| 18 | Hanoi S.A. | 3 | 3 | s/d | 3 | 2 | 1 | 0 | **12** | s/d | s/d | s/d | s/d | s/d | s/d | s/d | s/d | **0** | s/d | s/d | s/d | 1 | **1** | 12 | **N1** | IMP-0 |
| 19 | HD Invest E.A.S. Unipersonal | 0 | 0 | s/d | 0 | 0 | 0 | 0 | **0** | s/d | s/d | s/d | s/d | s/d | s/d | s/d | s/d | **0** | 1 | s/d | 1 | s/d | **2** | 11 | **N4** | IMP-0 |
| 20 | Impresión Distribución y Logística S.A. | 3 | 3 | s/d | 3 | 2 | 0 | 0 | **11** | s/d | s/d | s/d | s/d | s/d | s/d | s/d | s/d | **0** | s/d | s/d | s/d | s/d | **0** | 13 | **N1** | IMP-0 (socia 2% de Kaitel; ver Kaitel) |
| 21 | Inter-Express S.A. | 3 | 3 | s/d | 3 | 2 | 0 | 0 | **11** | s/d | s/d | s/d | s/d | s/d | s/d | s/d | s/d | **0** | s/d | s/d | s/d | s/d | **0** | 13 | **N1** | IMP-0 |
| 22 | Intertours S.A. | 3 | 3 | s/d | 3 | 2 | 0 | 0 | **11** | s/d | s/d | s/d | s/d | s/d | s/d | s/d | s/d | **0** | s/d | s/d | 1 | s/d | **1** | 12 | **N1** | IMP-0 |
| 23 | ITTI S.A.E.C.A. | 3 | 3 | 2 | 3 | 3 | 3 | 1 | **18** | 1 | 1 | s/d | 1 | 2 | s/d | s/d | s/d | **5** | 1 | 2 | 2 | s/d | **5** | 5 | **N1** | IMP-A(h); IMP-B(h) |
| 24 | Kaitel S.R.L. | 3 | 3 | 3 | 3 | 3 | 3 | 0 | **18** | 1 | 1 | s/d | 2 | 1 | 1 | s/d | 1 | **7** | s/d | s/d | 1 | 2 | **3** | 4 | **N1** | IMP-B(h); IMP-E(h); IMP-A(h) |
| 25 | Kasas Propiedades S.A.E. | 0 | 0 | s/d | 0 | 0 | 0 | 0 | **0** | s/d | s/d | s/d | s/d | s/d | s/d | s/d | s/d | **0** | 1 | s/d | s/d | s/d | **1** | 12 | **N4** | IMP-0 |
| 26 | Kostas Viajes y Turismo S.R.L. | 3 | 3 | s/d | 3 | 2 | 0 | 0 | **11** | s/d | s/d | s/d | s/d | s/d | s/d | s/d | s/d | **0** | s/d | s/d | s/d | s/d | **0** | 13 | **N1** | IMP-0 |
| 27 | La Tropa Fletes E.A.S. | 0 | 0 | s/d | 0 | 0 | 0 | 0 | **0** | s/d | s/d | s/d | s/d | s/d | s/d | s/d | s/d | **0** | 1 | s/d | 1 | s/d | **2** | 11 | **N4** | IMP-0 |
| 28 | MOWI S.A. | 1 | 0 | s/d | 1 | 0 | 3 | 0 | **5** | s/d | s/d | s/d | s/d | s/d | s/d | s/d | s/d | **0** | 1 | 2 | 2 | s/d | **5** | 10 | **N2** | IMP-0 |
| 29 | Nubicom Paraguay S.A. | 0 | 0 | s/d | 3 | 2 | 0 | 0 | **5** | s/d | s/d | s/d | s/d | s/d | s/d | s/d | s/d | **0** | s/d | s/d | s/d | s/d | **0** | 13 | **N2** | IMP-0 |
| 30 | Office Design S.R.L. | 1 | 0 | s/d | 1 | 0 | 1 | 0 | **3** | s/d | s/d | s/d | s/d | s/d | s/d | s/d | s/d | **0** | s/d | 2 | 2 | s/d | **4** | 11 | **N3** | IMP-0 |
| 31 | Oniria S.A. | 3 | 3 | s/d | 1 | 0 | 0 | 0 | **7** | s/d | s/d | s/d | s/d | s/d | s/d | s/d | s/d | **0** | s/d | s/d | 1 | s/d | **1** | 12 | **N2** | IMP-0 |
| 32 | Place Analyzer E.A.S. | 3 | 3 | 3 | 3 | 3 | 3 | 0 | **18** | s/d | s/d | s/d | s/d | s/d | s/d | s/d | s/d | **0** | s/d | s/d | s/d | s/d | **0** | 12 | **N1** | IMP-0 |
| 33 | Red Digital de Procesamiento S.A. (REDIPRO) | 3 | 3 | 3 | 3 | 3 | 3 | 1 | **19** | 1 | s/d | s/d | s/d | 2 | s/d | s/d | s/d | **3** | 3 | 3 | 2 | s/d | **8** | 7 | **N1** | IMP-D(h) |
| 34 | Red Digital S.A. (REDISA) | 3 | 3 | 3 | 3 | 3 | 3 | 1 | **19** | 1 | s/d | s/d | s/d | s/d | s/d | s/d | s/d | **1** | 3 | 2 | 2 | s/d | **7** | 8 | **N1** | IMP-D(h) |
| 35 | Red UTS Paraguay S.A. | 2 | 2 | 3 | 3 | 3 | 3 | 0 | **16** | s/d | s/d | s/d | s/d | s/d | s/d | s/d | s/d | **0** | s/d | s/d | s/d | s/d | **0** | 12 | **N1** | IMP-0 |
| 36 | Servicios de Asistencia Tecnológica al Comercio S.A. (SATEC) | 0 | 0 | s/d | 0 | 0 | 0 | 0 | **0** | s/d | s/d | s/d | s/d | s/d | s/d | s/d | s/d | **0** | 1 | s/d | s/d | s/d | **1** | 12 | **N4** | IMP-0 |
| 37 | Solución Efectiva S.A. | 1 | 1 | 0 | 0 | 0 | 0 | 0 | **2** | s/d | s/d | s/d | s/d | s/d | s/d | s/d | s/d | **0** | s/d | s/d | s/d | s/d | **0** | 12 | **N3** | IMP-0 |
| 38 | Technoma S.A.E.C.A. | 0 | 0 | s/d | 1 | 0 | 3 | 0 | **4** | s/d | s/d | s/d | s/d | s/d | s/d | s/d | s/d | **0** | 1 | s/d | s/d | s/d | **1** | 12 | **N2** | IMP-0 |
| 39 | Terravaz S.A. Emisora | 3 | 3 | s/d | 3 | 0 | 0 | 0 | **9** | s/d | s/d | s/d | s/d | s/d | s/d | s/d | s/d | **0** | s/d | s/d | 2 | s/d | **2** | 12 | **N1** | IMP-0 |
| 40 | Tiva S.A. | 3 | 3 | 3 | 3 | 3 | 0 | 0 | **15** | s/d | s/d | s/d | s/d | s/d | s/d | s/d | s/d | **0** | s/d | s/d | 1 | s/d | **1** | 11 | **N1** | IMP-0 |
| 41 | TUIU S.A. | 1 | 0 | s/d | 2 | 2 | 1 | 0 | **6** | s/d | s/d | s/d | s/d | s/d | s/d | s/d | s/d | **0** | 1 | 2 | 2 | s/d | **5** | 10 | **N2** | IMP-0 |
| 42 | UENO HOLDINGS S.A.R.L. | 3 | 3 | s/d | 2 | s/d | s/d | 1 | **9** | s/d | s/d | s/d | s/d | s/d | s/d | s/d | s/d | **0** | s/d | s/d | 2 | s/d | **2** | 14 | **N1** | IMP-0 (controlante último extranjero; ver IMP-D) |
| 43 | U Paraguay S.A. | 3 | 3 | 2 | 3 | 3 | 3 | 1 | **18** | s/d | s/d | s/d | s/d | 1 | s/d | s/d | s/d | **1** | 2 | 3 | 2 | s/d | **7** | 8 | **N1** | IMP-D(h) |
| 44 | Ueno Administradora de Fondos Patrimoniales de Inversión S.A. | 3 | 3 | s/d | 3 | 2 | 1 | 3 | **15** | s/d | s/d | s/d | s/d | s/d | s/d | s/d | s/d | **0** | s/d | 1 | s/d | s/d | **1** | 12 | **N1** | IMP-0 |
| 45 | Ueno Bank S.A. | 3 | 3 | s/d | 3 | 2 | 3 | 3 | **17** | s/d | s/d | s/d | s/d | s/d | s/d | s/d | s/d | **0** | 2 | 3 | 2 | s/d | **7** | 10 | **N1** | REF (empleador formal en resolución) |
| 46 | Ueno Casa de Bolsa S.A. | 3 | 3 | s/d | 3 | 2 | 1 | 3 | **15** | s/d | s/d | s/d | s/d | s/d | s/d | s/d | s/d | **0** | s/d | 1 | s/d | s/d | **1** | 12 | **N1** | IMP-0 |
| 47 | Ueno Holding S.A.E.C.A. | 2 | 2 | s/d | 3 | 3 | 3 | 3 | **16** | s/d | s/d | s/d | s/d | s/d | s/d | s/d | s/d | **0** | s/d | 3 | 2 | s/d | **5** | 11 | **N1** | IMP-C (absorbida por GV) |
| 48 | Ueno Seguros S.A. | 3 | 3 | s/d | 3 | 2 | 1 | 3 | **15** | s/d | s/d | s/d | s/d | s/d | s/d | s/d | s/d | **0** | s/d | 1 | 1 | s/d | **2** | 11 | **N1** | IMP-0 |
| 49 | V Media S.A. | 2 | 0 | s/d | 2 | 2 | 0 | 0 | **6** | s/d | s/d | s/d | s/d | s/d | s/d | s/d | s/d | **0** | s/d | 2 | 2 | s/d | **4** | 11 | **N2** | IMP-0 |
| 50 | Villa Oliva Rice S.A. | 0 | 0 | s/d | 0 | 0 | 0 | 0 | **0** | s/d | s/d | s/d | s/d | s/d | s/d | s/d | s/d | **0** | s/d | s/d | s/d | s/d | **0** | 13 | **N4** | IMP-0 |
| 51 | Vinanzas S.A. | 3 | 3 | s/d | 3 | 2 | 3 | 0 | **14** | s/d | s/d | s/d | s/d | s/d | s/d | s/d | s/d | **0** | 1 | s/d | 1 | s/d | **2** | 11 | **N1** | IMP-0 |

**Lectura rápida de la matriz:**
- **Plano societario (S):** completo y concluyente para el núcleo (PS 15–19 en Ueno Bank, U Paraguay, GV, ITTI, Kaitel, REDIPRO, REDISA, Place Analyzer).
- **Plano laboral (L):** casi todo "s/d". Solo Kaitel (PL 7), ITTI (PL 5), REDIPRO (PL 3), REDISA (PL 1) y U Paraguay (PL 1) tienen algún indicio. **Esta es la brecha que el MTESS debe cerrar** (§7).
- **Plano de fraude (F):** los valores más altos están en REDIPRO (8), Ueno Bank (7), REDISA (7) y U Paraguay (7), por la operatoria de preferidas de 2026. Les siguen Grupo Hendy (6) y las demás sociedades salidas del grupo (4–5).

---

## 4. Fichas por entidad, agrupadas por nivel

Formato de cada ficha: **hechos documentados** (con fuente MEF), **inferencias** (si las hay) y **vía jurídica más sólida**. Las referencias legales remiten a `marco_juridico_laboral.md` (CT = Código del Trabajo; CC = Código Civil).

### 4.1 Nivel N1 – Control común (25 entidades)

#### 4.1.a Cúspide y holdings

**16. Grupo Vázquez S.A.E. (RUC 80086759-9)** – N1 · PS 18 · PF 5 · **IMP-C; IMP-D(h)**
- *Hechos:*
  - Accionistas: F. M. Vázquez Villasanti 75,94 % del capital (≈94 % de los votos); Guillermo y Adriana Vázquez Muniagurria y Rebeca Villasanti Fariña 8,02 % cada uno, al 27/03/2026 [MEF: Grupo Vazquez SAE › Libro de registro de accionistas.pdf p.25]. El registro es manuscrito: confianza media.
  - Directorio: presidente F. M. Vázquez Villasanti, VP G. Vázquez Muniagurria, directores B. Algorta y J. Rey [MEF: › Acta de asamblea ordinaria N° 31.pdf p.2].
  - **Absorbió por fusión a Ueno Holding S.A.E.C.A.** [MEF: › Escritura Pública 131.pdf, 16/07/2025].
  - Domicilio: Torres del Paseo, Torre 2 piso 25, el mismo que U Paraguay y Kaitel. Dominio gvcorp.com.py [MEF].
  - No hay constancia de beneficiarios finales en la carpeta.
- *Vía:*
  - (i) **Sucesión universal por fusión**: GV responde por las obligaciones, incluidas las laborales, de Ueno Holding (hecho documentado; regla de derecho común de la fusión, artículo del CC no verificado).
  - (ii) Como controlante última, **IMP-D(h)** solo si se prueba uso abusivo o fraudulento (CC art. 372).
  - Su patrimonio relevante son las participaciones **no bancarias** (ITTI, Terravaz, 23 Sports, Oniria) [INFERENCIA, `analisis_economico.md` §5.2].

**42. U Holdings S.à r.l. (MEF: "Ueno Holdings S.A.R.L."; sin RUC)** – N1 · PS 9 · **IMP-0**
- *Hechos:*
  - Sin RUC ni registro SIARA [MEF: Informe CRA 385, p.2].
  - Titular del 97,99 % de U Paraguay al 25/09/2026 [MEF: U PARAGUAY S.A › REGISTRO ACCIONISTAS 25-09-2026.pdf].
  - Representada en asambleas por M. Almada (2025) y por F. M. Vázquez Villasanti (2026) [MEF: U PARAGUAY S.A › ESCRITURA MODIFICACION NRO 84.pdf p.4; ACTA ORDINARIA.pdf p.2].
  - En el listado de beneficiarios finales pendiente de REDISA figuran dos personas de Arendt Services (Luxemburgo) [MEF: RED DIGITAL S.A › Listado de Beneficiarios Finales … pendiente de aprobación.pdf p.2].
- *Inferencia:* es una sociedad interpuesta opaca en la cúspide. Según la prensa, GV tiene el 86,73 % [PÚBLICO].
- *Vía:* no es empleadora en Paraguay. Su relevancia es **probatoria**: la cadena de control y la interposición de una sociedad extranjera sin beneficiario final declarado son indicio F3 para el conjunto.

**43. U Paraguay S.A. (RUC 80135001-8)** – N1 · PS 18 · PL 1 · PF 7 · **IMP-D(h)**
- *Hechos:*
  - Controla Ueno Bank (93,08 % del capital, 98,70 % de los votos) [MEF: UENO BANK S.A › ACTA DE ASAMBLEA.pdf p.1, acta 99, 13/07/2026], Ueno Seguros (82,04 %), Casa de Bolsa (99,99 %), REDIPRO (100 % de los votos) y REDISA (99,99 % de los votos) [MEF].
  - Presidente J. M. Gustale Cardoni (también presidente del banco); VP F. M. Vázquez; síndico M. Almada [MEF: U PARAGUAY S.A › ACTA ORDINARIA.pdf p.2].
  - Correo SIARA legales@itti.digital: su función legal la lleva ITTI.
  - **Recibió del banco 263.339 preferidas de REDIPRO entre el 09/09 y el 02/10/2026** [MEF: RED DIGITAL DE PROCESAMIENTO S.A › REGISTRO ACCIONISTAS 02-10-2026.pdf].
  - Contradicción entre las actas del 21/07/2025 (GV 70,36 % de los votos) y los registros (U Holdings ≈100 %) [MEF].
- *Vía:* **preservación patrimonial e inoponibilidad (h)**. Es **receptora de activos salidos del banco** días antes de la resolución. No se le conocen empleados propios (s/d).

**47. Ueno Holding S.A.E.C.A. (RUC 80011000-5)** – N1 · PS 16 · PF 5 · **IMP-C**
- *Hechos:*
  - Presidente O. Urdapilleta, VP L. Angulo Rivera [MEF: UENO HOLDING SAECA › CONSTANCIA RA.pdf, 22/04/2025].
  - Declarante Sandra Caballero (@gvcorp.com.py), la misma que declara por Kaitel [MEF: › CONSTANCIA RA.pdf; CONSTANCIA BF NRO 347282.pdf].
  - Como emisora, no declaró accionistas ni beneficiarios finales (remisión al convenio CNV–Abogacía del Tesoro).
  - **Absorbida por GV** (Esc. 131, 16/07/2025) [MEF: GRUPO VAZQUEZ SAE › Escritura Pública 131.pdf].
- *Vía:* los trabajadores y ex trabajadores de Ueno Holding (ex Credicentro) tienen **como deudor a GV**.

**23. ITTI S.A.E. (ex S.A.E.C.A.; RUC 80028355-4)** – N1 · PS 18 · PL 5 · PF 5 · **IMP-A(h); IMP-B(h)**
- *Hechos:*
  - Accionistas al 02/10/2026: GV 77,46 %, **Ueno Bank 16,95 %**, Ueno Seguros 3,03 %, Business & Financial Group 2,56 % [MEF: ITTI S.A.E › REGISTRO ACCIONISTAS FOLIO 5.pdf p.2].
  - Directorio: presidente C. Astigarraga (síndico suplente del banco), VP G. Vázquez Muniagurria (director suplente del banco), B. Algorta (director de GV) [MEF: › ACTA ORDINARIA NRO 42.pdf p.1].
  - Sede: Torres del Paseo, Torre 3 piso 11. Su dominio itti.digital lo usan U Paraguay, Hanoi, IDL, Grupo M, Vinanzas y las empresas de turismo como correo SIARA [MEF].
  - Controla, directa o indirectamente, Kaitel (vía WOM77), IDL, Tiva, Place Analyzer, Hanoi, Kostas, Intertours, Discover, COMDETUR y Vinanzas [MEF; `control_indirecto.csv`].
  - Registro con 401.201 acciones frente a 250.000 suscriptas, sin documento de emisión [MEF].
- *Público:* "Itti ofrece servicios tecnológicos a Ueno". Unos 1.600 trabajadores afectados [PÚBLICO].
- *Vía:* **CT arts. 24 y 22**: si el personal de ITTI trabajaba en el core, la app o el soporte del banco, bajo dirección del banco, el banco o ITTI y el banco pueden ser coempleadores. **CT art. 26 a contrario** si ITTI carecía de autonomía. Respecto de los trabajadores de **Kaitel**, ITTI es controlante y posible **beneficiaria** de los servicios.
- **Faltan:** contrato ITTI–banco, facturación, nómina por destino y organigrama.

#### 4.1.b Núcleo financiero y de pagos

**45. Ueno Bank S.A. (RUC 80026157-7)** – N1 · PS 17 · PF 7 · **REF**
- *Hechos:*
  - Controlante U Paraguay; GV 1,96 % [MEF: UENO BANK S.A › ACTA DE ASAMBLEA.pdf p.1–2].
  - Presidente J. M. Gustale; VP1 F. M. Vázquez Villasanti; síndico titular M. Almada; síndico suplente C. Astigarraga [MEF: › ACTA ASAMBLEA.pdf p.4].
  - **No declaró beneficiarios finales** en la carpeta.
  - **Integró Gs. 640.468 M en preferidas de REDIPRO y Gs. 236.230 M en preferidas de REDISA (29/05/2026)** y las cedió parcialmente a U Paraguay en septiembre–octubre de 2026. **Recibió 68.000 acciones de ITTI el 02/10/2026** [MEF: carpetas REDIPRO, RED DIGITAL e ITTI].
- *Vía:* **empleador directo** de ≈490 trabajadores [PÚBLICO]. Rigen la **Ley 2334/03 art. 17** (el interventor determina los beneficios sociales) y el **art. 26** (preferencia de los no transferidos; las adquirentes no son sucesoras). No admite embargos durante la resolución (art. 25).

**48. Ueno Seguros S.A. (RUC 80004049-0)** – N1 · PS 15 · PF 2 · IMP-0
- *Hechos:*
  - U Paraguay 82,04 %, GV 5,39 %, familia Sarubbi ≈12 % [MEF: UENO SEGUROS S.A › Registro de accionistas.pdf, 31/12/2025].
  - Directorio: F. Boccia, E. Gross Brown (presidente de REDIPRO, Casa de Bolsa y AFPI), A. Vázquez Muniagurria y J. Rey (director de GV) [MEF: › Acta de Asamblea Ordinaria.pdf].
  - Es accionista del 3,03 % de ITTI.
- *Inferencia:* tiene actividad propia y patrimonio regulado. Es de las pocas sociedades con **capacidad de pago real**.
- *Vía:* empleador directo de su personal. Sin indicios de personal compartido con el banco (s/d). Verificar en inspección si hubo **bancaseguros con personal del banco o de Kaitel**: eso abriría IMP-A o IMP-B.

**46. Ueno Casa de Bolsa S.A. (RUC 80124419-6)** – N1 · PS 15 · PF 1 · IMP-0
- *Hechos:*
  - U Paraguay 99,99 % [MEF: UENO CASA DE BOLSA S.A › ACTA ORDINARIA NRO 10.pdf, 06/02/2026].
  - Presidente E. Gross Brown; VP **C. Impagliatelli** (director del banco y gerente de Kaitel).
  - Fundada con capital del banco (2023) y transferida a GV y luego a U Paraguay (2024–2025) [MEF].
- *Vía:* empleador directo. IMP-0.

**44. Ueno AFPI S.A. (RUC 80127778-7)** – N1 · PS 15 · PF 1 · IMP-0
- *Hechos:* Casa de Bolsa 99,97 %, GV 0,03 %. El mismo directorio que la Casa de Bolsa [MEF: UENO ADMINISTRADORA… › ACTA ORDINARIA NRO 8.pdf].
- *Vía:* empleador directo. IMP-0.

**33. REDIPRO – Red Digital de Procesamiento S.A. (RUC 80114621-6)** – N1 · PS 19 · PL 3 · PF 8 · **IMP-D(h)**
- *Hechos:*
  - Al 02/10/2026: U Paraguay 50,94 % del capital (100 % de los votos); **Ueno Bank 49,06 % en preferidas sin voto** [MEF: RED DIGITAL DE PROCESAMIENTO S.A › REGISTRO ACCIONISTAS 02-10-2026.pdf p.1].
  - Beneficiario final aprobado: F. M. Vázquez Villasanti, 62,87 % [MEF: › Constancia BF.pdf, jun-2025]. La declaración 2026 está **pendiente** y lista a U Holdings, U Paraguay y Ueno Bank [MEF: › BENEFICIARIOS FINALES.pdf].
  - Presidente E. Gross Brown. Los directores usan correos @itti.digital.
  - Declarante: A. Campos Pardo (@uenoholding.com.py), que también declara por AIME [MEF: › Constancia RA.pdf].
  - **Cadena del 09/09–25/09/2026**: 180.646 preferidas pasan Ueno Bank → Red Digital → ITTI → GV → U Paraguay. Siguen ventas al 30/09 y 02/10 [MEF: › REGISTRO ACCIONISTAS 02-10-2026.pdf].
- *Público:* marca de pagos "wepa" [PÚBLICO].
- *Vía:* **preservación del patrimonio aportado por el banco** e hipótesis de inoponibilidad o fraude (CC art. 372). Respecto de su propio personal (operadores y soporte de la red), la hipótesis es IMP-A con el banco, a verificar en inspección.

**34. REDISA – Red Digital S.A. (RUC 80114674-7)** – N1 · PS 19 · PL 1 · PF 7 · **IMP-D(h)**
- *Hechos:*
  - U Paraguay 99,99 % de los votos. **Ueno Bank 72,12 % del capital en preferidas** (Gs. 236.230 M integrados el 29/05/2026) [MEF: RED DIGITAL S.A › REGISTRO ACCIONISTAS.pdf p.10–11].
  - Beneficiario final F. M. Vázquez Villasanti, 76 % [MEF: › Constancia B.F..pdf]. Listado 2026 pendiente con 35 registros.
  - Directorio: presidente C. Berea; director y **gerente O. Urdapilleta** (comprador de Grupo M y Grupo Hendy); síndico M. Almada [MEF: › ACTA ORDINARIA NRO 16.pdf p.2; ESCRITURA MODIFICACION NRO 57.pdf p.5].
  - **Intervino en la cadena de las preferidas de REDIPRO (09–25/09/2026)** [MEF].
- *Vía:* la misma que REDIPRO. Tuvo utilidad de Gs. 19.115 M en 2025 [MEF, según `analisis_economico.md`]: hay **capacidad de pago**, que conviene preservar.

**51. Vinanzas S.A. (RUC 80090944-5)** – N1 · PS 14 · PF 2 · IMP-0
- *Hechos:*
  - ITTI 49,73 % + GV 12,34 % = 62,07 %; IOIO S.A.E.C.A. 37,93 % [MEF: VINANZAS S.A › ACTA ORDINARIA NRO 2.pdf; REGISTRO ACCIONISTAS.pdf].
  - Presidente G. Vázquez Muniagurria; síndico M. Almada. Correo legales@itti.digital.
- *Público:* habría comprado cartera del banco y tiene cautelas penales [PÚBLICO].
- *Vía:* empleador directo. IMP-0. Es de interés patrimonial (F1).

#### 4.1.c Tecnología, servicios y personal

**24. Kaitel S.R.L. (RUC 80119497-0)** – N1 · PS 18 · **PL 7** · PF 3 · **IMP-B(h); IMP-E(h); IMP-A(h)**
- *Hechos:*
  - Objeto: **tercerización de recursos humanos**.
  - Socios: **WOM77 S.A. 98 %** e **IDL 2 %** desde el 25/03/2025 [MEF: KAITEL SRL › KAITEL SRL-SIARA-REV/ESCRITURA MODIFICACION NRO 44.pdf p.8].
  - Beneficiario final **F. M. Vázquez, 74,51 % (92,15 % de los votos), vía WOM77 → ITTI → GV** [MEF: › CONSTANCIA BF NRO 389461.pdf p.1].
  - Gerentes: **C. Impagliatelli** (director de Ueno Bank, VP de Casa de Bolsa y AFPI) y **M. Almada** (síndico de Ueno Bank y U Paraguay) [MEF: › CONSTANCIA RA.pdf p.1].
  - Domicilio: Torre 2 piso 25, **el mismo que GV y U Paraguay**. Declarante S. Caballero (@gvcorp.com.py) [MEF].
  - **Capital social e integrado: Gs. 50.000.000** [MEF: › ESCRITURA CONSTITUCION NRO 1153.pdf; ESCRITURA MODIFICACION NRO 44.pdf].
- *Público:* unos 1.200 trabajadores afectados [PÚBLICO].
- *Inferencia:* con ese capital frente a esa nómina, Kaitel es estructuralmente insolvente. Su razón económica es proveer personal al banco y al grupo.
- *Vía (la más sólida de todo el conjunto):*
  - **CT art. 25 b)**: si Kaitel contrató personal que trabajaba en beneficio del banco (o de ITTI), con locales, equipos y sistemas de éstos y en actividades ordinarias o conexas, es **intermediaria**. Si no declaró su calidad y el nombre del empleador al contratar, **responde solidariamente** con el beneficiario, y éste es el **empleador**.
  - **CT art. 26 a contrario**: no asume riesgos con elementos propios.
  - **DL 1860/50 art. 70**: el patrón principal responde ante el IPS.
- **Faltan:** contratos Kaitel–banco y Kaitel–ITTI; destino de cada trabajador; quién daba las órdenes; contratos de trabajo (para ver si declaran por cuenta de quién se contrata).

**20. IDL – Impresión Distribución y Logística S.A. (RUC 80054859-0)** – N1 · PS 11 · IMP-0
- *Hechos:*
  - ITTI 99,23 %, GV 0,77 % [MEF: IMPRESION DISTRIBUCION Y LOGISTICA SA › ACTA ORDINARIA NRO 17.pdf].
  - Presidente C. Astigarraga; VP R. Ramírez Lezcano.
  - **Socia del 2 % de Kaitel.**
- *Inferencia:* por su objeto, logística de tarjetas y documentos del banco.
- *Vía:* empleador directo. Verificar si su personal servía al banco (IMP-A).

**40. Tiva S.A. (RUC 80074954-5)** – N1 · PS 15 · PF 1 · IMP-0
- *Hechos:*
  - ITTI 60 %; V. Cartes León 26 %; M. B. Serra 10 %; C. Rodríguez Alcalá 4 % [MEF: TIVA SA › Constancia RA 2025 1.pdf].
  - Beneficiario final **F. M. Vázquez Villasanti, 35,32 %, vía ITTI → GV** [MEF: › Constancia BF 2025 1.pdf].
  - Presidente C. Astigarraga; VP L. Angulo. Declarante S. Caballero.
- *Vía:* empleador directo. Si desarrollaba software para el banco: IMP-A o IMP-B (a verificar).

**32. Place Analyzer S.A. (RUC 80117081-8; transformada de E.A.S. a S.A. por Esc. 44/2025)** – N1 · PS 18 · IMP-0
- *Hechos:*
  - ITTI 60 %, Mayeregger 32 %, Vargas Peña 8 % [MEF: PLACE ANALYZER SA › PLACE ANALYZER SA-SIARA/ACTA ORDINARIA NRO 1.pdf].
  - Beneficiario final **F. M. Vázquez Villasanti, 43,77 %** [MEF: › CONSTANCIA BF NRO 399459.pdf].
  - Directores: G. Vázquez, C. Astigarraga, P. Meza. Sede: Torre 3 piso 11. Declarante S. Caballero (@uenoholding.com.py).
- *Vía:* la misma que Tiva.

**35. Red UTS Paraguay S.A. (RUC 80018381-9)** – N1 · PS 16 · IMP-0
- *Hechos:*
  - ITTI 40,23 % (sin mayoría), Masulli 20,12 %, Fleischman 19,83 %, Gayol 19,83 % [MEF: RED UTS PARAGUAY SA › RED UTS SA/REGISTRO ACCIONISTAS FOLIO 2.pdf].
  - Beneficiario final **F. M. Vázquez, 36,46 %** [MEF: › CONSTANCIA BF NRO 405711.pdf].
  - Presidente Astigarraga; VP Cardozo Ledesma. Declarante C. Dávalos (@uenoholding.com.py).
- *Vía:* empleador directo. IMP-0.

**18. Hanoi S.A. (RUC 80089722-6)** – N1 · PS 12 · PF 1 · IMP-0
- *Hechos:*
  - ITTI 72,76 %, Markhel S.A. 27,24 % [MEF: HANOI SA › REGISTRO ACCIONISTAS-HOJA 11.pdf].
  - Presidente Astigarraga; VP **D. Mongelos (vicepresidenta 2.ª de Ueno Bank)**.
  - Actividad no identificada.
- *Vía:* IMP-0. Pedir su objeto y su nómina (F4: posible sociedad sin actividad).

#### 4.1.d Turismo, inmobiliaria y diversificación

**27. Kostas Viajes y Turismo S.R.L. (RUC 80004240-9)** – N1 · PS 11 · IMP-0. ITTI 98,94 %, Discover 1,06 %; gerente L. M. Cardozo Ledesma [MEF: KOSTAS VIAJES Y TURISMO SRL › ESCRITURA MODIFICION NRO 301.pdf].
**21. Inter-Express S.A. (RUC 80007371-1)** – N1 · PS 11 · IMP-0. Kostas 99,98 %, ITTI 0,02 %; presidente Astigarraga; síndico Almada [MEF: INTER EXPRESS SA › REGISTRO ACCIONISTAS PAG 6.pdf; ACTA ORDINARIA NRO 152.pdf].
**22. Intertours S.A. (RUC 80014477-5)** – N1 · PS 11 · PF 1 · IMP-0. ITTI 70 % (con un 30 % adicional comprado el 22/07/2026, en vísperas de la crisis); Match S.A. 30 % [MEF: INTERTOURS SA › CONSTANCIA TRASFERENCIA ACCIONES NRO 548; ACTA DIRECTORIO NRO 109.pdf].
**7. Discover Paraguay S.A. (RUC 80087415-3)** – N1 · PS 11 · IMP-0. ITTI 74,79 %; F. M. Vázquez 0,41 %; presidente Cardozo Ledesma; síndico Almada; directora suplente D. Mongelos [MEF: DISCOVER PARAGUAY SA › REGISTRO ACCIONISTAS-PAG 14.pdf; ACTA ORDINARIA NRO 11.pdf].
**5. COMDETUR S.R.L. (RUC 80001894-0)** – N1 · PS 12 · IMP-0. ITTI 99 %, Discover 1 %; gerente y representante legal **G. Vázquez Muniagurria** [MEF: COMPAÑIA DE DESARROLLO TURISTICO SRL › ESCRITURA MODIFICACION NRO 201.pdf].
- *Vía común del subgrupo turismo:* son **empleadores directos** con actividad propia e ingresos de terceros [INFERENCIA]. No hay indicios de que su personal sirviera al banco. Interesan por su **capacidad de pago** y como **patrimonio del grupo** si prosperara una inoponibilidad respecto de ITTI.

**39. Terravaz S.A.E. (ex RADICE S.A.E.C.A.; RUC 80104014-0)** – N1 · PS 9 · PF 2 · IMP-0
- *Hechos:* GV 97,33 % desde 06–08/2025; presidente Cardozo Ledesma; VP Algorta; síndico Almada [MEF: TERRAVAZ SAE › ACTA ORDINARIA NRO 21.pdf; ESCRITURA MODIFICACION NRO 121.pdf].
- *Vía:* empleador directo. Tiene **activos inmobiliarios** (Encarnación) de interés para las cautelas.

**1. 23 Sports Marketing S.A. (RUC 80103199-0)** – N1 · PS 11 · PF 1 · IMP-0
- *Hechos:*
  - GV 60 % desde 01/2025 [MEF: 23 SPORTS MARKETING SA › ACTA ORDINARIA NRO 10-APROBADO.pdf].
  - Directora P. Meza (también directora de IDL y Place Analyzer).
  - La constancia de beneficiarios finales está **pendiente** e incluye personas jurídicas.
- *Vía:* empleador directo. Si hacía patrocinio o publicidad de "ueno", es solo un indicio L1.

### 4.2 Nivel N2 – Vinculación relevante (11 entidades)

**31. Oniria S.A. (RUC 80023654-8)** – N2 · PS 7 (S1 = 3, pero S3 y S4 < 2) · PF 1 · IMP-0. GV 60 % desde el 03/01/2025, representada por B. Algorta [MEF: ONIRIA SA › REGISTRO ACCIONISTAS.pdf; ACTA ORDINARIA NRO 31.pdf]. Su directorio actual no es del núcleo, salvo el síndico R. Barrios. Comparte sede (Complejo Textilia) con 23 Sports. *Vía:* empleador directo. Tiene patrimonio (dividendos 2025) [MEF, según `analisis_economico.md`].

**10. Fintux E.A.S. (RUC 80130722-8)** – N2 (decisión expresa) · PS 6 · IMP-0. ITTI 30 %; la constancia de beneficiarios finales declara a "Grupo Vázquez S.A.E." como BF [MEF: FINTUX EAS › Constancia EAS 2026 2.pdf; CONSTANCIA BF EAS.pdf]. Por ser E.A.S., Ley 6480/20 art. 4. *Vía:* IMP-0.

**Sociedades salidas del grupo en 2025–2026 hacia personas del entorno** (`salidas_grupo.csv`):

| # | Sociedad | Fecha de salida | Vendedores | Compradores (rol en el grupo) | Fuente MEF |
|---|---|---|---|---|---|
| 28 | MOWI S.A. | 19/05/2025 | ITTI, F. M. Vázquez, (Ueno Holding) | S. Pizurno (director de Grupo M; accionista de Technoma) 90 % / J. A. Sala Cardozo (socio de GSR) 10 % | MOWI S.A › REGISTRO ACCIONISTAS FOLIO NRO 7.pdf; ACTA ORDINARIA NRO 6.pdf |
| 11 | Franede S.A. | 30/06/2025 | GV | Mauro Vargas Wildberger 99,62 % (ex socio de AIME; representa a CBS) | FRANEDE S.A › REGISTRO ACCIONISTAS FOLIO 2.pdf; ACTA ORDINARIA NRO 78.pdf |
| 41 | TUIU S.A. | 28/08/2025 | ITTI | L. F. Ríos Espínola / A. Gayol (accionistas de Discover y Red UTS); síndica M. Gadea | TUIU S.A › REGISTRO ACCIONISTAS.pdf; ACTA ORDINARIA NRO 7.pdf |
| 15 | Grupo M S.A. | 30/09/2025 | ITTI, GV | O. Urdapilleta (director y gerente de REDISA; ex presidente de Ueno Holding) 90 % / D. Gómez 10 % | GRUPO M S.A › REGISTRO ACCIONISTA.pdf p.2; ACTA ORDINARIA NRO 21.pdf |
| 14 | Grupo Hendy S.A. | 30/09/2025 | ITTI, GV | V. Godoy (ex socia de Kaitel) 90 % / O. Urdapilleta 10 % | GRUPO HENDY S.A › REGISTRO ACCIONISTAS.pdf p.2; ACTA ORDINARIA NRO 21.pdf |
| 30 | Office Design S.R.L. | 30/10/2025 | GV, ITTI | M. Gadea 95 % / E. Vera 5 % (domicilio declarado: sede de ITTI) | Office Design S.R.L › Escritura Públcia N° 190.pdf |
| 49 | V Media S.A. | 23/03/2026 | GV | G. Villasanti Farinha 99,9 % (presidenta de AIME) / CBS 0,1 % | V MEDIA SA › REGISTRO DE ACCIONISTAS.pdf; ACTA ORDINARIA NRO 28.pdf |

- **28. MOWI** – N2 · PS 5 (S6 = 3: Torres del Paseo, Torre 3 nivel 11) · PF 5 · IMP-0.
- **11. Franede** – N2 · PS 7 · PF 5 · IMP-0. Declarantes S. Caballero (@gvcorp.com.py) y A. Campos [MEF: › Constancia RA 2025.pdf].
- **41. TUIU** – N2 · PS 6 · PF 5 · IMP-0. Fue fundada por ITTI el 28/11/2024.
- **15. Grupo M** – N2 · PS 8 · PF 5 · IMP-0. Su correo SIARA sigue siendo **legales@itti.digital** [MEF: › CONSTANCIA RA 30304.pdf].
- **14. Grupo Hendy** – N2 · PS 8 · PF 6 · IMP-0. Declarante a.pardo08@hotmail.com (A. Campos, declarante de REDIPRO) [MEF].
- **49. V Media** – N2 (decisión expresa) · PS 6 · PF 4 · IMP-0. Presidenta **Liz Raquel Vázquez Benítez**; síndico M. Almada; declarante S. Caballero (@vmedia.com.py) [MEF: › ACTA ORDINARIA NRO 28.pdf; CONSTANCIA RA NRO 13311.pdf].
- *Público:* según un informe del BCP citado por la prensa, **MOWI, Grupo M y Grupo Hendy recibieron ≈US$ 146 M en créditos del banco** después de su salida del grupo, y TUIU, Franede y AIME aparecen entre los receptores de créditos en exceso. Todas tienen cautelas penales [PÚBLICO].
- *Inferencia:* las ventas a directivos, ex socios o personas con el mismo domicilio que el grupo, seguidas de grandes créditos del banco, son compatibles con **testaferrato para eludir los límites de crédito a vinculados** (Ley 861/96 art. 59). No está probado: faltan precio, pago y origen de fondos.
- *Vía laboral:* **IMP-0**. No se conocen trabajadores propios relevantes. Su importancia para los trabajadores es **patrimonial**: si se prueba la simulación, los activos o créditos podrían reintegrarse al grupo o al banco. Esa acción no es del MTESS; corresponde a la Fiscalía, al interventor o a los acreedores. **Recomendación:** pedir sus planillas IPS para descartar que hayan **absorbido personal** del grupo (eso sería sustitución, CT art. 28).

**2. AIME S.A. Corredores de Seguros (RUC 80095816-0)** – N2 · PS 8 · PF 1 · IMP-0
- *Hechos:*
  - Accionistas M. y M. Vargas Wildberger; presidenta G. Villasanti Farinha; director suplente **M. Almada** [MEF: Aime S.A. Corredores de seguros › Constancia RA 2026.pdf].
  - Sede: Torres del Paseo, Torre 3 piso 11. Declarante **A. Campos (@uenoholding.com.py)**, el mismo que REDIPRO.
- *Inferencia:* probable canal de corretaje de los seguros del banco.
- *Vía:* IMP-0. Verificar si empleaba vendedores que operaban en sucursales del banco.

**29. Nubicom Paraguay S.A. (RUC 80155014-9)** – N2 · PS 5 (S4 = 3) · IMP-0. Controlada por Nubicom S.R.L. (99,32 %; dueño no identificado). **Presidente 2025–2026: G. Vázquez Muniagurria** [MEF: Nubicom Paraguay S.A › Escritura Públcia N° 83.pdf]. Declarante A. Campos (correo personal). *Vía:* IMP-0. Pedir los beneficiarios finales de Nubicom S.R.L.

**38. Technoma S.A.E.C.A. (RUC 80060858-5)** – N2 · PS 4 (S6 = 3) · PF 1 · IMP-0
- *Hechos:* accionistas E. Vera y S. Pizurno (compradores de Office Design y MOWI); 51,75 % en acciones propias; sede en Torres del Paseo, Torre 3 [MEF: Technoma SAECA › Registro de Accionistas.pdf; Acta de Asamblea.pdf].
- *Público:* deudora del banco y compradora de bonos de ITTI y GV; tiene cautelas penales [PÚBLICO].
- *Vía:* IMP-0. Contraparte, no empleadora del grupo.

### 4.3 Nivel N3 – Vinculación débil (7 entidades)

- **30. Office Design S.R.L.** – PS 3 · PF 4 · IMP-0. Salió del grupo el 30/10/2025 (ver tabla de §4.2). El domicilio de los nuevos socios es la sede de ITTI [MEF: Office Design S.R.L › Escritura Públcia N° 190.pdf].
- **3. BIC S.A. (RUC 80090066-9)** – PS 2 · IMP-0. Capital atomizado. El grupo suma ≈15 % (Ueno Bank 7,46 %; Ueno Holding, ITTI y REDISA 1,57 % cada una; Vinanzas 1,30 %), sin control [MEF: BIC SA › Registro de accionistas.pdf]. Proveedor o socio del sector, no del grupo.
- **37. Solución Efectiva S.A. (RUC 80082288-9)** – PS 2 · IMP-0. GV 8,1 % (05/2025); control de Achón y Electroban [MEF: Solución Efectiva SA › Constancia RA 2025 Simple.pdf].
- **13. Grupo Berilo S.A. (RUC 80109437-2)** – PS 2 (mismo complejo edilicio) · IMP-0. Controlada por 13 de Agosto S.A. y Sunlit S.A., sin beneficiarios finales identificados [MEF: Grupo Berilo SA › Libro de Registro de Accionistas.pdf]. Ningún documento menciona al grupo.
- **9. Fideicomiso Shopping Costanera (RUC 80105334-0)** – PS 1 · IMP-0. Fideicomitente desarrollador: RADICE S.A. (RUC 80104014-**7**), que sería Terravaz (80104014-**0**). El dígito verificador no coincide: **verificar** [MEF: Fideicomiso Shoping Costanera › contratodefideicomisoshoppingcostanera21….pdf]. Fiduciaria Finexpar/ZBanco.
- **4. CBS S.A. (RUC 80028763-0)** – PS 1 · IMP-0. Tiene el 0,1 % de V Media (comprado a GV el 23/03/2026) y la representa Mauro Vargas [MEF: V MEDIA SA › REGISTRO DE ACCIONISTAS.pdf]. Por lo demás, ningún vínculo en su carpeta.
- **17. GSR E.A.S. (RUC 80131927-7)** – PS 1 · IMP-0. Socio J. A. Sala Cardozo (50 %), comprador del 10 % de MOWI [MEF: GSR E.A.S › Constancia de RA 2026.pdf]. Ningún otro vínculo.

### 4.4 Nivel N4 – Sin vínculo societario acreditado (8 entidades)

- **19. HD Invest E.A.S. Unipersonal** y **27. La Tropa Fletes E.A.S.**
  - *Hecho:* presentaron una "regularización" en SIARA el 16/11/2026, después del inicio del expediente [MEF: HD Invest EAS Unipersonal › Constancia RA 2026 Siara.pdf; La Tropa Fletes EAS › Constancia 2026 SIARA.pdf].
  - **Aclaración:** en esas dos constancias, el nombre que aparece en el campo "Analista" es el del **representante o declarante de la propia empresa**, que cargó el trámite de autogestión. **No es un funcionario del MEF.** No hay base para sostener conflicto de interés ni autoaprobación (`notas_extraccion.md`; verificación del 24/11/2026).
  - *Público:* deudoras del banco (US$ 35 M y US$ 10 M) y con cautelas penales [PÚBLICO].
- **36. SATEC S.A.** – accionista del 0,86 % de BIC [MEF]. Deudora del banco con cautelas penales [PÚBLICO].
- **8. Factopar S.A.** y **25. Kasas Propiedades S.A.E.** – sin vínculo documentado [MEF]. Deudoras o contrapartes y con cautelas penales [PÚBLICO].
- **12. Galadriel S.A.**, **6. Condominio Estancia Don Miguel**, **50. Villa Oliva Rice S.A.** – ningún vínculo con el grupo en sus carpetas [MEF].
- *Vía:* IMP-0. Su relación sería de **deudoras o contrapartes del banco**. En lo laboral solo interesaría si se prueba que **recibieron personal** o pagaban sueldos de trabajadores del grupo (L7).

---

## 5. Conclusiones: existencia y perímetro del conjunto económico

### 5.1 ¿Existe un conjunto o grupo económico?

**Sí, en sentido económico y societario. Los hechos están documentados** [MEF]:

1. **Control común:** una persona física (F. M. Vázquez Villasanti) controla GV con ≈94 % de los votos. GV controla, directa o indirectamente, 25 entidades de la lista. El dato lo confirman **seis constancias de beneficiarios finales** que lo declaran BF por cadena: REDIPRO, REDISA, Kaitel, Tiva, Place Analyzer y Red UTS. La Ley 6446/19 art. 4 ofrece así una **definición legal paraguaya de control** que el propio grupo declaró bajo juramento (art. 5).
2. **Administración común:** un núcleo de unas 15 personas ocupa a la vez cargos en el banco y en las demás sociedades. El caso más claro: **M. Almada es síndico del banco y gerente de Kaitel**, y **C. Impagliatelli es director del banco y gerente de Kaitel**.
3. **Sede común** (Torres del Paseo, Avda. Santa Teresa 1827), **declarantes comunes** (S. Caballero, A. Campos, L. Pane), **dominios comunes** (gvcorp.com.py, uenoholding.com.py, itti.digital) y la **misma escribanía**.
4. **Financiamiento intragrupo**: el banco aportó ≈Gs. 877.000 M en preferidas sin voto a REDIPRO y REDISA, controladas por U Paraguay.
5. **Movimientos previos a la resolución**: la cadena circular de septiembre de 2026, la permuta REDIPRO–ITTI del 02/10/2026 y siete salidas del grupo hacia personas del entorno.

**En sentido laboral, todavía no está acreditado.** La unidad de dirección **del trabajo** (quién daba órdenes, quién pagaba y para quién se trabajaba) no surge de los documentos del MEF. Por eso, con la prueba actual, la conclusión jurídica es que **hay base suficiente para investigar y para que los trabajadores demanden a varias sociedades del grupo**. Pero **no hay base todavía para que el MTESS afirme solidaridad**, que solo puede declarar un juez.

### 5.2 Perímetro propuesto

| Círculo | Entidades | Relevancia laboral |
|---|---|---|
| **1. Núcleo de control** | GV, U Holdings, U Paraguay, ITTI, (WOM77, no incluida), Ueno Holding (absorbida) | Deudores por fusión (GV); destinatarios de cautelas e inoponibilidad (h) |
| **2. Núcleo operativo del banco** | **Ueno Bank, Kaitel, ITTI, REDIPRO, REDISA, IDL** (y posiblemente Tiva, Place Analyzer, Red UTS) | **Aquí están los trabajadores que servían al banco.** Vías IMP-A y IMP-B (Kaitel, ITTI) |
| **3. Financiero regulado** | Ueno Seguros, Casa de Bolsa, AFPI, Vinanzas | Empleadores directos con **capacidad de pago**; verificar personal compartido |
| **4. Diversificación** | Turismo (Kostas, Inter-Express, Intertours, Discover, COMDETUR), Terravaz, 23 Sports, Oniria, Hanoi, Fintux | Empleadores directos; **patrimonio** del grupo |
| **5. Entorno (ex-grupo)** | MOWI, Grupo M, Grupo Hendy, Franede, TUIU, Office Design, V Media, AIME, Technoma, Nubicom | Patrimonial o penal; verificar que no hayan absorbido personal |
| **6. Contrapartes y ajenas** | BIC, Solución Efectiva, Grupo Berilo, Fideicomiso, CBS, GSR, HD Invest, La Tropa, SATEC, Factopar, Kasas, Galadriel, Condominio, Villa Oliva Rice | Sin relevancia laboral directa con la prueba actual |

---

## 6. Casos prioritarios

### 6.1 Kaitel S.R.L. – prioridad máxima

- **Por qué:** es la vía jurídica más sólida (CT art. 25) para unos 1.200 trabajadores [PÚBLICO]. Su empleador formal no tiene patrimonio (capital de Gs. 50 M [MEF]). Su dirección está en manos de autoridades del banco [MEF].
- **Hechos documentados:**
  - Socios WOM77 (98 %) e IDL (2 %).
  - Beneficiario final F. M. Vázquez vía WOM77 → ITTI → GV.
  - Gerentes Impagliatelli (director del banco) y Almada (síndico del banco).
  - Sede en el piso de GV y U Paraguay.
  - Ex socia V. Godoy, hoy compradora de Grupo Hendy.
- **Lo que falta probar:**
  - (i) a quién prestaba servicios cada trabajador (banco, ITTI, REDISA u otras);
  - (ii) en qué locales y con qué sistemas;
  - (iii) quién daba las órdenes y aplicaba sanciones;
  - (iv) si los contratos de trabajo declaraban "por cuenta de" quién se contrataba (art. 25 in fine);
  - (v) el contrato y la facturación Kaitel–banco.
- **Hipótesis de demanda (para orientar a los trabajadores):** Kaitel como intermediaria, solidariamente con el **beneficiario real** (Ueno Bank en resolución: crédito a verificar en la liquidación; o ITTI o REDISA, si eran las beneficiarias). Además, inoponibilidad respecto de WOM77, ITTI y GV si se prueba que Kaitel era una sociedad "satélite" (TApel. Trab. 2.ª Sala, Ac. y Sent. 133/2012, citado en el marco §3.3).
- **WOM77 S.A. (RUC 80110878-0) no está entre las 51:** hay que **pedir su documentación al MEF** (accionistas, autoridades y beneficiarios finales).

### 6.2 ITTI S.A.E.

- Unos 1.600 trabajadores [PÚBLICO]. Es controlante (vía WOM77) de Kaitel y la sociedad con más participadas.
- Desde el 02/10/2026 **el banco es su accionista (16,95 %)**, lo que la vincula directamente con la masa de la resolución.
- **Hipótesis:** empleador real o coempleador junto con el banco del personal tecnológico asignado al banco (IMP-A), o contratista sin autonomía (IMP-B).
- **Prioridad probatoria:** contrato de servicios ITTI–banco, facturación (DNIT), nómina por proyecto o cliente, credenciales y correos (@ueno.com.py frente a @itti.digital).
- **Riesgo:** el registro de ITTI tiene inconsistencias de capital (401.201 frente a 250.000 acciones) [MEF], y la sociedad tiene cautelas penales [PÚBLICO]. Las acciones laborales deben coordinarse con esas medidas.

### 6.3 REDIPRO y REDISA

- **Hechos:**
  - Preferidas del banco por Gs. 640.468 M (REDIPRO) y Gs. 236.230 M (REDISA) [MEF].
  - **Entre el 09/09 y el 02/10/2026 el banco transfirió 263.339 preferidas de REDIPRO a U Paraguay**: 180.646 por la cadena Ueno Bank → Red Digital → ITTI → GV → U Paraguay (cuatro pasos el 25/09) y el resto por ventas y cesiones directas, incluidas 68.000 el 02/10, el mismo día en que el banco recibió 68.000 acciones de ITTI [MEF].
  - En ambas sociedades la declaración de beneficiarios finales de 2026 está pendiente [MEF].
- **Relevancia laboral:**
  - (i) Son **empleadoras de la red de pagos** ("wepa" [PÚBLICO]); hay que verificar su personal propio y si usaban personal de Kaitel.
  - (ii) Tienen **patrimonio**: es dinero del banco, y si sigue allí es la principal reserva de valor fuera de la resolución [INFERENCIA].
  - (iii) La operatoria es la base fáctica más fuerte para una **inoponibilidad o fraude (IMP-D)** si los trabajadores demandan al grupo.
- **Medida sugerida:** que el MTESS informe estos hechos al interventor y a la Superintendencia de Bancos, y que se considere la **revocación o ineficacia** de las transferencias del período sospechoso. Eso es competencia del BCP o del juez de la liquidación (Ley 2334/03 art. 16.4). Los trabajadores pueden pedir **cautelas** sobre las acciones y la caja de REDIPRO, REDISA y U Paraguay en sus demandas.

### 6.4 U Paraguay S.A.

Es la holding del núcleo financiero y **receptora de las preferidas** salidas del banco. Tiene contradicciones documentales sobre su control en 2025 [MEF]. No se le conocen empleados. **Objetivo de cautela patrimonial.** Pedir sus estados financieros y el detalle de los pagos (si los hubo) por las preferidas.

### 6.5 Grupo Vázquez S.A.E.

- **Hecho firme:** es **sucesora por fusión de Ueno Holding** (Esc. 131/2025). Los ex trabajadores de Ueno Holding o Credicentro pueden reclamarle directamente.
- Es controlante última y vendedora en las siete salidas del grupo.
- **Pedir:** balances de fusión, nómina transferida desde Ueno Holding, estados financieros 2024–2026 y libro de actas.

### 6.6 Transferencias 2025–2026 a personas vinculadas

- Siete salidas documentadas (§4.2). **Hechos:** fechas, vendedores, compradores, y que los compradores tienen roles en el grupo o declaran el mismo domicilio [MEF].
- **Inferencia:** posible testaferrato para recibir crédito del banco por encima de los límites [PÚBLICO e INFERENCIA].
- **Relevancia laboral indirecta:** (i) descartar que hayan **absorbido personal** (pedir planillas IPS de 2025–2026); (ii) si absorbieron una unidad productiva del grupo, corresponde **sustitución de empleador** (CT art. 28: solidaridad del sustituido por seis meses); (iii) como **patrimonio desplazado**, su recuperación es materia penal y de la resolución. El MTESS debe **comunicar a la Fiscalía** que existen créditos laborales que podrían verse afectados, para que los tenga en cuenta al administrar los bienes cautelados [NV: mecanismo procesal de participación de acreedores laborales en la causa penal, a verificar].
- **Intertours** (compra del 30 % adicional el 22/07/2026) y **Terravaz** (adquirida en 06/2025) son movimientos **de entrada**. Muestran que el grupo seguía invirtiendo en sociedades no bancarias poco antes de la crisis.

---

## 7. Recomendaciones concretas al MTESS

### 7.1 Pedidos de información (inmediatos)

| # | Destinatario | Qué pedir | Entidades | Indicador |
|---|---|---|---|---|
| 1 | **IPS** | Nómina de asegurados (altas y bajas) por RUC patronal de 01/2023 a la fecha; estado de cuenta patronal y mora; trabajadores que figuren en más de una de las entidades | Ueno Bank, Kaitel, **WOM77**, ITTI, REDIPRO, REDISA, IDL, Tiva, Place Analyzer, Red UTS, Ueno Seguros, Casa de Bolsa, AFPI, Vinanzas, U Paraguay, GV y las 7 sociedades salidas del grupo | L3, L6 |
| 2 | **MTESS (registros propios)** | Planillas de empleados, sueldos y jornales presentadas; reglamentos internos; comunicaciones de suspensión o cierre; denuncias | Las mismas | L3, L4, L6 |
| 3 | **Interventor de Ueno Bank / Superintendencia de Bancos** | Nómina al 02/11/2026; **determinación de beneficios sociales (Ley 2334/03 art. 17)**; trabajadores transferidos y adquirentes (art. 26); **contratos y facturación con Kaitel, ITTI, REDIPRO, REDISA, IDL, Ueno Seguros, AIME y 23 Sports**; saldos adeudados a esas sociedades; listado de personas vinculadas (Ley 861/96 arts. 46–47); créditos a MOWI, Grupo M, Grupo Hendy, TUIU, Franede, AIME, HD Invest, La Tropa, SATEC, Technoma, Factopar y Kasas; documentación de las preferidas de REDIPRO y REDISA y de su transferencia | Ueno Bank | L1, L2, F1, F2 |
| 4 | **MEF – DGPEJBF** | Documentación completa de **WOM77 S.A. (RUC 80110878-0)**, **Nubicom S.R.L.**, **IOIO S.A.E.C.A.**, **Markhel S.A.**, **Match S.A.**, **Business & Financial Group S.A.**, **13 de Agosto S.A.**, **Sunlit S.A.** y **Sky Link S.A.**; estado de las declaraciones de beneficiarios finales pendientes (REDIPRO, REDISA, 23 Sports); declaraciones de beneficiarios finales de Ueno Bank, GV, ITTI y U Paraguay | — | S2, S3 |
| 5 | **DNIT** | Facturas electrónicas emitidas entre las entidades del grupo y al banco (2023–2026); declaraciones de IRE con operaciones entre vinculadas; actividad económica declarada | Núcleo operativo y financiero | L1, L2, F1 |
| 6 | **Superintendencia de Valores (BCP)** | Estados financieros y notas de partes relacionadas de las emisoras (ITTI, GV, Terravaz, Technoma, Ueno Holding hasta su absorción) y de la Casa de Bolsa y la AFPI; prospectos de bonos de ITTI y GV | Emisoras | F1, S |
| 7 | **Superintendencia de Seguros (BCP)** | Contratos de bancaseguros entre Ueno Seguros, el banco y AIME; operaciones con vinculadas | Ueno Seguros, AIME | L1 |
| 8 | **Dirección General de Registros Públicos** | Inscripción de la fusión GV–Ueno Holding; poderes vigentes de Kaitel, ITTI y GV; inmuebles de GV, Terravaz, ITTI y U Paraguay | — | F, capacidad de pago |

### 7.2 Inspecciones (Ley 5115/13 arts. 17–18)

Orden sugerido:
1. **Kaitel** (Torre 2 piso 25) y **los lugares donde trabajaba su personal**: sucursales y centros de atención del banco, ITTI y REDISA.
2. **ITTI** (Torre 3 piso 11).
3. **REDISA y REDIPRO**.
4. **IDL**.

**Constatar en acta:**
- quién usa los servicios de cada trabajador;
- credenciales y correos;
- equipos y sistemas (¿son del banco?);
- jefes directos y su empleador;
- registros de asistencia;
- recibos de sueldo (quién paga);
- contratos de trabajo (cláusula del art. 25).

**Si se resiste la inspección:** pedir el acceso al Juez del Trabajo (art. 18).

### 7.3 Mediaciones (Ley 5115/13 art. 4 núm. 10 y art. 15 núm. 7)

- **Mesa 1 – Kaitel:** citar a Kaitel, WOM77, IDL, ITTI y GV, y al **interventor** de Ueno Bank como beneficiario de los servicios. **La comparecencia del empleador a la primera citación es obligatoria.** Objetivo: reconocimiento de antigüedad, liquidación y cronograma de pago. Si ITTI o GV no asumen, dejar constancia de los hechos admitidos o negados (sirve como prueba).
- **Mesa 2 – ITTI:** ITTI y GV, con el interventor.
- **Mesa 3 – Ueno Bank:** el interventor. Objetivos: el art. 17, liquidaciones y las condiciones de las transferencias a adquirentes (art. 26), sin renuncias (CT art. 3).
- **Mesa 4 – REDISA y REDIPRO**, con U Paraguay.
- En todas: **advertir por escrito** que son nulas las renuncias y los finiquitos por debajo de los mínimos legales (CT art. 3).

### 7.4 Medidas cautelares a sugerir a los trabajadores (y comunicaciones a la Fiscalía)

El MTESS no traba cautelas: las piden los trabajadores, por sus abogados, al **juez laboral** al demandar, según las normas procesales aplicables (arts. no verificados en este documento). Tampoco se verificó si existe en Paraguay un "Ministerio Público del Trabajo" como órgano autónomo. Si existe, cabe la misma comunicación que a la Fiscalía.

**Sugerencias, por orden de utilidad:**
1. **Embargo preventivo o inhibición** sobre **REDISA, REDIPRO y U Paraguay** (acciones preferidas, cuentas, créditos), en demandas que invoquen intermediación (Kaitel) o inoponibilidad. *Fundamento fáctico:* hechos MEF de §6.3.
2. **Inhibición general de vender y gravar** respecto de **GV** (sucesora de Ueno Holding; controlante) y de **ITTI**.
3. **Embargo o anotación de litis** sobre los inmuebles de **Terravaz** y las participaciones de GV en **23 Sports, Oniria y Terravaz**.
4. **Contra Ueno Bank no proceden cautelas** durante la resolución (Ley 2334/03 art. 25). La vía es la **verificación del crédito** (art. 17) y la **preferencia del art. 26** en la liquidación del residual.
5. **Coordinación con las cautelas penales:** varias de estas sociedades ya tienen prohibición de vender y gravar e inmovilización de cuentas en sede penal [PÚBLICO]. **Las cautelas penales no protegen a los acreedores laborales.** Conviene que el MTESS **informe a la Fiscalía y al juzgado penal** el universo de créditos laborales, para que se considere al disponer de los bienes [NV: vía procesal a verificar].

### 7.5 Otras medidas

- **Censo de afectados** (marco §9.1). Registrar en el SIME, para cada trabajador: empleador formal, beneficiario real, lugar de trabajo, jefe, correo, antigüedad, salario y aportes IPS.
- **Alerta de prescripción:** los plazos laborales son breves (CT arts. 399–400, a verificar). La interrupción del art. 16.1 de la Ley 2334/03 solo alcanza a los juicios ya iniciados.
- **E.A.S.:** Fintux, GSR, HD Invest y La Tropa son E.A.S. Por la Ley 6480/20 art. 4, **sus socios no responden por deudas laborales**. Las acciones deben dirigirse contra la sociedad o fundarse en fraude.
- **Nada de lo anterior debe comunicarse como imputación de delitos.** Hay que distinguir siempre hecho documentado de inferencia (ver "Cómo leer este documento").

---

## 8. Modelo de requerimiento de información

> **MINISTERIO DE TRABAJO, EMPLEO Y SEGURIDAD SOCIAL**
> Viceministerio de Trabajo – Dirección General de Inspección y Fiscalización de Trabajo y Seguridad Social
>
> Asunción, ___ de __________ de 2026
>
> **Nota MTESS N° ____/2026**
> **Ref.:** Expediente SIME N° 78.318/2026 – Requerimiento de información
>
> Señor/a Representante Legal de **[RAZÓN SOCIAL]** (RUC **[N°]**)
> Domicilio: **[domicilio declarado ante el MEF]**
>
> Me dirijo a usted, en el marco del expediente de la referencia y en ejercicio de las atribuciones de este Ministerio como Autoridad Administrativa del Trabajo y policía laboral (Ley N° 5115/2013, arts. 2, 4 núm. 11, 17 y 18; Código del Trabajo, Ley N° 213/1993), a fin de requerirle que, **dentro del plazo de cinco (5) días hábiles** desde la recepción de la presente, remita a esta Dirección la siguiente información y documentación, en copia autenticada o certificada por el representante legal y, cuando corresponda, en formato digital editable:
>
> 1. **Nómina del personal** dependiente, vigente y egresado desde el 1° de enero de 2023, con: nombre, cédula de identidad, fecha de ingreso y egreso, cargo, salario, **lugar físico de prestación de servicios**, **jefe inmediato (nombre y empresa empleadora del jefe)**, correo electrónico corporativo asignado y número patronal IPS bajo el cual fue inscripto.
> 2. **Contratos de trabajo** y sus modificaciones, de una muestra o de la totalidad según se indique, y planillas de sueldos y jornales presentadas ante este Ministerio.
> 3. **Contratos de prestación de servicios, provisión de personal, tecnología, procesamiento, cobranza, corresponsalía, logística, publicidad o cualquier otro** celebrados con UENO BANK S.A. o con cualquiera de las sociedades enumeradas en el Anexo, y la **facturación** emitida y recibida en virtud de ellos (2023 a la fecha).
> 4. **Organigrama** de la empresa y, en su caso, del grupo al que pertenece, con indicación de las áreas que prestan servicios a otras sociedades.
> 5. **Reglamento interno**, políticas de recursos humanos y documentos que acrediten qué persona o sociedad ejerce la dirección, el control de asistencia y el poder disciplinario sobre el personal.
> 6. **Constancias de pago de aportes al IPS** de los últimos doce (12) meses y detalle de los aportes pendientes.
> 7. **Estados financieros** de los ejercicios 2023, 2024 y 2025 y balance parcial a la fecha, con sus notas sobre operaciones con partes relacionadas.
> 8. **Libro de registro de accionistas o de cuotas** actualizado, y documentación de toda transferencia de acciones, cuotas o participaciones realizada desde el 1° de enero de 2025 (precio, forma de pago, comprobantes).
> 9. Toda comunicación cursada a sus trabajadores con motivo del procedimiento de resolución de UENO BANK S.A. (suspensiones, despidos, traslados, renuncias, finiquitos).
>
> La información se requiere a fin de determinar con precisión al empleador o empleadores de los trabajadores afectados y de resguardar sus derechos laborales y de seguridad social. Será utilizada exclusivamente para esos fines, con la reserva que corresponda a los datos personales.
>
> Se hace saber que la falta de respuesta, la respuesta incompleta o la obstrucción podrán dar lugar a la verificación in situ y a las medidas que prevé la legislación vigente, incluida la solicitud de acceso ante el Juzgado del Trabajo (Ley N° 5115/2013, art. 18), sin perjuicio de las sanciones administrativas que correspondan.
>
> Atentamente,
> **[Firma – Director/a]**
>
> **Anexo – Sociedades relacionadas (a efectos del punto 3):** Ueno Bank S.A.; U Paraguay S.A.; Grupo Vázquez S.A.E.; ITTI S.A.E.; WOM77 S.A.; Kaitel S.R.L.; Impresión Distribución y Logística S.A.; Red Digital S.A.; Red Digital de Procesamiento S.A.; Ueno Seguros S.A.; Ueno Casa de Bolsa S.A.; Ueno AFPI S.A.; Vinanzas S.A.; Tiva S.A.; Place Analyzer S.A.; Red UTS Paraguay S.A.; AIME S.A. Corredores de Seguros; y las demás que el MTESS indique.

*Variantes:* para el **interventor de Ueno Bank**, agregar el pedido de la determinación del art. 17 de la Ley 2334/03, la nómina al 02/11/2026, el listado de transferidos y adquirentes (art. 26) y los saldos con proveedores del grupo. Para el **IPS** y la **DNIT**, usar nota de cooperación interinstitucional con el listado de RUC de §7.1.

---

## 9. Limitaciones

1. **No es un dictamen vinculante.** Las etiquetas IMP son hipótesis de trabajo. Las calificaciones de empleador real, solidaridad o inoponibilidad corresponden a la justicia.
2. **El plano laboral está casi vacío.** No hay en la documentación del MEF planillas, contratos de trabajo, contratos intragrupo ni facturación. Las puntuaciones L son mínimas o "s/d". **El PL bajo refleja falta de prueba, no ausencia de vínculo.**
3. **Datos societarios con inconsistencias** [MEF]:
   - control de U Paraguay en 2025 (actas frente a registros);
   - capital de ITTI (401.201 frente a 250.000 acciones);
   - porcentajes de Kaitel (99/1 frente a 98/2);
   - CI de F. M. Vázquez (2.941.546 frente a 2.491.546);
   - RUC de RADICE frente a Terravaz (dígito verificador);
   - registros manuscritos de GV.
4. **Cifras de prensa** (≈7.000 afectados; 490, 1.600 y 1.200 trabajadores; montos de crédito y cautelas): **no verificadas**. Deben confirmarse con el propio MTESS, el IPS, el BCP y la Fiscalía.
5. **Sociedades no incluidas en las 51** que son relevantes: **WOM77 S.A.**, IOIO, Markhel, Match, Business & Financial Group, Nubicom S.R.L., 13 de Agosto, Sunlit, Sky Link y sociedades del exterior.
6. **Puntuación con criterio del analista** dentro de las reglas del §2. Otra persona podría asignar ±1 en algunos indicadores. Las dos decisiones expresas de nivel (V Media, Fintux) están señaladas.
7. **Normas no verificadas** señaladas en el marco (prescripción, privilegio en el CT, art. 237 de la Ley 154/69, normas procesales de cautelas, vía de participación de acreedores laborales en la causa penal).
8. **Datos personales:** el documento contiene nombres y CI de personas físicas tomados de registros públicos administrativos. Su uso debe limitarse a la finalidad laboral de la Nota MTESS 656/2026.
