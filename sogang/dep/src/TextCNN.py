# -*- coding: utf-8 -*-

'''
Created on 2017-04-21

@author: pymnlp
@description :
'''

import tensorflow as tf
import numpy as np

# 어절내 LSTM
class DepCNNv6(object):
    """
    A CNN for text classification.
    Uses an embedding layer, followed by a convolutional, max-pooling and softmax layer.
    """
    def __init__(
            self, model_idx, num_classes, vocab_size, pos_size, hc_size,
            embedding_size, mlp_size,l2_reg_lambda=0.0, ):

        with tf.name_scope(str(model_idx)+"th_model_scope"):
        # 윈도우 3개, 어절내 앞2개 뒤2개, stack, queue
            self.input_x_mor = tf.placeholder(tf.int32, [None, 3 * 4 * 2], name='input_x_mor')
            self.input_x_pos = tf.placeholder(tf.int32, [None, 3 * 4 * 2], name='input_x_pos')

            #  history 입력
            #  stack의 top -1 -2, 어절내 앞2개 뒤2개
            self.input_x_child_mor = tf.placeholder(tf.int32, [None, 3 * 4], name='input_x_child_mor')
            self.input_x_child_pos = tf.placeholder(tf.int32, [None, 3 * 4], name='input_x_child_pos')

            self.input_x_hc = tf.placeholder(tf.float32, [None, hc_size], name='input_x_hc')

            self.input_y = tf.placeholder(tf.float32, [None, num_classes], name="input_y")
            self.dropout_keep_prob = tf.placeholder(tf.float32, name="dropout_keep_prob")

            # Keeping track of l2 regularization loss (optional)


            # Embedding layer
            # with tf.device('/gpu:0'), tf.name_scope("embedding"):
            l2_loss = tf.constant(0.0)

            self.W_MOR = tf.Variable(
                tf.random_uniform([vocab_size, embedding_size], -1.0, 1.0),
                name="W_MOR")
            self.embedded_chars_mor = tf.nn.embedding_lookup(self.W_MOR, self.input_x_mor)

            self.W_POS = tf.Variable(
                tf.random_uniform([pos_size, embedding_size], -1.0, 1.0),
                name="W_POS")
            self.embedded_chars_pos = tf.nn.embedding_lookup(self.W_POS, self.input_x_pos)

            self.embedded_chars_child_mor = tf.nn.embedding_lookup(self.W_MOR, self.input_x_child_mor)
            self.embedded_chars_child_pos = tf.nn.embedding_lookup(self.W_POS, self.input_x_child_pos)

            self.mor_flat = tf.reshape(self.embedded_chars_mor, [-1, embedding_size * 3 * 4 * 2])
            self.pos_flat = tf.reshape(self.embedded_chars_pos, [-1, embedding_size * 3 * 4 * 2])

            self.child_mor_flat = tf.reshape(self.embedded_chars_child_mor, [-1, embedding_size * 3 * 4])
            self.child_pos_flat = tf.reshape(self.embedded_chars_child_pos, [-1, embedding_size * 3 * 4])

            self.h_flat = tf.concat([self.mor_flat, self.pos_flat, self.child_mor_flat, self.child_pos_flat], 1)

            # Add dropout
            with tf.name_scope("dropout"):
                self._h_drop = tf.nn.dropout(self.h_flat, self.dropout_keep_prob)
                self.h_drop = tf.concat([self._h_drop, self.input_x_hc], 1)

            # Final (unnormalized) scores and predictions
            with tf.name_scope("output"):

                W1 = tf.get_variable("W1", shape=[embedding_size * 3 * 4 * 2 * 2 + embedding_size * 3*4*2+hc_size, mlp_size],
                                     initializer=tf.contrib.layers.xavier_initializer())
                b1 = tf.Variable(tf.constant(0.1, shape=[mlp_size]), name="b1")
                L1 = tf.nn.relu(tf.nn.xw_plus_b(self.h_drop, W1, b1))
                l2_loss += tf.nn.l2_loss(W1)
                l2_loss += tf.nn.l2_loss(b1)
                L1_drop = tf.nn.dropout(L1, self.dropout_keep_prob)
                Wout = tf.get_variable("Wout", shape=[mlp_size, num_classes],
                                     initializer=tf.contrib.layers.xavier_initializer())
                bout = tf.Variable(tf.constant(0.1, shape=[num_classes]), name="bout")
                l2_loss += tf.nn.l2_loss(Wout)
                l2_loss += tf.nn.l2_loss(bout)

                #self.scores = tf.nn.softmax(tf.nn.xw_plus_b(L2_drop, Wout, bout))
                self.scores = tf.nn.relu(tf.nn.xw_plus_b(L1_drop, Wout, bout), name="scores")
                #self.scores = tf.nn.xw_plus_b(L2_drop, Wout, bout, name="scores")
                self.predictions = tf.argmax(self.scores, 1, name="predictions")

            # CalculateMean cross-entropy loss
            with tf.name_scope("loss"):
                losses = tf.nn.softmax_cross_entropy_with_logits(logits=self.scores, labels=self.input_y)
                self.loss = tf.reduce_mean(losses) + l2_reg_lambda * l2_loss

            # Accuracy
            with tf.name_scope("accuracy"):
                correct_predictions = tf.equal(self.predictions, tf.argmax(self.input_y, 1))
                self.accuracy = tf.reduce_mean(tf.cast(correct_predictions, "float"), name="accuracy1")


