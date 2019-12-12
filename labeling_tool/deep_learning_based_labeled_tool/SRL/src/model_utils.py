import logging
import os
import tensorflow as tf

from config import Config
from eval import EvalCounts, get_final_report

config = Config()

def get_logger(log_file):
	logger = logging.getLogger(log_file)
	logger.setLevel(logging.DEBUG)
	fh = logging.FileHandler(log_file)
	fh.setLevel(logging.DEBUG)
	ch = logging.StreamHandler()
	ch.setLevel(logging.INFO)
	formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
	ch.setFormatter(formatter)
	fh.setFormatter(formatter)
	logger.addHandler(ch)
	logger.addHandler(fh)
	return logger

def create_model(Model, logger, word2idx, pumsa2idx, char2idx, label2idx, lemma2idx, word_embedding_matrix):
	model = Model(word2idx, pumsa2idx, char2idx, label2idx, lemma2idx, word_embedding_matrix)
	logger.info("Created model with fresh parameters.")

	return model

def test_srl(results):
	counts = EvalCounts()
	num_features = None

	for result in results:
		for line in result:
			line = line.rstrip('\r\n')
			features = line.split()
			correct, guessed = features[-2], features[-1]

			if correct == guessed:
				counts.correct += 1

			if correct == guessed and correct not in ['-', 'O', '_']:
				counts.t_correct_tags[correct] += 1 #XXX
				counts.correct_tags += 1

			if correct not in ['-', 'O', '_']:
				counts.found_correct += 1
				counts.t_found_correct[correct] += 1
			if guessed not in ['-', 'O', '_']:
				counts.found_guessed += 1
				counts.t_found_guessed[guessed] += 1
			counts.num_words += 1

	return get_final_report(counts)

def write_tag(sentences):
	output_file = os.path.join(config.predict_path)
	with open(output_file, "w", encoding='utf-8') as f:
		for sentence in sentences:
			f.write(sentence+"\n")

def save_model(sess, SRL_Model, logger):
	checkpoint_path = os.path.join(config.ckpt_path)
	SRL_Model.saver.save(sess, checkpoint_path)
	logger.info("model saved")

def init_ELMo(sess):
	uninitialized_vars = []
	for var in tf.all_variables():
		try:
			sess.run(var)
		except tf.errors.FailedPreconditionError:
			uninitialized_vars.append(var)

	sess.run(tf.initialize_variables(uninitialized_vars))