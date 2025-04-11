import pandas as pd
from collections import defaultdict
from pathlib import Path

# Caminhos
csv_path = "Famalicao/entidades_Famalicao.csv"
output_path = Path("indice_entidades.html")

# Ler CSV
df = pd.read_csv(csv_path)

# Agrupar por tipo e valor (entidade)
entidades_agrupadas = defaultdict(lambda: defaultdict(list))

for _, row in df.iterrows():
    tipo = row["tipo"].strip()
    valor = row["valor"].strip().split("\r\n")[0]  # Nome da pessoa ou lugar
    documento = row["documento"].strip()
    unitid = row["id"].strip()

    # Gerar nome do ficheiro HTML a partir do ID (último bloco numérico)
    id_final = unitid.split("/")[-1]
    html_filename = f"record_Famalicao{id_final}.html"
    html_path = f"Famalicao/htmlFamalicao/{html_filename}"

    entidades_agrupadas[tipo][valor].append((documento, html_path))

# Criar diretório se necessário
output_path.parent.mkdir(parents=True, exist_ok=True)

# Escrever HTML
with open(output_path, "w", encoding="utf-8") as f:
    f.write("""<!DOCTYPE html>
<html lang="pt">
<head>
    <meta charset="UTF-8">
    <title>Índice de Entidades Mencionadas - Famalicão</title>
</head>
<body>
<h1>Índice de Entidades Mencionadas - Famalicão</h1>\n""")

    for tipo in sorted(entidades_agrupadas.keys()):
        f.write(f"<h2>{tipo}s</h2>\n<ul>\n")
        for entidade in sorted(entidades_agrupadas[tipo].keys()):
            f.write(f"<li>{entidade}\n<ul>\n")
            for doc, link in entidades_agrupadas[tipo][entidade]:
                f.write(f"<li><a href='{link}' target='_blank'>{doc}</a></li>\n")
            f.write("</ul>\n</li>\n")
        f.write("</ul>\n")

    f.write("</body>\n</html>")
