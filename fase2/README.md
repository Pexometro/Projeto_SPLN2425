# Pesquisa Semântica com SentenceTransformer (SPLN TP2)

## Grupo de Trabalho

- **Jorge Teixeira** - PG55965 - [JorgeTeixeira20](https://github.com/JorgeTeixeira20) 
- **Rui Pinto** - PG56010 - [RuiPintoUM](https://github.com/RuiPintoUM)
- **Pedro Azevedo** - PG57897 - [Pexometro](https://github.com/Pexometro)

## Visão Geral
Este projeto implementa um sistema de pesquisa semântica baseado em similaridade de textos, utilizando metadados de dissertações da coleção `col_1822_21316` do RepositóriUM. O processo envolve extrair dados via OAI-PMH, convertê-los para JSON, gerar pares de treino com similaridades heurísticas, treinar modelos SentenceTransformer e recuperar os documentos mais relevantes para consultas de utilizador.

## Dependências
- Python 3.8
- Pacotes necessários:
  ```bash
  pip install requests beautifulsoup4 sentence-transformers tensorflow-cpu
  ```

## Estrutura de Diretórios
- `OAI.xml`: Metadados brutos extraídos do RepositóriUM.
- `ColDoc.json`: Documentos estruturados (título, resumo, palavras-chave).
- `ColTrain.json`: Pares de treino (texto1, texto2, similaridade).
- `my_sentence_model_*/`: Modelos treinados e registos (e.g., `my_sentence_model_thr0.0_k5_e3_bs16/`).
- `eval/`: Resultados de inferência (e.g., `eval_query_dl_thr0.0_k5.txt`).
- `create_xml.py`: Extrai metadados via OAI-PMH.
- `create_json.py`: Converte XML para JSON.
- `02_treino_modelo_sentence_transformer.py`: Gera `ColTrain.json` e treina modelos.
- `03_inferencia.py`: Realiza pesquisa semântica.
- `run_trainings.sh`, `run_inferences.sh`: Scripts para execução em lote.
- `train_log.txt`, `inference_log.txt`: Registos de execução.

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

## Resultados
- **Melhor Modelo**: `thr0.0_k5_e3_bs16` (pontuações: 0.6218 para "segurança e privacidade em cloud computing", 0.4129 para "desenvolvimento de sistemas distribuídos tolerantes a falhas").
- **Consultas Fortes**:
  - Segurança em cloud: Resultados relevantes (e.g., “Análise de segurança para soluções de software para a cloud”).
  - Sistemas distribuídos: Títulos relevantes (e.g., “Verification of distributed algorithms with the Why3 tool”).
- **Consulta Fraca**: "inteligência artificial explicável" (pontuação máxima 0.3588), provavelmente devido à limitada cobertura no `ColDoc.json`.
- Resultados completos em `eval/eval_query_*.txt`.

## Exemplo de Uso
Executar uma consulta única:
```bash
python3 03_inferencia.py --model my_sentence_model_thr0.0_k5_e3_bs16 --docs ColDoc.json --query "segurança e privacidade em cloud computing" --top_k 5
```
Exemplo de saída:
```
Top 5 resultados para: “segurança e privacidade em cloud computing”
01. [0.6218] Análise de segurança para soluções de software para a cloud
02. [0.5703] Reforço da privacidade através do controlo da pegada digital
03. [0.4436] Middleware de acesso coerente a serviços de bases de dados na nuvem
04. [0.4185] Navegação segura - análise do uso de HTTPS na perspectiva do utilizador final
05. [0.3352] Integração de uma aplicação de reporting para testes de software no confluence cloud
```

## Notas
- Foram observados avisos do TensorFlow (e.g., AVX2, computation placer); usar `tensorflow-cpu` resolve problemas de GPU:
  ```bash
  pip uninstall tensorflow
  pip install tensorflow-cpu
  ```
- O ficheiro `ColDoc.json` tem cobertura limitada para inteligência artificial explicável, impactando o desempenho dessa consulta.
- Métricas de validação em `my_sentence_model_*/eval/train.txt` indicam que `thr0.0_k5_e3_bs16` é eficiente (e.g., Pearson cosseno ~0.65).
