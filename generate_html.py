import os
import xml.etree.ElementTree as ET
from pathlib import Path

INPUT_DIR = "registos_xml"
OUTPUT_DIR = "output_html"
os.makedirs(OUTPUT_DIR, exist_ok=True)

def extract_text(elem):
    return (elem.text or '').strip() if elem is not None else ''

def generate_html_page(record_id, root):
    html = f"""
    <html>
    <head><meta charset='UTF-8'><title>{record_id}</title></head>
    <body>
        <h1>{record_id}</h1>
        <ul>
    """
    
    for elem in root.iter():
        tag = elem.tag.split('}')[-1]  # remove namespace
        text = extract_text(elem)
        if text:
            html += f"<li><strong>{tag}</strong>: {text}</li>\n"

    html += """
        </ul>
        <a href='index.html'>Voltar ao índice</a>
    </body></html>
    """
    return html

def main():
    index_entries = []

    for xml_file in sorted(Path(INPUT_DIR).glob("*.xml")):
        record_id = xml_file.stem
        tree = ET.parse(xml_file)
        root = tree.getroot()

        html_content = generate_html_page(record_id, root)
        html_path = Path(OUTPUT_DIR) / f"{record_id}.html"
        with open(html_path, "w", encoding="utf-8") as f:
            f.write(html_content)

        index_entries.append(f"<li><a href='{record_id}.html'>{record_id}</a></li>")

    # Criar index.html
    index_html = """
    <html><head><meta charset='UTF-8'><title>Índice de Registos</title></head><body>
    <h1>Registos OAI-PMH</h1>
    <ul>
    """ + "\n".join(index_entries) + """
    </ul></body></html>
    """

    with open(Path(OUTPUT_DIR) / "index.html", "w", encoding="utf-8") as f:
        f.write(index_html)

if __name__ == "__main__":
    main()