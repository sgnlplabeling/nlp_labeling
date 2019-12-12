# -*- coding: utf-8 -*-

import os
from config import Config
import math

config = Config

def load_cluster():
    word2cluster = {}
    with open(config.cluter_path, "r") as f:
        for line in f.readlines():
            word, cluster = line.split("\t")
            word2cluster[word] = int(cluster.strip())
    return word2cluster

def mergePIC(predicts, sentences, mode):
    processed_sentences = []
    for line_idx, line in enumerate(sentences):
        if line.strip() == "": continue
        num_predicates, pred_idx, pred_mean = get_PIC_features(predicts[line_idx])
        for p_idx in range(num_predicates):
            processed_sentences.append(pred_idx[p_idx] + " " + pred_mean[p_idx] + " " + line.strip())

    if mode == "result_tagging":
        filename = config.result_processed_path
    elif mode == "PIC_tagging":
        filename = config.tagging_output_path

    with open(filename, "w") as f:
        for sentence_idx, sentence in enumerate(processed_sentences):
            f.write(sentence)
            if sentence_idx + 1 != len(processed_sentences):
                f.write("\n")

def get_PIC_features(predict):
    num_predicates = 0
    pred_idx = []
    pred_mean = []
    for p_idx, p in enumerate(predict):
        if p != "O":
            num_predicates += 1
            pred_idx.append(str(p_idx))
            pred_mean.append(str(p))
    return num_predicates, pred_idx, pred_mean

def get_data_path(mode, model_idx=None):
    if mode == "main_trainAIC":
        filename = config.main_corpus_AIC_path % config.iter
    elif mode == "eval":
        filename = config.testAIC_path
    elif mode == "self_tagging":
        filename = config.unlabeled_corpus_path
    elif mode == "bagging_train":
        if config.iter == 1: filename = config.main_corpus_AIC_path % config.iter
        else:filename = config.bagging_corpus_path % (config.iter-1, model_idx)
    elif mode == "bagging_bootstrap":
        if config.iter == 1: filename = config.main_corpus_AIC_path % config.iter
        else: filename = config.bagging_corpus_path % (config.iter-1, model_idx)
    elif mode == "main_bootstrap":
        if config.iter == 1: filename = config.main_corpus_AIC_path % config.iter
        else:filename = config.main_corpus_AIC_path % (config.iter)
    elif mode == "result_tagging":
        filename = config.result_processed_path

    return filename

def get_model_path(mode, model_idx=None):
    if mode == "main_model":
        model_path = config.main_model_AIC_path % config.iter
    elif mode == "bagging_eval":
        model_path = config.bagging_model_path % (config.iter, model_idx)
    elif mode == "bagging":
        model_path = config.bagging_model_path % (config.iter, model_idx)
    elif mode == "result":
        model_path = config.result_model_path

    return model_path

def readDataAIC(mode, model_idx=None):
    # AIC 전용 data read module
    filename = get_data_path(mode, model_idx)
    raw_sentences, sentences, posResults, labels, predicate_idxs, predicate_classes = [], [], [], [], [], []
    with open(filename, "r") as f:
        if "tagging" in mode:
            lines = f.readlines()[int((config.iter-1) * int(config.sample_num)):
                                  int((config.iter) * int(config.sample_num))]
        else: lines = f.readlines()

        for line_idx, line in enumerate(lines):
            if "tagging" not in mode:
                line, label = line.strip().split("|||")
            # if "++" in line: continue
            raw_sentence = line
            predicate_idx = line.split()[0]
            predicate_class = line.split()[1]
            sentence = line.split()[2:]

            pos, lex = [], []
            for word in sentence:
                tmp_pos, tmp_lex = [], []
                for w in word.split("+"):
                    idx = w.rfind("/")
                    if w[:idx].isdigit() :
                        tmp_lex.append("$NUM$")
                    else: tmp_lex.append(w)
                    tmp_pos.append(w[idx + 1:])

                pos.append(tmp_pos)
                lex.append(tmp_lex)

            if "tagging" not in mode:
                label = ["O" if l == "_" else l for l in label.split()]
                labels.append([l for l in label])
            raw_sentences.append(raw_sentence)
            predicate_idxs.append(predicate_idx)
            predicate_classes.append(predicate_class)
            sentences.append(lex)
            posResults.append(pos)

    return raw_sentences, sentences, posResults, predicate_idxs, labels, predicate_classes

def get_predicate(predi_eojoel):
    flag = 0
    for e in predi_eojoel:
        pred_pumsa = e.split("/")[-1]
        if pred_pumsa in config.V_PUMSA:
            flag = 1
            break
        if pred_pumsa in config.N_PUMSA:
            flag = 1
            break
    if flag == 0:
        e = predi_eojoel[0]

    return e

def readDataPIC(mode):
    if mode == "train":
        filename = config.trainPIC_path
    elif mode == "valid":
        filename = config.testPIC_path
    elif mode == "PIC_tagging":
        filename = config.tagging_input_path
    elif mode == "result_tagging":
        filename = config.result_input_path

    sentences, words, pumsas, labels = [], [], [], []
    with open(filename, "r") as f:
        for line in f.readlines():
            if len(line.strip()) == 0:
                words.append(word)
                pumsas.append(pumsa)
                word, pumsa = [], []
                continue
            word, pumsa = [], []
            sentences.append(line.strip())
            if "tagging" not in mode:
                line, label = line.split("|||")
                line = line.split()
            else:
                line = line.split()

            for token in line:
                tmp_pumsa, tmp_word = [], []
                for morph in token.split("+"):
                    idx = morph.rfind("/")
                    tmp_pumsa.append(morph[idx+1:])
                    tmp_word.append(morph)

                pumsa.append(tmp_pumsa)
                word.append(tmp_word)

            if "tagging" not in mode:
                labels.append(label.split())

            words.append(word)
            pumsas.append(pumsa)

    return words, pumsas, labels, sentences


def main_bootstrap(predicts):
    # main_train_corpus에 배깅으로 최종 생성된 상위 score 데이터 추가.
    filename = get_data_path("main_bootstrap")
    with open(filename, "r") as f:
        lines = f.readlines()
    lines += predicts

    with open(config.main_corpus_AIC_path % str(config.iter + 1), "w") as f:
        for line_idx, line in enumerate(lines):
            if line_idx != len(lines) - 1:
                f.write(line.strip() + "\n")

def result_write(labels, sentences):
    # result mode에서 태깅한 결과 file write
    with open(config.result_output_path, "w") as f:
        for idx, sentence in enumerate(sentences):
            line = sentence.strip()+"|||" + " ".join(label for label in labels[idx])
            f.write(line+"\n")

def self_traing2predicts(self_training):
    predicts = []
    labels, _, raw_sentences = self_training
    for idx, label in enumerate(labels):
        predicts.append(raw_sentences[idx].strip() + "|||" + ' '.join(label))

    return predicts

def bagging_bootstrap(model_idx, sentences, labels):
    # bagging 데이터를 이전 학습데이터와 merge한 후, file write하는 과정
    filename = get_data_path("bagging_bootstrap", model_idx)
    with open(filename, "r") as f:
        lines = f.readlines()
        for idx, sentence in enumerate(sentences):
            lines.append(sentence.strip() + "|||" + ' '.join(labels[idx]))

        if not os.path.exists('/'.join(config.bagging_corpus_path.split("/")[:-1]) % (config.iter)):
            os.mkdir('/'.join(config.bagging_corpus_path.split("/")[:-1]) % (config.iter))
        with open(config.bagging_corpus_path % (config.iter, model_idx), "w") as f:
            for line in lines:
                f.write(line.strip() + "\n")

def split_self_labeling(labels, features, raw_sentences):
    # self_tagging 결과를 술어 군집정보를 사용하여 split

    splited_labels, splited_features, splited_sentences = [], [], []
    model1_labels, model2_labels, model3_labels, model4_labels, model5_labels = [], [], [], [], []
    model1_features, model2_features, model3_features, model4_features, model5_features = [], [], [], [], []
    model1_sentences, model2_sentences, model3_sentences, model4_sentences, model5_sentences = [], [], [], [], []

    for idx, raw_sentence in enumerate(raw_sentences):
        predi_idx = int(raw_sentence.split()[0])
        predi = raw_sentence.split()[predi_idx + 2]
        e = get_predicate(predi.split("+"))

        if e in config.word2cluster:
            if config.word2cluster[e] == 0:
                model1_labels.append(labels[idx])
                model1_features.append(features[idx])
                model1_sentences.append(raw_sentences[idx])

            elif config.word2cluster[e] == 1:
                model2_labels.append(labels[idx])
                model2_features.append(features[idx])
                model2_sentences.append(raw_sentences[idx])

            elif config.word2cluster[e] == 2:
                model3_labels.append(labels[idx])
                model3_features.append(features[idx])
                model3_sentences.append(raw_sentences[idx])

            elif config.word2cluster[e] == 3:
                model4_labels.append(labels[idx])
                model4_features.append(features[idx])
                model4_sentences.append(raw_sentences[idx])

            elif config.word2cluster[e] == 4:
                model5_labels.append(labels[idx])
                model5_features.append(features[idx])
                model5_sentences.append(raw_sentences[idx])

    splited_labels.append(model1_labels)  # model2_labels + model3_labels + model4_labels + model5_labels
    splited_labels.append(model2_labels)
    splited_labels.append(model3_labels)
    splited_labels.append(model4_labels)
    splited_labels.append(model5_labels)

    splited_features.append(model1_features)  # = model1_features + model2_features + model3_features + model4_features + model5_features
    splited_features.append(model2_features)
    splited_features.append(model3_features)
    splited_features.append(model4_features)
    splited_features.append(model5_features)

    splited_sentences.append(model1_sentences)
    splited_sentences.append(model2_sentences)
    splited_sentences.append(model3_sentences)
    splited_sentences.append(model4_sentences)
    splited_sentences.append(model5_sentences)

    return splited_labels, splited_features, splited_sentences


def check_all_O_tag(predict):
    for p in predict:
        if p != "O":
            return False
    return True


def constraint_tag_num(predict):
    count = 0
    for p in predict:
        if p != "O":
            count += 1
    if count >= config.constraint_tag:
        return False

    return True

def load_weight_matrix():
    load_weight_matrix = {}
    label2idx = {}
    idx2label = {}
    if config.model == "AIC":
        model = 0
        with open(config.regression_path) as f:
            for line in f.readlines():
                if line[0] == "#":
                    for l in line[1:].split():
                        label2idx[l] = len(label2idx)
                        idx2label[len(label2idx) - 1] = l
                elif line[0] == "$":
                    model = 1
                    weight = line[1:].strip()
                else:
                    for l_idx, l in enumerate(line.split()):
                        load_weight_matrix[weight + "_model_" + str(model) +"_"+ idx2label[l_idx]] = sigmoid(float(l))
                    model += 1

            for label in label2idx:
                for model_idx_1 in range(1, config.model_num+1):
                    sum = .0
                    for model_idx_2 in range(1, config.model_num+1):
                        sum += load_weight_matrix["WEIGHT%s_model_%s_%s" %(model_idx_1, model_idx_2, label)]
                    for model_idx_2 in range(1, config.model_num + 1):
                        load_weight_matrix["WEIGHT%s_model_%s_%s" % (model_idx_1, model_idx_2, label)] = \
                            load_weight_matrix["WEIGHT%s_model_%s_%s" % (model_idx_1, model_idx_2, label)]/sum

    elif config.model == "PIC":
        with open(config.labelPIC_path) as f:
            for line in f.readlines():
                label2idx[line.strip()] = len(label2idx)
    idx2label = {v: k for k, v in label2idx.items()}

    return load_weight_matrix, label2idx, idx2label

def sigmoid(value):
    return 1 / (1 + math.exp(-value))
