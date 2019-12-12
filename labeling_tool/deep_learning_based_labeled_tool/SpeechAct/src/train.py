import os
import json
import shutil
import pickle
import logging
import data_helper
import main
import numpy as np
import tensorflow as tf
from text_cnn_rnn import TextCNNRNN

logging.getLogger().setLevel(logging.INFO)
os.environ["CUDA_DEVICE_ORDER"] = "PCI_BUS_ID"
os.environ["CUDA_VISIBLE_DEVICES"] = "1"

def train_cnn_rnn(embedding_mat, embedding_pre, x_train, x_dev, y_train, y_dev, pre_y_train, pre_y_dev, labels, vocabulary, out_dir = './trained_results/'):

    if out_dir == '':
        trained_dir = './trained_results/'
    else :
        trained_dir = out_dir
    params = {
            "batch_size": 128,
            "dropout_keep_prob": 0.5,
            "embedding_dim": 64,
            "evaluate_every": 500,
            "filter_sizes": "3,4,5",
            "hidden_unit": 64,
            "l2_reg_lambda": 0.0,
            "max_pool_size": 4,
            "non_static": True,
            "num_epochs": 100,
            "num_filters": 32,
            "attention_size" : 66
        }

    graph = tf.Graph()
    with graph.as_default():
        session_conf = tf.ConfigProto(allow_soft_placement=True, log_device_placement=False)
        sess = tf.Session(config=session_conf)
        with sess.as_default():

            cnn_rnn = TextCNNRNN(
                embedding_mat=embedding_mat,
                embedding_pre=embedding_pre,
                sequence_length=x_train.shape[1],
                num_classes=y_train.shape[1],
                non_static=params['non_static'],
                hidden_unit=params['hidden_unit'],
                max_pool_size=params['max_pool_size'],
                filter_sizes=map(int, params['filter_sizes'].split(",")),
                num_filters=params['num_filters'],
                embedding_size=params['embedding_dim'],
                l2_reg_lambda=params['l2_reg_lambda'])

            global_step = tf.Variable(0, name='global_step', trainable=False)
            optimizer = tf.train.RMSPropOptimizer(1e-3, decay=0.9)

            grads_and_vars = optimizer.compute_gradients(cnn_rnn.loss)
            train_op = optimizer.apply_gradients(grads_and_vars, global_step=global_step)

            def real_len(batches):
                return [np.ceil(np.argmin(batch + [0]) * 1.0 / params['max_pool_size']) for batch in batches]

            def train_step(x_batch, y_batch, pre_y_batch):

                feed_dict = {
                    cnn_rnn.input_x: x_batch,
                    cnn_rnn.input_y: y_batch,
                    cnn_rnn.input_pre_y : pre_y_batch,
                    cnn_rnn.dropout_keep_prob: params['dropout_keep_prob'],
                    cnn_rnn.batch_size: len(x_batch),
                    cnn_rnn.pad: np.zeros([len(x_batch), 1, params['embedding_dim'], 1]),
                    cnn_rnn.real_len: real_len(x_batch),
                }
                _, step, loss, accuracy, embedding_mat = sess.run(
                    [train_op, global_step, cnn_rnn.loss, cnn_rnn.accuracy, cnn_rnn.Word],
                    feed_dict)

                return embedding_mat

            def dev_step(x_batch, y_batch, pre_y_batch):
                feed_dict = {
                    cnn_rnn.input_x: x_batch,
                    cnn_rnn.input_y: y_batch,
                    cnn_rnn.input_pre_y : pre_y_batch,
                    cnn_rnn.dropout_keep_prob: 1.0,
                    cnn_rnn.batch_size: len(x_batch),
                    cnn_rnn.pad: np.zeros([len(x_batch), 1, params['embedding_dim'], 1]),
                    cnn_rnn.real_len: real_len(x_batch),
                }
                step, loss, accuracy, num_correct, predictions = sess.run(
                    [global_step, cnn_rnn.loss, cnn_rnn.accuracy, cnn_rnn.num_correct, cnn_rnn.predictions], feed_dict)
                return accuracy, loss, num_correct, predictions

            saver = tf.train.Saver()
            sess.run(tf.global_variables_initializer())

            # Training starts here
            train_batches = data_helper.batch_iter(list(zip(x_train, y_train, pre_y_train)),
                                                   params['batch_size'], params['num_epochs'])
            best_accuracy, best_at_step = 0, 0

            # Train the model with x_train and y_train
            for train_batch in train_batches:
                x_train_batch, y_train_batch, pre_y_train_batch = zip(*train_batch)
                embedding_mat = train_step(x_train_batch, y_train_batch, pre_y_train_batch)
                current_step = tf.train.global_step(sess, global_step)

                # Evaluate the model with x_dev and y_dev
                if current_step % params['evaluate_every'] == 0:
                    dev_batches = data_helper.batch_iter(list(zip(x_dev, y_dev, pre_y_dev)),
                                                         params['batch_size'], 1)

                    total_dev_correct = 0
                    for dev_batch in dev_batches:
                        x_dev_batch, y_dev_batch, pre_y_dev_batch = zip(*dev_batch)
                        acc, loss, num_dev_correct, predictions = dev_step(x_dev_batch, y_dev_batch, pre_y_dev_batch)
                        total_dev_correct += num_dev_correct
                    accuracy = float(total_dev_correct) / len(y_dev)
                    logging.info('Accuracy on dev set: {}'.format(accuracy))

                    if accuracy >= best_accuracy:
                        best_accuracy, best_at_step = accuracy, current_step
                        logging.critical('Best accuracy {} at step {}'.format(best_accuracy, best_at_step))
            logging.critical('Training is complete, testing the best model on x_test and y_test')

            # Save the model files to out_dir. predict.py needs trained model files.
            saver.save(sess, trained_dir + "best_model.ckpt")

    with open(trained_dir + 'words_index.json', 'w',encoding='utf-8') as outfile:
        json.dump(vocabulary, outfile, indent=4, ensure_ascii=False)

    with open(trained_dir + 'embedding_mat.pickle', 'wb') as outfile:
        pickle.dump(embedding_mat, outfile, pickle.HIGHEST_PROTOCOL)
    with open(trained_dir + 'embedding_pre.pickle', 'wb') as outfile:
        pickle.dump(embedding_pre, outfile, pickle.HIGHEST_PROTOCOL)

    with open(trained_dir + 'labels.json', 'w', encoding='utf-8') as outfile:
        json.dump(labels, outfile, indent=4, ensure_ascii=False)

    params['sequence_length'] = x_train.shape[1]
    with open(trained_dir + 'trained_parameters.json', 'w', encoding='utf-8') as outfile:
        json.dump(params, outfile, indent=4, sort_keys=True, ensure_ascii=False)

