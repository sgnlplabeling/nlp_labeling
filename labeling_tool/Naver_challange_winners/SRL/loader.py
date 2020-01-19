# -*-encoding:utf-8-*-
import os, sys, re, codecs, json
import pickle
import numpy as np
from data_utils import create_dico, create_mapping, zero_digits, get_feature_func


def load_feature_dict(path, config):
	with open(path, "rb") as f:
		f_list = pickle.load(f)
	feature_dict = {"<PAD>": {"idx": 0}, "<UNK>": {"idx": 1}}
	for x, y in enumerate(f_list):
		feature = y[0].decode("utf-8")
		idx = feature.rfind(":")
		f_idx = int(feature[:idx][1])
		if f_idx in config["feature_list"]:
			feature_dict[feature] = y[1]
			feature_dict[feature].update({"idx": len(feature_dict)})

	return feature_dict


def load_elmo_dict(path):
	elmo_dict = {}
	with open(path, "rb") as f:
	# with open(path) as f:
		for line in f.readlines():
			# print("raw line : ", line)
			# print("1 line : ", line.decode("utf-8"))
			line = line.decode("utf-8")
			line = line.strip()
			elmo_dict[line] = len(elmo_dict)

	return elmo_dict


def _load_conll_file(path):
	"""
	파일을 읽어 문장 단위 list로 리턴한다.
	"""
	sentences = []
	sentence = [[], [], []]

	with codecs.open(path, 'r', 'utf-8') as fp:
		for line in fp:  # 라인 단위로
			line = line.rstrip()

			if not line:  # 문장이 끝나면
				if len(sentence) > 0:
					sentences.append(sentence)  # 보관한다.
					sentence = []
			else:  # 문장이 진행 중이면
				word = line.split()
				sentence.append(word)
		if len(sentence) > 0:
			sentences.append(sentence)
	return sentences


def eojeol_mapping(sentences):
	"""
	어절 사전을 구축한다. 안쓸듯...
	"""
	eojeol = [[[word] for word in s[-2]] for s in sentences]
	dico = create_dico(eojeol)
	dico["<PAD>"] = 10000001
	dico['<UNK>'] = 10000000
	eojeol_to_id, id_to_eojeol = create_mapping(dico)
	print("Found %i unique words" % (len(dico)))
	return dico, eojeol_to_id, id_to_eojeol


def word_mapping(sentences):
	"""
	단어 사전을 구축한다.
	"""
	words1 = [[[word] for word in s[1]] for s in sentences]
	words2 = [[[word] for word in s[2]] for s in sentences]
	words3 = [[[word] for word in s[3]] for s in sentences]
	words4 = [[[word] for word in s[4]] for s in sentences]
	dico = create_dico(words1 + words2 + words3 + words4)
	dico["<PAD>"] = 10000001
	dico['<UNK>'] = 10000000
	word_to_id, id_to_word = create_mapping(dico)
	print("Found %i unique words" % (len(dico)))
	return dico, word_to_id, id_to_word


def pumsa_mapping(sentences):
	"""
	단어 사전을 구축한다.
	"""
	pumsas1 = [[[word] for word in s[5]] for s in sentences]
	pumsas2 = [[[word] for word in s[6]] for s in sentences]
	pumsas3 = [[[word] for word in s[7]] for s in sentences]
	pumsas4 = [[[word] for word in s[8]] for s in sentences]
	dico = create_dico(pumsas1 + pumsas2 + pumsas3 + pumsas4)
	dico["<PAD>"] = 10000001
	dico['<UNK>'] = 10000000
	pumsa_to_id, id_to_pumsa = create_mapping(dico)
	print("Found %i unique pumsa" % (len(pumsa_to_id)))
	return dico, pumsa_to_id, id_to_pumsa


def char_mapping(sentences, lower):
	"""
	음절 사전을 구축한다.
	"""
	if lower:
		chars = [[[char for char in word.lower()] for word in s[-2]] for s in sentences]
	else:
		chars = [[[char for char in word] for word in s[-2]] for s in sentences]
	dico = create_dico(chars)
	dico["<PAD>"] = 10000001
	dico['<UNK>'] = 10000000
	char_to_id, id_to_char = create_mapping(dico)
	print("Found %i unique chars" % (len(dico)))
	return dico, char_to_id, id_to_char


def tag_mapping(sentences):
	"""
	Create a dictionary and a mapping of tags, sorted by frequency.
	"""
	tags = [[tag for tag in s[-1]] for s in sentences]
	dico = create_dico(tags)
	tag_to_id, id_to_tag = create_mapping(dico)
	print("Found %i unique tags" % len(dico))
	return dico, tag_to_id, id_to_tag


def load_word_embedding_matrix(config, embed_file_path, word_to_id):
	print("Loading Pre-trained Embedding Model and merging it with current dict")
	if not config["pretrained_embedding"]:
		print("No Pre-trained Embedding!")
		return None

	# Get values from pre-trained word embedding
	embedding_dict = {}
	cnt = 0
	except_cnt = 0
	total_size = len(word_to_id)
	with open(embed_file_path, 'r') as f:
	# with open(embed_file_path, 'rb') as f:
		for idx, line in enumerate(f.readlines()):
			# try:
			# 	line = line.decode("euc-kr")
			# except:
			# 	except_cnt += 1
			# 	continue
			if line.strip():
				word = line.strip().split(' ')[0]
				if word == "PADDING":
					word = "<PAD>"
				elif word == "UNK":
					word = "<UNK>"
				_embedding = [v for v in line.strip().split(' ')[1:]]
				embedding = np.array(_embedding)
				embedding_dict[word] = embedding


	np.random.seed(0)	#for reproducibility
	embedding_matrix = np.random.randn(len(word_to_id), config["word_dim"])	#현재 100

	for k, v in word_to_id.items():
		word_vector = embedding_dict.get(k, None)
		if word_vector is not None:
			cnt += 1
			embedding_matrix[v] = word_vector

	#replace padding in embedding matrix into np.zeros
	pad_index = word_to_id['<PAD>']
	embedding_matrix[pad_index] = np.zeros(config["word_dim"])

	print("Loaded word embedding from %s" % embed_file_path)
	print("%s / %s" %(cnt, total_size))
	print("word except : %s", except_cnt)
	return embedding_matrix


def only_frequent_affix(dico, frequency):
	selectedKeys = list()
	for k, v in dico.items():
		if v < frequency:
			selectedKeys.append(k)

	for k in selectedKeys:
		if k in dico:
			del dico[k]

	return dico


def affix_mapping_with_word(sentences, type, size, frequency):
	"""
	Affix 사전을 구축한다.
	형태소 기준으로 구축할 지, 원 단어 기준으로 구축할 지 미정
	현재는 원 단어 기준
	:param sentences:  list형태의 sentence 정보
	:param *_size: *의 n-gram의 size
	:param frequency: frequency의 threshold ex) 50이상 등장
	:return:
	"""
	affixes = []
	for sentence in sentences:
		affix = []
		# 단어 기준으로 affix 진행 시
		for word in sentence[-2]:
			aff_tmp = ""
			if len(word) < size:
				for i in range(size - len(word)):
					aff_tmp += "^"
				if type == 'prefix':
					aff_tmp = aff_tmp + word  # size가 3이라면 ><><안 이런식으로
				elif type == 'suffix':
					aff_tmp = word + aff_tmp  # size가 3이라면 다><>< 이런식으로
			elif len(word) == size:
				aff_tmp = word
			else:
				idx = size - len(word)
				if type == 'prefix':
					aff_tmp = word[:idx]  # size가 3이면 apple => app
				elif type == 'suffix':
					aff_tmp = word[-idx:]  # size가 3이면 apple => ple
			affix.append(aff_tmp)
		affixes.append(affix)

	whole_aff_dico = create_dico(affixes)  # 전체 prefix 사전
	aff_dico = only_frequent_affix(whole_aff_dico, frequency)  # frequent한 것만 모아놓은 사전
	aff_dico["<PAD>"] = 10000001
	aff_dico["<UNK>"] = 10000000

	aff_to_id, id_to_aff = create_mapping(aff_dico)
	print("Found %i unique %s" % (len(aff_dico), type))
	return aff_dico, aff_to_id, id_to_aff


def affix_mapping_with_pos(sentences, type, size, frequency):
	"""
	Affix 사전을 구축한다.
	형태소 기준으로 구축할 지, 원 단어 기준으로 구축할 지 미정
	현재는 원 단어 기준
	:param sentences:  list형태의 sentence 정보
	:param *_size: *의 n-gram의 size
	:param frequency: frequency의 threshold ex) 50이상 등장
	:return:
	"""
	affixes = []
	for sentence in sentences:
		affix = []
		# 단어 기준으로 affix 진행 시
		# for word in sentence[-2]:

		# 형태소 기준으로 affix 진행 시
		for eojeol in sentence[-3]:
			word = ""
			for w in eojeol.split('|'):
				word += w.split('/')[0]

			aff_tmp = ""
			if len(word) < size:
				for i in range(size - len(word)):
					aff_tmp += "^"
				if type == 'prefix':
					aff_tmp = aff_tmp + word  # size가 3이라면 ><><안 이런식으로
				elif type == 'suffix':
					aff_tmp = word + aff_tmp  # size가 3이라면 다><>< 이런식으로
			elif len(word) == size:
				aff_tmp = word
			else:
				idx = size - len(word)
				if type == 'prefix':
					aff_tmp = word[:idx]  # size가 3이면 apple => app
				elif type == 'suffix':
					aff_tmp = word[-idx:]  # size가 3이면 apple => ple
			affix.append(aff_tmp)
		affixes.append(affix)

	whole_aff_dico = create_dico(affixes)  # 전체 prefix 사전
	aff_dico = only_frequent_affix(whole_aff_dico, frequency)  # frequent한 것만 모아놓은 사전
	aff_dico["<PAD>"] = 10000001
	aff_dico["<UNK>"] = 10000000

	aff_to_id, id_to_aff = create_mapping(aff_dico)
	print("Found %i unique %s" % (len(aff_dico), type))
	return aff_dico, aff_to_id, id_to_aff


def get_affix_ids_with_word(sentence, aff_to_ids, type, config):
	ids = []
	for word in sentence:
		aff_tmp = ""
		# suf_tmp = ""
		if len(word) < config["affix_size"]:
			for i in range(config["affix_size"] - len(word)):
				aff_tmp += "^"
			if type == 'prefix':
				aff_tmp = aff_tmp + word  # size가 3이라면 ><><안 이런식으로
			elif type == 'suffix':
				aff_tmp = word + aff_tmp  # size가 3이라면 다><>< 이런식으로
		elif len(word) == config["affix_size"]:
			aff_tmp = word
		else:
			idx = config["affix_size"] - len(word)
			if type == 'prefix':
				aff_tmp = word[:idx]  # size가 3이면 apple => app
			elif type == 'suffix':
				aff_tmp = word[-idx:]  # size가 3이면 apple => ple
		if aff_tmp in aff_to_ids:
			ids.append(aff_to_ids[aff_tmp])
		else:
			ids.append(aff_to_ids["<UNK>"])
	return ids


def get_affix_ids_with_pos(sentence, aff_to_ids, type, config):
	ids = []
	for eojeol in sentence:
		word = ""
		for w in eojeol.split('|'):
			word += w.split('/')[0]
		aff_tmp = ""
		# suf_tmp = ""
		if len(word) < config["affix_size"]:
			for i in range(config["affix_size"] - len(word)):
				aff_tmp += "^"
			if type == 'prefix':
				aff_tmp = aff_tmp + word  # size가 3이라면 ><><안 이런식으로
			elif type == 'suffix':
				aff_tmp = word + aff_tmp  # size가 3이라면 다><>< 이런식으로
		elif len(word) == config["affix_size"]:
			aff_tmp = word
		else:
			idx = config["affix_size"] - len(word)
			if type == 'prefix':
				aff_tmp = word[:idx]  # size가 3이면 apple => app
			elif type == 'suffix':
				aff_tmp = word[-idx:]  # size가 3이면 apple => ple
		if aff_tmp in aff_to_ids:
			ids.append(aff_to_ids[aff_tmp])
		else:
			ids.append(aff_to_ids["<UNK>"])
	return ids


def prepare_dataset(dataset, word_to_id, pumsa_to_id, char_to_id, tag_to_id, elmo_dict, config, train=True):
	"""
	데이터셋 전처리를 수행한다.
	return : list of list of dictionary
	dictionry
		- word indices
		- word char indices
		- tag indices
	"""
	none_index = tag_to_id["-"] if "-" in tag_to_id else tag_to_id["-"]

	data = []
	for idx, sen in enumerate(dataset):
		# sen : [['1', '2', '3', '4', '5', '6', '7', '8', '9', '10'], ['나는', '다른', '방배들과', '한', '다발씩', '묶여', '컴컴한', '금융기관', '속으로', '옮겨졌다.'], ['ARG0', '-', '-', '-', '-', '-', '-', '-', 'ARG3', '-']]
		fw_elmo_input = []
		if config['elmo']:
			for elmo_morph in sen[9]:
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
				fw_elmo_input.append(tmp_morph)

		word_ids1 = [word_to_id[w] if w in word_to_id else word_to_id['<UNK>'] for w in sen[1]]
		word_ids2 = [word_to_id[w] if w in word_to_id else word_to_id['<UNK>'] for w in sen[2]]
		word_ids3 = [word_to_id[w] if w in word_to_id else word_to_id['<UNK>'] for w in sen[3]]
		word_ids4 = [word_to_id[w] if w in word_to_id else word_to_id['<UNK>'] for w in sen[4]]

		pumsa_ids1 = [pumsa_to_id[p] if p in pumsa_to_id else pumsa_to_id['<UNK>'] for p in sen[5]]
		pumsa_ids2 = [pumsa_to_id[p] if p in pumsa_to_id else pumsa_to_id['<UNK>'] for p in sen[6]]
		pumsa_ids3 = [pumsa_to_id[p] if p in pumsa_to_id else pumsa_to_id['<UNK>'] for p in sen[7]]
		pumsa_ids4 = [pumsa_to_id[p] if p in pumsa_to_id else pumsa_to_id['<UNK>'] for p in sen[8]]

		chars = [[char_to_id[c if c in char_to_id else '<UNK>']
				  for c in word] for word in sen[-2]]
		if train:
			tag_ids = [tag_to_id[l] for l in sen[-1]]
		else:
			tag_ids = [none_index for _ in chars]
		data.append([word_ids1, word_ids2, word_ids3, word_ids4,
					 pumsa_ids1, pumsa_ids2, pumsa_ids3, pumsa_ids4, fw_elmo_input, sen[10], sen[11], chars, tag_ids])

	return data


def _search_index_by_dict( dict, key, size):
	if key in dict:
		return dict[key]
	else:
		if "UNK" in dict:
			return dict["UNK"]
		else:
			temp = [0.0] * 15
			temp[0] = 1.0
			return temp
