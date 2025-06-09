import requests
import time

base_url = "https://repositorium.sdum.uminho.pt/oai/oai"
col = "col_1822_21316"

xml_full = ""
offset = 0

while True:
    resumption_token = f"dim///{col}/{offset}"
    params = {
        "verb": "ListRecords",
        "resumptionToken": resumption_token
    }
    r = requests.get(base_url, params=params)
    if "<error code=\"noRecordsMatch\"" in r.text or "<ListRecords/>" in r.text:
        break
    xml_full += r.text
    offset += 100
    time.sleep(1)

with open("OAI.xml", "w", encoding="utf-8") as f:
    f.write(xml_full)

print("XML extraído para OAI.xml")