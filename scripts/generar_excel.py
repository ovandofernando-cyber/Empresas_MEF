"""Genera fichas/fichas_empresas.xlsx: índice, matriz laboral y una hoja por entidad.

Uso: python3 scripts/generar_excel.py [salida.xlsx]
Lee datos/empresas_base.csv y datos/consolidado/*.csv.
"""
import csv
import os
import re
import sys

from openpyxl import Workbook
from openpyxl.styles import Alignment, Font, PatternFill, Border, Side
from openpyxl.utils import get_column_letter

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CONS = os.path.join(RAIZ, "datos", "consolidado")
ARGS = [a for a in sys.argv[1:] if not a.startswith("--")]
# --sin-laboral: versión solo societaria, sin matriz laboral, niveles ni imputaciones jurídicas
LABORAL = "--sin-laboral" not in sys.argv
_defecto = "fichas_empresas.xlsx" if LABORAL else "fichas_empresas_societario.xlsx"
SALIDA = ARGS[0] if ARGS else os.path.join(RAIZ, "fichas", _defecto)

AZUL = PatternFill("solid", fgColor="1F4E78")
GRIS = PatternFill("solid", fgColor="D9E1F2")
CLARO = PatternFill("solid", fgColor="F2F2F2")
BLANCO_B = Font(bold=True, color="FFFFFF")
NEGRITA = Font(bold=True)
TITULO = Font(bold=True, size=14, color="1F4E78")
BORDE = Border(*(Side(style="thin", color="BFBFBF"),) * 4)
AJUSTE = Alignment(wrap_text=True, vertical="top")


def leer(nombre):
    ruta = os.path.join(CONS, nombre + ".csv")
    with open(ruta, encoding="utf-8") as f:
        return list(csv.DictReader(f))


def por_empresa(filas, clave="empresa_id"):
    d = {}
    for r in filas:
        d.setdefault(r.get(clave, ""), []).append(r)
    return d


def num(v):
    if v in (None, ""):
        return None
    try:
        x = float(v)
        return int(x) if x.is_integer() else x
    except ValueError:
        return v


with open(os.path.join(RAIZ, "datos", "empresas_base.csv"), encoding="utf-8") as f:
    BASE = list(csv.DictReader(f))
EMP = {r["id"]: r for r in leer("empresas")}
MAT = {r["id"]: r for r in leer("matriz_laboral")}
CTRL = {r["entidad_id"]: r for r in leer("control_indirecto") if r["corte"] == "vigente"}
PART = por_empresa(leer("participaciones"))
AUT = por_empresa(leer("autoridades"))
BF = por_empresa(leer("beneficiarios_finales"))
HIST = por_empresa(leer("historial"))
DECL = por_empresa(leer("declarantes_contactos"))
CAL = por_empresa(leer("calidad_datos"))
VINC = {}
for v in leer("vinculos"):
    for lado in ("origen", "destino"):
        VINC.setdefault(v[lado], []).append(v)

AGR = {}
for a in leer("participaciones_agregadas"):
    if a["corte"] == "vigente":
        AGR.setdefault(a["empresa_id"], []).append(a)
SEGMENTOS = {
    "nucleo_financiero_ueno": "Núcleo financiero Ueno",
    "holding_controlante": "Holding / controlante",
    "controlada_itti_gv": "Controlada por ITTI / Grupo Vázquez",
    "participada_minoritaria_o_vinculo_indirecto": "Participada minoritaria o vínculo indirecto",
    "ex_vinculada": "Ex vinculada (salió del grupo 2025-2026)",
    "sin_vinculo_detectado": "Sin vínculo detectado",
}


def seg(v):
    return SEGMENTOS.get(v, v)


def sino(v):
    return {"1": "Sí", "0": "No", "True": "Sí", "False": "No"}.get(str(v), v)


INTERPRETATIVO = re.compile(r"testaferr|fiduciario del grupo|empleador|laboral|fraude|interposici|solidari|vaciamiento|imputa|indicio de que sigue", re.I)

NIVELES = {"N1": "Control común", "N2": "Vínculo relevante", "N3": "Vínculo débil", "N4": "Sin vínculo documentado"}

# Nombres de hoja únicos (máx. 31 caracteres, sin caracteres prohibidos)
HOJA = {}
usados = set()
for r in BASE:
    n = re.sub(r"[\[\]\*\?/\\:]", "", f"{int(r['nro']):02d} {r['razon_social']}")[:31].strip()
    while n in usados:
        n = n[:29] + "_" + str(len(usados))
    usados.add(n)
    HOJA[r["id"]] = n


def anchos(ws, cols):
    for i, w in enumerate(cols, 1):
        ws.column_dimensions[get_column_letter(i)].width = w


def encabezado(ws, fila, titulos):
    for j, t in enumerate(titulos, 1):
        c = ws.cell(fila, j, t)
        c.fill, c.font, c.border, c.alignment = AZUL, BLANCO_B, BORDE, AJUSTE
    return fila + 1


def seccion(ws, fila, texto, ncols):
    ws.cell(fila, 1, texto).font = Font(bold=True, size=12, color="1F4E78")
    for j in range(1, ncols + 1):
        ws.cell(fila, j).fill = GRIS
    return fila + 1


def tabla(ws, fila, titulos, filas, ncols, vacio="Sin datos en la documentación remitida."):
    fila = encabezado(ws, fila, titulos)
    if not filas:
        ws.cell(fila, 1, vacio).font = Font(italic=True, color="7F7F7F")
        return fila + 2
    for valores, resaltar in filas:
        for j, v in enumerate(valores, 1):
            c = ws.cell(fila, j, v)
            c.border, c.alignment = BORDE, AJUSTE
            if resaltar:
                c.fill = CLARO
        fila += 1
    return fila + 1


def fuente(r):
    a, p = r.get("fuente_archivo", ""), r.get("fuente_pagina", "")
    return f"{a} p.{p}" if a and p else a


def es_vigente(r):
    return str(r.get("vigente", "")).lower() in ("true", "1", "sí", "si")


wb = Workbook()

# ---------- Índice ----------
ws = wb.active
ws.title = "Índice"
ws["A1"] = "Fichas de las 51 entidades remitidas por el MEF (Informe CRA N° 385/2026, SIME 78.318/2026)"
ws["A1"].font = TITULO
ws["A2"] = ("Fuente: Registro Administrativo de Personas y Estructuras Jurídicas y de Beneficiarios Finales (MEF). "
            "Datos de declaraciones juradas, registros manuscritos y OCR: cotejar con los originales antes de usarlos como prueba. "
            "Haga clic en el nombre para ir a la hoja de cada entidad.")
ws["A2"].alignment = AJUSTE
ws.merge_cells("A2:J2")
ws.row_dimensions[2].height = 45
tit = ["N°", "Razón social", "RUC", "Segmento", "Controlante directo", "Controlante último",
       "% integrado del grupo", "Nivel de vínculo (laboral)", "Imputación (hipótesis)", "Presidente / representante actual"]
if not LABORAL:
    tit = tit[:7] + tit[9:]
f = encabezado(ws, 4, tit)
for r in BASE:
    e, m, c = EMP.get(r["id"], {}), MAT.get(r["id"], {}), CTRL.get(r["id"], {})
    nivel = m.get("nivel", "")
    vals = [int(r["nro"]), r["razon_social"], r["ruc"] or "sin RUC", seg(e.get("segmento", "")),
            e.get("controlante_directo", "") or c.get("controlante_directo", ""),
            e.get("controlante_ultimo", "") or c.get("controlante_ultimo", ""),
            num(e.get("pct_integrado_grupo", "")),
            f"{nivel} – {NIVELES.get(nivel, '')}" if nivel else "", m.get("imputacion", ""),
            e.get("presidente_actual", "")]
    if not LABORAL:
        vals = vals[:7] + vals[9:]
    for j, v in enumerate(vals, 1):
        cell = ws.cell(f, j, v)
        cell.border, cell.alignment = BORDE, AJUSTE
    link = ws.cell(f, 2)
    link.hyperlink = f"#'{HOJA[r['id']]}'!A1"
    link.font = Font(color="0563C1", underline="single")
    f += 1
anchos(ws, [5, 42, 13, 26, 30, 30, 12, 26, 18, 34] if LABORAL else [5, 42, 13, 30, 30, 30, 12, 40])
ws.freeze_panes = "C5"
ws.auto_filter.ref = f"A4:{'J' if LABORAL else 'H'}{f - 1}"


# ---------- Diccionario de variables ----------
wd = wb.create_sheet("Diccionario", 1)
wd["A1"] = "Diccionario de variables"
wd["A1"].font = TITULO
wd["A3"] = "Columnas de la hoja Índice"
wd["A3"].font = Font(bold=True, size=12, color="1F4E78")
DIC = [
    ("N°", "Número de orden de la entidad en el listado del Informe CRA N° 385/2026 del MEF.", "1 a 51", "Informe CRA 385/2026"),
    ("Razón social", "Denominación de la entidad tal como figura en el Informe CRA 385/2026. Es un enlace a la hoja de la entidad. La denominación actual o las anteriores pueden diferir (ver la hoja de cada entidad).", "Texto", "Informe CRA 385/2026"),
    ("RUC", "Registro Único del Contribuyente con dígito verificador. U Holdings S.à r.l. (Luxemburgo) no tiene RUC ni está registrada en el SIARA.", "80000000-0 o «sin RUC»", "Informe CRA 385/2026, constancias RA"),
    ("Segmento", "Clasificación de la entidad según su posición respecto del grupo, asignada por el equipo de datos a partir de la composición accionaria vigente y la historia societaria.", "Ver tabla de valores de Segmento", "Elaboración propia (datos/consolidado/empresas.csv)"),
    ("Controlante directo", "Accionista o socio que tiene la mayoría de los votos de la entidad (o, si nadie la tiene, el mayor titular) según el dato vigente más reciente.", "Nombre de persona física o jurídica", "Registros de accionistas, actas, constancias RA"),
    ("Controlante último", "Persona en la cima de la cadena de control, recorriendo los controlantes directos hacia arriba hasta llegar a una persona física o a una entidad cuyos dueños no constan.", "Nombre de persona física o jurídica", "Cálculo propio sobre participaciones y constancias de beneficiarios finales"),
    ("% integrado del grupo", "Porcentaje del capital de la entidad que pertenece, directa o indirectamente, al grupo. Se multiplican los porcentajes de capital a lo largo de cada cadena (por ejemplo, 97,99 % de U Paraguay × 93,08 % de Ueno Bank) y se suman todas las cadenas que llegan desde U Holdings S.à r.l., Grupo Vázquez S.A.E. y Federico M. Vázquez Villasanti. Mide capital, no votos: puede ser bajo aunque el grupo controle por votos (acciones de voto múltiple). Supone que U Holdings y Grupo Vázquez responden al mismo controlante, lo que surge de una declaración de beneficiarios finales pendiente de aprobación.", "0 a 100; vacío = sin participación del grupo o sin datos", "Cálculo propio (datos/consolidado/control_indirecto.csv)"),
    ("Nivel de vínculo (laboral)", "Intensidad del vínculo de la entidad con el grupo según la matriz de indicadores del análisis laboral (hoja Matriz laboral).", "N1 a N4; ver tabla de valores", "analisis/analisis_laboral.md"),
    ("Imputación (hipótesis)", "Vía jurídica por la cual podría extenderse a la entidad la responsabilidad laboral. Son hipótesis de trabajo (h) a confirmar con prueba laboral (planillas IPS, contratos, inspección); solo un juez puede declarar la solidaridad.", "REF, IMP-A a IMP-E, IMP-0; ver tabla de valores", "analisis/analisis_laboral.md"),
    ("Presidente / representante actual", "Presidente del directorio, gerente o representante legal según el documento más reciente (acta, constancia RA o escritura).", "Nombre (cargo)", "Actas, constancias RA"),
]
if not LABORAL:
    DIC = [d for d in DIC if d[0] not in ("Nivel de vínculo (laboral)", "Imputación (hipótesis)")]
f = encabezado(wd, 4, ["Variable", "Definición", "Valores posibles", "Fuente"])
for fila_d in DIC:
    for j, v in enumerate(fila_d, 1):
        c = wd.cell(f, j, v)
        c.border, c.alignment = BORDE, AJUSTE
    wd.cell(f, 1).font = NEGRITA
    f += 1

def tabla_valores(f, titulo, filas):
    wd.cell(f, 1, titulo).font = Font(bold=True, size=12, color="1F4E78")
    f = encabezado(wd, f + 1, ["Valor", "Significado", "Cantidad de entidades", ""])
    for v, d, n in filas:
        for j, x in enumerate((v, d, n), 1):
            c = wd.cell(f, j, x)
            c.border, c.alignment = BORDE, AJUSTE
        wd.cell(f, 1).font = NEGRITA
        f += 1
    return f + 1

from collections import Counter
cs = Counter(seg(e.get("segmento", "")) for e in EMP.values())
f = tabla_valores(f + 1, "Valores de Segmento", [
    ("Núcleo financiero Ueno", "Entidades financieras, de seguros, de valores o de pagos con la marca Ueno o controladas por U Paraguay (Ueno Bank, Ueno Seguros, Ueno Casa de Bolsa, Ueno AFPI, Red Digital, Redipro).", cs.get("Núcleo financiero Ueno", 0)),
    ("Holding / controlante", "Sociedades cuya función es tener acciones de otras del grupo (U Holdings S.à r.l., U Paraguay, Grupo Vázquez, ITTI, Ueno Holding absorbida en 2025).", cs.get("Holding / controlante", 0)),
    ("Controlada por ITTI / Grupo Vázquez", "Sociedades operativas en las que ITTI o Grupo Vázquez tienen el control (mayoría de votos o control declarado).", cs.get("Controlada por ITTI / Grupo Vázquez", 0)),
    ("Participada minoritaria o vínculo indirecto", "El grupo tiene una participación sin control, o el vínculo es indirecto (directores, declarantes o socios en común, o la entidad es socia de otra del grupo).", cs.get("Participada minoritaria o vínculo indirecto", 0)),
    ("Ex vinculada (salió del grupo 2025-2026)", "Fue del grupo y en 2025-2026 sus acciones pasaron a personas físicas, varias del entorno del grupo. Ver hoja de la entidad para fecha y comprador.", cs.get("Ex vinculada (salió del grupo 2025-2026)", 0)),
    ("Sin vínculo detectado", "La documentación del MEF no muestra participación, directores ni declarantes comunes con el grupo. Puede ser contraparte comercial o deudora del banco.", cs.get("Sin vínculo detectado", 0)),
])
if LABORAL:
    cn = Counter(m.get("nivel", "") for m in MAT.values())
    f = tabla_valores(f, "Valores de Nivel de vínculo (laboral)", [
        ("N1 – Control común", "Participación o control del grupo, directo o por cadena (S1 o S2 ≥ 2), y además beneficiario final o directores comunes (S3 o S4 ≥ 2).", cn.get("N1", 0)),
        ("N2 – Vínculo relevante", "Puntaje societario PS ≥ 6, o algún indicador societario con puntaje 3, sin llegar a N1.", cn.get("N2", 0)),
        ("N3 – Vínculo débil", "Puntaje societario entre 1 y 5.", cn.get("N3", 0)),
        ("N4 – Sin vínculo documentado", "Ningún indicador societario con puntaje mayor a 0.", cn.get("N4", 0)),
    ])
    f = tabla_valores(f, "Valores de Imputación (hipótesis)", [
        ("REF", "Entidad de referencia: Ueno Bank, empleador formal en resolución (Ley 2334/03).", ""),
        ("IMP-A", "Empleador real o coempleador: la entidad utiliza los servicios de trabajadores registrados por otra (Código del Trabajo arts. 19, 22, 24 y 48).", ""),
        ("IMP-B", "Intermediación o contratista sin autonomía: responde solidariamente con el empleador (CT arts. 25 y 26).", ""),
        ("IMP-C", "Sustitución o sucesión de empleador, por ejemplo por absorción (CT art. 28).", ""),
        ("IMP-D", "Inoponibilidad de la personalidad jurídica por fraude o abuso (Código Civil art. 372 y jurisprudencia).", ""),
        ("IMP-E", "Seguridad social: el patrón principal responde ante el IPS por sus contratistas (Decreto-Ley 1860/50 art. 70).", ""),
        ("IMP-0", "Sin base de imputación con la información actual.", ""),
        ("(h)", "Sufijo que indica hipótesis no acreditada todavía con prueba laboral.", ""),
    ])

    wd.cell(f, 1, "Indicadores de la hoja Matriz laboral (escala 0 a 3; s/d = sin datos)").font = Font(bold=True, size=12, color="1F4E78")
    IND = [
        ("S1", "Participación directa de una sociedad del núcleo de control (GV, U Holdings, U Paraguay, ITTI, Ueno Bank, Ueno Holding, WOM77)."),
        ("S2", "Participación o control indirecto, por cadena de sociedades o personas del grupo."),
        ("S3", "Beneficiario final común con el grupo."),
        ("S4", "Directores, síndicos, representantes o apoderados comunes."),
        ("S5", "Mismo declarante ante el MEF, mismo correo, dominio o teléfono."),
        ("S6", "Mismo domicilio (por ejemplo Torres del Paseo, Avda. Santa Teresa 1827)."),
        ("S7", "Marca común (ueno) o presentación pública como parte del grupo."),
        ("L1", "Presta servicios al banco u otras del grupo en actividades conexas."),
        ("L2", "Dependencia económica: proporción de ingresos que vienen del grupo."),
        ("L3", "Trabajadores compartidos o que rotan entre sociedades del grupo."),
        ("L4", "Dirección y poder disciplinario común."),
        ("L5", "Infraestructura común (locales, sistemas, credenciales)."),
        ("L6", "El empleador registrado en IPS o planilla no coincide con quien usa los servicios."),
        ("L7", "Salarios o beneficios pagados por una sociedad distinta del empleador formal."),
        ("L8", "Contratista sin autonomía: sin riesgo, medios ni clientes propios."),
        ("F1", "Caja común o confusión patrimonial."),
        ("F2", "Movimientos de activos, personal o contratos previos a la resolución."),
        ("F3", "Cambios societarios recientes cercanos a la crisis."),
        ("F4", "Subcapitalización o sociedad «satélite»."),
        ("PS / PL / PF", "Suma de los puntajes societarios (S), laborales (L) y de fraude (F)."),
        ("n_sd", "Cantidad de indicadores sin datos."),
    ]
    f = encabezado(wd, f + 1, ["Indicador", "Qué mide", "", ""])
    for k, d in IND:
        wd.cell(f, 1, k).font = NEGRITA
        c = wd.cell(f, 2, d)
        c.alignment = AJUSTE
        for j in (1, 2):
            wd.cell(f, j).border = BORDE
        f += 1
    wd.cell(f + 1, 1, "Escala: 0 sin evidencia; 1 indicio débil; 2 indicio relevante (documental); 3 prueba fuerte. Detalle completo en analisis/marco_juridico_laboral.md.").alignment = AJUSTE
anchos(wd, [30, 90, 30, 34])
wd.sheet_view.showGridLines = False

if LABORAL:
    # ---------- Matriz laboral ----------
    wm = wb.create_sheet("Matriz laboral")
    wm["A1"] = "Matriz de indicadores laborales (ver analisis/marco_juridico_laboral.md y analisis/analisis_laboral.md)"
    wm["A1"].font = TITULO
    wm["A2"] = ("Escala 0–3 por indicador; s/d = sin datos. S = societarios, L = laborales/operativos, F = fraude. "
                "PS/PL/PF = puntajes por plano. N1 control común, N2 relevante, N3 débil, N4 sin vínculo. "
                "IMP-A empleador real, IMP-B intermediación, IMP-C sustitución, IMP-D fraude, IMP-E IPS, IMP-0 sin base; (h) = hipótesis.")
    wm["A2"].alignment = AJUSTE
    wm.merge_cells("A2:Z2")
    wm.row_dimensions[2].height = 45
    cols = list(next(iter(MAT.values())).keys())
    f = encabezado(wm, 4, cols)
    for r in BASE:
        m = MAT.get(r["id"])
        if not m:
            continue
        for j, k in enumerate(cols, 1):
            c = wm.cell(f, j, num(m[k]) if k not in ("ruc", "id") else m[k])
            c.border = BORDE
        f += 1
    anchos(wm, [5, 24, 40, 13] + [6] * (len(cols) - 7) + [8, 16, 50])
    wm.freeze_panes = "D5"

# ---------- Una hoja por entidad ----------
for r in BASE:
    eid = r["id"]
    e, m, c = EMP.get(eid, {}), MAT.get(eid, {}), CTRL.get(eid, {})
    ws = wb.create_sheet(HOJA[eid])
    N = 8
    anchos(ws, [34, 16, 16, 14, 14, 14, 16, 40])
    ws["A1"] = e.get("razon_social") or r["razon_social"]
    ws["A1"].font = TITULO
    ws["H1"] = "← Volver al índice"
    ws["H1"].hyperlink = "#'Índice'!A1"
    ws["H1"].font = Font(color="0563C1", underline="single")

    fila = seccion(ws, 3, "1. Identificación", N)
    nivel = m.get("nivel", "")
    datos = [
        ("Razón social (Informe CRA 385/2026)", r["razon_social"]),
        ("RUC", r["ruc"] or "sin RUC (no registrada en SIARA)"),
        ("Tipo", e.get("tipo", "")),
        ("Denominaciones anteriores", e.get("denominaciones_anteriores", "")),
        ("Fecha de constitución", e.get("fecha_constitucion", "")),
        ("Domicilio actual", e.get("domicilio_actual", "")),
        ("Actividad", e.get("actividad", "")),
        ("Objeto social", e.get("objeto_social", "")),
        ("Capital", e.get("capital", "")),
        ("Presidente / representante actual", e.get("presidente_actual", "")),
        ("Tiene constancia de beneficiarios finales", sino(e.get("tiene_BF", ""))),
        ("Documentos remitidos por el MEF", num(e.get("n_documentos", ""))),
        ("Carpeta en el expediente", r["carpeta_mef"]),
    ]
    for k, v in datos:
        a = ws.cell(fila, 1, k)
        a.font, a.border, a.alignment = NEGRITA, BORDE, AJUSTE
        b = ws.cell(fila, 2, v)
        b.border, b.alignment = BORDE, AJUSTE
        ws.merge_cells(start_row=fila, start_column=2, end_row=fila, end_column=N)
        if isinstance(v, str) and len(v) > 90:
            ws.row_dimensions[fila].height = 15 * min(8, len(v) // 90 + 1)
        fila += 1

    fila = seccion(ws, fila + 1, "2. Pertenencia al grupo y control", N)
    datos = [
        ("Segmento", seg(e.get("segmento", ""))),
        ("Justificación del segmento", e.get("justificacion_segmento", "")),
        ("Controlante directo", e.get("controlante_directo", "") or c.get("controlante_directo", "")),
        ("Controlante último", e.get("controlante_ultimo", "") or c.get("controlante_ultimo", "")),
        ("Cadena de control", c.get("cadena_control", "")),
        ("% integrado del grupo en el capital", num(e.get("pct_integrado_grupo", ""))),
        ("Nivel de vínculo (matriz laboral)", f"{nivel} – {NIVELES.get(nivel, '')}" if nivel else ""),
        ("Puntajes societario / laboral / fraude", f"PS {m.get('PS', '')} · PL {m.get('PL', '')} · PF {m.get('PF', '')}" if m else ""),
        ("Imputación (hipótesis de trabajo)", m.get("imputacion", "")),
        ("Vía jurídica principal", m.get("via_principal", "")),
    ]
    if not LABORAL:
        datos = datos[:6]
    for k, v in datos:
        a = ws.cell(fila, 1, k)
        a.font, a.border, a.alignment = NEGRITA, BORDE, AJUSTE
        b = ws.cell(fila, 2, v)
        b.border, b.alignment = BORDE, AJUSTE
        ws.merge_cells(start_row=fila, start_column=2, end_row=fila, end_column=N)
        if isinstance(v, str) and len(v) > 90:
            ws.row_dimensions[fila].height = 15 * min(8, len(v) // 90 + 1)
        fila += 1

    fila = seccion(ws, fila + 1, "3. Composición accionaria vigente (resumen por titular)", N)
    ag = sorted(AGR.get(eid, []), key=lambda x: -(num(x["pct_capital"]) or 0) if isinstance(num(x["pct_capital"]), (int, float)) else 0)
    filas = [([a["titular"], a["tipo"], num(a["pct_capital"]), num(a["pct_votos"]), a["fechas"], "", "", a["fuentes"]], False) for a in ag]
    fila = tabla(ws, fila, ["Titular", "Tipo de persona", "% capital", "% votos", "Fecha(s) del dato", "", "", "Fuentes"], filas, N)

    fila = seccion(ws, fila, "3b. Detalle de asientos de accionistas, vigentes e históricos (sombreado = vigente)", N)
    ps = sorted(PART.get(eid, []), key=lambda x: (not es_vigente(x), x.get("fecha_dato", "")), reverse=False)
    filas = [([p["accionista"], p["documento"], num(p["acciones"]), num(p["porcentaje"]), num(p["votos"]),
               p["fecha_dato"], "Sí" if es_vigente(p) else "No", f"{fuente(p)} · confianza {p['confianza']}" + (f" · {p['notas']}" if p.get("notas") else "")],
              es_vigente(p)) for p in ps]
    fila = tabla(ws, fila, ["Accionista", "Documento", "Acciones", "%", "Votos", "Fecha del dato", "Vigente", "Fuente / notas"], filas, N)

    fila = seccion(ws, fila, "4. Directores, síndicos y representantes (sombreado = vigente)", N)
    au = sorted(AUT.get(eid, []), key=lambda x: (not es_vigente(x), x.get("fecha_dato", "")))
    filas = [([a["nombre"], a["documento"], a["cargo"], a["fecha_asuncion"], a["vigencia"], a["fecha_dato"],
               "Sí" if es_vigente(a) else "No", fuente(a) + (f" · {a['notas']}" if a.get("notas") else "")], es_vigente(a)) for a in au]
    fila = tabla(ws, fila, ["Nombre", "Documento", "Cargo", "Asunción", "Vigencia", "Fecha del dato", "Vigente", "Fuente / notas"], filas, N)

    fila = seccion(ws, fila, "5. Beneficiarios finales declarados", N)
    filas = [([b["nombre"], b["documento"], b["tipo_control"], num(b["porcentaje"]), b["nacionalidad"], b["fecha_dato"],
               b["confianza"], (b["cadena_control"] + " · " if b.get("cadena_control") else "") + fuente(b) + (f" · {b['notas']}" if b.get("notas") else "")], False)
             for b in BF.get(eid, [])]
    fila = tabla(ws, fila, ["Nombre", "Documento", "Tipo de control", "%", "Nacionalidad", "Fecha del dato", "Confianza", "Cadena / fuente / notas"], filas, N,
                 "No consta constancia de beneficiarios finales en la documentación remitida.")

    fila = seccion(ws, fila, "6. Historial (cronológico)", N)
    hs = sorted(HIST.get(eid, []), key=lambda x: x.get("fecha", ""))
    filas = [([h["fecha"], h["evento"], h["detalle"], "", "", "", "", fuente(h)], False) for h in hs]
    fila0 = fila
    fila = tabla(ws, fila, ["Fecha", "Evento", "Detalle", "", "", "", "", "Fuente"], filas, N)
    for rr in range(fila0 + 1, fila - 1):
        ws.merge_cells(start_row=rr, start_column=3, end_row=rr, end_column=7)
        txt = ws.cell(rr, 3).value or ""
        ws.row_dimensions[rr].height = 15 * min(8, len(str(txt)) // 80 + 1)

    fila = seccion(ws, fila, "7. Vínculos con otras entidades y personas", N)
    vs = VINC.get(eid, [])
    filas = []
    for v in vs:
        otro = v["destino_nombre"] if v["origen"] == eid else v["origen_nombre"]
        sentido = "→" if v["origen"] == eid else "←"
        filas.append(([f"{sentido} {otro}", v["tipo"], num(v["peso"]), v["fecha"], "Sí" if es_vigente(v) else "No", "", "", f"{v['detalle']} · {v['fuente']}"], es_vigente(v)))
    fila = tabla(ws, fila, ["Entidad / persona relacionada", "Tipo de vínculo", "Peso / %", "Fecha", "Vigente", "", "", "Detalle y fuente"], filas, N)

    fila = seccion(ws, fila, "8. Declarantes ante el SIARA y contactos", N)
    filas = [([d["nombre"], d["documento"], d["tipo"], d["correo"], d["dominio"], d["telefono"], d["fecha"],
               (d["domicilio"] + " · " if d.get("domicilio") else "") + fuente(d) + (f" · {d['notas']}" if d.get("notas") else "")], False)
             for d in DECL.get(eid, [])]
    fila = tabla(ws, fila, ["Nombre", "Documento", "Tipo", "Correo", "Dominio", "Teléfono", "Fecha", "Domicilio / fuente / notas"], filas, N)

    fila = seccion(ws, fila, "9. Alertas de calidad de datos", N)
    cal = CAL.get(eid, [])
    if not LABORAL:  # en la versión societaria se omiten observaciones con valoraciones jurídicas o laborales
        cal = [q for q in cal if not INTERPRETATIVO.search(q["detalle"])]
    filas = [([q["severidad"], q["tipo"], q["detalle"], "", "", "", "", ""], False) for q in cal]
    fila0 = fila
    fila = tabla(ws, fila, ["Severidad", "Tipo", "Detalle", "", "", "", "", ""], filas, N, "Sin alertas registradas.")
    for rr in range(fila0 + 1, fila - 1):
        ws.merge_cells(start_row=rr, start_column=3, end_row=rr, end_column=N)

    ws.sheet_view.showGridLines = False
    ws.page_setup.orientation = "landscape"
    ws.page_setup.fitToWidth = 1
    ws.page_setup.fitToHeight = 0
    ws.sheet_properties.pageSetUpPr.fitToPage = True

os.makedirs(os.path.dirname(SALIDA), exist_ok=True)
wb.save(SALIDA)
print("OK", SALIDA, len(wb.sheetnames), "hojas")
