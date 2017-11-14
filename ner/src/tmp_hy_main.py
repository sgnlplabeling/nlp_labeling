import time
import sys
import codecs
import ner_preprocessing as pre
from ner_evaluation import myTagger
from ner_basicmodel import BasicModel
from ner_baggingmodel import BaggingModel
from ner_load import Loader
import ner_utils as utils
import ner_settings as st
from ner_active import Active_Assistant
import codecs
import os.path
import uuid
import shutil
import ner_generate

MODEL_NUMBER= time.strftime("%Y%m%d-%H%M%S")+'_'+ str(uuid.uuid4())
BASE_MODEL_PATH =st.MODEL_DIR+MODEL_NUMBER + '/base_model/'
BAGGING_MODEL_PATH = st.MODEL_DIR+ MODEL_NUMBER + '/bagging_model/'

#BOOT_ITER = 1

SAVE_MODEL = False
if '-s' in sys.argv:
    SAVE_MODEL = True
    sys.argv.remove('-s')
#SAVE_MODEL = False
GENERATE_FULL = False
if '-g' in sys.argv:
    GENERATE_FULL = True
    sys.argv.remove('-g')
#GENERATE_FULL = True


def print_name() :
    print('MODEL_NUMBER = ' + MODEL_NUMBER)
    #print('BASE_MODEL_PATH = ' + BASE_MODEL_PATH)
    #print('BAGGING_MODEL_PATH = ' + BAGGING_MODEL_PATH)
    #print('BASE_LINE_NAME = ' + BASE_LINE_NAME)
    #print('BAGGING_MODEL_NAME = ' +  BAGGING_MODEL_NAME)
def generate(all_active_sents, all_y_active, unlabeled_orisents, unlabeled_nesents, unlabeled_sents, X_unlabeled, y_unlabeled) :
    active_dict = ner_generate.gen_active_dict(all_active_sents, all_y_active)
    unlabeled_sents_act, X_unlabeled_act, y_pred_act,unlabeled_sents_ml, X_unlabeled_ml, y_pred_ml=ner_generate.separate_hy(active_dict, unlabeled_sents, X_unlabeled, y_unlabeled)
    utils.write_result_from_ft('', '', X_unlabeled_act, y_pred_act, 'tmp_act_2nd_hy.txt')
    utils.write_result_from_ft('','',X_unlabeled_ml, y_pred_ml,'tmp_ml_2nd_hy.txt')

    return  st.SELF_LABELED_PATH+'actNmachine_' + MODEL_NUMBER + '.txt',  st.SELF_LABELED_PATH+'active_' + MODEL_NUMBER + '.txt',  st.SELF_LABELED_PATH+'machine_' + MODEL_NUMBER + '.txt'

def main() :
    summary = '=========================== summary ============================\n'
    if not os.path.exists(st.MODEL_DIR+ MODEL_NUMBER):
        os.makedirs(st.MODEL_DIR+ MODEL_NUMBER)
    #st.print_setting()
    print_name()
    st.write_log('Reading files\n', open=True, close=True)
   # _,_,test_sents, X_test, y_test = utils.read_labeled_text_data_dir(st.TEST_DIR, encoding=st.ENCODING)##20170912
   # _,_,train_sents, X_train, y_train = utils.read_labeled_text_data_dir(st.TRAIN_DIR, encoding=st.ENCODING)##20170912
    _,_,act_sents, X_act, y_act = utils.read_labeled_text_data_dir(st.ACT_DIR, encoding=st.ENCODING)
    #_,_,good_sents, X_good, y_good = utils.read_labeled_text_data_dir(st.GOOD_ML_DATA_DIR, encoding=st.ENCODING)
    unlabeled_orisents, unlabeled_nesents, unlabeled_sents, X_unlabeled, y_unlabeled = utils.read_labeled_text_data_dir(st.UNLABELED_DIR, encoding=st.ENCODING)
    #if len(unlabeled_orisents) != len(unlabeled_sents) :
    #    print('error! check the unlabeled input file!')


    anm,a,m = generate(act_sents, y_act,unlabeled_orisents, unlabeled_nesents, unlabeled_sents, X_unlabeled, y_unlabeled)


if __name__ == "__main__" :
    main()
