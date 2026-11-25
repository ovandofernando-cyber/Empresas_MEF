"""Convierte los diagramas Mermaid (flowchart simple) de un .md a PNG con Graphviz
y genera una copia del .md con imágenes en lugar de bloques mermaid (para Word).

Uso: python3 scripts/mermaid_a_png.py analisis/red_societaria.md analisis/img salida.md
"""
import os
import re
import subprocess
import sys

src, imgdir, salida = sys.argv[1], sys.argv[2], sys.argv[3]
texto = open(src, encoding="utf-8").read()
bloques = re.findall(r"```mermaid\n(.*?)```", texto, re.S)
os.makedirs(imgdir, exist_ok=True)

NODO = re.compile(r'^\s*(\w+)(\(\[|\[)"(.*?)"(\]\)|\])\s*$')
ARISTA = re.compile(r'^\s*(\w+)\s*(==>|-\.->|-->)\s*(?:\|"(.*?)"\|)?\s*(\w+)\s*$')
SUB = re.compile(r'^\s*subgraph\s+(\w+)\["(.*?)"\]\s*$')
COLORES = {"persona": "#fde68a", "holding_controlante": "#dbeafe", "nucleo_financiero_ueno": "#dcfce7",
           "controlada_itti_gv": "#f3f4f6", "externa": "#fef2f2", "SAL": "#fff7ed", "REO": "#eef2ff"}


def q(s):
    return '"' + s.replace('"', '\\"') + '"'


def envolver(s, n=28):
    pal, lineas, act = s.split(), [], ""
    for p in pal:
        if len(act) + len(p) + 1 > n and act:
            lineas.append(act)
            act = p
        else:
            act = (act + " " + p).strip()
    lineas.append(act)
    return "\\n".join(lineas)


rutas = []
for i, b in enumerate(bloques, 1):
    dot = ['digraph G {', 'rankdir=LR; graph [fontname="DejaVu Sans", fontsize=11, nodesep=0.12, ranksep=0.9, newrank=true];',
           'node [shape=box, style="rounded,filled", fillcolor=white, fontname="DejaVu Sans", fontsize=10];',
           'edge [fontname="DejaVu Sans", fontsize=8, color="#555555"];']
    abierto = None
    for linea in b.splitlines():
        if not linea.strip() or linea.strip().startswith(("flowchart", "graph", "classDef", "class ", "%%", "style ")):
            continue
        m = SUB.match(linea)
        if m:
            abierto = m.group(1)
            dot.append(f'subgraph cluster_{abierto} {{ label={q(m.group(2))}; style="filled,rounded"; '
                       f'fillcolor="{COLORES.get(abierto, "#fafafa")}"; color="#999999";')
            continue
        if linea.strip() == "end":
            if abierto:
                dot.append("}")
                abierto = None
            continue
        m = NODO.match(linea)
        if m:
            forma = "ellipse" if m.group(2) == "([" else "box"
            dot.append(f'{m.group(1)} [label="{envolver(m.group(3))}", shape={forma}];')
            continue
        m = ARISTA.match(linea)
        if m:
            a, tipo, lab, d = m.groups()
            est = {"==>": 'penwidth=2.2, color="#1f4e78"', "-->": "", "-.->": 'style=dashed'}[tipo]
            etq = f'label="{envolver(lab, 22)}", ' if lab else ""
            dot.append(f"{a} -> {d} [{etq}{est}];")
            continue
        print("línea no reconocida:", linea, file=sys.stderr)
    dot.append("}")
    base = os.path.join(imgdir, f"{os.path.splitext(os.path.basename(src))[0]}_diagrama{i}")
    open(base + ".dot", "w", encoding="utf-8").write("\n".join(dot))
    subprocess.run(["dot", "-Tpng", "-Gdpi=170", base + ".dot", "-o", base + ".png"], check=True)
    rutas.append(base + ".png")

it = iter(rutas)
nuevo = re.sub(r"```mermaid\n.*?```", lambda m: f"![]({os.path.abspath(next(it))})", texto, flags=re.S)
open(salida, "w", encoding="utf-8").write(nuevo)
print("\n".join(rutas))
