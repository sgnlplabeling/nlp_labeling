#-*- coding: utf-8 -*-

import pycrfsuite
import os
import numpy as np

from feature_func import feature_func
from config import Config
from itertools import chain
from data_utils import readDataAIC, readDataPIC, mergePIC, constraint_tag_num, get_model_path, result_write

config = Config

class Tagger():
    def __init__(self):
        # CRF Class 생성
        # _featureFunc : 자질 추출 function
        self._tagger = pycrfsuite.Tagger()
        self._featureFunc = feature_func

    def main_trainAIC(self):
        # main crf model 학습
        trainer = pycrfsuite.Trainer(verbose=True)
        trainer.set_params({
            'c1': config.c1,  # coefficient for L1 penalty
            'c2': config.c2,  # coefficient for L2 penalty
            'max_iterations': config.maxiter,
            'feature.possible_transitions': config.possible_transitions
        })

        raw_setntences, morphs, poss, predicate_idxs, labels, predicate_classes = readDataAIC("main_trainAIC")
        for (raw_sentence, sentence, pos, predicate_idx, label, predicate_class) in zip(raw_setntences, morphs, poss, predicate_idxs, labels, predicate_classes):
            features = [self._featureFunc(config.model, sentence, pos, predicate_idx, predicate_class, global_idx)
                for global_idx in range(len(sentence))]
            trainer.append(features, label)
        model_path = config.main_model_AIC_path % (config.iter)
        trainer.train(model_path)

    def bagging_trainAIC(self, mode, model_idx, self_labeled_features, self_labeled_labels):
        # 매 iteration마다, 각 bagging model 학습
        trainer = pycrfsuite.Trainer(verbose=config.verbose)
        trainer.set_params({
            'c1': config.c1,  # coefficient for L1 penalty
            'c2': config.c2,  # coefficient for L2 penalty
            'max_iterations': config.maxiter,  # stop earlier ****
            'feature.possible_transitions': config.possible_transitions
        })

        raw_sentences, morphs, poss, predicate_idxs, labels, predicate_classes = readDataAIC(mode, model_idx)
        for (raw_sentence, sentence, pos, predicate_idx, label, predicate_class) in zip(raw_sentences, morphs, poss, predicate_idxs, labels,
                                                                          predicate_classes):
            if len(sentence) == 0: continue
            features = [
                self._featureFunc(config.model, sentence, pos, predicate_idx, predicate_class, global_idx)
                for global_idx in range(len(sentence))]
            trainer.append(features, label)

        # self-tagging 데이터를 배깅 학습데이터에 추가
        for idx, feature in enumerate(self_labeled_features):
            trainer.append(feature, self_labeled_labels[idx])

        if not os.path.isdir('/'.join(config.bagging_model_path.split("/")[:-1])%(config.iter)):
            os.mkdir('/'.join(config.bagging_model_path.split("/")[:-1])%(config.iter))
        model_path = config.bagging_model_path % (config.iter, model_idx)
        trainer.train(model_path)

    def bagging_taggingAIC(self, mode, model_idx):
        # 학습한 bagging model을 이용하여 다시 동일한 데이터에 self-tagging
        self._tagger.open(config.bagging_model_path % (config.iter, model_idx))
        raw_sentences, morphs, poss, pred_idxs, labels, pred_means = readDataAIC(mode)
        scores, features, sentences = [], [], []

        for (raw_sentence, sentence, pos, pred_idx, pred_mean) in zip(raw_sentences, morphs, poss, pred_idxs, pred_means):
            score = []
            if len(sentence) == 0: continue

            feature = [self._featureFunc(config.model, sentence, pos, pred_idx, pred_mean, global_idx) for global_idx in range(len(sentence))]
            predict = self._tagger.tag(feature)

            if model_idx == 1:
                features.append(feature)
            
            # 각 모델별 가중치 적용
            for p_idx, pred in enumerate(predict):
                s = []
                for l_idx in range(len(config.label2idx)):
                    if config.idx2label[l_idx] == "PAD" : continue
                    s.append(float(config.weight_matrix["WEIGHT1_model_%s_%s" % (model_idx, config.idx2label[l_idx])])
                             * (self._tagger.marginal(config.idx2label[l_idx], p_idx)))
                score.append(s)
            scores.append(score)
            sentences.append(raw_sentence)

        if model_idx == 1 : return np.asarray(scores), sentences, features
        else: return np.asarray(scores)

    def main_taggingAIC(self, mode=None):
        # main crf를 사용하여 unlabeled 에 대하여 self-tagging 진행
        
        if mode == "self_tagging": model_path = config.main_model_AIC_path % (config.iter)
        elif mode == "result_tagging": model_path = config.result_model_path
        print ("load to ", model_path)
        self._tagger.open(model_path)
        raw_setences, morphs, pumsas, pred_idxs, labels, pred_means = readDataAIC(mode)
        self_labeled_features, self_labeled_labels, self_labeled_sentences = [], [], []

        for idx, (raw_sentence, morph, pos, pred_idx, pred_mean) in enumerate(zip(raw_setences, morphs, pumsas, pred_idxs, pred_means)):
            if len(morph) == 0: continue
            feature = [self._featureFunc(config.model, morph, pos, pred_idx, pred_mean, global_idx)
                for global_idx in range(len(morph))]
            predict = self._tagger.tag(feature)

            # constraint
            if mode == "self_tagging":
                if self._tagger.probability(predict) >= config.confidence_socre and constraint_tag_num(predict) == False:
                    self_labeled_labels.append(predict)
                    self_labeled_features.append(feature)
                    self_labeled_sentences.append(raw_sentence)
            elif mode == "result_tagging":
                self_labeled_labels.append(predict)
                self_labeled_sentences.append(raw_sentence)

        if mode == "result_tagging":
            result_write(self_labeled_labels, self_labeled_sentences)

        return self_labeled_labels, self_labeled_features, self_labeled_sentences

    def main_trainPIC(self):
        trainer = pycrfsuite.Trainer(verbose=True)
        trainer.set_params({
            'c1': config.c1,  # coefficient for L1 penalty
            'c2': config.c2,  # coefficient for L2 penalty
            'max_iterations': config.maxiter,  # stop earlier ****
            'feature.possible_transitions': config.possible_transitions
        })

        words, pumsas, labels, _ = readDataPIC("train")
        for (word, pumsa, label) in zip(words, pumsas, labels):
            if len(word) == 0: continue
            features = [
                self._featureFunc("PIC", word, pumsa, None, None, global_idx) for global_idx in range(len(word))]
            trainer.append(features, label)
        trainer.train(config.modelPIC_path)

    def taggingPIC(self, mode):
        self._tagger.open(config.modelPIC_path)
        predicts = []
        morphs, poss, _, sentences = readDataPIC(mode)
        for (morph, pos) in zip(morphs, poss):
            if len(morph) == 0: continue
            features = [self._featureFunc("PIC", morph, pos, None, None, global_idx) for global_idx
                        in range(len(morph))]
            predict = self._tagger.tag(features)
            predicts.append([pred for pred in predict])

        mergePIC(predicts, sentences, mode)

    def evaluatePIC(self):
        self._tagger.open(config.modelPIC_path)
        self.predictPIC()

    def evaluateAIC(self, mode, model_idx=None):
        # 학습된 crf model F1 성능 평가
        model_path = get_model_path(mode, model_idx)
        self._tagger.open(model_path)
        self.predictAIC("eval", model_idx)

    def get_f1(self, predicts, labels):
        label_y_combined = [config.label2idx[token] for token in list(chain.from_iterable(labels))]
        pred_y_combined = [config.label2idx[token] for token in list(chain.from_iterable(predicts))]

        recall_count = 0.
        recall_total = 0.
        precision_count = 0.
        precision_total = 0.

        for idx, _ in enumerate(label_y_combined):
            if label_y_combined[idx] != config.label2idx["O"]: #recall
                recall_total += 1
                if label_y_combined[idx] == pred_y_combined[idx]:
                    recall_count += 1

            if pred_y_combined[idx] != config.label2idx["O"]:
                precision_total += 1
                if label_y_combined[idx] == pred_y_combined[idx]:
                    precision_count += 1

        recall = recall_count / recall_total
        precision = precision_count / precision_total
        f1 = (2 * recall * precision) / (recall + precision)
        print("F1 : %s, RECALL : %s, PRECISION : %s" % (str(f1), str(recall), str(precision)))

    def predictPIC(self):
        predicts = []
        morphs, poss, labels, _ = readDataPIC("valid")
        for (sentence, pos, label) in zip(morphs, poss, labels):
            if len(sentence) == 0: continue
            features = [self._featureFunc("PIC", sentence, pos, None, None, global_idx) for global_idx
                        in range(len(sentence))]
            predict = self._tagger.tag(features)
            predicts.append([pred for pred in predict])

        self.get_f1(predicts, labels)

    def predictAIC(self, mode, model_idx=None):
        predicts = []
        raw_sentences, morphs, poss, predicate_idxs, labels, predicate_classes = readDataAIC(mode, model_idx)
        for (raw_sentence, sentence, pos, predicate_idx, label, predicate_class) in zip(raw_sentences, morphs, poss, predicate_idxs, labels, predicate_classes):
            features = [self._featureFunc(config.model, sentence, pos, predicate_idx, predicate_class, global_idx)
                for global_idx in range(len(sentence))]
            predict = self._tagger.tag(features)
            predicts.append([pred for pred in predict])

        self.get_f1(predicts, labels)

    def score2tag(self, score, raw_sentences, features):
        # bagging model의 결과 중 상위 socre를 가진 결과를 최종 출력 return
        predicts = []
        predict_labels = []
        for sen_idx, sentence in enumerate(score):
            predict = []
            for token in sentence:
                argmax_idx= np.argmax(token)
                token = config.idx2label[argmax_idx+1]
                predict.append(token)

            self._tagger.set(features[sen_idx])
            if self._tagger.probability(predict) >= config.confidence_socre \
                    and constraint_tag_num(predict) == False:
                predicts.append(raw_sentences[sen_idx].strip() + "|||"+ ' '.join(str(p) for p in predict))
                predict_labels.append(predict)
        print("%s_iter(Ensemble) -> self_labled num : %s" % (config.iter, len(predicts)))
        return predicts