from config import Config


config = Config()

def prepare_dataset(dataset, word2idx, pumsa2idx, char2idx, lemma2idx, label2idx, ELMo_dict):
	distance2idx = {
		-6: 0, -5: 1, -4: 2, -3: 3, -2: 4, -1: 5, 0: 6,
		1: 7, 2: 8, 3: 9, 4: 10, 5: 11, 6: 12
	}

	data = []

	for idx, sen in enumerate(
			zip(dataset[0], dataset[1], dataset[2], dataset[3], dataset[4], dataset[5], dataset[6], dataset[7], \
				dataset[8], dataset[9], dataset[10], dataset[11], dataset[12], dataset[13], dataset[14], dataset[15], \
				dataset[16], dataset[17], dataset[18], dataset[19])):

		word_ids1 = [word2idx[w] if w in word2idx else word2idx['<UNK>'] for w in sen[0]]
		word_ids2 = [word2idx[w] if w in word2idx else word2idx['<UNK>'] for w in sen[1]]
		word_ids3 = [word2idx[w] if w in word2idx else word2idx['<UNK>'] for w in sen[2]]
		word_ids4 = [word2idx[w] if w in word2idx else word2idx['<UNK>'] for w in sen[3]]
		pumsa_ids1 = [pumsa2idx[p] if p in pumsa2idx else pumsa2idx['<UNK>'] for p in sen[4]]
		pumsa_ids2 = [pumsa2idx[p] if p in pumsa2idx else pumsa2idx['<UNK>'] for p in sen[5]]
		pumsa_ids3 = [pumsa2idx[p] if p in pumsa2idx else pumsa2idx['<UNK>'] for p in sen[6]]
		pumsa_ids4 = [pumsa2idx[p] if p in pumsa2idx else pumsa2idx['<UNK>'] for p in sen[7]]
		chars = [[char2idx[c if c in char2idx else '<UNK>'] for c in word] for word in sen[8]]
		lemma = [lemma2idx[sen[10]] if sen[10] in lemma2idx else lemma2idx['<UNK>']] * len(word_ids1)
		predicate = int(sen[11])
		predicate_word_ids1 = [word2idx[sen[15]] if sen[15] in word2idx else word2idx['<UNK>']] * len(word_ids1)
		predicate_word_ids2 = [word2idx[sen[16]] if sen[16] in word2idx else word2idx['<UNK>']] * len(word_ids1)
		predicate_pumsa_ids1 = [pumsa2idx[sen[17]] if sen[17] in pumsa2idx else pumsa2idx['<UNK>']] * len(word_ids1)
		predicate_pumsa_ids2 = [pumsa2idx[sen[18]] if sen[18] in pumsa2idx else pumsa2idx['<UNK>']] * len(word_ids1)
		predicate_distances = [(eojoel_idx - predicate) for eojoel_idx, _ in enumerate(word_ids1)]
		for d_idx, distance in enumerate(predicate_distances):
			if distance > 6 : predicate_distances[d_idx] = 6
			elif distance < -6 : predicate_distances[d_idx] = -6
			predicate_distances[d_idx] = distance2idx[predicate_distances[d_idx]]

		label_ids = [label2idx[l] if l in label2idx else '<UNK>' for l in sen[14]]

		ELMo_input = []
		if config.ELMo :
			for elmo_morph in sen[9]:
				tmp_morph = []
				elmo_idx = elmo_morph.rfind("/")
				for elmo_char in elmo_morph[:elmo_idx]:
					if len(elmo_morph[:elmo_idx]) >= 15:
						tmp_morph.append(ELMo_dict["<UNK>"])
						break
					elif elmo_char in ELMo_dict:
						tmp_morph.append(ELMo_dict[elmo_char])
					else:
						tmp_morph.append(ELMo_dict["<UNK>"])
				ELMo_input.append(tmp_morph)

		data.append([word_ids1, word_ids2, word_ids3, word_ids4, pumsa_ids1, pumsa_ids2, pumsa_ids3, pumsa_ids4, \
					 ELMo_input, sen[12], sen[13], chars, label_ids, lemma, predicate, \
					 predicate_word_ids1, predicate_word_ids2, predicate_pumsa_ids1, predicate_pumsa_ids2,
					 predicate_distances, sen[19]])

	return data
