# -*- coding: utf-8 -*-

'''
Created on 2017-05-07

@author: pymnlp
@description :
'''

# 파서 학습하기
from DataTools import CorpusReader, Dependency
from FeatureModel import FeatureModel, InputFeature


class TransitionState(object):
    def __init__(self,len_data):
        self.stack = [[] for _ in range(len_data)]
        self.queue = [[] for _ in range(len_data)]
        self.predict = [[] for _ in range(len_data)]
        self.transition_sequence = [[] for _ in range(len_data)]

    def get_child_of_stack(self, i, n):
        if len(self.stack) < n:
            return None
        head_idx = self.nth_stack(i, n)
        # predict에서 찾아보기 가장 가까운것으로..
        min_len = 99999
        rtn_p = None
        for p in self.predict[i]:
            if p.head == head_idx:
                if abs(head_idx - p.index) < min_len:
                    min_len = abs(head_idx - p.index)
                    rtn_p = p

        return rtn_p

    def get_num_of_child_of_stack(self, i, n):
        if len(self.stack[i]) < n:
            return -1
        head_idx = self.nth_stack(i, n)
        num = 0
        for p in self.predict[i]:
            if p.head == head_idx:
                num += 1

        return num

    def left(self, tag='none', batch_idx = 10000000):
        i = self.top_stack(batch_idx)
        # queue의 top을 stack에 push
        j = self.pop_queue(batch_idx)
        self.push_stack(batch_idx, j)
        self.transition_sequence[batch_idx].append('left')
        dep = Dependency()
        dep.index = j
        dep.head = i
        dep.type = tag
        self.predict[batch_idx].append(dep)

    def reduce(self, batch_idx):
        self.pop_stack(batch_idx)
        self.transition_sequence[batch_idx].append('reduce')

    def initialize_state(self, data):
        len_data = len(data)
        self.stack = [ [] for _ in range(len(data))]
        self.queue = [ [] for _ in range(len(data))]
        self.predict = [ [] for _ in range(len(data))]
        self.transition_sequence = [ [] for _ in range(len(data))]

        for i, sentence in enumerate(data):
            for j in range(sentence.get_size() - 1, -1, -1):
                self.push_queue(i,j)
            self.push_stack(i,-1)

    def is_final_state(self):
        for batch_idx, queue in enumerate(self.queue):
            if len(queue) > 0:
                return False
        return True

    def push_stack(self, i, j):
        self.stack[i].append(j)

    def pop_stack(self, i):
        return self.stack[i].pop()

    def top_stack(self, i):
        return self.stack[i][-1]

    def nth_stack(self, i, n):
        if len(self.stack[i]) <= n:
            return None
        n = - n - 1
        return self.stack[i][n]

    def push_queue(self, i, j):
        self.queue[i].append(j)

    def pop_queue(self, i):
        return self.queue[i].pop(0)

    def top_queue(self, i):
        return self.queue[i][0]

    def nth_queue(self, i, n):
        if len(self.queue[i]) <= n:
            return None
        return self.queue[i][n]

    def get_next_gold_transition(self, data, model):
        i = self.top_stack(0)
        j = self.top_queue(0)

        gold_head = data[0].correct_dep_list[j]
        gold_type = gold_head.type

        if i == gold_head.head:
            self.left(gold_type,0)
            return model.get_type_idx('left_' + gold_type)

        self.reduce(0)
        return model.get_type_idx('reduce')


class TransitionParser(object):
    def __init__(self, model, len_data = None):
        self.state = TransitionState(len_data)
        self.f_model = model

    def make_gold_corpus(self, data):
        total_sample = []
        self.state.initialize_state(data)
        # final_state 가 될때까지 코퍼스 생성
        while not self.state.is_final_state():
            sample = InputFeature()

            left_mor_cnn_input, left_pos_cnn_input, right_mor_cnn_input, right_pos_cnn_input, child_mor, child_pos, hc \
                = self.f_model.make_feature_vector(self.state, data, 'train')

            output_sample = self.state.get_next_gold_transition(data, self.f_model)
            sample.set(left_mor_cnn_input, left_pos_cnn_input, right_mor_cnn_input, right_pos_cnn_input, child_mor,
                       child_pos, hc,
                       output_sample)

            total_sample.append(sample)
        # 정답 검사
        result = self.get_result(mode = 'train')
        golds = data[0].correct_dep_list
        idx = 0
        while idx < len(golds):

            head = result[idx].head
            gold = golds[idx].head
            tag = result[idx].type
            gold_tag = golds[idx].type

            if head != gold or tag != gold_tag:
                print('error')
            idx += 1

        return total_sample

    def make_input_vector(self, data, mode = 'test'):
        return self.f_model.make_feature_vector(self.state, data, mode = mode)

    def initialize(self, data):
        self.state.initialize_state(data)

    def is_final_state(self):
        return self.state.is_final_state()

    def run_action(self, next_action, model, mode = 'test'):
        if mode == 'test':
            next_action = next_action.tolist()
            next_action = model.get_str_type(next_action)
            for batch_idx, na in enumerate(next_action):
                # print (''na)
                if na != 'reduce':
                    action = 'left'
                    tag = na[na.find('_') + 1:]
                else:
                    action = 'reduce'

                if len(self.state.queue[batch_idx]) == 0:
                    #Done
                    continue
                elif action == 'left':
                    self.state.left(tag, batch_idx)
                elif len(self.state.stack[batch_idx]) <= 2:
                    self.state.left('VP', batch_idx)
                    # print('강제left')
                else:
                    self.state.reduce(batch_idx)
        elif mode == 'train':
            next_action = model.get_str_type(next_action, mode)
            if next_action != 'reduce':
                action = 'left'
                tag = next_action[next_action.find('_') + 1:]
            else:
                action = 'reduce'

            if action == 'left':
                self.state.left(tag,0)
            elif len(self.state.stack[0]) <= 2:
                self.state.left('VP',0)
                # print('강제left')

            else:
                self.state.reduce(0)

    def get_result(self, mode = 'test'):
        # predict를 정리해서 출력
        if mode == 'test':
            try:
                predict = self.state.predict
                max_len = len(max(predict, key=lambda x: len(x)))
                # result = [[0] * len(predict)] * len(self.state.predict)
                result = [ [None for _ in range(max_len)] for _ in range(len(self.state.predict))]

                for i in range(len(predict)):
                    for j in range(max_len):
                        if j >= len(predict[i]):
                            break
                        tmp= predict[i][j].index
                        result[i][tmp] = predict[i][j]

                return result
            except:
                a=1
        elif mode == 'train':
            predict = self.state.predict
            result = [0] * len(predict[0])

            for i in range(len(predict[0])):
                result[predict[0][i].index] = predict[0][i]

            return result
