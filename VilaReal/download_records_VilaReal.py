from sickle import Sickle
import os
import xml.etree.ElementTree as ET

# Configuração inicial
OAI_URL = "https://digitarq.advrl.arquivos.pt/OAI-PMH/"

METADATA_PREFIX = "ead"
OUTPUT_DIR = "registosVilaReal_xml"
NUM_RECORDS = 500

def download_records():
    sickle = Sickle(OAI_URL)
    records = sickle.ListRecords(metadataPrefix=METADATA_PREFIX)

    os.makedirs(OUTPUT_DIR, exist_ok=True)

    for i, record in enumerate(records):
        xml_data = record.raw
        with open(os.path.join(OUTPUT_DIR, f"record_VilaReal{i+1:04d}.xml"), "w", encoding="utf-8") as f:
            f.write(xml_data)
        print(f"Guardado record_Famalicao{i+1:04d}.xml")

if __name__ == "__main__":
    download_records()
