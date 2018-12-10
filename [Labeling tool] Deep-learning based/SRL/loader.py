# -*- coding: utf-8 -*-

from __future__ import print_function, division
import os
import re
import codecs
import unicodedata
from utils import create_dico, create_mapping, zero_digits
import model
import string
import random
import numpy as np


def load_sentences(path, lower, zeros):
    """
    Load sentences. A line must contain at least a word and its tag.
    Sentences are separated by empty lines.
    """
    sentences = []
    sentence = []
    for line in codecs.open(path, 'r', 'utf-8'):

        line = zero_digits(line.rstrip()) if zeros else line.rstrip()

        if not line:
            if len(sentence) > 0:
                sentences.append(sentence)
                sentence = []
        else: 
            word = line.split()
            assert len(word) >= 2
            sentence.append(word)
    if len(sentence) > 0:

            sentences.append(sentence)
    return sentences




def word_mapping(sentences, lower):
    """
    Create a dictionary and a mapping of words, sorted by frequency.
    """
    words = [[x[0].lower() if lower else x[0] for x in s] for s in sentences]
    words1 = [[x[1].lower() if lower else x[1] for x in s] for s in sentences]
    sum_words = words+words1
    dico = create_dico(sum_words)
    dico['<UNK>'] = 10000000

    word_to_id, id_to_word = create_mapping(dico)

    print("Found %i unique words (%i in total)" % (
        len(dico), sum(len(x) for x in words)
    ))
    return dico, word_to_id, id_to_word


def tag_mapping(sentences):
    """
    Create a dictionary and a mapping of tags, sorted by frequency.
    """
    tags = [[word[-1] for word in s] for s in sentences]
    dico = create_dico(tags)
    dico[model.START_TAG] = -1
    dico[model.STOP_TAG] = -2
    tag_to_id, id_to_tag = create_mapping(dico)
    print("Found %i unique named entity tags" % len(dico))
    return dico, tag_to_id, id_to_tag


def prepare_dataset(sentences, word_to_id, tag_to_id,  lower=True):

    def f(x): return x.lower() if lower else x
    data = []
    for s in sentences:
        str_words = [w[0] for w in s]
        str_words1 = [w[1] for w in s]
        str_words2 = [w[15] for w in s]
        str_words3 = [w[16] for w in s]

        words = [word_to_id[f(w) if f(w) in word_to_id else '<UNK>']
                 for w in str_words]
        words1 = [word_to_id[f(w) if f(w) in word_to_id else '<UNK>']
                 for w in str_words1]
        words2 = [word_to_id[f(w) if f(w) in word_to_id else '<UNK>']
                 for w in str_words2]
        words3 = [word_to_id[f(w) if f(w) in word_to_id else '<UNK>']
                 for w in str_words3]

        tags = [tag_to_id[w[-1]] for w in s]

        data.append({
            'str_words' : str_words,
            'str_words1' : str_words1,
            'str_words2' : str_words2,
            'str_words3' : str_words3,
            'words': words,
            'words1': words1,
            'words2': words2,
            'words3': words3,
            'tags': tags,
        })
    return data


def augment_with_pretrained(dictionary, ext_emb_path, words):
    """
    Augment the dictionary with words that have a pretrained embedding.
    If `words` is None, we add every word that has a pretrained embedding
    to the dictionary, otherwise, we only add the words that are given by
    `words` (typically the words in the development and test sets.)
    """
    print('Loading pretrained embeddings from %s...' % ext_emb_path)
    assert os.path.isfile(ext_emb_path)


    emb_file = open(ext_emb_path, 'r')
    lines = emb_file.readlines()
    emb_file.close()
    pretrained = set([
        line.rstrip().split()[0].strip()
        for line in lines])


    if words is None:
        for word in pretrained:
            if word not in dictionary:
                dictionary[word] = 0
    else:
        for word in words:
            if any(x in pretrained for x in [
                word,
                word.lower(),
                re.sub('\d', '#', word.lower())
            ]) and word not in dictionary:
                dictionary[word] = 0


    word_to_id, id_to_word = create_mapping(dictionary)
    return dictionary, word_to_id, id_to_word




