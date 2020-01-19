# encoding=utf8
import os
import pickle
import sys
from collections import OrderedDict
from konlpy.tag import Komoran
import konlpy
import tensorflow as tf
import numpy as np
from model import Model
from loader import char_mapping, tag_mapping, word_mapping, pumsa_mapping, affix_mapping_with_word, affix_mapping_with_pos, load_word_embedding_matrix, eojeol_mapping, prepare_dataset, load_feature_dict, load_elmo_dict
from model_utils import get_logger, make_path, create_model, save_model, print_config, save_config, load_config, test_srl
from data_utils import inputs_from_sentences, BatchManager
from data_loader import data_loader
from elmo.elmo_model import BidirectionalLanguageModel
from elmo.elmo import weight_layers

try:
	import nsml
	from nsml import DATASET_PATH, IS_ON_NSML
except ImportError as e:
	IS_ON_NSML = False

# os.environ["CUDA_DEVICE_ORDER"]="PCI_BUS_ID"
# os.environ["CUDA_VISIBLE_DEVICES"]="1"

VERSION = '_adam_0.001_no_train_word2vec_dropout_0.6'
def parse_args():
	flags = tf.app.flags
	# configurations for the model
	flags.DEFINE_integer("seg_dim",			0,		"Embedding size for segmentation, 0 if not used")
	flags.DEFINE_integer("char_dim",		100,	"Embedding size for characters")
	flags.DEFINE_integer("word_dim",        200, 	"Embedding size for words")
	flags.DEFINE_integer("pumsa_dim", 		50, 	"Embedding size for pumsas")
	flags.DEFINE_integer("prefix_dim",		50,		"Num of hidden units in prefix LSTM")
	flags.DEFINE_integer("suffix_dim",		50,		"Num of hidden units in suffix LSTM")
	flags.DEFINE_integer("char_lstm_dim",	1000,		"Num of hidden units in char LSTM")
	flags.DEFINE_integer("word_lstm_dim",	400,	"Num of hidden units in word LSTM")
	flags.DEFINE_integer("pumsa_lstm_dim",	50,    "Num of hidden units in pumsa LSTM")
	flags.DEFINE_integer("max_char_length",	8,		"max number of character in word")
	flags.DEFINE_integer("max_word_length",	95,		"number of word")
	flags.DEFINE_integer("num_tags",		29,		"number of tags")
	flags.DEFINE_integer("num_chars",		8000,	"number of chars")
	flags.DEFINE_integer("num_layers",		1,		"num_layers")
	flags.DEFINE_integer("affix_size",		2,		"size of affix")
	flags.DEFINE_integer("affix_frequency",	50,		"frequency of affix")
	# configurations for training
	flags.DEFINE_float("clip",			5,			"Gradient clip")
	flags.DEFINE_float("dropout",		0.5,		"Dropout rate")
	flags.DEFINE_float("lr",			0.01,		"Initial learning rate")
	flags.DEFINE_string("optimizer",	"adam",		"Optimizer for training")
	flags.DEFINE_boolean("lower",		False,		"Wither lower case")
	flags.DEFINE_integer("batch_size",	32,			"batch size")
	flags.DEFINE_integer("patience",	25,			"Patience for the validation-based early stopping")

	flags.DEFINE_integer("max_epoch",	150,		"maximum training epochs")
	flags.DEFINE_integer("steps_check", 100,		"steps per checkpoint")
	flags.DEFINE_string("ckpt_path",	"ckpt",		 "Path to save model")
	flags.DEFINE_string("summary_path", "summary",		"Path to store summaries")
	flags.DEFINE_string("log_file",		"train%s.log" % VERSION,	"File for log")

	flags.DEFINE_string("vocab_file",	"vocab.json",	"File for vocab")
	flags.DEFINE_string("config_file",	"config_file",	"File for config")
	flags.DEFINE_string("script",		"conlleval",	"evaluation script")
	flags.DEFINE_string("result_path",	"result",		"Path for results")

	flags.DEFINE_string("initializer", "xavier", "orthogonal, xavier")
	##############yj change

	flags.DEFINE_string("EMBEDDING_PATH",	"./data/embeddings/KOR_komoran/glove/glove_100.vec",	"Path for pre-trained embedding")

	# flags.DEFINE_string("elmo_options", "/home/nlpgpu3/data/cm/nlp-challenge/missions/srl/data/elmo/weight/options.json", "Path for elmo options")
	# flags.DEFINE_string("elmo_weights", "/home/nlpgpu3/data/cm/nlp-challenge/missions/srl/data/elmo/weight/final_ner_weights.hdf5", "Path for elmo weights")
	# flags.DEFINE_string("elmo_dict",    "/home/nlpgpu3/data/cm/nlp-challenge/missions/srl/data/elmo/dict/final_char_dict.txt", "Path for elmo char_dict")
	# flags.DEFINE_string("necessary", "necessary_NER.pkl", "file for maps")

	flags.DEFINE_string("elmo_options", "/pretrained_data/NER/elmo/weight/options.json", "Path for elmo options")
	flags.DEFINE_string("elmo_weights", "/pretrained_data/NER/elmo/weight/final_ner_weights.hdf5", "Path for elmo weights")
	flags.DEFINE_string("elmo_dict",    "/pretrained_data/NER/elmo/dict/final_char_dict.txt", "Path for elmo char_dict")
	flags.DEFINE_string("necessary", "/pretrained_data/NER/necessary_NER.pkl", "file for maps")

	# reserved for NSML
	flags.DEFINE_integer("pause",		0,			"Pause")
	flags.DEFINE_string("mode",			"train",	"Train/Test mode")

	#experiments

	flags.DEFINE_boolean("self_attention", False, "self-attention")
	flags.DEFINE_boolean("highway", False, "highway")
	flags.DEFINE_string("stochastic_feature", "False", " ['False', 'embedding', 'probs'] ")
	flags.DEFINE_boolean("elmo", True, "elmo")

	flags.DEFINE_boolean("pretrained_embedding",		False,	"pretrained word embedding")
	flags.DEFINE_boolean("pretrained_pumsa_embedding", False, "pretrained word embedding")
	flags.DEFINE_string("task", "NER", "NER or SRL")

	# dataset
	if IS_ON_NSML:
		flags.DEFINE_string("DATASET_PATH",	nsml.DATASET_PATH, "path for dataset")
		flags.DEFINE_boolean("IS_PRACTICE", False, "whether practice or not")
		#logger.info("do you here?")
	else:
		flags.DEFINE_string("DATASET_PATH",	'./data/', "path for dataset")
		flags.DEFINE_boolean("IS_PRACTICE", True, "whether practice or not")

	FLAGS = tf.app.flags.FLAGS
	assert FLAGS.clip < 5.1, "gradient clip should't be too much"
	assert 0 <= FLAGS.dropout < 1, "dropout rate between 0 and 1"
	assert FLAGS.lr > 0, "learning rate must larger than zero"
	assert FLAGS.optimizer in ["adam", "sgd", "adagrad", "momentum"]

	return FLAGS


# config for the model
def config_model():
	config = OrderedDict()
	config["num_chars"] = FLAGS.num_chars
	config["char_dim"] = FLAGS.char_dim
	config["word_dim"] = FLAGS.word_dim
	config["pumsa_dim"] = FLAGS.pumsa_dim
	config["prefix_dim"] = FLAGS.prefix_dim
	config["suffix_dim"] = FLAGS.suffix_dim
	config["num_tags"] = FLAGS.num_tags
	config["seg_dim"] = FLAGS.seg_dim
	config["char_lstm_dim"] = FLAGS.char_lstm_dim
	config["word_lstm_dim"] = FLAGS.word_lstm_dim
	config["pumsa_lstm_dim"] = FLAGS.pumsa_lstm_dim
	config["batch_size"] = FLAGS.batch_size
	config["num_layers"] = FLAGS.num_layers
	config["affix_size"] = FLAGS.affix_size
	config["affix_frequency"] = FLAGS.affix_frequency

	config["clip"] = FLAGS.clip
	config["dropout_keep"] = 1.0 - FLAGS.dropout
	config["optimizer"] = FLAGS.optimizer
	config["lr"] = FLAGS.lr
	config["lower"] = FLAGS.lower
	config["max_char_length"] = FLAGS.max_char_length
	config["max_word_length"] = FLAGS.max_word_length
	config["initializer"] = FLAGS.initializer

	#Experiments
	config["self_attention"] = FLAGS.self_attention
	config["highway"] = FLAGS.highway
	#config["feature_list"] = FLAGS.feature_list
	config["elmo"] = FLAGS.elmo

	config["pretrained_embedding"] = FLAGS.pretrained_embedding
	config["pretrained_pumsa_embedding"] = FLAGS.pretrained_pumsa_embedding

	config["elmo_options"] = FLAGS.elmo_options
	config["elmo_weights"] = FLAGS.elmo_weights
	config["task"] = FLAGS.task

	# config["necessary"] = FLAGS.necessary % (config["task"])

	# config["elmo_options"] = FLAGS.elmo_options % (config["task"])
	# config["elmo_weights"] = FLAGS.elmo_weights % (config["task"])
	# config["elmo_dict"] = FLAGS.elmo_dict % (config["task"])
	# config["necessary"] = FLAGS.necessary % (config["task"])


	return config

"""
매 epoch에 validation/test set의 평가를 수행하고 그 결과를 출력한다.
"""
def evaluate(sess, context_embeddings_op, elmo_context, elmo_ids, model, name, data, id_to_tag, logger):
	logger.info("evaluate:{}".format(name))
	
	srl_results = model.evaluate_model(sess, context_embeddings_op, elmo_context, elmo_ids, data, id_to_tag)
	eval_lines = test_srl(srl_results, FLAGS.result_path)
	for line in eval_lines:
		logger.info(line.strip())
	f1 = float(eval_lines[1].strip().split()[-1])

	if name == "dev":
		best_test_f1 = model.best_dev_f1.eval(session=sess)
		if f1 > best_test_f1:
			tf.assign(model.best_dev_f1, f1).eval(session=sess)
			logger.info("new best dev f1 score:{:>.3f}".format(f1))
		return f1 > best_test_f1, f1
	elif name == "test":
		best_test_f1 = model.best_test_f1.eval(session=sess)
		if f1 > best_test_f1:
			tf.assign(model.best_test_f1, f1).eval(session=sess)
			logger.info("new best test f1 score:{:>.3f}".format(f1))
		return f1 > best_test_f1, f1


def bind_model(sess, context_embeddings_op, elmo_context, elmo_ids, ner_morph_tag, FLAGS):
	def save(dir_path, *args):
		os.makedirs(dir_path, exist_ok=True)
		saver = tf.train.Saver()
		saver.save(sess, os.path.join(dir_path, 'model'))

		# with open(os.path.join(dir_path, config["necessary"]), "wb") as f:
		# 	pickle.dump([word_to_id, id_to_word, char_to_id, id_to_char, pumsa_to_id, id_to_pumsa, tag_to_id, id_to_tag, ner_morph_tag], f)

	def load(dir_path, *args):
		global char_to_id
		global id_to_tag

		config = load_config(FLAGS.config_file)
		logger = get_logger(FLAGS.log_file)
		tf.get_variable_scope().reuse_variables()

		with open(os.path.join(dir_path, FLAGS.necessary), "rb") as f:
			# char_to_id, _, __, id_to_tag = pickle.load(f)
			_, _, char_to_id, _, _, _, _, id_to_tag, ner_morph_tag = pickle.load(f)

		saver = tf.train.Saver()
		ckpt = tf.train.get_checkpoint_state(dir_path)
		if ckpt and ckpt.model_checkpoint_path:
			checkpoint = os.path.basename(ckpt.model_checkpoint_path)
			saver.restore(sess, os.path.join(dir_path, checkpoint))
		else:
			raise NotImplemented('No checkpoint found!')
		print ('model loaded!')

	def infer(sentences, **kwargs):
		config = load_config(FLAGS.config_file)
		logger = get_logger(FLAGS.log_file)
		if config['elmo']:
			elmo_dict = load_elmo_dict(FLAGS.elmo_dict)
		else:
			elmo_dict = None

		results = []
		komoran = Komoran()
		reformed_sentences = [' '.join(sen[1]) for sen in sentences]
		for idx in range(0, len(reformed_sentences), 100):
			reformed_sentence = reformed_sentences[idx:idx+100]
			results.extend(model.evaluate_lines(sess, context_embeddings_op, elmo_context, elmo_ids, ner_morph_tag,
												inputs_from_sentences(komoran, reformed_sentence, word_to_id, pumsa_to_id, char_to_id,
																	  elmo_dict, FLAGS.max_char_length, ner_morph_tag),
												id_to_tag))
			# results.extend(model.evaluate_lines(sess, context_embeddings_op, elmo_context, elmo_ids, ner_morph_tag,\
			# 									inputs_from_sentences(komoran, reformed_sentence, word_to_id, pumsa_to_id, char_to_id, elmo_dict, FLAGS.max_char_length, ner_morph_tag), id_to_tag))
		'''
		result = [
			       (0.0, ['ARG0', 'ARG3', '-']),
				   (0.0, ['ARG0', 'ARG1', '-'])
				 ]
		# evaluate_lines 함수는 문장 단위 분석 결과를 내어줍니다.
		# len(result) : 문장의 갯수, 따라서 위 예제는 두 문장의 결과입니다.
		# result[0] : 첫번째 문장의 분석 결과, result[1] : 두번째 문장의 분석 결과.
		
		# 각 문장의 분석 결과는 다시 (prob, [labels])로 구성됩니다.
		# prob에 해당하는 자료는 이번 task에서 사용하지 않습니다. 에 영향을 미치지 않습니다.
		# [labels]는 각 어절의 분석 결과를 담고 있습니다. 따라서 다음과 같이 구성됩따라서 그 값이 결과니다.
		## ['첫번째 어절의 분석 결과', '두번째 어절의 분석 결과', ...]
		# 예를 들면 위 주어진 예제에서 첫번째 문장의 첫번째 어절은 'ARG0'을, 첫번째 문장의 두번째 어절은 'ARG3'을 argument label로 가집니다.

		### 주의사항 ###
		# 모든 어절의 결과를 제출하여야 합니다.
		# 어절의 순서가 지켜져야 합니다. (첫번째 어절부터 순서대로 list 내에 위치하여야 합니다.)
		'''''
		# results[1000000000000000000000000]
		# test
		return results

	if IS_ON_NSML:
		nsml.bind(save=save, load=load, infer=infer)

def train(sess, context_embeddings_op, elmo_context, elmo_ids, config):
	if not IS_ON_NSML:
		with open(FLAGS.necessary, "wb") as f:
			pickle.dump([word_to_id, id_to_word, pumsa_to_id, id_to_pumsa, char_to_id, id_to_char, tag_to_id, id_to_tag, ner_morph_tag], f)

	steps_per_epoch = train_manager.len_data
	early_stop = 0

	logger.info("start training")
	loss = []
	for epoch in range(FLAGS.max_epoch):
		for batch in train_manager.iter_batch(shuffle=True):
			step, batch_loss = model.run_step(sess, context_embeddings_op, elmo_context, elmo_ids, True, batch, ner_morph_tag)
			loss.append(batch_loss)
			if step % FLAGS.steps_check == 0:
				iteration = step // steps_per_epoch + 1
				logger.info("epoch:{} iteration:{} step:{}/{}, "
							"loss:{:>9.6f}".format(epoch, iteration, step%steps_per_epoch, \
									steps_per_epoch, np.mean(loss)))
			# break

		best, dev_f1 = evaluate(sess, context_embeddings_op, elmo_context, elmo_ids, model, "dev", dev_manager, id_to_tag, logger)

		# early stopping
		if best:
			print("best dev_f1 : %s, epoch : %s" %(dev_f1, epoch))
			early_stop = 0
		else:
			print("dev_f1 : %s" % dev_f1)
			early_stop += 1
			if early_stop > FLAGS.patience:
				print("Final best score : %s" % best)
				break

		# save model
		if best:
			save_model(sess, model, FLAGS.ckpt_path, logger)
		if IS_ON_NSML:
			nsml.report(summary=True, scope=locals(), epoch=epoch, epoch_total=FLAGS.max_epoch, train__loss=float(np.mean(loss)), valid__f1score=dev_f1)
			nsml.save(epoch)
		loss = []
	

def evaluate_cli(model, context_embeddings_op, elmo_context, elmo_ids):
	config = load_config(FLAGS.config_file)
	logger = get_logger(FLAGS.log_file)

	if FLAGS.task == "NER":
		with open(FLAGS.necessary, "rb") as f:
			word_to_id, id_to_word, char_to_id, id_to_char, pumsa_to_id, id_to_pumsa, tag_to_id, id_to_tag, ner_morph_tag = pickle.load(
				f)

	komoran = Komoran()
	results = []
	while True:
		# line = input("문장을 입력하세요.:")
		line = ["찬민이의 멘탈이 산산조각났습니다.",
				"진짜 진짜 진짜 맛있는 진짜 라면",
				"집에 가고 싶읍니다.",
				"집",
				"가 가 가 가 가 가, 가, 가 ,가, 가 가 가 가 가 가, 가, 가 ,가 !!!!! ."]
		for idx in range(0, len(line), 5):
			l = line[idx:idx+2]
			results.extend(model.evaluate_lines(sess, context_embeddings_op, elmo_context, elmo_ids, ner_morph_tag, inputs_from_sentences(komoran, l, word_to_id, pumsa_to_id, char_to_id, elmo_dict, FLAGS.max_char_length, ner_morph_tag), id_to_tag))
		print(results)



if __name__ == '__main__':
	FLAGS = parse_args()

	# tensorflow config
	tf_config = tf.ConfigProto()
	tf_config.gpu_options.allow_growth = True
	sess = tf.Session(config=tf_config)

	# model config
	make_path(FLAGS)
	config = config_model()
	save_config(config, FLAGS.config_file)
	log_path = os.path.join("log", FLAGS.log_file)
	logger = get_logger(log_path)
	print_config(config, logger)


	with open(FLAGS.necessary, 'rb') as f:
		word_to_id, id_to_word, char_to_id, id_to_char, pumsa_to_id, id_to_pumsa, tag_to_id, id_to_tag, ner_morph_tag = pickle.load(f)
		# ner_morph_tag = {"1걸":[0]*15}

	embedding_matrix = load_word_embedding_matrix(config, FLAGS.EMBEDDING_PATH, word_to_id)

	if config['elmo']:
		# elmo_dict = load_elmo_dict(config["elmo_dict"])
		elmo_dict = load_elmo_dict(FLAGS.elmo_dict)
	else:
		elmo_dict = None

	config["num_chars"] = len(char_to_id)
	config["num_words"] = len(word_to_id)
	config["num_pumsas"] = len(pumsa_to_id)
	config["num_tags"] = len(tag_to_id)


	logger.info("Now creating Model...")
	model = create_model(Model, FLAGS.ckpt_path, config, logger, word_to_id, pumsa_to_id, char_to_id, tag_to_id,
						 embedding_matrix, ner_morph_tag=ner_morph_tag)
	if config['elmo']:
		elmo_dict = load_elmo_dict(FLAGS.elmo_dict)
		ELMP_model = BidirectionalLanguageModel(
			config["elmo_options"],
			config["elmo_weights"])
		elmo_ids = tf.placeholder(tf.int32, shape=[None, None, None], name='elmo_ids')
		context_embeddings_op = ELMP_model(elmo_ids)
		elmo_context = weight_layers('input', context_embeddings_op, l2_coef=0.0)
		config_proto = tf.ConfigProto(
			log_device_placement=False,
			allow_soft_placement=True)

	else:
		elmo_dict, ELMP_model, elmo_ids, elmo_context, context_embeddings_op = None, None, None, None, None


	sess.run(tf.global_variables_initializer())
	bind_model(sess, context_embeddings_op, elmo_context, elmo_ids, ner_morph_tag, FLAGS)
	if FLAGS.pause and IS_ON_NSML:
		nsml.paused(scope=locals())

	# FLAGS.mode = 'local_test_cli'

	if FLAGS.mode == 'train':
		dataset = data_loader(FLAGS.DATASET_PATH, FLAGS.IS_PRACTICE, FLAGS.task)
		if config["task"] == "NER":
			train_dataset, dev_dataset = dataset[:-7500], dataset[-7500:]
		else:
			train_dataset, dev_dataset = dataset[:-3000], dataset[-3000:]

		# prepare data, get a collection of list containing index
		train_data = prepare_dataset(train_dataset, word_to_id, pumsa_to_id, char_to_id, tag_to_id, elmo_dict, config, ner_morph_tag=ner_morph_tag)
		dev_data = prepare_dataset(dev_dataset, word_to_id, pumsa_to_id, char_to_id, tag_to_id, elmo_dict, config, ner_morph_tag=ner_morph_tag)
		print("%i / %i  sentences in train / dev " % (
			len(train_data), len(dev_data)))

		train_manager = BatchManager(train_data, FLAGS.batch_size, FLAGS.max_char_length, config)
		dev_manager = BatchManager(dev_data, 100, FLAGS.max_char_length, config)
		train(sess, context_embeddings_op, elmo_context, elmo_ids, config)

	elif FLAGS.mode == 'local_test_cli':
		#model = create_model(sess, Model, FLAGS.ckpt_path, config, logger, word_to_id, pumsa_to_id, char_to_id, tag_to_id)
		evaluate_cli(model, context_embeddings_op, elmo_context, elmo_ids)
