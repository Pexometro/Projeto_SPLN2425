# 02_treino_modelo_sentence_transformer.ipynb

# !pip install sentence-transformers

from sentence_transformers import SentenceTransformer, InputExample, losses
from torch.utils.data import DataLoader
import json

# Carregar dados de treino
with open("ColDoc.json", encoding="utf-8") as f:
    docs = json.load(f)

# Construir ColTrain com heurística simples
import itertools

def guess_sim(d1, d2):
    k1 = set(d1["keywords"])
    k2 = set(d2["keywords"])
    if not (k1 or k2):
        return 0.0
    return len(k1 & k2) / len(k1 | k2)

col_train = []
for d1, d2 in itertools.combinations(docs, 2):
    sim = guess_sim(d1, d2)
    if sim > 0.3:
        col_train.append((d1["abstract"], d2["abstract"], sim))

print(f"Pares de treino: {len(col_train)}")

# Treinar modelo
train_examples = [InputExample(texts=[t1, t2], label=score) for t1, t2, score in col_train]
train_dataloader = DataLoader(train_examples, shuffle=True, batch_size=16)

model = SentenceTransformer("sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2")
train_loss = losses.CosineSimilarityLoss(model)

model.fit(train_objectives=[(train_dataloader, train_loss)], epochs=1, warmup_steps=100)
model.save("my_sentence_model")
