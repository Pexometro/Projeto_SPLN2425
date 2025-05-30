# 01_extrair_repositorium.py

import requests
from bs4 import BeautifulSoup
import json
import time

base_url = "https://repositorium.sdum.uminho.pt/oai/oai"
col = "col_1822_21316"
xml_full = ""

# Extrair XML por chunks (100 docs por vez)
for offset in range(0, 1000, 100):
    params = {
        "verb": "ListRecords",
        "resumptionToken": f"dim///{col}/{offset}"
    }
    r = requests.get(base_url, params=params)
    if "noRecordsMatch" in r.text:
        break
    xml_full += r.text
    time.sleep(1)  # respeitar o servidor

# Parsear XML e extrair campos
soup = BeautifulSoup(xml_full, "xml")
records = soup.find_all("record")
docs = []

for record in records:
    doc = {}
    fields = record.find_all("field")
    for f in fields:
        element = f.get("element")
        qualifier = f.get("qualifier")
        key = f"{element}.{qualifier}" if qualifier else element
        if key not in doc:
            doc[key] = []
        doc[key].append(f.text)

    docs.append({
        "title": doc.get("title", [""])[0],
        "abstract": doc.get("description", [""])[0],
        "keywords": doc.get("subject", [])
    })

# Guardar em JSON
with open("ColDoc.json", "w", encoding="utf-8") as f:
    json.dump(docs, f, ensure_ascii=False, indent=2)

print(f"Extraídos {len(docs)} documentos.")
