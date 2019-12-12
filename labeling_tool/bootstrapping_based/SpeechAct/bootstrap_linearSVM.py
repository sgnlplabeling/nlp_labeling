import numpy as np
import data_preprocessing as pre


from sklearn.svm import LinearSVC
from sklearn.svm.libsvm import *
from sklearn.model_selection import train_test_split


class Bootstrap():
    """
    Bootstrapping을 위한 여러가지 정보를 담고 있는 Class

    Arguments:
    unlabeled_data - list 형태의 채팅 데이터

    Return:
    None
    """

    def __init__(self, unlabeled_data=None):
        #form of sentence, not changed into bag of words yet.

        self.Test_X = None              #dataset for calculating model accuracy
        self.Test_Y = None              #after one iteration

        self.baseTrain_X = None
        self.baseTrain_Y = None

        self.target_dict = None
        self.inv_target_dict = None

        self.morph_list = None
        self.target_list = None
        self.prev_list = None

        #It is sliced into N dataset.
        self.once_filtered_X = None             #ex: 1000 samples
        self.once_filtered_Y = None             #form of list of list

        self.twice_filtered_X = None            #ex: 300samples of something
        self.twice_filtered_Y = None

        self.best_score_X = None
        self.best_score_Y = None

        self.first_filter_threshold = 1
        self.second_filter_threshold = 1
        self.number_of_bagging_model = 5
        self.best_score = 0

        self.unlabeled_data = None


    def first_filter(self, baseModel, unlabeled_data):
        """
        채팅 데이터 중 첫번째 threshold를 넘은 데이터를 리턴하는 메소드.

        Arguments:
        baseModel - 현재 golden set으로 만든 SVM 모델
        unlabeled_data - list 형태의 채팅 데이터

        Return:
        filtered_X_list - 첫번째 threshold를 넘은 채팅 데이터 문장
        filtered_Y_list - 첫번째 threshold를 넘은 채팅 데이터의 machine labeled 라벨
        score - 현재 데이터의 accuracy
        """
        word_dict, model = baseModel.word_dictionary(), baseModel.model()


        """ Testing Accuracy Here"""
        test_array = np.zeros((len(self.Test_X), len(word_dict)))
        for i ,v in enumerate(self.Test_X):
            for word in (v).split('|'):
                if word in word_dict:
                    test_array[i][word_dict[word]] += 1
        score = model.score(test_array, self.Test_Y)
        print("Accuracy with", len(self.baseTrain_X)," examples: ",score,'\n')

        array_form = np.zeros((len(unlabeled_data), len(word_dict)))
        for i, v in enumerate(unlabeled_data):
            for word in v.strip().split('|'):
                if word in word_dict:
                    array_form[i][word_dict[word]] += 1

        filtered_x_list = []
        filtered_y_list = []
        prev_x_list = []

        predicted_probs = model.decision_function(array_form)
        predicted_targets = model.predict(array_form)

        for i, v in enumerate(predicted_probs):
            max_prob = -999999
            idxtmp=-1
            for j, prob in enumerate(v):
                if prob >= max_prob:
                    idxtmp = j
                    max_prob = prob
            if idxtmp != -1 and v[idxtmp] >= self.first_filter_threshold:
                filtered_x_list.append(unlabeled_data[i].strip('|'))
                filtered_y_list.append(predicted_targets[i])
                if i%2 == 0:
                    prev_x_list.append(14)
                else:
                    prev_x_list.append(int(model.predict(array_form[i-1].reshape(1,-1))))

        return filtered_x_list, filtered_y_list, score

class SVMModel():
    """
    SVM Classfier 모델 구성을 위한 Class

    Arguments:
    Train_X - 트레이닝 데이터로 사용할 문장
    Train_Y - 트레이닝 데이터로 사용할 화행 라벨
    Test_X - 테스트 데이터로 사용할 문장
    Test_Y - 테스트 데이터로 사용할 화행 라벨
    위의 모든 arguement는 list 형태.

    Return:
    Class 타입
    """

    def __init__(self, Train_X, Train_Y, Test_X=None, Test_Y=None):
        self.Train_X = Train_X
        self.Train_Y = Train_Y
        self.Test_X = Test_X
        self.Test_Y = Test_Y

    def word_dictionary(self):
        """
        Bag of word 방식을 위한 단어 사전

        Arguments:
        self

        Return:
        단어 사전
        """

        word_dict = {}
        count=0
        for sentence in self.Train_X:
            for word in (sentence).split('|'):
                if word not in word_dict:
                    word_dict[word] = count
                    count += 1
        return word_dict

    def model(self):
        """
        SVM Classifier 모델을 만드는 메소드.

        Arguments:
        None

        Return:
        SVM Classifier 모델을 리턴
        """

        word_dict = self.word_dictionary()
        array_form = np.zeros((len(self.Train_X), len(word_dict))) #bag of words 형태의 문장 표현
        for i, v in enumerate(self.Train_X):
            for word in (v).split('|'):
                if word in word_dict:
                    array_form[i][word_dict[word]] += 1
        
        clf = LinearSVC(random_state=0, max_iter=10000)
        clf.fit(array_form, self.Train_Y)

        return clf


