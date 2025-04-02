import os
import re
import csv
from pathlib import Path
import xml.etree.ElementTree as ET

INPUT_DIR = "registosPontedeLima_xml"
OUTPUT_FILE = "entidades_pontedelima.csv"

# Expressões regulares para entidades
regex_pessoas = re.compile(r"(?:[A-ZÀ-\u0178][a-zà-\u017f]+\s){1,4}[A-ZÀ-\u0178][a-zà-\u017f]+")
regex_datas = re.compile(r"\b(\d{4}|s[ée]culo\s+[XVI]+|anos\s+\d{3,4})\b", re.IGNORECASE)
regex_lugares = re.compile(r"(?:em|na|no|nas|nos)\s+[A-ZÀ-\u0178][a-zà-\u017f]+(?:\s+[A-ZÀ-\u0178][a-zà-\u017f]+)?")

def extract_entities_from_text(text):
    pessoas = regex_pessoas.findall(text)
    datas = regex_datas.findall(text)
    lugares = regex_lugares.findall(text)
    return set(pessoas), set(datas), set(lugares)

def main():
    entidades = []

    for file in Path(INPUT_DIR).glob("*.xml"):
        with open(file, encoding="utf-8") as f:
            content = f.read()
            pessoas, datas, lugares = extract_entities_from_text(content)
            for p in pessoas:
                entidades.append((file.name, "Pessoa", p))
            for d in datas:
                entidades.append((file.name, "Data", d))
            for l in lugares:
                entidades.append((file.name, "Lugar", l))

    # Guardar CSV
    with open(OUTPUT_FILE, "w", newline="", encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["Ficheiro", "Tipo", "Entidade"])
        writer.writerows(entidades)

    print(f"\n✅ Extração concluída. Guardado em '{OUTPUT_FILE}' com {len(entidades)} entidades.")

if __name__ == "__main__":
    main()
