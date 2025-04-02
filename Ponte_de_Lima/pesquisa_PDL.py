import os

INPUT_DIR = "registosPonteDeLima_xml"

def procurar_termo(termo):
    resultados = []
    termo = termo.lower()

    for ficheiro in os.listdir(INPUT_DIR):
        if ficheiro.endswith(".xml"):
            caminho = os.path.join(INPUT_DIR, ficheiro)
            with open(caminho, "r", encoding="utf-8") as f:
                conteudo = f.read().lower()
                if termo in conteudo:
                    resultados.append(ficheiro)

    return resultados

if __name__ == "__main__":
    termo = input("🔍 Introduz termo a procurar: ")
    encontrados = procurar_termo(termo)

    if encontrados:
        print(f"\n✅ Encontrado em {len(encontrados)} ficheiros:\n")
        for f in encontrados:
            print(f"  - {f}")
    else:
        print("❌ Nenhum ficheiro contém esse termo.")
