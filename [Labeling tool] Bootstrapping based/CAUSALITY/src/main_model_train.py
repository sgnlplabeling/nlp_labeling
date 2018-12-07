# -*- coding:utf-8 -*-
import time
from causality_evaluation import myTagger
from causality_basicmodel import BasicModel
from causality_baggingmodel import BaggingModel
from causality_load import Loader
import causality_utils as utils
import causality_settings as st
import os.path

if st.RELOAD is False :
    MODEL_NUMBER = time.strftime("%Y%m%d-%H%M%S")
    BASE_MODEL_PATH = '../'+ MODEL_NUMBER + '/base_model/'
    BASE_DATA_SAVE_PATH = '../'+ MODEL_NUMBER + '/base_data/'
    BAGGING_MODEL_PATH = '../'+ MODEL_NUMBER + '/bagging_model/'
    ACTIVE_DIR = '../' + MODEL_NUMBER + '/active_learning/'
    MACHINE_DIR = '../' + MODEL_NUMBER + '/machine_labeled/'
    BASE_LINE_NAME = MODEL_NUMBER + '_base'
    BAGGING_MODEL_NAME = MODEL_NUMBER + '_bagging'
#    START_ITER = 0
else :
    MODEL_NUMBER = st.LOADING_MODEL_NUMBER
    BASE_MODEL_PATH = st.LOADING_DIR+ 'base_model/'
    BASE_DATA_SAVE_PATH = st.LOADING_DIR + 'base_data/'
    st.LOG = '../' + MODEL_NUMBER + '/train.log'
    ACTIVE_DIR = '../' + MODEL_NUMBER + '/active_learning/'
    BAGGING_MODEL_PATH = st.LOADING_DIR + 'bagging_model/'
#    START_ITER = st.START_ITER
    BASE_LINE_NAME = st.LOADING_MODEL_NUMBER + '_base'
    BAGGING_MODEL_NAME = st.LOADING_MODEL_NUMBER + '_bagging'

LOAD_MODEL_N = st.START_ITER
def write_result(test_sents, y_pred, ori_sents,file_path,file_full_name):
    if not os.path.isdir(file_path):
        os.mkdir(file_path)

    with open(file_full_name, 'w') as wf:
        for s_idx in range(len(test_sents)):
            str1 = ";"
            for i in ori_sents[s_idx]:
                str1+=i
            
            wf.write(str1.encode('utf-8')+"\n")
            for tup_idx in range(len(test_sents[s_idx])):
                mark = ''
                if test_sents[s_idx][tup_idx][3] != y_pred[s_idx][tup_idx]:
                    mark = '$$'
                out_str = test_sents[s_idx][tup_idx][0] + ' ' + test_sents[s_idx][tup_idx][1] + ' ' + test_sents[s_idx][tup_idx][2] + ' '\
                + y_pred[s_idx][tup_idx] +'\n'
                wf.write(out_str.encode('utf-8'))
            wf.write('\n'.encode('utf-8'))


def print_name() :
    print('MODEL_NUMBER = ' + MODEL_NUMBER)
    print('BASE_MODEL_PATH = ' + BASE_MODEL_PATH)
    print('BASE_DATA_SAVE_PATH = ' + BASE_DATA_SAVE_PATH)
    print('BASE_LINE_NAME = ' + BASE_LINE_NAME)
    print('ACTIVE_PATH = ' + ACTIVE_DIR)
    print('BAGGING_MODEL_PATH = ' + BAGGING_MODEL_PATH)
    print('BAGGING_MODEL_NAME = ' + BAGGING_MODEL_NAME+'\n')

def main() :
    if not os.path.exists('../'+ MODEL_NUMBER):
        os.makedirs('../'+ MODEL_NUMBER)
    if st.RELOAD == True :
        print('---------reload---------')
    st.print_setting()
    print_name()
    print ('Reading files')
    test_original_sents, test_sents, X_test, y_test = utils.read_labeled_text_data('../data/causality/' + st.TEST_FILE, encoding=st.ENCODING)##20170912
    train_original_sents, train_sents, X_train, y_train = utils.read_labeled_text_data('../data/causality/' + st.TRAIN_FILE, encoding=st.ENCODING)##20170912
    unlabeled_original_sents, unlabeled_sents, X_unlabeled, y_unlabeled = utils.read_labeled_text_data('../data/unlabeled_data/' + st.UNLABELED_FILE, encoding=st.ENCODING)
    #print len(test_sents), len(test_original_sents), len(train_sents), len(train_original_sents), len(unlabeled_sents), len(unlabeled_original_sents)

    if st.RELOAD is False :
        X_basiccrf = X_train
        y_basiccrf = y_train
        y_basiccrf_mar_p = utils.generate_all(y_basiccrf, 1)
    else :
        loader = Loader(BASE_DATA_SAVE_PATH, LOAD_MODEL_N)
        X_basiccrf = loader.get_X()
        y_basiccrf = loader.get_y()
        y_basiccrf_mar_p = loader.get_yprob()

    X_unlabeled_ori_sents_devied = utils.split_set_w_size(unlabeled_original_sents,st.BOOTSTRAP_SAMPLE_SIZE,st.BOOT_ITER_LIMIT)
    X_unlabeled_devied = utils.split_set_w_size(X_unlabeled,st.BOOTSTRAP_SAMPLE_SIZE,st.BOOT_ITER_LIMIT)
    X_unlabeled_sents_devied = utils.split_set_w_size(unlabeled_sents, st.BOOTSTRAP_SAMPLE_SIZE, st.BOOT_ITER_LIMIT)
    #print len(X_unlabeled_ori_sents_devied), len(X_unlabeled_devied), len(X_unlabeled_sents_devied)
    tester = myTagger(X_test=X_test, y_test=y_test, test_sents=test_sents)
    basic_CRF = BasicModel(BASE_MODEL_PATH, BASE_LINE_NAME, BASE_DATA_SAVE_PATH, st.START_ITER)
    bagging_model = BaggingModel(BAGGING_MODEL_PATH, BAGGING_MODEL_NAME, num_of_comp_mds=st.NUM_BAGGING_MODEL,
                                 boot_sample_size=st.BOOTSTRAP_SAMPLE_SIZE / st.NUM_BAGGING_MODEL, X_labeled=X_train,
                                 y_labeled=y_train, save_path=None, start_iter = st.START_ITER)

    cnt = 0
    c = []
    for i in range(10):
        c.append(0)


    for boot_iter in range(st.START_ITER, len(X_unlabeled_devied)):
        print ('boot : ' + str(boot_iter) + '/' + str(len(X_unlabeled_devied)))
        print('Training Basic CRF(for)')


        X_unlabeled_now = X_unlabeled_devied[boot_iter]
        X_unlabeled_sents_now = X_unlabeled_sents_devied[boot_iter]
        X_unlabeled_ori_sents_now = X_unlabeled_ori_sents_devied[boot_iter]

        X_unlabeled_7_data = []
        X_unlabeled_8_data = []
        X_unlabeled_9_data = []

        for i in range(4):
            X_unlabeled_7_data.append(list())
            X_unlabeled_8_data.append(list())
            X_unlabeled_9_data.append(list())


        if boot_iter == 0:
            basic_CRF.add_n_train_CRF(X_basiccrf, y_basiccrf,y_basiccrf_mar_p)
        else:
            basic_CRF.add_n_train_CRF(X_basiccrf, y_basiccrf,y_basiccrf_mar_p)
            
        tester.eval_prediction(test_sents,basic_CRF.make_prediction(tester.X_test,remove_all_o = False)[0])
        y_pred_u, y_pred_u_probs= basic_CRF.make_prediction(X_unlabeled_now, remove_all_o=st.REMOVE_ALL_ZERO, min_conf=st.FIXED_MIN_SEQ_PROB)

        if st.BAGGING is False :
            X_basiccrf = X_unlabeled_now
            y_basiccrf = y_pred_u
            y_basiccrf_mar_p = None
            continue
        print('Training Bagging CRFs')
        bagging_model.set_selflabeled_data_n_train(X_unlabeled_sents_now, X_unlabeled_now, y_pred_u, y_pred_u_probs)
        y_pred_test, _ = bagging_model.make_prediction(tester.X_test, remove_all_o=False)
        tester.eval_prediction(test_sents,y_pred_test)
        X_basiccrf = X_unlabeled_now
        y_basiccrf, y_basiccrf_mar_p = bagging_model.make_prediction(X_basiccrf,
                                                                     remove_all_o=st.REMOVE_ALL_ZERO,
                                                                     min_conf=st.FIXED_MIN_MARGINAL_PROB if st.VOTE_ON_DIST is True else st.FIXED_MIN_PERC_OF_VOTES)
        for i in range(len(y_basiccrf)):
            if len(y_basiccrf_mar_p[i]) != 0:
                if min(y_basiccrf_mar_p[i])>=0.7 and min(y_basiccrf_mar_p[i])<0.8:
                    X_unlabeled_7_data[0].append(str(i)+' '+X_unlabeled_ori_sents_now[i])
                    X_unlabeled_7_data[1].append(X_unlabeled_sents_now[i])
                    X_unlabeled_7_data[2].append(y_basiccrf[i])
                    X_unlabeled_7_data[3].append(y_basiccrf_mar_p[i])
                elif min(y_basiccrf_mar_p[i])>=0.8 and min(y_basiccrf_mar_p[i])<0.9:
                    X_unlabeled_8_data[0].append(str(i)+' '+X_unlabeled_ori_sents_now[i])
                    X_unlabeled_8_data[1].append(X_unlabeled_sents_now[i])
                    X_unlabeled_8_data[2].append(y_basiccrf[i])
                    X_unlabeled_8_data[3].append(y_basiccrf_mar_p[i])
                elif min(y_basiccrf_mar_p[i])>=0.9:
                    X_unlabeled_9_data[0].append(X_unlabeled_ori_sents_now[i])
                    X_unlabeled_9_data[1].append(X_unlabeled_sents_now[i])
                    X_unlabeled_9_data[2].append(y_basiccrf[i])
                    X_unlabeled_9_data[3].append(y_basiccrf_mar_p[i])

       # print len(X_unlabeled_9_data[2]), len(X_unlabeled_8_data[2]), len(X_unlabeled_7_data[2])
        

        write_result(X_unlabeled_9_data[1], X_unlabeled_9_data[2],X_unlabeled_9_data[0], MACHINE_DIR, MACHINE_DIR+str(boot_iter)+'.bio')
        write_result(X_unlabeled_7_data[1], X_unlabeled_7_data[2],X_unlabeled_7_data[0], ACTIVE_DIR, ACTIVE_DIR+str(boot_iter)+'_7.bio')
        write_result(X_unlabeled_8_data[1], X_unlabeled_8_data[2],X_unlabeled_8_data[0], ACTIVE_DIR, ACTIVE_DIR+str(boot_iter)+'_8.bio')

        for i in range(len(y_basiccrf)):
            if len(y_basiccrf_mar_p[i]) != 0:
                if 0.0<min(y_basiccrf_mar_p[i]) and min(y_basiccrf_mar_p[i])<0.1:
                    c[0]+=1
                elif 0.1<=min(y_basiccrf_mar_p[i]) and min(y_basiccrf_mar_p[i])<0.2:
                    c[1]+=1
                elif 0.2<=min(y_basiccrf_mar_p[i]) and min(y_basiccrf_mar_p[i])<0.3:
                    c[2]+=1
                elif 0.3<=min(y_basiccrf_mar_p[i]) and min(y_basiccrf_mar_p[i])<0.4:
                    c[3]+=1
                elif 0.4<=min(y_basiccrf_mar_p[i]) and min(y_basiccrf_mar_p[i])<0.5:
                    c[4]+=1
                elif 0.5<=min(y_basiccrf_mar_p[i]) and min(y_basiccrf_mar_p[i])<0.6:
                    c[5]+=1
                elif 0.6<=min(y_basiccrf_mar_p[i]) and min(y_basiccrf_mar_p[i])<0.7:
                    c[6]+=1
                elif 0.7<=min(y_basiccrf_mar_p[i]) and min(y_basiccrf_mar_p[i])<0.8:
                    c[7]+=1
                elif 0.8<=min(y_basiccrf_mar_p[i]) and min(y_basiccrf_mar_p[i])<0.9:
                    c[8]+=1
                elif 0.9<=min(y_basiccrf_mar_p[i]) and min(y_basiccrf_mar_p[i])<=1.0:
                    c[9]+=1
        # print("태깅중! 잘못된 문장 번호를 입력하시고, 태깅이 완료 되었다면 x를 입력해 주세요")
        # wrong_num = []
        # while True:
        #     inp = raw_input()
        #     if inp == "x":
        #         break
        #     else:
        #         wrong_num.append(int(inp))
        # for i in range(len(wrong_num)):
        #     y_basiccrf[wrong_num[i]] = []
        #     y_basiccrf_mar_p[wrong_num[i]] = []

    boot_iter += 1
    print('boot : ' + str(boot_iter) + '/' + str(len(X_unlabeled_devied)))
    print('Training Basic CRF')

    basic_CRF.add_n_train_CRF(X_basiccrf, y_basiccrf, y_basiccrf_mar_p)

    tester.eval_prediction(test_sents,basic_CRF.make_prediction(tester.X_test, remove_all_o = False)[0])
if __name__ == "__main__" :
    main()
