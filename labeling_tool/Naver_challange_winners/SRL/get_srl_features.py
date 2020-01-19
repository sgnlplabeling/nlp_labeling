def update_f_dict(feature, l):
    feature = feature.encode("utf-8")
    if feature not in posed_f_dict:
        # posed_f_dict[feature] = {"-":0, "ARG0" : 0, "ARG1" : 0, "ARG2" : 0,	"ARG3" : 0,	"ARGM-CAU" : 0,	"ARGM-CND" : 0,	"ARGM-DIR" : 0,"ARGM-DIS" : 0,	"ARGM-INS" : 0,	"ARGM-LOC" : 0,	"ARGM-MNR" : 0,	"ARGM-NEG" : 0,	"ARGM-PRD" : 0,	"ARGM-PRP" : 0,	"ARGM-TMP" : 0,"ARGM-ADV" : 0,"ARGM-EXT" : 0}
        posed_f_dict[feature] = {"total": 0, "sum": 0}


    if l != "-":
        if feature not in posed_f_dict:
            # posed_f_dict[feature] = {"-":0, "ARG0" : 0, "ARG1" : 0, "ARG2" : 0,	"ARG3" : 0,	"ARGM-CAU" : 0,	"ARGM-CND" : 0,	"ARGM-DIR" : 0,"ARGM-DIS" : 0,	"ARGM-INS" : 0,	"ARGM-LOC" : 0,	"ARGM-MNR" : 0,	"ARGM-NEG" : 0,	"ARGM-PRD" : 0,	"ARGM-PRP" : 0,	"ARGM-TMP" : 0,"ARGM-ADV" : 0,"ARGM-EXT" : 0}
            # posed_f_dict[feature] = {"total": 0, "sum": 0}
            if l not in posed_f_dict[feature]:
                posed_f_dict[feature][l] = 1
            else:
                posed_f_dict[feature][l] += 1
        else:
            if l not in posed_f_dict[feature]:
                posed_f_dict[feature][l] = 1
            else:
                posed_f_dict[feature][l] += 1

        posed_f_dict[feature]['sum'] += 1.
    posed_f_dict[feature]['total'] += 1.

raw_sentences = []
posed_sentences = []
posed_sentence, raw_sentence, label = "", "", ""
labels = []
with open("./data/cm/nlp-challenge/missions/srl/data/train/[naver]komoran_train_data.txt") as f:
    for line in f.readlines():
        if line.strip() == "":
            raw_sentences.append(raw_sentence)
            posed_sentences.append(posed_sentence)
            labels.append(label)
            posed_sentence, raw_sentence, label = "", "", ""
            continue

        _, posed_eojeol, raw_eojoel, l =  line.split()
        posed_sentence += posed_eojeol + " "
        raw_sentence += raw_eojoel + " "
        label += l + " "

posed_f_dict = {}
len_sentence = len(posed_sentences)
for sen_idx, _ in enumerate(posed_sentences):
    print("%s/%s ... " % (sen_idx+1, len_sentence))
    posed_sentence = posed_sentences[sen_idx].split()
    raw_sentence = raw_sentences[sen_idx].split()
    label = labels[sen_idx].split()
    for eojeol_idx, l in enumerate(label):
        posed_eojeol = posed_sentence[eojeol_idx]
        raw_eojoel = raw_sentence[eojeol_idx]

        if eojeol_idx == 0 :
            prev_word1 = "<BOS>"
            prev_word2 = "<BOS>"
            prev_pumsa1 = "<BOS>"
            prev_pumsa2 = "<BOS>"
        else:
            prev_word1 = posed_sentence[eojeol_idx-1].split("|")[0]
            prev_word2 = posed_sentence[eojeol_idx - 1].split("|")[-1]
            prev_pumsa1_idx = prev_word1.rfind("/")
            prev_pumsa2_idx = prev_word2.rfind("/")
            prev_pumsa1 = prev_word1[prev_pumsa1_idx+1:]
            prev_pumsa2 = prev_word2[prev_pumsa2_idx + 1:]

        if eojeol_idx == len(label)-1:
            next_word1 = "<EOS>"
            next_word2 = "<EOS>"
            next_pumsa1 = "<EOS>"
            next_pumsa2 = "<EOS>"
        else:
            next_word1 = posed_sentence[eojeol_idx + 1].split("|")[0]
            next_word2 = posed_sentence[eojeol_idx + 1].split("|")[-1]
            next_pumsa1_idx = next_word1.rfind("/")
            next_pumsa2_idx = next_word2.rfind("/")
            next_pumsa1 = next_word1[next_pumsa1_idx + 1:]
            next_pumsa2 = next_word2[next_pumsa2_idx + 1:]

        cur_word1 = posed_eojeol.split("|")[0]
        cur_word2 = posed_eojeol.split("|")[-1]
        cur_pumsa1_idx = cur_word1.rfind("/")
        cur_pumsa2_idx = cur_word2.rfind("/")
        cur_pumsa1 = cur_word1[cur_pumsa1_idx + 1:]
        cur_pumsa2 = cur_word2[cur_pumsa2_idx + 1:]

        # 모든 feature는 현재 label 기준
        update_f_dict(u"F1:cur_word1+cur_word2 = %s|%s" %(cur_word1, cur_word2), l)
        update_f_dict(u"F2:cur_pumsa1+cur_pumsa2 = %s|%s" % (cur_pumsa1, cur_pumsa2), l)
        update_f_dict(u"F3:cur_word1+next_word1 = %s|%s" % (cur_word1, next_word1), l)
        update_f_dict(u"F4:cur_word1+next_word2 = %s|%s" % (cur_word1, next_word2), l)
        update_f_dict(u"F5:cur_word2+next_word1 = %s|%s" % (cur_word2, next_word1), l)
        update_f_dict(u"F6:cur_word2+next_word2 = %s|%s" % (cur_word2, next_word2), l)

        update_f_dict(u"F7:cur_pumsa1+next_pumsa1 = %s|%s" % (cur_pumsa1, next_pumsa1), l)
        update_f_dict(u"F8:cur_pumsa1+next_pumsa2 = %s|%s" % (cur_pumsa1, next_pumsa2), l)
        update_f_dict(u"F9:cur_pumsa2+next_pumsa1 = %s|%s" % (cur_pumsa2, next_pumsa1), l)
        update_f_dict(u"F10:cur_pumsa2+next_pumsa2 = %s|%s" % (cur_pumsa2, next_pumsa2), l)

        update_f_dict(u"F11:cur_word1+prev_word1 = %s|%s" % (cur_word1, prev_word1), l)
        update_f_dict(u"F12:cur_word1+prev_word2 = %s|%s" % (cur_word1, prev_word2), l)
        update_f_dict(u"F13:cur_word2+prev_word1 = %s|%s" % (cur_word2, prev_word1), l)
        update_f_dict(u"F14:cur_word2+prev_word2 = %s|%s" % (cur_word2, prev_word2), l)

        update_f_dict(u"F15:cur_pumsa1+prev_pumsa1 = %s|%s" % (cur_pumsa1, prev_pumsa1), l)
        update_f_dict(u"F16:cur_pumsa1+prev_pumsa2 = %s|%s" % (cur_pumsa1, prev_pumsa2), l)
        update_f_dict(u"F17:cur_pumsa2+prev_pumsa1 = %s|%s" % (cur_pumsa2, prev_pumsa1), l)
        update_f_dict(u"F18:cur_pumsa2+prev_pumsa2 = %s|%s" % (cur_pumsa2, prev_pumsa2), l)

        update_f_dict(u"F19:prev_word1+next_word1 = %s|%s" % (prev_word1, next_word1), l)
        update_f_dict(u"F20:prev_word1+next_word2 = %s|%s" % (prev_word1, next_word2), l)
        update_f_dict(u"F21:prev_word2+next_word1 = %s|%s" % (prev_word2, next_word1), l)
        update_f_dict(u"F22:prev_word2+next_word2 = %s|%s" % (prev_word2, next_word2), l)

        update_f_dict(u"F23:prev_pumsa1+next_pumsa1 = %s|%s" % (prev_pumsa1, next_pumsa1), l)
        update_f_dict(u"F24:prev_pumsa1+next_pumsa2 = %s|%s" % (prev_pumsa1, next_pumsa2), l)
        update_f_dict(u"F25:prev_pumsa2+next_pumsa1 = %s|%s" % (prev_pumsa2, next_pumsa1), l)
        update_f_dict(u"F26:prev_pumsa2+next_pumsa2 = %s|%s" % (prev_pumsa2, next_pumsa2), l)
    # break
# a=1
import pickle as pk

with open("./data/cm/nlp-challenge/missions/srl/data/dict/1203.pkl", "wb") as f:
    a=1
    pk.dump(posed_f_dict, f)

import pickle as pk
with open("./data/cm/nlp-challenge/missions/srl/data/dict/1203.pkl" ,"rb") as f:
    data = pk.load(f)

data_O = sorted(data.items(), key=lambda x: x[1]['sum'], reverse=True)


with open("./data/cm/nlp-challenge/missions/srl/data/dict/1203_top50.pkl" ,"wb") as f:
    data = pk.dump(data_O[:50],f)

with open("./data/cm/nlp-challenge/missions/srl/data/dict/1203_top100.pkl" ,"wb") as f:
    data = pk.dump(data_O[:100],f)

with open("./data/cm/nlp-challenge/missions/srl/data/dict/1203_top500.pkl" ,"wb") as f:
    data = pk.dump(data_O[:500], f)

with open("./data/cm/nlp-challenge/missions/srl/data/dict/1203_top1000.pkl" ,"wb") as f:
    data = pk.dump(data_O[:1000], f)

with open("./data/cm/nlp-challenge/missions/srl/data/dict/1203_top2500.pkl" ,"wb") as f:
    data = pk.dump(data_O[:2500], f)

with open("./data/cm/nlp-challenge/missions/srl/data/dict/1203_top5000.pkl" ,"wb") as f:
    data = pk.dump(data_O[:5000], f)

with open("./data/cm/nlp-challenge/missions/srl/data/dict/1203_top10000.pkl" ,"wb") as f:
    data = pk.dump(data_O[:10000], f)



import pickle as pk
with open("./data/cm/nlp-challenge/missions/srl/data/dict/1203_top50.pkl" ,"rb") as f:
    data50 = pk.load(f)

with open("./data/cm/nlp-challenge/missions/srl/data/dict/1203_top100.pkl" ,"rb") as f:
    data100 = pk.load(f)

with open("./data/cm/nlp-challenge/missions/srl/data/dict/1203_top150.pkl" ,"rb") as f:
    data150 = pk.load(f)

with open("./data/cm/nlp-challenge/missions/srl/data/dict/1203_top500.pkl" ,"rb") as f:
    data500 = pk.load(f)

with open("./data/cm/nlp-challenge/missions/srl/data/dict/1203_top1000.pkl" ,"rb") as f:
    data1000 = pk.load(f)

with open("./data/cm/nlp-challenge/missions/srl/data/dict/1203_top2500.pkl" ,"rb") as f:
    data2500 = pk.load(f)

with open("./data/cm/nlp-challenge/missions/srl/data/dict/1203_top5000.pkl" ,"rb") as f:
    data5000 = pk.load(f)

with open("./data/cm/nlp-challenge/missions/srl/data/dict/1203_top10000.pkl" ,"rb") as f:
    data10000 = pk.load(f)




