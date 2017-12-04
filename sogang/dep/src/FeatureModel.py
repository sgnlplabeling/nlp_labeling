# -*- coding: utf-8 -*-

'''
Created on 2017-05-07

@author: pymnlp
@description :
'''

import DataTools as dt
import numpy as np

class FeatureModel:
    def __init__(self):
        self.type_map = {}
        self.type_size = 0
        self.num_actions = 2
        self.rev_type_map = {}
        self.mor_map = {}
        self.mor_size = 0
        self.pos_map = {}
        self.pos_size = 0
        self.window_size = 3
        self.max_length = self.window_size * 4
        self.feature_size = 0

        # empty를 위한 더미 넣기
        self.empty_dummy = dt.Morpheme()
        self.empty_dummy.lex = '$empty'
        self.empty_dummy.pos = '$empty'
        str_mor = self.empty_dummy.lex + '/' + self.empty_dummy.pos
        self.mor_map[str_mor] = self.mor_size + 1
        self.mor_size += 1
        self.pos_map[self.empty_dummy.pos] = self.pos_size + 1
        self.pos_size += 1

        # position_mark [sequence_length, sequence_length]
        self.position_mark = []

        for i in range(self.max_length):
            _position_mark = [float(0)] * self.max_length
            _position_mark[i] = float(1)
            self.position_mark.append(_position_mark)

        # root를 위한 더미 넣기
        self.root_dummy = dt.Morpheme()
        self.root_dummy.lex = '$root'
        self.root_dummy.pos = '$root'
        str_mor = self.root_dummy.lex + '/' + self.root_dummy.pos
        self.mor_map[str_mor] = self.mor_size + 1
        self.mor_size += 1
        self.pos_map[self.root_dummy.pos] = self.pos_size + 1
        self.pos_size += 1

        # hand crafted feature
        self.hc_feature_map = {}
        self.hc_feature_size = 0

    def get_feature_size(self):
        size = 0
        # morph 입력
        size += self.mor_size * 2
        # pos 입력
        size += self.pos_size * 2
        # hc
        size += self.hc_feature_size

        return size

    def add_feature(self, sentence):
        for i in range(len(sentence.eojeol_list)):
            dep_type = sentence.correct_dep_list[i]
            if not dep_type in self.type_map:
                # tag 추가
                self.type_map[dep_type] = self.type_size
                self.rev_type_map[self.type_size] = [dep_type]
                self.type_size += 1

            eoj = sentence.eojeol_list[i]
            for mor in eoj.morpheme_list:
                str_mor = mor.lex + '/' + mor.pos

                if not str_mor in self.mor_map:
                    # feature 추가
                    self.mor_map[str_mor] = self.mor_size + 1
                    self.mor_size += 1

                str_pos = mor.pos

                if not str_pos in self.pos_map:
                    # feature 추가
                    self.pos_map[str_pos] = self.pos_size + 1
                    self.pos_size += 1

    def get_mor_feature_idx(self, mor, mode):
        if mor in self.mor_map:
            return self.mor_map.get(mor)
        elif mode == 'train':
            self.mor_map[mor] = self.mor_size + 1
            self.mor_size += 1
            return self.mor_map.get(mor)
        else:
            return 0

    def get_pos_feature_idx(self, pos, mode):
        if pos in self.pos_map:
            return self.pos_map.get(pos)
        elif mode == 'train':
            self.pos_map[pos] = self.pos_size + 1
            self.pos_size += 1
            return self.pos_map.get(pos)
        else:
            return 0

    def get_type_idx(self, type):
        if type in self.type_map:
            return self.type_map.get(type)
        else:
            self.type_map[type] = self.type_size
            self.rev_type_map[self.type_size] = type
            self.type_size += 1
            return self.type_map.get(type)

    def get_str_type(self, idx , mode = 'test'):
        if mode == 'test':
            rev_tpyes=[]
            for i in idx:
                rev_tpyes.append(self.rev_type_map.get(i))

            return rev_tpyes
        elif mode =='train':
            return self.rev_type_map.get(idx)

    def get_hc_feature_idx(self, hc, mode):
        if hc in self.hc_feature_map:
            return self.hc_feature_map.get(hc)
        elif mode == 'train':
            self.hc_feature_map[hc] = self.hc_feature_size
            self.hc_feature_size += 1
            return self.hc_feature_map.get(hc)
        else:
            return 0

    def make_feature_vector(self, state, data, mode='test'):
        # sentences = np.array([])

        if mode == 'test':
            sentences = []
            hcs = []
            for batch_i, sentence in enumerate(data):
                # CNN 입력 만들기
                left_mor_cnn_input = [0] * self.max_length
                left_pos_cnn_input = [0] * self.max_length
                # left_mor_cnn_input = np.zeros(self.max_length)
                # left_pos_cnn_input = np.zeros(self.max_length)
                nth_queue = 0
                idx_eoj = state.nth_queue(batch_i, nth_queue)
                if idx_eoj == None:
                    sentences.append([[-1]*24, [-1]*24, [-1]*12, [-1]*12])
                    hcs.append([-1]*7)
                    continue
                idx_input = self.max_length - 1
                while idx_input > 0 and idx_eoj != None:
                    eoj = sentence.eojeol_list[idx_eoj]
                    mor_list = eoj.morpheme_list
                    idx_mor0 = self.get_mor_feature_idx(mor_list[0].lex + '/' + mor_list[0].pos, mode)
                    idx_mor2 = self.get_mor_feature_idx(self.empty_dummy.lex + '/' + self.empty_dummy.pos, mode)
                    idx_mor1 = self.get_mor_feature_idx(self.empty_dummy.lex + '/' + self.empty_dummy.pos, mode)
                    idx_mor3 = self.get_mor_feature_idx(mor_list[-1].lex + '/' + mor_list[-1].pos, mode)

                    idx_pos0 = self.get_pos_feature_idx(mor_list[0].pos, mode)
                    idx_pos1 = self.get_pos_feature_idx(self.empty_dummy.pos, mode)
                    idx_pos2 = self.get_pos_feature_idx(self.empty_dummy.pos, mode)
                    idx_pos3 = self.get_pos_feature_idx(mor_list[-1].pos, mode)

                    if len(mor_list) >= 2:
                        idx_mor1 = self.get_mor_feature_idx(mor_list[1].lex + '/' + mor_list[1].pos, mode)
                        idx_mor2 = self.get_mor_feature_idx(mor_list[-2].lex + '/' + mor_list[-2].pos, mode)

                        idx_pos1 = self.get_pos_feature_idx(mor_list[1].pos, mode)
                        idx_pos2 = self.get_pos_feature_idx(mor_list[-2].pos, mode)
                    left_mor_cnn_input[idx_input] = idx_mor3
                    left_pos_cnn_input[idx_input] = idx_pos3
                    idx_input -= 1
                    left_mor_cnn_input[idx_input] = idx_mor2
                    left_pos_cnn_input[idx_input] = idx_pos2
                    idx_input -= 1
                    left_mor_cnn_input[idx_input] = idx_mor1
                    left_pos_cnn_input[idx_input] = idx_pos1
                    idx_input -= 1
                    left_mor_cnn_input[idx_input] = idx_mor0
                    left_pos_cnn_input[idx_input] = idx_pos0
                    idx_input -= 1
                    nth_queue += 1
                    idx_eoj = state.nth_queue(batch_i, nth_queue)
                    if idx_eoj is None:
                        break

                right_mor_cnn_input = [0] * self.max_length
                right_pos_cnn_input = [0] * self.max_length
                # right_mor_cnn_input = np.zeros(self.max_length)
                # right_pos_cnn_input = np.zeros(self.max_length)
                nth_stack = 0
                idx_eoj = state.nth_stack(batch_i, nth_stack)
                idx_input = self.max_length - 1
                while idx_input > 0 and idx_eoj != None:
                    eoj = sentence.eojeol_list[idx_eoj]
                    mor_list = eoj.morpheme_list
                    idx_mor0 = self.get_mor_feature_idx(mor_list[0].lex + '/' + mor_list[0].pos, mode)
                    idx_mor1 = self.get_mor_feature_idx(self.empty_dummy.lex + '/' + self.empty_dummy.pos, mode)
                    idx_mor2 = self.get_mor_feature_idx(self.empty_dummy.lex + '/' + self.empty_dummy.pos, mode)
                    idx_mor3 = self.get_mor_feature_idx(mor_list[-1].lex + '/' + mor_list[-1].pos, mode)

                    idx_pos0 = self.get_pos_feature_idx(mor_list[0].pos, mode)
                    idx_pos1 = self.get_pos_feature_idx(self.empty_dummy.pos, mode)
                    idx_pos2 = self.get_pos_feature_idx(self.empty_dummy.pos, mode)
                    idx_pos3 = self.get_pos_feature_idx(mor_list[-1].pos, mode)

                    if len(mor_list) >= 2:
                        idx_mor1 = self.get_mor_feature_idx(mor_list[1].lex + '/' + mor_list[1].pos, mode)
                        idx_mor2 = self.get_mor_feature_idx(mor_list[-2].lex + '/' + mor_list[-2].pos, mode)
                        idx_pos1 = self.get_pos_feature_idx(mor_list[1].pos, mode)
                        idx_pos2 = self.get_pos_feature_idx(mor_list[-2].pos, mode)
                    right_mor_cnn_input[idx_input] = idx_mor3
                    right_pos_cnn_input[idx_input] = idx_pos3
                    idx_input -= 1
                    right_mor_cnn_input[idx_input] = idx_mor2
                    right_pos_cnn_input[idx_input] = idx_pos2
                    idx_input -= 1
                    right_mor_cnn_input[idx_input] = idx_mor1
                    right_pos_cnn_input[idx_input] = idx_pos1
                    idx_input -= 1
                    right_mor_cnn_input[idx_input] = idx_mor0
                    right_pos_cnn_input[idx_input] = idx_pos0
                    idx_input -= 1
                    nth_stack += 1
                    idx_eoj = state.nth_stack(batch_i, nth_stack)
                    if idx_eoj is None:
                        break

                # topn'child feature
                child_mor = [0] * self.max_length
                child_pos = [0] * self.max_length
                # child_mor = np.zeros(self.max_length)
                # child_pos = np.zeros(self.max_length)
                idx_input = self.max_length - 1
                for i in range(self.window_size):
                    # head의 가장가까운 child
                    child = state.get_child_of_stack(batch_i, i)
                    if child is not None:
                        eoj = sentence.eojeol_list[child.index]
                        mor_list = eoj.morpheme_list
                        idx_mor0 = self.get_mor_feature_idx(mor_list[0].lex + '/' + mor_list[0].pos, mode)
                        idx_mor2 = self.get_mor_feature_idx(self.empty_dummy.lex + '/' + self.empty_dummy.pos, mode)
                        idx_mor1 = self.get_mor_feature_idx(self.empty_dummy.lex + '/' + self.empty_dummy.pos, mode)
                        idx_mor3 = self.get_mor_feature_idx(mor_list[-1].lex + '/' + mor_list[-1].pos, mode)

                        idx_pos0 = self.get_pos_feature_idx(mor_list[0].pos, mode)
                        idx_pos1 = self.get_pos_feature_idx(self.empty_dummy.pos, mode)
                        idx_pos2 = self.get_pos_feature_idx(self.empty_dummy.pos, mode)
                        idx_pos3 = self.get_pos_feature_idx(mor_list[-1].pos, mode)

                        if len(mor_list) >= 2:
                            idx_mor1 = self.get_mor_feature_idx(mor_list[1].lex + '/' + mor_list[1].pos, mode)
                            idx_mor2 = self.get_mor_feature_idx(mor_list[-2].lex + '/' + mor_list[-2].pos, mode)

                            idx_pos1 = self.get_pos_feature_idx(mor_list[1].pos, mode)
                            idx_pos2 = self.get_pos_feature_idx(mor_list[-2].pos, mode)

                        child_mor[idx_input] = idx_mor3
                        child_pos[idx_input] = idx_pos3
                        idx_input -= 1
                        child_mor[idx_input] = idx_mor2
                        child_pos[idx_input] = idx_pos2
                        idx_input -= 1
                        child_mor[idx_input] = idx_mor1
                        child_pos[idx_input] = idx_pos1
                        idx_input -= 1
                        child_mor[idx_input] = idx_mor0
                        child_pos[idx_input] = idx_pos0
                        idx_input -= 1
                    else:
                        child_mor[idx_input] = 0
                        child_pos[idx_input] = 0
                        idx_input -= 1
                        child_mor[idx_input] = 0
                        child_pos[idx_input] = 0
                        idx_input -= 1
                        child_mor[idx_input] = 0
                        child_pos[idx_input] = 0
                        idx_input -= 1
                        child_mor[idx_input] = 0
                        child_pos[idx_input] = 0
                        idx_input -= 1

                # handcrafted feature
                hc = []

                # 거리
                # self.hc_feature_map = {'dist:1': 1, 'dist:2': 2, 'dist:3~4': 3, 'dist:5~7': 4, 'dist:8~': 5}
                ts = state.top_stack(batch_i)
                tq = state.top_queue(batch_i)
                dist = ts - tq

                if ts is -1:
                    dist = 1
                if dist < 2:
                    feature_value = "d:0"
                elif dist < 3:
                    feature_value = "d:1"
                elif dist < 5:
                    feature_value = "d:2"
                elif dist < 8:
                    feature_value = "d:3"
                else:
                    feature_value = "d:4"
                hc.append(self.get_hc_feature_idx(feature_value, mode))

                # stack top3의 의존소 레이블
                for i in range(3):
                    # top1
                    child = state.get_child_of_stack(batch_i, i)
                    feature_value = 'f1_' + str(i) + '_'
                    if child is None:
                        feature_value += 'no'
                    else:
                        # child 로가는 label 가져오기
                        feature_value += child.type

                    hc.append(self.get_hc_feature_idx(feature_value, mode))
                # stack top3의 의존소 갯수 0,1,2,3~
                for i in range(3):
                    # top1
                    child = state.get_num_of_child_of_stack(batch_i, i)
                    feature_value = 'f2_' + str(i) + '_'
                    if child > 3:
                        child = 3
                    feature_value += str(child)

                    hc.append(self.get_hc_feature_idx(feature_value, mode))

                # x_mor = np.concatenate((left_mor_cnn_input,right_mor_cnn_input),axis=0)
                # x_pos =  np.concatenate((left_pos_cnn_input, right_pos_cnn_input),axis=0)
                x_mor = left_mor_cnn_input + right_mor_cnn_input
                x_pos = left_pos_cnn_input + right_pos_cnn_input

                sentence = [x_mor, x_pos, child_mor, child_pos]
                hcs.append(hc)
                # sentence = [x_mor, x_pos,child_mor,child_pos ]

                sentences.append(sentence)

            # sentences = np.array(sentences)
            return sentences, hcs
        elif mode == 'train':
            left_mor_cnn_input = [0] * self.max_length
            left_pos_cnn_input = [0] * self.max_length
            nth_queue = 0
            idx_eoj = state.nth_queue(nth_queue, 0)
            idx_input = self.max_length - 1
            while idx_input > 0:
                eoj = data[0].eojeol_list[idx_eoj]
                mor_list = eoj.morpheme_list
                idx_mor0 = self.get_mor_feature_idx(mor_list[0].lex + '/' + mor_list[0].pos, mode)
                idx_mor2 = self.get_mor_feature_idx(self.empty_dummy.lex + '/' + self.empty_dummy.pos, mode)
                idx_mor1 = self.get_mor_feature_idx(self.empty_dummy.lex + '/' + self.empty_dummy.pos, mode)
                idx_mor3 = self.get_mor_feature_idx(mor_list[-1].lex + '/' + mor_list[-1].pos, mode)

                idx_pos0 = self.get_pos_feature_idx(mor_list[0].pos, mode)
                idx_pos1 = self.get_pos_feature_idx(self.empty_dummy.pos, mode)
                idx_pos2 = self.get_pos_feature_idx(self.empty_dummy.pos, mode)
                idx_pos3 = self.get_pos_feature_idx(mor_list[-1].pos, mode)

                if len(mor_list) >= 2:
                    idx_mor1 = self.get_mor_feature_idx(mor_list[1].lex + '/' + mor_list[1].pos, mode)
                    idx_mor2 = self.get_mor_feature_idx(mor_list[-2].lex + '/' + mor_list[-2].pos, mode)

                    idx_pos1 = self.get_pos_feature_idx(mor_list[1].pos, mode)
                    idx_pos2 = self.get_pos_feature_idx(mor_list[-2].pos, mode)
                left_mor_cnn_input[idx_input] = idx_mor3
                left_pos_cnn_input[idx_input] = idx_pos3
                idx_input -= 1
                left_mor_cnn_input[idx_input] = idx_mor2
                left_pos_cnn_input[idx_input] = idx_pos2
                idx_input -= 1
                left_mor_cnn_input[idx_input] = idx_mor1
                left_pos_cnn_input[idx_input] = idx_pos1
                idx_input -= 1
                left_mor_cnn_input[idx_input] = idx_mor0
                left_pos_cnn_input[idx_input] = idx_pos0
                idx_input -= 1
                nth_queue += 1
                idx_eoj = state.nth_queue(0, nth_queue)
                if idx_eoj is None:
                    break

            right_mor_cnn_input = [0] * self.max_length
            right_pos_cnn_input = [0] * self.max_length
            nth_stack = 0
            idx_eoj = state.nth_stack(0, nth_stack)
            idx_input = self.max_length - 1
            while idx_input > 0:

                eoj = data[0].eojeol_list[idx_eoj]
                mor_list = eoj.morpheme_list
                idx_mor0 = self.get_mor_feature_idx(mor_list[0].lex + '/' + mor_list[0].pos, mode)
                idx_mor1 = self.get_mor_feature_idx(self.empty_dummy.lex + '/' + self.empty_dummy.pos, mode)
                idx_mor2 = self.get_mor_feature_idx(self.empty_dummy.lex + '/' + self.empty_dummy.pos, mode)
                idx_mor3 = self.get_mor_feature_idx(mor_list[-1].lex + '/' + mor_list[-1].pos, mode)

                idx_pos0 = self.get_pos_feature_idx(mor_list[0].pos, mode)
                idx_pos1 = self.get_pos_feature_idx(self.empty_dummy.pos, mode)
                idx_pos2 = self.get_pos_feature_idx(self.empty_dummy.pos, mode)
                idx_pos3 = self.get_pos_feature_idx(mor_list[-1].pos, mode)

                if len(mor_list) >= 2:
                    idx_mor1 = self.get_mor_feature_idx(mor_list[1].lex + '/' + mor_list[1].pos, mode)
                    idx_mor2 = self.get_mor_feature_idx(mor_list[-2].lex + '/' + mor_list[-2].pos, mode)
                    idx_pos1 = self.get_pos_feature_idx(mor_list[1].pos, mode)
                    idx_pos2 = self.get_pos_feature_idx(mor_list[-2].pos, mode)
                right_mor_cnn_input[idx_input] = idx_mor3
                right_pos_cnn_input[idx_input] = idx_pos3
                idx_input -= 1
                right_mor_cnn_input[idx_input] = idx_mor2
                right_pos_cnn_input[idx_input] = idx_pos2
                idx_input -= 1
                right_mor_cnn_input[idx_input] = idx_mor1
                right_pos_cnn_input[idx_input] = idx_pos1
                idx_input -= 1
                right_mor_cnn_input[idx_input] = idx_mor0
                right_pos_cnn_input[idx_input] = idx_pos0
                idx_input -= 1
                nth_stack += 1
                idx_eoj = state.nth_stack(0, nth_stack)
                if idx_eoj is None:
                    break

            # topn'child feature
            child_mor = [0] * self.max_length
            child_pos = [0] * self.max_length
            idx_input = self.max_length - 1
            for i in range(self.window_size):
                # head의 가장가까운 child
                child = state.get_child_of_stack(0, i)
                if child is not None:
                    eoj = data[0].eojeol_list[child.index]
                    mor_list = eoj.morpheme_list
                    idx_mor0 = self.get_mor_feature_idx(mor_list[0].lex + '/' + mor_list[0].pos, mode)
                    idx_mor2 = self.get_mor_feature_idx(self.empty_dummy.lex + '/' + self.empty_dummy.pos, mode)
                    idx_mor1 = self.get_mor_feature_idx(self.empty_dummy.lex + '/' + self.empty_dummy.pos, mode)
                    idx_mor3 = self.get_mor_feature_idx(mor_list[-1].lex + '/' + mor_list[-1].pos, mode)

                    idx_pos0 = self.get_pos_feature_idx(mor_list[0].pos, mode)
                    idx_pos1 = self.get_pos_feature_idx(self.empty_dummy.pos, mode)
                    idx_pos2 = self.get_pos_feature_idx(self.empty_dummy.pos, mode)
                    idx_pos3 = self.get_pos_feature_idx(mor_list[-1].pos, mode)

                    if len(mor_list) >= 2:
                        idx_mor1 = self.get_mor_feature_idx(mor_list[1].lex + '/' + mor_list[1].pos, mode)
                        idx_mor2 = self.get_mor_feature_idx(mor_list[-2].lex + '/' + mor_list[-2].pos, mode)

                        idx_pos1 = self.get_pos_feature_idx(mor_list[1].pos, mode)
                        idx_pos2 = self.get_pos_feature_idx(mor_list[-2].pos, mode)

                    child_mor[idx_input] = idx_mor3
                    child_pos[idx_input] = idx_pos3
                    idx_input -= 1
                    child_mor[idx_input] = idx_mor2
                    child_pos[idx_input] = idx_pos2
                    idx_input -= 1
                    child_mor[idx_input] = idx_mor1
                    child_pos[idx_input] = idx_pos1
                    idx_input -= 1
                    child_mor[idx_input] = idx_mor0
                    child_pos[idx_input] = idx_pos0
                    idx_input -= 1
                else:
                    child_mor[idx_input] = 0
                    child_pos[idx_input] = 0
                    idx_input -= 1
                    child_mor[idx_input] = 0
                    child_pos[idx_input] = 0
                    idx_input -= 1
                    child_mor[idx_input] = 0
                    child_pos[idx_input] = 0
                    idx_input -= 1
                    child_mor[idx_input] = 0
                    child_pos[idx_input] = 0
                    idx_input -= 1

            # handcrafted feature
            hc = []

            # 거리
            # self.hc_feature_map = {'dist:1': 1, 'dist:2': 2, 'dist:3~4': 3, 'dist:5~7': 4, 'dist:8~': 5}
            ts = state.top_stack(0)
            tq = state.top_queue(0)
            dist = ts - tq
            if ts is -1:
                dist = 1
            if dist < 2:
                feature_value = "d:0"
            elif dist < 3:
                feature_value = "d:1"
            elif dist < 5:
                feature_value = "d:2"
            elif dist < 8:
                feature_value = "d:3"
            else:
                feature_value = "d:4"
            hc.append(self.get_hc_feature_idx(feature_value, mode))

            # stack top3의 의존소 레이블
            for i in range(3):
                # top1
                child = state.get_child_of_stack(0, i)
                feature_value = 'f1_' + str(i) + '_'
                if child is None:
                    feature_value += 'no'
                else:
                    # child 로가는 label 가져오기
                    feature_value += child.type

                hc.append(self.get_hc_feature_idx(feature_value, mode))
            # stack top3의 의존소 갯수 0,1,2,3~
            for i in range(3):
                # top1
                child = state.get_num_of_child_of_stack(0, i)
                feature_value = 'f2_' + str(i) + '_'
                if child > 3:
                    child = 3
                feature_value += str(child)

                hc.append(self.get_hc_feature_idx(feature_value, mode))

            return left_mor_cnn_input, left_pos_cnn_input, right_mor_cnn_input, right_pos_cnn_input, \
                   child_mor, child_pos, hc

    @staticmethod
    def convert_to_zero_one(feature_list, size , mode = 'test'):
        # hc = [0] * size
        if mode == 'test':
            hc = np.zeros([len(feature_list), size])
            for batch_idx, hc_feature in enumerate(feature_list):
                for hc_feature in hc_feature:
                    hc[batch_idx][int(hc_feature)] = 1
            return hc
        elif mode == 'train':
            hc = [0] * size
            for hc_feature in feature_list:
                hc[int(hc_feature)] = 1
            return hc


class InputFeature(object):
    def __init__(self):
        self.left_mor_cnn = []
        self.left_pos_cnn = []
        self.right_mor_cnn = []
        self.right_pos_cnn = []
        self.child_mor = []
        self.child_pos = []
        self.hand_crafted = []
        self.y = None

    def set(self, left_mor_cnn_input, left_pos_cnn_input, right_mor_cnn_input, right_pos_cnn_input,
            child_mor, child_pos, hc,
            output_sample=None):
        self.left_mor_cnn = left_mor_cnn_input
        self.left_pos_cnn = left_pos_cnn_input
        self.right_mor_cnn = right_mor_cnn_input
        self.right_pos_cnn = right_pos_cnn_input
        self.child_mor = child_mor
        self.child_pos = child_pos
        self.hand_crafted = hc
        self.y = output_sample
