import os
import sys
import json
import time
import shutil
import pickle
import logging
import main
import data_helper
import numpy as np
import tensorflow as tf
from text_cnn_rnn import TextCNNRNN

logging.getLogger().setLevel(logging.INFO)

def predict_cnn_rnn(x_test, y_test, out_dir='trained_results'):
    ###################################################################
    # 		ARG : x_test/y_test (test data/label matrix)			  #
    # 			                                      				  #
    # 		RETURN : predict_labels, accuracy         				  #
    # 			    (predict label vector)             				  #
    # 			                                      				  #
    #       AT predicted_dir, there is predict_labels.txt   		  #
    #		which stores the prediction result of test file	    	  #
    # 				                                				  #
    ###################################################################



    if out_dir == '':
        trained_dir = 'trained_results'
    else :
        trained_dir = out_dir

    with tf.Graph().as_default():
        session_conf = tf.ConfigProto(allow_soft_placement=True, log_device_placement=False)
        sess = tf.Session(config=session_conf)
        with sess.as_default():
            params = json.loads(open(trained_dir + 'trained_parameters.json',encoding='utf-8').read())
            words_index = json.loads(open(trained_dir + 'words_index.json',encoding='utf-8').read())
            labels = json.loads(open(trained_dir + 'labels.json',encoding='utf-8').read())
            with open(trained_dir + 'embeddings.pickle', 'rb') as input_file:
                fetched_embedding = pickle.load(input_file)
            embedding_mat = np.array(fetched_embedding, dtype=np.float32)

            cnn_rnn2 = TextCNNRNN(
                embedding_mat=embedding_mat,
                non_static=params['non_static'],
                hidden_unit=params['hidden_unit'],
                sequence_length=len(x_test[0]),
                max_pool_size=params['max_pool_size'],
                filter_sizes=map(int, params['filter_sizes'].split(",")),
                num_filters=params['num_filters'],
                num_classes=len(labels),
                embedding_size=params['embedding_dim'],
                l2_reg_lambda=params['l2_reg_lambda']
                )

            def real_len(batches):
                return [np.ceil(np.argmin(batch + [0]) * 1.0 / params['max_pool_size']) for batch in batches]

            def predict_step(x_batch):
                feed_dict = {
                    cnn_rnn2.input_x: x_batch,
                    cnn_rnn2.dropout_keep_prob: 1.0,
                    cnn_rnn2.batch_size: len(x_batch),
                    cnn_rnn2.pad: np.zeros([len(x_batch), 1, params['embedding_dim'], 1]),
                    cnn_rnn2.real_len: real_len(x_batch),
                }
                predictions = sess.run([cnn_rnn2.predictions], feed_dict)
                return predictions

            checkpoint_file = trained_dir + 'best_model.ckpt'
            saver = tf.train.Saver(tf.global_variables())
            saver = tf.train.import_meta_graph("{}.meta".format(checkpoint_file))
            saver.restore(sess, checkpoint_file)
            logging.critical('{} has been loaded'.format(checkpoint_file))

            batches = data_helper.batch_iter(list(x_test), params['batch_size'], 1,
                                             shuffle=False)

            predictions, predict_labels = [], []
            for x_test_batch in batches:
                batch_predictions = predict_step(x_test_batch)[0]
                for batch_prediction in batch_predictions:
                    predictions.append(batch_prediction)
                    predict_labels.append(labels[batch_prediction])

            if y_test is not None:
                y_test = np.array(np.argmax(y_test, axis=1))
                accuracy = sum(np.array(predictions) == y_test) / float(len(y_test))
                logging.critical('The prediction accuracy is: {}'.format(accuracy))

            logging.critical('Prediction is complete')

    return predict_labels, accuracy
