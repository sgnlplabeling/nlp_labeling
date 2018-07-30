#-*- coding : utf-8 -*-
from __future__ import print_function
#import sys
#reload(sys)
#sys.setdefaultencoding('utf-8')

import random
import numpy as np
import copy

#문장마다 예측하는 function.
def predict(Model,input):
    test_dic = {"inputs":input["morphemes"],\
                "prime_idx":input["prime_idx"],\
                "istrain":0,\
                "point_idx":input["point_idx"],\
                "pointings":input["pointings"]}
    points,_,_1,labels = Model(test_dic)
    return points[:-1],labels[:-1]

#test data를 평가하는 function.
def evaluation(Model,test):
    correct = 0.0 #의존 관계가 맞는 것을 count하는 변수.
    every = 0.0 #전체 어절 수를 count하는 변수.
    label_correct = 0.0 # 의존관계, 의존 관계명 모두 맞는 것을 count하는 변수.

    Model.train(False)
    for i in range(len(test)):
        input = test[i]
        test_dic = {"inputs":input["morphemes"],\
                    "prime_idx":input["prime_idx"],\
                    "istrain": 0,\
                    "drop_rate":1.,\
                    "point_idx":input["point_idx"],\
                    "pointings":input["pointings"]}
        points,_,_1,labels = Model(test_dic)
        answer_points = input["point_idx"]
        answer_labels = input["label_idx"]
        
        for j in range(len(points)-1): #padding인 마지막을 제외한 어절만 평가 수행.
            if int(points[j]) == int(answer_points[j]):
                correct += 1.0
                if int(labels[j]) == int(answer_labels[j]):
                    label_correct +=1.0
            every += 1.0

    print ("UAS : ",str(round(correct/every*100,2))+", LAS : ",str(round(label_correct/every*100,2)))
    return round(correct/every*100,2), round(label_correct/every*100,2)

#size와 index를 주면 one-hot으로 표현하는 function.    
def one_hot(size,idx):
    vector = [0 for i in range(size)]
    vector[idx] = 1
    return vector

#data가 주어지면 학습을 위해 숫자로 변환하는 function.
def create_data(data,word2idx,r_dic):
    datas = []
    for sentence in data:
        pointings = []
        labels = []
        morphemes = []
        prime_idx = []
        point_idx = []
        label_idx = []
        for line in sentence:
            src_morp = line["morpheme"]
            for morp in src_morp:
                word = morp["morpheme"]
                if morp["morpheme"] not in word2idx: #해당 형태소가 없으면 형태소 태그로 치환.
                    word = morp["m_tag"]
                morphemes.append(word2idx[word]) #전체 형태소를 숫자의 형태로 저장.
            prime_idx.append((len(morphemes)-1))  #어절의 대표 형태소의 위치를 저장.
            morphemes.append(word2idx["<SP>"]) #어절을 구분하기 위해 <SP> simbol 추가.
            pointings.append(one_hot(len(sentence),line["pointing_idx"])) #의존 관계 정답 위치 one-hot.
            point_idx.append(line["pointing_idx"]) #의존 관계 위치 저장.
            labels.append(one_hot(len(r_dic),r_dic[line["label"]])) #의존 관계명 one-hot.
            label_idx.append(r_dic[line["label"]]) #의존 관계명 숫자로 저장.
        datas.append({"prime_idx":prime_idx,"morphemes":morphemes[:-1],"pointings":pointings,"labels":labels,"point_idx":point_idx,"label_idx":label_idx}) 
    return datas

#word2idx를 만드는 function.
def create_word2idx(data,p_dic):
    word2idx = {}
    morp = []
    word_freq = {} #형태소의 빈도를 저장하기 위한 dictionary.

    p_dic_keys = list(p_dic.keys())
    
    #형태소 태그를 저장.
    for key in p_dic_keys:
        if key not in word2idx:
            word2idx[key] = len(word2idx)

    word2idx["<SP>"] = len(word2idx) #어절을 구분하기 위한 공백simbol

    for sentence in data:
        for line in sentence:
            morphemes = line["morpheme"]
            
            for m in morphemes:
                morp.append(m["morpheme"])
                if m["morpheme"] not in word_freq:
                    word_freq[m["morpheme"]] = 1
                else:
                    word_freq[m["morpheme"]]+=1


    word_freq_keys = list(word_freq.keys())
    for k in word_freq_keys:
        if (word_freq[k]) > 5 and (k not in word2idx): #cut off에 대한 부분. 빈도가 5 초과인 형태소들에 대해서 word2idx에 추가
            word2idx[k] = len(word2idx)

    return word2idx

#형태소 태그 및 관계명 태그에 사용하는 function.
def loading_dic(filename):
    dic = {}
    for line in open(filename):
        line = line.strip()
        line = line.split(" ")
        dic[line[0]] = int(line[1])
    return dic

#embedding file을 loading하는 function.
def loading_embedding(filename):
    dic = {}
    for line in open(filename):
        line = line.strip()
        line = line.split(" ")
        vector = []
        for v in line[1:]:
            vector.append(float(v))
        dic[line[0]] = np.array(vector)
    return dic

#data를 loading하는 function
def data_loading(filename,p_dic,symbol):
    sentences = []
    sentence = []
    for line in open(filename):
        line = line.strip()
        if len(line) < 2:
            extracted_sentence = dependency_infor_extractor(sentence,p_dic,symbol)
            sentences.append(extracted_sentence)
            if len(sentences) % 1000 == 0:
                print (str(len(sentences))+" sentence loading success...")
            sentence = []
            continue
        if line[0] == ";":
            continue
        line = line.split("\t")
        line[0] = int(line[0])-1
        line[1] = int(line[1])-1
        sentence.append(line)
        
    return sentences

#어절 안의 형태소들을 형태소 단위로 잘라주는 function.
def word_to_morp(p_dic,word,symbol):
    p_keys = list(p_dic.keys())
    for i in range(len(p_keys)):
        new_tag = str(p_keys[i])+" "
        old_tag = str(p_keys[i])+symbol
        word = word.replace(old_tag, new_tag)
    return word

#형태소와 형태소태그를 분리하는 function.
def replace_tag(p_dic,word,symbol):
    p_keys = list(p_dic.keys())
    for i in range(len(p_keys)):
        new_tag = " "+str(p_keys[i])
        old_tag = symbol+str(p_keys[i])
        word = word.replace(old_tag,new_tag)
    return word

#문장마다 형태소 및 의존 관계, 의존 관계명을 추출하는 함수
def dependency_infor_extractor(sentence,p_dic,symbol):
    final_idx = sentence[-1][0]+1 
    sentence[-1][1] = final_idx #root index는 마지막 어절의 뒤로 정의.
    sentence.append([final_idx,final_idx,"VP","<eos>/EOS"]) #문장의 끝을 알려주는 simbol 추가. loss와 optimizing은 하지않음.
    data = []
    for line in sentence:
        word = line[-1]
        morpheme = word_to_morp(p_dic,word,symbol)
        morpheme = morpheme.split(" ")
        morpheme_list = []
        syllable_list = []
        eojeol_lexical = ""

        for m in morpheme:
            tag = replace_tag(p_dic,m,"/")
            tag = tag.split(" ")
            lexical = tag[0]
            tag = tag[1]
            if tag == "SN": #숫자 normalize
                lexical = "0"
                m = "0/SN"
            morpheme_list.append({"morpheme":m,"m_tag":tag,"m_lexical":lexical})
        
        data.append({"current_idx":line[0],"pointing_idx":line[1],"label":line[2],\
                "morpheme":morpheme_list,"pure_morphemes":line[-1]})
    return data
