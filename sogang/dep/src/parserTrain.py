# -*- coding: utf-8 -*-

'''
Created on 2017-05-13

@author: pymnlp
@description : 
'''
import pickle
import random
import time
import numpy as np

import DataTools as dt
import tensorflow as tf
import TransitionParser as tp
import TextCNN as mycnn
import os

from config import FLAGS

class YM_parser():
    def __init__(self,bagging_iter):
        self.train(bagging_iter)

    def test_step(self, cnn, graph, sess, x_mor, x_pos, x_child_mor, x_child_pos, x_hc, model_idx):
        feed_dict = {
            cnn.input_x_mor: x_mor,
            cnn.input_x_pos: x_pos,
            cnn.input_x_child_mor: x_child_mor,
            cnn.input_x_child_pos: x_child_pos,
            cnn.input_x_hc: x_hc,
            cnn.dropout_keep_prob: 1.0
        }
        predictions = graph.get_operation_by_name("%sth_model_scope/output/predictions"%(model_idx)).outputs[0]
        predictions = sess.run(
            [predictions],
            feed_dict=feed_dict)

        return predictions
    def train_step(self, cnn, sess, train_op, x_mor, x_pos, x_child_mor, x_child_pos, x_hc, y1_batch):
        """
        A single training step
        """
        feed_dict = {
            cnn.input_x_mor: x_mor,
            cnn.input_x_pos: x_pos,
            cnn.input_x_child_mor: x_child_mor,
            cnn.input_x_child_pos: x_child_pos,
            cnn.input_x_hc: x_hc,
            cnn.input_y: y1_batch,
            cnn.dropout_keep_prob: FLAGS.dropout_keep_prob
        }
        _ = sess.run(
            [train_op], feed_dict)

        return

    def train(self, bagging_iter):
        for model_idx in range(FLAGS.num_models):
            model_idx += 1
            start_time = time.time()
            graph = tf.Graph()
            with graph.as_default():
                session_conf = tf.ConfigProto()
                session_conf.gpu_options.allow_growth = True
                sess = tf.Session(config=session_conf)
                f_model_path = '../data/f_model/%sth_f_model/%sth_f_model.dat' % (bagging_iter, model_idx)
                f = open(f_model_path, 'r')
                model = pickle.load(f)
                f.close()
                with sess.as_default():
                    cnn = mycnn.DepCNNv6(
                        model_idx = model_idx,
                        num_classes=model.type_size,
                        vocab_size=model.mor_size + 1,
                        pos_size=model.pos_size + 1,
                        hc_size=model.hc_feature_size,
                        embedding_size=FLAGS.embedding_dim,
                        mlp_size=FLAGS.mlp_size,
                        l2_reg_lambda=FLAGS.l2_reg_lambda)

                    # Define Training procedure
                    optimizer = tf.train.AdamOptimizer(0.0001)
                    grads_and_vars = optimizer.compute_gradients(cnn.loss)
                    train_op = optimizer.apply_gradients(grads_and_vars)

                    saver = tf.train.Saver(tf.global_variables(), max_to_keep=FLAGS.num_checkpoints)

                    # Initialize all variables
                    sess.run(tf.global_variables_initializer())

                    out_path = '../data/training_data/' + str(bagging_iter) + 'th_out'
                    sample_list = dt.make_sample_list_from_input_data(
                        out_path + '/train' + str(model_idx) + '.out', model)

                    # print('데이터 로드 끝')
                    total_batch = len(sample_list) / FLAGS.batch_size
                    print('total_batch = ' + str(total_batch))
                    for ep in range(FLAGS.num_epochs):
                        # 학습 phase
                        # sample 섞기
                        random.shuffle(sample_list)
                        # batch 만큼 데이터 가져오기
                        batch_number = 0
                        tmp = 0
                        while True:
                            tmp += 1
                            sample_batch = sample_list[batch_number * FLAGS.batch_size: (batch_number + 1) * FLAGS.batch_size]
                            batch_number += 1

                            x_mor, x_pos, x_left_mor, x_left_pos, x_right_mor, x_right_pos, \
                            x_position_mark_batch, x_child_mor, x_child_pos, x_hc_batch, y_batch\
                                = dt.convert_to_input_vector(sample_batch, model)

                            if sample_batch == []:
                                if batch_number * FLAGS.batch_size > len(sample_list):
                                    break
                                continue

                            self.train_step(cnn, sess, train_op, x_mor, x_pos, x_child_mor, x_child_pos, x_hc_batch, y_batch)
                            if (batch_number % (total_batch / 50)) == 0:
                                print('.'),
                            if batch_number * FLAGS.batch_size > len(sample_list):
                                break

                        # 테스트 phase
                        total_arc = 0
                        correct_arc = 0
                        correct_sentence = 0
                        total_sentence = 0
                        correct_arc_with_tag = 0
                        correct_sentence_with_tag = 0

                        cr_test = dt.CorpusReader()
                        cr_test.set_file('../data/raw_data/valid_data/sejong_test_edit_VV.txt')
                        parser = tp.TransitionParser(model, 1)
                        while True:
                            data = cr_test.get_next(1)

                            if data == []:
                                break
                            if data[0].raw_sentence is None:
                                continue
                            parser.initialize(data)
                            while parser.is_final_state() is False:
                                left_mor, left_pos, right_mor, right_pos, child_mor, child_pos, hc = parser.make_input_vector(data, mode = 'train')
                                x_mor = left_mor + right_mor
                                x_pos = left_pos + right_pos
                                hc = model.convert_to_zero_one(hc, model.hc_feature_size, mode='train')
                                next_action = self.test_step(cnn, graph,sess, np.array([x_mor]), np.array([x_pos]), np.array([child_mor]),
                                                                      np.array([child_pos]), np.array([hc]), model_idx)
                                next_action = next_action[0][0]
                                parser.run_action(next_action,  model, mode ='train')

                            # 성능 평가
                            predicts = parser.get_result('train')
                            golds = data[0].correct_dep_list

                            sentence_flag = True
                            sentence_with_tag_flag = True
                            for i in range(len(predicts)):
                                if predicts[i].head == golds[i].head:
                                    correct_arc += 1
                                    if predicts[i].type == golds[i].type:
                                        correct_arc_with_tag += 1
                                    else:
                                        sentence_with_tag_flag = False
                                else:
                                    sentence_flag = False
                                    sentence_with_tag_flag = False
                                total_arc += 1
                            if sentence_flag is True:
                                correct_sentence += 1
                            if sentence_with_tag_flag is True:
                                correct_sentence_with_tag += 1
                            total_sentence += 1

                            if (total_sentence % 300) == 0:
                                print('.'),

                        cr_test.close_file()
                        with open('../data/log/' +str(bagging_iter) + 'th_bagging_model.txt', 'a') as f:
                            if ep is 0:
                                print('%sth_total_arc = %s %sth_total_sentence = %s' % (model_idx, total_arc, model_idx, total_sentence))
                                f.write('%sth_total_arc = %s %sth_total_sentence = %s\n' %  (model_idx, total_arc, model_idx, total_sentence))

                            if not os.path.isdir('../data/ckpt/%sth_ckpt' % (bagging_iter)):
                                os.mkdir('../data/ckpt/%sth_ckpt' % (bagging_iter))

                            if (ep % FLAGS.num_checkpoints) == 0:
                                path = saver.save(sess, '../data/ckpt/%sth_ckpt/%sth_%s' % (bagging_iter, model_idx, ep))
                                f.write('\n')
                                f.write("Saved model checkpoint to {}\n".format(path))
                                print("Saved model checkpoint to {}\n".format(path))

                            f.write(str(model_idx)+'th model result : ' + 'epoch = ' + str(ep+1) + ', acc = ' + str(correct_arc / float(total_arc))
                                  + ', sen_acc = ' + str(correct_sentence / float(total_sentence))
                                  + ', acc_with_tag = ' + str(correct_arc_with_tag / float(total_arc))
                                  + ', sen_acc_with_tag = ' + str(correct_sentence_with_tag / float(total_sentence))
                                  )
                            print(str(model_idx)+'th model result : ' ,'epoch = ' + str(ep+1) + ', acc = ' + str(correct_arc / float(total_arc))
                                  + ', sen_acc = ' + str(correct_sentence / float(total_sentence))
                                  + ', acc_with_tag = ' + str(correct_arc_with_tag / float(total_arc))
                                  + ', sen_acc_with_tag = ' + str(correct_sentence_with_tag / float(total_sentence))
                                  )

                print (str(bagging_iter) + '_bagging ',str(model_idx)+'th trainning time : ', str(time.time() - start_time))


