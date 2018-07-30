# -*- coding: utf-8 -*-

'''
Created on 2017-05-13

@author: pymnlp
@description :
'''
import pickle
import os

import DataTools as dt
import TransitionParser as tp
import FeatureModel as fm
from config import FLAGS

def make_corpus_and_model(model_idx = 0, bagging_iter = None, input_path = None):

    if input_path == 'default':
        input_path = '../data/training_data/%sth_in' % (bagging_iter)

    out_path = '../data/training_data/%sth_out' %(bagging_iter)
    if not os.path.isdir(out_path):
        os.mkdir(out_path)

    model = fm.FeatureModel()
    parser = tp.TransitionParser(model, 1)
    cr = dt.CorpusReader()
    cr.set_file(input_path + '/train_' + str(model_idx) + '.txt',
                out_path + '/train' + str(model_idx) + '.out')

    num_data = 0
    while True:
        data = cr.get_next(1)
        if data == [] or data == None or data[0] == [] or data[0].raw_sentence is None:
            break

        total_sample = parser.make_gold_corpus(data)
        cr.write_out_data(total_sample)
        num_data += 1

    print(str(model_idx) + '_th model, '+ str(num_data) + '문장')
    cr.close_file()
    return model


def save_model(bagging_iter = None, input_path = None):
    print ('Welcome to ' +str(bagging_iter)+ 'th save_model')
    dir_path = '../data/f_model/'+str(bagging_iter)+'th_f_model'
    if not os.path.isdir(dir_path):
        os.mkdir(dir_path)

    for model_idx in range(FLAGS.num_models):
        model_idx += 1
        f_model_path = '../data/f_model/%sth_f_model/%sth_f_model.dat' % (bagging_iter, model_idx)
        f_model = make_corpus_and_model(model_idx, bagging_iter, input_path)
        f = open(f_model_path, 'w')
        pickle.dump(f_model, f)
        f.close()


