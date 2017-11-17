CRF_ITER = 300 #FULL is 2147483647 #this

ALL_TEST = True
FIXED_MIN_SEQ_PROB = 0.75
FIXED_MIN_MARGINAL_PROB = 0.9

MODEL_DIR = '../models/'
TRAIN_DIR = '../input/original_labeled_data/'
TEST_DIR = '../input/optional_test_data/'
UNLABELED_DIR = '../input/unlabeled_raw_data/'
GOOD_ML_DATA_DIR = '../input/machine_labeled_data/'
ACT_DIR = '../input/active_data/'
GOOD_ML_DATA_DIR_OUT = '../output/machine_labeled_good_data/'
ACT_DIR_OUT = '../output/active_data/'
SELF_LABELED_PATH = '../output/full_data/'

PROB_OUT = True

ENCODING = 'utf-8'

BOOTSTRAP_SAMPLE_SIZE = 2500

NUM_BAGGING_MODEL = 5

SELF_ITER_N = 3

active_min_prob = FIXED_MIN_MARGINAL_PROB
active_max_prob = 0.95

DICTIONARY = False

TAG = ['B-DT','B-LC', 'B-OG','B-PS','B-TI','I-DT','I-LC','I-OG','I-PS','I-TI', 'O']

NE_CLASSES = ['DT','LC', 'OG','PS','TI']
ft_idx = {'word':1,'word.isdigit':2,'postag':3,'postag[:2]':4,'len_word':5,'dic[B-DT]':6,'dic[B-LC]':7,'dic[B-OG]':8,
          'dic[B-PS]':9,'dic[B-TI]':10,'dic[I-DT]':11,'dic[I-LC]':12,'dic[I-OG]':13,'dic[I-PS]':14,'dic[I-TI]':15}
import  codecs

def print_setting() :
    print('CRF_ITER = ' + str(CRF_ITER))
    print('ALL_TEST = ' +str(ALL_TEST))
    print('FIXED_MIN_SEQ_PROB = ' +str(FIXED_MIN_SEQ_PROB))
    print('FIXED_MIN_MARGINAL_PROB = ' +str(FIXED_MIN_MARGINAL_PROB))

    print('ENCODING = ' +  ENCODING)

    print('BOOTSTRAP_SAMPLE_SIZE = ' +str(BOOTSTRAP_SAMPLE_SIZE))

    print('NUM_BAGGING_MODEL = ' + str(NUM_BAGGING_MODEL))

    print('SELF_ITER_N = ' + str(SELF_ITER_N))

    print('active_min_prob = ' +str(active_min_prob))
    print('active_max_prob = ' + str(active_max_prob))

def write_log(logtext, open = False, close = False, std_print = False) :
    print(logtext)
    #global log_f
    #if open is True:
    #    log_f = codecs.open(LOG, 'a', encoding=ENCODING)
    #log_f.write(logtext+'\n')
    #if std_print is True :
    #    print(logtext)
    #if close is True :
    #   log_f.close()
