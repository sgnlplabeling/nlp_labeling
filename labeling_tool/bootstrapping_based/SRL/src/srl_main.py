#-*- coding: utf-8 -*-
import numpy as np
from data_utils import main_bootstrap, split_self_labeling, load_cluster, bagging_bootstrap, load_weight_matrix
from config import Config
from tagger import Tagger

config = Config

# config.word2cluster : K-Means 알고리즘을 사용하여 사전에 분류된 술어 군집 dict
# config.weight_matrix : weighted voting 에서 사용되는 각 weight_matrix
# config.label2idx, config.idx2label : 정답 dict
config.word2cluster = load_cluster()
config.weight_matrix, config.label2idx, config.idx2label = load_weight_matrix()


def AIC_train():
    # bootstrapping에 사용되는 학습데이터는 "PIC_train"을 통해 PIC 처리를 사전에 진행해야 함.
    for epoch in range(1, config.boot_iter):
        print ("iter : ", config.iter)
        main_tagger_AIC = Tagger()
        main_tagger_AIC.main_trainAIC()
        main_tagger_AIC.evaluateAIC("main_model")
        self_trainig = main_tagger_AIC.main_taggingAIC(mode="self_tagging") # init self training data\

        # 배깅 모델 학습
        splited_labels, splited_features, splited_sentences = split_self_labeling(self_trainig[0], self_trainig[1], self_trainig[2])
        print("%s_iter(main) -> self_labled_s1 : %s" % (config.iter, len(self_trainig[0])))

        for model_idx in range(1, config.model_num+1):
            print("model_idx : ", model_idx)
            bagging_taggerAIC = Tagger()
            bagging_taggerAIC.bagging_trainAIC("bagging_train", model_idx, splited_features[model_idx-1], splited_labels[model_idx-1])
            print("bagging model%s acc" % model_idx)
            bagging_taggerAIC.evaluateAIC("bagging_eval", model_idx) # each bagging model
            bagging_bootstrap(model_idx, splited_sentences[model_idx-1], splited_labels[model_idx-1])

            if model_idx == 1 : score_i, raw_sentences, features = bagging_taggerAIC.bagging_taggingAIC("self_tagging", model_idx)
            else:
                new_socre_i = bagging_taggerAIC.bagging_taggingAIC("self_tagging", model_idx)
                for idx, _ in enumerate(new_socre_i):
                    score_i[idx] = np.asarray(score_i[idx]) + np.asarray(new_socre_i[idx])

        predicts = bagging_taggerAIC.score2tag(score_i, raw_sentences, features)
        main_bootstrap(predicts)
        config.iter += 1

def AIC_predict():
    print("iter : ", config.iter)
    # 형태소분석된 raw_sentence에 PIC 처리
    # input : config.result_input_path
    # output : config.result_processed_path
    main_tagger_PIC = Tagger()
    main_tagger_PIC.taggingPIC("result_tagging")
    
    # PIC 처리된 raw_sentence에 AIC 적용
    # input : config.result_processed_path
    # output : config.result_output_path
    main_tagger_AIC = Tagger()
    main_tagger_AIC.evaluateAIC("result")
    main_tagger_AIC.main_taggingAIC(mode="result_tagging")

def PIC_train():
    # bootstrapping 에 사용될 unlabeled 학습데이터에 PIC 를 적용하는 과정
    # train_set : config.trainPIC_path
    # test_set : config.testPIC_path
    main_tagger_PIC = Tagger()
    main_tagger_PIC.main_trainPIC()
    main_tagger_PIC.evaluatePIC()

def PIC_predict():
    # input : config.tagging_input_path
    # output : config.tagging_output_path
    main_tagger_PIC = Tagger()
    main_tagger_PIC.evaluatePIC()
    main_tagger_PIC.taggingPIC("PIC_tagging")

if __name__ == "__main__":
    if config.mode == "AIC_train":
        # bootstrapping 진행, 대용량 unlabled 학습데이터에 사전에 PIC 처리해야 함.
        AIC_train()
    elif config.mode == "PIC_train":
        # PIC model 학습
        PIC_train()
    elif config.mode == "PIC_predict":
        # 학습에 사용될 대용량 코퍼스에 PIC 작업 진행
        PIC_predict()
    elif config.mode == "AIC_predict":
        # 학습된 crf model 을 사용하여 태깅, PIC 작업 필수 X
        AIC_predict()
