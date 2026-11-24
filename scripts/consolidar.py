#!/usr/bin/env python3
"""Consolidación de las 51 fichas JSON (datos/empresas/*.json) del expediente SIME 78.318/2026.

Genera en datos/consolidado/:
  empresas.csv, participaciones.csv, autoridades.csv, beneficiarios_finales.csv,
  historial.csv, declarantes_contactos.csv, personas.csv, personas_roles.csv,
  vinculos.csv, calidad_datos.csv, control_indirecto.csv, salidas_grupo.csv, grafo.graphml

Uso:  python3 -I scripts/consolidar.py
Requiere sólo la biblioteca estándar (networkx es opcional: si está instalado se usa
para centralidad y componentes; si no, se usan implementaciones propias).

El código es tolerante a variaciones de nombres de campos (p. ej. 'nota'/'notas',
'pagina' numérica o texto, fechas parciales AAAA-MM).
"""
import csv, json, re, sys, unicodedata, collections, itertools, pathlib, datetime

ROOT = pathlib.Path(__file__).resolve().parent.parent
DIR_JSON = ROOT / "datos" / "empresas"
DIR_OUT = ROOT / "datos" / "consolidado"
DIR_OUT.mkdir(parents=True, exist_ok=True)

# ---------------------------------------------------------------------------
# Utilidades
# ---------------------------------------------------------------------------
def g(d, *keys, default=None):
    """Obtiene el primer campo presente (tolerante a variantes de nombre)."""
    if not isinstance(d, dict):
        return default
    for k in keys:
        if k in d and d[k] not in (None, ""):
            return d[k]
    return default

def notas(d):
    return g(d, "notas", "nota", "observaciones", default="") or ""

def sin_tildes(s):
    s = unicodedata.normalize("NFKD", s)
    return "".join(c for c in s if not unicodedata.combining(c))

def norm(s):
    s = sin_tildes(str(s or "")).upper()
    s = s.replace("&", " Y ")
    s = re.sub(r"[^A-Z0-9 ]", " ", s)
    return re.sub(r"\s+", " ", s).strip()

def fuente_txt(f):
    if not isinstance(f, dict):
        return ("", "")
    return (str(g(f, "archivo", "file", default="") or ""), str(g(f, "pagina", "paginas", "page", default="") or ""))

def num(x):
    if x is None or x == "":
        return None
    if isinstance(x, (int, float)):
        return float(x)
    try:
        return float(str(x).replace(".", "").replace(",", ".")) if re.fullmatch(r"[\d\.]+,\d+", str(x)) else float(str(x))
    except ValueError:
        return None

def fecha_ok(s):
    s = str(s or "")
    m = re.match(r"(\d{4})(?:-(\d{2}))?(?:-(\d{2}))?", s)
    return s if m else ""

def ruc_dv(base):
    """Dígito verificador del RUC paraguayo (módulo 11, pesos 2..11)."""
    total, k = 0, 2
    for c in reversed(str(base)):
        if k > 11:
            k = 2
        total += int(c) * k
        k += 1
    r = total % 11
    return 11 - r if r > 1 else 0

def write_csv(name, rows, cols):
    with open(DIR_OUT / name, "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=cols, extrasaction="ignore")
        w.writeheader()
        for r in rows:
            w.writerow({c: ("" if r.get(c) is None else r.get(c)) for c in cols})

def fmt_pct(x, nd=2):
    return "" if x is None else round(float(x), nd)

# ---------------------------------------------------------------------------
# Carga
# ---------------------------------------------------------------------------
BASE = list(csv.DictReader(open(ROOT / "datos" / "empresas_base.csv", encoding="utf-8")))
BASE_BY_ID = {b["id"]: b for b in BASE}
FICHAS = {}
for b in BASE:
    p = DIR_JSON / f"{b['id']}.json"
    FICHAS[b["id"]] = json.loads(p.read_text(encoding="utf-8")) if p.exists() else {"id": b["id"]}
IDS = [b["id"] for b in BASE]

def nombre_corto(i):
    return BASE_BY_ID[i]["razon_social"]

# ---------------------------------------------------------------------------
# Reconocimiento de entidades del listado (alias)
# ---------------------------------------------------------------------------
LEGAL = set("""S A SA SAE SAECA SRL EAS SAS SOCIEDAD ANONIMA EMISORA DE CAPITAL ABIERTO RESPONSABILIDAD LIMITADA
UNIPERSONAL SARL R L E C I SACI SAICAG LTDA EMPRESA POR ACCIONES SIMPLIFICADA""".split())

def core(name):
    n = norm(re.sub(r"\(.*?\)", " ", str(name or "")))
    n = n.split(" Y CIA")[0] if " Y CIA" in n else n
    toks = n.split()
    while toks and toks[-1] in LEGAL:
        toks.pop()
    while toks and toks[0] in ("EL", "LA"):
        toks.pop(0)
    return " ".join(toks)

ALIAS = {}
def add_alias(a, i):
    c = core(a)
    if c:
        ALIAS[c] = i
for b in BASE:
    add_alias(b["razon_social"], b["id"])
    add_alias(b["carpeta_mef"], b["id"])
for i, d in FICHAS.items():
    if d.get("razon_social"):
        add_alias(d["razon_social"], i)
    for x in d.get("denominaciones_anteriores") or []:
        add_alias(g(x, "nombre", default=""), i)
for a, i in {
    "ITTI": "itti", "IT CONSULTORES TECNOLOGIA Y ORGANIZACION": "itti", "UENO BANK": "ueno_bank",
    "FINANCIERA UENO": "ueno_bank", "UENO HOLDING": "ueno_holding_saeca", "CREDICENTRO": "ueno_holding_saeca",
    "U HOLDINGS": "ueno_holdings_sarl", "UENO HOLDINGS": "ueno_holdings_sarl", "U HOLDINGS S A R L": "ueno_holdings_sarl",
    "RED DIGITAL": "redisa", "REDISA": "redisa", "RED DIGITAL DE PROCESAMIENTO": "redipro", "REDIPRO": "redipro",
    "SATECSA": "satec", "SATEC": "satec", "RADICE": "terravaz", "RACIDE": "terravaz", "TERRAVAZ": "terravaz",
    "GRUPO VAZQUEZ": "grupo_vazquez", "GV GRUPO VAZQUEZ": "grupo_vazquez", "U PARAGUAY": "u_paraguay",
    "UENO SEGUROS": "ueno_seguros", "UENO CASA DE BOLSA": "ueno_casa_de_bolsa", "DISCOVER PARAGUAY": "discover_paraguay",
    "KOSTAS VIAJES Y TURISMO": "kostas_viajes", "CBS": "cbs", "VINANZAS": "vinanzas", "FRANEDE": "franede",
    "IMPRESION DISTRIBUCION Y LOGISTICA": "idl", "IMPRESION DISTRIBUCION LOGISTICA": "idl", "TECHNOMA": "technoma",
    "UENO ADMINISTRADORA DE FONDOS PATRIMONIALES DE INVERSION": "ueno_afpi", "INTER EXPRESS": "inter_express",
}.items():
    ALIAS[a] = i
RUC2ID = {}
for b in BASE:
    m = re.match(r"(\d{6,8})", b["ruc"] or "")
    if m:
        RUC2ID[m.group(1)] = b["id"]

def match_entidad(name, documento=None):
    """Devuelve el id de una de las 51 entidades si el nombre/RUC corresponde, si no None."""
    doc = str(documento or "")
    m = re.search(r"\b(80\d{6})\b", doc.replace(".", ""))
    if m and m.group(1) in RUC2ID:
        return RUC2ID[m.group(1)]
    first = re.split(r"\s/\s", str(name or ""))[0]
    c = core(first)
    if c in ALIAS:
        return ALIAS[c]
    toks = c.split()
    best = None
    for a, i in ALIAS.items():
        at = a.split()
        if len(at) >= 1 and toks[:len(at)] == at and (best is None or len(at) > len(best[0].split())):
            # evita confundir 'RED DIGITAL DE PROCESAMIENTO' con 'RED DIGITAL'
            best = (a, i)
    if best and (len(best[0].split()) >= 2 or len(toks) == 1 or best[0] in ("ITTI", "CBS", "SATECSA", "RADICE", "RACIDE", "TERRAVAZ", "VINANZAS", "FRANEDE", "TECHNOMA", "REDISA", "REDIPRO")):
        return best[1]
    return None

JUR_RX = re.compile(r"\b(S\.?\s?A\.?|S\.?A\.?E\.?C\.?A|S\.?A\.?E|S\.?R\.?L|E\.?A\.?S|LTDA|COOP|SICAV|S\.?[AÀ]\.?\s?R\.?\s?L|SOCIEDAD|FIDEICOMISO|CAMARA|CÁMARA|CAJA|BANCO|BANK|GRUPO|HOLDINGS?|COOPERATIVE|COMPA[NÑ]IA|SUCESI[OÓ]N|SERFIN|CREDICLAVE|CREDISOLUCION)\b", re.I)

def es_juridica(nombre, tipo=None, documento=None):
    t = (tipo or "").lower()
    if t.startswith("jur"):
        return True
    if t.startswith("fis") or t.startswith("fís"):
        return False
    if re.search(r"\bRUC\s*80\d", str(documento or "")):
        return True
    return bool(JUR_RX.search(str(nombre or "")))

GRUPO = {"grupo_vazquez", "itti", "ueno_holdings_sarl", "u_paraguay", "ueno_bank", "ueno_holding_saeca", "ueno_seguros",
         "ueno_casa_de_bolsa", "ueno_afpi", "redisa", "redipro"}

# ---------------------------------------------------------------------------
# Personas físicas: normalización y deduplicación
# ---------------------------------------------------------------------------
PARTICULAS = {"DE", "DEL", "LA", "LAS", "LOS", "Y", "VDA", "VIUDA", "SR", "SRA", "DR", "DRA", "ING", "LIC", "ABOG", "ESC"}
# Correcciones de CI verificadas en fuentes (ver analisis/metodologia_datos.md)
CI_CORRECCIONES = {"2491546": "2941546"}   # transposición en constancias BF de Kaitel y Tiva

def limpiar_nombre(raw):
    """Devuelve (nombre_normalizado, variantes) a partir del texto tal como figura."""
    s = str(raw or "")
    s = re.sub(r"\((?:fallecido|acciones propias|copropiedad|OCR[^)]*|dudoso[^)]*)\)", " ", s, flags=re.I)
    s = s.split(" / ")[0]
    variantes = [s]
    inside = re.findall(r"\(([^)]*)\)", s)
    outside = re.sub(r"\([^)]*\)", " ", s)
    if "," in outside:  # 'Apellidos, Nombres'
        a, b = outside.split(",", 1)
        outside = f"{b} {a}"
    out_t = [t for t in norm(outside).split() if t not in PARTICULAS]
    best = out_t
    for ins in inside:
        it = [t for t in norm(ins).split() if t not in PARTICULAS]
        if len(it) >= 2 and out_t and it[0] == out_t[0] and len(it) > len(out_t):
            best = it                                        # '(ANDRE GAYOL PIRES)'
        elif len(it) == 1 and out_t and it[0] not in out_t and len(out_t) >= 2 and it[0][0] != out_t[0][0]:
            best = out_t + it if len(out_t) <= 3 else out_t  # 'Nelson Ferreira (Prieto)'
        variantes.append(ins)
    return " ".join(best), variantes

def extraer_ci(doc):
    """CI (sólo dígitos) o documento extranjero; '' si no hay o es ilegible."""
    s = str(doc or "")
    if not s or s.lower() == "none":
        return "", ""
    m = re.search(r"(DNI|PASAPORTE|C[EÉ]DULA (?:TRIBUTARIA )?EXTRANJERA|DOCUMENTO[^0-9]*EXTRANJERO)[^0-9A-Z]*([A-Z]{0,3}[\d\.]{4,12})", s, re.I)
    if m:
        return "EXT:" + re.sub(r"\D", "", m.group(2)), ""
    m = re.search(r"(?:C\.?\s?I\.?|CI/RUC|RUC|C[EÉ]DULA)?[^0-9?]{0,8}(\??[\d\.\?]{5,12})(-\d)?", s)
    if not m:
        return "", ""
    raw = m.group(1)
    if "?" in raw:
        return "", "CI ilegible: " + s
    ci = raw.replace(".", "")
    if ci.startswith("80") and len(ci) == 8:   # RUC de persona jurídica
        return "", ""
    if not (4 <= len(ci) <= 8):
        return "", ""
    obs = ""
    if ci in CI_CORRECCIONES:
        obs = f"CI {ci} corregida a {CI_CORRECCIONES[ci]} (transposición verificada)"
        ci = CI_CORRECCIONES[ci]
    return ci, obs

MENCIONES = []   # cada mención de persona física en un rol

def add_mencion(empresa, nombre, documento, rol, cargo, fecha, vigente, fuente, confianza=None, extra=None):
    if not nombre or es_juridica(nombre, None, documento):
        return None
    sin_par = re.sub(r"\([^)]*\)", "", str(nombre))
    partes = [x.strip() for x in re.split(r";|,", sin_par) if x.strip()]
    if ";" in sin_par or sin_par.count(",") >= 2 or (len(partes) == 2 and all(len(x.split()) >= 3 for x in partes)):
        r = None
        for x in partes:   # lista de varias personas en una misma fila
            r = add_mencion(empresa, x, None, rol, cargo, fecha, vigente, fuente, confianza, extra) or r
        return None
    nn, var = limpiar_nombre(nombre)
    if len(nn.split()) < 2:
        return None
    ci, obs = extraer_ci(documento)
    m = {"empresa_id": empresa, "nombre_raw": str(nombre), "nombre_norm": nn, "variantes": var, "documento": documento or "",
         "ci": ci, "ci_obs": obs, "rol": rol, "cargo": cargo or "", "fecha": fecha or "", "vigente": vigente,
         "fuente": fuente, "confianza": confianza or "", "extra": extra or {}}
    MENCIONES.append(m)
    return m

# ---------------------------------------------------------------------------
# 1. Tablas planas
# ---------------------------------------------------------------------------
empresas_rows, part_rows, aut_rows, bf_rows, hist_rows, decl_rows = [], [], [], [], [], []

for i in IDS:
    d, b = FICHAS[i], BASE_BY_ID[i]
    # --- accionistas
    for k, a in enumerate(d.get("accionistas") or []):
        nombre = g(a, "nombre", default="")
        doc = g(a, "documento", default="")
        tp = g(a, "tipo_persona", default="")
        jur = es_juridica(nombre, tp, doc)
        ent = match_entidad(nombre, doc) if jur else None
        arch, pag = fuente_txt(g(a, "fuente"))
        row = {"empresa_id": i, "empresa": nombre_corto(i), "fila": k, "accionista": nombre,
               "tipo_persona": "juridica" if jur else ("fisica" if nombre else "desconocido"),
               "documento": doc, "id_entidad_accionista": ent or "", "acciones": g(a, "acciones", "cantidad_acciones"),
               "clase_acciones": g(a, "clase_acciones", "clase"), "porcentaje": num(g(a, "porcentaje", "porcentaje_capital", "pct")),
               "porcentaje_calculado": g(a, "porcentaje_calculado"), "votos": g(a, "votos"),
               "fecha_dato": fecha_ok(g(a, "fecha_dato", "fecha")), "vigente": g(a, "vigente"),
               "fuente_archivo": arch, "fuente_pagina": pag, "confianza": g(a, "confianza"), "notas": notas(a)}
        part_rows.append(row)
        if not jur:
            m = add_mencion(i, nombre, doc, "accionista", "Accionista", row["fecha_dato"], row["vigente"], f"{arch} p.{pag}", row["confianza"], {"pct": row["porcentaje"]})
            row["_mencion"] = m
    # --- autoridades
    for a in d.get("autoridades") or []:
        arch, pag = fuente_txt(g(a, "fuente"))
        row = {"empresa_id": i, "empresa": nombre_corto(i), "nombre": g(a, "nombre"), "documento": g(a, "documento"),
               "cargo": g(a, "cargo"), "fecha_asuncion": fecha_ok(g(a, "fecha_asuncion")), "vigencia": g(a, "vigencia"),
               "fecha_dato": fecha_ok(g(a, "fecha_dato")), "vigente": g(a, "vigente"), "fuente_archivo": arch,
               "fuente_pagina": pag, "confianza": g(a, "confianza"), "notas": notas(a)}
        aut_rows.append(row)
        m = add_mencion(i, row["nombre"], row["documento"], "autoridad", row["cargo"], row["fecha_asuncion"] or row["fecha_dato"], row["vigente"], f"{arch} p.{pag}", row["confianza"])
        row["_mencion"] = m
    # --- beneficiarios finales
    for a in d.get("beneficiarios_finales") or []:
        arch, pag = fuente_txt(g(a, "fuente"))
        nombre = g(a, "nombre", default="")
        jur = es_juridica(nombre, None, g(a, "documento"))
        row = {"empresa_id": i, "empresa": nombre_corto(i), "nombre": nombre, "tipo_persona": "juridica" if jur else "fisica",
               "id_entidad": (match_entidad(nombre, g(a, "documento")) or "") if jur else "",
               "documento": g(a, "documento"), "nacionalidad": g(a, "nacionalidad"), "porcentaje": num(g(a, "porcentaje")),
               "tipo_control": g(a, "tipo_control"), "cadena_control": g(a, "cadena_control"), "fecha_dato": fecha_ok(g(a, "fecha_dato")),
               "fuente_archivo": arch, "fuente_pagina": pag, "confianza": g(a, "confianza"), "notas": notas(a)}
        bf_rows.append(row)
        if not jur and not nombre.lower().startswith("listado"):
            row["_mencion"] = add_mencion(i, nombre, row["documento"], "beneficiario_final", row["tipo_control"] or "BF", row["fecha_dato"], True, f"{arch} p.{pag}", row["confianza"], {"pct": row["porcentaje"]})
    # --- historial
    for h in d.get("historial") or []:
        arch, pag = fuente_txt(g(h, "fuente"))
        hist_rows.append({"empresa_id": i, "empresa": nombre_corto(i), "fecha": fecha_ok(g(h, "fecha")), "evento": g(h, "evento", "tipo"),
                          "detalle": g(h, "detalle", "descripcion"), "fuente_archivo": arch, "fuente_pagina": pag})
    # --- declarantes y contactos
    for x in d.get("declarantes_siara") or []:
        arch, pag = fuente_txt(g(x, "fuente"))
        correo = (g(x, "correo", "email", default="") or "").strip()
        dom = correo.split("@")[-1].lower().strip(" .") if "@" in correo else ""
        row = {"empresa_id": i, "empresa": nombre_corto(i), "tipo": "declarante", "nombre": g(x, "nombre"), "documento": g(x, "documento"),
               "correo": correo.lower(), "dominio": dom, "telefono": g(x, "telefono"), "domicilio": "", "fecha": fecha_ok(g(x, "fecha")),
               "fuente_archivo": arch, "fuente_pagina": pag, "notas": notas(x)}
        decl_rows.append(row)
        if row["nombre"]:
            row["_mencion"] = add_mencion(i, row["nombre"], row["documento"], "declarante", "Responsable de la solicitud SIARA", row["fecha"], None, f"{arch} p.{pag}")
    for dom in d.get("correos_dominios") or []:
        decl_rows.append({"empresa_id": i, "empresa": nombre_corto(i), "tipo": "dominio_correo", "dominio": str(dom).lower().lstrip("@")})
    for x in d.get("domicilio") or []:
        arch, pag = fuente_txt(g(x, "fuente"))
        decl_rows.append({"empresa_id": i, "empresa": nombre_corto(i), "tipo": "domicilio", "domicilio": g(x, "direccion", "domicilio"),
                          "fecha": fecha_ok(g(x, "fecha_dato", "fecha")), "fuente_archivo": arch, "fuente_pagina": pag})

# ---------------------------------------------------------------------------
# 2. Deduplicación de personas
# ---------------------------------------------------------------------------
def toks(n):
    return n.split()

def compatibles_ci(a, b):
    """Dos nombres con la misma CI se unen si comparten >=2 tokens o uno contiene al otro."""
    ta, tb = set(toks(a)), set(toks(b))
    return len(ta & tb) >= 2 or (ta <= tb or tb <= ta) and min(len(ta), len(tb)) >= 2

def subnombre(corto, largo):
    """'MIGUEL ALMADA' es subnombre de 'MIGUEL ANGEL ALMADA FRUTOS' (todos sus tokens incluidos y
    su primer token es uno de los dos primeros del nombre largo)."""
    tc, tl = toks(corto), toks(largo)
    return len(tc) >= 2 and len(tc) < len(tl) and set(tc) <= set(tl) and tc[0] in tl[:2] and tc[-1] in tl[1:]

# union-find sobre formas de nombre
forms = collections.OrderedDict()
for m in MENCIONES:
    forms.setdefault(m["nombre_norm"], []).append(m)
parent = {f: f for f in forms}
def find(x):
    while parent[x] != x:
        parent[x] = parent[parent[x]]
        x = parent[x]
    return x
def union(a, b):
    ra, rb = find(a), find(b)
    if ra != rb:
        parent[rb] = ra

conflictos = collections.defaultdict(set)
# (a) por CI
by_ci = collections.defaultdict(set)
for f, ms in forms.items():
    for m in ms:
        if m["ci"]:
            by_ci[m["ci"]].add(f)
for ci, fs in by_ci.items():
    fs = sorted(fs, key=lambda x: -len(x))
    ancla = fs[0]
    for f in fs[1:]:
        if compatibles_ci(ancla, f) or any(compatibles_ci(f, o) for o in fs if o != f and find(o) == find(ancla)):
            union(ancla, f)
        else:
            conflictos[f].add(f"CI {ci} también asignada a '{ancla}'")
            conflictos[ancla].add(f"CI {ci} también asignada a '{f}'")
            # la mención discordante no aporta esa CI a su cluster
            for m in forms[f]:
                if m["ci"] == ci:
                    m["ci_obs"] = (m["ci_obs"] + "; " if m["ci_obs"] else "") + f"CI {ci} pertenece a {ancla} (conflicto; no usada como clave)"
                    m["ci"] = ""
# (b) por nombre contenido (sin CI contradictoria), sólo si el candidato es único
def ci_set(root):
    return {m["ci"] for f in forms if find(f) == root for m in forms[f] if m["ci"]}
def empresas_de(root):
    return {m["empresa_id"] for f in forms if find(f) == root for m in forms[f]}
amb = {}
unidos_nombre = set()
for _pass in range(3):
  amb = {}
  for f in sorted(forms, key=lambda x: -len(x.split())):
    if f in unidos_nombre:
        continue
    cands = {find(o) for o in forms if o != f and subnombre(f, o)}
    cands.discard(find(f))
    if len(cands) > 1:   # desempate: candidato que comparte empresa con la forma abreviada
        mias = {m["empresa_id"] for m in forms[f]}
        comp = {c for c in cands if empresas_de(c) & mias}
        if len(comp) == 1:
            cands = comp
    if len(cands) == 1:
        c = cands.pop()
        a, b = ci_set(find(f)), ci_set(c)
        if a and b and not (a & b):
            conflictos[f].add(f"nombre contenido en '{c}' pero con CI distinta ({','.join(sorted(a))} vs {','.join(sorted(b))}); no se unió")
            continue
        unidos_nombre.add(f)
        if not (a and b):
            conflictos[f].add(f"forma '{f}' unida por nombre (sin CI común)")
        union(c, f)
    elif len(cands) > 1:
        amb[f] = "nombre abreviado ambiguo (no unido); coincide con: " + " | ".join(sorted(cands))
for f, t in amb.items():
    conflictos[f].add(t)

clusters = collections.defaultdict(list)
for f in forms:
    clusters[find(f)].append(f)

personas = []
form2pid = {}
for root, fs in clusters.items():
    ms = [m for f in fs for m in forms[f]]
    cis = collections.Counter(m["ci"].replace("EXT:", "") for m in ms if m["ci"])
    canon = max(fs, key=lambda x: (len(x.split()), sum(1 for m in forms[x]), x))
    disp = [m for m in ms if m["nombre_norm"] == canon]
    disp = max((norm(re.sub(r"\([^)]*\)", " ", m["nombre_raw"].split(" / ")[0])) for m in disp if "," not in m["nombre_raw"]),
               key=lambda x: (len(x.split()), x), default=canon)
    if len(disp.split()) < len(canon.split()):
        disp = canon
    personas.append({"_root": root, "_forms": fs, "_ms": ms, "nombre_canonico": disp, "clave_nombre": canon,
                     "ci": cis.most_common(1)[0][0] if cis else "", "cis": cis})
personas.sort(key=lambda p: (-len({m["empresa_id"] for m in p["_ms"]}), p["nombre_canonico"]))
for n, p in enumerate(personas, 1):
    p["persona_id"] = f"P{n:04d}"
    for f in p["_forms"]:
        form2pid[f] = p["persona_id"]
for m in MENCIONES:
    m["persona_id"] = form2pid[m["nombre_norm"]]
PID = {p["persona_id"]: p for p in personas}
CI2PID = {}
for p in personas:
    for ci in p["cis"]:
        CI2PID.setdefault(ci, p["persona_id"])

def pid_de(nombre, documento=None):
    nn, _ = limpiar_nombre(nombre)
    if nn in form2pid:
        return form2pid[nn]
    ci, _ = extraer_ci(documento)
    return CI2PID.get(ci)

FEDERICO = pid_de("FEDERICO MIGUEL VAZQUEZ VILLASANTI", "CI 2941546")

personas_rows, roles_rows = [], []
for p in personas:
    ms = p["_ms"]
    emp = sorted({m["empresa_id"] for m in ms})
    roles = collections.Counter(m["rol"] for m in ms)
    cargos = sorted({f"{m['empresa_id']}:{m['cargo']}" for m in ms if m["rol"] == "autoridad"})
    variantes = sorted({v.strip() for m in ms for v in [m["nombre_raw"]] + m["variantes"] if v and v.strip()} , key=str.upper)
    obs = sorted({m["ci_obs"] for m in ms if m["ci_obs"]} | {c for f in p["_forms"] for c in conflictos.get(f, [])})
    if len(p["cis"]) > 1:
        obs.append("CI distintas en las fuentes: " + ", ".join(f"{c} (x{n})" for c, n in p["cis"].items()))
    p["n_empresas"] = len(emp)
    personas_rows.append({"persona_id": p["persona_id"], "nombre_canonico": p["nombre_canonico"], "ci": p["ci"],
                          "n_empresas": len(emp), "empresas": "; ".join(emp),
                          "n_menciones": len(ms), "roles": "; ".join(f"{r} ({n})" for r, n in roles.most_common()),
                          "cargos": "; ".join(cargos)[:1500],
                          "es_accionista": int(roles.get("accionista", 0) > 0), "es_bf": int(roles.get("beneficiario_final", 0) > 0),
                          "es_autoridad": int(roles.get("autoridad", 0) > 0), "es_declarante": int(roles.get("declarante", 0) > 0),
                          "formas_unidas": " | ".join(sorted(p["_forms"])), "variantes_texto": " | ".join(variantes)[:1500],
                          "metodo_union": ("CI" if p["cis"] else "nombre") + ("+nombre" if len(p["_forms"]) > 1 else ""),
                          "observaciones_ci_conflictos": " || ".join(obs)})
    for m in ms:
        arch_pag = m["fuente"]
        roles_rows.append({"persona_id": p["persona_id"], "nombre_canonico": p["nombre_canonico"], "empresa_id": m["empresa_id"],
                           "empresa": nombre_corto(m["empresa_id"]), "rol": m["rol"], "cargo": m["cargo"], "fecha": m["fecha"],
                           "vigente": m["vigente"], "pct": (m["extra"] or {}).get("pct"), "nombre_en_fuente": m["nombre_raw"],
                           "documento_en_fuente": m["documento"], "fuente": arch_pag, "confianza": m["confianza"]})

for rows in (part_rows, aut_rows, bf_rows, decl_rows):
    for r in rows:
        m = r.pop("_mencion", None)
        if m:
            r["persona_id"] = m["persona_id"]

# ---------------------------------------------------------------------------
# 3. Participaciones vigentes y en 2024, votos
# ---------------------------------------------------------------------------
def titular_key(r):
    if r["tipo_persona"] == "juridica":
        return r["id_entidad_accionista"] or ("EXT:" + core(r["accionista"]))
    return r.get("persona_id") or ("PX:" + norm(r["accionista"]))

def es_detalle_duplicado(r):
    return str(r["notas"]).startswith("Fila del registro (detalle")

# Porcentajes de votos documentados que prevalecen sobre el cálculo (fuente: notas de las fichas)
VOTOS_DOC = {
    ("ueno_bank", "u_paraguay"): (98.70, "Acta Asamblea N° 99 (13/07/2026): U Paraguay 98,70% de los votos"),
    ("ueno_bank", "grupo_vazquez"): (0.08, "Acta N° 99: Grupo Vázquez 0,08% de los votos"),
    ("itti", "grupo_vazquez"): (90.97, "Calculado: 150.000 OVM×5 + 160.764 OVS = 910.764 de 1.001.201 votos (registro 02/10/2026)"),
    ("itti", "ueno_bank"): (6.79, "Calculado: 68.000 OVS de 1.001.201 votos"),
    ("itti", "ueno_seguros"): (1.21, "Calculado: 12.159 OVS de 1.001.201 votos"),
    ("redipro", "u_paraguay"): (100.0, "Registro 02/10/2026: U Paraguay 100% de los votos (Ueno Bank sólo preferidas)"),
    ("redipro", "ueno_bank"): (0.0, "Preferidas sin voto"),
    ("redisa", "u_paraguay"): (99.99, "Registro: 9.131 OVS de 9.132 votos; preferidas sin voto"),
    ("redisa", "ueno_bank"): (0.01, "1 OVS; 23.623 preferidas sin voto"),
    ("ueno_seguros", "u_paraguay"): (90.58, "Calculado: 5.648 OVS + 55.135 OVM×5 sobre 310.593 votos (OVM 5 votos, Art. 9)"),
    ("ueno_seguros", "grupo_vazquez"): (6.43, "Calculado: 3.992 OVM×5 sobre 310.593 votos"),
}

# Porcentajes de capital documentados que prevalecen cuando las filas vigentes mezclan bases distintas
CAP_DOC = {
    ("redisa", "u_paraguay"): 27.88,   # 9.132 de 32.756 acciones (OVS + preferidas) al 29/05/2026
    ("redisa", "ueno_bank"): 72.12,    # 23.624 de 32.756 acciones
}

def snapshot(empresa, corte="vigente"):
    """Filas de participación para el corte pedido. 'vigente' = filas marcadas vigentes (o, si ninguna lo está,
    las de fecha más reciente). '2024' = la foto más reciente con fecha_dato <= 2024-12-31."""
    rows = [r for r in part_rows if r["empresa_id"] == empresa and not es_detalle_duplicado(r)]
    if corte == "vigente":
        sel = [r for r in rows if r["vigente"] is True]
        if not sel:
            nn = [r for r in rows if r["vigente"] is None]
            if nn:
                mx = max(r["fecha_dato"] for r in nn)
                sel = [r for r in nn if r["fecha_dato"] == mx]
        return sel
    lim = "2024-12-31"
    rows = [r for r in rows if r["fecha_dato"] and r["fecha_dato"] <= lim]
    if not rows:
        return []
    mx = max(r["fecha_dato"] for r in rows)
    exacta = [r for r in rows if r["fecha_dato"] == mx]
    arch = {r["fuente_archivo"] for r in exacta}
    mismo_doc = [r for r in rows if r["fuente_archivo"] in arch]
    ult = {}
    for r in sorted(mismo_doc, key=lambda r: r["fecha_dato"]):
        ult.setdefault(titular_key(r), [])
        if ult[titular_key(r)] and ult[titular_key(r)][0]["fecha_dato"] != r["fecha_dato"]:
            ult[titular_key(r)] = []
        ult[titular_key(r)].append(r)
    sel = [r for v in ult.values() for r in v]
    s = sum(r["porcentaje"] or 0 for r in sel)
    return sel if s <= 101.5 else exacta

def agregar(empresa, sel, corte):
    """Agrega por titular: % capital, % votos (documentado, calculado o = capital)."""
    agg = collections.OrderedDict()
    for r in sel:
        k = titular_key(r)
        if k == empresa or (k.startswith("EXT:") and match_entidad(r["accionista"]) == empresa):
            continue   # acciones propias en cartera
        a = agg.setdefault(k, {"titular": k, "nombre": r["accionista"], "tipo": r["tipo_persona"], "cap": 0.0, "cap_ok": False,
                               "votos_abs": 0.0, "votos_ok": True, "fechas": set(), "fuentes": set(), "confianza": set()})
        if r["porcentaje"] is not None:
            a["cap"] += r["porcentaje"]; a["cap_ok"] = True
        v = num(r["votos"])
        if v is None:
            a["votos_ok"] = False
        else:
            a["votos_abs"] += v
        a["fechas"].add(r["fecha_dato"]); a["fuentes"].add(f"{r['fuente_archivo']} p.{r['fuente_pagina']}"); a["confianza"].add(str(r["confianza"]))
    vals = list(agg.values())
    all_v = vals and all(a["votos_ok"] for a in vals) and sum(a["votos_abs"] for a in vals) > 0
    tot_v = sum(a["votos_abs"] for a in vals) if all_v else None
    for a in vals:
        doc = VOTOS_DOC.get((empresa, a["titular"])) if corte == "vigente" else None
        if doc:
            a["vot"], a["vot_origen"] = doc
        elif all_v:
            a["vot"], a["vot_origen"] = 100.0 * a["votos_abs"] / tot_v, "calculado sobre votos de las filas del mismo corte"
        else:
            a["vot"], a["vot_origen"] = (a["cap"] if a["cap_ok"] else None), "igual a % de capital (sin dato de votos)"
        a["cap"] = a["cap"] if a["cap_ok"] else None
        if corte == "vigente" and (empresa, a["titular"]) in CAP_DOC:
            a["cap"] = CAP_DOC[(empresa, a["titular"])]
            a["vot_origen"] = (a.get("vot_origen") or "") + "; % capital documentado (CAP_DOC)"
    return vals

# Reconstrucción documentada de la situación a 2024 para entidades cuya foto <=2024 falta o es parcial.
# Cada fila cita la evidencia de las fichas (fila previa a la transferencia de 2025-2026).
SITUACION_2024_MANUAL = {
    "itti": [("grupo_vazquez", 94.41, 94.4, "Registro folio 8 (02/01/2026) refleja tenencia de GV previa a 2025; Asamblea N° 39 (12/05/2025)"),
             ("ueno_seguros", 3.03, 1.0, "Títulos comprados a GV el 23/03/2023")],
    "u_paraguay": [("ueno_holdings_sarl", 99.99, 99.99, "Registro de acciones: integraciones de U Holdings desde 10/03/2023 (CONTRADICCIÓN: actas 21/07/2025 dan GV 70,36% votos)")],
    "ueno_seguros": [("grupo_vazquez", None, "control", "Notas del registro: compras de GV en 2023-2024 y canje GV→U Paraguay el 30/06/2025 (aprobado SIS 30/12/2025); GV mayoritario, % 2024 no determinado"),
                     ("u_paraguay", None, None, "748 acciones cedidas por GV a U Paraguay el 28/06/2024")],
    "grupo_vazquez": [(FEDERICO, None, "control", "Constancias BF de Tiva (23/01/2025) y Kaitel (04/07/2025): Federico M. Vázquez V. 'accionista mayoritario en Grupo Vázquez'; registro de GV sólo disponible a 27/03/2026")],
    "ueno_bank": [("grupo_vazquez", 94.91, 94.91, "Acta N° 90 (Asamblea Extraordinaria 25/03/2024): GV 94,91% de los votos")],
    "kaitel": [("Carlos F. Impagliatelli Bareiro y Vanessa E. Godoy Ayala (50 cuotas, reparto no indicado)", None, None, "Socios hasta la cesión a WOM77/IDL del 25/03/2025")],
    "ueno_casa_de_bolsa": [("grupo_vazquez", 88.6, 88.6, "Registro folio 6 (27/06/2025), anterior a la transferencia a U Paraguay"),
                           ("u_paraguay", 11.4, 11.4, "Registro folio 6 (27/06/2025)")],
    "redisa": [("itti", 99.99, 99.99, "Registro: cadena Financiera Ueno→Ueno Holding→ITTI (2023)→GV (30/06/2025)→U Paraguay")],
    "redipro": [("itti", None, "control", "BF 26/06/2025: Federico M. Vázquez vía GV→ITTI–Ueno Holding (62,87% / 77,75% votos); reparto no documentado")],
    "grupo_m": [("itti", 99.02, 99.02, "Registro: acciones 1-1624 de ITTI hasta la venta del 30/09/2025"), ("grupo_vazquez", 0.98, 0.98, "Acciones 1625-1640 hasta 30/09/2025")],
    "grupo_hendy": [("itti", 99.04, 99.04, "Registro: 1.951 acciones de ITTI hasta 30/09/2025"), ("grupo_vazquez", 0.96, 0.96, "19 acciones hasta 30/09/2025")],
    "office_design": [("grupo_vazquez", None, "control", "Esc. 190 (30/10/2025): GV e ITTI ceden la totalidad de las cuotas; reparto ilegible (control conjunto GV/ITTI)"), ("itti", None, None, "Idem")],
    "mowi": [("itti", 100.0, 100.0, "Registro: ITTI 8.000 acciones (compras a GV 29/12/2022 y a Ueno Holding 30/06/2023) hasta 19/05/2025")],
    "franede": [("grupo_vazquez", 99.62, 99.62, "Registro folio 2: GV 2.618 acciones hasta la transferencia a Mauro Vargas (30/06/2025); fecha de ingreso de GV no documentada")],
    "v_media": [("grupo_vazquez", 99.9, 99.9, "Asambleas N° 26-27 (07/10/2025) con GV 99,90% (Invercentro S.A.); tenencia previa a 2025 no documentada")],
    "discover_paraguay": [("itti", 74.79, 74.79, "Suscripción ITTI 19/02/2024")],
    "hanoi": [("itti", 72.76, 72.76, "Registro: acciones a nombre de ITTI desde 14/03/2024")],
    "idl": [("itti", 99.23, 99.23, "Registro: títulos suscritos 2021-2022 (J. Fleischman fusionada en ITTI)"), ("grupo_vazquez", 0.77, 0.77, "Registro 2021-2022")],
    "tiva": [("itti", 60.0, 60.0, "RA ene-2025 (tenencia previa)")],
    "ueno_afpi": [("ueno_casa_de_bolsa", 90.0, 90.0, "Asamblea Extraordinaria N° 3 (11/09/2023)"), ("ueno_bank", 10.0, 10.0, "Acción N° 10 transferida por Sergio Pizurno a Ueno Bank el 31/05/2024")],
}

# Vínculos de control declarados (sin porcentaje) que no surgen de un registro de acciones
CONTROL_DECLARADO = [
    (None, "ueno_holdings_sarl", "BF declarado (condición E: control o cadena de titularidad) en el listado BF de Redipro (2026-10): Federico M. Vázquez Villasanti controla a través de U Holdings S.à r.l.; la composición de U Holdings no consta"),
    ("itti", "EXT:WOM77", "BF de Kaitel (04/07/2025): cadena WOM 77 S.A. – ITTI S.A.E.C.A. – Grupo Vázquez; WOM 77 preside César Astigarraga"),
]

def construir_red(corte):
    """Devuelve dict empresa -> lista de titulares agregados."""
    red = {}
    for i in IDS:
        sel = snapshot(i, corte)
        vals = agregar(i, sel, corte)
        if corte == "2024" and SITUACION_2024_MANUAL.get(i):
            vals = []   # la reconstrucción documentada reemplaza a la foto automática (desactualizada o parcial)
            for t, cap, vot, ev in SITUACION_2024_MANUAL[i]:
                vals.append({"titular": t, "nombre": etiqueta(t), "tipo": "juridica" if t in BASE_BY_ID else "otro", "cap": cap,
                             "vot": None if vot == "control" else vot, "declarado": vot == "control",
                             "vot_origen": "reconstrucción 2024: " + ev, "fechas": {"<=2024"}, "fuentes": {ev}, "confianza": {"media"}})
        red[i] = vals
    if FEDERICO:
        for src, dst, ev in CONTROL_DECLARADO:
            s = src or FEDERICO
            red.setdefault(dst, [])
            if not any(a["titular"] == s for a in red[dst]):
                red[dst].append({"titular": s, "nombre": etiqueta(s), "tipo": "declarado", "cap": None, "vot": None,
                                 "vot_origen": "control declarado: " + ev, "fechas": set(), "fuentes": {ev}, "confianza": {"media"}, "declarado": True})
    return red

def etiqueta(k):
    if k in BASE_BY_ID:
        return nombre_corto(k)
    if k in PID:
        return PID[k]["nombre_canonico"].title()
    if k.startswith("EXT:"):
        return k[4:].title()
    return k

def controlante(red):
    """Controlante directo por mayoría de votos (>50%), o por mayoría de grupo (titulares bajo el mismo
    controlante último que juntos superan 50%), o declarado."""
    ctrl = {}
    for y, vals in red.items():
        if "fideicomiso" in y:
            continue   # los fideicomitentes no son accionistas: no se computa control societario
        best = max((a for a in vals if a.get("vot") is not None), key=lambda a: a["vot"], default=None)
        if best and best["vot"] > 50:
            ctrl[y] = (best["titular"], best["vot"], "mayoría directa de votos")
        else:
            dec = [a for a in vals if a.get("declarado")]
            if dec:
                ctrl[y] = (dec[0]["titular"], None, "control declarado (BF)" if "BF" in dec[0].get("vot_origen", "") or "declarado" in dec[0].get("vot_origen", "") else "control documentado sin % (reconstrucción 2024)")
    def ultimo(x, seen=()):
        while x in ctrl and x not in seen:
            seen = seen + (x,)
            x = ctrl[x][0]
        return x
    for _ in range(3):
        for y, vals in red.items():
            if y in ctrl or "fideicomiso" in y:
                continue
            grupos = collections.defaultdict(float)
            for a in vals:
                if a.get("vot"):
                    grupos[ultimo(a["titular"])] += a["vot"]
            if grupos:
                u, v = max(grupos.items(), key=lambda kv: kv[1])
                if v > 50:
                    mejor = max((a for a in vals if a.get("vot") and ultimo(a["titular"]) == u), key=lambda a: a["vot"])
                    ctrl[y] = (mejor["titular"], v, f"mayoría de grupo ({round(v, 2)}% votos sumando titulares bajo {etiqueta(u)})")
    return ctrl, ultimo

def integrada(red, raiz, objetivo, maxdepth=8):
    """Participación integrada en el capital: suma sobre todas las cadenas del producto de %."""
    hijos = collections.defaultdict(list)
    for y, vals in red.items():
        for a in vals:
            if a.get("cap"):
                hijos[a["titular"]].append((y, a["cap"] / 100.0))
    total, caminos = 0.0, []
    def dfs(n, acc, path):
        nonlocal total
        if len(path) > maxdepth:
            return
        for y, f in hijos.get(n, []):
            if y in path:
                continue
            if y == objetivo:
                total += acc * f
                caminos.append((path + [y], acc * f))
            else:
                dfs(y, acc * f, path + [y])
    dfs(raiz, 1.0, [raiz])
    return total * 100.0, caminos

RAICES = [("ueno_holdings_sarl", "U Holdings S.à r.l."), ("grupo_vazquez", "Grupo Vázquez S.A.E."), (FEDERICO, "Federico M. Vázquez Villasanti (vía GV y directo)"),
          ("itti", "ITTI"), ("u_paraguay", "U Paraguay"), ("ueno_bank", "Ueno Bank")]

control_rows = []
REDES, CTRLS = {}, {}
for corte in ("vigente", "2024"):
    red = construir_red(corte)
    ctrl, ultimo = controlante(red)
    REDES[corte], CTRLS[corte] = red, (ctrl, ultimo)
    for i in IDS:
        vals = red.get(i, [])
        c = ctrl.get(i)
        cadena, x, seen = [nombre_corto(i)], i, set()
        while x in ctrl and x not in seen:
            seen.add(x)
            t, v, tipo = ctrl[x]
            cadena.append(f"{etiqueta(t)} ({'%.2f%% votos' % v if v is not None else 'declarado'})")
            x = t
        ult = ultimo(i) if c else ""
        row = {"corte": corte, "entidad_id": i, "razon_social": nombre_corto(i),
               "n_titulares_dato": len(vals), "fechas_dato": "; ".join(sorted({f for a in vals for f in a["fechas"] if f})),
               "controlante_directo": etiqueta(c[0]) if c else "", "controlante_directo_id": c[0] if c else "",
               "pct_votos_controlante_directo": fmt_pct(c[1]) if c and c[1] is not None else "",
               "tipo_control": c[2] if c else ("no aplica (fideicomiso): fideicomitente desarrollador RADICE S.A. = Terravaz S.A.E., controlada por GV" if "fideicomiso" in i else ("sin datos de accionistas" if not vals else "sin controlante mayoritario identificado")),
               "controlante_ultimo": etiqueta(ult) if c else "", "controlante_ultimo_id": ult if c else "",
               "cadena_control": " ← ".join(cadena) if c else ""}
        tot_grupo = 0.0
        for rk, rn in RAICES:
            if not rk or rk == i:
                row[f"integ_{rk if rk in BASE_BY_ID else 'federico'}"] = ""
                continue
            v, cam = integrada(red, rk, i)
            row[f"integ_{rk if rk in BASE_BY_ID else 'federico'}"] = fmt_pct(v, 3) if v else ""
        ugh = num(row.get("integ_ueno_holdings_sarl")) or 0
        gvh = num(row.get("integ_grupo_vazquez")) or 0
        fd = 0.0
        if FEDERICO:
            # participación directa de Federico (no a través de GV)
            for a in vals:
                if a["titular"] == FEDERICO and a.get("cap"):
                    fd += a["cap"]
        row["integ_grupo_total"] = fmt_pct(ugh + gvh + (fd if i not in ("grupo_vazquez",) else 0), 3) if (ugh or gvh or fd) else ""
        if i in ("ueno_holdings_sarl", "grupo_vazquez"):
            row["integ_grupo_total"] = 100.0
        row["en_grupo_por_control"] = int(bool(c) and (ult in (FEDERICO, "grupo_vazquez", "ueno_holdings_sarl") or i in ("grupo_vazquez", "ueno_holdings_sarl")))
        row["notas"] = "; ".join(sorted({a["vot_origen"] for a in vals if a.get("vot_origen") and not a["vot_origen"].startswith("igual")}))[:800]
        control_rows.append(row)

# ---------------------------------------------------------------------------
# 4. Salidas del grupo 2025-2026 y transferencias internas
# ---------------------------------------------------------------------------
salidas = []
red_v = REDES["vigente"]
for i in IDS:
    if i in GRUPO:
        continue
    prev = [r for r in part_rows if r["empresa_id"] == i and r["id_entidad_accionista"] in GRUPO | {"ueno_holding_saeca"} and r["vigente"] is False]
    vig_grupo = [a for a in red_v.get(i, []) if a["titular"] in GRUPO]
    if prev and not vig_grupo:
        hs = [h for h in hist_rows if h["empresa_id"] == i and h["evento"] == "transferencia_acciones" and (h["fecha"] or "") >= "2025"
              and re.search(r"ITTI|GRUPO V[AÁ]ZQUEZ|GV|UENO", str(h["detalle"]), re.I)]
        fecha = min((h["fecha"] for h in hs), default=max(r["fecha_dato"] for r in prev))
        compradores = [f"{etiqueta(a['titular'])} ({fmt_pct(a['cap'])}%)" for a in red_v.get(i, []) if a.get("cap")]
        salidas.append({"empresa_id": i, "empresa": nombre_corto(i), "fecha_salida": fecha,
                        "vendedores_grupo": "; ".join(sorted({etiqueta(r["id_entidad_accionista"]) for r in prev})),
                        "titulares_actuales": "; ".join(compradores),
                        "titulares_actuales_ids": "; ".join(a["titular"] for a in red_v.get(i, []) if a.get("cap")),
                        "detalle": " | ".join(f"{h['fecha']}: {h['detalle']}" for h in hs)[:900],
                        "fuente": "; ".join(sorted({f"{h['fuente_archivo']} p.{h['fuente_pagina']}" for h in hs}))})
write_csv("salidas_grupo.csv", salidas, ["empresa_id", "empresa", "fecha_salida", "vendedores_grupo", "titulares_actuales", "titulares_actuales_ids", "detalle", "fuente"])

# ---------------------------------------------------------------------------
# 5. Segmentación
# ---------------------------------------------------------------------------
CTRL_V, ULT_V = CTRLS["vigente"]
SEG = {}
SEG_JUST = {}
NUCLEO = ["ueno_bank", "ueno_seguros", "ueno_casa_de_bolsa", "ueno_afpi", "redisa", "redipro"]
HOLD = ["ueno_holdings_sarl", "u_paraguay", "grupo_vazquez", "itti", "ueno_holding_saeca"]
# vínculos indirectos/minoritarios: justificación textual basada en las fichas
INDIRECTOS = {
    "bic": "Participada minoritaria: Ueno Bank 7,46%, Ueno Holding 1,57%, ITTI 1,57%, Red Digital 1,57% y Vinanzas 1,30% (≈13,5% el conjunto) en el registro 22/09/2026; sin control.",
    "solucion_efectiva": "Participada minoritaria: Grupo Vázquez 8,1% del capital (registro 05/05/2025); controlan Achón Fornells / Electroban.",
    "fideicomiso_shopping_costanera": "Vínculo indirecto: su fideicomitente desarrollador RADICE S.A. es Terravaz S.A.E. (controlada 97,33% por GV desde 2025). Verificado.",
    "nubicom_paraguay": "Vínculo por directorio: Guillermo Vázquez Muniagurria fue Presidente (AGO N° 1, 13/09/2025) hasta jun-2026; secretarios de asamblea Algorta/Almada; escribana del grupo. Sin participación accionaria del grupo.",
    "technoma": "Vínculo por personas: accionistas/directores Enrique J. Vera Moreira (cesionario de Office Design) y Sergio Pizurno (ex accionista de Ueno AFPI, director de Grupo M, accionista de MOWI); Miguel Almada representó a accionistas; sede en Torres del Paseo.",
    "aime_corredores": "Vínculo por personas: Presidente Gloria E. Villasanti Farinha (compradora de V Media), director suplente Miguel Á. Almada Frutos; declarante Alan Campos (@uenoholding.com.py); sede Torres del Paseo, Torre 3 piso 11.",
    "gsr": "Vínculo débil por persona: accionista y representante José Augusto Sala Cardozo, comprador de acciones de MOWI a ITTI (2025). Sin otra relación documental.",
    "cbs": "Vínculo débil: CBS compró 0,1% de V Media a Grupo Vázquez (23/03/2026) y fue representada por Mauro Vargas. Sus accionistas (Chaco-I Trader 90%) no se vinculan al grupo.",
}
for i in IDS:
    c = CTRL_V.get(i)
    ult = ULT_V(i) if c else None
    if i in NUCLEO:
        SEG[i] = "nucleo_financiero_ueno"
        SEG_JUST[i] = f"Entidad financiera/de pagos del grupo Ueno; controlante directo {etiqueta(c[0]) if c else 's/d'}" + (f" ({fmt_pct(c[1])}% votos)" if c and c[1] is not None else "") + f"; controlante último {etiqueta(ult) if ult else 's/d'}."
    elif i in HOLD:
        SEG[i] = "holding_controlante"
        SEG_JUST[i] = {"ueno_holdings_sarl": "Holding luxemburguesa, titular de 97,99% de U Paraguay; composición propia no documentada (BF declarado: Federico M. Vázquez V.).",
                       "u_paraguay": "Holding local del núcleo financiero (Ueno Bank, Ueno Seguros, Casa de Bolsa, Red Digital, Redipro); 97,99% de U Holdings.",
                       "grupo_vazquez": "Holding familiar: Federico M. Vázquez Villasanti 75,94% del capital y ≈94% de los votos; controla ITTI y las sociedades no financieras.",
                       "itti": "Holding intermedio/tecnológica: GV 77,46% (≈91% de votos), Ueno Bank 16,95%; titular de la mayoría de las sociedades operativas no financieras.",
                       "ueno_holding_saeca": "Ex holding (ex Credicentro); absorbida por Grupo Vázquez por fusión (Esc. 131, 16/07/2025). Entidad extinguida."}[i]
    elif any(s["empresa_id"] == i for s in salidas):
        s = next(s for s in salidas if s["empresa_id"] == i)
        SEG[i] = "ex_vinculada"
        SEG_JUST[i] = f"Salió del grupo el {s['fecha_salida']}: vendedores {s['vendedores_grupo']}; titulares actuales {s['titulares_actuales']}."
    elif c and (ult in (FEDERICO, "grupo_vazquez", "ueno_holdings_sarl", "itti")):
        SEG[i] = "controlada_itti_gv"
        SEG_JUST[i] = f"Controlante directo {etiqueta(c[0])}" + (f" ({fmt_pct(c[1])}% votos)" if c[1] is not None else "") + f" — {c[2]}; controlante último {etiqueta(ult)}."
    elif i in INDIRECTOS:
        SEG[i] = "participada_minoritaria_o_vinculo_indirecto"
        SEG_JUST[i] = INDIRECTOS[i]
    else:
        SEG[i] = "sin_vinculo_detectado"
        SEG_JUST[i] = "No se detectó participación, autoridades, beneficiarios, declarantes ni correos comunes con el grupo en la documentación remitida."
# Casos que requieren criterio explícito (control de hecho / declarado)
SEG_OVERRIDE = {
    "red_uts_paraguay": ("controlada_itti_gv", "Control de hecho: ITTI es el mayor accionista (40,23%) frente a tres personas físicas de ≈20% cada una; la constancia BF declara a Federico M. Vázquez V. (36,46%, condición B)."),
    "fintux": ("controlada_itti_gv", "ITTI 30% (mayor accionista) y la constancia BF (05/11/2026) declara a Grupo Vázquez por 'condición de control' vía ITTI."),
}
for i, (s, j) in SEG_OVERRIDE.items():
    if SEG.get(i) not in ("ex_vinculada",):
        SEG[i], SEG_JUST[i] = s, j

# ---------------------------------------------------------------------------
# 6. Vínculos entre entidades
# ---------------------------------------------------------------------------
vinc = []
def add_v(a, b, tipo, peso, detalle, fuente="", fecha="", vigente=""):
    vinc.append({"origen": a, "origen_nombre": etiqueta(a), "destino": b, "destino_nombre": etiqueta(b), "tipo": tipo,
                 "peso": fmt_pct(peso, 4) if isinstance(peso, float) else peso, "detalle": detalle, "fecha": fecha, "vigente": vigente, "fuente": fuente})

# (a) participación directa (titular persona jurídica -> empresa)
seen = set()
for r in part_rows:
    if r["tipo_persona"] != "juridica":
        continue
    src = titular_key(r)
    if src == r["empresa_id"]:
        continue
    key = (src, r["empresa_id"], r["fecha_dato"], r["vigente"])
    if key in seen or es_detalle_duplicado(r):
        continue
    seen.add(key)
    agg = [x for x in part_rows if titular_key(x) == src and x["empresa_id"] == r["empresa_id"] and x["fecha_dato"] == r["fecha_dato"] and x["vigente"] == r["vigente"] and not es_detalle_duplicado(x) and x["porcentaje"] is not None]
    pct = sum(x["porcentaje"] for x in agg) if agg else None
    add_v(src, r["empresa_id"], "participacion_directa" if r["vigente"] is not False else "participacion_historica",
          pct, f"{r['accionista']}: {fmt_pct(pct)}% del capital al {r['fecha_dato']}", f"{r['fuente_archivo']} p.{r['fuente_pagina']}", r["fecha_dato"], r["vigente"])

# (b) personas comunes por rol
def pares_por_rol(rol_filter, tipo):
    porp = collections.defaultdict(lambda: collections.defaultdict(set))
    for m in MENCIONES:
        if rol_filter(m):
            porp[m["persona_id"]][m["empresa_id"]].add(m["cargo"] or m["rol"])
    pares = collections.defaultdict(list)
    for pid, emps in porp.items():
        for a, b in itertools.combinations(sorted(emps), 2):
            pares[(a, b)].append(pid)
    for (a, b), pids in pares.items():
        add_v(a, b, tipo, len(pids), "; ".join(f"{PID[p]['nombre_canonico'].title()} [{', '.join(sorted(porp[p][a]))[:60]} / {', '.join(sorted(porp[p][b]))[:60]}]" for p in pids)[:900])
pares_por_rol(lambda m: m["rol"] == "autoridad", "autoridad_comun")
pares_por_rol(lambda m: m["rol"] == "beneficiario_final", "bf_comun")
pares_por_rol(lambda m: m["rol"] == "accionista", "accionista_fisico_comun")
pares_por_rol(lambda m: m["rol"] == "declarante", "mismo_declarante")
# BF persona jurídica común (p. ej. GV declarado BF)
bfj = collections.defaultdict(set)
for r in bf_rows:
    if r["tipo_persona"] == "juridica" and r["id_entidad"]:
        bfj[r["empresa_id"]].add(r["id_entidad"])
        add_v(r["id_entidad"], r["empresa_id"], "bf_declarado_persona_juridica", r["porcentaje"], f"{r['nombre']} declarado BF ({r['tipo_control']})", f"{r['fuente_archivo']} p.{r['fuente_pagina']}", r["fecha_dato"])

# (c) domicilio
def dom_key(s):
    n = norm(s)
    if re.search(r"TORRES? DEL PASEO|SANTA TERESA (N )?1827|PASEO LA GALERIA", n):
        return "TORRES DEL PASEO / PASEO LA GALERIA (AVDA. SANTA TERESA 1827, ASUNCION)"
    n = re.sub(r"\b(AVDA|AVENIDA|CALLE|N|NRO|ESQ|ESQUINA|C|CASI|ASUNCION|PARAGUAY)\b", " ", n)
    return re.sub(r"\s+", " ", n).strip()
domk = collections.defaultdict(set)
for r in decl_rows:
    if r["tipo"] == "domicilio" and r.get("domicilio"):
        k = dom_key(r["domicilio"])
        if len(k) > 8:
            domk[k].add(r["empresa_id"])
for k, emps in domk.items():
    for a, b in itertools.combinations(sorted(emps), 2):
        add_v(a, b, "mismo_domicilio", 1, k)

# (d) correos y dominios
PUBLICOS = {"gmail.com", "hotmail.com", "yahoo.com", "outlook.com", "live.com", "hotmail.es", "yahoo.com.ar", "icloud.com"}
corr, domi = collections.defaultdict(set), collections.defaultdict(set)
for r in decl_rows:
    c = (r.get("correo") or "").lower()
    if c:
        corr[c].add(r["empresa_id"])
    dmn = (r.get("dominio") or "").lower()
    if dmn and dmn not in PUBLICOS:
        domi[dmn].add(r["empresa_id"])
for c, emps in corr.items():
    for a, b in itertools.combinations(sorted(emps), 2):
        add_v(a, b, "mismo_correo", 1, c)
for dmn, emps in domi.items():
    for a, b in itertools.combinations(sorted(emps), 2):
        add_v(a, b, "mismo_dominio_correo", 1, dmn)

# (e) transferencias de acciones entre entidades (historial que menciona >=1 entidad del listado distinta de la emisora)
ent_rx = sorted(((a, i) for a, i in ALIAS.items() if len(a) >= 4), key=lambda x: -len(x[0]))
for h in hist_rows:
    if h["evento"] not in ("transferencia_acciones", "fusion", "aumento_capital"):
        continue
    txt = " " + norm(h["detalle"]) + " "
    found = set()
    for a, i in ent_rx:
        if f" {a} " in txt and i != h["empresa_id"]:
            found.add(i)
            txt = txt.replace(f" {a} ", " ")
    for i in found:
        add_v(i, h["empresa_id"], "transferencia_acciones" if h["evento"] == "transferencia_acciones" else h["evento"], 1,
              str(h["detalle"])[:400], f"{h['fuente_archivo']} p.{h['fuente_pagina']}", h["fecha"])

# vínculos declarados por los extractores (texto) que nombran otra entidad del listado
for i in IDS:
    for v in FICHAS[i].get("vinculos") or []:
        ent = match_entidad(g(v, "entidad_o_persona", default=""))
        if ent and ent != i and g(v, "tipo") not in ("accionista_de", "participada"):
            arch, pag = fuente_txt(g(v, "fuente"))
            add_v(i, ent, "mencion_extractor:" + str(g(v, "tipo", default="otro")), 1, str(g(v, "detalle", default=""))[:400], f"{arch} p.{pag}")

write_csv("vinculos.csv", vinc, ["origen", "origen_nombre", "destino", "destino_nombre", "tipo", "peso", "detalle", "fecha", "vigente", "fuente"])

# ---------------------------------------------------------------------------
# 7. Calidad de datos
# ---------------------------------------------------------------------------
cal = []
def q(i, tipo, sev, det):
    cal.append({"empresa_id": i, "empresa": nombre_corto(i) if i in BASE_BY_ID else i, "tipo": tipo, "severidad": sev, "detalle": det})

for i in IDS:
    d = FICHAS[i]
    b = BASE_BY_ID[i]
    ruc = str(d.get("ruc") or b["ruc"] or "")
    m = re.match(r"(\d{6,8})-(\d)", ruc)
    if m and ruc_dv(m.group(1)) != int(m.group(2)):
        q(i, "ruc_dv_invalido", "alta", f"RUC {ruc}: DV calculado {ruc_dv(m.group(1))}")
    if not ruc or ruc == "None":
        q(i, "sin_ruc", "media", "Entidad sin RUC en los documentos")
    if b["ruc"] and d.get("ruc") and re.sub(r"\D", "", b["ruc"]) != re.sub(r"\D", "", str(d["ruc"])):
        q(i, "ruc_distinto_base", "media", f"Base {b['ruc']} vs ficha {d['ruc']}")
    # RUC de terceros con DV erróneo citados en participaciones
    for r in part_rows:
        if r["empresa_id"] != i:
            continue
        for mm in re.finditer(r"\b(80\d{6})-(\d{1,2})\b", str(r["documento"] or "")):
            if ruc_dv(mm.group(1)) != int(mm.group(2)):
                q(i, "ruc_tercero_dv_invalido", "baja", f"{r['accionista']}: RUC {mm.group(0)} (DV correcto {ruc_dv(mm.group(1))})")
    sel = snapshot(i, "vigente")
    if not d.get("accionistas"):
        q(i, "sin_accionistas", "alta", "No se declaran accionistas/socios en los documentos remitidos")
    elif not sel:
        q(i, "sin_foto_vigente", "media", "Hay accionistas históricos pero ninguno marcado vigente")
    else:
        pcts = [r["porcentaje"] for r in sel if r["porcentaje"] is not None]
        s = sum(pcts)
        if pcts and not (98.5 <= s <= 101.5):
            q(i, "suma_pct_vigente", "media" if 90 <= s <= 110 else "alta", f"La suma de % de los accionistas vigentes es {round(s, 2)}% ({len(pcts)} filas)")
        if len(pcts) < len(sel):
            q(i, "pct_faltante", "media", f"{len(sel) - len(pcts)} fila(s) vigentes sin porcentaje")
        fechas = sorted({r["fecha_dato"] for r in sel})
        if len(fechas) > 1:
            q(i, "foto_vigente_mixta", "baja", "Filas vigentes con fechas distintas: " + ", ".join(fechas))
        srcs = {r["fuente_archivo"] for r in sel}
        if len(srcs) > 1 and i in ("mowi", "ueno_bank", "intertours"):
            q(i, "fuentes_contradictorias", "media", "Las filas vigentes provienen de documentos distintos: " + "; ".join(sorted(srcs)))
    if any(r["empresa_id"] == i and es_detalle_duplicado(r) for r in part_rows):
        q(i, "filas_detalle_y_total", "baja", "El registro trae filas por título y totales; se usan los totales para el cálculo")
    if any(r["empresa_id"] == i and r["porcentaje_calculado"] for r in part_rows):
        q(i, "pct_calculado", "baja", "Porcentajes calculados por el extractor (no declarados en el documento)")
    nb = sum(1 for r in part_rows if r["empresa_id"] == i and str(r["confianza"]) == "baja")
    if nb:
        q(i, "confianza_baja", "media", f"{nb} fila(s) de accionistas con confianza baja (OCR/manuscrito)")
    if not d.get("beneficiarios_finales"):
        q(i, "sin_bf", "media", "No hay constancia/listado de beneficiarios finales en la documentación")
    if not d.get("autoridades"):
        q(i, "sin_autoridades", "media", "No se identifican autoridades")
    sin_doc = sum(1 for r in aut_rows if r["empresa_id"] == i and not r["documento"])
    if sin_doc:
        q(i, "autoridades_sin_ci", "baja", f"{sin_doc} autoridad(es) sin número de documento")
    for o in d.get("observaciones") or []:
        q(i, "observacion_extractor", "info", str(o)[:600])
# conflictos de CI
for p in personas_rows:
    for o in filter(None, p["observaciones_ci_conflictos"].split(" || ")):
        if "unida por nombre" in o:
            tipo, sev = "persona_union_por_nombre", "info"
        elif "corregida" in o:
            tipo, sev = "persona_ci_corregida", "baja"
        else:
            tipo, sev = "persona_ci_conflicto", "media"
        empresas_o = p["empresas"].split("; ")
        for e in empresas_o:
            q(e, tipo, sev, f"{p['nombre_canonico']} ({p['persona_id']}): {o[:300]}")
# BF declarados vs participación integrada calculada (Federico M. Vázquez)
integ_fed = {r["entidad_id"]: r for r in control_rows if r["corte"] == "vigente"}
for r in bf_rows:
    if r.get("persona_id") == FEDERICO and r["porcentaje"] is not None:
        calc = num(integ_fed[r["empresa_id"]].get("integ_federico"))
        q(r["empresa_id"], "bf_vs_calculo", "info", f"BF declara {r['porcentaje']}% para Federico M. Vázquez V. ({r['fecha_dato']}); participación integrada calculada vía GV con la foto vigente: {fmt_pct(calc)}%")
# contradicción U Paraguay
q("u_paraguay", "contradiccion_documental", "alta", "Actas N° 5 y 6 (21/07/2025) atribuyen a Grupo Vázquez 70,36% de los votos y a U Holdings 29,63%, mientras los registros de acciones muestran a U Holdings con ≈99,99% desde 2023.")
write_csv("calidad_datos.csv", cal, ["empresa_id", "empresa", "tipo", "severidad", "detalle"])

# ---------------------------------------------------------------------------
# 8. Empresas
# ---------------------------------------------------------------------------
def presidente_actual(i):
    cand = [r for r in aut_rows if r["empresa_id"] == i and re.search(r"presidente|representante legal|gerente|administrador", str(r["cargo"]), re.I)
            and not re.search(r"vice|suplente", str(r["cargo"]), re.I)]
    cand.sort(key=lambda r: (r["vigente"] is True, re.search(r"presidente", str(r["cargo"]), re.I) is not None, r["fecha_dato"] or r["fecha_asuncion"] or ""), reverse=True)
    return f"{cand[0]['nombre']} ({cand[0]['cargo']})" if cand else ""

for i in IDS:
    d, b = FICHAS[i], BASE_BY_ID[i]
    doms = sorted(d.get("domicilio") or [], key=lambda x: str(g(x, "fecha_dato", default="") or ""), reverse=True)
    caps = sorted(d.get("capital") or [], key=lambda x: (str(g(x, "fecha_dato", default="") or ""), {"integrado": 3, "suscripto": 2, "social": 1}.get(g(x, "tipo", default=""), 0)), reverse=True)
    cap = caps[0] if caps else None
    const = d.get("constitucion") or {}
    c = CTRL_V.get(i)
    cr = next(r for r in control_rows if r["corte"] == "vigente" and r["entidad_id"] == i)
    empresas_rows.append({
        "id": i, "razon_social": d.get("razon_social") or b["razon_social"], "razon_social_base": b["razon_social"], "ruc": d.get("ruc") or b["ruc"],
        "tipo": d.get("tipo"), "actividad": d.get("actividad_principal"), "objeto_social": (d.get("objeto_social") or "")[:300],
        "fecha_constitucion": fecha_ok(g(const, "fecha")), "domicilio_actual": g(doms[0], "direccion") if doms else "",
        "capital": f"{cap.get('tipo')}: {cap.get('moneda') or ''} {cap.get('monto') if cap.get('monto') is not None else 's/d'} ({cap.get('fecha_dato')})" if cap else "",
        "denominaciones_anteriores": "; ".join(f"{g(x, 'nombre')} (hasta {g(x, 'hasta')})" for x in d.get("denominaciones_anteriores") or []),
        "presidente_actual": presidente_actual(i), "tiene_BF": int(bool(d.get("beneficiarios_finales"))),
        "n_documentos": len(d.get("documentos") or []), "segmento": SEG[i], "justificacion_segmento": SEG_JUST[i],
        "controlante_directo": cr["controlante_directo"], "controlante_ultimo": cr["controlante_ultimo"],
        "pct_integrado_grupo": cr["integ_grupo_total"],
        "observaciones": " | ".join(str(o) for o in d.get("observaciones") or [])[:2000]})

write_csv("empresas.csv", empresas_rows, ["id", "razon_social", "razon_social_base", "ruc", "tipo", "actividad", "objeto_social", "fecha_constitucion",
          "domicilio_actual", "capital", "denominaciones_anteriores", "presidente_actual", "tiene_BF", "n_documentos", "segmento",
          "justificacion_segmento", "controlante_directo", "controlante_ultimo", "pct_integrado_grupo", "observaciones"])
write_csv("participaciones.csv", part_rows, ["empresa_id", "empresa", "accionista", "tipo_persona", "documento", "persona_id", "id_entidad_accionista",
          "acciones", "clase_acciones", "porcentaje", "porcentaje_calculado", "votos", "fecha_dato", "vigente", "fuente_archivo", "fuente_pagina", "confianza", "notas"])
write_csv("autoridades.csv", aut_rows, ["empresa_id", "empresa", "nombre", "documento", "persona_id", "cargo", "fecha_asuncion", "vigencia", "fecha_dato", "vigente",
          "fuente_archivo", "fuente_pagina", "confianza", "notas"])
write_csv("beneficiarios_finales.csv", bf_rows, ["empresa_id", "empresa", "nombre", "tipo_persona", "persona_id", "id_entidad", "documento", "nacionalidad",
          "porcentaje", "tipo_control", "cadena_control", "fecha_dato", "fuente_archivo", "fuente_pagina", "confianza", "notas"])
hist_rows.sort(key=lambda h: (h["fecha"] or "9999", h["empresa_id"]))
write_csv("historial.csv", hist_rows, ["fecha", "empresa_id", "empresa", "evento", "detalle", "fuente_archivo", "fuente_pagina"])
write_csv("declarantes_contactos.csv", decl_rows, ["empresa_id", "empresa", "tipo", "nombre", "documento", "persona_id", "correo", "dominio", "telefono",
          "domicilio", "fecha", "fuente_archivo", "fuente_pagina", "notas"])
write_csv("personas.csv", personas_rows, ["persona_id", "nombre_canonico", "ci", "n_empresas", "empresas", "n_menciones", "roles", "cargos", "es_accionista",
          "es_bf", "es_autoridad", "es_declarante", "metodo_union", "formas_unidas", "variantes_texto", "observaciones_ci_conflictos"])
write_csv("personas_roles.csv", roles_rows, ["persona_id", "nombre_canonico", "empresa_id", "empresa", "rol", "cargo", "fecha", "vigente", "pct",
          "nombre_en_fuente", "documento_en_fuente", "fuente", "confianza"])
write_csv("control_indirecto.csv", control_rows, ["corte", "entidad_id", "razon_social", "controlante_directo", "controlante_directo_id",
          "pct_votos_controlante_directo", "tipo_control", "controlante_ultimo", "controlante_ultimo_id", "cadena_control",
          "integ_ueno_holdings_sarl", "integ_grupo_vazquez", "integ_federico", "integ_itti", "integ_u_paraguay", "integ_ueno_bank",
          "integ_grupo_total", "en_grupo_por_control", "n_titulares_dato", "fechas_dato", "notas"])
# participaciones agregadas usadas en el cálculo (trazabilidad)
agg_rows = []
for corte, red in REDES.items():
    for y, vals in red.items():
        for a in vals:
            agg_rows.append({"corte": corte, "empresa_id": y, "titular_id": a["titular"], "titular": etiqueta(a["titular"]), "tipo": a["tipo"],
                             "pct_capital": fmt_pct(a.get("cap"), 4), "pct_votos": fmt_pct(a.get("vot"), 4), "origen_votos": a.get("vot_origen"),
                             "fechas": "; ".join(sorted(f for f in a["fechas"] if f)), "fuentes": "; ".join(sorted(a["fuentes"]))[:600]})
write_csv("participaciones_agregadas.csv", agg_rows, ["corte", "empresa_id", "titular_id", "titular", "tipo", "pct_capital", "pct_votos", "origen_votos", "fechas", "fuentes"])

# ---------------------------------------------------------------------------
# 9. Grafo (GraphML) y métricas
# ---------------------------------------------------------------------------
def xml(s):
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")
nodos = {}
for i in IDS:
    nodos[i] = {"label": nombre_corto(i), "tipo": "entidad_listado", "segmento": SEG[i]}
aristas = []
for v in vinc:
    for k in (v["origen"], v["destino"]):
        if k not in nodos:
            nodos[k] = {"label": etiqueta(k), "tipo": "persona" if k in PID else "entidad_externa", "segmento": ""}
    aristas.append((v["origen"], v["destino"], v["tipo"], v["peso"], v["detalle"][:200]))
for p in personas:
    if p["n_empresas"] >= 2:
        nodos[p["persona_id"]] = {"label": p["nombre_canonico"], "tipo": "persona", "segmento": ""}
for r in roles_rows:
    if r["persona_id"] in nodos:
        aristas.append((r["persona_id"], r["empresa_id"], "persona_" + r["rol"], r["pct"] or "", (r["cargo"] or "")[:100]))
with open(DIR_OUT / "grafo.graphml", "w", encoding="utf-8") as fh:
    fh.write('<?xml version="1.0" encoding="UTF-8"?>\n<graphml xmlns="http://graphml.graphdrawing.org/xmlns">\n')
    for k, n in (("label", "node"), ("tipo", "node"), ("segmento", "node"), ("tipo", "edge"), ("peso", "edge"), ("detalle", "edge")):
        fh.write(f'<key id="{n[0]}_{k}" for="{n}" attr.name="{k}" attr.type="string"/>\n')
    fh.write('<graph id="red_societaria" edgedefault="directed">\n')
    for k, n in nodos.items():
        fh.write(f'<node id="{xml(k)}"><data key="n_label">{xml(n["label"])}</data><data key="n_tipo">{n["tipo"]}</data><data key="n_segmento">{n["segmento"]}</data></node>\n')
    for e, (a, b, t, w, det) in enumerate(aristas):
        fh.write(f'<edge id="e{e}" source="{xml(a)}" target="{xml(b)}"><data key="e_tipo">{xml(t)}</data><data key="e_peso">{xml(w)}</data><data key="e_detalle">{xml(det)}</data></edge>\n')
    fh.write("</graph>\n</graphml>\n")

# guardar estructuras auxiliares para los generadores de informes
aux = {"segmento": SEG, "justificacion": SEG_JUST, "federico": FEDERICO,
       "control": {corte: {k: [v[0], v[1], v[2]] for k, v in CTRLS[corte][0].items()} for corte in CTRLS}}
(DIR_OUT / "_aux.json").write_text(json.dumps(aux, ensure_ascii=False, indent=1), encoding="utf-8")

print(f"empresas={len(empresas_rows)} participaciones={len(part_rows)} autoridades={len(aut_rows)} bf={len(bf_rows)} historial={len(hist_rows)} "
      f"contactos={len(decl_rows)} personas={len(personas_rows)} roles={len(roles_rows)} vinculos={len(vinc)} calidad={len(cal)} "
      f"control={len(control_rows)} salidas={len(salidas)}")
