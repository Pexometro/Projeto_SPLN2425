import xml.etree.ElementTree as ET
from pathlib import Path
import csv
import re
import sys

if sys.argv[1] == "Famalicao":
    cidade = "Famalicao"
elif sys.argv[1] == "VilaReal":
    cidade = "VilaReal"
else:
    print("❌ Cidade não reconhecida.")
    sys.exit(1)

INPUT_DIR = Path(f"{cidade}/registos{cidade}_xml")
OUTPUT_FILE = Path(f"{cidade}/entidades_{cidade}.csv")

NS = {'ns': 'urn:isbn:1-931666-22-9'}

def extrair_texto(archdesc, tag):
    elem = archdesc.find(f"ns:{tag}/ns:p", NS)
    return (elem.text or "").strip() if elem is not None else ""

# Regex para nomes próprios (padrão simples)
re_nome = re.compile(r"\b[A-ZÁÉÍÓÚÂÊÔÃÕÇ][a-záéíóúâêôãõç]+(?:\s+[A-ZÁÉÍÓÚÂÊÔÃÕÇ][a-záéíóúâêôãõç]+)+\b")
# (Opcional) lugares conhecidos (exemplo simples)
lugares_conhecidos = ["Vila Real", "Braga", "Porto", "Lisboa"]

entidades = []

for file in INPUT_DIR.glob("*.xml"):
    try:
        tree = ET.parse(file)
        root = tree.getroot()
        archdesc = root.find(".//ns:archdesc", NS)
        did = archdesc.find("ns:did", NS)
        unitid = did.findtext("ns:unitid", default="SEM_ID", namespaces=NS).strip()
        titulo = did.findtext("ns:unittitle", default="(sem título)", namespaces=NS).strip()

        scope = extrair_texto(archdesc, "scopecontent")
        biog = extrair_texto(archdesc, "bioghist")
        texto = f"{scope} {biog}"

        # Pessoas
        for nome in re_nome.findall(texto):
            entidades.append({"tipo": "Pessoa", "valor": nome, "documento": titulo, "id": unitid})

        # Lugares
        for lugar in lugares_conhecidos:
            if lugar in texto:
                entidades.append({"tipo": "Lugar", "valor": lugar, "documento": titulo, "id": unitid})

    except Exception as e:
        print(f"⚠️ Erro ao processar {file.name}: {e}")

# Guardar CSV
with open(OUTPUT_FILE, "w", newline="", encoding="utf-8") as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=["tipo", "valor", "documento", "id"])
    writer.writeheader()
    writer.writerows(entidades)

print(f"✅ Entidades extraídas e guardadas em: {OUTPUT_FILE}")
