#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
import json
import itertools
import random

from sentence_transformers import SentenceTransformer, InputExample, losses
from torch.utils.data import DataLoader
from sentence_transformers.evaluation import EmbeddingSimilarityEvaluator


def guess_sim(d1, d2):
    """Calcula similaridade Jaccard sobre keywords de dois documentos."""
    k1 = set(d1.get("keywords", []))
    k2 = set(d2.get("keywords", []))
    if not (k1 or k2):
        return 0.0
    return len(k1 & k2) / len(k1 | k2)


def load_docs(path):
    """Carrega documentos do JSON e atribui IDs se não existirem."""
    with open(path, 'r', encoding='utf-8') as f:
        docs = json.load(f)
    # Se faltar campo 'id', adiciona um incremental
    if docs and 'id' not in docs[0]:
        for idx, doc in enumerate(docs):
            doc['id'] = idx
    return docs


def save_pairs(pairs, path):
    """Salva lista de pares (id1, id2, score) em JSON."""
    to_save = [{"id1": a['id'], "id2": b['id'], "score": sim} for a, b, sim in pairs]
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(to_save, f, ensure_ascii=False, indent=2)


def main():
    parser = argparse.ArgumentParser(
        description="Gera ColTrain.json e treina um modelo SentenceTransformer"
    )
    parser.add_argument('--docs', type=str, default='ColDoc.json',
                        help='Ficheiro JSON com documentos')
    parser.add_argument('--threshold', type=float, default=0.0,
                        help='Limiar mínimo de similaridade heurística')
    parser.add_argument('--top_k', type=int, default=5,
                        help='Número de vizinhos positivos garantidos por documento')
    parser.add_argument('--batch_size', type=int, default=16,
                        help='Tamanho do batch para treino')
    parser.add_argument('--epochs', type=int, default=3,
                        help='Número de épocas de treino')
    parser.add_argument('--model_name', type=str,
                        default='paraphrase-multilingual-MiniLM-L12-v2',
                        help='Modelo pré-treinado de base')
    args = parser.parse_args()

    # 1) Carrega documentos
    docs = load_docs(args.docs)

    # 2) Gera pares positivos (top_k por doc) e filtra pelo threshold
    positives = []
    for doc in docs:
        sims = sorted(
            ((other, guess_sim(doc, other)) for other in docs if other['id'] != doc['id']),
            key=lambda x: x[1], reverse=True
        )
        for other, sim in itertools.islice(sims, args.top_k):
            if sim >= args.threshold:
                positives.append((doc, other, sim))
    print(f"Pares positivos gerados: {len(positives)}")

    # 3) Gera pares negativos (fáceis e "hard") na mesma quantidade de positivos
    num_pos = len(positives)
    easy_negs = [(a, b, 0.0)
                 for a, b in itertools.combinations(docs, 2)
                 if guess_sim(a, b) == 0.0]
    hard_negs = []
    for a, b in itertools.combinations(docs, 2):
        sim = guess_sim(a, b)
        if 0.0 < sim < args.threshold:
            hard_negs.append((a, b, sim))
    neg_samples = []
    neg_samples += random.sample(easy_negs, min(len(easy_negs), num_pos))
    neg_samples += random.sample(hard_negs, min(len(hard_negs), num_pos))

    # Junta positivos e negativos, e embaralha
    all_pairs = positives + neg_samples
    random.shuffle(all_pairs)
    print(f"Total de pares (pos + neg): {len(all_pairs)}")

    # 4) Salva ColTrain.json
    save_pairs(all_pairs, 'ColTrain.json')
    print("ColTrain.json gravado com sucesso")

    # 5) Converte para InputExample e faz split treino/validação
    examples = [InputExample(texts=[a['abstract'], b['abstract']], label=float(sim))
                for a, b, sim in all_pairs]
    split_idx = int(0.9 * len(examples))
    train_examples = examples[:split_idx]
    val_examples   = examples[split_idx:]

    train_loader = DataLoader(train_examples, shuffle=True, batch_size=args.batch_size)
    evaluator    = EmbeddingSimilarityEvaluator.from_input_examples(val_examples, name='val-eval')

    # 6) Carrega modelo, define warmup e treina
    model = SentenceTransformer(args.model_name)
    warmup_steps = int(len(train_loader) * args.epochs * 0.1)

    model.fit(
        train_objectives=[(train_loader, losses.CosineSimilarityLoss(model))],
        evaluator=evaluator,
        epochs=args.epochs,
        warmup_steps=warmup_steps,
        output_path='my_sentence_model',
        show_progress_bar=True
    )

    print("Treino concluído e modelo salvo em ./my_sentence_model/")

if __name__ == '__main__':
    main()
