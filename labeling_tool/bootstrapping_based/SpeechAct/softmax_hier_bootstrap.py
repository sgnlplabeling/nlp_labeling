import bootstrap_linearSVM as bsSVM
import data_preprocessing as pre
import predict

import os
import sys
import numpy as np

def softmax(x):
    """
    softmax 함수

    Arguments:
    x - real number

    Return:
    softmax(x)
    """

    ex = np.exp(x - np.expand_dims(np.max(x, axis=1), 1))
    return ex / np.expand_dims(ex.sum(axis=1), 1)

def train_with_hierarchy(boot, unlabeled_data):
    """
    Batch size만큼의 채팅 데이터를 가지고 Bootstrapping 한 iteration을 진행.

    Arguments:
    boot - 부트스트랩핑을 위한 Class
    unlabeled_data - list 형태의 채팅 데이터

    Return:
    None
    """

    print("Current number of data: ", len(boot.baseTrain_X), '\n')
    Train_X, Train_Y = boot.baseTrain_X, boot.baseTrain_Y
    baseModel = bsSVM.SVMModel(Train_X, Train_Y)
    boot.once_filtered_X, boot.once_filtered_Y, score = boot.first_filter(baseModel, unlabeled_data)
    new_X, new_Y = organize_filtered_data(boot, boot.once_filtered_X, boot.once_filtered_Y)
    boot.twice_filtered_X, boot.twice_filtered_Y = normed_hier_svm(boot, new_X, new_Y, unlabeled_data)

    if score > boot.best_score:
        boot.best_score = score
        boot.best_score_X = boot.baseTrain_X.copy()
        boot.best_score_Y = boot.baseTrain_Y.copy()

    if boot.twice_filtered_X is not None:
        print("Additional ",len(boot.twice_filtered_X), " data bootstrapped\n")
        boot.baseTrain_X += boot.twice_filtered_X
        boot.baseTrain_Y += boot.twice_filtered_Y


def normed_hier_svm(boot, new_X, new_Y, unlabeled_data):
    """
    labeled data + threshold  score 이상의 채팅 데이터들로 계층적 bootstrapping을 진행하는 메소드
    
    Arguments:
    new_X - list 형태의 문장
    new_Y - list 형태의 라벨
    unlabeled_data - 채팅 데이터

    Return:
    result_X - 채팅데이터 중 최종적으로 golden set에 추가할 list 형태의 문장
    result_Y - 채팅데이터 중 최종적으로 golden set에 추가할 list 형태의 machine labeled 라벨
    """

    tmpTrain_Y = []                     #줄인 화행 총 4가지
    for target in boot.baseTrain_Y:
        if target == boot.in_target_dict['wh-question'] or target == boot.in_target_dict['request'] or \
                target == boot.in_target_dict['yn-question'] or target == boot.in_target_dict['offer']:
            tmpTrain_Y.append(0)
        elif target == boot.in_target_dict['ack'] or target == boot.in_target_dict['negate'] or \
                target == boot.in_target_dict['reject'] or target == boot.in_target_dict['affirm']:
            tmpTrain_Y.append(1)
        elif target == boot.in_target_dict['expressive'] or target == boot.in_target_dict['closing'] or \
                target == boot.in_target_dict['promise']:
            tmpTrain_Y.append(2)
        elif target ==  boot.in_target_dict['opening']or target == boot.in_target_dict['inform'] or \
                target == boot.in_target_dict['introduce']:
            tmpTrain_Y.append(3)

    hierBaseModel = bsSVM.SVMModel(boot.baseTrain_X, tmpTrain_Y)
    word_dict, model = hierBaseModel.word_dictionary(), hierBaseModel.model()

    reduced_array = np.zeros((len(unlabeled_data), len(word_dict)))
    for i, v in enumerate(unlabeled_data):
        for word in v.strip().split('|'):
            if word in word_dict:
                reduced_array[i][word_dict[word]] += 1

    predicted_reduced_prob = (model.decision_function(reduced_array))
    predicted_reduced_softmax_prob = softmax(predicted_reduced_prob) #normalize된 array

    bagging_X, bagging_Y = organize_hier_data(boot, boot.baseTrain_X, boot.baseTrain_Y, new_X, new_Y)
    result_X, result_Y = get_softmax_hier_result(boot, bagging_X, bagging_Y, predicted_reduced_softmax_prob, unlabeled_data, op='plus')
    return result_X, result_Y

def get_softmax_hier_result(boot, bagging_X, bagging_Y, predicted_reduced_softmax_prob, unlabeled_data, op):
    """
    계층적 bootstrapping을 진행할 때 각 문장들의 최종 score를 계산하고, threshold 이상의 문장만 반환.

    Arguments:
    bagging_X - 첫번째 threshold를 통과한 문장의 list
    bagging_Y - 첫번째 threshold를 통과한 문장의 machine labeled 라벨
    predicted_reduced_softmax_prob - 채팅데이터 각각의 score
    unlabeled_data - 채팅 데이터
    op - 최종 score 계산 방법으로 사용할 operator. plus와 mul 둘 중에 하나 선택

    Return:
    filtered_X_list - 최종 score가 threshold를 넘은 채팅 데이터의 list 형태의 문장
    filtered_Y_list - 최종 score가 threshold를 넘은 채팅 데이터의 list 형태의 machine labeled 라벨
    """
    word_dict = [None]*4
    model = [None]*4
    hierModel = [None]*4
    predicted_probs = [None]*4
    predicted_targets = [None]*4

    for i in range(4):
        hierModel[i] = bsSVM.SVMModel(bagging_X[i], bagging_Y[i])
        word_dict[i], model[i] = hierModel[i].word_dictionary(), hierModel[i].model()

    filtered_X_list = []
    filtered_Y_list = []

    for i, v in enumerate(unlabeled_data):
        idxtmp = -1
        max_prob = -1.0
        for k in range(4):
            tmp_word_dict = word_dict[k]
            array_form = np.zeros(len(tmp_word_dict))
            for word in v.strip().split('|'):
                if word in tmp_word_dict:
                    array_form[tmp_word_dict[word]] += 1
            predicted_targets[k] = model[k].predict(array_form.reshape(1, -1))
            predicted_probs[k] = softmax(model[k].decision_function(array_form.reshape(1,-1)))

            for j, prob in enumerate(predicted_probs[k][0]):
                if op == 'plus':
                    tmp_prob = prob+predicted_reduced_softmax_prob[i][k]
                elif op == 'mul':
                    tmp_prob = prob * predicted_reduced_softmax_prob[i][k]
                else:
                    print("Wrong Input!")
                    sys.exit(-1)
                if tmp_prob > max_prob:
                    max_prob = tmp_prob
                    idxtmp = k
        if max_prob > boot.second_filter_threshold and max_prob < 2:
            filtered_X_list.append(v.strip())
            filtered_Y_list.append(predicted_targets[idxtmp])


    return filtered_X_list, filtered_Y_list

def organize_hier_data(boot, X, Y, newX, newY):
    """
    분류된 bootstrapping 데이터에 golden set을 추가하는 메소드.

    Arguments:
    X - 기존 golden set의 문장
    Y - 기존 godlen set의 라벨
    newX - 이미 분류가 완료된 threshold를 넘은 채팅 데이터의 문장
    newY - 이미 분류가 안료된 threshold를 넘은 채팅 데이터의 machine labeled 라벨

    Return:
    new_X - golden set 문장 + 채팅 데이터의 문장
    new_Y - golden set 라벨 + 채팅 데이터의 machine labeled 라벨
    """

    new_X = newX.copy()
    new_Y = newY.copy()
    for morph, target in zip(X, Y):
        if target == boot.in_target_dict['wh-question'] or target == boot.in_target_dict['request'] or \
                target == boot.in_target_dict['yn-question'] or target == boot.in_target_dict['offer']:
            new_X[0].append(morph)
            new_Y[0].append(target)
        elif target == boot.in_target_dict['ack'] or target == boot.in_target_dict['negate'] or \
                target == boot.in_target_dict['reject'] or target == boot.in_target_dict['affirm']:
            new_X[1].append(morph)
            new_Y[1].append(target)
        elif target == boot.in_target_dict['expressive'] or target == boot.in_target_dict['closing'] or \
                target == boot.in_target_dict['promise']:
            new_X[2].append(morph)
            new_Y[2].append(target)
        elif target ==  boot.in_target_dict['opening']or target == boot.in_target_dict['inform'] or \
                target == boot.in_target_dict['introduce']:
            new_X[3].append(morph)
            new_Y[3].append(target)

    return new_X, new_Y


def organize_filtered_data(boot, X, Y):
    """
    추가된 bootstrapping 데이터를 크게 4가지 라벨에 맞게 변경하는 메소드.

    Arguments:
    X - threhosld를 넘은 채팅 데이터의 문장
    Y - threshold를 넘은 채팅 데이터의 machine labeled 라벨

    Return:
    new_X - golden set 문장 + 채팅 데이터의 문장
    new_Y - golden set 라벨 + 채팅 데이터의 machine labeled 라벨
    """

    new_X = [None]*4
    new_Y = [None]*4
    for i in range(4):
        new_X[i] = []
        new_Y[i] = []

    for morph, target in zip(X, Y):
        if target == boot.in_target_dict['wh-question'] or target == boot.in_target_dict['request'] or \
                target == boot.in_target_dict['yn-question'] or target == boot.in_target_dict['offer']:
            new_X[0].append(morph)
            new_Y[0].append(target)
        elif target == boot.in_target_dict['ack'] or target == boot.in_target_dict['negate'] or \
                target == boot.in_target_dict['reject'] or target == boot.in_target_dict['affirm']:
            new_X[1].append(morph)
            new_Y[1].append(target)
        elif target == boot.in_target_dict['expressive'] or target == boot.in_target_dict['closing'] or \
                target == boot.in_target_dict['promise']:
            new_X[2].append(morph)
            new_Y[2].append(target)
        elif target ==  boot.in_target_dict['opening']or target == boot.in_target_dict['inform'] or \
                target == boot.in_target_dict['introduce']:
            new_X[3].append(morph)
            new_Y[3].append(target)

    return new_X, new_Y


if __name__ == '__main__':
    whole_unlabeled_data = pre.load_unlabeled_data('../data/unlabeled_data/donga_pos_unlabeled_data.txt', dup=False, shuffle=False)

    batch_size = 5000

    boot = bsSVM.Bootstrap()
    pre.initializing(boot, reduced_label = False)

    boot.first_filter_threshold = 1
    boot.second_filter_threshold = 1.7

    for i in range(len(whole_unlabeled_data) // batch_size + 1):
        unlabeled_data = whole_unlabeled_data[int(i)*batch_size: (i+1)*batch_size]
        train_with_hierarchy(boot, unlabeled_data)

    train_label = []
    with open('./bootstrapped_data/data.txt', 'w') as f:
        for sentence in boot.best_score_X:
            f.write(sentence+'\n')
    with open('./bootstrapped_data/label.txt', 'w') as f:
        for label in boot.best_score_Y:
            f.write(boot.inv_target_dict[int(label)]+'\n')
            train_label.append(boot.inv_target_dict[int(label)])

    del whole_unlabeled_data

    unlabeled_data_for_labeling = pre.load_unlabeled_data('../data/unlabeled_data/donga_pos_unlabeled_data.txt', dup=True, shuffle=False)
    if os.path.isfile('./results/DailyLife_MachineLabeled_SG_SVM.txt'):
        os.remove('./results/DailyLife_MachineLabeled_SG_SVM.txt')

    for i in range(len(unlabeled_data_for_labeling) // 50000 + 1):
        predict.predict_label(boot.best_score_X, train_label, unlabeled_data_for_labeling[i*50000: (i+1)*50000])

