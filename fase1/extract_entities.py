import xml.etree.ElementTree as ET
from pathlib import Path
import csv
import spacy
import sys

# Verifica cidade via argumento
if sys.argv[1] == "Famalicao":
    cidade = "Famalicao"
elif sys.argv[1] == "VilaReal":
    cidade = "VilaReal"
else:
    print("❌ Cidade não reconhecida.")
    sys.exit(1)

INPUT_DIR = Path(f"{cidade}/registos{cidade}_xml")
OUTPUT_CSV = Path(f"{cidade}/entidades_{cidade}.csv")

NS = {'ns': 'urn:isbn:1-931666-22-9'}

# Carregar modelo spaCy
nlp = spacy.load("pt_core_news_lg")

def extrair_texto(archdesc, tag):
    elem = archdesc.find(f"ns:{tag}/ns:p", NS)
    return (elem.text or "").strip() if elem is not None else ""

entidades = []

for file in INPUT_DIR.glob("*.xml"):
    try:
        tree = ET.parse(file)
        root = tree.getroot()
        archdesc = root.find(".//ns:archdesc", NS)
        did = archdesc.find("ns:did", NS)
        unitid = did.findtext("ns:unitid", default="SEM_ID", namespaces=NS).strip()
        titulo = did.findtext("ns:unittitle", default="(sem título)", namespaces=NS).strip()

        texto = extrair_texto(archdesc, "scopecontent") + " " + extrair_texto(archdesc, "bioghist")
        doc = nlp(texto)

        for ent in doc.ents:
            if ent.label_ == "PER":
                entidades.append({"tipo": "Pessoa", "valor": ent.text, "documento": titulo, "id": unitid})
            elif ent.label_ in ("LOC", "GPE"):
                entidades.append({"tipo": "Lugar", "valor": ent.text, "documento": titulo, "id": unitid})

    except Exception as e:
        print(f"⚠️ Erro ao processar {file.name}: {e}")

# Exportar CSV
with open(OUTPUT_CSV, "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=["tipo", "valor", "documento", "id"])
    writer.writeheader()
    writer.writerows(entidades)

print(f"✅ Entidades extraídas com sucesso para: {OUTPUT_CSV}")
