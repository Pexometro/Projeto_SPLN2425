# Trabalho Prático 1 — SPLN 2024/2025
## Mestrado em Informática — Unidade Curricular de Sistemas de Processamento de Linguagem Natural
Este projeto tem como objetivo a exploração, transformação e apresentação de metadados arquivísticos disponibilizados via protocolo OAI-PMH, com foco na análise textual, organização hierárquica e estruturação semântica dos dados.

## Estrutura do Projeto
### 1-  Download de Registos (OAI-PMH)
**Script:** download_records.py

Permite descarregar os ficheiros XML com metadados arquivísticos das cidades de Famalicão ou Vila Real.
```
python download_records.py Famalicao
```
### 2 - Estudo da Estrutura dos Documentos
Foi analisada a estrutura EAD (Encoded Archival Description), com identificação de:

- Dependências funcionais e campos constantes

- Chaves (ex: unitid, title)


### 3 - Árvore Arquivística
**Script:** generate_index_estruturado.py

Com base nos campos unitid, level, parent, foi construída a árvore arquivística:

Fundo (F), Secção (SC), Subsecção (SSC), Série (SR), Unidade de Instalação (UI), Documento (D/DC)

### 4 - Geração de Estrutura de Diretorias
A estrutura hierárquica dos registos é usada para gerar:

Uma árvore de diretorias lógica

Representação em HTML com links entre documentos

- 4b. Geração de HTML Estático

    **Script:** generate_html.py

Cada registo XML é convertido numa página HTML com:

1. Título

2. Data

3. Nível arquivístico

4. ScopeContent

5. BiogHist

Um índice é gerado automaticamente para navegação.

### 5 - Script de Procura
**Script:** pesquisa.py

Permite procurar por um termo nos registos locais.

```
python pesquisa.py <Cidade>
```

### 6 - Entidades Mencionadas
**Script:** extract_entities.py

Utilizando spacy (pt_core_news_lg), são extraídas entidades:

Pessoas (com ocupação ou títulos)

Lugares (GPE e LOC)

Resultados guardados em CSV e convertidos com:

**Script:** generate_indice_entidades.py

### 7 - Foco nos campos ScopeContent e BiogHist
Estes campos são os principais para análise de conteúdo e extração de entidades.

### 8 - Exploração de Thesaurus

Estrutura usada para a contrução do HTML, como indicado no ponto 4.

#### Estrutura de Pastas Esperada
```
Famalicao/
├── registosFamalicao_xml/
├── htmlFamalicao/
├── entidades_Famalicao.csv
├── entidades_Famalicao.html
├── index_estruturado_Famalicao.html
```
## Requisitos
1. Python 3.8+

2. Bibliotecas:

    1. sickle

    2. spacy

    3. pt_core_news_lg

## Como correr
```
python download_records.py <Cidade>
python generate_html.py <Cidade>
python generate_index_estruturado.py <Cidade>
python extract_entities.py <Cidade>
python generate_indice_entidades.py <Cidade>
python pesquisa.py <Cidade>
```