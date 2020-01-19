#-*-coding:utf-8-*-
import re, sys
import math
import codecs
import random

import numpy as np

def get_feature_func(posed_sentence, f_dict, config):
	feature_vecs = []
	for eojeol_idx, _ in enumerate(posed_sentence):
		posed_eojeol = posed_sentence[eojeol_idx]
		if eojeol_idx == 0:
			prev_word1 = "<BOS>"
			prev_word2 = "<BOS>"
			prev_pumsa1 = "<BOS>"
			prev_pumsa2 = "<BOS>"
		else:
			prev_word1 = posed_sentence[eojeol_idx - 1].split("|")[0]
			prev_word2 = posed_sentence[eojeol_idx - 1].split("|")[-1]
			prev_pumsa1_idx = prev_word1.rfind("/")
			prev_pumsa2_idx = prev_word2.rfind("/")
			prev_pumsa1 = prev_word1[prev_pumsa1_idx + 1:]
			prev_pumsa2 = prev_word2[prev_pumsa2_idx + 1:]

		if eojeol_idx == len(posed_sentence) - 1:
			next_word1 = "<EOS>"
			next_word2 = "<EOS>"
			next_pumsa1 = "<EOS>"
			next_pumsa2 = "<EOS>"
		else:
			next_word1 = posed_sentence[eojeol_idx + 1].split("|")[0]
			next_word2 = posed_sentence[eojeol_idx + 1].split("|")[-1]
			next_pumsa1_idx = next_word1.rfind("/")
			next_pumsa2_idx = next_word2.rfind("/")
			next_pumsa1 = next_word1[next_pumsa1_idx + 1:]
			next_pumsa2 = next_word2[next_pumsa2_idx + 1:]

		cur_word1 = posed_eojeol.split("|")[0]
		cur_word2 = posed_eojeol.split("|")[-1]
		cur_pumsa1_idx = cur_word1.rfind("/")
		cur_pumsa2_idx = cur_word2.rfind("/")
		cur_pumsa1 = cur_word1[cur_pumsa1_idx + 1:]
		cur_pumsa2 = cur_word2[cur_pumsa2_idx + 1:]

		if config['stochastic_feature'] == "embedding":
			feature_vec = []
			if ("F1:cur_word1+cur_word2 = %s|%s" % (cur_word1, cur_word2)) in f_dict:
				feature_vec.append(f_dict["F1:cur_word1+cur_word2 = %s|%s" % (cur_word1, cur_word2)]["idx"])
			else:
				feature_vec.append(f_dict["<UNK>"]["idx"])

			# if ("F2:cur_pumsa1+cur_pumsa2 = %s|%s" % (cur_pumsa1, cur_pumsa2))  in f_dict:
			# 	feature_vec[13:26]=(get_normalized_vec(f_dict["F2:cur_pumsa1+cur_pumsa2 = %s|%s" % (cur_pumsa1, cur_pumsa2)]))
			# if ("F3:cur_word1+next_word1 = %s|%s" % (cur_word1, next_word1)) in f_dict:
			# 	feature_vec[26:39]=(get_normalized_vec(f_dict["F3:cur_word1+next_word1 = %s|%s" % (cur_word1, next_word1)]))
			# if ("F4:cur_word1+next_word2 = %s|%s" % (cur_word1, next_word2)) in f_dict:
			# 	feature_vec[39:52]=(get_normalized_vec(f_dict["F4:cur_word1+next_word2 = %s|%s" % (cur_word1, next_word2)]))


			if "F5:cur_word2+next_word1 = %s|%s" % (cur_word2, next_word1) in f_dict:
				feature_vec.append(f_dict["F5:cur_word2+next_word1 = %s|%s" % (cur_word2, next_word1)]["idx"])
			else:
				feature_vec.append(f_dict["<UNK>"]["idx"])
			if "F6:cur_word2+next_word2 = %s|%s" % (cur_word2, next_word2) in f_dict:
				feature_vec.append(f_dict["F6:cur_word2+next_word2 = %s|%s" % (cur_word2, next_word2)]["idx"])
			else:
				feature_vec.append(f_dict["<UNK>"]["idx"])
			# if "F7:cur_pumsa1+next_pumsa1 = %s|%s" % (cur_pumsa1, next_pumsa1) in f_dict:
			# 	feature_vec[78:91]=(get_normalized_vec(f_dict["F7:cur_pumsa1+next_pumsa1 = %s|%s" % (cur_pumsa1, next_pumsa1)]))
			# if "F8:cur_pumsa1+next_pumsa2 = %s|%s" % (cur_pumsa1, next_pumsa2) in f_dict:
			# 	feature_vec[91:104]=(get_normalized_vec(f_dict["F8:cur_pumsa1+next_pumsa2 = %s|%s" % (cur_pumsa1, next_pumsa2)]))
			# if "F9:cur_pumsa2+next_pumsa1 = %s|%s" % (cur_pumsa2, next_pumsa1) in f_dict:
			# 	feature_vec[104:117]=(get_normalized_vec(f_dict["F9:cur_pumsa2+next_pumsa1 = %s|%s" % (cur_pumsa2, next_pumsa1)]))
			# if "F10:cur_pumsa2+next_pumsa2 = %s|%s" % (cur_pumsa2, next_pumsa2) in f_dict:
			# 	feature_vec[117:130]=(get_normalized_vec(f_dict["F10:cur_pumsa2+next_pumsa2 = %s|%s" % (cur_pumsa2, next_pumsa2)]))

			# if "F11:cur_word1+prev_word1 = %s|%s" % (cur_word1, prev_word1) in f_dict:
			# 	feature_vec[130:143]=(get_normalized_vec(f_dict["F11:cur_word1+prev_word1 = %s|%s" % (cur_word1, prev_word1)]))
			if "F12:cur_word1+prev_word2 = %s|%s" % (cur_word1, prev_word2) in f_dict:
				feature_vec.append(f_dict["F12:cur_word1+prev_word2 = %s|%s" % (cur_word1, prev_word2)]["idx"])
			else:
				feature_vec.append(f_dict["<UNK>"]["idx"])
			if "F13:cur_word2+prev_word1 = %s|%s" % (cur_word2, prev_word1) in f_dict:
				feature_vec.append(f_dict["F13:cur_word2+prev_word1 = %s|%s" % (cur_word2, prev_word1)]["idx"])
			else:
				feature_vec.append(f_dict["<UNK>"]["idx"])
			if "F14:cur_word2+prev_word2 = %s|%s" % (cur_word2, prev_word2) in f_dict:
				feature_vec.append(f_dict["F14:cur_word2+prev_word2 = %s|%s" % (cur_word2, prev_word2)]["idx"])
			else:
				feature_vec.append(f_dict["<UNK>"]["idx"])

			# if "F15:cur_pumsa1+prev_pumsa1 = %s|%s" % (cur_pumsa1, prev_pumsa1) in f_dict:
			# 	feature_vec[182:195]=(get_normalized_vec(f_dict["F15:cur_pumsa1+prev_pumsa1 = %s|%s" % (cur_pumsa1, prev_pumsa1)]))
			# if "F16:cur_pumsa1+prev_pumsa2 = %s|%s" % (cur_pumsa1, prev_pumsa2) in f_dict:
			# 	feature_vec[195:208]=(get_normalized_vec(f_dict["F16:cur_pumsa1+prev_pumsa2 = %s|%s" % (cur_pumsa1, prev_pumsa2)]))
			# if "F17:cur_pumsa2+prev_pumsa1 = %s|%s" % (cur_pumsa2, prev_pumsa1) in f_dict:
			# 	feature_vec[208:221]=(get_normalized_vec(f_dict["F17:cur_pumsa2+prev_pumsa1 = %s|%s" % (cur_pumsa2, prev_pumsa1)]))
			# if "F18:cur_pumsa2+prev_pumsa2 = %s|%s" % (cur_pumsa2, prev_pumsa2) in f_dict:
			# 	feature_vec[221:234]=(get_normalized_vec(f_dict["F18:cur_pumsa2+prev_pumsa2 = %s|%s" % (cur_pumsa2, prev_pumsa2)]))
            #
			# if "F19:prev_word1+next_word1 = %s|%s" % (prev_word1, next_word1) in f_dict:
			# 	feature_vec[234:247]=(get_normalized_vec(f_dict["F19:prev_word1+next_word1 = %s|%s" % (prev_word1, next_word1)]))
			# if "F20:prev_word1+next_word2 = %s|%s" % (prev_word1, next_word2) in f_dict:
			# 	feature_vec[247:260]=(get_normalized_vec(f_dict["F20:prev_word1+next_word2 = %s|%s" % (prev_word1, next_word2)]))
			# if "F21:prev_word2+next_word1 = %s|%s" % (prev_word2, next_word1) in f_dict:
			# 	feature_vec[260:273]=(get_normalized_vec(f_dict["F21:prev_word2+next_word1 = %s|%s" % (prev_word2, next_word1)]))
			if "F22:prev_word2+next_word2 = %s|%s" % (prev_word2, next_word2) in f_dict:
				feature_vec.append(f_dict["F22:prev_word2+next_word2 = %s|%s" % (prev_word2, next_word2)]["idx"])
			else:
				feature_vec.append(f_dict["<UNK>"]["idx"])
			# if "F23:prev_pumsa1+next_pumsa1 = %s|%s" % (prev_pumsa1, next_pumsa1) in f_dict:
			# 	feature_vec[286:299]=(get_normalized_vec(f_dict["F23:prev_pumsa1+next_pumsa1 = %s|%s" % (prev_pumsa1, next_pumsa1)]))
			if "F24:prev_pumsa1+next_pumsa2 = %s|%s" % (prev_pumsa1, next_pumsa2) in f_dict:
				feature_vec.append(f_dict["F24:prev_pumsa1+next_pumsa2 = %s|%s" % (prev_pumsa1, next_pumsa2)]["idx"])
			else:
				feature_vec.append(f_dict["<UNK>"]["idx"])
			if "F25:prev_pumsa2+next_pumsa1 = %s|%s" % (prev_pumsa2, next_pumsa1) in f_dict:
				feature_vec.append(f_dict["F25:prev_pumsa2+next_pumsa1 = %s|%s" % (prev_pumsa2, next_pumsa1)]["idx"])
			else:
				feature_vec.append(f_dict["<UNK>"]["idx"])
			if "F26:prev_pumsa2+next_pumsa2 = %s|%s" % (prev_pumsa2, next_pumsa2) in f_dict:
				feature_vec.append(f_dict["F26:prev_pumsa2+next_pumsa2 = %s|%s" % (prev_pumsa2, next_pumsa2)]["idx"])
			else:
				feature_vec.append(f_dict["<UNK>"]["idx"])

			feature_vecs.append(feature_vec)

		elif config['stochastic_feature'] == "probs":
			feature_vec = np.zeros(13*26, dtype=float)
			if ("F1:cur_word1+cur_word2 = %s|%s" % (cur_word1, cur_word2)) in f_dict:
				feature_vec[0:13]=(get_normalized_vec(f_dict["F1:cur_word1+cur_word2 = %s|%s" % (cur_word1, cur_word2)]))
			if ("F2:cur_pumsa1+cur_pumsa2 = %s|%s" % (cur_pumsa1, cur_pumsa2))  in f_dict:
				feature_vec[13:26]=(get_normalized_vec(f_dict["F2:cur_pumsa1+cur_pumsa2 = %s|%s" % (cur_pumsa1, cur_pumsa2)]))
			if ("F3:cur_word1+next_word1 = %s|%s" % (cur_word1, next_word1)) in f_dict:
				feature_vec[26:39]=(get_normalized_vec(f_dict["F3:cur_word1+next_word1 = %s|%s" % (cur_word1, next_word1)]))
			if ("F4:cur_word1+next_word2 = %s|%s" % (cur_word1, next_word2)) in f_dict:
				feature_vec[39:52]=(get_normalized_vec(f_dict["F4:cur_word1+next_word2 = %s|%s" % (cur_word1, next_word2)]))

			if "F5:cur_word2+next_word1 = %s|%s" % (cur_word2, next_word1) in f_dict:
				feature_vec[52:65]=(get_normalized_vec(f_dict["F5:cur_word2+next_word1 = %s|%s" % (cur_word2, next_word1)]))
			if "F6:cur_word2+next_word2 = %s|%s" % (cur_word2, next_word2) in f_dict:
				feature_vec[65:78]=(get_normalized_vec(f_dict["F6:cur_word2+next_word2 = %s|%s" % (cur_word2, next_word2)]))
			if "F7:cur_pumsa1+next_pumsa1 = %s|%s" % (cur_pumsa1, next_pumsa1) in f_dict:
				feature_vec[78:91]=(get_normalized_vec(f_dict["F7:cur_pumsa1+next_pumsa1 = %s|%s" % (cur_pumsa1, next_pumsa1)]))
			if "F8:cur_pumsa1+next_pumsa2 = %s|%s" % (cur_pumsa1, next_pumsa2) in f_dict:
				feature_vec[91:104]=(get_normalized_vec(f_dict["F8:cur_pumsa1+next_pumsa2 = %s|%s" % (cur_pumsa1, next_pumsa2)]))
			if "F9:cur_pumsa2+next_pumsa1 = %s|%s" % (cur_pumsa2, next_pumsa1) in f_dict:
				feature_vec[104:117]=(get_normalized_vec(f_dict["F9:cur_pumsa2+next_pumsa1 = %s|%s" % (cur_pumsa2, next_pumsa1)]))
			if "F10:cur_pumsa2+next_pumsa2 = %s|%s" % (cur_pumsa2, next_pumsa2) in f_dict:
				feature_vec[117:130]=(get_normalized_vec(f_dict["F10:cur_pumsa2+next_pumsa2 = %s|%s" % (cur_pumsa2, next_pumsa2)]))

			if "F11:cur_word1+prev_word1 = %s|%s" % (cur_word1, prev_word1) in f_dict:
				feature_vec[130:143]=(get_normalized_vec(f_dict["F11:cur_word1+prev_word1 = %s|%s" % (cur_word1, prev_word1)]))
			if "F12:cur_word1+prev_word2 = %s|%s" % (cur_word1, prev_word2) in f_dict:
				feature_vec[143:156]=(get_normalized_vec(f_dict["F12:cur_word1+prev_word2 = %s|%s" % (cur_word1, prev_word2)]))
			if "F13:cur_word2+prev_word1 = %s|%s" % (cur_word2, prev_word1) in f_dict:
				feature_vec[156:169]=(get_normalized_vec(f_dict["F13:cur_word2+prev_word1 = %s|%s" % (cur_word2, prev_word1)]))
			if "F14:cur_word2+prev_word2 = %s|%s" % (cur_word2, prev_word2) in f_dict:
				feature_vec[169:182]=(get_normalized_vec(f_dict["F14:cur_word2+prev_word2 = %s|%s" % (cur_word2, prev_word2)]))

			if "F15:cur_pumsa1+prev_pumsa1 = %s|%s" % (cur_pumsa1, prev_pumsa1) in f_dict:
				feature_vec[182:195]=(get_normalized_vec(f_dict["F15:cur_pumsa1+prev_pumsa1 = %s|%s" % (cur_pumsa1, prev_pumsa1)]))
			if "F16:cur_pumsa1+prev_pumsa2 = %s|%s" % (cur_pumsa1, prev_pumsa2) in f_dict:
				feature_vec[195:208]=(get_normalized_vec(f_dict["F16:cur_pumsa1+prev_pumsa2 = %s|%s" % (cur_pumsa1, prev_pumsa2)]))
			if "F17:cur_pumsa2+prev_pumsa1 = %s|%s" % (cur_pumsa2, prev_pumsa1) in f_dict:
				feature_vec[208:221]=(get_normalized_vec(f_dict["F17:cur_pumsa2+prev_pumsa1 = %s|%s" % (cur_pumsa2, prev_pumsa1)]))
			if "F18:cur_pumsa2+prev_pumsa2 = %s|%s" % (cur_pumsa2, prev_pumsa2) in f_dict:
				feature_vec[221:234]=(get_normalized_vec(f_dict["F18:cur_pumsa2+prev_pumsa2 = %s|%s" % (cur_pumsa2, prev_pumsa2)]))

			if "F19:prev_word1+next_word1 = %s|%s" % (prev_word1, next_word1) in f_dict:
				feature_vec[234:247]=(get_normalized_vec(f_dict["F19:prev_word1+next_word1 = %s|%s" % (prev_word1, next_word1)]))
			if "F20:prev_word1+next_word2 = %s|%s" % (prev_word1, next_word2) in f_dict:
				feature_vec[247:260]=(get_normalized_vec(f_dict["F20:prev_word1+next_word2 = %s|%s" % (prev_word1, next_word2)]))
			if "F21:prev_word2+next_word1 = %s|%s" % (prev_word2, next_word1) in f_dict:
				feature_vec[260:273]=(get_normalized_vec(f_dict["F21:prev_word2+next_word1 = %s|%s" % (prev_word2, next_word1)]))
			if "F22:prev_word2+next_word2 = %s|%s" % (prev_word2, next_word2) in f_dict:
				feature_vec[273:286]=(get_normalized_vec(f_dict["F22:prev_word2+next_word2 = %s|%s" % (prev_word2, next_word2) ]))

			if "F23:prev_pumsa1+next_pumsa1 = %s|%s" % (prev_pumsa1, next_pumsa1) in f_dict:
				feature_vec[286:299]=(get_normalized_vec(f_dict["F23:prev_pumsa1+next_pumsa1 = %s|%s" % (prev_pumsa1, next_pumsa1)]))
			if "F24:prev_pumsa1+next_pumsa2 = %s|%s" % (prev_pumsa1, next_pumsa2) in f_dict:
				feature_vec[299:312]=(get_normalized_vec(f_dict["F24:prev_pumsa1+next_pumsa2 = %s|%s" % (prev_pumsa1, next_pumsa2)]))
			if "F25:prev_pumsa2+next_pumsa1 = %s|%s" % (prev_pumsa2, next_pumsa1) in f_dict:
				feature_vec[312:325]=(get_normalized_vec(f_dict["F25:prev_pumsa2+next_pumsa1 = %s|%s" % (prev_pumsa2, next_pumsa1)]))
			if "F26:prev_pumsa2+next_pumsa2 = %s|%s" % (prev_pumsa2, next_pumsa2) in f_dict:
				feature_vec[325:338]=(get_normalized_vec(f_dict["F26:prev_pumsa2+next_pumsa2 = %s|%s" % (prev_pumsa2, next_pumsa2)]))

			feature_vecs.append(feature_vec)

	return  feature_vecs

def get_normalized_vec(value):
	"""
	output 목록
	'-'
	'ARG0'
	'ARG1'
	'ARG2'
	'ARG3'
	'ARGM-CAU'
	'ARGM-DIR'
	'ARGM-EXT'
	'ARGM-INS'
	'ARGM-LOC'
	'ARGM-MNR'
	'ARGM-PRP'
	'ARGM-TMP'
	"""
	normalized_vec = np.zeros(13, dtype=float)
	total = value["total"]
	normalized_vec[0] = (total - value['sum']) / total
	if 'ARG0' in value: normalized_vec[1] = value['ARG0']/total
	else:normalized_vec[1] = 0.0
	if 'ARG1' in value: normalized_vec[2] = value['ARG1']/total
	else:normalized_vec[1] = 0.0
	if 'ARG2' in value: normalized_vec[3] = value['ARG2']/total
	else:normalized_vec[1] = 0.0
	if 'ARG3' in value: normalized_vec[4] = value['ARG3']/total
	else:normalized_vec[1] = 0.0
	if 'ARGM-CAU' in value: normalized_vec[5] = value['ARGM-CAU']/total
	else:normalized_vec[1] = 0.0
	if 'ARGM-DIR' in value: normalized_vec[6] = value['ARGM-DIR']/total
	else:normalized_vec[1] = 0.0
	if 'ARGM-EXT' in value: normalized_vec[7] = value['ARGM-EXT']/total
	else:normalized_vec[1] = 0.0
	if 'ARGM-INS' in value: normalized_vec[8] = value['ARGM-INS']/total
	else:normalized_vec[1] = 0.0
	if 'ARGM-LOC' in value: normalized_vec[9] = value['ARGM-LOC']/total
	else:normalized_vec[1] = 0.0
	if 'ARGM-MNR' in value: normalized_vec[10] = value['ARGM-MNR']/total
	else:normalized_vec[1] = 0.0
	if 'ARGM-PRP' in value: normalized_vec[11] = value['ARGM-PRP']/total
	else:normalized_vec[1] = 0.0
	if 'ARGM-TMP' in value: normalized_vec[12] = value['ARGM-TMP']/total
	else:normalized_vec[1] = 0.0

	return normalized_vec


def get_sequence_length(data, pad_id, axis=1):
    sequence_length = np.sum(np.not_equal(data[:], pad_id), axis=axis)
    # print(f"sequence_length={sequence_length}")
    return sequence_length

def get_word_length(data, pad_id, axis=2):
    return np.sum(np.not_equal(data, pad_id), axis=axis)

def get_max(a):
    return np.amax(a)

def create_dico(item_list):
	"""
	Create a dictionary of items from a list of list of items.
	"""
	assert type(item_list) is list
	dico = {}
	for items in item_list:
		for item in items:
			if type(item) == list:
				for i in item:
					if i not in dico: dico[i] = 1
					else: dico[i] += 1
			else:
				if item not in dico: dico[item] = 1
				else: dico[item] += 1
	return dico


def create_mapping(dico):
	"""
	Create a mapping (item to ID / ID to item) from a dictionary.
	Items are ordered by decreasing frequency.
	"""
	sorted_items = sorted(dico.items(), key=lambda x: (-x[1], x[0]))
	id_to_item = {i: v[0] for i, v in enumerate(sorted_items)}
	item_to_id = {v: k for k, v in id_to_item.items()}
	return item_to_id, id_to_item


def zero_digits(s):
	"""
	Replace every digit in a string by a zero.
	"""
	return re.sub('\d', '0', s)


def inputs_from_sentences(komoran, sentences, word_to_id, pumsa_to_id, char_to_id, elmo_dict, max_char_length, ner_morph_tag):
	"""
	line : 문장셋 ['나는 집에 갔다.', '그리고 밥을 먹었다.']
	"""
	bos_char = 4  # <begin sentence>
	eos_char = 5  # <end sentence>
	bow_char = 3  # <begin word>
	eow_char = 6  # <end word>
	pad_char = 0  # <padding>
	hanja_char = 1
	max_characters_per_token = 17

	def char_padding(char, max_eojoel_len):
		len_char = len(char)
		for _ in range(max_eojoel_len - len(char)):
			char.append([0]*max_char_length)
		return char

	def _search_index_by_dict(dict, key, size):
		if key in dict:
			return dict[key]
		else:
			if "UNK" in dict:
				return dict["UNK"]
			else:
				temp = [0.0] * 15
				temp[0] = 1.0
				return temp

	def char_processing(word, max_char_length):
		chars = [char_to_id[char] if char in char_to_id else char_to_id["<UNK>"] for char in word]
		if len(chars) <= max_char_length:
			return chars + [0]*(max_char_length - len(chars))
		else:
			return chars[:max_char_length]

	def get_max_sen_len(sentences):
		return max([len(sen.split(' ')) for sen in sentences])

	def word_processing(words, max_sen_len):
		words = [word_to_id[word] if word in word_to_id else word_to_id["<UNK>"] for word in words]
		'''
		chars = two-dim python list shape:(num_words, max_char_length)
		return two-dim python list shape:(max_sen_len, max_char_length)
		'''
		if len(words) <= max_sen_len:
			return words + [0]*(max_sen_len - len(words))
		else:
			return words[:max_sen_len]
		# for _ in range(max_sen_len - len(chars)):
		# 	chars.append([0]*max_char_length)
		return words

	def pumsa_processing(pumsas, max_sen_len):
		pumsas = [pumsa_to_id[pumsa] if pumsa in pumsa_to_id else pumsa_to_id["<UNK>"] for pumsa in pumsas]
		'''
		chars = two-dim python list shape:(num_words, max_char_length)
		return two-dim python list shape:(max_sen_len, max_char_length)
		'''
		if len(pumsas) <= max_sen_len:
			return pumsas + [0]*(max_sen_len - len(pumsas))
		else:
			return pumsas[:max_sen_len]
		# for _ in range(max_sen_len - len(chars)):
		# 	chars.append([0]*max_char_length)
		return pumsas

	def elmo_processing(elmo_input):
		processed_elmo_input = []
		for elmo_morph in elmo_input:
			tmp_morph = []
			elmo_idx = elmo_morph.rfind("/")
			for elmo_char in elmo_morph[:elmo_idx]:
				if len(elmo_morph[:elmo_idx]) >= 15:
					tmp_morph.append(elmo_dict["<UNK>"])
					break
				elif elmo_char in elmo_dict:
					tmp_morph.append(elmo_dict[elmo_char])
				else:
					tmp_morph.append(elmo_dict["<UNK>"])
			processed_elmo_input.append(tmp_morph)

		return processed_elmo_input

	def elmo_padding(processed_elmo_input, max_morph_len):
		tmp_elmo_input = []
		processed_elmo_input.insert(0, [4])
		processed_elmo_input.append([5])
		for p_elmo_input in processed_elmo_input:
			p_elmo_input.insert(0, bow_char)
			p_elmo_input.append(eow_char)
			p_elmo_input.extend([pad_char] * (max_characters_per_token-len(p_elmo_input)))
			tmp_elmo_input.append(p_elmo_input)
		if len(tmp_elmo_input) <= max_morph_len:
			for _ in range(max_morph_len - len(tmp_elmo_input)):
				tmp_elmo_input.append([pad_char] * (max_characters_per_token))
		return tmp_elmo_input

	def eojeol_processing(raw_eojeol, max_sen_len):
		ner_eojeol = [_search_index_by_dict(ner_morph_tag, raw_e, 15) for raw_e in raw_eojeol]
		raw_eojeol_len = len(raw_eojeol)
		for _ in range(max_sen_len-raw_eojeol_len):
			ner_eojeol.append([0]*15)
		return ner_eojeol


	# TODO : sentences = [["문장쓰"], ["문장쓰"] ... ["문장쓰"]] 라고 가정하자..
	#char indices
	max_eojoel_len = get_max_sen_len(sentences) # 어절 length
	words1, words2, words3, words4, pumsas1, pumsas2, pumsas3, pumsas4,\
	elmo_inputs, no_padding_elmo_inputs, word1_idxs, word4_idxs, chars, raw_eojeols = [], [], [], [], [], [], [], [], [], [], [], [], [], []
	for sentence in sentences:
		# _input = [[], [], [], [], [], [], [], [], [], [], [], [], []]
		word1, word2, word3, word4, pumsa1, pumsa2, pumsa3, pumsa4, elmo_input, word1_idx, word4_idx, raw_eojeol = [], [], [], [], [], [], [], [], [], [], [], []
		w1_idx, w4_idx = 0, 0
		for word in sentence.split(' '):
			raw_eojeol.append(word)
			eojeol = ""
			for posed_token in komoran.pos(word):
				eojeol += posed_token[0] + '/' + posed_token[1] + '|'
			eojeol = eojeol[:-1]

			eojeol = eojeol.split("|")
			word1_idx.append(w1_idx)
			word4_idx.append(w1_idx + (len(eojeol) - 1))
			w1_idx += len(eojeol)
			elmo_input.extend(eojeol)

			w1 = eojeol[0]
			w2 = "<DUMMY>"
			w3 = "<DUMMY>"
			w4 = eojeol[-1]

			idx1 = w1.rfind("/")
			idx4 = w4.rfind("/")
			p1 = w1[idx1 + 1:]
			p2 = "<DUMMY>"
			p3 = "<DUMMY>"
			p4 = w1[idx4 + 1:]

			if len(eojeol) > 2:
				w2 = eojeol[1]
				w3 = eojeol[-2]
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


		char = []
		for w in sentence.split(' '):
			char.append(char_processing(w, max_char_length))
		word1_idxs.append(word1_idx)
		word4_idxs.append(word4_idx)
		if elmo_dict != None:
			no_padding_elmo_inputs.append(elmo_processing(elmo_input))

		raw_eojeols.append(eojeol_processing(raw_eojeol, max_eojoel_len))
		chars.append(char_padding(char, max_eojoel_len))
		words1.append(word_processing(word1, max_eojoel_len))
		words2.append(word_processing(word2, max_eojoel_len))
		words3.append(word_processing(word3, max_eojoel_len))
		words4.append(word_processing(word4, max_eojoel_len))
		pumsas1.append(pumsa_processing(pumsa1, max_eojoel_len))
		pumsas2.append(pumsa_processing(pumsa2, max_eojoel_len))
		pumsas3.append(pumsa_processing(pumsa3, max_eojoel_len))
		pumsas4.append(pumsa_processing(pumsa4, max_eojoel_len))


	if elmo_dict != None:
		max_morph_len = 0
		for e_input in no_padding_elmo_inputs:
			if len(e_input) > max_morph_len:
				max_morph_len = (len(e_input))
		max_morph_len += 2
		for no_padding_elmo_input in no_padding_elmo_inputs:
			elmo_inputs.append(elmo_padding(no_padding_elmo_input, max_morph_len))
	else:
		elmo_inputs = None
		word1_idxs = None
		word4_idxs = None

	return (words1, words2, words3, words4, pumsas1, pumsas2, pumsas3, pumsas4, elmo_inputs, raw_eojeols, word1_idxs, word4_idxs, chars, [])

class BatchManager(object):

	def __init__(self, data, batch_size, max_char_length, config):
		if config['elmo']:
			self.bos_char = 4  # <begin sentence>
			self.eos_char = 5  # <end sentence>
			self.bow_char = 3  # <begin word>
			self.eow_char = 6  # <end word>
			self.pad_char = 0  # <padding>
			self.hanja_char = 1
			self.max_characters_per_token = 17
		self.config = config
		self.batch_data = self.sort_and_pad(data, batch_size, max_char_length)
		self.len_data = len(self.batch_data)

	def sort_and_pad(self, data, batch_size, max_char_length):
		num_batch = int(math.ceil(len(data) /batch_size))
		sorted_data = sorted(data, key=lambda x: len(x[0]))
		batch_data = list()
		for i in range(num_batch):
			batch_data.append(self.pad_data(sorted_data[i*batch_size : (i+1)*batch_size], max_char_length, self.config))
		return batch_data

	# @staticmethod
	def pad_data(self, data, max_char_length, config):
		words1 = []
		words2 = []
		words3 = []
		words4 = []
		pumsas1 = []
		pumsas2 = []
		pumsas3 = []
		pumsas4 = []
		ner_dicts = []
		"""12.06 영준 수정"""
		chars = []
		targets = []
		elmo_input = []
		w1_idxs, w4_idxs = [], []
		max_eojeol_length = max([len(sentence[0]) for sentence in data])
		max_morph_length = max([len(sentence[8]) for sentence in data]) + 2
		for line in data:
			word1, word2, word3, word4, pumsa1, pumsa2, pumsa3, pumsa4, elmos, token_dict, w1_idx, w4_idx, char, target = line
			eoj_padding = [0] * (max_eojeol_length - len(word1))
			words1.append(word1 + eoj_padding)
			words2.append(word2 + eoj_padding)
			words3.append(word3 + eoj_padding)
			words4.append(word4 + eoj_padding)
			pumsas1.append(pumsa1 + eoj_padding)
			pumsas2.append(pumsa2 + eoj_padding)
			pumsas3.append(pumsa3 + eoj_padding)
			pumsas4.append(pumsa4 + eoj_padding)

			if config['task'] == "NER":
				token_dict_len = len(token_dict)
				for _ in range(max_eojeol_length - token_dict_len):
					token_dict.append([0]*15)
				ner_dicts.append(token_dict)
			else:
				ner_dicts = None


			if config['elmo']:
				w1_idxs.append(w1_idx)
				w4_idxs.append(w4_idx)

				tmp_elmo_input = []
				elmos.insert(0, [4])
				elmos.append([5])
				# bw_elmos.insert(0, [5])
				# bw_elmos.append([4])

				for elmo in elmos:
					elmo.insert(0, self.bow_char)
					elmo.append(self.eow_char)
					elmo.extend([self.pad_char] * (self.max_characters_per_token - len(elmo)))
					tmp_elmo_input.append(elmo)

				# for elmo in bw_elmos:
				# 	elmo.insert(0, self.bow_char)
				# 	elmo.append(self.eow_char)
				# 	elmo.extend([self.pad_char] * (self.max_characters_per_token - len(elmo)))
				# 	bw_tmp_elmo_input.append(elmo)

				if len(tmp_elmo_input) <= max_morph_length:
					for _ in range(max_morph_length - len(tmp_elmo_input)):
						# bw_tmp_elmo_input.append([self.pad_char]*(self.max_characters_per_token))
						tmp_elmo_input.append([self.pad_char]*(self.max_characters_per_token))

				elmo_input.append(tmp_elmo_input)

			if len(eoj_padding) != 0:
				char.extend([[0]] * (max_eojeol_length - len(word1)))

			new_chars = []
			for el in char:
				if len(el) <= max_char_length:
					new_chars.append( el + [0]*(max_char_length - len(el)) )
				else:
					new_chars.append( el[:max_char_length] )

			chars.append(new_chars)
			targets.append(target + eoj_padding)
			assert len(chars[-1]) == len(targets[-1])
			assert len(chars[-1]) == len(words1[-1])

		return [words1, words2, words3, words4,
				pumsas1, pumsas2, pumsas3, pumsas4, elmo_input, ner_dicts, w1_idxs, w4_idxs, chars, targets]

	def iter_batch(self, shuffle=False):
		if shuffle:
			random.shuffle(self.batch_data)
		for idx in range(self.len_data):
			yield self.batch_data[idx]
