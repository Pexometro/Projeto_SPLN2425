import os
import sys

if sys.argv[1] == "Famalicao":
        cidade = "Famalicao"
        print("Famalicao")
elif sys.argv[1] == "VilaReal":
        cidade = "VilaReal"    
        print("VilaReal")
else:
        print("Cidade não reconhecida. A execução do script será encerrada.")
        sys.exit(1) 

INPUT_DIR = f"{cidade}/registos{cidade}_xml"

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
