import csv
from collections import defaultdict
from pathlib import Path
import sys

if sys.argv[1] == "Famalicao":
    cidade = "Famalicao"
elif sys.argv[1] == "VilaReal":
    cidade = "VilaReal"
else:
    print("❌ Cidade não reconhecida.")
    sys.exit(1)

CSV_FILE = Path(f"{cidade}/entidades_{cidade}.csv")
HTML_OUT = Path(f"{cidade}/html{cidade}/entidades.html")

# Carregar entidades
entidades = defaultdict(lambda: defaultdict(list))  # tipo -> entidade -> lista de (titulo, id)

with open(CSV_FILE, newline='', encoding="utf-8") as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        tipo = row["tipo"]
        valor = row["valor"]
        doc = row["documento"]
        uid = row["id"]
        entidades[tipo][valor].append((doc, uid))

# Gerar HTML
html = """<html><head><meta charset='utf-8'><title>Entidades Mencionadas</title></head>
<body><h1>Índice de Entidades Mencionadas</h1>
"""

for tipo in sorted(entidades.keys()):
    html += f"<h2>{tipo}s</h2><ul>\n"
    for entidade in sorted(entidades[tipo].keys()):
        html += f"<li><strong>{entidade}</strong><ul>\n"
        for doc, uid in entidades[tipo][entidade]:
            filename = uid.replace("/", "_") + ".html"
            html += f"<li><a href='{filename}'>{doc}</a> ({uid})</li>\n"
        html += "</ul></li>\n"
    html += "</ul>\n"

html += "<a href='index.html'>⬅ Voltar ao índice</a>\n</body></html>"

# Guardar
with open(HTML_OUT, "w", encoding="utf-8") as f:
    f.write(html)

print(f"✅ Índice de entidades gerado em: {HTML_OUT}")
