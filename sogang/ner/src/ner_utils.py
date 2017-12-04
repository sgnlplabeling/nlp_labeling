import codecs
import ner_preprocessing as pre
import cPickle as pickle
import ner_settings as st
import math
import os, os.path
##added for dictionary##
#ft_idx = {'word':1,'word.isdigit':2,'postag':3,'postag[:2]':4,'len_word':5,'dic[B-DT]':6,'dic[B-LC]':7,'dic[B-OG]':8,
#          'dic[B-PS]':9,'dic[B-TI]':10,'dic[I-DT]':11,'dic[I-LC]':12,'dic[I-OG]':13,'dic[I-PS]':14,'dic[I-TI]':15 ,'position':16}
ft_idx = {'word':1,'word.isdigit':2,'postag':3,'postag[:2]':4,'position':5, 'len_word':6}

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

def change_ej_yj2donga(ej_yj) :
    ej_donga = []
    donga_i = 0
    for e in ej_yj :
        if e == 0 :
            donga_i += 1
        ej_donga.append(donga_i)
    return ej_donga
def write_result_from_ft(orisents, nesents, X, y_pred,file_full_name, yprob = None) :
    if yprob != None :
        sent_prob = [min(prob_list) if len(prob_list)>0 else 0.0 for prob_list in yprob ]

    wf = codecs.open(file_full_name, 'w',encoding= st.ENCODING)
    if len(orisents) != len(X) or len(nesents) != len(X) :
        print('error!!!') #blocked for tmp hy
    for s_idx in range(len(X)):
        if s_idx % 100000 == 0 :
            print ('...'+str(s_idx)+'/'+str(len(X))+'...')
        if len(y_pred[s_idx]) == 0:
            continue
        if yprob != None :
            wf.write(';'+orisents[s_idx]+'\t'+str(sent_prob[s_idx])+'\n') #blocked for tmp hy
        else :
            wf.write(';' + orisents[s_idx] +'\n')
        #wf.write('$' + nesents[s_idx] + '\n')
        ej_number_yj = [int(get_ft_value(w, 'position')) for w in X[s_idx]]
        ej_number_donga = change_ej_yj2donga(ej_number_yj)
        for word_idx in range(len(X[s_idx])):
            word_fts = X[s_idx][word_idx]
            if yprob == None:
                out_str = get_ft_value(word_fts, 'word') + ' ' + get_ft_value(word_fts, 'postag') + ' ' + str(ej_number_donga[word_idx])+ ' ' + y_pred[s_idx][word_idx] + '\n'
            else :
                out_str = get_ft_value(word_fts, 'word') + ' ' + get_ft_value(word_fts, 'postag') + ' ' + str(ej_number_donga[word_idx]) + ' ' + y_pred[s_idx][word_idx] + ' '+str(yprob[s_idx][word_idx])+'\n'
            wf.write(out_str)
        wf.write('\n')
    #with open(file_full_name, 'w') as wf:
        '''for s_idx in range(len(X)):
            if len(y_pred[s_idx]) == 0 :
                continue
            for word_idx in range(len(X[s_idx])):
                word_fts = X[s_idx][word_idx]
                out_str = get_ft_value(word_fts,'word') + ' ' + get_ft_value(word_fts,'postag') + ' ' + get_ft_value(word_fts,'position') + ' ' + y_pred[s_idx][word_idx] + '\n'
                wf.write(out_str.encode('utf-8'))
            wf.write('\n'.encode('utf-8'))'''

def modify_feature(word_features, ft_name, new_value_str) :
    word_features[ft_idx[ft_name]] = ft_name+'='+new_value_str
def get_ft_value(word_fts, feature_name) :
    return word_fts[ft_idx[feature_name]].replace(feature_name+'=','')

def generate_all(seq_of_seq, val) :
    all_val_seq_of_seq = [[val for e in seq] for seq in seq_of_seq ]
    return all_val_seq_of_seq
########################
def _remove_not_candidates(yseq, y_prob, candidate):
    copy_yseq = list(yseq)
    copy_yprob = list(y_prob)
    for i in range(len(copy_yseq)):
        if i not in candidate:
            if copy_yprob[i]<st.LINK_MIN_PROB_OF_REPLACE :
                copy_yseq[i] = 'O'
                copy_yprob[i] = st.LINK_REPLACE_PROB_TO
    return copy_yseq, copy_yprob
def _remove_all_o(yseq,r_idxs, y_prob) :
    num_BorI = len([y for y in yseq if y != 'O'])
    if num_BorI == 0:
        return [[], [], []]
    else:
        return yseq, r_idxs, y_prob
def _mul_sqrt_ne_cnt(yseq, y_prob) :
    ne_cnt = len([bio for bio in yseq if bio.startswith('B')])
    sqrt_ne_cnt = min(math.sqrt(ne_cnt),st.ROOT)

    for idx, bio in enumerate(yseq) :
        if bio != 'O' :
            y_prob[idx] = min(y_prob[idx]*sqrt_ne_cnt, 1.0)
    return  yseq, y_prob
def post_process_y(yseq, y_prob, remove_all_o, min_conf, link_pos, seq_prob = None, replace_o = False, mul_ne_cnt = False) :
    if mul_ne_cnt == True :
        yseq , y_prob = _mul_sqrt_ne_cnt(yseq, y_prob)
    if replace_o == False :
        if seq_prob is None :
            seq_prob = min(y_prob)
        if seq_prob< min_conf :
            return [[], [], []]
    else:
        replaced_yseq = []
        replaced_y_prob = []
        for y, p in zip(yseq, y_prob) :
            if p < min_conf and y!= 'O' :
                replaced_yseq.append('O') #fixed!!!
                replaced_y_prob.append(min_conf)
            else:
                replaced_yseq.append(y)
                replaced_y_prob.append(p)
        yseq = replaced_yseq
        y_prob = replaced_y_prob
    if link_pos != None :
        yseq, y_prob = _remove_not_candidates(yseq, y_prob, link_pos)
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
def read_labeled_text_data_dir(dir_path, encoding,flatten=False) :
    orisent = []
    nesent = []
    sent  = []
    X = []
    y = []
    file_names = os.listdir(dir_path)
    for fn in file_names :
        orisent_f, nesent_f, sent_f, x_f, y_f = read_labeled_text_data(dir_path+fn,encoding, flatten=flatten)
        orisent += orisent_f
        nesent += nesent_f
        sent += sent_f
        X += x_f
        y += y_f
    return orisent,nesent, sent, X, y
def read_labeled_text_data(file_path, encoding, save = False, save_path = None, flatten = False, make_ft = True) :
    f = codecs.open(file_path, 'r', encoding=encoding)
    orisents, nesents, sents = pre.read_labeled_file(f, flatten=flatten)
    X = []
    if make_ft == True :
        X = [pre.sent2features(s, flatten=flatten) for s in sents]
    y = [pre.sent2labels(s, flatten=flatten) for s in sents]

    f.close()

    if save is True :
        save_points = [10000,50000,200000,1000000]
        for sp in save_points :
            st.write_log('writing : ' + str(sp)+'.pkl', open=True, close=True, std_print=False)
            with open(save_path + str(sp) + '.pkl', 'wb') as output :
                pickle.dump(sents[:sp], output, pickle.HIGHEST_PROTOCOL)
                pickle.dump(X[:sp], output, pickle.HIGHEST_PROTOCOL)
                pickle.dump(y[:sp], output, pickle.HIGHEST_PROTOCOL)
    return orisents, nesents, sents, X, y
def read_labeled_pickle_data(file_path, num_of_obj=1, flatten = True) :
    with open(file_path, 'rb') as input:
        readed_obj = []
        for i in range(num_of_obj) :
            readed_obj.append( pickle.load(input))
        if num_of_obj == 1:
            unlabeled_sents = []
            for s in readed_obj[0] :
                if len(s) != 0 :
                    link_flag = False
                    for mor in s :
                        if mor[0] == '[[' or mor[0] == ']]' :
                            link_flag = True
                    if link_flag is False :
                        unlabeled_sents.append(s)
            #unlabeled_sents = [s for s in readed_obj[0] if len(s)!=0 ]
            X_unlabeled = [pre.sent2features(s, flatten=flatten) for s in unlabeled_sents]
            y_unlabeled = [pre.sent2labels(s, flatten=flatten) for s in unlabeled_sents]
            return unlabeled_sents, X_unlabeled, y_unlabeled, None
        if num_of_obj == 2 :
            unlabeled_sents = []
            unlabeled_links = []
            X_unlabeled = []
            y_unlabeled = []
            for idx in range(len(readed_obj[0])) :
                if len(readed_obj[1][idx]) == 0 or len(readed_obj[0][idx]) == 0:
                    continue
                s=readed_obj[0][idx]
                unlabeled_sents.append(s)
                unlabeled_links.append(readed_obj[1][idx])
                X_unlabeled.append(pre.sent2features(s))
                y_unlabeled.append(pre.sent2labels(s))
            return unlabeled_sents, X_unlabeled, y_unlabeled, unlabeled_links
    #readed_obj.append(X_unlabeled)
        #readed_obj.append(y_unlabeled)
