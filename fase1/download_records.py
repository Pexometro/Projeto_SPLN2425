from sickle import Sickle
import os
import xml.etree.ElementTree as ET
import sys

# Configuração inicial

if sys.argv[1] == "Famalicao":
        OAI_URL = "https://www.arquivoalbertosampaio.org/OAI-PMH/"
        cidade = "Famalicao"
        print("Famalicao")
elif sys.argv[1] == "VilaReal":
        OAI_URL = "https://digitarq.advrl.arquivos.pt/OAI-PMH/"
        cidade = "VilaReal"    
        print("VilaReal")
else:
        print("Cidade não reconhecida. A execução do script será encerrada.")
        sys.exit(1) 

METADATA_PREFIX = "ead"
OUTPUT_DIR = f"{cidade}/registos{cidade}_xml"

def download_records():
    sickle = Sickle(OAI_URL)
    records = sickle.ListRecords(metadataPrefix=METADATA_PREFIX)

    os.makedirs(OUTPUT_DIR, exist_ok=True)

    for i, record in enumerate(records):
        xml_data = record.raw
        with open(os.path.join(OUTPUT_DIR, f"record_{cidade}{i+1:04d}.xml"), "w", encoding="utf-8") as f:
            f.write(xml_data)
        print(f"Guardado record_{cidade}{i+1:04d}.xml")

if __name__ == "__main__":
    download_records()
