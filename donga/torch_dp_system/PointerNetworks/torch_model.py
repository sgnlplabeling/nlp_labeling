import torch
import numpy as np
import torch.nn as nn
from torch.autograd import Variable
import torch.nn.functional as F

#layer 초기화 function.
def init_linear(input_linear):
    bias = np.sqrt(6.0 / (input_linear.weight.size(0) + input_linear.weight.size(1)))
    nn.init.uniform(input_linear.weight, -bias, bias)
    if input_linear.bias is not None:
        input_linear.bias.data.zero_()

#embedding 초기화 function.
def init_embedding(input_embedding):
    """
    Initialize embedding
    """
    bias = np.sqrt(3.0 / input_embedding.size(1))
    nn.init.uniform(input_embedding, -bias, bias)

#lstm hidden 초기화 function.
def init_lstm(input_lstm):
    """
    Initialize lstm
    """
    for ind in range(0, input_lstm.num_layers):
        weight = eval('input_lstm.weight_ih_l' + str(ind))
        bias = np.sqrt(6.0 / (weight.size(0) / 4 + weight.size(1)))
        nn.init.uniform(weight, -bias, bias)
        weight = eval('input_lstm.weight_hh_l' + str(ind))
        bias = np.sqrt(6.0 / (weight.size(0) / 4 + weight.size(1)))
        nn.init.uniform(weight, -bias, bias)

    if input_lstm.bidirectional:
        for ind in range(0, input_lstm.num_layers):
            weight = eval('input_lstm.weight_ih_l' + str(ind) + '_reverse')
            bias = np.sqrt(6.0 / (weight.size(0) / 4 + weight.size(1)))
            nn.init.uniform(weight, -bias, bias)
            weight = eval('input_lstm.weight_hh_l' + str(ind) + '_reverse')
            bias = np.sqrt(6.0 / (weight.size(0) / 4 + weight.size(1)))
            nn.init.uniform(weight, -bias, bias)

    if input_lstm.bias:
        for ind in range(0, input_lstm.num_layers):
            weight = eval('input_lstm.bias_ih_l' + str(ind))
            weight.data.zero_()
            weight.data[input_lstm.hidden_size: 2 * input_lstm.hidden_size] = 1
            weight = eval('input_lstm.bias_hh_l' + str(ind))
            weight.data.zero_()
            weight.data[input_lstm.hidden_size: 2 * input_lstm.hidden_size] = 1
        if input_lstm.bidirectional:
            for ind in range(0, input_lstm.num_layers):
                weight = eval('input_lstm.bias_ih_l' + str(ind) + '_reverse')
                weight.data.zero_()
                weight.data[input_lstm.hidden_size: 2 * input_lstm.hidden_size] = 1
                weight = eval('input_lstm.bias_hh_l' + str(ind) + '_reverse')
                weight.data.zero_()
                weight.data[input_lstm.hidden_size: 2 * input_lstm.hidden_size] = 1

#Encoder class
class Encoder(nn.Module):
    def __init__(self,word_dim,lstm_width, nword,drop_rate,weights = False):
        super(Encoder, self).__init__()
        self.lstm_width = lstm_width  # lstm hidden width
        self.nword = nword # lengh of word2idx
        self.word_dim = word_dim # word embedding dimensions
        self.num_layers = 2 

        self.lookuptable = nn.Embedding(self.nword,self.word_dim) #embedding layer 정의.
        if weights is not False:
             self.lookuptable.weight = nn.Parameter(torch.FloatTensor(weights))
        #LSTM 정의, bidirectional LSTM 사용.
        self.LSTM = nn.LSTM(self.word_dim,self.lstm_width,self.num_layers,bidirectional=True)
        self.drop_layer = nn.Dropout(p=drop_rate) #dropout 정의.
        init_lstm(self.LSTM) #lstm initializing.

    def forward(self,for_inputs,prime_idxs):

        projection_inputs = self.lookuptable(for_inputs).unsqueeze(1) #embedding layer 거쳐 word_dim으로 표현.
        
        enc_state,_ = self.LSTM(self.drop_layer(projection_inputs))
        enc_state = enc_state.view(len(for_inputs),self.lstm_width*2)
        prime_state = []
        for idx in prime_idxs:
            prime_state.append(enc_state[idx]) #어절의 대표형태소 추출.
        prime_state = torch.stack(prime_state,0).unsqueeze(1)
        return prime_state
        
#Decoder class        
class Decoder(nn.Module):
    def __init__(self,lstm_width,drop_rate):
        super(Decoder,self).__init__()
        self.lstm_width = lstm_width
        self.num_layers = 2        
        self.De_LSTM = nn.LSTM(self.lstm_width*2,self.lstm_width,self.num_layers) #decoder lstm 정의.
        self.drop_layer = nn.Dropout(p=drop_rate)
        init_lstm(self.De_LSTM)
        self.layer_size = int(self.lstm_width*5/2) #layer hidden node 수 계산.

        #score_y1,y2는 의존 관계를 계산하는 layer.
        self.score_y1 = nn.Linear(self.lstm_width*5,self.layer_size) 
        self.score_y2 = nn.Linear(self.layer_size,1)

        #score_z1,z2는 의존 관계명을 계산하는 layer.
        self.score_z1 = nn.Linear(self.lstm_width*5,self.layer_size)
        self.score_z2 = nn.Linear(self.layer_size,36)

        init_linear(self.score_y1) #layer initializing
        init_linear(self.score_y2)
        init_linear(self.score_z1)
        init_linear(self.score_z2)

    #의존 관계를 계산할 때 attention score를 이용하여 계산. attention를 계산하는 function.
    def attention(self,idx,src_vector,dec_state):
        scores = []
        conc1 = torch.cat((dec_state,src_vector),1)
         
        for i in range(len(self.prime_state)):
            vector = torch.cat((conc1,self.prime_state[i]),1)
            layer1 = F.tanh(self.score_y1(vector))
            layer2 = self.score_y2(layer1) # 어절과 어절사이의 계산된 score(스칼라).
            scores.append(layer2.squeeze(0))
        return scores
    
    def forward(self,inputs,istrain,point_idx):
        self.prime_state = inputs
        predict_points = []
        predict_labels = []
        predict_points_idx = []
        predict_labels_idx = []

        dec_state, _ = self.De_LSTM(self.drop_layer(inputs)) #encoding된 값을 이용하여 decoding 수행.
        dec_state = dec_state.view(len(inputs),self.lstm_width)
        dec_state = dec_state.unsqueeze(1)

        for i in range(len(inputs)):
            score = self.attention(i,inputs[i],dec_state[i]) #현재 한 어절과 나머지 어절 사이 score를 계산한 list.
            score = torch.stack(score,0).squeeze(1)
            predict_points.append(score)
            if istrain == 1: #training 중이면 정답 의존 관계를 사용.
                p_idx = point_idx[i]
            else:
                max_val,max_idx = torch.max(score,0) #test중에는 실제 예측한 값의 의존 관계를 사용.
                p_idx = int(max_idx)

            predict_points_idx.append(p_idx)
            conc1 = torch.cat((inputs[i],dec_state[i]),1)
            vector = torch.cat((conc1,self.prime_state[p_idx]),1)
            layer1 = F.relu(self.score_z1(vector))
            layer2 = self.score_z2(layer1)
            layer2 = layer2.squeeze() #어절 사이의 의존 관계명을 계산한 분포.
            max_label_val, max_label_idx = torch.max(layer2,0)
            predict_labels_idx.append(int(max_label_idx))
            predict_labels.append(layer2)
        predict_points = torch.stack(predict_points)
        predict_labels = torch.stack(predict_labels).squeeze(1)
        return predict_points_idx,predict_points, predict_labels,predict_labels_idx
        
class PointerNetworks(nn.Module):
    def __init__(self,word_dim,lstm_width, nword,weights,drop_rate):
        super(PointerNetworks, self).__init__()
        self.lstm_width = lstm_width #lstm hidden size.
        self.word_dim = word_dim #word embedding dimensions.
        self.nword = nword 
        self.word_weights = weights #embedding weights.
        self.BI_encoder = Encoder(word_dim = word_dim,lstm_width = self.lstm_width,nword = self.nword,drop_rate=drop_rate,weights = self.word_weights) #Encoder 생성.
        self.decoder = Decoder(lstm_width = self.lstm_width,drop_rate = drop_rate) #decoder 생성.

    def forward(self,dic):
        prime_state = self.BI_encoder(Variable(torch.LongTensor(dic["inputs"])),\
                                      dic["prime_idx"]) #encoding value 계산.
        points_idx,points, labels, labels_idx = self.decoder(prime_state,\
                                      dic["istrain"],
                                      torch.LongTensor(dic["point_idx"])) #의존 관계 및 의존 관계명 계산.
        return points_idx,points,labels,labels_idx


