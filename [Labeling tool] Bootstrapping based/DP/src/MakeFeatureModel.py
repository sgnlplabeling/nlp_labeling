# -*- coding: utf-8 -*-

'''
Created on 2017-04-24

@author: pymnlp
@description : 
'''
import pickle

from DataTools import CorpusReader

class MakeFeatureModel:
    def __init__(self):
        pass

class FeatureModel(object):
    def __init__(self):
        self.cat_map = {}  # action 종류 , left_NP...
        self.cat_size = 0  # len(self.cat_map)
        self.feature_map = {}  # word idx
        self.feature_size = 0
        self.max_length = 5

    def add_feature(self, one_doc):

        for eoj in one_doc.eojeol_list :

            if not eoj.rel_tag in self.cat_map:
                # tag 추가
                self.cat_map[eoj.rel_tag] = self.cat_size + 1
                self.cat_size += 1

            for mor in eoj.morpheme_list :
                if not mor in self.feature_map :
                    # feature 추가
                    self.feature_map[mor] = self.feature_size+1
                    self.feature_size += 1
        # max_length
        #if self.max_length < len ( one_doc.mor_list):
        #    self.max_length = len ( one_doc.mor_list)
    def get_feature_idx(self, mor):
        if mor in self.feature_map :
            return self.feature_map.get(mor)
        return 0



def get_feature_model():
    cr = CorpusReader()

    train_filename = 'data/train.txt'
    model = FeatureModel()

    # 코퍼스 파일 읽기
    cr.set_file(train_filename)
    while True :
        data = cr.get_next()
        if data is None :
            break
        model.add_feature(data)
    return model

def save_f_model(f_model) :
    # 파일로 저장
    f = open("f_model", 'w')
    pickle.dump(f_model, f)
    f.close()
def load_f_model() :
    f = open("f_model", 'r')
    f_model = pickle.load(f)
    f.close()
    return f_model


#save_f_model(f_model)
#f_model = load_f_model()






