# -*- coding: utf-8 -*-

'''
Created on 2017-02-08

@author: pymnlp
@description :
'''

import FeatureModel as f_model
import numpy as np
from config import FLAGS

def convert_to_input_vector(sample_batch, model):
    y_batch = []
    y_tag_batch = []
    x_left_mor_cnn_batch = []
    x_left_pos_cnn_batch = []
    x_right_mor_cnn_batch = []
    x_right_pos_cnn_batch = []
    x_position_batch = []
    x_hc_batch = []

    for sample in sample_batch:
        # word embedding에 들어갈 것은 index 그대로 넣기
        x_left_mor_cnn_batch.append(sample.left_mor_cnn)
        x_left_pos_cnn_batch.append(sample.left_pos_cnn)
        x_right_mor_cnn_batch.append(sample.right_mor_cnn)
        x_right_pos_cnn_batch.append(sample.right_pos_cnn)
        x_position_batch.append(model.position_mark)

        # 그외 자질은 zero-one representation
        hc = [0] * model.hc_feature_size
        for idx_hc in sample.hand_crafted:
            hc[idx_hc] = 1
        x_hc_batch.append(hc)

        y = [0] * model.num_actions
        y[sample.y] = 1
        y_batch.append(y)

        y_tag = [0] * model.type_size
        if sample.y_tag is not -1:
            y_tag[sample.y_tag] = 1
        y_tag_batch.append(y_tag)

    # 기본 자질
    x_mor_batch = []
    x_pos_batch = []
    for sample in sample_batch:
        # word embedding에 들어갈 것은 index 그대로 넣기
        x_mor_batch.append(sample.left_mor_cnn + sample.right_mor_cnn)
        x_pos_batch.append(sample.left_pos_cnn + sample.right_pos_cnn)

        y = [0] * model.type_size
        y[sample.y] = 1

    return np.array(x_mor_batch), np.array(x_pos_batch), \
           np.array(x_left_pos_cnn_batch), np.array(x_left_pos_cnn_batch), \
           np.array(x_right_mor_cnn_batch), np.array(x_right_pos_cnn_batch), \
           np.array(x_position_batch), np.array(x_hc_batch), np.array(y_batch), np.array(y_tag_batch)

def convert_to_input_vector(sample_batch, model):
    y_batch = []
    x_left_mor_cnn_batch = []
    x_left_pos_cnn_batch = []
    x_right_mor_cnn_batch = []
    x_right_pos_cnn_batch = []
    x_position_batch = []
    x_child_mor_batch = []
    x_child_pos_batch = []
    x_hc_batch = []

    for sample in sample_batch:
        # word embedding에 들어갈 것은 index 그대로 넣기
        x_left_mor_cnn_batch.append(sample.left_mor_cnn)
        x_right_mor_cnn_batch.append(sample.right_mor_cnn)
        x_right_pos_cnn_batch.append(sample.right_pos_cnn)
        x_child_mor_batch.append(sample.child_mor)
        x_child_pos_batch.append(sample.child_pos)
        x_position_batch.append(model.position_mark)

        # 그외 자질은 zero-one representation

        hc = [0] * model.hc_feature_size

        for idx_hc in sample.hand_crafted:
            hc[idx_hc] = 1

        x_hc_batch.append(hc)

        y = [0] * model.type_size
        y[sample.y] = 1
        y_batch.append(y)


    # 기본 자질
    x_mor_batch = []
    x_pos_batch = []
    for sample in sample_batch:
        # word embedding에 들어갈 것은 index 그대로 넣기
        x_mor_batch.append(sample.left_mor_cnn + sample.right_mor_cnn)
        x_pos_batch.append(sample.left_pos_cnn + sample.right_pos_cnn)

        y = [0] * model.type_size
        y[sample.y] = 1

    return np.array(x_mor_batch), np.array(x_pos_batch), \
           np.array(x_left_pos_cnn_batch), np.array(x_left_pos_cnn_batch), \
           np.array(x_right_mor_cnn_batch), np.array(x_right_pos_cnn_batch), \
           np.array(x_position_batch), np.array(x_child_mor_batch), np.array(x_child_pos_batch), \
           np.array(x_hc_batch), np.array(y_batch)

def make_sample_from_line(line, model):
    sample = f_model.InputFeature()
    input_list = line.split()

    sample.y = int(input_list[0])

    sample.left_mor_cnn = [0] * model.max_length
    for i in range(1, model.max_length + 1):
        sample.left_mor_cnn[i - 1] = int(input_list[i])

    sample.left_pos_cnn = [0] * model.max_length
    for i in range(model.max_length + 1, model.max_length * 2 + 1):
        sample.left_pos_cnn[i - (model.max_length + 1)] = int(input_list[i])

    sample.right_mor_cnn = [0] * model.max_length
    for i in range(model.max_length * 2 + 1, model.max_length * 3 + 1):
        sample.right_mor_cnn[i - (model.max_length * 2 + 1)] = int(input_list[i])

    sample.right_pos_cnn = [0] * model.max_length
    for i in range(model.max_length * 3 + 1, model.max_length * 4 + 1):
        sample.right_pos_cnn[i - (model.max_length * 3 + 1)] = int(input_list[i])

    sample.child_mor = [0] * model.max_length
    for i in range(model.max_length * 4 + 1, model.max_length * 5 + 1):
        sample.child_mor[i - (model.max_length * 4 + 1)] = int(input_list[i])

    sample.child_pos = [0] * model.max_length
    for i in range(model.max_length * 5 + 1, model.max_length * 6 + 1):
        sample.child_pos[i - (model.max_length * 5 + 1)] = int(input_list[i])

    sample.hand_crafted = []
    for i in range(model.max_length * 6 + 1, len(input_list)):
        sample.hand_crafted.append(int(input_list[i]))
    return sample


def make_sample_list_from_input_data(file_path, model):
    sample_list = []
    with open(file_path, 'r') as f:

        while True:
            line = f.readline()
            if not line: break
            sample = make_sample_from_line(line, model)
            sample_list.append(sample)
    return sample_list


class CorpusReader(object):
    def __init__(self):
        self.file = None
        self.str_sentence = None
        self.out_file = None

    def set_file(self, file_path, out_file_path=None):
        self.file = open(file_path, 'r')

        if out_file_path is not None:
            self.out_file = open(out_file_path, 'w')

    def close_files(self):
        if self.file is not None:
            self.file.close()
            self.file = None
        if self.out_file is not None:
            self.out_file.close()
            self.out_file = None

    def get_next(self, batch_size = FLAGS.batch_size):
        sentences = []
        for i in range(batch_size):
            sentence = Sentence()
            while True:
                line = self.file.readline()
                if not line: break
                # ; 로 시작하면 문장
                if line[0] == ';':
                    sentence.raw_sentence = line
                # 문장 하나 완성
                elif len(line) < 3:
                    sentences.append(sentence)
                    break
                else:
                    if FLAGS.pos == 'donga':
                        sentence.add_dependency_donga(line)
                    else:
                        sentence.add_dependency(line)

        return sentences
        # return None

    def close_file(self):
        self.file.close()

    def write_out_data(self, total_sample):
        for sample in total_sample:
            line = str(sample.y)
            for val in sample.left_mor_cnn:
                line += ' ' + str(val)

            for val in sample.left_pos_cnn:
                line += ' ' + str(val)

            for val in sample.right_mor_cnn:
                line += ' ' + str(val)

            for val in sample.right_pos_cnn:
                line += ' ' + str(val)

            for val in sample.child_mor:
                line += ' ' + str(val)

            for val in sample.child_pos:
                line += ' ' + str(val)

            for val in sample.hand_crafted:
                line += ' ' + str(val)

            self.out_file.write(line + '\n')


class DataReader(object):
    def __init__(self):
        self.file = None
        self.model = None

    def set_file(self, file_path):
        self.file = open(file_path, 'r')

    def set_model(self, model):
        self.model = model

    def close_files(self):
        if self.file is not None:
            self.file.close()
            self.file = None

    def get_next(self):
        line = self.file.readline()
        if not line:
            return None
        arr = line.split()
        # 정답
        idx_output = int(arr[0])
        output = [0] * 2
        output[idx_output] = 1

        length = self.model.max_length

        left_mor = [0] * length
        right_mor = [0] * length
        left_pos = [0] * length
        right_pos = [0] * length

        for i in range(length):
            left_mor[i] = int(arr[i + length * 0 + 1])
        for i in range(length):
            right_mor[i] = int(arr[i + length * 1 + 1])
        for i in range(length):
            left_pos[i] = int(arr[i + length * 2 + 1])
        for i in range(length):
            right_pos[i] = int(arr[i + length * 3 + 1])

        ######################################################################
        head_mor1 = [0] * (self.model.mor_size + 1)
        head_mor2 = [0] * (self.model.mor_size + 1)
        head_mor3 = [0] * (self.model.mor_size + 1)
        head_mor4 = [0] * (self.model.mor_size + 1)
        child_mor1 = [0] * (self.model.mor_size + 1)
        child_mor2 = [0] * (self.model.mor_size + 1)
        child_mor3 = [0] * (self.model.mor_size + 1)
        child_mor4 = [0] * (self.model.mor_size + 1)

        head_pos1 = [0] * (self.model.pos_size + 1)
        head_pos2 = [0] * (self.model.pos_size + 1)
        head_pos3 = [0] * (self.model.pos_size + 1)
        head_pos4 = [0] * (self.model.pos_size + 1)
        child_pos1 = [0] * (self.model.pos_size + 1)
        child_pos2 = [0] * (self.model.pos_size + 1)
        child_pos3 = [0] * (self.model.pos_size + 1)
        child_pos4 = [0] * (self.model.pos_size + 1)

        head_mor1[int(arr[0 + 4 * 0 + length * 4 + 1])] = 1
        head_mor2[int(arr[1 + 4 * 0 + length * 4 + 1])] = 1
        head_mor3[int(arr[2 + 4 * 0 + length * 4 + 1])] = 1
        head_mor4[int(arr[3 + 4 * 0 + length * 4 + 1])] = 1
        child_mor1[int(arr[0 + 4 * 1 + length * 4 + 1])] = 1
        child_mor2[int(arr[1 + 4 * 1 + length * 4 + 1])] = 1
        child_mor3[int(arr[3 + 4 * 1 + length * 4 + 1])] = 1
        child_mor4[int(arr[4 + 4 * 1 + length * 4 + 1])] = 1
        head_pos1[int(arr[0 + 4 * 2 + length * 4 + 1])] = 1
        head_pos2[int(arr[1 + 4 * 2 + length * 4 + 1])] = 1
        head_pos3[int(arr[2 + 4 * 2 + length * 4 + 1])] = 1
        head_pos4[int(arr[3 + 4 * 2 + length * 4 + 1])] = 1
        child_pos1[int(arr[0 + 4 * 3 + length * 4 + 1])] = 1
        child_pos2[int(arr[1 + 4 * 3 + length * 4 + 1])] = 1
        child_pos3[int(arr[2 + 4 * 3 + length * 4 + 1])] = 1
        child_pos4[int(arr[3 + 4 * 3 + length * 4 + 1])] = 1

        head_mor = head_mor1 + head_mor2 + head_mor3 + head_mor4
        child_mor = child_mor1 + child_mor2 + child_mor3 + child_mor4

        head_pos = head_pos1 + head_pos2 + head_pos3 + head_pos4
        child_pos = child_pos1 + child_pos2 + child_pos3 + child_pos4

        ########################################


        # head_mor = [0] * 4
        # head_pos = [0] * 4
        # child_mor = [0] * 4
        # child_pos = [0] * 4

        # for i in range(4) :
        #     head_mor[i] = int(arr[i + 4*0+length*4+1])
        # for i in range(4) :
        #     child_mor[i] = int(arr[i + 4*1+length*4+1])
        # for i in range(4) :
        #     head_pos[i] = int(arr[i + 4*2+length*4+1])
        # for i in range(4) :
        #     child_pos[i] = int(arr[i + 4*3+length*4+1])



        hc = [0] * (self.model.hc_feature_size + 1)
        hc_list = arr[4 * 4 + length * 4 + 1:]
        for hc_feature in hc_list:
            hc[int(hc_feature)] = 1

        return output, left_mor, right_mor, left_pos, right_pos, head_mor, child_mor, head_pos, child_pos, hc


class Sentence:
    def __init__(self):
        self.raw_sentence = None
        self.correct_dep_list = []
        self.predict_dep_list = []
        self.eojeol_list = []

    def get_size(self):
        return len(self.eojeol_list)

    def add_dependency_donga(self, line):
        str_list = line.split()
        dep = Dependency()
        dep.index = int(str_list[0]) - 1
        dep.head = int(str_list[1]) - 1
        dep.type = str_list[2]
        self.correct_dep_list.append(dep)
        eoj = Eojeol()

        mor_list = str_list[3].split('+')

        for mor in mor_list:
            idx = mor.rfind('/')
            new_mor = Morpheme()
            new_mor.pos = mor[idx + 1:]
            new_mor.lex = mor[:idx]
            eoj.morpheme_list.append(new_mor)
        self.eojeol_list.append(eoj)
        return


    def add_dependency(self, line):
        str_list = line.split()
        dep = Dependency()
        dep.index = int(str_list[0]) - 1
        dep.head = int(str_list[1]) - 1
        dep.type = str_list[2]
        self.correct_dep_list.append(dep)
        eoj = Eojeol()
        mor_list = str_list[4].split('|')
        for mor in mor_list:
            idx = mor.rfind('/')
            new_mor = Morpheme()
            new_mor.pos = mor[idx + 1:]
            new_mor.lex = mor[:idx]
            eoj.morpheme_list.append(new_mor)
        self.eojeol_list.append(eoj)
        return


class Dependency(object):
    def __init__(self):
        self.index = -1
        self.head = -1
        self.type = ''


class Eojeol:
    def __init__(self):
        self.morpheme_list = []
        self.raw_eojeol = None


class Morpheme:
    def __init__(self):
        self.lex = ''
        self.pos = ''


def get_feature_model(train_filename):
    cr = CorpusReader()
    model = f_model.FeatureModel()

    # 코퍼스 파일 읽기
    cr.set_file(train_filename)

    while True:
        data = cr.get_next()
        if data is None:
            break
        model.add_feature(data)

    cr.close_file()
    return model
