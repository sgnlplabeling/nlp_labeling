#-*- coding:utf-8 -*-
import codecs
import pickle as pickle
import causality_settings as st
import sys

def read_labeled_file (f,n = None) : # file read. data to tuple
    original_sents = []
    all_sents = []
    sent_list = []
    count = 0
    for s in f.readlines():
        split_s = s.split(' ')
        if len(split_s) > 0 and split_s[0].startswith(';') and (len(split_s)<4 or len(split_s) > 5 or (len(split_s)>= 4 and split_s[3].strip() not in st.TAG)):
            original_sents.append(s[1:].strip())
            continue

        if len(split_s) < 3:
            all_sents.append(sent_list)
            sent_list = []
            if n is not None:
                if len(all_sents) >= n:
                    break
            continue
        try :
            sent_list.append((split_s[0], split_s[1],split_s[2], str(split_s[3]).replace("\n", "").replace("\r", "")))
        except :
            print()
        
    return original_sents, all_sents
def word2features(sent, i): #feature engineering part
    word = sent[i][0]
    postag = sent[i][1]
    position = sent[i][2]

    features = [
        'bias',
        'word=' + word,
        'word.lower =' + word.lower(),
        'word[-3:]=' + word[-3:],
        'word[-2:]=' + word[-2:],
        'word.isupper = %s' % word.isupper(),
        'word.istitle = %s' % word.istitle(),
        'word.isdigit=%s' % word.isdigit(),
        'postag=' + postag,
        'postag[:2]=' + postag[:2],
        #'n=' + n,
        'position=' + position,
        'len_word=' + str(len(word)) #JUAE
    ]
    if i > 0:
        word1 = sent[i - 1][0]
        postag1 = sent[i - 1][1]
        #n1 = '1' if postag1[:2] == 'NN' else '0'
        features.extend([
            '-1:word.lower=' + word1.lower(),
            '-1:word.istitle=%s' % word1.istitle(),
            '-1:word.isupper=%s' % word1.isupper(),
            '-1:word=' + word1,
            '-1:postag=' + postag1,
            '-1:postag[:2]=' + postag1[:2],
        ])
    else:
        features.append('BOS')

    if i < len(sent) - 1:
        word1 = sent[i + 1][0]
        postag1 = sent[i + 1][1]
        features.extend([
            '+1:word.lower=' +word1.lower(),
            '+1:word.istitle=%s' % word1.istitle(),
            '+1:word.isupper=%s' % word1.isupper(),
            '+1:word=' + word1,
            '+1:postag=' + postag1,
            '+1:postag[:2]=' + postag1[:2],
        ])
    else:
        features.append('EOS')

    if i < len(sent) - 2:
        word1 = sent[i + 2][0]
        postag1 = sent[i + 2][1]
        features.extend([
            '+2:word=' + word1,
            '+2:postag=' + postag1,
            '+2:postag[:2]=' + postag1[:2],
        ])
    # if i < len(sent) - 3:
    #     word1 = sent[i+3][0]
    #     postag1 = sent[i+3][1]
    #     features.extend([
    #         '+3:word=' +word1,
    #         '+3:postag='+postag1,
    #         '+3:postag[:2]='+postag1[:2],
    #         ])
    # if i < len(sent) - 4:
    #     word1 = sent[i+4][0]
    #     postag1 = sent[i+4][1]
    #     features.extend([
    #         '+4:word=' +word1,
    #         '+4:postag='+postag1,
    #         '+4:postag[:2]='+postag1[:2],
    #         ])
    # if i < len(sent) - 5:
    #     word1 = sent[i+3][0]
    #     postag1 = sent[i+3][1]
    #     features.extend([
    #         '+5:word=' +word1,
    #         '+5:postag='+postag1,
    #         '+5:postag[:2]='+postag1[:2],
    #         ])
    # if i < len(sent) - 6:
    #     word1 = sent[i+3][0]
    #     postag1 = sent[i+3][1]
    #     features.extend([
    #         '+6:word=' +word1,
    #         '+6:postag='+postag1,
    #         '+6:postag[:2]='+postag1[:2],
    #         ])

    if i > 1:
        word1 = sent[i - 2][0]
        postag1 = sent[i - 2][1]
        features.extend([
            '-2:word=' + word1,
            '-2:postag=' + postag1,
            '-2:postag[:2]=' + postag1[:2],
        ])

    return features
def sent2features(sent):
    return [word2features(sent, i) for i in range(len(sent))]
def sent2labels(sent):
    return [label for token, postag, position, label in sent]
def sent2tokens(sent):
    return [token for token, postag, label, link in sent]
def marginal_prob (X_test, tagger) :
    for xseq in X_test:
        # Tag the sequence.
        tagger.set(xseq)
        # Obtain the label sequence predicted by the tagger.
        y_pred = tagger.tag(xseq)
        # Output the probability of the predicted label sequence.
        print (tagger.probability(y_pred))
        for t, y in enumerate(y_pred):
            # Output the predicted labels with their marginal probabilities.
            print ('%s:%f' % (y, tagger.marginal(y, t)))
        print
def split_set_w_size(source_set,subset_size, max_num_of_subsets ) : #subset_size = 2500, max_num_of_subsets = 10
    s = 0
    e = subset_size
    sub_sets = []
    while s < len(source_set) :
        if max_num_of_subsets*subset_size < e :
            break
        sub_sets.append(source_set[s:e])
        s = e
        e += subset_size
    return sub_sets
def split_set(source_set,ratio_list) :
    try : assert sum(ratio_list) == 1
    except : print(str(sum(ratio_list)) + '!!!')
    num_of_total_e = len(source_set)
    num_of_e_list = [int(r*num_of_total_e) for r in ratio_list]
    if num_of_total_e > sum(num_of_e_list) :
        num_of_e_list[0] += num_of_total_e - sum(num_of_e_list)
    splited_sets = []
    start = 0
    end = 0
    for num_e in num_of_e_list :
        end += num_e
        splited_sets.append(source_set[start:end])
        start = end
    return splited_sets
def write_result(test_sents, y_pred,file_full_name) :
    with open(file_full_name, 'w') as wf:
        for s_idx in range(len(test_sents)):
            for tup_idx in range(len(test_sents[s_idx])):
                mark = ''
                if test_sents[s_idx][tup_idx][3] != y_pred[s_idx][tup_idx] :
                    mark = '$$'
                out_str = mark + test_sents[s_idx][tup_idx][0] + ' ' + test_sents[s_idx][tup_idx][1] + test_sents[s_idx][tup_idx][2] + ' ' + y_pred[s_idx][tup_idx] + '('+test_sents[s_idx][tup_idx][3]+')'+'\n'
                wf.write(out_str.encode('utf-8'))
            wf.write('\n'.encode('utf-8'))
def write_result_from_ft(X, y_pred,file_full_name) :
    wf = codecs.open(file_full_name, 'w',encoding= st.ENCODING)
    for s_idx in range(len(X)):
        if len(y_pred[s_idx]) == 0:
            continue
        for word_idx in range(len(X[s_idx])):
            word_fts = X[s_idx][word_idx]
            out_str = get_ft_value(word_fts, 'word') + ' ' + get_ft_value(word_fts, 'postag') + ' ' + get_ft_value(
                word_fts, 'position') + ' ' + y_pred[s_idx][word_idx] + '\n'
            wf.write(out_str)
        wf.write('\n')
def modify_feature(word_features, ft_name, new_value_str) :
    word_features[st.ft_idx[ft_name]] = ft_name+'='+new_value_str
def get_ft_value(word_fts, feature_name) :
    return word_fts[st.ft_idx[feature_name]].replace(feature_name+'=','')
def generate_all(seq_of_seq, val) :
    all_val_seq_of_seq = [[val for e in seq] for seq in seq_of_seq ]
    return all_val_seq_of_seq

def _remove_all_o(yseq,r_idxs, y_prob) :
    num_BorI = len([y for y in yseq if y != 'O'])
    if num_BorI == 0:
        return [[], [], []]
    else:
        return yseq, r_idxs, y_prob

def post_process_y(yseq, y_prob, remove_all_o, min_conf, seq_prob = None) :
    if seq_prob is None :
        seq_prob = min(y_prob)
    if seq_prob< min_conf :
        return [[], [], []]
    yseq, r_idxs = _remove_I_without_B(yseq)
    if remove_all_o is False :
        return yseq, r_idxs, y_prob
    return _remove_all_o(yseq,r_idxs,y_prob)

def _remove_I_without_B(yseq):
    remomved_idxs = []
    for y_idx in range(len(yseq)):
        if yseq[y_idx][0] is 'I':
            if y_idx is 0:
                yseq[y_idx] = 'O'
                remomved_idxs.append(y_idx)
            elif yseq[y_idx - 1] != 'B' + yseq[y_idx][1:] and yseq[y_idx - 1] != yseq[y_idx]:
                yseq[y_idx] = 'O'
                remomved_idxs.append(y_idx)
    return [yseq, remomved_idxs]
def read_labeled_text_data(file_path, encoding, save = False, save_path = None) :
    f = codecs.open(file_path, 'r', encoding=encoding)
    original_sents, sents = read_labeled_file(f)
    #for s in sents:
    X = [sent2features(s) for s in sents]
    # print X[0]
    y = [sent2labels(s) for s in sents]
    f.close()

    if save is True :
        save_points = [10000,50000,200000,1000000]
        for sp in save_points :
            st.write_log('writing : ' + str(sp)+'.pkl', open=True, close=True, std_print=False)
            with open(save_path + str(sp) + '.pkl', 'wb') as output :
                pickle.dump(sents[:sp], output, pickle.HIGHEST_PROTOCOL)
                pickle.dump(X[:sp], output, pickle.HIGHEST_PROTOCOL)
                pickle.dump(y[:sp], output, pickle.HIGHEST_PROTOCOL)
    return original_sents, sents, X, y

def read_labeled_pickle_data(file_path) :
    with open(file_path, 'rb') as input:
        readed_obj = pickle.load(input)
        unlabeled_sents = []
        for s in readed_obj :
            if len(s) != 0 :
                link_flag = False
                for mor in s :
                    if mor[0] == '[[' or mor[0] == ']]' :
                        link_flag = True
                if link_flag is False :
                    unlabeled_sents.append(s)
        X_unlabeled = [sent2features(s) for s in unlabeled_sents]
        y_unlabeled = [sent2labels(s) for s in unlabeled_sents]
        return unlabeled_sents, X_unlabeled, y_unlabeled, None

