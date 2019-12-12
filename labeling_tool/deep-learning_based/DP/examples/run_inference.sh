#!/usr/bin/env bash
CUDA_VISIBLE_DEVICES=0
python examples/inference.py --parser stackptr --beam 10 --ordered --gpu \
 --punctuation '.' '``' "''" ':' ',' --pos_embedding 4 \
 --test "data/sejong/test.conllx" \
 --bert --bert_path "bert/" --bert_feature_dim 1600 --etri_test "data/etri_data/etri.test.conllx"\
 --model_path "models/stack_ptr/RL_BERT" --model_name 'network.pt'
