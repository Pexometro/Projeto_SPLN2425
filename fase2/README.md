# SPLN - Trabalho Prático 2

## 📌 Objetivo
Desenvolver um sistema de recuperação de informação com base em dissertações académicas do RepositóriUM, utilizando embeddings semânticos para medir similaridade entre textos.

---

## 🧱 Estrutura do Projeto

- `01_extrair_repositorium.py`:  
  Extrai os metadados das dissertações via OAI-PMH e guarda-os em `ColDoc.json`.

- `02_treino_modelo_sentence_transformer.ipynb`:  
  Cria pares de documentos com similaridade estimada e treina um modelo `sentence-transformer`.

- `03_inferencia.ipynb`:  
  Permite consultar o modelo treinado. O utilizador insere uma query e recebe os documentos mais relevantes da coleção.

- `ColDoc.json`:  
  Documento com os dados extraídos do RepositóriUM, em formato JSON.

- `my_sentence_model/`:  
  Pasta que contém o modelo treinado.

---

## ▶️ Instruções para correr

1. **Extração dos dados**
   ```bash
   python 01_extrair_repositorium.py
   ```

2. **Treino do modelo**
   - Abrir e correr todas as células do ficheiro `02_treino_modelo_sentence_transformer.ipynb`.

3. **Consulta ao sistema**
   - Abrir o ficheiro `03_inferencia.ipynb`.
   - Executar e inserir queries no final para obter os documentos mais relevantes.

---

## 💡 Exemplo de uso
```
Query: redes neurais em visão computacional

Top 5 documentos mais relevantes:
0.78 - Redes Neuronais Convolucionais em Imagem Médica
...
```

---

## 📚 Tecnologias
- Python
- BeautifulSoup
- SentenceTransformers (BERT)
- Torch