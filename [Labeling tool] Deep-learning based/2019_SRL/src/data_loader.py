import numpy as np
import tensorflow as tf

from config import Config
from ELMo.ELMo_model import BidirectionalLanguageModel
from ELMo.ELMo import weight_layers

config = Config()

def load_data(data_path):
	words1, words2, words3, words4, pumsas1, pumsas2, pumsas3, pumsas4, predicate_idxs, predicate_lemmas, chars, elmos, \
	predicate_words1, predicate_words2, predicate_pumsas1, predicate_pumsas2, predicate_idxs, labels, elmo_w1_idxs, elmo_w2_idxs, sentences \
		= [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], []

	with open(data_path, encoding='utf-8') as fp:
		contents = fp.read().strip()
		for line in contents.split('\n'):
			w1_idx, w2_idx = 0, 0
			word1, word2, word3, word4, pumsa1, pumsa2, pumsa3, pumsa4, char, elmo, \
			elmo_w1_idx, elmo_w2_idx = [], [], [], [], [], [], [], [], [], [], [], []

			sentence, label = line.split("|||")
			sentences.append(sentence)
			sentence = sentence.split()
			predicate_idx = int(sentence[0])
			predicate_lemma = sentence[1]
			sentence = sentence[2:]
			predicate_eojeol = sentence[predicate_idx].split("+")
			predicate_word1 = predicate_eojeol[0]
			predicate_pumsa1_idx = predicate_word1.rfind("/")
			predicate_pumsa1 = predicate_word1[predicate_pumsa1_idx+1:]
			predicate_word2 = predicate_eojeol[-1]
			predicate_pumsa2_idx = predicate_word2.rfind("/")
			predicate_pumsa2 = predicate_word2[predicate_pumsa2_idx + 1:]

			for token in sentence:
				char_string = token
				token = token.split("+")

				elmo.extend(token)
				elmo_w1_idx.append(w1_idx)
				elmo_w2_idx.append(w1_idx + (len(token) - 1))
				w1_idx += len(token)

				w1 = token[0]
				w2 = "<DUMMY>"
				w3 = "<DUMMY>"
				w4 = token[-1]

				idx1 = w1.rfind("/")
				idx4 = w4.rfind("/")
				p1 = w1[idx1 + 1:]
				p2 = "<DUMMY>"
				p3 = "<DUMMY>"
				p4 = w4[idx4 + 1:]

				if len(token) > 2:
					w2 = token[1]
					w3 = token[-2]
					idx2 = w2.rfind("/")
					idx3 = w3.rfind("/")
					p2 = w2[idx2 + 1:]
					p3 = w3[idx3 + 1:]

				word1.append(w1)
				word2.append(w2)
				word3.append(w3)
				word4.append(w4)
				pumsa1.append(p1)
				pumsa2.append(p2)
				pumsa3.append(p3)
				pumsa4.append(p4)
				char.append(char_string)

			elmos.append(elmo)
			words1.append(word1)
			words2.append(word2)
			words3.append(word3)
			words4.append(word4)
			pumsas1.append(pumsa1)
			pumsas2.append(pumsa2)
			pumsas3.append(pumsa3)
			pumsas4.append(pumsa4)
			elmo_w1_idxs.append(elmo_w1_idx)
			elmo_w2_idxs.append(elmo_w2_idx)
			chars.append(char)
			predicate_lemmas.append(predicate_lemma)
			predicate_idxs.append(predicate_idx)
			labels.append(label.split())
			predicate_words1.append(predicate_word1)
			predicate_words2.append(predicate_word2)
			predicate_pumsas1.append(predicate_pumsa1)
			predicate_pumsas2.append(predicate_pumsa2)

	return (words1, words2, words3, words4, pumsas1, pumsas2, pumsas3, pumsas4, chars, elmos, \
			predicate_lemmas, predicate_idxs, elmo_w1_idxs, elmo_w2_idxs, labels, \
			predicate_words1, predicate_words2, predicate_pumsas1, predicate_pumsas2, sentences)

def load_word_embedding_matrix(word2idx):
	print("Loading Pre-trained Embedding Model and merging it with current dict")
	embedding_dict = {}
	word_cnt = 0

	with open(config.word_emb_path, 'rb') as f:
		for idx, line in enumerate(f.readlines()):
			line = line.decode("euc-kr")

			if line.strip():
				word = line.strip().split(' ')[0]
				if word == "PADDING":
					word = "<PAD>"
				elif word == "UNK":
					word = "<UNK>"
				embedding = [v for v in line.strip().split(' ')[1:]]
				embedding = np.array(embedding)
				embedding_dict[word] = embedding

	np.random.seed(0)
	embedding_matrix = np.random.randn(len(word2idx), config.word_dim) / np.sqrt(config.word_dim)

	for k, v in word2idx.items():
		# continue
		word_vector = embedding_dict.get(k, None)
		if word_vector is not None:
			word_cnt += 1
			embedding_matrix[v] = word_vector

	pad_index = word2idx['<PAD>']
	embedding_matrix[pad_index] = np.zeros(config.word_dim)

	print("%s / %s" % (word_cnt, len(word2idx)))
	return embedding_matrix

def load_ELMo_dict():
	ELMo_dict = {}
	with open(config.ELMo_dict, "rb") as f:
		for line in f.readlines():
			line = line.decode("utf-8")
			line = line.strip()
			ELMo_dict[line] = len(ELMo_dict)

	return ELMo_dict

def load_ELMo():
	if config.ELMo:
		ELMo_dict = load_ELMo_dict()
		ELMo_model = BidirectionalLanguageModel(
			config.ELMo_options,
			config.ELMo_weights)
		ELMo_ids = tf.placeholder(tf.int32, shape=[None, None, None], name="ELMo_ids")
		context_embeddings_op = ELMo_model(ELMo_ids)
		ELMo_context = weight_layers('input', context_embeddings_op, l2_coef=0.0)
	else:
		ELMo_dict, context_embeddings_op, ELMo_context, ELMo_ids = None, None, None, None

	return ELMo_dict, context_embeddings_op, ELMo_context, ELMo_ids