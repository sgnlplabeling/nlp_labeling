import numpy as np
import tensorflow as tf
from cnn_attention import cnn_attention
class TextCNNRNN(object):
    def __init__(self,embedding_mat, embedding_pre, non_static, hidden_unit, sequence_length, max_pool_size,
                 num_classes, embedding_size, filter_sizes, num_filters, attention_size = 64, l2_reg_lambda=0.0):

        self.input_x = tf.placeholder(tf.int32, [None, sequence_length], name='input_x')
        self.input_y = tf.placeholder(tf.float32, [None, num_classes], name='input_y')
        self.input_pre_y = tf.placeholder(tf.int32, [None, 1], name='input_pre_y')
        self.dropout_keep_prob = tf.placeholder(tf.float32, name='dropout_keep_prob')
        self.batch_size = tf.placeholder(tf.int32, [])
        self.pad = tf.placeholder(tf.float32, [None, 1, embedding_size, 1], name='pad')
        self.real_len = tf.placeholder(tf.int32, [None], name='real_len')

        l2_loss = tf.constant(0.0)

        with tf.device('/cpu:0'), tf.name_scope('embedding'):
            if not non_static:
                self.Word = tf.constant(embedding_mat, name='W')
            else:
                self.Word = tf.get_variable(initializer=embedding_mat, name='W',trainable=True)
            self.embedded_chars = tf.nn.embedding_lookup(self.Word, self.input_x)

        with tf.device('/cpu:0'), tf.name_scope('embedding_pre_y'):
            if not non_static:
                self.Pre = tf.constant(embedding_pre, name='P')
            else:
                self.Pre = tf.get_variable(initializer=embedding_pre, name='P', trainable=True)
            self.embedded_pre_y = tf.nn.embedding_lookup(self.Pre, self.input_pre_y)
        with tf.name_scope('Attention_layer'):
            attention_output = cnn_attention(self.embedded_chars, attention_size, self.embedded_pre_y, time_major=False,
                                                 return_alphas=False)

        emb = tf.expand_dims(attention_output, -1)
        pooled_concat = []
        reduced = np.int32(np.ceil((sequence_length) * 1.0 / max_pool_size))

        for i, filter_size in enumerate(filter_sizes):
            with tf.name_scope('conv-maxpool-%s' % filter_size):
                # Zero paddings so that the convolution output have dimension batch x sequence_length x emb_size x channel
                num_prio = (filter_size - 1) // 2
                num_post = (filter_size - 1) - num_prio
                pad_prio = tf.concat([self.pad] * num_prio, 1)
                pad_post = tf.concat([self.pad] * num_post, 1)
                emb_pad = tf.concat([pad_prio, emb, pad_post], 1)
                filter_shape = [filter_size, embedding_size, 1, num_filters]
                W = tf.Variable(tf.truncated_normal(filter_shape, stddev=0.1), name='W')
                b = tf.Variable(tf.constant(0.1, shape=[num_filters]), name='b')
                conv = tf.nn.conv2d(emb_pad, W, strides=[1, 1, 1, 1], padding='VALID', name='conv')

                h = tf.nn.relu(tf.nn.bias_add(conv, b), name='relu')

                # Maxpooling over the outputs
                pooled = tf.nn.max_pool(h, ksize=[1, max_pool_size, 1, 1], strides=[1, max_pool_size, 1, 1],
                                        padding='SAME', name='pool')
                pooled = tf.reshape(pooled, [-1, reduced, num_filters])
                pooled_concat.append(pooled)

        pooled_concat = tf.concat(pooled_concat, 2)
        pooled_concat = tf.nn.dropout(pooled_concat, self.dropout_keep_prob)
        #lstm_cell = tf.nn.rnn_cell.LSTMCell(num_units=hidden_unit)
        lstm_cell = tf.nn.rnn_cell.GRUCell(num_units=hidden_unit)

        lstm_cell = tf.nn.rnn_cell.DropoutWrapper(lstm_cell, output_keep_prob=self.dropout_keep_prob)

        self._initial_state = lstm_cell.zero_state(self.batch_size, tf.float32)
        inputs = [tf.squeeze(input_, [1]) for input_ in
                  tf.split(pooled_concat, num_or_size_splits=int(reduced), axis=1)]

        outputs, state = tf.contrib.rnn.static_rnn(lstm_cell, inputs, initial_state=self._initial_state,sequence_length=self.real_len)

        output = outputs[0]
        with tf.variable_scope('Output'):
            tf.get_variable_scope().reuse_variables()
            one = tf.ones([1, hidden_unit], tf.float32)
            for i in range(0, len(outputs)):
                ind = self.real_len < (i + 1)
                ind = tf.to_float(ind)
                ind = tf.expand_dims(ind, -1)
                mat = tf.matmul(ind, one)
                output = tf.add(tf.multiply(output, mat), tf.multiply(outputs[i], 1.0 - mat))

        with tf.name_scope('output'):
            self.W = tf.Variable(tf.truncated_normal([hidden_unit, num_classes], stddev=0.1), name='W')
            b = tf.Variable(tf.constant(0.1, shape=[num_classes]), name='b')
            l2_loss += tf.nn.l2_loss(self.W)
            l2_loss += tf.nn.l2_loss(b)
            self.scores_ = tf.nn.xw_plus_b(output, self.W, b, name='scores')
            self.scores = tf.nn.softmax(self.scores_, name='scores')
            self.predictions = tf.argmax(self.scores, 1, name='predictions')

        with tf.name_scope('loss'):
            losses = tf.nn.softmax_cross_entropy_with_logits_v2(labels=self.input_y,
                                                             logits=self.scores_)  # only named arguments accepted
            self.loss = tf.reduce_mean(losses) + l2_reg_lambda * l2_loss

        with tf.name_scope('accuracy'):
            correct_predictions = tf.equal(self.predictions, tf.argmax(self.input_y, 1))
            self.accuracy = tf.reduce_mean(tf.cast(correct_predictions, "float"), name='accuracy')

        with tf.name_scope('num_correct'):
            correct = tf.equal(self.predictions, tf.argmax(self.input_y, 1))
            self.num_correct = tf.reduce_sum(tf.cast(correct, 'float'))