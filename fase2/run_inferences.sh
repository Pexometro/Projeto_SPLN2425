#!/bin/bash

# Create necessary directories
mkdir -p eval

# Run inference commands sequentially
python3 03_inferencia.py --model my_sentence_model_thr0.0_k5_e3_bs16 --docs ColDoc.json --query "deep learning para imagens médicas" --top_k 5 > eval/eval_query_dl_thr0.0_k5.txt
python3 03_inferencia.py --model my_sentence_model_thr0.0_k5_e3_bs16 --docs ColDoc.json --query "segurança e privacidade em cloud computing" --top_k 5 > eval/eval_query_privacidade_thr0.0_k5.txt
python3 03_inferencia.py --model my_sentence_model_thr0.0_k5_e3_bs16 --docs ColDoc.json --query "mineração de dados em contextos clínicos" --top_k 5 > eval/eval_query_saude_thr0.0_k5.txt
python3 03_inferencia.py --model my_sentence_model_thr0.0_k5_e3_bs16 --docs ColDoc.json --query "inteligência artificial explicável" --top_k 5 > eval/eval_query_IA_thr0.0_k5.txt
python3 03_inferencia.py --model my_sentence_model_thr0.0_k5_e3_bs16 --docs ColDoc.json --query "desenvolvimento de sistemas distribuídos tolerantes a falhas" --top_k 5 > eval/eval_query_distribuidos_thr0.0_k5.txt

python3 03_inferencia.py --model my_sentence_model_thr0.0_k10_e5_bs16 --docs ColDoc.json --query "deep learning para imagens médicas" --top_k 5 > eval/eval_query_dl_thr0.0_k10.txt
python3 03_inferencia.py --model my_sentence_model_thr0.0_k10_e5_bs16 --docs ColDoc.json --query "segurança e privacidade em cloud computing" --top_k 5 > eval/eval_query_privacidade_thr0.0_k10.txt
python3 03_inferencia.py --model my_sentence_model_thr0.0_k10_e5_bs16 --docs ColDoc.json --query "mineração de dados em contextos clínicos" --top_k 5 > eval/eval_query_saude_thr0.0_k10.txt
python3 03_inferencia.py --model my_sentence_model_thr0.0_k10_e5_bs16 --docs ColDoc.json --query "inteligência artificial explicável" --top_k 5 > eval/eval_query_IA_thr0.0_k10.txt
python3 03_inferencia.py --model my_sentence_model_thr0.0_k10_e5_bs16 --docs ColDoc.json --query "desenvolvimento de sistemas distribuídos tolerantes a falhas" --top_k 5 > eval/eval_query_distribuidos_thr0.0_k10.txt

python3 03_inferencia.py --model my_sentence_model_thr0.05_k10_e5_bs16 --docs ColDoc.json --query "deep learning para imagens médicas" --top_k 5 > eval/eval_query_dl_thr0.05_k10.txt
python3 03_inferencia.py --model my_sentence_model_thr0.05_k10_e5_bs16 --docs ColDoc.json --query "segurança e privacidade em cloud computing" --top_k 5 > eval/eval_query_privacidade_thr0.05_k10.txt
python3 03_inferencia.py --model my_sentence_model_thr0.05_k10_e5_bs16 --docs ColDoc.json --query "mineração de dados em contextos clínicos" --top_k 5 > eval/eval_query_saude_thr0.05_k10.txt
python3 03_inferencia.py --model my_sentence_model_thr0.05_k10_e5_bs16 --docs ColDoc.json --query "inteligência artificial explicável" --top_k 5 > eval/eval_query_IA_thr0.05_k10.txt
python3 03_inferencia.py --model my_sentence_model_thr0.05_k10_e5_bs16 --docs ColDoc.json --query "desenvolvimento de sistemas distribuídos tolerantes a falhas" --top_k 5 > eval/eval_query_distribuidos_thr0.05_k10.txt

python3 03_inferencia.py --model my_sentence_model_thr0.1_k20_e5_bs16 --docs ColDoc.json --query "deep learning para imagens médicas" --top_k 5 > eval/eval_query_dl_thr0.1_k20.txt
python3 03_inferencia.py --model my_sentence_model_thr0.1_k20_e5_bs16 --docs ColDoc.json --query "segurança e privacidade em cloud computing" --top_k 5 > eval/eval_query_privacidade_thr0.1_k20.txt
python3 03_inferencia.py --model my_sentence_model_thr0.1_k20_e5_bs16 --docs ColDoc.json --query "mineração de dados em contextos clínicos" --top_k 5 > eval/eval_query_saude_thr0.1_k20.txt
python3 03_inferencia.py --model my_sentence_model_thr0.1_k20_e5_bs16 --docs ColDoc.json --query "inteligência artificial explicável" --top_k 5 > eval/eval_query_IA_thr0.1_k20.txt
python3 03_inferencia.py --model my_sentence_model_thr0.1_k20_e5_bs16 --docs ColDoc.json --query "desenvolvimento de sistemas distribuídos tolerantes a falhas" --top_k 5 > eval/eval_query_distribuidos_thr0.1_k20.txt

python3 03_inferencia.py --model my_sentence_model_thr0.0_k20_e10_bs32 --docs ColDoc.json --query "deep learning para imagens médicas" --top_k 5 > eval/eval_query_dl_thr0.0_k20.txt
python3 03_inferencia.py --model my_sentence_model_thr0.0_k20_e10_bs32 --docs ColDoc.json --query "segurança e privacidade em cloud computing" --top_k 5 > eval/eval_query_privacidade_thr0.0_k20.txt
python3 03_inferencia.py --model my_sentence_model_thr0.0_k20_e10_bs32 --docs ColDoc.json --query "mineração de dados em contextos clínicos" --top_k 5 > eval/eval_query_saude_thr0.0_k20.txt
python3 03_inferencia.py --model my_sentence_model_thr0.0_k20_e10_bs32 --docs ColDoc.json --query "inteligência artificial explicável" --top_k 5 > eval/eval_query_IA_thr0.0_k20.txt
python3 03_inferencia.py --model my_sentence_model_thr0.0_k20_e10_bs32 --docs ColDoc.json --query "desenvolvimento de sistemas distribuídos tolerantes a falhas" --top_k 5 > eval/eval_query_distribuidos_thr0.0_k20.txt

echo "All inference commands completed."