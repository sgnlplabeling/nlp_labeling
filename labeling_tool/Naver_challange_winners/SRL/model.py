#-*-encoding:utf-8-*-
import numpy as np
import tensorflow as tf
from data_utils import get_sequence_length, get_max, get_word_length
from highway_lstm_cell import LSTMCell
from tensorflow.contrib.crf import crf_log_likelihood
from tensorflow.contrib.crf import viterbi_decode
from tensorflow.contrib.layers.python.layers import initializers

import custom_rnncell as rnn
from model_utils import result_to_json
from attention import multihead_attention, attention_bias, linear
import sys

class Model(object):
	def __init__(self, config, word_to_id, pumsa_to_id, char_to_id, tag_to_id, embedding_matrix):
		self.word_to_id = word_to_id
		self.pumsa_to_id = pumsa_to_id
		self.char_to_id = char_to_id
		self.tag_to_id = tag_to_id
		"""12.06 영준 수정"""
		self.embedding_matrix = embedding_matrix

		self.config = config
		self.lr = config["lr"]
		self.char_dim = config["char_dim"]
		self.word_dim = config["word_dim"]
		self.pumsa_dim = config["pumsa_dim"]
		self.char_lstm_dim = config["char_lstm_dim"]
		self.word_lstm_dim = config["word_lstm_dim"]
		self.pumsa_lstm_dim = config["pumsa_lstm_dim"]


		self.num_tags = config["num_tags"]
		self.num_chars = config["num_chars"]
		self.num_word = config["num_words"]
		self.num_pumsa = config["num_pumsas"]
		self.num_layers = config["num_layers"]

		self.global_step = tf.Variable(0, trainable=False)
		self.best_dev_f1 = tf.Variable(0.0, trainable=False)
		self.best_test_f1 = tf.Variable(0.0, trainable=False)
		if config["initializer"] == "xavier":
			self.initializer = initializers.xavier_initializer()
		elif config["initializer"] == "orthogonal":
			self.initializer = tf.orthogonal_initializer()
		# add placeholders for the model

		self.word_inputs1 = tf.placeholder(dtype=tf.int32,
										   shape=[None, None],
										   name="word_inputs1"
										   )
		self.word_inputs2 = tf.placeholder(dtype=tf.int32,
										   shape=[None, None],
										   name="word_inputs2"
										   )
		self.word_inputs3 = tf.placeholder(dtype=tf.int32,
										   shape=[None, None],
										   name="word_inputs3"
										   )
		self.word_inputs4 = tf.placeholder(dtype=tf.int32,
										   shape=[None, None],
										   name="word_inputs4"
										   )
		self.pumsa_inputs1 = tf.placeholder(dtype=tf.int32,
										   shape=[None, None],
										   name="pumsa_inputs1"
										   )
		self.pumsa_inputs2 = tf.placeholder(dtype=tf.int32,
										   shape=[None, None],
										   name="pumsa_inputs2"
										   )
		self.pumsa_inputs3 = tf.placeholder(dtype=tf.int32,
											shape=[None, None],
											name="pumsa_inputs3"
											)
		self.pumsa_inputs4 = tf.placeholder(dtype=tf.int32,
											shape=[None, None],
											name="pumsa_inputs4"
											)

		self.char_inputs = tf.placeholder(dtype=tf.int32,
											# [batch, word_in_sen, char_in_word]
										  shape=[None, None, None],
										  name="CharInputs")
		self.targets = tf.placeholder(dtype=tf.int32,
									  shape=[None, None],
									  name="Targets")
		# dropout keep prob
		self.dropout = tf.placeholder(dtype=tf.float32,
									  name="Dropout")

		self.elmo_dropout = tf.placeholder(dtype=tf.float32,
										   name='Elmo_Dropout')

		self.char_length = tf.placeholder(dtype=tf.int32,
										  name = "char_length")
		if config["elmo"]:
			self.elmo1 = tf.placeholder(dtype=tf.float32,
										shape=[None, None, 1024],
										name="elmo1"
										)
			self.elmo4 = tf.placeholder(dtype=tf.float32,
										shape=[None, None, 1024],
										name="elmo4"
										)


		char_used = tf.sign(tf.abs(self.char_inputs)) #존재하는 곳에 1인 mask
		word_used = tf.to_float(tf.sign(tf.abs(self.word_inputs1)))
		char_length = tf.reduce_sum(char_used, reduction_indices=2)
		word_length = tf.reduce_sum(tf.sign(char_length), reduction_indices=1)
		self.word_lengths = tf.cast(word_length, tf.int32)
		self.batch_size = tf.shape(self.char_inputs)[0]
		self.word_num_steps = tf.shape(self.char_inputs)[-2]

		# embeddings for chinese character and segmentation representation
		word_embed, embedding = self.embedding_layer(self.word_inputs1, self.word_inputs2, self.word_inputs3, self.word_inputs4,
													 self.pumsa_inputs1, self.pumsa_inputs2, self.pumsa_inputs3, self.pumsa_inputs4, self.char_inputs, word_length)

		# apply dropout before feed to lstm layer
		embedding = tf.nn.dropout(embedding, self.dropout)
		word_encoded = self.get_word_representation(embedding)
		word_encoded = tf.nn.dropout(word_encoded, self.dropout)

		if config["elmo"]:
			self.elmo1 = tf.nn.dropout(self.elmo1, self.elmo_dropout)
			self.elmo4 = tf.nn.dropout(self.elmo4, self.elmo_dropout)
			word_encoded = tf.concat([word_embed, word_encoded, self.elmo1, self.elmo4], axis=-1)
		else:
			word_encoded = tf.concat([word_embed, word_encoded], axis=-1)

		lstm_outputs = self.add_stacked_lstm_layers(word_encoded, self.word_lstm_dim, self.word_lengths, config["highway"])
		if config["self_attention"]:
			attn_bias = attention_bias(word_used, "masking")
			lstm_outputs = multihead_attention(
				lstm_outputs,
				None,
				attn_bias,
				100,
				100,
				100,
				2,
				attention_function="dot_product")
			# x = self._residual_fn(x, y, params)

		# self.logits = linear(lstm_outputs, self.num_tags, True)

		# logits for tags
		self.logits = self.project_layer(lstm_outputs)

		# loss of the model
		self.loss = self.loss_layer(self.logits, self.word_lengths)

		with tf.variable_scope("optimizer", reuse=tf.AUTO_REUSE):
			optimizer = self.config["optimizer"]
			if optimizer == "sgd":
				self.opt = tf.train.GradientDescentOptimizer(self.lr)
			elif optimizer == "adam":
				self.opt = tf.train.AdamOptimizer(self.lr)
			elif optimizer == "adgrad":
				self.opt = tf.train.AdagradOptimizer(self.lr)
			elif optimizer == "momentum":
				self.opt = tf.train.MomentumOptimizer(self.lr, 0.9)
			else:
				raise KeyError

			# apply grad clip to avoid gradient explosion
			grads_vars = self.opt.compute_gradients(self.loss)
			capped_grads_vars = [[tf.clip_by_value(g, -self.config["clip"], self.config["clip"]), v]
								 for g, v in grads_vars]
			self.train_op = self.opt.apply_gradients(capped_grads_vars, self.global_step)

		# saver of the model
		self.saver = tf.train.Saver(tf.global_variables(), max_to_keep=5)


	def affix_embedding(self, pre, suf):
		"""
		:param pre: prefix input
		:param suf: suffix input
		:return: embedded affix
		"""
		with tf.variable_scope("prefix_embedding", reuse=tf.AUTO_REUSE), tf.device('/cpu:0'):
			self.prefix_lookup = tf.get_variable(
				name="prefix_embedding",
				shape=[self.num_prefix, self.prefix_dim],
				initializer=self.initializer)
			prefix_embedded = tf.nn.embedding_lookup(self.prefix_lookup, self.prefix_vec)

		with tf.variable_scope("suffix_embedding", reuse=tf.AUTO_REUSE), tf.device('/cpu:0'):
			self.suffix_lookup = tf.get_variable(
				name="suffix_embedding",
				shape=[self.num_suffix, self.suffix_dim],
				initializer=self.initializer)
			suffix_embedded =tf.nn.embedding_lookup(self.suffix_lookup, self.suffix_vec)

		return prefix_embedded, suffix_embedded

	def get_word_representation(self, embedding):
		position_encoding_mat = self._position_encoding(self.config["max_char_length"], self.char_dim)
		position_encoded = tf.reduce_sum(embedding * position_encoding_mat, 2)
		return position_encoded
	
	def _position_encoding(self, sentence_size, embedding_size):
		encoding = np.ones((embedding_size, sentence_size), dtype=np.float32)
		ls = sentence_size+1
		le = embedding_size+1
		for i in range(1, le):
			for j in range(1, ls):
				encoding[i-1, j-1] = (i - (le-1)/2) * (j - (ls-1)/2)
		encoding = 1 + 4 * encoding / embedding_size / sentence_size
		return np.transpose(encoding)

	def embedding_layer(self, word_inputs1, word_inputs2, word_inputs3, word_inputs4,
						pumsa_inputs1, pumsa_inputs2, pumsa_inputs3, pumsa_inputs4, char_inputs, char_length, name=None):
		"""
		:param char_inputs: one-hot encoding of sentence
		:return: [1, num_steps, embedding size],
		"""
		with tf.variable_scope("word_embedding"), tf.device('/cpu:0'):

			if self.config["pretrained_embedding"]:
				self.glove_lookup = tf.Variable(
					self.embedding_matrix,
					name="word_embedding",
					dtype=tf.float32
				)
			else:
				self.glove_lookup = tf.get_variable(
						name="word_embedding",
						shape=[self.num_word, self.word_dim],
						initializer=self.initializer)

			glove_embed1 = tf.nn.embedding_lookup(self.glove_lookup, word_inputs1)
			glove_embed2 = tf.nn.embedding_lookup(self.glove_lookup, word_inputs2)
			glove_embed3 = tf.nn.embedding_lookup(self.glove_lookup, word_inputs3)
			glove_embed4 = tf.nn.embedding_lookup(self.glove_lookup, word_inputs4)

			word_embed = tf.concat([glove_embed1, glove_embed2, glove_embed3, glove_embed4], axis=-1)
			word_embed = tf.nn.dropout(word_embed, self.dropout)

		with tf.variable_scope("pumsa_embedding", reuse=tf.AUTO_REUSE), tf.device('/cpu:0'):
			if self.config["pretrained_pumsa_embedding"]:
				self.pumsa_lookup = tf.Variable(self.pumsa_matrix,
												"pumsa_embedding",
												dtype=tf.float32)
			else:
				self.pumsa_lookup = tf.get_variable(
						name="pumsa_embedding",
						shape=[self.num_pumsa, self.pumsa_dim],
						initializer=self.initializer)
			pumsa_embed1 = tf.nn.embedding_lookup(self.pumsa_lookup, pumsa_inputs1)
			pumsa_embed2 = tf.nn.embedding_lookup(self.pumsa_lookup, pumsa_inputs2)
			pumsa_embed3 = tf.nn.embedding_lookup(self.pumsa_lookup, pumsa_inputs3)
			pumsa_embed4 = tf.nn.embedding_lookup(self.pumsa_lookup, pumsa_inputs4)
			pumsa_embed = tf.concat([pumsa_embed1, pumsa_embed2, pumsa_embed3, pumsa_embed4], axis=-1)
			pumsa_embed = tf.nn.dropout(pumsa_embed, self.dropout)

		with tf.variable_scope("char_embedding", reuse=tf.AUTO_REUSE), tf.device('/cpu:0'):
			self.char_lookup = tf.get_variable(
					name="char_embedding",
					shape=[self.num_chars, self.char_dim],
					initializer=self.initializer)
			embed = tf.nn.embedding_lookup(self.char_lookup, char_inputs)

			s = tf.shape(embed)
			char_embeddings = tf.reshape(embed, shape=[-1, s[-2], self.config["char_dim"]])
			word_lengths = tf.reshape(self.char_length, shape=[-1])
			# bi lstm on chars
			# need 2 instances of cells since tf 1.1
			char_cell_fw = LSTMCell(self.config["char_lstm_dim"], state_is_tuple=True,
									initializer=self.initializer)
			char_cell_bw = LSTMCell(self.config["char_lstm_dim"], state_is_tuple=True,
									initializer=self.initializer)

			_, ((_, char_output_fw), (_, char_output_bw)) = tf.nn.bidirectional_dynamic_rnn(char_cell_fw,
																							char_cell_bw,
																							char_embeddings,
																							sequence_length=word_lengths,
																							dtype=tf.float32)

			output = tf.concat([char_output_fw, char_output_bw], axis=-1)
			char_embed = tf.reshape(output, shape=[-1, s[1], 2 * self.config["char_lstm_dim"]])
			char_embed = tf.nn.dropout(char_embed, self.dropout)

		#print(tf.shape(word_embed))
		#print(tf.shape(pumsa_embed))
		#print(tf.shape(char_embed))
		word_embed = tf.concat([word_embed, pumsa_embed, char_embed], axis=-1)
		return word_embed, embed



	def biLSTM_layer(self, lstm_inputs, lstm_dim, lengths, name=None):
		"""
		:param lstm_inputs: [batch_size, num_steps, emb_size] 
		:return: [batch_size, num_steps, 2*lstm_dim] 
		"""
		with tf.variable_scope("char_BiLSTM" if not name else name, reuse=tf.AUTO_REUSE):
			lstm_cell = {}
			for direction in ["forward", "backward"]:
				with tf.variable_scope(direction, reuse=tf.AUTO_REUSE):
					lstm_cell[direction] = rnn.CoupledInputForgetGateLSTMCell(
						lstm_dim,
						use_peepholes=True,
						initializer=self.initializer,
						state_is_tuple=True)
			outputs, final_states = tf.nn.bidirectional_dynamic_rnn(
				lstm_cell["forward"],
				lstm_cell["backward"],
				lstm_inputs,
				dtype=tf.float32,
				sequence_length=lengths)
		return tf.concat(outputs, axis=2)

	def add_stacked_lstm_layers(self, lstm_inputs, lstm_dim, lengths, highway=False, name=None):
		if highway :
			cell = LSTMCell
		else:
			cell = tf.contrib.rnn.LSTMCell
		cells_fw = [cell(lstm_dim)
					for _ in range(self.num_layers)]
		cells_bw = [cell(lstm_dim)
					for _ in range(self.num_layers)]

		cells_fw = [tf.nn.rnn_cell.DropoutWrapper(
			cell,
			input_keep_prob=self.dropout,
			state_keep_prob=self.dropout) for cell in cells_fw]
		cells_bw = [tf.nn.rnn_cell.DropoutWrapper(
			cell,
			input_keep_prob=self.dropout,
			state_keep_prob=self.dropout) for cell in cells_bw]
		outputs, _, _ = tf.contrib.rnn.stack_bidirectional_dynamic_rnn(
			cells_fw=cells_fw,
			cells_bw=cells_bw,
			inputs=lstm_inputs,
			sequence_length=lengths,
			dtype=tf.float32)
		return outputs

	def project_layer(self, lstm_outputs, name=None):
		"""
		hidden layer between lstm layer and logits
		:param lstm_outputs: [batch_size, num_steps, emb_size] 
		:return: [batch_size, num_steps, num_tags]
		"""
		with tf.variable_scope("project"  if not name else name, reuse=tf.AUTO_REUSE):
			with tf.variable_scope("hidden", reuse=tf.AUTO_REUSE):
				W = tf.get_variable("W", shape=[self.word_lstm_dim*2, self.word_lstm_dim],
									dtype=tf.float32, initializer=self.initializer)

				b = tf.get_variable("b", shape=[self.word_lstm_dim], dtype=tf.float32,
									initializer=tf.zeros_initializer())
				output = tf.reshape(lstm_outputs, shape=[-1, self.word_lstm_dim*2])
				hidden = tf.tanh(tf.nn.xw_plus_b(output, W, b))

			# project to score of tags
			with tf.variable_scope("logits", reuse=tf.AUTO_REUSE):
				W = tf.get_variable("W", shape=[self.word_lstm_dim, self.num_tags],
									dtype=tf.float32, initializer=self.initializer)

				b = tf.get_variable("b", shape=[self.num_tags], dtype=tf.float32,
									initializer=tf.zeros_initializer())

				pred = tf.nn.xw_plus_b(hidden, W, b)

			return tf.reshape(pred, [-1, self.word_num_steps, self.num_tags])

	def loss_layer(self, project_logits, lengths, name=None):
		"""
		calculate crf loss
		:param project_logits: [1, num_steps, num_tags]
		:return: scalar loss
		"""
		with tf.variable_scope("crf_loss"  if not name else name, reuse=tf.AUTO_REUSE):
			small = -1000.0
			# pad logits for crf loss
			start_logits = tf.concat(
				[small * tf.ones(shape=[self.batch_size, 1, self.num_tags]), tf.zeros(shape=[self.batch_size, 1, 1])], axis=-1)
			pad_logits = tf.cast(small * tf.ones([self.batch_size, self.word_num_steps, 1]), tf.float32)
			logits = tf.concat([project_logits, pad_logits], axis=-1)
			logits = tf.concat([start_logits, logits], axis=1)
			targets = tf.concat(
				[tf.cast(self.num_tags*tf.ones([self.batch_size, 1]), tf.int32), self.targets], axis=-1)

			self.trans = tf.get_variable(
				"transitions",
				shape=[self.num_tags + 1, self.num_tags + 1],
				initializer=self.initializer)
			log_likelihood, self.trans = crf_log_likelihood(
				inputs=logits,
				tag_indices=targets,
				transition_params=self.trans,
				sequence_lengths=lengths+1)
			return tf.reduce_mean(-log_likelihood)

	def create_feed_dict(self, sess, context_embeddings_op, elmo_context, elmo_ids, is_train, batch):
		"""
		:param is_train: Flag, True for train batch
		:param batch: list train/evaluate data 
		:return: structured data to feed
		"""
		words1, words2, words3, words4, pumsas1, pumsas2, pumsas3, pumsas4, elmo, w1_idxs, w4_idxs, chars, tags = batch
		char_length = get_word_length(chars, self.char_to_id["<PAD>"])

		if self.config['elmo']:
			elmo_context_input_ = sess.run(
				[elmo_context['weighted_op']],
				feed_dict={elmo_ids: elmo}
			)

			elmo_context_input_ = elmo_context_input_[0]
			w1_elmo_contexts, w4_elmo_contexts = [], []
			max_morph_length = max([len(a) for a in w4_idxs])
			for batch_idx in range(len(w1_idxs)):
				w1_elmo_context, w4_elmo_context = [], []
				for w_idx, _ in enumerate(w1_idxs[batch_idx]):
					w1_idx = w1_idxs[batch_idx][w_idx]
					w4_idx = w4_idxs[batch_idx][w_idx]

					w1_elmo_context.append(elmo_context_input_[batch_idx][w1_idx])
					w4_elmo_context.append(elmo_context_input_[batch_idx][w4_idx])

				if len(w1_elmo_context) < max_morph_length:
					for _ in range(max_morph_length-len(w1_elmo_context)):
						w1_elmo_context.append(np.zeros(1024, dtype=float))
						w4_elmo_context.append(np.zeros(1024, dtype=float))
				w1_elmo_contexts.append(w1_elmo_context)
				w4_elmo_contexts.append(w4_elmo_context)

		feed_dict = {
			self.word_inputs1: np.array(words1),
			self.word_inputs2: np.array(words2),
			self.word_inputs3: np.array(words3),
			self.word_inputs4: np.array(words4),
			self.pumsa_inputs1: np.array(pumsas1),
			self.pumsa_inputs2: np.array(pumsas2),
			self.pumsa_inputs3: np.array(pumsas3),
			self.pumsa_inputs4: np.array(pumsas4),
			self.char_inputs: np.array(chars),
			self.dropout: 1.0,
			self.elmo_dropout: 1.0,
			self.char_length : char_length
		}
		'''
		print ('chars')
		print (chars)
		print ('after chars')
		print (feed_dict[self.char_inputs])
		print 
		'''
		if self.config["elmo"]:
			feed_dict[self.elmo1] = np.array(w1_elmo_contexts)
			feed_dict[self.elmo4] = np.array(w4_elmo_contexts)
		if is_train:
			feed_dict[self.targets] = np.asarray(tags)
			feed_dict[self.dropout] = self.config["dropout_keep"]
			feed_dict[self.elmo_dropout] = self.config["elmo_dropout_keep"]
			'''
			print ('tags')
			print (tags)
			print ('after tags')
			print (feed_dict[self.targets])
			print
			'''
		return feed_dict

	def run_step(self, sess, context_embeddings_op, elmo_context, elmo_ids, is_train, batch, elmo_dict=None):
		"""
		:param sess: session to run the batch
		:param is_train: a flag indicate if it is a train batch
		:param batch: a dict containing batch data
		:return: batch result, loss of the batch or logits
		"""
		feed_dict = self.create_feed_dict(sess, context_embeddings_op, elmo_context, elmo_ids, is_train, batch)
		
		if is_train:
			global_step, loss, _ = sess.run(
				[self.global_step, self.loss, self.train_op],
				feed_dict)
			return global_step, loss
		else:
			lengths, logits = sess.run([self.word_lengths, self.logits], feed_dict)
			return lengths, logits

	def decode(self, logits, lengths, matrix):
		"""
		:param logits: [batch_size, num_steps, num_tags]float32, logits
		:param lengths: [batch_size]int32, real length of each sequence
		:param matrix: transaction matrix for inference
		:return:
		"""
		# inference final labels usa viterbi Algorithm
		paths = []
		small = -1000.0
		start = np.asarray([[small]*self.num_tags +[0]])
		for score, length in zip(logits, lengths):
			score = score[:length]
			pad = small * np.ones([length, 1])
			logits = np.concatenate([score, pad], axis=1)
			logits = np.concatenate([start, logits], axis=0)
			path, _ = viterbi_decode(logits, matrix)

			paths.append(path[1:])
		return paths

	def evaluate_model(self, sess, context_embeddings_op, elmo_context, elmo_ids, data_manager, id_to_tag):
		"""
		:param sess: session  to run the model 
		:param data: list of data
		:param id_to_tag: index to tag name
		:return: evaluate result
		"""
		results = []
		trans = self.trans.eval(session=sess)
		for batch in data_manager.iter_batch():
			strings = batch[-2]
			tags = batch[-1]
			lengths, scores = self.run_step(sess, context_embeddings_op, elmo_context, elmo_ids, False, batch)
			batch_paths = self.decode(scores, lengths, trans)
			for i in range(len(strings)):
				result = []
				string = strings[i][:lengths[i]]
				gold = [id_to_tag[int(x)] for x in tags[i][:lengths[i]]]
				pred = [id_to_tag[int(x)] for x in batch_paths[i][:lengths[i]]]
				for char, gold, pred in zip(string, gold, pred):
					result.append(" ".join([gold, pred]))
				results.append(result)
		return results

	def evaluate_lines(self, sess, context_embeddings_op, elmo_context, elmo_ids, inputs, id_to_tag):
		trans = self.trans.eval(session=sess)
		lengths, scores = self.run_step(sess, context_embeddings_op, elmo_context, elmo_ids, False, inputs)
		batch_paths = self.decode(scores, lengths, trans)
		total_tags = [[id_to_tag[idx] for idx in path] for path in batch_paths]
		return [(0.0,tag) for tag in total_tags]

	def input_Bilstm_layer(self, inputs, sequence_length, num_units):
		cell = tf.contrib.rnn.LSTMCell
		cell_fw = cell(num_units, state_is_tuple=True)
		cell_bw = cell(num_units, state_is_tuple=True)
		_, ((_, output_fw), (_, output_bw)) = tf.nn.bidirectional_dynamic_rnn(
			cell_fw, cell_bw,
			inputs, sequence_length=sequence_length,
			dtype=tf.float32)
		final_states = tf.concat([output_fw, output_bw], axis=-1)
		return final_states