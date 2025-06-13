#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
import json

from sentence_transformers import SentenceTransformer, util

def load_docs(path):
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)

def main():
    parser = argparse.ArgumentParser(description="Inferência com modelo SentenceTransformer")
    parser.add_argument('--model', type=str, default='my_sentence_model',
                        help='Pasta do modelo treinado')
    parser.add_argument('--docs', type=str, default='ColDoc.json',
                        help='Ficheiro JSON com documentos (título + abstract)')
    parser.add_argument('--query', type=str, required=True,
                        help='String de consulta')
    parser.add_argument('--top_k', type=int, default=5,
                        help='Número de resultados a devolver')
    args = parser.parse_args()

    # Carrega modelo e documentos
    model = SentenceTransformer(args.model)
    docs = load_docs(args.docs)
    abstracts = [d.get("abstract", "") for d in docs]
    titles    = [d.get("title", "") for d in docs]

    # Embaralha/encode
    corpus_embeddings = model.encode(abstracts, convert_to_tensor=True)
    q_emb = model.encode(args.query, convert_to_tensor=True)

    # Busca top_k
    hits = util.semantic_search(q_emb, corpus_embeddings, top_k=args.top_k)[0]
    hits = sorted(hits, key=lambda x: x['score'], reverse=True)

    print(f"\nTop {args.top_k} resultados para: “{args.query}”\n")
    for rank, hit in enumerate(hits, start=1):
        idx = hit['corpus_id']
        print(f"{rank:02d}. [{hit['score']:.4f}] {titles[idx]}")

if __name__ == '__main__':
    main()
