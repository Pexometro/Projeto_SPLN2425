# Pesquisa Semântica com SentenceTransformer (SPLN TP2)

## Grupo de Trabalho
- **Jorge Teixeira** - PG55965 - [JorgeTeixeira20](https://github.com/JorgeTeixeira20)
- **Rui Pinto** - PG56010 - [RuiPintoUM](https://github.com/RuiPintoUM)
- **Pedro Azevedo** - PG57897 - [Pexometro](https://github.com/Pexometro)

## Visão Geral
Este projeto tem como objetivo principal desenvolver um sistema de recuperação de informação baseado em similaridade semântica, utilizando metadados de dissertações académicas da coleção `col_1822_21316` do RepositóriUM (teses de mestrado do Departamento de Informática da UMinho). A metodologia envolve a extração de dados via OAI-PMH, conversão para JSON, geração de pares de treino com similaridades heurísticas baseadas em palavras-chave, treino de modelos SentenceTransformer, e implementação de uma função de recuperação de documentos relevantes para consultas de utilizador. O trabalho foi desenvolvido no âmbito da unidade curricular de Sistemas de Processamento de Linguagem Natural (SPLN) no 2º semestre de 2024/2025.

## Dependências
- Python 3.8
- Pacotes necessários:
  ```bash
  pip install requests beautifulsoup4 sentence-transformers tensorflow-cpu
  ```

## Estrutura de Diretórios
- `OAI.xml`: Metadados brutos extraídos do RepositóriUM via OAI-PMH.
- `ColDoc.json`: Coleção de documentos estruturados com campos `title`, `abstract`, e `keywords`.
- `ColTrain.json`: Pares de treino consistindo em `(texto1, texto2, similaridade)`.
- `my_sentence_model_*/`: Diretórios contendo modelos treinados e métricas de validação (e.g., `my_sentence_model_thr0.0_k5_e3_bs16/`).
- `eval/`: Resultados de inferência para várias consultas (e.g., `eval_query_dl_thr0.0_k5.txt`).
- `create_xml.py`: Script para extração de metadados do RepositóriUM.
- `create_json.py`: Script para conversão de XML para JSON.
- `02_treino_modelo_sentence_transformer.py`: Script para geração de `ColTrain.json` e treino dos modelos.
- `03_inferencia.py`: Script para realização da pesquisa semântica.
- `run_trainings.sh`, `run_inferences.sh`: Scripts shell para execução em lote de treino e inferência.
- `train_log.txt`, `inference_log.txt`: Ficheiros de registo das execuções.

## Configuração
1. Criar diretórios necessários:
   ```bash
   mkdir -p my_sentence_model_thr0.0_k5_e3_bs16/eval my_sentence_model_thr0.0_k10_e5_bs16/eval my_sentence_model_thr0.05_k10_e5_bs16/eval my_sentence_model_thr0.1_k20_e5_bs16/eval my_sentence_model_thr0.0_k20_e10_bs32/eval eval
   ```
2. Configurar um ambiente conda:
   ```bash
   conda create -n sentence_transformers python=3.8
   conda activate sentence_transformers
   pip install requests beautifulsoup4 sentence-transformers tensorflow-cpu
   ```

## Metodologia
### Extração e Conversão de Dados
- Dados extraídos do RepositóriUM usando `create_xml.py` com pedidos OAI-PMH e salvos em `OAI.xml`.
- Conversão para `ColDoc.json` realizada por `create_json.py`, extraindo `title`, `abstract`, e `keywords` com `BeautifulSoup`.

### Geração de Pares de Treino
- Função `guess_sim` em `02_treino_modelo_sentence_transformer.py` calcula similaridade Jaccard baseada em palavras-chave, títulos e resumos.
- Pares filtrados com limiares (`threshold`) de 0.0, 0.05, e 0.1, e `top_k` variando de 5 a 20, gerando `ColTrain.json`.

### Treino do Modelo
- Modelo base: `paraphrase-multilingual-MiniLM-L12-v2`.
- Treino com `CosineSimilarityLoss` por 3 a 10 épocas, com `batch_size` de 16 a 32.
- Hiperparâmetros testados: `threshold` (0.0, 0.05, 0.1), `top_k` (5, 10, 20), `epochs` (3, 5, 10), `batch_size` (16, 32).
- Modelos salvos em `my_sentence_model_thrX.X_kX_eX_bsX/`.

### Recuperação de Documentos
- `03_inferencia.py` codifica consultas e resumos com embeddings, calcula similaridade cosseno, e retorna os top-5 resultados.

## Execução do Projeto
1. Extrair e converter dados:
   ```bash
   python3 create_xml.py
   python3 create_json.py
   ```
2. Treinar modelos:
   ```bash
   nohup ./run_trainings.sh > train_log.txt 2>&1 &
   ```
3. Executar inferência:
   ```bash
   nohup ./run_inferences.sh > inference_log.txt 2>&1 &
   ```

## Relatório

### Análise de Resultados
Foram treinados cinco modelos com diferentes hiperparâmetros e testados em cinco consultas. Abaixo, uma visão geral dos melhores resultados por consulta:

- **"segurança e privacidade em cloud computing"**:
  - Melhor modelo: `thr0.0_k5_e3_bs16` (score: 0.6218)
  - Top 5: 
    1. [0.6218] Análise de segurança para soluções de software para a cloud
    2. [0.5703] Reforço da privacidade através do controlo da pegada digital
    3. [0.4436] Middleware de acesso coerente a serviços de bases de dados na nuvem
    4. [0.4185] Navegação segura - análise do uso de HTTPS na perspectiva do utilizador final
    5. [0.3352] Integração de uma aplicação de reporting para testes de software no confluence cloud

- **"deep learning para imagens médicas"**:
  - Melhor modelo: `thr0.0_k20_e10_bs32` (score: 0.3580)
  - Top 5: Menos relevante (e.g., [0.3580] Otimizações de armazenamento distribuído para aprendizagem profunda).

- **"mineração de dados em contextos clínicos"**:
  - Melhor modelo: `thr0.0_k20_e10_bs32` (score: 0.4286)
  - Top 5: Inclui resultados relevantes (e.g., [0.4286] O impacto da aplicação de modelos de maturidade...).

- **"inteligência artificial explicável"**:
  - Melhor modelo: `thr0.05_k10_e5_bs16` (score: 0.3588)
  - Top 5: Resultados fracos (e.g., [0.3588] Automatic driving...), indicando limitação do dataset.

- **"desenvolvimento de sistemas distribuídos tolerantes a falhas"**:
  - Melhor modelo: `thr0.0_k5_e3_bs16` (score: 0.4129)
  - Top 5: Relevantes (e.g., [0.4129] Verification of distributed algorithms with the Why3 tool).

### Desafios e Limitações
- **Avisos do TensorFlow**: Observados durante o treino (e.g., AVX2, computation placer), resolvidos com `tensorflow-cpu`.
- **Cobertura do Dataset**: A consulta "inteligência artificial explicável" teve desempenho inferior devido à ausência de documentos relevantes em `ColDoc.json`.
- **Escalabilidade**: O processo de geração de pares em `ColTrain.json` é computacionalmente intensivo para grandes coleções.

### Melhorias Futuras
- Aumentar a coleção `ColDoc.json` com mais dissertações relevantes.
- Implementar métricas de avaliação (e.g., precisão@5, recall@5) com um conjunto de validação anotado.
- Otimizar `guess_sim` com pesos diferenciados para palavras-chave raras.
- Explorar modelos mais avançados (e.g., `all-MiniLM-L6-v2`) para melhorar a precisão.

## Exemplo de Uso
Executar uma consulta única:
```bash
python3 03_inferencia.py --model my_sentence_model_thr0.0_k5_e3_bs16 --docs ColDoc.json --query "segurança e privacidade em cloud computing" --top_k 5
```
Exemplo de output:
```
Top 5 resultados para: “segurança e privacidade em cloud computing”
01. [0.6218] Análise de segurança para soluções de software para a cloud
02. [0.5703] Reforço da privacidade através do controlo da pegada digital
03. [0.4436] Middleware de acesso coerente a serviços de bases de dados na nuvem
04. [0.4185] Navegação segura - análise do uso de HTTPS na perspectiva do utilizador final
05. [0.3352] Integração de uma aplicação de reporting para testes de software no confluence cloud
```

## Conclusão
O sistema desenvolvido alcança bons resultados para consultas relacionadas com segurança em cloud e sistemas distribuídos, com o modelo `thr0.0_k5_e3_bs16` como o mais eficiente. Apesar das limitações do dataset, o projeto demonstra a viabilidade de um sistema de recuperação semântica baseado em SentenceTransformer, com potencial para melhorias futuras.

## Referências
- Documentação SentenceTransformers: [https://www.sbert.net/](https://www.sbert.net/)
- RepositóriUM OAI-PMH: [https://repositorium.sdum.uminho.pt/oai/oai](https://repositorium.sdum.uminho.pt/oai/oai)

## Notas
- O diretório `my_sentence_model_*` e ficheiros de log foram excluídos do controlo de versões via `.gitignore` para otimizar o repositório.
- Data de submissão: 14 de junho de 2025.