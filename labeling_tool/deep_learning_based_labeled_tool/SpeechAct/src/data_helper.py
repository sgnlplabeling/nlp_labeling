import sys
import json
import pickle
import logging
import numpy as np
from collections import Counter
import itertools
import pickle

logging.getLogger().setLevel(logging.INFO)

def load_embeddings(vocabulary):

	word_size, emb_dim, word, embedding = load_pretrained_embeddings()

	word_embeddings = {}
	embedding_mat = []
	del_voc = []

	for voca in vocabulary:
		if voca in word:
			word_embeddings[voca] = np.array(embedding[word.index(voca)])
		elif voca == '<PAD>':
			word_embeddings[voca] = np.random.uniform(-0.25, 0.25, emb_dim)
		elif len(del_voc)>221:
			word_embeddings[voca] = np.random.uniform(-0.25, 0.25, emb_dim)
		else:
			del_voc.append(voca)
			if '<UNK>' not in word_embeddings:
				word_embeddings['<UNK>'] = np.random.uniform(-0.25, 0.25, emb_dim)
	for voca in del_voc:
		del vocabulary[voca]
	vocabulary['<UNK>'] = len(vocabulary)
	new_vocabulary = {}
	cnt = 0
	for word, index in sorted(vocabulary.items(), key=lambda x: x[1]):
		new_vocabulary[word] = cnt
		if word in word_embeddings:
			embedding_mat.append(np.array(word_embeddings[word]))
		cnt += 1
	embedding_mat = np.array(embedding_mat, dtype=np.float32)

	return new_vocabulary, embedding_mat

def load_pretrained_embeddings():
	data = []
	error_voc = 0
	# load word embedding
	with open('./word_Embeddings_size64.pkl', 'rb') as f:
		while True:
			try:
				line = pickle.load(f)
				data.append(line.split('\n')[0])

			except EOFError:
				break
	voca_size, emb_dim = data[0].split()
	voca_size, emb_dim = int(voca_size), int(emb_dim)

	word = []
	embedding = []
	for i in range(1, len(data)):
		temp_embedding = []
		temp = data[i].split()

		if len(temp) != 65:
			error_voc += 1
			continue

		for i in range(0, emb_dim):
			temp_embedding.append(float(temp[i + 1]))
		word.append(temp[0])
		embedding.append(temp_embedding)

	return voca_size - error_voc, emb_dim, word, embedding


def pad_sentences(sentences, padding_word="<PAD/>", forced_sequence_length=None):
	"""Pad setences during training or prediction"""
	if forced_sequence_length is None: # Train
		sequence_length = max(len(x) for x in sentences)
	else: # Prediction
		logging.critical('This is prediction, reading the trained sequence length')
		sequence_length = forced_sequence_length

	padded_sentences = []
	for i in range(len(sentences)):
		sentence = sentences[i]
		num_padding = sequence_length - len(sentence)

		if num_padding < 0: # Prediction: cut off the sentence if it is longer than the sequence length
			logging.info('This sentence has to be cut off because it is longer than trained sequence length')
			padded_sentence = sentence[0:sequence_length]
		else:
			padded_sentence = sentence + [padding_word] * num_padding
		padded_sentences.append(padded_sentence)
	return padded_sentences

def build_vocab(sentences):
	word_counts = Counter(itertools.chain(*sentences))
	limit = int(len(word_counts.items())*0.9)
	vocabulary_inv = [word[0] for word in word_counts.most_common()]
	vocabulary = {word: index for index, word in enumerate(vocabulary_inv)}

	return vocabulary, vocabulary_inv, limit

def morph_data(str):

	pair = ""

	for (word, morp) in k:
		pair += word + '/' + morp+' '
	return pair.strip()

def batch_iter(data, batch_size, num_epochs, shuffle=False):
	data = np.array(data)
	data_size = len(data)
	num_batches_per_epoch = int(data_size / batch_size) + 1

	for epoch in range(num_epochs):
		if shuffle:
			shuffle_indices = np.random.permutation(np.arange(data_size))
			shuffled_data = data[shuffle_indices]
		else:
			shuffled_data = data

		for batch_num in range(num_batches_per_epoch):
			start_index = batch_num * batch_size
			end_index = min((batch_num + 1) * batch_size, data_size)
			yield shuffled_data[start_index:end_index]

def load_data(in_file, out_file):
	###################################################################
	#       open corpuses, analyes the sentences into morphemes       #
	#       INPUT : nothing											  #
	#		RETURN : x, y, vocabulary, 								  #
	# 				embedding_mat, labels, new_x, new_y				  #
	###################################################################

	corpus = list(open(in_file, "r", encoding='utf-8').readlines())
	corpus = np.array([s.strip() for s in corpus])

	label_list=[]
	sentence_list=[]

	for line in corpus:
		if len(line)<=1:
			continue
		line_ = line.split('\t')

		label_list.append(line_[-1])
		sentence_list.append(line_[0])
	label_list.append('None')
	labels = sorted(list(set(label_list)))
	label_list.pop()
	num_labels = len(labels)
	one_hot = np.zeros((num_labels, num_labels), int)
	np.fill_diagonal(one_hot, 1)

	label_dict = dict(zip(labels, one_hot))

	x_raw = [s.split('|') for s in sentence_list[:-3000]]
	y_raw = [label_dict[s] for s in label_list[:-3000]]
	pre_y_raw = [[labels.index('None')]]
	pre_y_raw.extend([[labels.index(s)] for s in label_list[:-3000]])
	pre_y_raw.pop()

	yj_x = [s.split('|') for s in sentence_list[-3000:]]
	yj_y = [label_dict[s] for s in label_list[-3000:]]
	yj_pre_y = [[labels.index('None')]]
	yj_pre_y.extend([[labels.index(s)] for s in label_list[-3000:]])
	yj_pre_y.pop()
	pre_label_dict = {}
	for p,_ in enumerate(label_list):
		pre_label_dict[p] = np.random.uniform(-0.25,0.25,64)

	total_x = np.r_[x_raw, yj_x]

	del label_list

	total_x = pad_sentences(total_x)
	vocabulary_, vocabulary_inv,limit = build_vocab(total_x)
	vocabulary, embedding_mat = load_embeddings(vocabulary_)

	x_raw = pad_sentences(x_raw)

	yj_x = pad_sentences(yj_x, forced_sequence_length=len(x_raw[0]))

	tmp = []
	tmp_ = []
	for sentence in x_raw:
		for word in sentence:
			if word in vocabulary:
				tmp.append(vocabulary[word])
			else:
				tmp.append(vocabulary['<UNK>'])
		tmp_.append(tmp)
		tmp = []

	x = np.array(tmp_)
	y = np.array(y_raw)
	pre_y = np.array(pre_y_raw)

	tmp = []
	tmp_ = []
	for sentence in yj_x:
		for word in sentence:
			if word in vocabulary:
				tmp.append(vocabulary[word])
			else:
				tmp.append(vocabulary['<UNK>'])
		tmp_.append(tmp)
		tmp = []

	new_x = np.array(tmp_)
	new_y = np.array(yj_y)
	new_pre_y = np.array(yj_pre_y)

	del x_raw
	del y_raw

	return x, y, pre_y, vocabulary, embedding_mat, pre_label_dict, labels, new_x, new_y, new_pre_y
