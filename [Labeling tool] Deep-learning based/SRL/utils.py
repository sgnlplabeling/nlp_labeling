# -*- coding: utf-8 -*-

from __future__ import print_function
import os
import re
import numpy as np
import codecs
import torch.nn as nn
from torch.nn import init


models_path = "./models"
eval_path = "./evaluation"
eval_temp = os.path.join(eval_path, "temp")
eval_script = os.path.join(eval_path, "conlleval")

def adjust_learning_rate(optimizer, lr):

    for param_group in optimizer.param_groups:
        param_group['lr'] = lr

def create_dico(item_list):

    assert type(item_list) is list
    dico = {}
    for items in item_list:
        for item in items:
            if item not in dico:
                dico[item] = 1
            else:
                dico[item] += 1
    return dico


def create_mapping(dico):

    sorted_items = sorted(dico.items(), key=lambda x: (-x[1], x[0]))
    id_to_item = {i: v[0] for i, v in enumerate(sorted_items)}
    item_to_id = {v: k for k, v in id_to_item.items()}
    return item_to_id, id_to_item


def zero_digits(s):

    return re.sub('\d', '0', s)



def insert_singletons(words, singletons, p=0.5):

    new_words = []
    for word in words:
        if word in singletons and np.random.uniform() < p:
            new_words.append(0)
        else:
            new_words.append(word)
    return new_words

def create_input(data,singletons=None):
    
    words = data['words']
    words1 = data['words1']
    words2 = data['words2']
    words3 = data['words3']

    if singletons is not None:
        words = insert_singletons(words, singletons)
        words1 = insert_singletons(words1, singletons)
        words2 = insert_singletons(words2, singletons)
        words3 = insert_singletons(words3, singletons)

    input = {}
    input['words'] = words
    input['words1'] = words1
    input['words2'] = words2
    input['words3'] = words3
    input['tags'] = data['tags']

    return input

def init_word_embeddings(parameters, id_to_word, path, word_dim):
    n_words = len(id_to_word)
    shape = [n_words, word_dim]
    drange = np.sqrt(6. / (np.sum(shape)))
    value = drange * np.random.uniform(low=-1.0, high=1.0, size=shape)
    new_weights = value
    if parameters['is_pre_emb']:
        print('Loading pretrained embeddings from %s' % path)
        pretrained = {}
        emb_invalid = 0 
        for i , line in enumerate(codecs.open(path, 'r', 'utf-8')):
            line = line.rstrip().split()
            if len(line) == word_dim + 1:
                pretrained[line[0]] = np.array([float(x) for x in line[1:]]).astype(np.float32)
            else:
                emb_invalid += 1
        if emb_invalid > 0:
            print('WARNING: %i invalid lines' % emb_invalid)
        c_found = 0 
        c_lower = 0 
        c_zeros = 0 
        # Lookup table initialization
        for i in range(n_words):
            word = id_to_word[i]
            if word in pretrained:
                new_weights[i] = pretrained[word]
                c_found += 1
            elif word.lower() in pretrained:
                new_weights[i] = pretrained[word.lower()]
                c_lower += 1
            elif re.sub('\d','0',word) in pretrained:
                new_weights[i] = pretrained[re.sub('\d','0',word)]
                c_zeros += 1
            elif re.sub('\d','#',word) in pretrained:
                new_weights[i] = pretrained[re.sub('\d','#',word)]		
#        else:
#            print(word)
             

        print('Loaded %i pretrained embeddings.' % len(pretrained))
        print(('%i / %i (%.4f%%) words have been initialized with pretrained embeddings.') % (c_found + c_lower + c_zeros, n_words, 100. * (c_found + c_lower + c_zeros) / n_words))
        print(('%i found directly, %i after lowercasing, %i after lowercasing + zero.') % (c_found, c_lower, c_zeros))
    return new_weights


def init_linear(input_linear):

    bias = np.sqrt(6.0 / (input_linear.weight.size(0) + input_linear.weight.size(1)))
    nn.init.uniform(input_linear.weight, -bias, bias)
    if input_linear.bias is not None:
        input_linear.bias.data.zero_()



def init_lstm(input_lstm):

    for ind in range(0, input_lstm.num_layers):
        weight = eval('input_lstm.weight_ih_l' + str(ind))
        bias = np.sqrt(6.0 / (weight.size(0) / 4 + weight.size(1)))
        nn.init.uniform(weight, -bias, bias)
        weight = eval('input_lstm.weight_hh_l' + str(ind))
        bias = np.sqrt(6.0 / (weight.size(0) / 4 + weight.size(1)))
        nn.init.uniform(weight, -bias, bias)
    if input_lstm.bidirectional:
        for ind in range(0, input_lstm.num_layers):
            weight = eval('input_lstm.weight_ih_l' + str(ind) + '_reverse')
            bias = np.sqrt(6.0 / (weight.size(0) / 4 + weight.size(1)))
            nn.init.uniform(weight, -bias, bias)
            weight = eval('input_lstm.weight_hh_l' + str(ind) + '_reverse')
            bias = np.sqrt(6.0 / (weight.size(0) / 4 + weight.size(1)))
            nn.init.uniform(weight, -bias, bias)

    if input_lstm.bias:
        for ind in range(0, input_lstm.num_layers):
            weight = eval('input_lstm.bias_ih_l' + str(ind))
            weight.data.zero_()
            weight.data[input_lstm.hidden_size: 2 * input_lstm.hidden_size] = 1
            weight = eval('input_lstm.bias_hh_l' + str(ind))
            weight.data.zero_()
            weight.data[input_lstm.hidden_size: 2 * input_lstm.hidden_size] = 1
        if input_lstm.bidirectional:
            for ind in range(0, input_lstm.num_layers):
                weight = eval('input_lstm.bias_ih_l' + str(ind) + '_reverse')
                weight.data.zero_()
                weight.data[input_lstm.hidden_size: 2 * input_lstm.hidden_size] = 1
                weight = eval('input_lstm.bias_hh_l' + str(ind) + '_reverse')
                weight.data.zero_()
                weight.data[input_lstm.hidden_size: 2 * input_lstm.hidden_size] = 1


