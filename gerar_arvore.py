import os
import xml.etree.ElementTree as ET
from pathlib import Path
from collections import defaultdict
import sys


if sys.argv[1] == "Famalicao":
        cidade = "Famalicao"
        print("Famalicao")
elif sys.argv[1] == "VilaReal":
        cidade = "VilaReal"    
        print("VilaReal")
else:
        print("Cidade não reconhecida. A execução do script será encerrada.")
        sys.exit(1) 

INPUT_DIR = f"{cidade}/registos{cidade}_xml"
TXT_OUT = f"{cidade}/arvore_{cidade}.txt"
HTML_OUT = f"{cidade}/arvore_{cidade}.html"

NS = {'ns': 'urn:isbn:1-931666-22-9'}

# Estruturas auxiliares
registos = {}
filhos = defaultdict(list)

for file in Path(INPUT_DIR).glob("*.xml"):
    tree = ET.parse(file)
    root = tree.getroot()
    
    archdesc = root.find(".//ns:archdesc", NS)
    did = archdesc.find("ns:did", NS)

    unitid = did.findtext("ns:unitid", default="SEM_ID", namespaces=NS).strip()
    title = did.findtext("ns:unittitle", default="(sem título)", namespaces=NS).strip()
    level = archdesc.attrib.get("otherlevel", archdesc.attrib.get("level", "N/D")).strip()

    # Procurar parent
    parent_elem = archdesc.find(".//ns:relatedmaterial/ns:ref", NS)
    parent = parent_elem.text.strip() if parent_elem is not None else None

    registos[unitid] = {
        "id": unitid,
        "titulo": title,
        "nivel": level,
        "parent": parent,
        "ficheiro": file.name
    }

    if parent:
        filhos[parent].append(unitid)

# Construção da árvore (recursiva)
def construir_arvore(no_id, nivel=0):
    linha = "  " * nivel + f"- [{no_id}] {registos[no_id]['titulo']} ({registos[no_id]['nivel']})\n"
    for filho in filhos.get(no_id, []):
        linha += construir_arvore(filho, nivel + 1)
    return linha

# Encontrar raízes (sem parent)
raizes = [r["id"] for r in registos.values() if r["parent"] is None]

# Gerar TXT
with open(TXT_OUT, "w", encoding="utf-8") as f:
    for raiz in raizes:
        f.write(construir_arvore(raiz))

# Gerar HTML
def construir_html(no_id):
    linha = f"<li><strong>{registos[no_id]['titulo']}</strong> [{registos[no_id]['nivel']}] - {registos[no_id]['id']}<br><em>{registos[no_id]['ficheiro']}</em>"
    filhos_html = "".join([construir_html(filho) for filho in filhos.get(no_id, [])])
    if filhos_html:
        linha += f"<ul>{filhos_html}</ul>"
    linha += "</li>"
    return linha

html_conteudo = "".join([construir_html(r) for r in raizes])

with open(HTML_OUT, "w", encoding="utf-8") as f:
    f.write(f"""
    <html><head><meta charset='utf-8'><title>Árvore Arquivística - {cidade}</title></head>
    <body><h1>Árvore Arquivística</h1>
    <ul>{html_conteudo}</ul>
    </body></html>
    """)

print(f"✅ Gerado:\n- {TXT_OUT}\n- {HTML_OUT}")
