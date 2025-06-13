# Run training commands sequentially

python3 02_treino_modelo_sentence_transformer.py \                            
  --threshold 0.0 --top_k 5  --epochs 3  --batch_size 16 \
  --output_path my_sentence_model \
> my_sentence_model_thr0.0_k5_e3_bs16/eval/train.txt

python3 02_treino_modelo_sentence_transformer.py \
  --threshold 0.0 --top_k 10 --epochs 5 --batch_size 16 \
  --output_path my_sentence_model \
> my_sentence_model_thr0.0_k10_e5_bs16/eval/train.txt

python3 02_treino_modelo_sentence_transformer.py \
  --threshold 0.05 --top_k 10 --epochs 5 --batch_size 16 \
  --output_path my_sentence_model \
> my_sentence_model_thr0.05_k10_e5_bs16/eval/train.txt

python3 02_treino_modelo_sentence_transformer.py \
  --threshold 0.1 --top_k 20 --epochs 5 --batch_size 16 \
  --output_path my_sentence_model \
> my_sentence_model_thr0.1_k20_e5_bs16/eval/train.txt

python3 02_treino_modelo_sentence_transformer.py \
  --threshold 0.0 --top_k 20 --epochs 10 --batch_size 32 \
  --output_path my_sentence_model \
> my_sentence_model_thr0.0_k20_e10_bs32/eval/train.txt

echo "All training commands completed."