#-*- coding: utf-8 -*-

class Config():
	def __init__ (self):
		pass

	mode = "train" # "train", or "tagging"

	H_PAD = 130

	pretrained_word_embedding = True

	restart = False
	shuffle = True

	nepoch_no_imprv = 150

	pumsa_dim = 100
	char_dim = 200
	word_dim = 50

	words_filename = "../data/vocab/words.txt"
	pumsas_filename = "../data/vocab/pumsa.txt"
	chars_filename = "../data/vocab/char.txt"
	rels_filename = "../data/vocab/rels.txt"

	embedding_filename = ""

	test_filename = ""
	dev_filename = ""
	train_filename = ""

	unlabeled_filename = ""
	tagging_file = ""

	max_iter = None  

	nepochs = 50
	batch_size = 100
	lr = 0.001
	decay_factor = 0.90

	#maximum length
	seq_length = 131
	word_length = 80

	#hidden size
	rel_mlp_size = 200
	arc_mlp_size = 500
	hidden_size = 400
	dropout = 1.0

	char_hidden = 100
	num_layer = 4
	num_layer_MLP = 1

	summary = ""

	ckpt_path = "../data/result/ckpt/test.."
	predict_path = "../predict_log/predict.txt"


