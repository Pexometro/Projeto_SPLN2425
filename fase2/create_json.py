import json
from bs4 import BeautifulSoup
import unicodedata
import re

def normalize_keyword(kw):
    kw = kw.lower()
    kw = unicodedata.normalize('NFKD', kw).encode('ASCII', 'ignore').decode('utf-8')
    kw = re.sub(r'[-_]', ' ', kw)
    kw = re.sub(r'[^\w\s]', '', kw)
    kw = re.sub(r'\s+', ' ', kw).strip()
    return kw

with open("OAI.xml", encoding="utf-8") as f:
    xml = f.read()

soup = BeautifulSoup(xml, "xml")
docs = []

for record in soup.find_all("record"):
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
        "keywords": [normalize_keyword(kw) for kw in doc.get("subject", [])]
    })

with open("ColDoc.json", "w", encoding="utf-8") as f:
    json.dump(docs, f, ensure_ascii=False, indent=2)

print(f"Extraídos {len(docs)} documentos para ColDoc.json")