import pickle as pk
import math
import random
import numpy as np

from config import Config
from data_loader import load_data

config = Config()

def get_vocab(value_list, char=False):
	return_dict = {"<PAD>":0, "<UNK>":1}
	for value in value_list:
		for v in value:
			if char:
				for c in list(v):
					if c not in return_dict:
						return_dict[c] = len(return_dict)
			else:
				if v not in return_dict:
					return_dict[v] = len(return_dict)

	return return_dict

def get_necessary():
	train_words1, train_words2, train_words3, train_words4, \
	train_pumsas1, train_pumsas2, train_pumsas3, train_pumsas4, \
	train_chars, train_elmos, train_predicate_lemmas, train_predicate_idxs, train_elmo_w1_idxs, train_elmo_w2_idxs,\
	labels, predicate_words1, predicate_word2, predicate_pumsas1, predicate_pumsas2 = load_data(config.train_path)

	test_words1, test_words2, test_words3, test_words4, \
	test_pumsas1, test_pumsas2, test_pumsas3, test_pumsas4, \
	test_chars, test_elmos, test_predicate_lemmas, test_predicate_idxs, test_elmo_w1_idxs, test_elmo_w2_idxs, \
	test_labels, test_predicate_words1, test_predicate_word2, test_predicate_pumsas1, test_predicate_pumsas2 = load_data(config.test_path)

	word2idx = get_vocab(train_words1 + train_words2 + train_words3 + train_words4 + test_words1 + test_words2 + test_words3 + test_words4)
	pumsa2idx = get_vocab(train_pumsas1 + train_pumsas2 + train_pumsas3 + train_pumsas4 + test_pumsas1 + test_pumsas2 + test_pumsas3 + test_pumsas4)
	lemma2idx = get_vocab([train_predicate_lemmas + test_predicate_lemmas])
	char2idx = get_vocab(train_chars+test_chars, char=True)
	label2idx = get_vocab(labels)
	idx2label = {v: k for k, v in label2idx.items()}
	with open(config.necessary, "wb") as f:
		pk.dump((word2idx, pumsa2idx, lemma2idx, char2idx, label2idx, idx2label), f)

	return word2idx, pumsa2idx, lemma2idx, char2idx, label2idx, idx2label

class BatchManager(object):
	def __init__(self, data, label2idx):
		if config.ELMo:
			self.bos_char = 4  # <begin sentence>
			self.eos_char = 5  # <end sentence>
			self.bow_char = 3  # <begin word>
			self.eow_char = 6  # <end word>
			self.pad_char = 0  # <padding>
			self.hanja_char = 1
			self.max_characters_per_token = 17

		self.label2idx = label2idx
		self.batch_data = self.sort_and_pad(data, config.batch_size, config.max_char_length)
		self.len_data = len(self.batch_data)

	def sort_and_pad(self, data, batch_size, max_char_length):
		num_batch = int(math.ceil(len(data) / batch_size))
		sorted_data = sorted(data, key=lambda x: len(x[0]))
		batch_data = list()
		for i in range(num_batch):
			batch_data.append(
				self.pad_data(sorted_data[i * batch_size: (i + 1) * batch_size], max_char_length))

		return batch_data

	def pad_data(self, data, max_char_length):
                batch_idx = 0
                words1, words2, words3, words4, pumsas1, pumsas2, pumsas3, pumsas4,\
                predicate_words1, predicate_words2, predicate_pumsas1, predicate_pumsas2,\
                lemmas, predicate_boolean, predicate_idxs, chars, targets, ELMo_inputs,\
                w1_idxs, w2_idxs, role_inputs, predicate_distances, sentences, word_berts1 = [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], []

                max_eojeol_length = max([len(sentence[0]) for sentence in data])
                max_morph_length = max([len(sentence[8]) for sentence in data]) + 2

                for line in data:
                        word1, word2, word3, word4, pumsa1, pumsa2, pumsa3, pumsa4, ELMo, w1_idx, w2_idx, char, target, \
                        lemma, predicate_idx, predicate_word_ids1, predicate_word_ids2, predicate_pumsa_ids1, predicate_pumsa_ids2, predicate_distance, sentence, word_bert1 = line

                        eoj_padding = [0] * (max_eojeol_length - len(word1))

                        # get distance between current word and predicate word
                        predicate_distance = predicate_distance + [13] * (max_eojeol_length - len(word1))
                        distance_onehot_list = []
                        for distance in predicate_distance:
                                distance_onehot = [0.0] * 14
                                distance_onehot[distance] = 1.0
                                distance_onehot_list.append(distance_onehot)
                        predicate_distances.append(distance_onehot_list)

                        sentences.append(sentence)
                        empty_list = [[1, 0]] * max_eojeol_length
                        empty_list[predicate_idx] = [0, 1]
                        role_inputs.append([idx for idx in range(len(self.label2idx))])
                        words1.append(word1 + eoj_padding)
                        words2.append(word2 + eoj_padding)
                        words3.append(word3 + eoj_padding)
                        words4.append(word4 + eoj_padding)
                        pumsas1.append(pumsa1 + eoj_padding)
                        pumsas2.append(pumsa2 + eoj_padding)
                        pumsas3.append(pumsa3 + eoj_padding)
                        pumsas4.append(pumsa4 + eoj_padding)
                        predicate_words1.append(predicate_word_ids1 + eoj_padding)
                        predicate_words2.append(predicate_word_ids2 + eoj_padding)
                        predicate_pumsas1.append(predicate_pumsa_ids1 + eoj_padding)
                        predicate_pumsas2.append(predicate_pumsa_ids2 + eoj_padding)
                        lemmas.append(lemma + eoj_padding)
                        predicate_boolean.append(empty_list)
                        predicate_idxs.append([batch_idx, predicate_idx])

                        word_berts1.append(word_bert1)

                        batch_idx += 1

                        if config.ELMo:
                                w1_idxs.append(w1_idx)
                                w2_idxs.append(w2_idx)

                                tmp_ELMo_input = []
                                ELMo.insert(0, [self.bos_char])
                                ELMo.append([self.eos_char])
                                for e in ELMo:
                                        e.insert(0, self.bow_char)
                                        e.append(self.eow_char)
                                        e.extend([self.pad_char] * (self.max_characters_per_token - len(e)))
                                        tmp_ELMo_input.append(e)

                                if len(tmp_ELMo_input) <= max_morph_length:
                                        for _ in range(max_morph_length - len(tmp_ELMo_input)):
                                                tmp_ELMo_input.append([self.pad_char]*(self.max_characters_per_token))

                                ELMo_inputs.append(tmp_ELMo_input)

                        if len(eoj_padding) != 0:
                                char.extend([[0]] * (max_eojeol_length - len(word1)))

                        padded_chars = []
                        for c in char:
                                if len(c) <= max_char_length:
                                        padded_chars.append(c + [0]*(max_char_length - len(c)))
                                else:
                                        padded_chars.append(c[:max_char_length])

                        chars.append(padded_chars)
                        targets.append(target + eoj_padding)
                return [words1, words2, words3, words4, pumsas1, pumsas2, pumsas3, pumsas4, \
                                ELMo_inputs, w1_idxs, w2_idxs, chars, targets, lemmas, predicate_idxs, predicate_boolean, \
                                predicate_words1, predicate_words2, predicate_pumsas1, predicate_pumsas2, predicate_distances, role_inputs, sentences, word_berts1
                                ]

	def iter_batch(self, shuffle=False):
		if shuffle:
			random.shuffle(self.batch_data)
		for idx in range(self.len_data):
			yield self.batch_data[idx]

def get_word_length(data, pad_id, axis=2):
    return np.sum(np.not_equal(data, pad_id), axis=axis)