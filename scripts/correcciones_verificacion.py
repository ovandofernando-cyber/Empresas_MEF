"""Correcciones a las fichas JSON derivadas de las verificaciones puntuales (punto 5).
Idempotente: puede ejecutarse varias veces."""
import json, pathlib
BASE = pathlib.Path(__file__).resolve().parent.parent / "datos" / "empresas"
MARCA = "[VERIFICACIÓN 2026-11-24]"

def load(i): return json.loads((BASE / f"{i}.json").read_text(encoding="utf-8"))
def save(i, d): (BASE / f"{i}.json").write_text(json.dumps(d, ensure_ascii=False, indent=1), encoding="utf-8")
def add_obs(d, txt):
    if not any(MARCA in o and txt[:60] in o for o in d["observaciones"]):
        d["observaciones"] = [o for o in d["observaciones"] if not o.startswith(MARCA) or txt[:60] not in o]
        d["observaciones"].append(f"{MARCA} {txt}")

EXPL = ("En las 35 constancias SIARA restantes el campo 'Analista' muestra funcionarios del MEF (≈16 nombres distintos, "
        "ninguno vinculado a las empresas). En las dos constancias de tipo 'REGULARIZACIÓN DE EAS' (HD Invest y La Tropa Fletes), "
        "presentadas y expedidas el mismo día 16/11/2026 en horario nocturno, el campo 'Analista' repite el nombre del representante "
        "legal de la propia EAS. Se interpreta que en ese trámite de autogestión el sistema consigna al usuario que cargó la declaración "
        "(equivalente al 'Responsable de la Solicitud' / declarante de la empresa), NO a un funcionario del MEF. No hay base para afirmar "
        "conflicto de interés ni autoaprobación.")

# (a) HD Invest
d = load("hd_invest")
for v in d["vinculos"]:
    if "Analista" in v["detalle"] or "analista" in v["detalle"]:
        v["tipo"] = "otro"
        v["detalle"] = ("El socio único y representante legal figura en el campo 'Analista' de la Constancia RA N° 35431 (Regularización de EAS, "
                        "16/11/2026 22:27). Verificado: corresponde al usuario declarante de la propia empresa, no a un funcionario del MEF.")
d["observaciones"] = [o for o in d["observaciones"] if not o.startswith("Conflicto de interés: el analista")]
add_obs(d, "Corregida la lectura previa ('analista del MEF = accionista'). " + EXPL)
if not any((x.get("nombre") or "").upper().startswith("KARIM") for x in d["declarantes_siara"]):
    d["declarantes_siara"].append({"nombre": "KARIM HAMZA DAMANI CHAPARRO", "documento": "CI 3.875.748 (manuscrito en proforma)", "correo": "andreabarrua20@gmail.com",
        "telefono": None, "fecha": "2026-11-16", "fuente": {"archivo": "Constancia RA 2026 Siara.pdf", "pagina": 1},
        "notas": "Consignado en el campo 'Analista' de la constancia; interpretado como usuario declarante (ver observaciones)."})
for doc in d["documentos"]:
    if doc["archivo"].startswith("Constancia RA 2026"):
        doc["resumen"] = "Constancia RA N° 35431, tipo Regularización de EAS; campo 'Analista' = Karim Hamza Damani Chaparro (declarante de la propia EAS)."
save("hd_invest", d)

# (a) La Tropa Fletes
d = load("la_tropa_fletes")
for v in d["vinculos"]:
    if "analista" in v["entidad_o_persona"].lower():
        v["entidad_o_persona"] = "CARLOS DAMIAN GAUTO PAREDES (declarante SIARA)"
        v["detalle"] = ("Figura en el campo 'Analista' de la Constancia RA N° 32824 (Regularización de EAS, 16/11/2026 20:41). Verificado: es el "
                        "representante legal y accionista mayoritario actuando como usuario declarante, no un funcionario del MEF.")
d["observaciones"] = [o.replace(", y fue expedida por un analista homónimo del accionista mayoritario", "") for o in d["observaciones"]]
for x in d["declarantes_siara"]:
    if x.get("nombre") is None and "GAUTO" in (x.get("notas") or "").upper():
        x["nombre"] = "CARLOS DAMIAN GAUTO PAREDES"
        x["notas"] = "Constancia RA N° 32824; consignado en el campo 'Analista' (usuario declarante de la EAS, no funcionario MEF)."
add_obs(d, "Corregida la lectura previa ('analista homónimo del accionista'). " + EXPL)
save("la_tropa_fletes", d)

# (b) RADICE S.A. = Terravaz
TXT_B = ("RADICE S.A., fideicomitente desarrollador del Fideicomiso Shopping Costanera (contrato 21/01/2019), es la misma persona jurídica que "
         "TERRAVAZ S.A.E. (ex RADICE S.A.E.C.A., RUC 80104014-0): mismo número base de RUC (el contrato, leído por OCR, trae '80104014-7'; el "
         "dígito verificador correcto de 80104014 es 0), mismos firmantes Horacio José Biga (CI 5.990.871, Presidente) y Carlos Emilio Soler "
         "(CI 5.992.466, Vicepresidente), que son fundadores de RADICE S.A. (Esc. 119 del 28/08/2018), mismo ámbito (Encarnación, Costanera) "
         "y correos @radice.com.py. Desde jun-ago 2025 Grupo Vázquez controla 97,33% de Terravaz, por lo que el fideicomiso queda vinculado "
         "indirectamente al grupo (salvo cesión de la posición de fideicomitente, que no consta en los documentos).")
d = load("fideicomiso_shopping_costanera")
add_obs(d, TXT_B)
if not any("TERRAVAZ" in v["entidad_o_persona"].upper() for v in d["vinculos"]):
    d["vinculos"].append({"entidad_o_persona": "TERRAVAZ S.A.E. (ex RADICE S.A.E.C.A., RUC 80104014-0)", "tipo": "otro",
        "detalle": "Fideicomitente desarrollador y beneficiario (RADICE S.A.) = Terravaz; controlada por Grupo Vázquez desde 2025.",
        "fuente": {"archivo": "contratodefideicomisoshoppingcostanera21012019091525.pdf", "pagina": 1}, "confianza": "alta"})
save("fideicomiso_shopping_costanera", d)
d = load("terravaz")
add_obs(d, TXT_B)
if not any("FIDEICOMISO" in v["entidad_o_persona"].upper() for v in d["vinculos"]):
    d["vinculos"].append({"entidad_o_persona": "FIDEICOMISO SHOPPING COSTANERA (RUC 80105334-0)", "tipo": "otro",
        "detalle": "Como RADICE S.A. es fideicomitente desarrollador y beneficiaria del fideicomiso (contrato 21/01/2019, fiduciario Financiera Finexpar).",
        "fuente": {"archivo": "(carpeta Fideicomiso Shoping Costanera) contratodefideicomisoshoppingcostanera21012019091525.pdf", "pagina": 1}, "confianza": "alta"})
save("terravaz", d)

# (c) CI Federico M. Vázquez Villasanti
TXT_C = ("CI de Federico Miguel Vázquez Villasanti: el correcto es 2.941.546 (14 archivos fuente, incluida la Escritura 131 de Grupo Vázquez y "
         "constancias BF de Red Digital, Redipro, Place Analyzer, Red UTS). La variante 2.491.546 aparece sólo en las constancias BF de Kaitel "
         "y Tiva y es una transposición de dígitos: en ambas va acompañada del DV '-2', que es el dígito verificador de 2941546 (el de 2491546 sería 7).")
for i in ("kaitel", "tiva"):
    d = load(i); add_obs(d, TXT_C); save(i, d)
print("ok")
