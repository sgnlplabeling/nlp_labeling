# -*- coding=utf-8 -*-
__author__ = 'max'

import sys
import os

sys.path.append(".")
sys.path.append("..")

import time
import argparse
import uuid
import json

import numpy as np
import torch
from neuronlp2.io import get_logger, conllx_stacked_data, conllx_data
from neuronlp2.io import CoNLLXWriter
from neuronlp2.tasks import parser
from neuronlp2.models import StackPtrNet, BiRecurrentConvBiAffine
from neuronlp2 import utils

uid = uuid.uuid4().hex[:6]

def main():
    args_parser = argparse.ArgumentParser(description='Tuning with stack pointer parser')
    args_parser.add_argument('--parser', choices=['stackptr', 'biaffine'], help='Parser', default='stackptr')
    args_parser.add_argument('--test')
    args_parser.add_argument('--model_path', help='path for saving model file.', required=True)
    args_parser.add_argument('--model_name', help='name for saving model file.', default='network.pt')
    args_parser.add_argument('--punctuation', nargs='+', type=str, help='List of punctuations')
    args_parser.add_argument('--beam', type=int, default=1, help='Beam size for decoding')
    args_parser.add_argument('--ordered', action='store_true', help='Using order constraints in decoding')
    args_parser.add_argument('--gpu', action='store_true', help='Using GPU')
    args_parser.add_argument('--pos_embedding', type=int, default=4)
    args_parser.add_argument('--bert', action='store_true', help='use elmo embedding.')
    args_parser.add_argument('--bert_path', help='path for bert embedding model.')
    args_parser.add_argument('--bert_feature_dim', type=int, help='dimension for bert feature embedding')
    args_parser.add_argument('--etri_test', help='path for etri data of bert')

    args = args_parser.parse_args()

    logger = get_logger("Analyzer")

    test_path = args.test
    model_path = args.model_path
    model_name = args.model_name

    punct_set = None
    punctuation = args.punctuation
    if punctuation is not None:
        punct_set = set(punctuation)
        logger.info("punctuations(%d): %s" % (len(punct_set), ' '.join(punct_set)))

    use_gpu = args.gpu
    parser = args.parser
    if parser == 'stackptr':
        stackptr(model_path, model_name, test_path, punct_set, use_gpu, logger, args)
    else:
        raise ValueError('Unknown parser: %s' % parser)


def stackptr(model_path, model_name, test_path, punct_set, use_gpu, logger, args):
    pos_embedding = args.pos_embedding
    alphabet_path = os.path.join(model_path, 'alphabets/')
    model_name = os.path.join(model_path, model_name)
    word_alphabet, char_alphabet, pos_alphabet, type_alphabet = conllx_stacked_data.create_alphabets\
        (alphabet_path,None, pos_embedding,data_paths=[None, None], max_vocabulary_size=50000, embedd_dict=None)

    num_words = word_alphabet.size()
    num_chars = char_alphabet.size()
    num_pos = pos_alphabet.size()
    num_types = type_alphabet.size()

    logger.info("Word Alphabet Size: %d" % num_words)
    logger.info("Character Alphabet Size: %d" % num_chars)
    logger.info("POS Alphabet Size: %d" % num_pos)
    logger.info("Type Alphabet Size: %d" % num_types)

    beam = args.beam
    ordered = args.ordered
    use_bert = args.bert
    bert_path = args.bert_path
    bert_feature_dim = args.bert_feature_dim
    if use_bert:
        etri_test_path = args.etri_test
    else:
        etri_test_path = None

    def load_model_arguments_from_json():
        arguments = json.load(open(arg_path, 'r'))
        return arguments['args'], arguments['kwargs']

    arg_path = model_name + '.arg.json'
    args, kwargs = load_model_arguments_from_json()

    prior_order = kwargs['prior_order']
    logger.info('use gpu: %s, beam: %d, order: %s (%s)' % (use_gpu, beam, prior_order, ordered))

    data_test = conllx_stacked_data.read_stacked_data_to_variable(test_path, word_alphabet, char_alphabet, pos_alphabet, type_alphabet, pos_embedding,
                                                                  use_gpu=use_gpu, volatile=True, prior_order=prior_order, is_test=False,
                                                                  bert=use_bert, etri_path=etri_test_path)

    pred_writer = CoNLLXWriter(word_alphabet, char_alphabet, pos_alphabet, type_alphabet, pos_embedding)

    logger.info('model: %s' % model_name)
    word_path = os.path.join(model_path, 'embedding.txt')
    word_dict, word_dim = utils.load_embedding_dict('NNLM', word_path)
    def get_embedding_table():
        table = np.empty([len(word_dict), word_dim])
        for idx,(word, embedding) in enumerate(word_dict.items()):
            try:
                table[idx, :] = embedding
            except:
                print(word)
        return torch.from_numpy(table)

    def construct_word_embedding_table():
        scale = np.sqrt(3.0 / word_dim)
        table = np.empty([word_alphabet.size(), word_dim], dtype=np.float32)
        table[conllx_stacked_data.UNK_ID, :] = np.random.uniform(-scale, scale, [1, word_dim]).astype(np.float32)
        oov = 0
        for word, index in list(word_alphabet.items()):
            if word in word_dict:
                embedding = word_dict[word]
            elif word.lower() in word_dict:
                embedding = word_dict[word.lower()]
            else:
                embedding = np.random.uniform(-scale, scale, [1, word_dim]).astype(np.float32)
                oov += 1
            table[index, :] = embedding
        print('word OOV: %d' % oov)
        return torch.from_numpy(table)

    # word_table = get_embedding_table()
    word_table = construct_word_embedding_table()
    # kwargs['embedd_word'] = word_table
    # args[1] = len(word_dict) # word_dim

    network = StackPtrNet(*args, **kwargs, bert=use_bert, bert_path=bert_path, bert_feature_dim=bert_feature_dim)
    network.load_state_dict(torch.load(model_name))
    """
    model_dict = network.state_dict()
    pretrained_dict = torch.load(model_name)
    model_dict.update({k:v for k,v in list(pretrained_dict.items())
        if k != 'word_embedd.weight'})
    
    network.load_state_dict(model_dict)
    """

    if use_gpu:
        network.cuda()
    else:
        network.cpu()

    network.eval()

    if not ordered:
        pred_writer.start(model_path + '/inference.txt')
    else:
        pred_writer.start(model_path + '/RL_B[test].txt')
    sent = 1

    dev_ucorr_nopunc = 0.0
    dev_lcorr_nopunc = 0.0
    dev_total_nopunc = 0
    dev_ucomlpete_nopunc = 0.0
    dev_lcomplete_nopunc = 0.0
    dev_total_inst = 0.0
    sys.stdout.write('Start!\n')
    start_time = time.time()
    for batch in conllx_stacked_data.iterate_batch_stacked_variable(data_test, 1, pos_embedding, type='dev', bert=use_bert):
        if sent % 100 == 0:
            ####
            print('Wo Punct: ucorr: %d, lcorr: %d, total: %d, uas: %.2f%%, las: %.2f%%, ucm: %.2f%%, lcm: %.2f%%' % (
                dev_ucorr_nopunc, dev_lcorr_nopunc, dev_total_nopunc, dev_ucorr_nopunc * 100 / dev_total_nopunc,
                dev_lcorr_nopunc * 100 / dev_total_nopunc, dev_ucomlpete_nopunc * 100 / dev_total_inst,
                dev_lcomplete_nopunc * 100 / dev_total_inst))
            sys.stdout.write('[%d/%d]\n' %(sent, int(data_test[2][0])))
            ####
        sys.stdout.flush()
        sent += 1

        input_encoder, input_decoder = batch
        word, char, pos, heads, types, masks_e, lengths, word_bert = input_encoder
        stacked_heads, children, sibling, stacked_types, skip_connect, previous, nexts, masks_d, lengths_d = input_decoder
        heads_pred, types_pred, _, _ = network.decode(word, char, pos, previous, nexts, stacked_heads, mask_e=masks_e, mask_d=masks_d,
                                                              length=lengths, beam=beam, leading_symbolic=conllx_stacked_data.NUM_SYMBOLIC_TAGS, input_word_bert=word_bert)
        """
        stacked_heads = stacked_heads.data
        children = children.data
        stacked_types = stacked_types.data
        children_pred = torch.from_numpy(children_pred).long()
        stacked_types_pred = torch.from_numpy(stacked_types_pred).long()
        if use_gpu:
            children_pred = children_pred.cuda()
            stacked_types_pred = stacked_types_pred.cuda()
        """

        word = word.data.cpu().numpy()
        pos = pos.data.cpu().numpy()
        lengths = lengths.cpu().numpy()
        heads = heads.data.cpu().numpy()
        types = types.data.cpu().numpy()

        pred_writer.test_write(word, pos, heads_pred, types_pred, lengths, symbolic_root=True)
###########
        stats, stats_nopunc, _, num_inst = parser.eval(word, pos, heads_pred, types_pred, heads, types,
                                                                word_alphabet, pos_alphabet, lengths,
                                                                punct_set=punct_set, symbolic_root=True)

        ucorr_nopunc, lcorr_nopunc, total_nopunc, ucm_nopunc, lcm_nopunc = stats_nopunc
        dev_ucorr_nopunc += ucorr_nopunc
        dev_lcorr_nopunc += lcorr_nopunc
        dev_total_nopunc += total_nopunc
        dev_ucomlpete_nopunc += ucm_nopunc
        dev_lcomplete_nopunc += lcm_nopunc

        dev_total_inst += num_inst
    end_time = time.time()
################
    pred_writer.close()

    print('\nFINISHED!!\n', end_time - start_time)
    print('Wo Punct: ucorr: %d, lcorr: %d, total: %d, uas: %.2f%%, las: %.2f%%, ucm: %.2f%%, lcm: %.2f%%' % (
        dev_ucorr_nopunc, dev_lcorr_nopunc, dev_total_nopunc, dev_ucorr_nopunc * 100 / dev_total_nopunc,
        dev_lcorr_nopunc * 100 / dev_total_nopunc, dev_ucomlpete_nopunc * 100 / dev_total_inst,
        dev_lcomplete_nopunc * 100 / dev_total_inst))

if __name__ == '__main__':
    os.environ["CUDA_DEVICE_ORDER"]="PCI_BUS_ID"
    os.environ["CUDA_VISIBLE_DEVICES"]="0"
    main()
