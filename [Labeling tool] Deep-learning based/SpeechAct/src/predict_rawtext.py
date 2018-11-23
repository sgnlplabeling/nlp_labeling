import os
import sys
import json
import getopt
import time
import shutil
import pickle
import logging
import data_helper
import numpy as np
import tensorflow as tf
from text_cnn_rnn import TextCNNRNN

logging.getLogger().setLevel(logging.INFO)

def load_trained_params(trained_dir):
	#load trained params at the trained_dir
	params = json.loads(open(trained_dir + 'trained_parameters.json',encoding='utf-8').read())
	words_index = json.loads(open(trained_dir + 'words_index.json',encoding='utf-8').read())
	labels = json.loads(open(trained_dir + 'labels.json',encoding='utf-8').read())
	with open(trained_dir + 'embeddings.pickle', 'rb') as input_file:
		fetched_embedding = pickle.load(input_file)
	embedding_mat = np.array(fetched_embedding, dtype=np.float32)

	return params, words_index,  labels, embedding_mat

def load_test_data(in_file):

	data = list(open(in_file, 'r', encoding='utf-8').readlines())
	data_ = np.array([s.strip() for s in data])
	data = [s.split('|') for s in data_]

	return data_, data, None

def map_word_to_index(examples, words_index):
	x_ = []
	for example in examples:
		temp = []
		for word in example:
			if word in words_index:
				temp.append(words_index[word])
			else:
				temp.append(0)
		x_.append(temp)
	return x_

def predict_raw_data(argv):
	###################################################################
	#       Make sure to enter the trained_dir you want to load       #
	# 				                                				  #
	#       AT predicted_dir, there is predict_labels.txt   		  #
	#		which store the prediction result of test file			  #
	# 				                                				  #
	###################################################################

	in_file = ''
	out_file = ''

	try:
		opts, args = getopt.getopt(argv, "h:t:i:o:", ["trained_dir=","in_filepath=", "out_filepath="])
	except getopt.GetoptError:
		print("python main.py -i <in_filepath> -o <out_filepath> -t <trained_dir>")
		sys.exit(2)

	trained_dir = './trained_results/'

	for opt, arg in opts:
		if opt == '-h':
			print("python main.py -i <in_filepath> -o <out_filepath>")
			sys.exit()
		elif opt in ("-i", "--in_filepath"):
			in_file = arg
		elif opt in ("-o", "--out_filepath"):
			out_file = arg
		elif opt in ("-t", "--trained_dir"):
			trained_dir = arg

	params, words_index, labels, embedding_mat = load_trained_params(trained_dir)
	original_x, x_, y_ = load_test_data(in_file)

	x_ = data_helper.pad_sentences(x_, forced_sequence_length= params['sequence_length'])
	x_ = map_word_to_index(x_, words_index)

	x_test, y_test = np.asarray(x_), None
	if y_ is not None:
		y_test = np.asarray(y_)

	with tf.Graph().as_default():
		session_conf = tf.ConfigProto(allow_soft_placement=True, log_device_placement=False)
		sess = tf.Session(config=session_conf)

		with sess.as_default():
			cnn_rnn = TextCNNRNN(
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
					cnn_rnn.input_x: x_batch,
					cnn_rnn.dropout_keep_prob: 1.0,
					cnn_rnn.batch_size: len(x_batch),
					cnn_rnn.pad: np.zeros([len(x_batch), 1, params['embedding_dim'], 1]),
					cnn_rnn.real_len: real_len(x_batch),
				}
				predictions, scores = sess.run([cnn_rnn.predictions, cnn_rnn.scores], feed_dict)
				return predictions, scores

			checkpoint_file = trained_dir + 'best_model.ckpt'
			saver = tf.train.Saver(tf.global_variables())
			saver = tf.train.import_meta_graph("{}.meta".format(checkpoint_file))
			saver.restore(sess, checkpoint_file)
			logging.critical('{} has been loaded'.format(checkpoint_file))

			batches = data_helper.batch_iter(list(x_test), params['batch_size'], 1,
											 shuffle=False)

			predictions, predict_labels, predict_probs = [], [], []
			for x_test_batch in batches:
				batch_predictions = predict_step(x_test_batch)[0]
				batch_prop_preds = predict_step(x_test_batch)[1]

				for  batch_prediction, batch_prop_pred in zip( batch_predictions, batch_prop_preds):
					predictions.append(batch_prediction)
					predict_labels.append(labels[batch_prediction])
					predict_probs.append(batch_prop_pred[batch_prediction])

			with open(out_file, "w",encoding='utf-8') as f:
				for original_x_, predict_label, predict_prob in zip(original_x, predict_labels, predict_probs):
					print_prob = round(predict_prob*100, 2)
					f.write(str(original_x_)+'\t'+str(predict_label)+'\t'+str(print_prob)+'\n')

			if y_test is not None:
				y_test = np.array(np.argmax(y_test, axis=1))
				accuracy = sum(np.array(predictions) == y_test) / float(len(y_test))
				logging.critical('The prediction accuracy is: {}'.format(accuracy))

			logging.critical('Prediction is complete')

if __name__ == '__main__':
	predict_raw_data(sys.argv[1:])
