from sentence_transformers import SentenceTransformer, util
import json
import torch

# Carregar o modelo treinado
model = SentenceTransformer("my_sentence_model")

# Carregar os documentos processados
with open("ColDoc.json", encoding="utf-8") as f:
    docs = json.load(f)

# Separar abstracts e títulos
abstracts = [doc["abstract"] for doc in docs]
titles = [doc["title"] for doc in docs]

# Codificar todos os abstracts com o modelo treinado
abstract_embeddings = model.encode(abstracts, convert_to_tensor=True)

# Função de consulta
def consultar(query, top_k=5):
    query_embedding = model.encode(query, convert_to_tensor=True)
    cos_scores = util.cos_sim(query_embedding, abstract_embeddings)[0]
    top_results = torch.topk(cos_scores, k=top_k)

    print(f"\n🔎 Query: {query}\n")
    print(f"📄 Top {top_k} documentos mais relevantes:\n")
    for score, idx in zip(top_results.values, top_results.indices):
        print(f"{score:.4f} - {titles[idx]}")
        print(f"    ➤ Resumo: {abstracts[idx][:200]}...\n")

# Exemplo de utilização:
consultar("aprendizagem automática em processamento de linguagem natural")
