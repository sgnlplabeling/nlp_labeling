import numpy as np
import os
import tensorflow as tf

from data_utils import minibatchs, pad_sequences
from general_utils import Progbar

from config import Config
config = Config()
#-*- coding: utf-8 -*-

# from TDNN import TDNN
class BiAffineModel(object):
	def __init__(self, default_NNLM, pos_embedding, word2idx, pumsa2idx, rel2idx, char2idx):
		self.mode = ""
		self.default_NNLM = default_NNLM
		self.pos_embedding = pos_embedding

		self.word2idx = word2idx
		self.pumsa2idx = pumsa2idx
		self.rel2idx = rel2idx
		self.char2idx = char2idx

		self.idx2word = {v: k for k, v in self.word2idx.items()}
		self.idx2rel = {v: k for k, v in self.rel2idx.items()}
		self.initiailizer = tf.orthogonal_initializer()

	def add_placeholders(self):
		self.words = tf.placeholder(tf.int32, [None, None, None],
									name="words")
		self.pumsas = tf.placeholder(tf.int32, [None, None, None],
								  name="pumsas")
		self.chars = tf.placeholder(tf.int32, [None, None, None],
									name="chars")


		self.H_ids = tf.placeholder(tf.int32, shape=[None, None],
									name="H_ids")
		self.rel_ids = tf.placeholder(tf.int32, shape=[None, None],
									name="rel_ids")


		self.sequence_lengths = tf.placeholder(tf.int32, shape=[None],
							name="sequence_lengths")
		self.word_lengths = tf.placeholder(tf.int32, shape=[None, None],
							name="word_lengths")
		self.char_lengths = tf.placeholder(tf.int32, shape=[None, None],
										   name="char_lengths")

		# hyper parameters
		self.dropout = tf.placeholder(dtype=tf.float32, shape=[],
							name="dropout")
		self.lr = tf.placeholder(dtype=tf.float32, shape=[],
							name="lr")

	def get_feed_dict(self, M_batch, H_batch, words_batch, chars_batch, pumsas_batch, rels_batch, isTrain=True):
		M, _ = pad_sequences(M_batch, level="arc", pad_token=self.word2idx["$PAD$"])
		H, _ = pad_sequences(H_batch, level="arc", pad_token=config.H_PAD)

		RELS, sequence_lengths = pad_sequences(rels_batch, level="rel", pad_token=self.rel2idx["$PAD$"])
		PUMSA, _=  pad_sequences(pumsas_batch, level="seq", pad_token=self.pumsa2idx["$PAD$"])
		WORDS, word_lengths = pad_sequences(words_batch, level="seq", pad_token=self.word2idx["$PAD$"])
		CHARS, char_lengths = pad_sequences(chars_batch, level="seq", pad_token=self.char2idx["$PAD$"])

		feed = {
			self.pumsas: PUMSA,
			self.words : WORDS,
			self.chars : CHARS,
			self.char_lengths: char_lengths,
			self.word_lengths: word_lengths,
			self.sequence_lengths: sequence_lengths,
			self.dropout : config.dropout,
			self.H_ids : H,
			self.rel_ids : RELS,
			self.lr : config.lr
		}

		if isTrain :
			pass
			# feed[self.rel_ids] = RELS
			# feed[self.H_ids] = H
		else:
			feed[self.dropout] = 1.0

		return feed, sequence_lengths

	def embedding_layer(self):
		with tf.variable_scope("words"):
			word_shape = tf.shape(self.words)
			word_lengths = tf.reshape(self.word_lengths, shape=[-1])

			if config.pretrained_word_embedding == True:
				word_table = tf.Variable(self.default_NNLM, name="word_table", dtype=tf.float32, trainable=False)
			else:
				word_table = tf.get_variable(name = "word_table", shape=[len(self.word2idx), config.word_dim],  dtype=tf.float32)

			pumsa_table = tf.get_variable(name = "pumsa_table", shape=[len(self.pumsa2idx), config.pumsa_dim], dtype=tf.float32)

			word_emb = tf.nn.embedding_lookup(word_table, self.words, name="word_emb")
			# word_emb = tf.nn.dropout(word_emb, config.dropout)

			pumsa_emb = tf.nn.embedding_lookup(pumsa_table, self.pumsas, name="pos_emb")
			# pumsa_emb = tf.nn.dropout(pumsa_emb, config.dropout)

			word_emb = tf.concat([word_emb, pumsa_emb], axis=-1)
			word_emb = tf.reshape(word_emb, shape=[-1, word_shape[2], config.word_dim+config.pumsa_dim])

			word_cell_fw = tf.contrib.rnn.LSTMCell((config.word_dim+config.pumsa_dim)/2,
												   state_is_tuple=True)
			word_cell_bw = tf.contrib.rnn.LSTMCell((config.word_dim+config.pumsa_dim)/2,
												   state_is_tuple=True)

			_, ((_, word_output_fw), (_, word_output_bw)) = tf.nn.bidirectional_dynamic_rnn(word_cell_fw,
																							word_cell_bw,
																							word_emb,
																							sequence_length=word_lengths,
																							dtype=tf.float32)
			word_output = tf.concat([word_output_fw, word_output_bw], axis=-1)
			word_output = tf.reshape(word_output, shape=[-1, word_shape[1], config.word_dim+config.pumsa_dim])
			# self.input_emb = tf.nn.dropout(word_output, self.dropout)

		with tf.variable_scope("chars"):
			char_lengths = tf.reshape(self.char_lengths, shape=[-1])
			char_table = tf.get_variable(shape=[len(self.char2idx), int(config.char_dim)], name="char_table",
										dtype=tf.float32)
			char_emb = tf.nn.embedding_lookup(char_table, self.chars, name="char_embeddings")
			char_shape = tf.shape(char_emb)
			# char_emb = tf.nn.dropout(char_emb, config.dropout)
			char_emb = tf.reshape(char_emb, shape=[-1, char_shape[-2], config.char_dim])



			char_cell_fw = tf.contrib.rnn.LSTMCell(config.char_hidden,
												   state_is_tuple=True)
			char_cell_bw = tf.contrib.rnn.LSTMCell(config.char_hidden,
												   state_is_tuple=True)

			_, ((_, char_output_fw), (_, char_output_bw)) = tf.nn.bidirectional_dynamic_rnn(char_cell_fw,
																							char_cell_bw,
																							char_emb,
																							sequence_length=char_lengths,
																							dtype=tf.float32)
			char_output = tf.concat([char_output_fw, char_output_bw], axis=-1)
			char_output = tf.reshape(char_output, shape=[-1, char_shape[1], 2 * config.char_hidden])
			# char_output = tf.nn.dropout(char_output, self.dropout)
			self.input_emb = tf.concat([word_output, char_output], axis=-1)

	def bilstm_layer(self, inputs, sequence_length, num_units):
		cell = tf.contrib.rnn.LSTMCell
		cell_fw = cell(num_units, state_is_tuple=True)
		cell_bw = cell(num_units, state_is_tuple=True)
		_, ((_, output_fw), (_, output_bw)) = tf.nn.bidirectional_dynamic_rnn(
			cell_fw, cell_bw,
			inputs, sequence_length=sequence_length,
			dtype=tf.float32)
		final_states = tf.concat([output_fw, output_bw], axis=-1)
		return final_states

	def add_logits_op(self):
		self.batch_size = tf.shape(self.input_emb)[0]
		self.seq_length = tf.shape(self.input_emb)[1]

		with tf.variable_scope("stacked-bi-lstm"):
			cell = tf.contrib.rnn.LSTMCell
			cells_fw = [cell(config.hidden_size) for _ in range(config.num_layer)]
			cells_bw = [cell(config.hidden_size) for _ in range(config.num_layer)]

			cells_fw = [tf.nn.rnn_cell.DropoutWrapper(cell, input_keep_prob=self.dropout, state_keep_prob=self.dropout) for cell in cells_fw]
			cells_bw = [tf.nn.rnn_cell.DropoutWrapper(cell, input_keep_prob=self.dropout, state_keep_prob=self.dropout) for cell in cells_bw]

			output, _, _ = tf.contrib.rnn.stack_bidirectional_dynamic_rnn(
				cells_fw=cells_fw,
				cells_bw=cells_bw,
				inputs=self.input_emb,
				sequence_length=self.sequence_lengths,
				dtype=tf.float32)
			output = tf.reshape(output, [-1, 2 * config.hidden_size])

		with tf.variable_scope("MLP"):
			arc_dep = self.MLP(output, "arc_dep")
			arc_head = self.MLP(output, "arc_head")

			rel_dep = self.MLP(output, "rel_dep")
			rel_head = self.MLP(output, "rel_head")

			arc_dep = tf.reshape(
				arc_dep, [self.batch_size, -1, config.arc_mlp_size])
			arc_head = tf.reshape(
				arc_head, [self.batch_size, -1, config.arc_mlp_size])
			rel_dep = tf.reshape(
				rel_dep, [self.batch_size, -1, config.arc_mlp_size])
			rel_head = tf.reshape(
				rel_head, [self.batch_size, -1, config.arc_mlp_size])


		with tf.variable_scope("Bi-Affine"):
			with tf.variable_scope("Arc"):
				U_arc = tf.get_variable("U_arc1", shape=[config.arc_mlp_size + 1, 1, config.arc_mlp_size],
										dtype=tf.float32, initializer=self.initiailizer)

				arc_dep = tf.concat([arc_dep, tf.ones(shape=[self.batch_size, self.seq_length, 1])], axis=-1)
				arc_dep = tf.reshape(arc_dep, [self.batch_size, self.seq_length, -1])
				arc_head = tf.reshape(arc_head, [self.batch_size, self.seq_length, -1])

				arc_lin = tf.matmul(tf.reshape(arc_dep, shape=[-1, config.arc_mlp_size+1]),
								tf.reshape(U_arc, shape=[config.arc_mlp_size+1, -1]))
				arc_bilin = tf.matmul(tf.reshape(arc_lin, tf.stack([self.batch_size, self.seq_length*1, config.arc_mlp_size])),
								  arc_head, transpose_b=True)
				arc_logits1 = tf.reshape(arc_bilin, tf.stack([self.batch_size, self.seq_length, -1]))

				rel_dep = tf.concat([rel_dep, tf.ones(shape=[self.batch_size, self.seq_length, 1])], axis=-1)
				rel_dep = tf.reshape(rel_dep, [self.batch_size, self.seq_length, -1])

				# U_arc2 = tf.get_variable("U_arc2", shape=[config.arc_mlp_size + 1, 1, config.arc_mlp_size],
				# 						dtype=tf.float32, initializer=self.initiailizer)
				# arc_lin2 = tf.matmul(tf.reshape(rel_dep, shape=[-1, config.arc_mlp_size + 1]),
				# 					tf.reshape(U_arc2, shape=[config.arc_mlp_size + 1, -1]))
				# arc_bilin2 = tf.matmul(tf.reshape(arc_lin2, tf.stack([self.batch_size, self.seq_length * 1, config.arc_mlp_size])),
				# 					  arc_head, transpose_b=True)
				# arc_logits2 = tf.reshape(arc_bilin2, tf.stack([self.batch_size, self.seq_length, -1]))
				#
				rel_head = tf.concat([rel_head, tf.ones(shape=[self.batch_size, self.seq_length, 1])], axis=-1)
				rel_head = tf.reshape(rel_head, [self.batch_size, self.seq_length, -1])
				#
				# U_arc3 = tf.get_variable("U_arc3", shape=[config.arc_mlp_size + 1, 1, config.arc_mlp_size],
				# 						 dtype=tf.float32, initializer=self.initiailizer)
				# arc_lin3 = tf.matmul(tf.reshape(rel_head, shape=[-1, config.arc_mlp_size + 1]),
				# 					 tf.reshape(U_arc3, shape=[config.arc_mlp_size + 1, -1]))
				# arc_bilin3 = tf.matmul(
				# 	tf.reshape(arc_lin3, tf.stack([self.batch_size, self.seq_length * 1, config.arc_mlp_size])),
				# 	arc_head, transpose_b=True)
				# arc_logits3 = tf.reshape(arc_bilin3, tf.stack([self.batch_size, self.seq_length, -1]))

				# self.arc_logits = tf.add(
				# 	tf.divide(arc_logits1, 3),
				# 	tf.divide(arc_logits2, 3) + tf.divide(arc_logits3, 3),
				# 	name='arc_logits')
				self.arc_logits = arc_logits1
				arc_preds = tf.to_int32(tf.argmax(self.arc_logits, axis=-1))

			with tf.variable_scope("Rel"):
				U_rel = tf.get_variable("U_rel",
										shape=[config.arc_mlp_size + 1, len(self.rel2idx), config.arc_mlp_size+1],
										dtype=tf.float32, initializer=self.initiailizer)

				rel_lin = tf.matmul(tf.reshape(rel_dep, shape=[-1, config.arc_mlp_size+1]),
								tf.reshape(U_rel, shape=[config.arc_mlp_size+1, -1]))
				rel_lin = tf.reshape(rel_lin, tf.stack([self.batch_size, self.seq_length * len(self.rel2idx), config.arc_mlp_size+1]))
				rel_bilin = tf.matmul(rel_lin, rel_head, transpose_b=True)
				rel_logits = tf.reshape(rel_bilin, tf.stack([self.batch_size, self.seq_length, -1, self.seq_length]))

				# if Train mode
				mask = tf.cast(tf.not_equal(self.H_ids, config.H_PAD), dtype=tf.int32)
				H_ids = tf.multiply(self.H_ids, mask)

				one_hot = tf.one_hot(H_ids, self.seq_length)
				one_hot = tf.expand_dims(one_hot, axis=3)

				self.rel_logits = tf.matmul(rel_logits, one_hot)
				self.rel_logits = tf.reshape(self.rel_logits, [self.batch_size, self.seq_length, len(self.rel2idx)])

				# if eval mode
				one_hot = tf.one_hot(arc_preds, self.seq_length)
				one_hot = tf.expand_dims(one_hot, axis=3)

				select_rel_logits = tf.matmul(rel_logits, one_hot)
				self.select_rel_logits = tf.squeeze(select_rel_logits, axis=3)

	def add_loss_op(self):
		max_len = tf.reduce_max(self.sequence_lengths)
		mask = tf.sequence_mask(self.sequence_lengths)

		self.H_onehot = tf.one_hot(self.H_ids, max_len)
		self.rel_onehot = tf.one_hot(self.rel_ids, len(self.rel2idx))

		self.rel_loss = tf.nn.softmax_cross_entropy_with_logits_v2(logits=self.rel_logits, labels=self.rel_onehot)
		self.arc_loss =  tf.nn.softmax_cross_entropy_with_logits_v2(logits=self.arc_logits, labels=self.H_onehot)

		self.rel_loss = tf.boolean_mask(self.rel_loss[:, 1:], mask[:, 1:])
		self.arc_loss = tf.boolean_mask(self.arc_loss[:, 1:], mask[:, 1:])

		self.rel_loss = tf.reduce_mean(self.rel_loss)
		self.arc_loss = tf.reduce_mean(self.arc_loss)

		self.loss = self.arc_loss + self.rel_loss
		tf.summary.scalar("arc_loss", self.arc_loss)

		with tf.variable_scope('uas'):
			sequence_mask = tf.sequence_mask(self.sequence_lengths)
			self.head_preds = tf.argmax(self.arc_logits, axis=-1, output_type=tf.int32)
			self.masked_head_preds = tf.boolean_mask(self.head_preds[:, 1:], sequence_mask[:, 1:])

			masked_head_ids = tf.boolean_mask(
				self.H_ids[:, 1:], sequence_mask[:, 1:])
			head_correct = tf.equal(self.masked_head_preds, masked_head_ids)

			self.uas = tf.reduce_mean(tf.cast(head_correct, tf.float32))

		with tf.variable_scope('las'):
			self.rel_preds = tf.argmax(self.rel_logits, axis=-1, output_type=tf.int32)
			masked_rel_ids = tf.boolean_mask(
				self.rel_ids[:, 1:], sequence_mask[:, 1:])
			self.masked_rel_preds = tf.boolean_mask(self.rel_preds[:, 1:], sequence_mask[:, 1:])

			rel_correct = tf.equal(self.masked_rel_preds, masked_rel_ids)
			head_rel_correct = tf.logical_and(head_correct, rel_correct)

			self.las = tf.reduce_mean(tf.cast(head_rel_correct, tf.float32))

	def add_train_op(self):
		with tf.variable_scope("train_step"):
			optimizer = tf.train.AdamOptimizer(self.lr, beta2=config.decay_factor)
			self.train_op = optimizer.minimize(self.loss)

	def add_init_op(self):
		self.init = tf.global_variables_initializer()

	def add_summary(self, sess):
		self.merged = tf.summary.merge_all()
		self.file_writer = tf.summary.FileWriter(config.summary, sess.graph)

	def build(self):
		self.add_placeholders()
		self.embedding_layer()
		self.add_logits_op()
		self.add_loss_op()
		self.add_train_op()
		self.add_init_op()

	def evaluate_batch(self, sess, M_batch, H_batch, words_batch, chars_batch, pumsas_batch, rels_batch):
		fd, sequence_lengths = self.get_feed_dict(M_batch, H_batch, words_batch, chars_batch, pumsas_batch,
									   rels_batch, isTrain = False)

		uas, las = sess.run([self.uas, self.las], feed_dict=fd)

		return uas, las

	def predict_batch(self, sess, M_batch, H_batch, words_batch, chars_batch, pumsas_batch, rels_batch):
		fd, sequence_lengths = self.get_feed_dict(M_batch, H_batch, words_batch, chars_batch, pumsas_batch,
									   rels_batch, isTrain = False)

		arc_pred, select_rel_logits = sess.run([self.arc_logits, self.select_rel_logits], feed_dict=fd)

		return arc_pred, select_rel_logits, sequence_lengths


	def run_epoch(self, sess, train, dev, epoch):
		nbatches = (len(train) + config.batch_size - 1) // config.batch_size
		prog = Progbar(target=nbatches)
		for batch_idx, (M_batch, H_batch, words_batch, chars_batch, pumsas_batch, rels_batch, sentences_batch, eojeol_batch) \
				in enumerate(minibatchs(train, config.batch_size)):


			fd, _ = self.get_feed_dict(M_batch, H_batch, words_batch, chars_batch, pumsas_batch, rels_batch)
			_, train_loss, summary = sess.run([self.train_op, self.loss, self.merged], feed_dict=fd)

			# if batch_idx == 10:
			# 	break

			prog.update(batch_idx + 1, [("train loss ", train_loss)])

		self.mode = "test"
		UAS, LAS = self.run_evaluate(sess, dev)
		self.mode = "train"

		return UAS, LAS

	def run_evaluate(self, sess, test):
		total_uas = []
		total_las = []
		for (M_batch, H_batch, words_batch, chars_batch, pumsas_batch, rels_batch, sentences_batch, eojeol_batch) in minibatchs(test, config.batch_size):
			uas, las = self.evaluate_batch(sess, M_batch, H_batch, words_batch, chars_batch, pumsas_batch, rels_batch)
			total_uas.append(uas)
			total_las.append(las)

		print("new uas %s, las: %s"%(np.mean(total_uas), np.mean(total_las)))
		print(config.ckpt_path)
		return  np.mean(total_uas), np.mean(total_las)

	def train(self, train, dev):
		best_score, best_LAS = 0, 0
		nepoch_no_imprv = 0

		session_conf = tf.ConfigProto(allow_soft_placement=True)
		session_conf.gpu_options.allow_growth = True
		sess = tf.Session(config=session_conf)
		saver = tf.train.Saver()

		if config.restart:
			saver.restore(sess, config.ckpt_path)
		else:
			sess.run(self.init)

		self.add_summary(sess)

		for epoch in range(config.nepochs):
			print ("Epoch {:} out of {:}".format(epoch + 1, config.nepochs))
			UAS, LAS = self.run_epoch(sess, train, dev, epoch)

			# early stopping and saving best parameters
			if UAS >= best_score:
				saver.save(sess, config.ckpt_path)
				nepoch_no_imprv = 0
				if not os.path.exists(config.ckpt_path):
					os.makedirs(config.ckpt_path)
				saver.save(sess, config.ckpt_path)

				best_score = UAS
				best_LAS = LAS
				print("- new best score!")
				print("- Writing...")

			else:
				nepoch_no_imprv += 1
				if nepoch_no_imprv >= config.nepoch_no_imprv:
					print("- early stopping {} epochs without improvement".format(nepoch_no_imprv))
					break

		print("- final best score! : %s, %s" % (best_score, best_LAS))


	def MLP(self, input, scope):
		if "arc" in scope:
			output_dim = config.arc_mlp_size
		elif "rel" in scope:
			output_dim = config.rel_mlp_size

		input = tf.reshape(input, [-1, 2 * config.hidden_size])
		weights = {
			'%s_w1'%scope: tf.get_variable('%s_w1'%scope, shape=[2*config.hidden_size, output_dim], dtype=tf.float32),
			'%s_w2'%scope: tf.get_variable('%s_w2'%scope, shape=[output_dim, config.arc_mlp_size], dtype=tf.float32)
		}
		biases = {
			'%s_b1'%scope: tf.get_variable('%s_b1'%scope, shape=[output_dim], dtype=tf.float32, initializer=tf.zeros_initializer()),
			'%s_b2'%scope: tf.get_variable('%s_b2'%scope, shape=[config.arc_mlp_size], dtype=tf.float32, initializer=tf.zeros_initializer())
		}

		tmp_layer = tf.add(tf.matmul(input, weights['%s_w1'%scope]), biases['%s_b1'%scope])
		tmp_layer = tf.nn.relu(tmp_layer)
		mlp_layer = tf.add(tf.matmul(tmp_layer, weights['%s_w2'%scope]), biases['%s_b2'%scope])
		mlp_layer = tf.nn.dropout(mlp_layer, self.dropout)

		return mlp_layer

	def tagging(self, unlabeled):
		session_conf = tf.ConfigProto(allow_soft_placement=True)
		session_conf.gpu_options.allow_growth = True
		saver = tf.train.Saver()
		with tf.Session(config=session_conf) as sess:
			saver.restore(sess, config.ckpt_path)
			with open(config.tagging_file, "w") as f:
				for batch_idx, (M_batch, H_batch, words_batch, chars_batch, pumsas_batch, rels_batch, sentences_batch, eojeol_batch) in enumerate(minibatchs(unlabeled, 100)):
					arc_preds, rel_preds, sequence_lengths = self.predict_batch(sess, M_batch, H_batch, words_batch, chars_batch, pumsas_batch, rels_batch)
					for idx, (arc_pred, rel_pred, length, eojeols, sentence) in enumerate(zip(arc_preds, rel_preds, sequence_lengths, eojeol_batch, sentences_batch)):
						arc_pred = arc_pred[:length]
						rel_pred = rel_pred[:length]
						re_arc_pred = [a_pred[:length] for a_pred in arc_pred]
						re_rel_pred = [r_pred[:length] for r_pred in rel_pred]

						arc_pred_max = np.argmax(re_arc_pred, axis=-1)
						rel_pred_max = np.argmax(re_rel_pred, axis=-1)

						f.write(sentence[0] + "\n")
						for M, (a_pred_max, r_pred_max, a_pred, r_pred, eojeol) in enumerate(zip(arc_pred_max, rel_pred_max, arc_pred, rel_pred, eojeols)):
							if M == 0: continue
							if M == len(arc_pred_max)-1:
								a_pred_max = 0
							f.write(str(M)+"\t"+str(a_pred_max)+"\t"+self.idx2rel[r_pred_max]+"\t"+eojeol+"\n")
						f.write("\n")