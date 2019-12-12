#-*- coding: utf-8 -*-

from config import Config

config = Config
NONE = "None"
START = "Start"
END = "End"
UNK = "Unk"

def feature_func(model, sentence, pos, predicate_idx, predicate_class, global_idx):
    # 자질 추출 함수
    # input
    # model : ["AIC", "PIC"]
    # sentence : 문장의 형태소 정보 (["공개하/VV"+"ㄴ/ETM"])
    # pos : 문장의 형태소 품사 정보 ("VV"+"ETM")
    # predicate_idx : 술어의 position index 정보 (0~len)
    # predicate_class 술어의 class 정보 (P1, P2, ...)
    # global_idx : 어절 index
    features = [] # 추출한 자질들
    features += extractDefaultFeatures(model, sentence, pos, global_idx, predicate_class, predicate_idx) # word features
    features += extractPrefixSuffix(sentence[global_idx], prefix=2, suffix=2)
    return features

def get_hangul(token):
    hangul = ""
    for t in token:
        hangul += t.split("/")[0]
    return hangul

def extractPrefixSuffix(token, prefix, suffix):
    # 어절의 접두사, 접미사 추출 함수
    features = []
    hangul = get_hangul(token)

    if len(token) == 1:
        if prefix != 0 and len(token[0]) >= prefix:
            for local_idx in range(1,prefix+1):
                features.append("prefix[0]="+hangul[:local_idx])

        if suffix != 0 and len(token[0]) >= suffix:
            for local_idx in range(1, suffix+1):
                features.append("suffix[0]="+hangul[-local_idx:])

    else:
        if prefix != 0 and len(token[0]) >= prefix:
            for local_idx in range(1,prefix+1):
                features.append("prefix[0][%s]="%(local_idx)+hangul[:local_idx])
        if suffix != 0 and len(token[0]) >= suffix:
            for local_idx in range(1, suffix+1):
                features.append("suffix[0][%s]="%(local_idx)+hangul[-local_idx:])

    return features

def extractDefaultFeatures(model, sentence, pos, global_idx, predicate_class, predicate_idx=None):
    # 기본 자질 추출 함수
    features = []
    if model == "AIC":
        if predicate_idx == None:
            pass
        elif global_idx == int(predicate_idx):
            features.append("pred=0")
        elif global_idx < int(predicate_idx):
            features.append("pred=-1")
        elif global_idx > int(predicate_idx):
            features.append("pred=1")

        d = int(predicate_idx)-global_idx
        if d >= 6 :
            d = 6
        elif d <= -6:
            d = -6
        d = str(d)
        features.append("d=" + d)

        pred_eojeol = sentence[int(predicate_idx)]
        for pred in pred_eojeol:
            pred_pumsa = pred.split("/")[-1]

            if pred_pumsa in config.V_PUMSA:
                pred_word_0 = pred
                pred_pos_0 = pred.split("/")[-1]
                break
            elif pred_pumsa in config.N_PUMSA:
                pred_word_0 = pred
                pred_pos_0 = pred.split("/")[-1]
                break
            elif pred_pumsa == "XSV":
                pred_word_0 = pred
                pred_pos_0 = pred.split("/")[-1]
                break
            else:
                pred_word_0 = UNK
                pred_pos_0 = UNK

        pred_word_1 = NONE
        pred_pos_1 = NONE

        if len(sentence[int(predicate_idx)]) != 1:
            pred_word_1 = sentence[int(predicate_idx)][-1]
            pred_pos_1 = pos[int(predicate_idx)][-1]

    if global_idx == 0 :
        prev_word_0 = START
        prev_pos_0 = START
        prev_word_1 = START
        prev_pos_1 = START
    else:
        prev_word_0 = sentence[global_idx-1][0]
        prev_pos_0 = pos[global_idx - 1][0]
        prev_pos_1 = NONE
        prev_word_1 = NONE

        if  len(sentence[global_idx -1]) != 1:
            prev_pos_1 = pos[global_idx - 1][-1]
            prev_word_1 = sentence[global_idx - 1][-1]

    cur_word_1 = NONE
    cur_pos_1 = NONE
    if len(sentence[global_idx]) != 1:
        cur_word_1 = sentence[global_idx][-1]
        cur_pos_1 = pos[global_idx][-1]

    if global_idx != len(sentence)-1:
        next_word_0 = sentence[global_idx+1][0]
        next_pos_0 = sentence[global_idx+1][0]
        next_word_1 = NONE
        next_pos_1 = NONE

        if len(sentence[global_idx + 1]) != 1:
            next_word_1 = sentence[global_idx+1][-1]
            next_pos_1 = pos[global_idx + 1][-1]

    else:
        next_word_0 = END
        next_word_1 = END
        next_pos_0 = END
        next_pos_1 = END

    cur_word_0 = sentence[global_idx][0]
    cur_pos_0 = pos[global_idx][0]

    features.append("F1=" + prev_word_0 + "|" + prev_word_1)
    features.append("F2=" + prev_word_1 + "|" + cur_word_0)
    features.append("F3=" + prev_pos_0 + "|" + prev_pos_1)
    features.append("F4=" + prev_pos_1 + "|" + cur_pos_0)
    features.append("F5=" + cur_word_0 + "|" + cur_word_1)
    features.append("F6=" + cur_pos_0 + "|" + cur_pos_1)
    features.append("F7=" + cur_word_1 + "|" + next_word_0)
    features.append("F8=" + cur_pos_1 + "|" + next_pos_0)
    features.append("F9=" + next_word_0 + "|" + next_word_1)
    features.append("F10=" + next_pos_0 + "|" + next_pos_1)

    if model == "AIC":
        features.append("F11=" + cur_word_0 + "|" + pred_word_0)
        features.append("F12=" + cur_word_0 + "|" + pred_word_1)
        features.append("F13=" + cur_word_1 + "|" + pred_word_0)
        features.append("F14=" + cur_pos_0 + "|" + pred_word_0)
        features.append("F15=" + cur_pos_0 + "|" + pred_word_1)
        features.append("F16=" + cur_pos_1 + "|" + pred_word_0)
        features.append("F17=" + cur_word_0 + "|" + pred_pos_0)
        features.append("F18=" + cur_word_0 + "|" + pred_pos_1)
        features.append("F19=" + cur_word_1 + "|" + pred_pos_0)
        features.append("F20=" + cur_pos_0 + "|" + pred_pos_0)
        features.append("F21=" + cur_pos_0 + "|" + pred_pos_1)
        features.append("F22=" + cur_pos_1 + "|" + pred_pos_0)
        features.append("F23=" + cur_word_0 + "|" + predicate_class)
        features.append("F24=" + cur_word_1 + "|" + predicate_class)
        features.append("F25=" + cur_pos_0 + "|" + predicate_class)
        features.append("F26=" + cur_pos_1 + "|" + predicate_class)
        features.append("F27=" + cur_word_0 + "|" + pred_word_0)
        features.append("F28=" + cur_word_1 + "|" + pred_word_0)
        features.append("F29=" + cur_pos_0 + "|" + pred_word_0)
        features.append("F30=" + cur_pos_1 + "|" + pred_word_0)
        features.append("F31=" + cur_word_0 + "|" + pred_word_1)
        features.append("F32=" + cur_word_1 + "|" + pred_word_1)
        features.append("F33=" + cur_pos_0 + "|" + pred_word_1)
        features.append("F34=" + cur_pos_1 + "|" + pred_word_1)

        features.append("F35=" + prev_word_0 + "|" + predicate_class)
        features.append("F36=" + prev_word_1 + "|" + predicate_class)
        features.append("F37=" + prev_pos_0 + "|" + predicate_class)
        features.append("F38=" + prev_pos_1 + "|" + predicate_class)
        features.append("F39=" + next_word_0 + "|" + predicate_class)
        features.append("F40=" + next_word_1 + "|" + predicate_class)
        features.append("F41=" + next_pos_0 + "|" + predicate_class)
        features.append("F42=" + next_pos_1 + "|" + predicate_class)

        features.append("F43=" + cur_pos_0 + "|" + pred_pos_1)
        features.append("F44=" + cur_pos_1 + "|" + pred_pos_1)

        features.append("F45=" + next_pos_0 + "|" + pred_word_1)
        features.append("F46=" + next_pos_1 + "|" + pred_word_1)
        features.append("F43=" + next_word_0 + "|" + pred_word_0)
        features.append("F44=" + next_word_1 + "|" + pred_word_0)
        features.append("F45=" + next_pos_0 + "|" + pred_word_0)
        features.append("F46=" + next_pos_1 + "|" + pred_word_0)

        features.append("F47=" + prev_word_0 + "|" + d)
        features.append("F48=" + prev_word_1 + "|" + d)
        features.append("F49=" + cur_word_0 + "|" + d)
        features.append("F50=" + cur_word_1 + "|" + d)
        features.append("F51=" + next_word_0 + "|" + d)
        features.append("F52=" + next_word_1 + "|" + d)
        features.append("F53=" + predicate_class + "|" + d)
        features.append("F54=" + pred_word_0 + "|" + d)
        features.append("F55=" + pred_word_1 + "|" + d)

    return features
