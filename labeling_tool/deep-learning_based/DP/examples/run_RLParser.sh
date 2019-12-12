#!/usr/bin/env bash
CUDA_VISIBLE_DEVICES=0
python examples/StackPointerParser.py --mode FastLSTM --num_epochs 200 --batch_size 32 --decoder_input_size 256 --hidden_size 512 --encoder_layers 2 --decoder_layers 2 \
 --pos_dim 100 --char_dim 100 --num_filters 100 --arc_space 512 --type_space 128 \
 --opt adam --learning_rate 0.001 --decay_rate 0.75 --epsilon 1e-4 --coverage 0.0 --gamma 0.0 --clip 5.0 \
 --schedule 20 --double_schedule_decay 5 --max_decay 9 \
 --p_in 0.33 --p_out 0.33 --p_rnn 0.33 0.33 --unk_replace 0.5 --label_smooth 1.0 --pos --char --beam 10 --prior_order inside_out \
 --grandPar --sibling \
 --elmo --elmo_path "elmo/model" --elmo_dim 2048 \
 --word_embedding NNLM --word_path "data/embedding/NNLM_clean.txt" --char_embedding random \
 --punctuation '.' '``' "''" ':' ',' \
 --train "data/sejong/train.conllx" \
 --dev "data/sejong/test.conllx" \
 --model_path "models/parsing/stack_ptr/" --model_name 'network.pt' \
 --pos_embedding 4 --pos_path "data/embedding/14_skipgram_100.vec"
