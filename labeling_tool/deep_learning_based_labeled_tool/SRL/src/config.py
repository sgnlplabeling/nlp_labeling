class Config():
	def __init__ (self):
		pass

	mode = "train" # "train" or "tagging"

	ELMo = True
	pretrained_embeddings = False

	# Input_dim
	char_dim = 50
	word_dim = 50
	pumsa_dim = 100
	ELMo_dim = 1024 # Do not change.

	# LSTM_dim
	lstm_dim = 256
	char_lstm_dim = 50
	pumsa_lstm_dim = 50

	# lemgth
	max_word_length = 95
	max_char_length = 8

	num_layers = 2
	clip = 5
	dropout = 0.7
	lr = 0.001
	batch_size = 32
	patience = 1
	max_epoch = 10
	steps_check = 100

	initializer = "xavier"

	word_emb_path = ""
	necessary = ""
	ELMo_options = ""
	ELMo_weights = ""
	ELMo_dict = ""

	train_path = ""
	test_path = ""
	unlabeld_path = ""

	ckpt_path = ""
	predict_path = ""
	summary_path = ""
	log_file = ""




