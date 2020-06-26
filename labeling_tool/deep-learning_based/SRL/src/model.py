import tensorflow as tf
import numpy as np
import biRNN

from data_utils import get_word_length
from config import Config
from tensorflow.contrib.layers.python.layers import initializers
from tensorflow.contrib.crf import crf_log_likelihood
from tensorflow.contrib.crf import viterbi_decode

config = Config()

class Model(object):
	def __init__(self, word2idx, pumsa2idx, char2idx, label2idx, lemma2idx, word_embedding_matrix):

		self.word2idx = word2idx
		self.pumsa2idx = pumsa2idx
		self.char2idx = char2idx
		self.label2idx = label2idx
		self.lemma2idx = lemma2idx

		self.word_embedding_matrix = word_embedding_matrix

		self.global_step = tf.Variable(0, trainable=False)
		self.best_dev_f1 = tf.Variable(0.0, trainable=False)
		self.best_test_f1 = tf.Variable(0.0, trainable=False)

		if config.initializer == "xavier":
			self.initializer = initializers.xavier_initializer()
		elif config.initializer == "orthogonal":
			self.initializer = tf.orthogonal_initializer()

		self.add_placeholder()
		self.get_input_embeddings()
		self.build_model()
		self.loss_layer()


	def add_placeholder(self):
                self.word_berts1 = tf.placeholder(dtype=tf.float32, shape=[None, None, 768], name = "word_berts1")

                self.word_inputs1 = tf.placeholder(dtype=tf.int32, shape=[None, None], name="word_inputs1")
                self.word_inputs2 = tf.placeholder(dtype=tf.int32,  shape=[None, None],  name="word_inputs2" )
                self.word_inputs3 = tf.placeholder(dtype=tf.int32, shape=[None, None],  name="word_inputs3" )
                self.word_inputs4 = tf.placeholder(dtype=tf.int32, shape=[None, None],  name="word_inputs4" )


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
                self.char_inputs = tf.placeholder(dtype=tf.int32, shape=[None, None, None], name="char_inputs")

                self.input_lemma = tf.placeholder(dtype=tf.int32, shape=[None, None],name="input_lemma")
                self.predicate_idxs = tf.placeholder(dtype=tf.int32,shape=[None, 2],name="predicate_idxs")
                self.predicate_distances = tf.placeholder(dtype=tf.float32,shape=[None, None, 14], name="predicate_distances")
                self.binary_vector = tf.placeholder(dtype=tf.float32,
											shape=[None, None, 2],
											name="binary_vector"
											)
                self.predicate_words1 = tf.placeholder(dtype=tf.int32,shape=[None, None], name="predicate_words1" )
                self.predicate_words2 = tf.placeholder(dtype=tf.int32,  shape=[None, None], name="predicate_words2")
                self.predicate_pumsas1 = tf.placeholder(dtype=tf.int32,
												shape=[None, None],
												name="predicate_pumsas1"
												)
                self.predicate_pumsas2 = tf.placeholder(dtype=tf.int32,
												shape=[None, None],
												name="predicate_pumsas2"
												)
                self.input_roles = tf.placeholder(dtype=tf.int32,
									shape=[None, None],
									name="input_roles")
                self.labels = tf.placeholder(dtype=tf.int32,shape=[None, None],name="labels")
                self.dropout = tf.placeholder(dtype=tf.float32,name="dropout")
                self.char_length = tf.placeholder(dtype=tf.int32, name="char_length")

                if config.ELMo:
                        self.ELMo_input1 = tf.placeholder(dtype=tf.float32,
										shape=[None, None, 1024],
										name="ELMo_input1")
                        self.ELMo_input2 = tf.placeholder(dtype=tf.float32, shape=[None, None, 1024],name="ELMo_input2")

	def get_input_embeddings(self):
		char_used = tf.sign(tf.abs(self.char_inputs))
		# word_used = tf.to_float(tf.sign(tf.abs(self.word_inputs1)))
		char_length = tf.reduce_sum(char_used, reduction_indices=2)
		word_length = tf.reduce_sum(tf.sign(char_length), reduction_indices=1)

		self.word_lengths = tf.cast(word_length, tf.int32)
		self.batch_size = tf.shape(self.char_inputs)[0]
		self.word_num_steps = tf.shape(self.char_inputs)[-2]

		word_embed, char_embedding = self.embedding_layer(self.word_inputs1, self.word_inputs2,self.word_inputs3, self.word_inputs4,
													 self.pumsa_inputs1, self.pumsa_inputs2, self.pumsa_inputs3, self.pumsa_inputs4,
													 self.char_inputs)

		char_positioning_encoded = self.get_positioning_encoding(char_embedding)
		char_positioning_encoded = tf.nn.dropout(char_positioning_encoded, self.dropout)

		self.input_encoding = tf.concat([word_embed, char_positioning_encoded, self.binary_vector, self.predicate_distances, self.word_berts1], axis=-1)
		if config.ELMo:
			self.ELMo_input1 = tf.nn.dropout(self.ELMo_input1, self.dropout)
			self.ELMo_input2 = tf.nn.dropout(self.ELMo_input2, self.dropout)
			self.input_encoding = tf.concat([self.input_encoding, self.ELMo_input1, self.ELMo_input2], axis=-1)


	def build_model(self):
		lstm_outputs, hidden_states = self.add_stacked_lstm_layers()

		fw_predicate_state = tf.gather_nd(hidden_states[0], self.predicate_idxs)
		fw_predicate_state = tf.tile(tf.expand_dims(fw_predicate_state, 1), [1, tf.shape(lstm_outputs)[1], 1])
		bw_predicate_state = tf.gather_nd(hidden_states[1], self.predicate_idxs)
		bw_predicate_state = tf.tile(tf.expand_dims(bw_predicate_state, 1), [1, tf.shape(lstm_outputs)[1], 1])

		hidden_states = tf.concat([hidden_states[0], hidden_states[1]], -1)
		predicate_state = tf.concat([fw_predicate_state, bw_predicate_state], -1)
		mul_state = tf.multiply(tf.reshape(hidden_states, [-1, 2 * config.lstm_dim]),
								tf.reshape(predicate_state, [-1, 2 * config.lstm_dim]))
		mul_state = tf.reshape(mul_state, [-1, tf.shape(lstm_outputs)[1], 2 * config.lstm_dim])

		lstm_outputs = tf.concat(
			[lstm_outputs, predicate_state, mul_state, hidden_states], axis=-1)
		lstm_outputs_dim = 2 * 4 * config.lstm_dim



		self.role_embedding_table = tf.get_variable(name="role_lookup",
			shape=[23, 100], initializer=self.initializer)
		role_embed = tf.nn.embedding_lookup(self.role_embedding_table, self.input_roles)

		U = tf.get_variable(name="U",
			shape=[300, lstm_outputs_dim],
			initializer=self.initializer)

		lemma_embedding_table = tf.get_variable(
			name="lemma_embedding_table",
			shape=[len(self.lemma2idx), 100],
			initializer=self.initializer)

		lemma_embed = tf.nn.embedding_lookup(lemma_embedding_table, self.input_lemma)

		replicated_lemma_embed = tf.tile(lemma_embed[:, :1, :], [1, 23, 1])
		role_lemma_info = tf.concat([role_embed, replicated_lemma_embed, role_embed+replicated_lemma_embed], axis=-1)
		specific_W = tf.nn.relu(tf.matmul(role_lemma_info, tf.tile(tf.expand_dims(U, 0), [tf.shape(lstm_outputs)[0], 1, 1])))
		specific_W = tf.transpose(specific_W, [0, 2, 1])

		self.logits = tf.matmul(lstm_outputs, specific_W)

	def loss_layer(self):
		self.loss = self.crf_loss_layer()
		tf.summary.scalar('loss', self.loss)

		with tf.variable_scope("optimizer", reuse=tf.AUTO_REUSE):
			self.opt = tf.train.AdamOptimizer(config.lr)

		grads_vars = self.opt.compute_gradients(self.loss)
		capped_grads_vars = [[tf.clip_by_value(g, -config.clip, config.clip), v]
							 for g, v in grads_vars]
		self.train_op = self.opt.apply_gradients(capped_grads_vars, self.global_step)

		self.saver = tf.train.Saver(tf.global_variables(), max_to_keep=5)
		self.merge = tf.summary.merge_all()

	def crf_loss_layer(self):
		with tf.variable_scope("crf_loss", reuse=tf.AUTO_REUSE):
			small = -1000.0
			# pad logits for crf loss
			start_logits = tf.concat(
				[small * tf.ones(shape=[self.batch_size, 1, len(self.label2idx)]), tf.zeros(shape=[self.batch_size, 1, 1])], axis=-1)
			pad_logits = tf.cast(small * tf.ones([self.batch_size, self.word_num_steps, 1]), tf.float32)
			logits = tf.concat([self.logits, pad_logits], axis=-1)
			logits = tf.concat([start_logits, logits], axis=1)
			targets = tf.concat(
				[tf.cast(len(self.label2idx)*tf.ones([self.batch_size, 1]), tf.int32), self.labels], axis=-1)

			self.trans = tf.get_variable(
				"transitions",
				shape=[len(self.label2idx) + 1, len(self.label2idx) + 1],
				initializer=self.initializer)
			log_likelihood, self.trans = crf_log_likelihood(
				inputs=logits,
				tag_indices=targets,
				transition_params=self.trans,
				sequence_lengths=self.word_lengths+1)
			return tf.reduce_mean(-log_likelihood)


	def add_stacked_lstm_layers(self):
		with tf.variable_scope("stacked_LSTM_layers", reuse=tf.AUTO_REUSE), tf.device('/cpu:0'):
			cell = tf.contrib.rnn.LSTMCell
			cells_fw = [cell(config.lstm_dim) for _ in range(config.num_layers)]
			cells_bw = [cell(config.lstm_dim) for _ in range(config.num_layers)]

			cells_fw = [tf.nn.rnn_cell.DropoutWrapper(cell,
				input_keep_prob=self.dropout,
				state_keep_prob=self.dropout) for cell in cells_fw]
			cells_bw = [tf.nn.rnn_cell.DropoutWrapper(cell,
				input_keep_prob=self.dropout,
				state_keep_prob=self.dropout) for cell in cells_bw]

			outputs, _, _, each_states = biRNN.stack_bidirectional_dynamic_rnn(
				cells_fw=cells_fw,
				cells_bw=cells_bw,
				inputs=self.input_encoding,
				sequence_length=self.word_lengths,
				dtype=tf.float32,
				return_all_states=True)
			return outputs, each_states


	def embedding_layer(self, word_inputs1, word_inputs2, word_inputs3, word_inputs4,
						pumsa_inputs1, pumsa_inputs2, pumsa_inputs3, pumsa_inputs4, char_inputs):

		with tf.variable_scope("word_embedding"), tf.device('/cpu:0'):
			if config.pretrained_embeddings:
				self.word_embedding_table = tf.Variable(
						self.word_embedding_matrix,
						name="word_embedding_matrix",
						dtype=tf.float32)
			else:
				self.word_embedding_table = tf.get_variable(
				name="word_embedding_matrix",
				shape=[len(self.word2idx), config.word_dim],
				initializer=self.initializer)

			word_embed1 = tf.nn.embedding_lookup(self.word_embedding_table, word_inputs1)
			word_embed2 = tf.nn.embedding_lookup(self.word_embedding_table, word_inputs2)
			word_embed3 = tf.nn.embedding_lookup(self.word_embedding_table, word_inputs3)
			word_embed4 = tf.nn.embedding_lookup(self.word_embedding_table, word_inputs4)

			word_embed = tf.concat([word_embed1, word_embed2, word_embed3, word_embed4], axis=-1)
			word_embed = tf.nn.dropout(word_embed, self.dropout)

		with tf.variable_scope("pumsa_embedding", reuse=tf.AUTO_REUSE), tf.device('/cpu:0'):
			self.pumsa_embedding_table = tf.get_variable(
				name="pumsa_embedding_table",
				shape=[len(self.pumsa2idx), config.pumsa_dim],
				initializer=self.initializer)
			pumsa_embed1 = tf.nn.embedding_lookup(self.pumsa_embedding_table, pumsa_inputs1)
			pumsa_embed2 = tf.nn.embedding_lookup(self.pumsa_embedding_table, pumsa_inputs2)
			pumsa_embed3 = tf.nn.embedding_lookup(self.pumsa_embedding_table, pumsa_inputs3)
			pumsa_embed4 = tf.nn.embedding_lookup(self.pumsa_embedding_table, pumsa_inputs4)

			pumsa_embed = tf.concat([pumsa_embed1, pumsa_embed2, pumsa_embed3, pumsa_embed4], axis=-1)
			pumsa_embed = tf.nn.dropout(pumsa_embed, self.dropout)

		with tf.variable_scope("char_embedding", reuse=tf.AUTO_REUSE), tf.device('/cpu:0'):
			self.char_embedding_table = tf.get_variable(
				name="char_embedding_table",
				shape=[len(self.char2idx), config.char_dim],
				initializer=self.initializer)

			char_embed = tf.nn.embedding_lookup(self.char_embedding_table, char_inputs)
			char_shape = tf.shape(char_embed)
			char_embeddings = tf.reshape(char_embed, shape=[-1, char_shape[-2], config.char_dim])
			char_length = tf.reshape(self.char_length, shape=[-1])

			char_cell_fw = tf.contrib.rnn.LSTMCell(config.char_lstm_dim, state_is_tuple=True,
												   initializer=self.initializer)
			char_cell_bw = tf.contrib.rnn.LSTMCell(config.char_lstm_dim, state_is_tuple=True,
												   initializer=self.initializer)
			_, ((_, char_output_fw), (_, char_output_bw)) = tf.nn.bidirectional_dynamic_rnn(char_cell_fw,
																							char_cell_bw,
																							char_embeddings,
																							sequence_length=char_length,
																							dtype=tf.float32)

			output = tf.concat([char_output_fw, char_output_bw], axis=-1)
			LSTM_char_embed = tf.reshape(output, shape=[-1, char_shape[1], 2 * config.char_lstm_dim])
			LSTM_char_embed = tf.nn.dropout(LSTM_char_embed, self.dropout)

		with tf.variable_scope("predicate_embedding"), tf.device('/cpu:0'):
			predicate_word_embedding1 = tf.nn.embedding_lookup(self.word_embedding_table, self.predicate_words1)
			predicate_word_embedding2 = tf.nn.embedding_lookup(self.word_embedding_table, self.predicate_words2)

			predicate_word_embedding = tf.concat([predicate_word_embedding1, predicate_word_embedding2], axis=-1)
			predicate_word_embedding = tf.nn.dropout(predicate_word_embedding, self.dropout)

			predicate_pumsa_embedding1 = tf.nn.embedding_lookup(self.pumsa_embedding_table, self.predicate_pumsas1)
			predicate_pumsa_embedding2 = tf.nn.embedding_lookup(self.pumsa_embedding_table, self.predicate_pumsas2)

			predicate_pumsa_embedding = tf.concat([predicate_pumsa_embedding1, predicate_pumsa_embedding2], axis=-1)
			predicate_pumsa_embedding = tf.nn.dropout(predicate_pumsa_embedding, self.dropout)

		word_embed = tf.concat([word_embed, pumsa_embed, LSTM_char_embed,
								predicate_word_embedding, predicate_pumsa_embedding], axis=-1)

		# word_embed = tf.concat([word_embed, pumsa_embed, LSTM_char_embed,
		# 						predicate_word_embedding1, predicate_word_embedding2,
		# 						predicate_pumsa_embedding1, predicate_pumsa_embedding2], axis=-1)

		return word_embed, char_embed

	def get_positioning_encoding(self, input_embedding):
		position_encoding_mat = self.position_encoding(config.max_char_length, config.char_dim)
		position_encoded = tf.reduce_sum(input_embedding * position_encoding_mat, 2)
		return position_encoded

	def position_encoding(self, sentence_size, embedding_size):
		encoding = np.ones((embedding_size, sentence_size), dtype=np.float32)
		ls = sentence_size+1
		le = embedding_size+1
		for i in range(1, le):
			for j in range(1, ls):
				encoding[i-1, j-1] = (i - (le-1)/2) * (j - (ls-1)/2)
		encoding = 1 + 4 * encoding / embedding_size / sentence_size
		return np.transpose(encoding)

	def run_step(self, sess, ELMo_context, ELMo_ids, is_train, batch):
		feed_dict = self.create_feed_dict(sess, ELMo_context, ELMo_ids, is_train, batch)

		if is_train:
			global_step, loss, _, summary = sess.run(
				[self.global_step, self.loss, self.train_op, self.merge],
				feed_dict
			)
			return global_step, loss, summary
		else:
			lengths, logits = sess.run([self.word_lengths, self.logits],
										feed_dict
									    )
			return lengths, logits


	def create_feed_dict(self, sess, ELMo_context, ELMo_ids, is_train, batch):
                words1, words2, words3, words4, pumsas1, pumsas2, pumsas3, pumsas4, \
                ELMo_inputs, w1_idxs, w2_idxs, chars, labels, lemmas, predicate_idxs, predicate_boolean, \
                predicate_words1, predicate_words2, predicate_pumsas1, predicate_pumsas2, predicate_distances, role_inputs, _ ,word_bert1= batch

                char_length = get_word_length(chars, self.char2idx["<PAD>"])

		# get ELMo embeddings
                if config.ELMo:
                        w1_ELMo_contexts, w2_ELMo_contexts = self.get_ELMo_embeddings(sess, ELMo_context, ELMo_ids, ELMo_inputs, w1_idxs, w2_idxs)

                words1_nparray = np.array(words1)
                words1_num = words1_nparray.shape[1]
                word_bert1_ex = np.array(word_bert1)
                word_bert1_expand = np.expand_dims(word_bert1_ex, axis=1)
                for i in range(words1_num-1):
                    word_bert1_expand = np.append(word_bert1_expand, np.expand_dims(np.array(word_bert1), axis=1), axis=1)


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
                        self.char_length: char_length,
                        self.predicate_words1: np.array(predicate_words1),
                        self.predicate_words2: np.array(predicate_words2),
                        self.predicate_pumsas1: np.array(predicate_pumsas1),
                        self.predicate_pumsas2: np.array(predicate_pumsas2),
                        self.input_lemma: np.array(lemmas),
                        self.binary_vector: np.array(predicate_boolean),
                        self.input_roles: np.array(role_inputs),
                        self.predicate_distances: np.array(predicate_distances),
                        self.predicate_idxs: np.array(predicate_idxs),
                        self.word_berts1: np.array(word_bert1_expand)
                }

                if config.ELMo:
                        feed_dict[self.ELMo_input1] = np.array(w1_ELMo_contexts)
                        feed_dict[self.ELMo_input2] = np.array(w2_ELMo_contexts)
                if is_train:
                        feed_dict[self.labels] = np.asarray(labels)
                        feed_dict[self.dropout] = config.dropout

                return feed_dict

	def get_ELMo_embeddings(self, sess, ELMo_context, ELMo_ids, ELMo_inputs, w1_idxs, w2_idxs):
		ELMo_context_input = sess.run(
			[ELMo_context['weighted_op']],
			feed_dict={ELMo_ids: ELMo_inputs}
		)

		ELMo_context_input = ELMo_context_input[0]
		w1_ELMo_contexts, w2_ELMo_contexts = [], []
		max_morph_length = max([len(m) for m in w2_idxs])
		for batch_idx in range(len(w1_idxs)):
			w1_ELMo_context, w2_ELMo_context = [], []
			for w_idx, _ in enumerate(w1_idxs[batch_idx]):
				w1_idx = w1_idxs[batch_idx][w_idx]
				w2_idx = w2_idxs[batch_idx][w_idx]

				w1_ELMo_context.append(ELMo_context_input[batch_idx][w1_idx])
				w2_ELMo_context.append(ELMo_context_input[batch_idx][w2_idx])

			if len(w1_ELMo_context) < max_morph_length:
				for _ in range(max_morph_length - len(w1_ELMo_context)):
					w1_ELMo_context.append(np.zeros(config.ELMo_dim, dtype=float))
					w2_ELMo_context.append(np.zeros(config.ELMo_dim, dtype=float))
			w1_ELMo_contexts.append(w1_ELMo_context)
			w2_ELMo_contexts.append(w2_ELMo_context)

		return w1_ELMo_contexts, w2_ELMo_contexts

	def evaluate_crf_model(self, sess, data_manager, ELMo_context, ELMo_ids, idx2label):
		results = []
		trans = self.trans.eval(session=sess)
		for batch in data_manager.iter_batch():
			tags = batch[12]
			lengths, scores = self.run_step(sess, ELMo_context, ELMo_ids, False, batch)
			batch_paths = self.decode(scores, lengths, trans)
			for i in range(len(tags)):
				result = []
				gold = [idx2label[int(x)] for x in tags[i][:lengths[i]]]
				pred = [idx2label[int(x)] for x in batch_paths[i][:lengths[i]]]

				for gold, pred in zip(gold, pred):
					result.append(" ".join([gold, pred]))
				results.append(result)

		return results

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
		start = np.asarray([[small]*len(self.label2idx) +[0]])
		for score, length in zip(logits, lengths):
			score = score[:length]
			pad = small * np.ones([length, 1])
			logits = np.concatenate([score, pad], axis=1)
			logits = np.concatenate([start, logits], axis=0)
			path, _ = viterbi_decode(logits, matrix)
			paths.append(path[1:])
		return paths






