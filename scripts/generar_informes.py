#!/usr/bin/env python3
"""Genera analisis/red_societaria.md, fichas/<id>.md y fichas/README.md a partir de datos/consolidado/*.csv.
Ejecutar después de scripts/consolidar.py:   python3 -I scripts/generar_informes.py
networkx es opcional (centralidad de intermediación); sin él se informa sólo el grado."""
import csv, json, re, collections, pathlib, itertools

ROOT = pathlib.Path(__file__).resolve().parent.parent
C = ROOT / "datos" / "consolidado"
def rd(n):
    return list(csv.DictReader(open(C / n, encoding="utf-8")))
EMP = {r["id"]: r for r in rd("empresas.csv")}
IDS = list(EMP)
CTRL = rd("control_indirecto.csv")
AGG = rd("participaciones_agregadas.csv")
PERS = rd("personas.csv")
ROLES = rd("personas_roles.csv")
VINC = rd("vinculos.csv")
SAL = rd("salidas_grupo.csv")
CAL = rd("calidad_datos.csv")
HIST = rd("historial.csv")
AUT = rd("autoridades.csv")
BF = rd("beneficiarios_finales.csv")
PART = rd("participaciones.csv")
DECL = rd("declarantes_contactos.csv")
AUX = json.loads((C / "_aux.json").read_text(encoding="utf-8"))
FED = AUX["federico"]
FICHAS = {i: json.loads((ROOT / "datos" / "empresas" / f"{i}.json").read_text(encoding="utf-8")) for i in IDS}

SEG_NOMBRE = {"nucleo_financiero_ueno": "Núcleo financiero Ueno", "holding_controlante": "Holding / controlantes",
              "controlada_itti_gv": "Controladas por ITTI / Grupo Vázquez", "participada_minoritaria_o_vinculo_indirecto": "Participadas minoritarias / vínculo indirecto",
              "ex_vinculada": "Ex vinculadas (salidas 2025-2026)", "sin_vinculo_detectado": "Sin vínculo detectado"}
SEG_ORDEN = list(SEG_NOMBRE)
PNAME = {p["persona_id"]: p["nombre_canonico"] for p in PERS}

def nom(k):
    if k == "ueno_holdings_sarl":
        return "U Holdings S.à r.l. (Luxemburgo)"
    if k in EMP:
        return EMP[k]["razon_social_base"]
    if k in PNAME:
        return PNAME[k].title()
    return k.replace("EXT:", "").title()

def mid(k):
    return "n_" + re.sub(r"[^A-Za-z0-9]", "_", k)

def f(x, nd=2):
    try:
        return f"{float(x):.{nd}f}".replace(".", ",")
    except (TypeError, ValueError):
        return "s/d"

ctrl_v = {r["entidad_id"]: r for r in CTRL if r["corte"] == "vigente"}
ctrl_24 = {r["entidad_id"]: r for r in CTRL if r["corte"] == "2024"}

# ---------------------------------------------------------------------------
# Métricas de red entre entidades
# ---------------------------------------------------------------------------
FUERTES = {"participacion_directa", "participacion_historica", "autoridad_comun", "bf_comun", "accionista_fisico_comun",
           "mismo_declarante", "mismo_correo", "transferencia_acciones", "fusion", "bf_declarado_persona_juridica"}
adj = collections.defaultdict(lambda: collections.defaultdict(set))
for v in VINC:
    a, b = v["origen"], v["destino"]
    if a in EMP and b in EMP and a != b:
        adj[a][b].add(v["tipo"]); adj[b][a].add(v["tipo"])

def componentes(filtro):
    seen, comps = set(), []
    for n in IDS:
        if n in seen:
            continue
        st, comp = [n], []
        seen.add(n)
        while st:
            x = st.pop(); comp.append(x)
            for y, ts in adj[x].items():
                if y not in seen and any(filtro(t) for t in ts):
                    seen.add(y); st.append(y)
        comps.append(sorted(comp))
    return sorted(comps, key=lambda c: -len(c))

comp_todos = componentes(lambda t: True)
comp_fuertes = componentes(lambda t: t in FUERTES)
comp_societ = componentes(lambda t: t in {"participacion_directa", "participacion_historica", "transferencia_acciones", "fusion"})

betw = {}
try:
    import networkx as nx
    G = nx.Graph()
    G.add_nodes_from(IDS)
    for a in adj:
        for b, ts in adj[a].items():
            if any(t in FUERTES for t in ts):
                G.add_edge(a, b, weight=1)
    betw = nx.betweenness_centrality(G)
except ImportError:
    pass
deg_f = {n: sum(1 for y, ts in adj[n].items() if any(t in FUERTES for t in ts)) for n in IDS}
deg_t = {n: len(adj[n]) for n in IDS}

# ---------------------------------------------------------------------------
# Diagrama (a): control vigente (>=10% o control)
# ---------------------------------------------------------------------------
GRUPO_SEG = {"nucleo_financiero_ueno", "holding_controlante", "controlada_itti_gv"}
aristas = []
for r in AGG:
    if r["corte"] != "vigente":
        continue
    y, t = r["empresa_id"], r["titular_id"]
    cap = float(r["pct_capital"]) if r["pct_capital"] else None
    vot = float(r["pct_votos"]) if r["pct_votos"] else None
    es_ctrl = ctrl_v.get(y, {}).get("controlante_directo_id") == t
    if EMP.get(y, {}).get("segmento") not in GRUPO_SEG and r["tipo"] != "declarado" and not (t in EMP and EMP[t]["segmento"] in GRUPO_SEG and (cap or 0) >= 5):
        continue
    if y == "ueno_holding_saeca":
        continue
    if not ((cap is not None and cap >= 10) or es_ctrl or r["tipo"] == "declarado"):
        continue
    if not (t in EMP or t == FED or t.startswith("EXT:")):
        continue
    aristas.append((t, y, cap, vot, es_ctrl, r["tipo"] == "declarado"))
nodos = {a for e in aristas for a in e[:2]}

def etiqueta_arista(cap, vot, ctrl, decl):
    if decl:
        return "control declarado BF"
    s = f"{f(cap, 1)}%" if cap is not None else ""
    if vot is not None and cap is not None and abs(vot - cap) > 1:
        s += f" / {f(vot, 1)}% votos"
    return s

mer_a = ["```mermaid", "flowchart TD"]
subg = collections.defaultdict(list)
for n in sorted(nodos):
    seg = EMP[n]["segmento"] if n in EMP else ("persona" if n == FED else "externa")
    subg[seg].append(n)
tit = {"persona": "Controlante último (persona física)", "externa": "Sociedades fuera del listado", **SEG_NOMBRE}
for seg in ["persona", "holding_controlante", "nucleo_financiero_ueno", "controlada_itti_gv", "participada_minoritaria_o_vinculo_indirecto", "externa"]:
    if not subg.get(seg):
        continue
    mer_a.append(f'  subgraph {seg}["{tit[seg]}"]')
    for n in subg[seg]:
        mer_a.append(f'    {mid(n)}["{nom(n)}"]')
    mer_a.append("  end")
for t, y, cap, vot, ctrl, decl in aristas:
    lab = etiqueta_arista(cap, vot, ctrl, decl)
    arrow = "-.->" if decl else ("==>" if ctrl else "-->")
    mer_a.append(f'  {mid(t)} {arrow}|"{lab}"| {mid(y)}' if lab else f"  {mid(t)} {arrow} {mid(y)}")
mer_a += ["  classDef persona fill:#fde68a,stroke:#92400e;", f"  class {mid(FED)} persona;", "```"]

# ---------------------------------------------------------------------------
# Diagrama (b): salidas y reorganizaciones 2025-2026
# ---------------------------------------------------------------------------
REORG = [  # (origen, destino, etiqueta) — reorganizaciones internas documentadas en historial.csv
    ("ueno_holding_saeca", "grupo_vazquez", "fusión por absorción 16/07/2025"),
    ("grupo_vazquez", "u_paraguay", "canje acciones Ueno Seguros y Casa de Bolsa 30/06/2025"),
    ("itti", "grupo_vazquez", "acciones Red Digital y Redipro 30/06/2025 (→ U Paraguay)"),
    ("grupo_vazquez", "u_paraguay", "68.000 acciones ITTI 02/10/2026 (→ Ueno Bank)"),
    ("u_paraguay", "ueno_bank", "cede 68.000 acciones ITTI 02/10/2026"),
    ("ueno_bank", "redisa", "preferidas Redipro 09/09/2026 → ITTI → GV → U Paraguay 25/09/2026"),
]
ENTRADAS = [("grupo_vazquez", "oniria", "compra 60% 03/01/2025"), ("grupo_vazquez", "23_sports_marketing", "60% suscr. 03/01/2025"),
            ("itti", "tiva", "ingreso 60% 20/01/2025"), ("grupo_vazquez", "terravaz", "toma 97,33% jun-ago 2025"),
            ("itti", "comdetur", "99% 25/07/2025"), ("itti", "kostas_viajes", "98,94% 2025"), ("itti", "intertours", "45% 09/2025 → 70% 07/2026")]
mer_b = ["```mermaid", "flowchart LR"]
n_b = set()
def nd(k, lines):
    if k not in n_b:
        n_b.add(k)
        lines.append(f'  {mid(k)}["{nom(k)}"]')
mer_b.append('  subgraph SAL["Salidas del grupo (ventas a personas físicas)"]')
for s in SAL:
    nd(s["empresa_id"], mer_b)
mer_b.append("  end")
for s in SAL:
    for v in s["vendedores_grupo"].split("; "):
        vid = next((k for k in EMP if EMP[k]["razon_social_base"] == v or nom(k) == v), None)
        if not vid:
            continue
        nd(vid, mer_b)
        mer_b.append(f'  {mid(vid)} -->|"vende {s["fecha_salida"]}"| {mid(s["empresa_id"])}')
    for tid, tn in zip(s["titulares_actuales_ids"].split("; "), s["titulares_actuales"].split("; ")):
        k = "B_" + tid
        nombre_b, pct_b = (tn.rsplit(" (", 1) + [""])[:2]
        if k not in n_b:
            n_b.add(k)
            mer_b.append(f'  {mid(k)}(["{nombre_b.title()}"])')
        mer_b.append(f'  {mid(s["empresa_id"])} -.->|"{pct_b.rstrip(")")}"| {mid(k)}')
mer_b.append('  subgraph REO["Reorganización interna 2025-2026"]')
for a, b, lab in REORG:
    nd(a, mer_b); nd(b, mer_b)
mer_b.append("  end")
for a, b, lab in REORG:
    mer_b.append(f'  {mid(a)} ==>|"{lab}"| {mid(b)}')
for a, b, lab in ENTRADAS:
    nd(a, mer_b); nd(b, mer_b)
    mer_b.append(f'  {mid(a)} -->|"{lab}"| {mid(b)}')
mer_b.append("```")

# ---------------------------------------------------------------------------
# Tablas
# ---------------------------------------------------------------------------
def tabla(cab, filas):
    out = ["| " + " | ".join(cab) + " |", "|" + "|".join("---" for _ in cab) + "|"]
    for fl in filas:
        out.append("| " + " | ".join(str(x).replace("|", "/").replace("\n", " ") for x in fl) + " |")
    return out

roles_por_p = collections.defaultdict(lambda: collections.defaultdict(set))
for r in ROLES:
    lab = r["cargo"] if r["rol"] == "autoridad" else {"accionista": "accionista", "beneficiario_final": "BF", "declarante": "declarante"}.get(r["rol"], r["rol"])
    roles_por_p[r["persona_id"]][r["empresa_id"]].add(re.sub(r"\s*\(.*", "", lab)[:40])
top = sorted(PERS, key=lambda p: (-int(p["n_empresas"]), -int(p["n_menciones"])))[:30]
filas_top = []
for p in top:
    emp = roles_por_p[p["persona_id"]]
    det = "; ".join(f"{EMP[e]['razon_social_base']}: {', '.join(sorted(r))}" for e, r in sorted(emp.items()))
    filas_top.append([p["persona_id"], p["nombre_canonico"].title(), p["ci"] or "s/d", p["n_empresas"], det[:600]])

filas_cent = []
for n in sorted(IDS, key=lambda n: (-deg_f[n], -betw.get(n, 0)))[:20]:
    filas_cent.append([EMP[n]["razon_social_base"], SEG_NOMBRE[EMP[n]["segmento"]], deg_f[n], deg_t[n], f(betw.get(n, 0) * 100, 1) if betw else "n/d"])

def comp_tab(comps):
    out = []
    for k, c in enumerate(comps, 1):
        if len(c) == 1:
            continue
        out.append([k, len(c), ", ".join(EMP[x]["razon_social_base"] for x in c)])
    aisl = [EMP[c[0]]["razon_social_base"] for c in comps if len(c) == 1]
    return out, aisl

ct, ais = comp_tab(comp_fuertes)
cs, ais_s = comp_tab(comp_societ)
ctodo, ais_t = comp_tab(comp_todos)

# Control vigente vs 2024
filas_ctrl = []
for i in IDS:
    v, a = ctrl_v[i], ctrl_24[i]
    if not (v["controlante_directo"] or a["controlante_directo"]):
        continue
    filas_ctrl.append([EMP[i]["razon_social_base"], SEG_NOMBRE[EMP[i]["segmento"]],
                       f"{v['controlante_directo'] or '—'}" + (f" ({f(v['pct_votos_controlante_directo'])}% v.)" if v["pct_votos_controlante_directo"] else ""),
                       v["controlante_ultimo"] or "—", f(v["integ_ueno_holdings_sarl"]) if v["integ_ueno_holdings_sarl"] else "—",
                       f(v["integ_grupo_vazquez"]) if v["integ_grupo_vazquez"] else "—", f(v["integ_grupo_total"]) if v["integ_grupo_total"] else "—",
                       (a["controlante_directo"] or "s/d") + (f" ({f(a['pct_votos_controlante_directo'])}% v.)" if a["pct_votos_controlante_directo"] else "")])

ub = ctrl_v["ueno_bank"]
md = ["# Red societaria — entidades remitidas por el MEF (SIME 78.318/2026)", "",
      "Generado automáticamente por `scripts/generar_informes.py` a partir de `datos/consolidado/`. "
      "Las cifras de participación integrada multiplican los porcentajes de capital a lo largo de todas las cadenas; "
      "el control se determina por mayoría de votos (directa o sumando sociedades bajo el mismo controlante). "
      "Fecha de corte \"vigente\" = dato más reciente marcado vigente en cada ficha (2025-2026). Ver `analisis/metodologia_datos.md`.", "",
      "## Hallazgos principales", "",
      f"- **Controlante último declarado:** Federico Miguel Vázquez Villasanti (CI 2.941.546), titular de 75,94% del capital y ≈94% de los votos de Grupo Vázquez S.A.E., "
      "y declarado beneficiario final (condición E, cadena de titularidad) a través de U Holdings S.à r.l. (Luxemburgo, B280698) en el listado BF de Redipro. "
      "La composición societaria de U Holdings **no consta** en ningún documento: es el eslabón opaco de la cadena.",
      f"- **Cadena de control de Ueno Bank:** {ub['cadena_control']}. Participación integrada en el capital: {f(ub['integ_ueno_holdings_sarl'])}% vía U Holdings + "
      f"{f(ub['integ_grupo_vazquez'])}% vía Grupo Vázquez (directo 1,96% + 2,01% de U Paraguay) = {f(ub['integ_grupo_total'])}%. A marzo de 2024 el controlante directo era Grupo Vázquez (94,91% de los votos).",
      "- **Dos ramas:** (1) financiera: U Holdings → U Paraguay → Ueno Bank, Ueno Seguros, Ueno Casa de Bolsa (→ Ueno AFPI), Red Digital y Redipro; "
      "(2) no financiera: Grupo Vázquez → ITTI (77,46% capital, ≈91% votos) → sociedades de tecnología, turismo, logística; GV directamente en Terravaz, Oniria y 23 Sports. "
      "Las ramas se cruzan: Ueno Bank tiene 16,95% de ITTI (02/10/2026) y GV conserva 2,01% de U Paraguay y 1,96% de Ueno Bank.",
      f"- **Reestructuración 2025-2026:** {len(SAL)} sociedades salieron del grupo por venta a personas físicas (Franede, MOWI, TUIU, Grupo Hendy, Grupo M, Office Design, V Media); "
      "los compradores son en su mayoría directivos o allegados del propio grupo (Urdapilleta, Pizurno, Vera, Gadea, Villasanti, Mauro Vargas). "
      "En paralelo, el núcleo financiero se trasladó de Grupo Vázquez a U Paraguay/U Holdings (30/06/2025) y Ueno Holding S.A.E.C.A. fue absorbida por GV (16/07/2025).",
      "- **Personas clave** (por número de entidades): " + ", ".join(f"{p['nombre_canonico'].title()} ({p['n_empresas']})" for p in top[:10]) + ".",
      "- **Domicilio común:** Torres del Paseo / Paseo La Galería (Avda. Santa Teresa 1827, Asunción); dominios de correo comunes gvcorp.com.py, uenoholding.com.py, itti.digital.", "",
      "## (a) Organigrama de control vigente (participaciones ≥ 10% o control)", "",
      "Flecha gruesa = controlante directo; punteada = control declarado en constancias BF sin porcentaje. Sólo entidades del grupo y sus titulares societarios.", ""] + mer_a + [
      "", "## (b) Salidas y transferencias 2025-2026", "",
      "Salidas del grupo (venta de la totalidad de la participación de GV/ITTI) y principales reorganizaciones/entradas documentadas en los historiales.", ""] + mer_b + [
      "", "### Salidas del grupo (tabla)", ""] + tabla(["Entidad", "Fecha", "Vendedores", "Titulares actuales"],
      [[s["empresa"], s["fecha_salida"], s["vendedores_grupo"], s["titulares_actuales"]] for s in SAL]) + [
      "", "## Control por entidad: vigente vs. 2024", "",
      "UH = participación integrada desde U Holdings; GV = desde Grupo Vázquez; Grupo = UH + GV + tenencia directa de F. M. Vázquez. La situación 2024 combina la foto ≤ 31/12/2024 y una reconstrucción documentada (ver `control_indirecto.csv`, columna notas).", ""] + tabla(
      ["Entidad", "Segmento", "Controlante directo vigente", "Controlante último", "% UH", "% GV", "% Grupo", "Controlante directo 2024"], filas_ctrl) + [
      "", "## Personas recurrentes (top 30 por número de entidades)", ""] + tabla(["ID", "Persona", "CI", "Nº entidades", "Roles por entidad"], filas_top) + [
      "", "## Entidades con más vínculos (centralidad)", "",
      "Grado fuerte = nº de otras entidades del listado con las que comparte participación, autoridades, BF, accionistas, declarante, correo o transferencias; "
      "grado total incluye también domicilio y dominio de correo. Intermediación = betweenness sobre la red de vínculos fuertes (%).", ""] + tabla(
      ["Entidad", "Segmento", "Grado fuerte", "Grado total", "Intermediación"], filas_cent) + [
      "", "## Componentes conexos", "", "### Con vínculos fuertes", ""] + tabla(["#", "Tamaño", "Entidades"], ct) + [
      "", "Aisladas: " + (", ".join(ais) or "ninguna"), "", "### Sólo vínculos societarios (participaciones y transferencias)", ""] + tabla(["#", "Tamaño", "Entidades"], cs) + [
      "", "Aisladas: " + (", ".join(ais_s) or "ninguna"), "", "### Todos los vínculos (incluye domicilio y dominio de correo)", ""] + tabla(["#", "Tamaño", "Entidades"], ctodo) + [
      "", "Aisladas: " + (", ".join(ais_t) or "ninguna"), "",
      "## Archivos", "", "- `datos/consolidado/vinculos.csv` (aristas tipadas), `control_indirecto.csv`, `participaciones_agregadas.csv`, `salidas_grupo.csv`",
      "- `datos/consolidado/grafo.graphml` (entidades, personas con ≥ 2 entidades y entidades externas; abrir con Gephi/yEd/Cytoscape)", ""]
(ROOT / "analisis" / "red_societaria.md").write_text("\n".join(md), encoding="utf-8")

# ---------------------------------------------------------------------------
# Fichas por entidad
# ---------------------------------------------------------------------------
(ROOT / "fichas").mkdir(exist_ok=True)
def fuente(r):
    a, p = r.get("fuente_archivo", ""), r.get("fuente_pagina", "")
    return f"{a} p.{p}" if a else ""

for i in IDS:
    e, d, cv, c4 = EMP[i], FICHAS[i], ctrl_v[i], ctrl_24[i]
    L = [f"# {e['razon_social']}", "", f"*Ficha generada automáticamente — id `{i}`. Datos: `datos/empresas/{i}.json` y `datos/consolidado/`.*", "",
         "## Identificación", ""]
    L += tabla(["Campo", "Dato"], [["Razón social", e["razon_social"]], ["RUC", e["ruc"] or "s/d"], ["Tipo", e["tipo"]], ["Actividad", e["actividad"]],
               ["Constitución", e["fecha_constitucion"] or "s/d"], ["Domicilio actual", e["domicilio_actual"] or "s/d"], ["Capital (último dato)", e["capital"] or "s/d"],
               ["Denominaciones anteriores", e["denominaciones_anteriores"] or "—"], ["Presidente / representante", e["presidente_actual"] or "s/d"],
               ["Constancia/listado BF", "sí" if e["tiene_BF"] == "1" else "no"], ["Documentos remitidos", e["n_documentos"]]])
    L += ["", "## Segmento", "", f"**{SEG_NOMBRE[e['segmento']]}** — {e['justificacion_segmento']}", "", "## Accionistas vigentes", ""]
    vig = [r for r in AGG if r["corte"] == "vigente" and r["empresa_id"] == i]
    if vig:
        L += tabla(["Titular", "% capital", "% votos", "Fecha dato", "Fuente"],
                   [[nom(r["titular_id"]) if (r["titular_id"] in EMP or r["titular_id"] in PNAME) else r["titular"], f(r["pct_capital"]), f(r["pct_votos"]),
                     r["fechas"], r["fuentes"][:160]] for r in sorted(vig, key=lambda r: -float(r["pct_capital"] or 0))])
    else:
        L.append("Sin datos de accionistas vigentes en la documentación.")
    L += ["", "## Control", ""]
    L += tabla(["Corte", "Controlante directo", "Tipo de control", "Controlante último", "Cadena", "% integrado grupo"],
               [["Vigente", cv["controlante_directo"] or "—", cv["tipo_control"], cv["controlante_ultimo"] or "—", cv["cadena_control"] or "—", f(cv["integ_grupo_total"]) if cv["integ_grupo_total"] else "—"],
                ["2024", c4["controlante_directo"] or "—", c4["tipo_control"], c4["controlante_ultimo"] or "—", c4["cadena_control"] or "—", f(c4["integ_grupo_total"]) if c4["integ_grupo_total"] else "—"]])
    L += ["", "## Autoridades vigentes", ""]
    av = [r for r in AUT if r["empresa_id"] == i and r["vigente"] == "True"]
    if not av:
        ult = max((r["fecha_dato"] or r["fecha_asuncion"] for r in AUT if r["empresa_id"] == i), default=None)
        av = [r for r in AUT if r["empresa_id"] == i and (r["fecha_dato"] or r["fecha_asuncion"]) == ult] if ult else []
        if av:
            L.append(f"*(ninguna marcada vigente; se muestran las del dato más reciente, {ult})*")
    L += tabla(["Nombre", "CI", "Cargo", "Desde", "Fuente"], [[r["nombre"], r["documento"] or "", r["cargo"], r["fecha_asuncion"] or r["fecha_dato"], fuente(r)] for r in av]) if av else ["Sin datos."]
    L += ["", "## Beneficiarios finales declarados", ""]
    bf = [r for r in BF if r["empresa_id"] == i]
    L += tabla(["Nombre", "Documento", "%", "Tipo de control", "Cadena", "Fecha"], [[r["nombre"], r["documento"] or "", f(r["porcentaje"]) if r["porcentaje"] else "", r["tipo_control"], (r["cadena_control"] or "")[:150], r["fecha_dato"]] for r in bf]) if bf else ["No consta constancia ni listado de BF."]
    L += ["", "## Historial", ""]
    hs = [h for h in HIST if h["empresa_id"] == i]
    L += [f"- **{h['fecha'] or 's/f'}** ({h['evento']}): {h['detalle']} _[{fuente(h)}]_" for h in hs] or ["Sin eventos registrados."]
    L += ["", "## Vínculos con otras entidades del listado", ""]
    vv = collections.defaultdict(list)
    for v in VINC:
        if v["origen"] == i and v["destino"] in EMP:
            vv[v["destino"]].append(v)
        elif v["destino"] == i and v["origen"] in EMP:
            vv[v["origen"]].append(v)
    if vv:
        filas = []
        for o, vs in sorted(vv.items(), key=lambda kv: -len(kv[1])):
            tipos = collections.Counter(v["tipo"] for v in vs)
            det = "; ".join(sorted({v["detalle"][:120] for v in vs if v["tipo"] in ("participacion_directa", "autoridad_comun", "bf_comun", "accionista_fisico_comun", "mismo_declarante", "transferencia_acciones")}))[:350]
            filas.append([EMP[o]["razon_social_base"], ", ".join(f"{t} ({n})" for t, n in tipos.most_common()), det])
        L += tabla(["Entidad", "Tipos de vínculo", "Detalle (selección)"], filas)
    else:
        L.append("Ninguno detectado.")
    L += ["", "## Contactos SIARA", ""]
    dc = [r for r in DECL if r["empresa_id"] == i and r["tipo"] == "declarante"]
    L += tabla(["Declarante", "Documento", "Correo", "Teléfono", "Fecha"], [[r["nombre"] or "", r["documento"] or "", r["correo"], r["telefono"], r["fecha"]] for r in dc]) if dc else ["Sin datos."]
    L += ["", "## Documentos fuente", ""]
    docs = d.get("documentos") or []
    L += tabla(["Archivo", "Tipo", "Fecha", "Págs.", "Legibilidad", "Resumen"], [[x.get("archivo"), x.get("tipo"), x.get("fecha"), x.get("paginas"), x.get("legibilidad"), (x.get("resumen") or "")[:200]] for x in docs]) if docs else ["Sin documentos propios (información tomada de otras carpetas)."]
    L += ["", "## Alertas de calidad", ""]
    cq = [r for r in CAL if r["empresa_id"] == i and r["severidad"] != "info"]
    ob = [r for r in CAL if r["empresa_id"] == i and r["severidad"] == "info"]
    L += [f"- [{r['severidad']}] {r['tipo']}: {r['detalle']}" for r in cq] or ["- Sin alertas automáticas."]
    if ob:
        L += ["", "Observaciones de extracción y verificación:", ""] + [f"- {r['detalle']}" for r in ob]
    (ROOT / "fichas" / f"{i}.md").write_text("\n".join(L) + "\n", encoding="utf-8")

idx = ["# Fichas por entidad — SIME 78.318/2026", "", "Índice de las 51 personas y estructuras jurídicas remitidas por el MEF. Generado por `scripts/generar_informes.py`.", ""]
for seg in SEG_ORDEN:
    ids = [i for i in IDS if EMP[i]["segmento"] == seg]
    if not ids:
        continue
    idx += [f"## {SEG_NOMBRE[seg]} ({len(ids)})", ""]
    idx += tabla(["#", "Entidad", "RUC", "Actividad", "Controlante directo", "Controlante último", "% grupo", "BF"],
                 [[k, f"[{EMP[i]['razon_social_base']}]({i}.md)", EMP[i]["ruc"] or "s/d", (EMP[i]["actividad"] or "")[:60], ctrl_v[i]["controlante_directo"] or "—",
                   ctrl_v[i]["controlante_ultimo"] or "—", f(ctrl_v[i]["integ_grupo_total"]) if ctrl_v[i]["integ_grupo_total"] else "—", "sí" if EMP[i]["tiene_BF"] == "1" else "no"]
                  for k, i in enumerate(ids, 1)])
    idx.append("")
(ROOT / "fichas" / "README.md").write_text("\n".join(idx), encoding="utf-8")
print("ok", len(IDS), "fichas;", len(aristas), "aristas diagrama a;", len(SAL), "salidas")
