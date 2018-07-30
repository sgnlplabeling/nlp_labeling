#-*-* coding:utf-8 -*-
import torch
from torch.autograd import Variable
from utils import loading_dic,data_loading,create_word2idx,\
        create_data,evaluation,loading_embedding,predict

from torch_model import PointerNetworks
import numpy as np
import random
import copy
import os
import optparse
from collections import OrderedDict
import pickle

optparser = optparse.OptionParser()
optparser.add_option(
    "-T", "--train", default="../data_set/donga_Tr.txt",
    help="Train set location")

optparser.add_option(
    "-d", "--dev", default="../data_set/donga_Te.txt",
    help="Dev set location")

optparser.add_option(
    "-t", "--test", default="../data_set/donga_Te.txt",
    help="Test set location")

optparser.add_option(
    "-w", "--word_dim", default="64",
    type='int', help="Token embedding dimension")

optparser.add_option(
    "-l", "--lstm_dim", default="200",
    type='int', help="Token LSTM hidden layer size")

optparser.add_option(
    "-p", "--pre_emb", default="../resource/word_embedding.pkl",
    help="Location of pretrained embeddings")

optparser.add_option(
    "-D", "--dropout", default="0.2",
    type="float", help="Dropout on the input(0=no dropout)")

optparser.add_option(
    "-M", "--mode", default = "0",
    type="int", help="Training mode = 0, Predict mode = 1")

optparser.add_option(
    "-E", "--epoch", default ="10",
    type="int", help="train epoch num ... ")

optparser.add_option(
    "-P", "--predict", default="../input/input.txt",
    help = "target file location")

opts = optparser.parse_args()[0]

parameters = OrderedDict()
parameters["word_dim"] = opts.word_dim
parameters["lstm_dim"] = opts.lstm_dim
parameters["pre_emb"] = opts.pre_emb
parameters["dropout"] = opts.dropout
parameters["mode"] = opts.mode


with open("../resource/p_dic_value.pkl","rb") as fout: #형태소 태그 사전을 loading. 
    p_dic = pickle.load(fout)

with open("../resource/r_dic_value.pkl","rb") as fout: #의존 관계명 사전을 loading.
    r_dic = pickle.load(fout)

def Train_Mode():
 
    print ("\n","Train Mode select ... ","\n")

    assert os.path.isfile(opts.train)
    assert os.path.isfile(opts.dev)
    assert os.path.isfile(opts.test)

    try : #pre_emb 파일이 있으면 embedding file을 loading.
        assert os.path.isfile(opts.pre_emb)
        with open(opts.pre_emb,"rb") as fout:
            embedding = pickle.load(fout)
        print ("vocab loading success ... ")
    except : #pre_emb 파일이 없으면 random embedding으로 학습 수행.
        print ("embedding is random...")
        embeddings = {} 
    
    Tr_data = []
    Te_data = []
    Dev_data = []

    Tr_data = data_loading(opts.train,p_dic,"+") #학습 데이터 loading.
    Dev_data = data_loading(opts.dev,p_dic,"+") #평가 데이터 loading.
    Te_data = data_loading(opts.test,p_dic,"+") #개발 데이터 loading.
    print ("data_loading success ...")


    word_dim = parameters["word_dim"] #word embedding의 dimensions
    word2idx = create_word2idx(Tr_data,p_dic) # key:word, value:index의 형태로 dictionary 생성.
    print ("word2idx create success ...")

    #embedding layer 초기 weights는 random 사용.
    matrix = np.random.uniform(-np.sqrt(1.0),np.sqrt(1.0),(len(word2idx),word_dim))

    for w in word2idx:
        if w in embeddings:
            matrix[word2idx[w]] = embeddings[w] #word2id에 있는 word가 pretrained된 embedding이 있으면 matrix 변환.
    print ("word matrix create success ...")

    with open("./Pickles/word2idx.pkl","wb") as fout: #word2id를 pickle타입으로 저장.
        pickle.dump(word2idx,fout)
    print ("Pickle file save success ...")


    Tr = create_data(Tr_data,word2idx,r_dic) #data를 학습이 가능한 형태로 변환.(각 형태소 및 태그를 형태소 단위로 변환)
    Dev = create_data(Dev_data,word2idx,r_dic)
    Te = create_data(Te_data,word2idx,r_dic)

    #Pointer Networks 모델 생성.
    Model = PointerNetworks(word_dim = parameters["word_dim"],\
                            lstm_width=parameters["lstm_dim"], #lstm dimensions
                            nword=len(word2idx), 
                            weights = matrix,
                            drop_rate = parameters["dropout"]) #드랍아웃 파라미터.
    print ("Model Create...")

    optimizer = torch.optim.Adam(Model.parameters(), lr=0.0001) #optimizer 정의. learning rate는 0.0001
    max_v = -100 # dev data를 이용하여 가장 높은 성능을 기록하는 변수.

    Model.train(True)
    for e in range(opts.epoch):
        losses = []
        #random.shuffle(Tr)
        for i in range(len(Tr)):
            input = Tr[i]
            Model.zero_grad()
            train_dic = {"inputs":input["morphemes"],\
                         "prime_idx":input["prime_idx"],\
                         "istrain" : 1,\
                         "drop_rate" : 0.2,\
                         "point_idx":input["point_idx"],\
                         "pointings":input["pointings"]}

            _,predict_points,predict_labels,_1 = Model(train_dic)
            answer_point = input["point_idx"]
            answer_point = torch.LongTensor(answer_point)
            answer_label = input["label_idx"]
            answer_label = torch.LongTensor(answer_label)
            cost1 = torch.nn.functional.cross_entropy(predict_points,Variable(answer_point)) #의존 관계에 대한 Loss계산.
            cost2 = torch.nn.functional.cross_entropy(predict_labels,Variable(answer_label)) #의존 관계명에 대한 Loss 계산.
            costs = 0.8*cost1 + 0.2*cost2 #cost1과 cost2의 반영 비율에 따라 계산.
            costs.backward()
            torch.nn.utils.clip_grad_norm(Model.parameters(), 5.0)
            optimizer.step()
            losses.append(float(costs)) #한 문장에 대한 loss append.
            if len(losses) == 3000: #1000문장당 loss출력 및 dev data 평가, 성능이 오를때마다 model save.
                print ("Epoch : "+str(e)+", sentence_num : "+str(i+1)+", average_loss : "+str(round(sum(losses)/len(losses),2))+", max_uas : "+str(max_v))
                losses = []
                Model.train(False)
                if e > 2:
                    uas,las = evaluation(Model,Dev) #dev data 평가.
                    if uas > max_v: # uas가 max_v보다 높으면 max_v 교체.
                        max_v = uas
                        print ("Best Model chanes ... ")
                        torch.save(Model,"BestModel.pt") #model save.
                Model.train(True)
                

def Predict_Mode():
    print ("\n","Test Mode select ... ","\n")

    id2tag = dict((y,x) for x,y in r_dic.items()) #인덱스를 key로, 관계명을 value인 dictionary.

    with open("./Pickles/word2idx.pkl","rb") as fout: #학습에 사용된 동일한 word2id loading.
        word2idx = pickle.load(fout)

    Model = torch.load("BestModel.pt") #best model reload.
    Pre_data = data_loading(opts.predict,p_dic,"+") #predict할 파일 loading
    sentence = []
    for line in open(opts.predict):
        line = line.strip()
        if len(line) == 0:
            continue
        if line[0] == ";":
            sentence.append(line)

    out = open("../output/result.txt","w") #의존관계 결과를 저장할 파일.
    Pre = create_data(Pre_data,word2idx,r_dic)
    Model.train(False)
    for i in range(len(Pre_data)):
        out.write(sentence[i]+"\n")
        points,labels = predict(Model,Pre[i]) #한 문장마다 best model로 예측 수행.
        points[-1] = -1
        for j in range(len(Pre_data[i][:-1])):
            input = Pre_data[i][j]
            out.write(str(input["current_idx"]+1)+"\t"+\
                      str(points[j]+1)+"\t"+\
                      id2tag[labels[j]]+"\t"+\
                      input["pure_morphemes"]+"\n")
        out.write("\n")
    print ("predict success ... ")



if parameters["mode"] == 0: #mode가 0이면 training 수행
    Train_Mode()
else:
    Predict_Mode() #mode가 1이면 predict수행

