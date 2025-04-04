import os
import xml.etree.ElementTree as ET
from pathlib import Path

# Diretórios
INPUT_DIR = Path("registosFamalicao_xml")
OUTPUT_DIR = Path("htmlFamalicao")
OUTPUT_DIR.mkdir(exist_ok=True)

NS = {'ns': 'urn:isbn:1-931666-22-9'}

def extract_text(elem):
    return (elem.text or '').strip() if elem is not None else ""

# Lista de páginas para o índice
html_index = []

for xml_file in sorted(INPUT_DIR.glob("*.xml")):
    try:
        tree = ET.parse(xml_file)
        root = tree.getroot()
        
        archdesc = root.find(".//ns:archdesc", NS)
        did = archdesc.find("ns:did", NS) if archdesc is not None else None
        
        unitid = extract_text(did.find("ns:unitid", NS)) if did is not None else "Sem ID"
        unittitle = extract_text(did.find("ns:unittitle", NS)) if did is not None else "Sem título"
        unitdate = extract_text(did.find("ns:unitdate", NS)) if did is not None else ""
        level = archdesc.attrib.get("otherlevel", archdesc.attrib.get("level", "N/D")) if archdesc is not None else "N/D"
        scope = extract_text(archdesc.find("ns:scopecontent/ns:p", NS)) if archdesc is not None else ""
        biog = extract_text(archdesc.find("ns:bioghist/ns:p", NS)) if archdesc is not None else ""

        html_content = f"""
        <html><head><meta charset='utf-8'><title>{unitid}</title></head><body>
        <h1>{unittitle}</h1>
        <p><strong>Identificador:</strong> {unitid}</p>
        <p><strong>Data:</strong> {unitdate}</p>
        <p><strong>Nível:</strong> {level}</p>
        <p><strong>Descrição:</strong> {scope}</p>
        <p><strong>Biografia/Histórico:</strong> {biog}</p>
        <a href='index.html'>⬅ Voltar ao índice</a>
        </body></html>
        """

        html_filename = xml_file.stem + ".html"
        with open(OUTPUT_DIR / html_filename, "w", encoding="utf-8") as out:
            out.write(html_content)

        html_index.append(f"<li><a href='{html_filename}'>{unittitle or unitid}</a></li>")

    except Exception as e:
        print(f"Erro no ficheiro {xml_file.name}: {e}")

# Gerar índice
index_html = "<html><head><meta charset='utf-8'><title>Índice Famalicão</title></head><body><h1>Registos de Famalicão</h1><ul>"
index_html += "\n".join(html_index)
index_html += "</ul></body></html>"

with open(OUTPUT_DIR / "index.html", "w", encoding="utf-8") as f:
    f.write(index_html)

print("✅ HTML gerado com sucesso em: htmlFamalicao/")
