# -*- coding: utf-8 -*-

'''
Created on 2017-05-13

@author: pymnlp
@description :
'''
import pickle

import numpy as np

import DataTools as dt
import tensorflow as tf
import TransitionParser as tp
import threading
import time
import os

from config import FLAGS
import TextCNN as mycnn


class YM_PARSER(threading.Thread):

    def __init__(self, sess, model_idx, pos,file_idx, bagging_iter, input_path, mode = None, output_path = None):
        threading.Thread.__init__(self)
        self.sess = sess
        self.model_idx = model_idx
        self.pos = pos
        self.file_idx = file_idx
        self.bagging_iter = bagging_iter
        self.mode = mode
        self.input_path = input_path
        self.output_path = output_path

        if mode == 'g_predict' and self.input_path == 'default':
            self.input_path = '../data/input_data/test_data'


    def run(self):
        self.graph = tf.Graph()
        with self.graph.as_default():
            f = open('../data/f_model/%sth_f_model/%sth_f_model.dat' % (self.bagging_iter, self.model_idx),'r')
            model = pickle.load(f)
            f.close()

            self.cnn = mycnn.DepCNNv6(
                model_idx=self.model_idx,
                num_classes=model.type_size,
                vocab_size=model.mor_size + 1,
                pos_size=model.pos_size + 1,
                hc_size=model.hc_feature_size,
                embedding_size=FLAGS.embedding_dim,
                mlp_size=FLAGS.mlp_size,
                l2_reg_lambda=FLAGS.l2_reg_lambda)

            checkpoint_file = '../data/ckpt/%sth_ckpt/%sth_%s' % (self.bagging_iter, self.model_idx, int(FLAGS.num_epochs)-1)
            cr_test = dt.CorpusReader()
            if self.bagging_iter == str(0) and self.mode != 'g_predict':
                cr_test.set_file((self.input_path + '/test_%s.txt') % (self.file_idx))
            elif self.mode == 'g_predict' :
                cr_test.set_file(self.input_path)

            if self.input_path == 'default':
                self.input_path = '../data/test_data/%sth_test_data'
                cr_test.set_file((self.input_path + '/test_%s.txt') % (self.bagging_iter, self.file_idx))
            elif self.input_path != 'default' and self.mode != 'g_predict':
                self.input_path = self.input_path
                cr_test.set_file((self.input_path + '/test_%s.txt') % (self.file_idx))

            session_conf = tf.ConfigProto()
            session_conf.gpu_options.allow_growth = True
            self.sess = tf.Session(config=session_conf)
            saver = tf.train.Saver()
            saver.restore(self.sess, checkpoint_file)

            last_flag = False
            data_dix = 0

            parser = tp.TransitionParser(model, FLAGS.batch_size)
            results = []
            while True:
                data = cr_test.get_next()
                data_dix += 1
                parsing_trees = [0] * len(data)

                if data == []:
                    last_flag == True
                    self.file_write(parsing_trees)
                    parsing_trees = [0] * len(data)
                    break
                if data[0].raw_sentence is None:
                    last_flag == True
                    self.file_write(parsing_trees)
                    parsing_trees = [0] * len(data)
                    break
                if data == None:
                    last_flag == True
                    self.file_write(parsing_trees)
                    parsing_trees = [0] * len(data)
                    break

                for batch_idx in range(len(data)):
                    parsing_trees[batch_idx] = {'raw_sentence': data[batch_idx].raw_sentence, 'tree': [], 'eojeol_list': data[batch_idx].eojeol_list}

                parser.initialize(data)

                tmp_idx = 0
                while parser.is_final_state() is False:
                    features, hc = parser.make_input_vector(data)
                    hc = model.convert_to_zero_one(hc, model.hc_feature_size)
                    next_action = self.test_step(features, hc)
                    next_action = next_action[0]
                    parser.run_action(next_action, model)
                    tmp_idx += 1

                predicts = parser.get_result('test')

                for batch_idx, predict in enumerate(predicts):
                    parsing_trees[batch_idx]['tree'] = (predict)

                results.append(parsing_trees)
                parsing_trees = [0] * len(data)

                if data_dix % 20 == 1:
                    print (str(self.file_idx) + 'th_file , ' + str(self.model_idx) + 'th_model index, ' + str(data_dix)+'_th batch')
                    self.file_write(results)
                    results = []

            self.file_write(results)

    def test_step(self, features, hc):

        features = np.stack(features, axis = 0)

        y = [[np.array(f) for f in np.array(feature)] for feature in features]
        y = np.array(y)
        x_mor = np.array(y[:, 0]).tolist()
        x_pos = np.array(y[:, 1]).tolist()
        x_child_mor = np.array(y[:, 2]).tolist()
        x_child_pos = np.array(y[:, 3]).tolist()

        hc = np.array(hc)

        feed_dict = {
            self.cnn.input_x_mor: x_mor,
            self.cnn.input_x_pos: x_pos,
            self.cnn.input_x_child_mor: x_child_mor,
            self.cnn.input_x_child_pos: x_child_pos,
            self.cnn.input_x_hc: hc,
            self.cnn.dropout_keep_prob: 1.0
        }

        predictions = self.graph.get_operation_by_name(str(self.model_idx)+"th_model_scope/output/predictions").outputs[0]
        predictions = self.sess.run(
            [predictions],
            feed_dict=feed_dict)

        return predictions

    def file_write(self, results):
        if self.mode == 'g_predict' :
            before_voting_path = '../data/tmp_data/%s_g_tmp_data' % (self.bagging_iter)
            if not os.path.isdir(before_voting_path):
                os.mkdir(before_voting_path)

            before_voting_path = '../data/tmp_data/%s_g_tmp_data/before_voting' % (self.bagging_iter)
            if not os.path.isdir(before_voting_path):
                time.sleep(1)
                if not os.path.isdir(before_voting_path):
                    os.mkdir(before_voting_path)

        else:
            before_voting_path = '../data/tmp_data/%sth_tmp_data' % (self.bagging_iter)
            if not os.path.isdir(before_voting_path):
                os.mkdir(before_voting_path)

            before_voting_path = '../data/tmp_data/%sth_tmp_data/before_voting' % (self.bagging_iter)
            if not os.path.isdir(before_voting_path):
                os.mkdir(before_voting_path)

        with open(before_voting_path+'/'+str(self.model_idx)+'th_model_result_' + str(
                self.file_idx) + 'th_file.txt', 'a') as f:

            for parsing_trees in results:
                for trees in parsing_trees:

                    if trees['raw_sentence'] == None:
                        continue

                    f.write(trees['raw_sentence'])
                    eojeol_list = trees['eojeol_list']
                    for tree_i, tree in enumerate(trees['tree']):
                        if tree == None:
                            break

                        token = ''
                        eojeols = eojeol_list[tree_i].morpheme_list
                        for e_i, t in enumerate(eojeols):
                            token += t.lex + '/' + t.pos + '+'

                        f.write(str(tree.index+1) + '\t' + str(tree.head+1) + '\t' + str(tree.type) + '\t' + token + '\n')
                    f.write('\n')



