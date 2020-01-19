import os, logging
from konlpy.tag import Komoran

#practice_mode = True
def parse_sentence_pos(line):
	komoran = Komoran()
	idx, raw, label = line.split('\t')
	pos = ""
	for elem in komoran.pos(line):
		pos += elem[0]+'/'+elem[1]+'|'
	pos = pos[-1]
	return idx, pos, raw, label

def test_data_loader(root_path):
	"""
	문장을 리턴한다.
	return: list of sentence
	"""
	data_path = os.path.join(root_path, 'test', 'test_data')
	return _load_data(data_path, is_train=False)

def local_test_data_loader(root_path):
	"""
	문장을 리턴한다.
	return: list of sentence
	"""
	data_path = os.path.join(root_path, 'test', 'test_data')
	return _load_data(data_path, is_train=True)

def _load_data(data_path, is_train=False, practice_mode=True):
	"""
	파일을 읽어 문장 단위 list로 리턴한다.
	"""
	#print("_load_data_successful")
	sentences = []
	sentence = [[], [], [], [] ,[], [], [], [], [], [], [], [], [], [], []] # idx, word1, word4, pumsa1, pumsa4, label
	#posed_sentence = ""
	komoran = Komoran()
	w1_idx, w4_idx = 0, 0
	with open(data_path, encoding='utf-8') as fp:
		contents = fp.read().strip()
		for line in contents.split('\n'):
			if line == '':
				#print("line appended")
				sentences.append(sentence)
				sentence = [[], [], [], [] ,[], [], [], [], [], [], [], [], [], [], []]
				w1_idx, w4_idx = 0, 0
			else:
				if practice_mode is True:
					idx, eojeol, chars, label = line.split('\t')
				else:
					# print("???????????????????????")
					idx, chars, label = line.split('\t')
					eojeol = ""
					for elem in komoran.pos(chars):
						eojeol += elem[0] + '/' + elem[1] + '|'
					eojeol = eojeol[:-1]

				eojeol = eojeol.split("|")
				sentence[10].append(w1_idx)
				sentence[11].append(w1_idx + (len(eojeol) - 1))
				w1_idx += len(eojeol)

				#print(eojeol)
				sentence[-3].append(eojeol)
				word1 = eojeol[0]
				word2 = "<DUMMY>"
				word3 = "<DUMMY>"
				word4 = eojeol[-1]

				idx1 = word1.rfind("/")
				idx4 = word4.rfind("/")
				pumsa1 = word1[idx1+1:]
				pumsa2 = "<DUMMY>"
				pumsa3 = "<DUMMY>"
				pumsa4 = word4[idx4+1:]

				if len(eojeol) > 2:
					word2 = eojeol[1]
					word3 = eojeol[-2]

					idx2 = word2.rfind("/")
					idx3 = word3.rfind("/")
					pumsa2 = word2[idx2+1:]
					pumsa3 = word3[idx3+1:]

				sentence[0].append(idx)
				sentence[1].append(word1)
				sentence[2].append(word2)
				sentence[3].append(word3)
				sentence[4].append(word4)
				sentence[5].append(pumsa1)
				sentence[6].append(pumsa2)
				sentence[7].append(pumsa3)
				sentence[8].append(pumsa4)
				sentence[9].extend(eojeol)
				sentence[-2].append(chars)
				sentence[-1].append(label)
	return sentences


def data_loader(root_path, is_practice, task):
	data_path = os.path.join(root_path, 'train', 'train_data')

	# data_path = os.path.join(root_path, 'train', 'real_[NER]komoran_train_data.txt')



	print(data_path)
	return _load_data(data_path, is_train=True, practice_mode=is_practice)
	# return _load_data(data_path, is_train=True, practice_mode=False)