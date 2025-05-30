# Trabalho Prático 2 - Sistemas de Recuperação de Informação (SPLN)
## Objetivo Geral
Desenvolver um sistema de recuperação de informação baseado em similaridade semântica entre textos, utilizando dissertações académicas retiradas do RepositóriUM. O projeto passa por construir uma coleção de documentos, gerar dados de treino com base em similaridades heurísticas, treinar um modelo do tipo BERT/sentence-transformer e aplicar o modelo para encontrar os documentos mais relevantes para uma dada consulta.

## Etapas do Projeto
### 1. Extração de dados do RepositóriUM
**Objetivo:** Obter metadados de dissertações académicas da UMinho através do protocolo OAI-PMH.

O que fazer:

- Usar a URL base do repositório:
https://repositorium.sdum.uminho.pt/oai/oai

- Utilizar a coleção col_1822_21316 (ex. teses de mestrado do DI).

- Fazer pedidos com requests.get(...) utilizando o parâmetro resumptionToken com valores como dim///col_1822_21316/0, .../100, .../200, etc.

- Concatenar os resultados XML até não haver mais documentos.

- Guardar todos os metadados num ficheiro OAI.xml.

### 2. Conversão de XML para JSON estruturado
**Objetivo:** Transformar os dados XML brutos em documentos estruturados em JSON com os campos:

1. title

2. abstract (descrição)

3. keywords (assuntos)

O que fazer:

- Usar BeautifulSoup ou xml.etree.ElementTree para parsear o XML.

- Para cada record, extrair os campos mencionados.

- Guardar a coleção como ColDoc.json, uma lista de dicionários.

### 3. Geração da coleção de treino (ColTrain)

**Objetivo:** Criar uma coleção de pares de documentos com uma estimativa de similaridade.

O que fazer:

- Para todos os pares de documentos de ColDoc.json, aplicar uma função guess_sim(doc1, doc2) baseada em:

- Número de keywords em comum.

- Proporção das keywords comuns relativamente ao total.

- Filtrar os pares com similaridade mínima (ex: sim > 0.3).

- Guardar os pares (texto1, texto2, sim) como lista no ColTrain.json.

### 4. Treino de um modelo sentence-transformer

**Objetivo:** Treinar um modelo para prever a similaridade entre pares de textos com base em ColTrain.json.

O que fazer:

- Usar um modelo pré-treinado como paraphrase-multilingual-MiniLM-L12-v2.

- Criar InputExample(texts=[t1, t2], label=sim) a partir de ColTrain.

- Treinar com CosineSimilarityLoss durante 1–3 épocas.

- Guardar o modelo final em my_sentence_model/.

### 5. Utilização do modelo treinado
**Objetivo:** Criar uma função de recuperação de documentos com base numa pergunta (query) de utilizador.

O que fazer:

- Codificar a query e os resumos da coleção com embeddings.

- Calcular a similaridade (ex: cos_sim) entre a query e todos os documentos.

- Devolver o top-N dos mais relevantes, com título e score.

## ✅ Entrega esperada

Ficheiro .py com scraping e conversão XML → JSON.

Ficheiro .ipynb com treino do modelo e sistema de recuperação.

Ficheiros ColDoc.json, ColTrain.json e pasta my_sentence_model/.

Um README.md com instruções claras sobre:

Como correr cada parte.

Descrição de ficheiros.

Exemplos de uso do sistema de recuperação.