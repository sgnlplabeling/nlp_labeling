from sklearn.model_selection import train_test_split
import json
import random


def making_all_dict(dict_set):
    """
    list 안의 데이터를 dictionary 형태로 바꾸는 메소드

    Arguments:
    dict_set - dictionary를 만들 리스트

    Return:
    만들어진 dictionary
    """

    dic={}
    idx=0

    for i in dict_set:
        dic[i] = idx
        idx+=1

    return dic

def making_target_list(lis, dic):
    """
    dictionary를 이용해 list안의 element를 해당하는 dictionary 값으로 변환.

    Arguments:
    lis - list 데이터
    dic - dictionary 데이터

    Return:
    변환된 후의 list 데이터
    """


    target_list = []
    for target in lis:
        target_list.append(dic[target])
    return target_list

def load_unlabeled_data(file_path, dup, shuffle=False):
    """
    채팅 데이터를 리스트 형태로 바꾸는 메소드.

    Arguments:
    file_path - 파일 경로
    dup - question, answer 쌍 데이터에 대해 중복될 문장을 허용할지 여부
    shuffle - 데이터를 섞을 지 여부

    Return:
    리스트 형태로 변환된 채팅 데이터.
    """


    with open(file_path, 'r') as f:
        whole_data = f.readlines()

    data_dict = {}
    whole_tuple = []
    whole_list = []

    if dup is True:
        for tmp1, tmp2 in zip(whole_data[0::2], whole_data[1::2]):
            tmp1 = tmp1.replace("DQAI", "####")
            tmp2 = tmp2.replace("DQAI", "####")

            tuple_tmp = (tmp1, tmp2)
            whole_tuple.append(tuple_tmp)

        if shuffle is True:
            random.shuffle(whole_tuple)

        for t in whole_tuple:
            whole_list.append(t[0])
            whole_list.append(t[1])

    elif dup is False:
        for line in whole_data:
            if line not in data_dict:
                data_dict[line] = 1
                whole_list.append(line)

        if shuffle is True:
            random.shuffle(whole_list)

    return whole_list

def data_into_list(file_path):
    """
    파일명을 입력받아 list 형태로 리턴하는 메소드

    Arguments:
    file_path - 파일명

    Return:
    list형태의 데이터
    """

    f = open(file_path, 'r')
    f.readline() 
    data = [s.strip() for s in f.read().split('\n\n')]
    f.close() 
    return data


class Labeled_data():
    """
    Labeled data의 정보를 저장하기 위한 Class 변수

    Arguments:
    None

    Return:
    None
    """

    def __init__(self):
        self.speaker = None
        self.utterance = None
        self.prev_act = None
        self.cur_act = None
        self.i = None
        self.j = None

#paragraph 단위로 저장되어 있는 1d list를 sentence 기준의 2dlist로 변환
def organize_data(data):
    """
    Paragraph 단위로 저장되어 있는 Labeled data dialogue를
    sentence 기준으로 변환하고 관련 정보를 저장.

    Arguments:
    Data - dialogue 단위로 저장되어 있는 labeled data

    Return:
    'Labeled_data'타입을 element로 가지는 list
    """

    organized_data = []
    for i, paragraph in enumerate(data):
        line_skipped = False
        sentence_list = []
        sentence_idx = 0

        for j, line in enumerate(paragraph.split('\n')):
            line = line.strip()
            if line is "":
                line_skipped = True
                continue
            tmp = Labeled_data()
            tmp.speaker = line.split('\t')[0]
            tmp.utterance = line.split('\t')[1]
            tmp.cur_act = line.split('\t')[-1]
            tmp.i = i
            tmp.j = j
            if j == 0:
                tmp.prev_act = 'None'
            else:
                tmp.prev_act = sentence_list[sentence_idx-1].cur_act
            sentence_list.append(tmp)
            sentence_idx += 1
        organized_data.append(sentence_list)
    return organized_data


def initializing(boot, reduced_label=False):
    """
    SVM Classifier에 필요한 변수 초기화 및
    Preprocessing 을 진행하는 메소드.

    Arguments:
    boot - Class
    reduced_label - 총 14가지 화행 그대로 사용할지, 크게 묶어서 4가지로 사용할 지
                    정하는 변수

    Return:
    None
    """

    target_change_dict = {}

    target_change_dict["wh-question"] = "request"
    target_change_dict["request"] = "request"
    target_change_dict["yn-question"] = "request"
    target_change_dict["offer"] = "request"

    target_change_dict["ack"] = "response"
    target_change_dict["negate"] = "response"
    target_change_dict["response"] = "response"
    target_change_dict["affirm"] = "response"

    target_change_dict["expressive"] = "emotion"
    target_change_dict["closing"] = "emotion"
    target_change_dict["promise"] = "emotion"

    target_change_dict["opening"] = "common use"
    target_change_dict["inform"] = "common use"
    target_change_dict["introduce"] = "common use"

    target_change_dict["None"] = "None"

    labeled_data = data_into_list('../data/labeled_data/donga_pos_hotel_corpus.txt')
    labeled_data.extend(data_into_list('../data/labeled_data/donga_pos_schedule_corpus.txt'))

    morph_list = []
    target_list = []
    prev_list = []
    organized_data = organize_data(labeled_data)

    if reduced_label is True:
        for paragraph in organized_data:
            for sentence in paragraph:
                morph_list.append(sentence.utterance)
                target_list.append(target_change_dict[sentence.cur_act])
                prev_list.append(target_change_dict[sentence.prev_act])
    else:
        for paragraph in organized_data:
            for sentence in paragraph:
                morph_list.append(sentence.utterance)
                target_list.append(sentence.cur_act)

    all_target_dict = making_all_dict(list(set(target_list)))
    boot.inv_target_dict = {v: k for k, v in all_target_dict.items()}
    all_target_1dlist = making_target_list(target_list, all_target_dict)
    target_list = all_target_1dlist
    boot.target_dict = making_all_dict(list(set(target_list)))
    boot.in_target_dict = all_target_dict

    boot.morph_list = morph_list
    boot.target_list = target_list

    boot.baseTrain_X, boot.Test_X, boot.baseTrain_Y, boot.Test_Y = train_test_split(morph_list, target_list,
                                                                                    test_size=0.1, random_state=42)




