import bootstrap_linearSVM as bsSVM
import data_preprocessing as pre

import numpy as np
import os

def predict_label(train_x, train_y, unlabeled_data):
    """
    채팅 데이터에 대해 machine labeled  라벨을 다는 메소드

    Arguments:
    train_x - bootstrapping을 통해 부풀린 데이터의 문장
    train_y - bootstrapping을 통해 부풀린 데이터의 라벨
    unlabeled_data - 태깅이 되어있지 않은 채팅 데이터

    Return:
    None
    """

    baseModel = bsSVM.SVMModel(train_x, train_y)
    word_dict, model = baseModel.word_dictionary(), baseModel.model()

    test_array = np.zeros((len(unlabeled_data), len(word_dict)))
    for i, v in enumerate(unlabeled_data):
        for word in (v).split('|'):
            if word in word_dict:
                test_array[i][word_dict[word]] += 1

    machine_label = model.predict(test_array)
    
    with open('./result/label.txt', 'a') as f:
        for label in machine_label:
            f.write(label+'\n')


if __name__ == '__main__':
    train_x = []
    train_y = []
    with open('./bootstrapped_data/data.txt', 'r') as f:
        for sentence in f.readlines():
            train_x.append(sentence.strip())
    with open('./bootstrapped_data/label.txt', 'r') as f:
        for label in f.readlines():
            train_y.append(label.strip())

    whole_unlabeled_data = pre.load_unlabeled_data('../data/unlabeled_data/donga_pos_unlabeled_data.txt', dup=True, shuffle=False)
    if os.path.isfile('./result/DailyLife_MachineLabeled_SG_SVM.txt'):
        os.remove('./result/DailyLife_MachineLabeled_SG_SVM.txt')

    for i in range(len(whole_unlabeled_data) // 50000 + 1):
        predict_label(train_x, train_y, whole_unlabeled_data[(i)*50000: (i+1)*50000])
