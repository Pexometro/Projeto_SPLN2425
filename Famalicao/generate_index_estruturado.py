import os
import xml.etree.ElementTree as ET
from pathlib import Path
from collections import defaultdict

INPUT_DIR = Path("registosFamalicao_xml")
HTML_DIR = "htmlFamalicao"
OUTPUT_FILE = "index_estruturado.html"

NS = {'ns': 'urn:isbn:1-931666-22-9'}

registos = {}
filhos = defaultdict(list)

# 1. Ler todos os registos
for file in INPUT_DIR.glob("*.xml"):
    try:
        tree = ET.parse(file)
        root = tree.getroot()
        archdesc = root.find(".//ns:archdesc", NS)
        did = archdesc.find("ns:did", NS) if archdesc is not None else None

        unitid_elem = did.find("ns:unitid", NS) if did is not None else None
        identifier = unitid_elem.attrib.get("identifier") if unitid_elem is not None else None
        unitid = unitid_elem.text.strip() if unitid_elem is not None else "SEM_UNITID"
        title = did.findtext("ns:unittitle", default="(sem título)", namespaces=NS).strip() if did is not None else ""
        level = archdesc.attrib.get("otherlevel", archdesc.attrib.get("level", "N/D")) if archdesc is not None else "N/D"
        parent_elem = archdesc.find(".//ns:relatedmaterial/ns:ref", NS)
        parent = parent_elem.text.strip() if parent_elem is not None else None

        if identifier:
            registos[identifier] = {
                "id": identifier,
                "unitid": unitid,
                "titulo": title,
                "nivel": level,
                "parent": parent,
                "ficheiro_html": f"{file.stem}.html"
            }

            if parent:
                filhos[parent].append(identifier)

    except Exception as e:
        print(f"⚠️ Erro ao processar {file.name}: {e}")

# 2. Construir HTML recursivamente
def construir_html(no_id):
    if no_id not in registos:
        return ""
    
    dados = registos[no_id]
    tipo = "📁" if dados["nivel"] in ["F", "SC", "SSC", "SR"] else "📄"
    link = f"{HTML_DIR}/{dados['ficheiro_html']}"
    linha = f"<li>{tipo} <a href='{link}'>{dados['titulo']} [{dados['nivel']}]</a>"

    subitens = "".join([construir_html(filho) for filho in sorted(filhos.get(no_id, []))])
    if subitens:
        linha += f"<ul>{subitens}</ul>"

    linha += "</li>"
    return linha

# 3. Encontrar raízes
raizes = [r["id"] for r in registos.values() if r["parent"] is None]

# 4. Gerar o ficheiro HTML final
html_total = "".join([construir_html(r) for r in raizes])

html_out = f"""
<html>
<head>
    <meta charset="utf-8">
    <title>Árvore Estruturada de Famalicão</title>
</head>
<body>
    <h1>Árvore Arquivística - Estrutura Hierárquica</h1>
    <ul>{html_total}</ul>
</body>
</html>
"""

Path(OUTPUT_FILE).write_text(html_out, encoding="utf-8")
print(f"✅ index_estruturado.html gerado com sucesso!")
