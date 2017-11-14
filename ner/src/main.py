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
BOOT_ITER = int(sys.argv[1])
#BOOT_ITER = 1
BASE_LINE_NAME = MODEL_NUMBER + '_base' + str(BOOT_ITER)
BAGGING_MODEL_NAME = MODEL_NUMBER + '_bagging' + str(BOOT_ITER)

LOAD_MODEL_N = BOOT_ITER * st.SELF_ITER_N #????
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
    print('BOOT_ITER = ' + str(BOOT_ITER))
    #print('BASE_LINE_NAME = ' + BASE_LINE_NAME)
    #print('BAGGING_MODEL_NAME = ' +  BAGGING_MODEL_NAME)
def generate(all_active_sents, all_y_active, unlabeled_orisents, unlabeled_nesents, unlabeled_sents, X_unlabeled, model) :
    active_dict = ner_generate.gen_active_dict(all_active_sents, all_y_active)
    print('making predictions for unlabeled full data')
    y_pred_unlabled, y_pred_prob = model.make_prediction(X_unlabeled, remove_all_o=False, min_conf=-1.0, link_pos=None)
    y_pred_including_act, y_prob_including_act, unlabeled_orisents_act, unlabeled_nesents_act, X_unlabeled_act, y_pred_act, y_prob_act, unlabeled_orisents_ml,\
    unlabeled_nesents_ml, X_unlabeled_ml,y_pred_ml, y_prob_ml = ner_generate.separate(active_dict, unlabeled_orisents, unlabeled_nesents, unlabeled_sents, X_unlabeled, y_pred_unlabled, y_pred_prob)
    if st.PROB_OUT == True :
        print('writing : ' + st.SELF_LABELED_PATH+ 'actNmachine_'+MODEL_NUMBER +'.txt')
        utils.write_result_from_ft(unlabeled_orisents, unlabeled_nesents, X_unlabeled, y_pred_including_act,  st.SELF_LABELED_PATH + 'actNmachine_'+MODEL_NUMBER +'.txt', yprob = y_prob_including_act)
        print('writing : ' + st.SELF_LABELED_PATH+ 'active_' + MODEL_NUMBER + '.txt')
        utils.write_result_from_ft(unlabeled_orisents_act, unlabeled_nesents_act, X_unlabeled_act, y_pred_act,
                                   st.SELF_LABELED_PATH + 'active_' + MODEL_NUMBER + '.txt', yprob=y_prob_act)
        print('writing : ' + st.SELF_LABELED_PATH+ 'machine_' + MODEL_NUMBER + '.txt')
        utils.write_result_from_ft(unlabeled_orisents_ml, unlabeled_nesents_ml, X_unlabeled_ml, y_pred_ml,
                                   st.SELF_LABELED_PATH + 'machine_' + MODEL_NUMBER + '.txt', yprob=y_prob_ml)
    else :
        print('writing : ' +  st.SELF_LABELED_PATH+'actNmachine_' + MODEL_NUMBER + '.txt')
        utils.write_result_from_ft(unlabeled_orisents, unlabeled_nesents, X_unlabeled, y_pred_including_act,
                                   st.SELF_LABELED_PATH + 'actNmachine_' + MODEL_NUMBER + '.txt')
        print('writing : ' + st.SELF_LABELED_PATH+ 'active_' + MODEL_NUMBER + '.txt')
        utils.write_result_from_ft(unlabeled_orisents_act, unlabeled_nesents_act, X_unlabeled_act, y_pred_act,
                                   st.SELF_LABELED_PATH + 'active_' + MODEL_NUMBER + '.txt')
        print('writing : ' +  st.SELF_LABELED_PATH+'machine_' + MODEL_NUMBER + '.txt')
        utils.write_result_from_ft(unlabeled_orisents_ml, unlabeled_nesents_ml, X_unlabeled_ml, y_pred_ml,
                                   st.SELF_LABELED_PATH + 'machine_' + MODEL_NUMBER + '.txt')
    return  st.SELF_LABELED_PATH+'actNmachine_' + MODEL_NUMBER + '.txt',  st.SELF_LABELED_PATH+'active_' + MODEL_NUMBER + '.txt',  st.SELF_LABELED_PATH+'machine_' + MODEL_NUMBER + '.txt'

def main() :
    summary = '=========================== summary ============================\n'
    if not os.path.exists(st.MODEL_DIR+ MODEL_NUMBER):
        os.makedirs(st.MODEL_DIR+ MODEL_NUMBER)
    #st.print_setting()
    print_name()
    st.write_log('Reading files\n', open=True, close=True)
    _,_,test_sents, X_test, y_test = utils.read_labeled_text_data_dir(st.TEST_DIR, encoding=st.ENCODING)##20170912
    _,_,train_sents, X_train, y_train = utils.read_labeled_text_data_dir(st.TRAIN_DIR, encoding=st.ENCODING)##20170912
    _,_,act_sents, X_act, y_act = utils.read_labeled_text_data_dir(st.ACT_DIR, encoding=st.ENCODING)
    _,_,good_sents, X_good, y_good = utils.read_labeled_text_data_dir(st.GOOD_ML_DATA_DIR, encoding=st.ENCODING)
    unlabeled_orisents, unlabeled_nesents, unlabeled_sents, X_unlabeled, y_unlabeled = utils.read_labeled_text_data_dir(st.UNLABELED_DIR, encoding=st.ENCODING)
    if len(unlabeled_orisents) != len(unlabeled_sents) :
        print('error! check the unlabeled input file!')

    X_basiccrf = X_train + X_act + X_good
    y_basiccrf = y_train + y_act + y_good

    if len(test_sents) > 1 :
        tester = myTagger(X_test=X_test, y_test=y_test, test_sents=test_sents)
    basic_CRF = BasicModel(BASE_MODEL_PATH, BASE_LINE_NAME)
    bagging_model = BaggingModel(BAGGING_MODEL_PATH, BAGGING_MODEL_NAME, num_of_comp_mds=st.NUM_BAGGING_MODEL,
                                 boot_sample_size=st.BOOTSTRAP_SAMPLE_SIZE / st.NUM_BAGGING_MODEL, X_labeled=X_train,
                                 y_labeled=y_train)

    st.write_log('Training Basic CRF', close=True, std_print=True)
    unlabeled_orisents_now = unlabeled_orisents[BOOT_ITER*st.BOOTSTRAP_SAMPLE_SIZE : (BOOT_ITER+1)*st.BOOTSTRAP_SAMPLE_SIZE]
    unlabeled_nesents_now = unlabeled_nesents[BOOT_ITER*st.BOOTSTRAP_SAMPLE_SIZE : (BOOT_ITER+1)*st.BOOTSTRAP_SAMPLE_SIZE]
    X_unlabeled_now = X_unlabeled[BOOT_ITER*st.BOOTSTRAP_SAMPLE_SIZE : (BOOT_ITER+1)*st.BOOTSTRAP_SAMPLE_SIZE]
    y_basiccrf,_,_ = utils._remove_all_o(y_basiccrf,[], [])
    if st.SELF_ITER_N == 1 :
        basic_CRF._add_n_train_CRF(X_basiccrf, y_basiccrf)
    else :
        basic_CRF.add_n_train_CRF(X_basiccrf, y_basiccrf, clear_past_model=True, add_total=True, write_added=True)
    if st.ALL_TEST is True :
        tester.eval_prediction(basic_CRF.make_prediction(tester.X_test,remove_all_o = False)[0])
    if GENERATE_FULL is True :
        anm,a,m = generate(act_sents, y_act,unlabeled_orisents, unlabeled_nesents, unlabeled_sents, X_unlabeled, basic_CRF)
        summary += '=generated full data\n' + '='+anm+'\n'+'='+a+'\n'+'='+m+'\n'
        #y_pred_u_full, y_mar_p_u_full = basic_CRF.make_prediction(X_unlabeled, remove_all_o= False, min_conf= -1.0, link_pos=None)
    y_pred_u = basic_CRF.make_prediction(X_unlabeled_now, remove_all_o=True, min_conf=st.FIXED_MIN_SEQ_PROB,link_pos=None)[0]
    print('Training Bagging CRF')
    bagging_model.set_selflabeled_data_n_train(X_unlabeled_now, y_pred_u)
    if st.ALL_TEST is True:
        y_pred_test, _ = bagging_model.make_prediction(tester.X_test, remove_all_o=False)
        tester.eval_prediction(y_pred_test)

    X_basiccrf = X_unlabeled_now
    if st.SELF_ITER_N ==1 :
        y_basiccrf, y_basiccrf_mar_p = bagging_model.make_prediction(X_basiccrf, remove_all_o=False, min_conf=st.FIXED_MIN_MARGINAL_PROB, link_pos=None,replace_o=False,mul_ne_cnt=False)

    elif st.SELF_ITER_N >1:
        y_basiccrf, y_basiccrf_mar_p = bagging_model.make_prediction(X_basiccrf, remove_all_o=True,min_conf=st.FIXED_MIN_MARGINAL_PROB, link_pos=None,replace_o=False, mul_ne_cnt=False)
        for boot_sub_iter in range(1, st.SELF_ITER_N):
            st.write_log('sub-iter : ' + str(boot_sub_iter) + '/' + str( st.SELF_ITER_N-1), open=True, std_print=True)
            print('sub : Training Basic CRF')
            basic_CRF.temp_add_n_train_CRF(X_basiccrf, y_basiccrf, boot_sub_iter)
            if st.ALL_TEST is True:
                tester.eval_prediction(basic_CRF.make_prediction(tester.X_test, remove_all_o=False)[0])
            y_pred_u = basic_CRF.make_prediction(X_unlabeled_now, remove_all_o=True,min_conf=st.FIXED_MIN_SEQ_PROB, link_pos=None)[0]
            print('sub : Training Bagging CRF')
            bagging_model.set_selflabeled_data_n_train(X_unlabeled_now, y_pred_u)
            if st.ALL_TEST is True:
                y_pred_test, _ = bagging_model.make_prediction(tester.X_test, remove_all_o=False)
                tester.eval_prediction(y_pred_test)
            X_basiccrf = X_unlabeled_now
            if boot_sub_iter < st.SELF_ITER_N -1 :
                y_basiccrf, y_basiccrf_mar_p = bagging_model.make_prediction(X_basiccrf,remove_all_o=True,min_conf=st.FIXED_MIN_MARGINAL_PROB,link_pos=None,replace_o=False,mul_ne_cnt=False)#remove all o false
            elif boot_sub_iter == st.SELF_ITER_N -1 :
                y_basiccrf, y_basiccrf_mar_p = bagging_model.make_prediction(X_basiccrf,remove_all_o=False,min_conf=st.FIXED_MIN_MARGINAL_PROB,link_pos=None,replace_o=False,mul_ne_cnt=False)#remove all o false

    #print out file & remove model dir
    active_assistant = Active_Assistant(st.active_min_prob, st.active_max_prob, st.GOOD_ML_DATA_DIR_OUT, st.ACT_DIR_OUT,BOOT_ITER)
    a, g = active_assistant.write_ML_data(unlabeled_orisents_now, unlabeled_nesents_now,X_basiccrf, y_basiccrf, y_basiccrf_mar_p)
    summary += '=generated bootstrapping data\n' + '=' + a + '\n' + '=' + g + '\n'
    if SAVE_MODEL == False :
        shutil.rmtree(st.MODEL_DIR+ MODEL_NUMBER + '/')
    else :
        shutil.rmtree(st.MODEL_DIR + MODEL_NUMBER + '/bagging_model/')
        if st.SELF_ITER_N > 1 :
            basic_CRF.remove_latest_model()
        summary += '=generated model\n' + '='+basic_CRF.get_first_model_name()+'\n'
    summary+= '================================================================\n'
    print(summary)


if __name__ == "__main__" :
    main()
