import os
import pickle
import tensorflow as tf
import numpy as np

from model import Model
from data_loader import load_word_embedding_matrix, load_data, load_ELMo
from loader import prepare_dataset
from data_utils import get_necessary, BatchManager
from config import Config
from model_utils import create_model, get_logger, test_srl, write_tag, save_model, init_ELMo


os.environ["CUDA_DEVICE_ORDER"]="PCI_BUS_ID"
os.environ["CUDA_VISIBLE_DEVICES"]="0"

config = Config()

def evaluate(sess, SRL_Model, name, data, idx2label, logger):

	logger.info("evaluate:{}".format(name))
	srl_results = SRL_Model.evaluate_crf_model(sess, data, ELMo_context, ELMo_ids, idx2label)

	eval_lines = test_srl(srl_results)
	for line in eval_lines:
		logger.info(line.strip())
	f1 = float(eval_lines[1].strip().split()[-1])

	if name == "dev":
		best_test_f1 = SRL_Model.best_dev_f1.eval(session=sess)
		if f1 > best_test_f1:
			tf.assign(SRL_Model.best_dev_f1, f1).eval(session=sess)
			logger.info("new best dev f1 score:{:>.3f}".format(f1))

		if f1 > best_test_f1:
			final_report = eval_lines
		else:
			final_report = None

		return f1 > best_test_f1, f1, final_report
	elif name == "test":
		best_test_f1 = SRL_Model.best_test_f1.eval(session=sess)
		if f1 > best_test_f1:
			tf.assign(SRL_Model.best_test_f1, f1).eval(session=sess)
			logger.info("new best test f1 score:{:>.3f}".format(f1))

		return f1 > best_test_f1, f1, eval_lines

def train(sess):
	logger.info("start training")

	loss = []
	best_dev = ""

	steps_per_epoch = train_manager.len_data
	early_stop = 0

	writer = tf.summary.FileWriter(config.summary_path, sess.graph)

	for epoch in range(config.max_epoch):
		for _, batch in enumerate(train_manager.iter_batch(shuffle= True)):
			step, batch_loss, summary = SRL_Model.run_step(sess, ELMo_context, ELMo_ids, True, batch)
			loss.append(batch_loss)
			if step % config.steps_check == 0:
				iteration = step // steps_per_epoch + 1
				logger.info("epoch:{} iteration:{} step:{}/{}, "hghg
							"loss:{:>9.6f}".format(epoch, iteration, step % steps_per_epoch, \
												   steps_per_epoch, np.mean(loss)))
		writer.add_summary(summary, step)

		best, dev_acc, final_report = evaluate(sess, SRL_Model, "dev", test_manager, idx2label, logger)

		if final_report != None:
			best_dev = final_report

		if best:
			print("best dev_f1 : %s, epoch : %s" %(dev_acc, epoch))
			early_stop = 0
			save_model(sess, SRL_Model, logger)

		else:
			print("dev_f1 : %s" % dev_acc)
			early_stop += 1
			if early_stop > config.patience:

				print("Final best test score : %s" % best)
				print("============DEV=============")

				for line in best_dev:
					logger.info(line.strip())
				break
		loss = []

def tagging(sess):
	logger.info("start tagging")
	sentences = []
	trans = SRL_Model.trans.eval(session=sess)

	for _, batch in enumerate(unlabeled_manager.iter_batch(shuffle=False)):
		sentence = batch[-1]
		lengths, scores = SRL_Model.run_step(sess, ELMo_context, ELMo_ids, False, batch)
		batch_paths = SRL_Model.decode(scores, lengths, trans)
		for i in range(len(sentence)):
			string = sentence[i] + "|||"
			pred = [idx2label[int(x)] for x in batch_paths[i][:lengths[i]]]
			sentences.append(string + " ".join(pred))

	write_tag(sentences)

if __name__ == "__main__":
	log_path = os.path.join("log", config.log_file)
	logger = get_logger(log_path)

	tf_config = tf.ConfigProto()
	tf_config.gpu_options.allow_growth = True
	sess = tf.Session(config=tf_config)

	#load or make vocab
	if os.path.isfile(config.necessary):
		with open(config.necessary, 'rb') as f:
			word2idx, pumsa2idx, lemma2idx, char2idx, label2idx, idx2label = pickle.load(f)
	else:
		word2idx, pumsa2idx, lemma2idx, char2idx, label2idx, idx2label = get_necessary()

	if config.pretrained_embeddings:
		word_embedding_matrix = load_word_embedding_matrix(word2idx)
	else:
		word_embedding_matrix = None

	logger.info("Now creating Model...")
	SRL_Model = create_model(Model, logger, word2idx, pumsa2idx, char2idx, label2idx,
							 lemma2idx, word_embedding_matrix)

	if config.mode == "train":
		ELMo_dict, context_embeddings_op, ELMo_context, ELMo_ids = load_ELMo()
		sess.run(tf.global_variables_initializer())

		train_dataset = load_data(config.train_path)
		test_dataset = load_data(config.test_path)

		train_data = prepare_dataset(train_dataset, word2idx, pumsa2idx, char2idx, lemma2idx, label2idx, ELMo_dict)
		test_data = prepare_dataset(test_dataset, word2idx, pumsa2idx, char2idx, lemma2idx, label2idx, ELMo_dict)

		print("%i / %i  sentences in train / dev " % (len(train_data), len(test_data)))

		train_manager = BatchManager(train_data, label2idx)
		test_manager = BatchManager(test_data, label2idx)

		train(sess)

	elif config.mode == "tagging":
		saver = tf.train.Saver()
		saver.restore(sess, config.ckpt_path)

		ELMo_dict, context_embeddings_op, ELMo_context, ELMo_ids = load_ELMo()
		init_ELMo(sess)

		unlabeled_dataset = load_data(config.unlabeld_path)
		unlabeled_data = prepare_dataset(unlabeled_dataset, word2idx, pumsa2idx, char2idx, lemma2idx, label2idx, ELMo_dict)

		print("%i sentences in unlabeled " % len(unlabeled_data))

		unlabeled_manager = BatchManager(unlabeled_data, label2idx)

		tagging(sess)