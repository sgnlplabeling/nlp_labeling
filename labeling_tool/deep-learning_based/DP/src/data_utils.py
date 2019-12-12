#-*- coding: utf-8 -*-
from config import Config

import numpy as np
import random


config=Config()

class CoNLLDataset(object):
	def __len__(self):
		if self.length is None:
			self.length = 0
			for _ in self:
				self.length += 1

		return self.length

	def __init__(self, filename, word2idx, pumsa2idx, rel2idx, char2idx, shuffle):
		self.filename = filename
		self.word2idx = word2idx
		self.pumsa2idx = pumsa2idx
		self.rel2idx = rel2idx
		self.char2idx = char2idx

		self.shuffle = shuffle
		self.length = None

	def __iter__(self):
		n_iter = 0
		with open(self.filename, 'r') as f:
			M, H, words, chars, pumsas, rels, eojeols, sentences = [], [], [], [], [], [], [], []

			lines = f.read().strip().split("\n\n")
			if self.shuffle == True and n_iter == 0:
				random.shuffle(lines)

			for line_idx, line in enumerate(lines):
				for l_idx, l in enumerate(line.split("\n")):
					l = l.strip()

					if l[0] == ";":
						sentences.append(l)
						continue

					# Root
					if M == []:
						M.append(0)
						H.append(0)
						rels.append(self.rel2idx["$ROOT$"])
						pumsas.append([self.pumsa2idx["$ROOT$"]])
						words.append([self.word2idx["$ROOT$"]])
						chars.append([self.char2idx["$ROOT$"]])

					m, h, rel, eojeol = l.split()

					eojeols.append(eojeol)
					M.append(int(m))
					H.append(int(h))

					rels.append(self.rel2idx[rel])
					eojeol = eojeol.split("|")

					char = ""
					word_list, char_list, pumsa_list = [], [], []

					for e in eojeol:
						word_list.append(self.word2idx[e] if e in self.word2idx else self.word2idx["$UNK$"])
						pumsa_list.append(self.pumsa2idx[e[e.rfind('/') + 1:]] if e[e.rfind('/') + 1:] in self.pumsa2idx else self.pumsa2idx["$UNK$"])
						char += e[:e.rfind('/')]

					for c in char:
						char_list.append(self.char2idx[c] if c in self.char2idx else self.char2idx["$UNK$"])

					words.append(word_list)
					pumsas.append(pumsa_list)
					chars.append(char_list)

					if l_idx == len(line.split('\n'))-1:
						if len(M) != 0:
							n_iter += 1

							if config.max_iter is not None and n_iter > config.max_iter:
								break

							if M == []:
								continue

							H[-1] = 0
							yield M, H, words, chars, pumsas, rels, sentences, eojeols
							M, H, words, pumsas, chars, pos, rels, sentences, eojeols \
								= [], [], [], [], [], [], [], [], []


def load_vocab(filename):
	vocab = {"$ROOT$":0, "$UNK$":1, "$PAD$":2}

	with open(filename, "rb") as f:
		lines = f.readlines()
		for idx, word in enumerate(lines):
			word = word.decode()
			word = word.split("\t")[0].strip()
			if word not in vocab:
				vocab[word] = len(vocab)

	return vocab

def load_word_embeddings(word2idx):
	print("Loading Pre-trained Embedding Model and merging with current dict")
	glove_dict = {}
	size = config.word_dim
	cnt = 0

	with open(config.embedding_filename, 'r', encoding="euc-kr", errors='ignore') as f:
		for index, line in enumerate(f.read().split("\n")):
			if line.strip():
				word_and_embedding = line.strip().split('\t', 1)
				word = word_and_embedding[0].split()[0]
				embedding = np.array([a for a in word_and_embedding[0].split()[-size:]])
				glove_dict[word] = embedding

	np.random.seed(0)
	embedding_matrix = np.random.rand(len(word2idx), size) #/ np.sqrt(50)
	for key, value in word2idx.items():
		word_vocab = key
		word_index = value
		word_vector = glove_dict.get(word_vocab, None)
		if word_vector is not None:
			cnt += 1
			embedding_matrix[word_index] = word_vector

	pad_index = word2idx['$PAD$']
	embedding_matrix[pad_index] = np.zeros(size)

	print("%s / %s" % (len(word2idx), cnt))
	return embedding_matrix

def pad_sequences(raw_sequence, level, pad_token=0):
	paded_sequence, sequence_length = [], []

	max_seq_len = max([len(rs) for rs in raw_sequence])
	if level=="arc":
		for seq in raw_sequence:
			seq = seq + [pad_token] * max(max_seq_len - len(seq), 0)
			paded_sequence.append(seq)
	elif level=="rel":
		for seq in raw_sequence:
			sequence_length.append(len(seq))
			seq = seq + [pad_token] * max(max_seq_len - len(seq), 0)
			paded_sequence.append(seq)
	elif level=="seq":
		pad = [pad_token] * config.word_length
		for seq in raw_sequence:
			words = []
			length = []
			for char in seq:
				length += [min(len(char), config.word_length)]
				char = char + [pad_token] * max(config.word_length - len(char), 0)
				if len(char) > config.word_length:
					char = char[:config.word_length]
				words += [char]

			len_words = len(words)
			for _ in range(max_seq_len-len_words):
				words.append(pad)
				length.append(0)

			paded_sequence.append(words)
			sequence_length.append(length)

	return paded_sequence, sequence_length

def minibatchs(data, miniBatch_size):
	M_batch, H_batch, words_batch, chars_batch, pumsas_batch, rels_batch, sentences_batch, eojeol_batch = [], [], [], [], [], [], [], []

	for (M, H, words, chars, pumsas, rels, sentences, eojeol) in data:
		if len(M_batch) == miniBatch_size:
			yield M_batch, H_batch, words_batch, chars_batch, pumsas_batch, rels_batch, sentences_batch, eojeol_batch
			M_batch, H_batch, words_batch, chars_batch, pumsas_batch, rels_batch, sentences_batch, eojeol_batch = [], [], [], [], [], [], [], []

		if len(M_batch) > config.seq_length:
			print ("sentence len  : %s pass" % len(M_batch))

		eojeol_batch += [eojeol]
		M_batch += [M]
		H_batch += [H]
		pumsas_batch += [pumsas]
		words_batch += [words]
		chars_batch += [chars]
		rels_batch += [rels]
		sentences_batch += [sentences]

	if len(M_batch) != 0:
		yield M_batch, H_batch, words_batch, chars_batch, pumsas_batch, rels_batch, sentences_batch, eojeol_batch
