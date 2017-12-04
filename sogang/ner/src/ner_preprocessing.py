from itertools import chain
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.preprocessing import LabelBinarizer

from random import shuffle

import ner_settings as st
import re

pos_linkmark_s = (u'[[', u'SW')
pos_linkmark_e = (u']]', u'SW')
def split_set_w_size(source_set,subset_size, max_num_of_subsets ) :
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
    assert sum(ratio_list) == 1
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

def rawtext2input(f) :
    all_sents = []
    one_sentence = []
    tmp = f.readlines()
    sentences = [s for s in tmp if len(s.strip())>1]
    #shuffle(sentences)#remove any inter-sentence sequentiality
    for s in sentences:
        pos_result = kkma.pos(s)
        for p in pos_result :
            temp = list(p)
            temp.append(u"O")
            one_sentence.append(tuple(temp))

        all_sents.append(one_sentence)
        one_sentence=[]

    return all_sents
'''trial code : try to compare eojeol in pos_result_link_removed and pos_result_link to find position of link mark in morphs
but.. kkm doesn't support eojeol preservation... :( - too many bugs...

def insert_link_marks(target, source, source_idxs) :
    copy_target = list(target)
    for s_idx in source_idxs :
        copy_target.insert(s_idx,source[s_idx])
    #for sidx in range(len(incl_marks)) :
    #    if incl_marks[sidx][0] == u'[[' or incl_marks[sidx][0] ==u']]' :
    #        copy_target.insert(sidx, incl_marks[sidx])
    return copy_target
def flatten_with_links(pos_result_link_removed, pos_result_link, idx_of_e_link_mark) :
    pos_result = []
    for eojeal_idx in range(len(pos_result_link_removed)) :
        if eojeal_idx in idx_of_e_link_mark :
            idx_of_p_link_mark_in_ej = [pidx for pidx in range(len(pos_result_link[eojeal_idx])) if'[[' == pos_result_link[eojeal_idx][pidx][0] or ']]' == pos_result_link[eojeal_idx][pidx][0]]
            if len(pos_result_link[eojeal_idx]) == len(pos_result_link_removed[eojeal_idx]) + len(idx_of_p_link_mark_in_ej) :
                eojeal_pos=insert_link_marks(pos_result_link_removed[eojeal_idx], pos_result_link[eojeal_idx],idx_of_p_link_mark_in_ej)
                print('!')
            else :
                eojeal_pos = pos_result_link[eojeal_idx]
                print('?')
        pos_result+=eojeal_pos
    return pos_result

def rawlinktext2input(f) :
    all_sents = []
    one_sentence = []
    tmp = f.readlines()
    sentences = [s for s in tmp if len(s.strip())>1 and '[[' in s]
    #shuffle(sentences)#remove any inter-sentence sequentiality
    for s in sentences:
        s_doublelinks_removed = re.sub(r'\[\[[^\]\]]*\|','[[',s)
        s_link_removed = re.sub(r'(\[\[|\]\])', '', s_doublelinks_removed)
        ejs_doublelinks_removed=s_doublelinks_removed.split()
        idx_of_link_mark = [ idx for idx in range(len(ejs_doublelinks_removed)) if '[[' in ejs_doublelinks_removed[idx] or ']]' in ejs_doublelinks_removed[idx]]
        #num_of_link_marks = s_doublelinks_removed.count('[[') * 2
        #s_mark_removed = re.sub(r'(\[\[[^\]\]]*\||\[\[|\]\])','',s)
        pos_result_link = kkma.pos(s_doublelinks_removed, flatten=False)
        pos_result_link_removed = kkma.pos(s_link_removed, flatten=False)
        #assert len(pos_result_link) == len(pos_result_link_removed)
        pos_result=flatten_with_links(pos_result_link_removed, pos_result_link, idx_of_link_mark)


        for p in pos_result :
            temp = list(p)
            temp.append(u"O")
            one_sentence.append(tuple(temp))

        all_sents.append(one_sentence)
        one_sentence=[]

    return all_sents
    '''
def insert_link_marks(target, incl_marks) :
    copy_target = list(target)
    for sidx in range(len(incl_marks)) :
        if incl_marks[sidx][0] == u'[[' or incl_marks[sidx][0] ==u']]' :
            copy_target.insert(sidx, incl_marks[sidx])
    return copy_target
def recover_link_marks(pos_result_link_replaced, new_mark) :
    copy_pos_replaced = list(pos_result_link_replaced)
    new_cnt = 0
    for pos_idx in range(len(copy_pos_replaced)) :
        if copy_pos_replaced[pos_idx][0] == new_mark:
            new_cnt += 1
            if new_cnt%2 == 1 :
                copy_pos_replaced[pos_idx] = pos_linkmark_s
            else :
                copy_pos_replaced[pos_idx] = pos_linkmark_e
    return copy_pos_replaced
def morph_compare_and_insert (pos_result_link, pos_result_link_removed, num_of_rd_link_marks, new_mark = None):
    #if num_of_link_marks is -1 :
    #    num_of_link_marks = len(re.findall(link_regex, s_link))
    if len(pos_result_link) == len(pos_result_link_removed) + num_of_rd_link_marks:
        if new_mark is None :
            pos_result = insert_link_marks(pos_result_link_removed, pos_result_link)
        else :
            pos_result = recover_link_marks(pos_result_link_removed, new_mark)
        return pos_result
    else :
        return False
def seperate_link_from_pos(pos_result) :
    copy_pos_result = list(pos_result)
    pidx = 0
    link_flag = -1
    list_idx = []
    link_bio = []
    while True :
        if len(copy_pos_result) <= pidx : break
        if copy_pos_result[pidx][0] == '[[' :
            link_flag = 0
            del copy_pos_result[pidx]
            continue
        if copy_pos_result[pidx][0] == ']]':
            link_flag = -1
            del copy_pos_result[pidx]
            continue
        if link_flag == 0 :
            list_idx.append(pidx)
            link_bio.append(u'B-LNK')
            link_flag += 1
        elif link_flag > 0 :
            list_idx.append(pidx)
            link_bio.append(u'I-LNK')
            link_flag += 1
        else :
            link_bio.append(u'O')
        pidx += 1
    return copy_pos_result, list_idx, link_bio
def rawlinktext2input(f,link_ft = False) :
    all_results = []
    all_candidate_idxs = []
    all_sents = []
    one_sentence = []
    tmp = f.readlines()
    #sentences = [s for s in tmp if len(s.strip())>1 and '[[' in s]
    sentences = [s for s in tmp if len(s.strip()) > 1]
    sentences = sentences [:10000]
    #shuffle(sentences)#remove any inter-sentence sequentiality
    can_find1 = 0
    cant_find1 = 0
    cant_find2 = 0
    for sidx in range(len(sentences)):
        if sidx%1000 == 0 :
            print('...'+str(sidx)+'...')
            #write
        s=sentences[sidx]
        s_doublelinks_removed = re.sub(r'\[\[[^\]\]]*\|','[[',s)
        s_doublelinks_removed = re.sub(r'\[\[[^\]\]]*\:[^\[\[]*\]\]', '', s_doublelinks_removed)
        s_link_removed = re.sub(r'(\[\[|\]\])', '', s_doublelinks_removed)
        if len(s_link_removed.strip()) < 2 :
            continue
        pos_result_link = kkma.pos(s_doublelinks_removed)
        try :
            pos_result_link_removed = kkma.pos(s_link_removed)
        except :
            print('err : '+ s)
            continue
        num_of_link_marks = len(re.findall(r'\[\[|\]\]', s_doublelinks_removed))
        pos_result = morph_compare_and_insert(pos_result_link, pos_result_link_removed, num_of_link_marks)
        if pos_result is False :
            cant_find1 += 1
            #if '"' not in s_link_removed :
            #    s_link_replaced = s_doublelinks_removed.replace('[[', '"').replace(']]', '"')
            #    pos_result_link_replaced = kkma.pos(s_link_replaced)
            #    pos_result = morph_compare_and_insert(pos_result_link, pos_result_link_replaced,0, new_mark = '"')
            #elif "'" not in s_link_removed :
            #    s_link_replaced = s_doublelinks_removed.replace('[[', "'").replace(']]', "'")
            #    pos_result_link_replaced = kkma.pos(s_link_replaced)
            #    pos_result = morph_compare_and_insert(pos_result_link, pos_result_link_replaced, 0, new_mark="'")
            if pos_result is False :
                cant_find2 += 1
                pos_result = pos_result_link
        else :
            can_find1 += 1
        #pos_result = pos_result_link #override
        pos_result, candidate_idxs, link_bio = seperate_link_from_pos(pos_result)
        all_results.append(pos_result)
        all_candidate_idxs.append(candidate_idxs)
        cand_idx = 0
        for pidx in range(len(pos_result)) :
            p = pos_result[pidx]
            temp = list(p)
            temp.append(u"O")
            if link_ft is True :
                temp.append(link_bio[pidx])
            one_sentence.append(tuple(temp))
        all_sents.append(one_sentence)
        one_sentence=[]

    return all_sents, all_candidate_idxs

def read_labeled_file (f,n = None,link=False, flatten = True) : # file read. data to tuple
    original_sents = []
    ne_marked_sents = []
    all_sents = []
    sent_list = []
    for s in f.readlines():
        #split_s = s.split()
        split_s = s.split(' ')
        if len(split_s) > 0 and split_s[0].startswith(';') and (len(split_s)<4 or len(split_s) > 5 or (len(split_s)>= 4 and split_s[3].strip() not in st.TAG)):
            original_sents.append(s[1:].strip())
            continue
        if len(split_s) > 0 and split_s[0].startswith('$') and (len(split_s)<4 or len(split_s) > 5 or (len(split_s)>= 4 and split_s[3].strip() not in st.TAG)):
            ne_marked_sents.append(s[1:].strip())
            continue
        if len(split_s) < 3 and s.strip()=='':
            all_sents.append(sent_list)
            if len(original_sents) == len(all_sents) -1 :
                original_sents.append('')
            if len(ne_marked_sents) == len(all_sents) -1 :
                ne_marked_sents.append('')
            sent_list = []
            if n is not None:
                if len(all_sents) >= n:
                    break
            continue
        if link is True :
            sent_list.append((split_s[0], split_s[1], str(split_s[3]).replace("\n", "").replace("\r", ""),u'O')) #LAST is LINK BIO
        else :
            if flatten == True :
                sent_list.append((split_s[0], split_s[1], str(split_s[3]).replace("\n", "").replace("\r", "")))
            if flatten == False :
                try :
                    sent_list.append((split_s[0], split_s[1],split_s[2], str(split_s[3]).replace("\n", "").replace("\r", "")))
                except :
                    print(s)
    return original_sents, ne_marked_sents, all_sents

def word2features(sent, i, link_ft = False): #feature engineering part
    word = sent[i][0]
    postag = sent[i][1]

    '''if link_ft is True:
        linktag = sent[i][3]
        features = [
            'bias',
            'word='+ word,
            'link='+ linktag,
            'word.isdigit=%s' % word.isdigit(),
            'postag=' + postag,
            'postag[:2]=' + postag[:2],
        ]
        if i > 0:
            word1 = sent[i - 1][0]
            postag1 = sent[i - 1][1]
            linktag1 = sent[i - 1][3]
            features.extend([
                '-1:word=' + word1,
                '-1:link=' +linktag1,
                '-1:postag=' + postag1,
                '-1:postag[:2]=' + postag1[:2],
            ])
        else:
            features.append('BOS')

        if i < len(sent) - 1:
            word1 = sent[i + 1][0]
            postag1 = sent[i + 1][1]
            linktag1 = sent[i + 1][3]
            features.extend([
                '+1:word=' + word1,
                '+1:link=' + linktag1,
                '+1:postag=' + postag1,
                '+1:postag[:2]=' + postag1[:2],
            ])
        else:
            features.append('EOS')

    else :'''

    if st.DICTIONARY is True :
        features = [
            'bias',
            'word=' + word,
            'word.isdigit=%s' % word.isdigit(),
            'postag=' + postag,
            'postag[:2]=' + postag[:2],
            'len_word=' + unicode(len(word)), #JUAE
            'dic[B-DT]=0',  # dictionay features are initialized by 0
            'dic[B-LC]=0',
            'dic[B-OG]=0',
            'dic[B-PS]=0',
            'dic[B-TI]=0',
            'dic[I-DT]=0',
            'dic[I-LC]=0',
            'dic[I-OG]=0',
            'dic[I-PS]=0',
            'dic[I-TI]=0'
        ]
    else :
        features = [
            'bias',
            'word=' + word,
            'word.isdigit=%s' % word.isdigit(),
            'postag=' + postag,
            'postag[:2]=' + postag[:2],
            'len_word=' + unicode(len(word))  # JUAE
        ]
    if i > 0:
        word1 = sent[i - 1][0]
        postag1 = sent[i - 1][1]
        features.extend([
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
            '+1:word=' + word1,
            '+1:postag=' + postag1,
            '+1:postag[:2]=' + postag1[:2],
        ])
    else:
        features.append('EOS')


        ###########juae

    if i < len(sent) - 2:
        word1 = sent[i + 2][0]
        postag1 = sent[i + 2][1]
        features.extend([
            '+2:word=' + word1,
            '+2:postag=' + postag1,
            '+2:postag[:2]=' + postag1[:2],
        ])

    if i > 1:
        word1 = sent[i - 2][0]
        postag1 = sent[i - 2][1]
        features.extend([
            '-2:word=' + word1,
            '-2:postag=' + postag1,
            '-2:postag[:2]=' + postag1[:2],
        ])

    return features

def word2features_flatten(sent, i): #feature engineering part
    word = sent[i][0]
    postag = sent[i][1]
    position = sent[i][2]

    #n = '0'
    #if postag[:2] == 'NN' :
    #    n = '1'
    if st.DICTIONARY is True :
        features = [
            'bias',
            'word=' + word,
            'word.isdigit=%s' % word.isdigit(),
            'postag=' + postag,
            'postag[:2]=' + postag[:2],
            'len_word=' + unicode(len(word)),  # JUAE
            'dic[B-DT]=0',  # dictionay features are initialized by 0
            'dic[B-LC]=0',
            'dic[B-OG]=0',
            'dic[B-PS]=0',
            'dic[B-TI]=0',
            'dic[I-DT]=0',
            'dic[I-LC]=0',
            'dic[I-OG]=0',
            'dic[I-PS]=0',
            'dic[I-TI]=0',
            'position=' + position
        ]
    else :
        features = [
            'bias',
            'word=' + word,
            'word.isdigit=%s' % word.isdigit(),
            'postag=' + postag,
            'postag[:2]=' + postag[:2],
            #'n=' + n,
            'position=' + position,
            'len_word=' + unicode(len(word)) #JUAE
        ]
    if i > 0:
        word1 = sent[i - 1][0]
        postag1 = sent[i - 1][1]
        #n1 = '1' if postag1[:2] == 'NN' else '0'
        features.extend([
            '-1:word=' + word1,
            #'-1:n=' + n1
            '-1:postag=' + postag1,
            '-1:postag[:2]=' + postag1[:2],
        ])
    else:
        features.append('BOS')

    if i < len(sent) - 1:
        word1 = sent[i + 1][0]
        postag1 = sent[i + 1][1]
        #n1 = '1' if postag1[:2] == 'NN' else '0'
        features.extend([
            '+1:word=' + word1,
            #'+1:n=' + n1
            '+1:postag=' + postag1,
            '+1:postag[:2]=' + postag1[:2],
        ])
    else:
        features.append('EOS')


            ###########juae

    if i < len(sent) - 2:
        word1 = sent[i + 2][0]
        postag1 = sent[i + 2][1]
        #n1 = '1' if postag1[:2] == 'NN' else '0'
        features.extend([
            '+2:word=' + word1,
            #'+2:n=' + n1
            '+2:postag=' + postag1,
            '+2:postag[:2]=' + postag1[:2],
        ])

    if i > 1:
        word1 = sent[i - 2][0]
        postag1 = sent[i - 2][1]
        #n1 = '1' if postag1[:2] == 'NN' else '0'
        features.extend([
            '-2:word=' + word1,
            #'-2:n=' + n1
            '-2:postag=' + postag1,
            '-2:postag[:2]=' + postag1[:2],
        ])

    return features
def ej_numbering(sent) :
    new_sent  = []
    ej_idx = 0
    bf_ejnum = -1
    this_ejnum = 0
    for tup in sent :
        this_ejnum = tup[2]
        if bf_ejnum != this_ejnum :
            ej_idx = 0
        new_sent.append((tup[0],tup[1], str(ej_idx), tup[3]))
        ej_idx += 1
        bf_ejnum = this_ejnum
    return new_sent
def sent2features(sent,link_ft=False, flatten = True):
    if flatten is True :
        return [word2features(sent, i, link_ft) for i in range(len(sent))]
    else :
        sent = ej_numbering(sent)
        return [word2features_flatten(sent, i) for i in range(len(sent))]


def sent2labels(sent, link_ft = False, flatten = True):
    if link_ft is True :
        return [label for token, postag, label, link in sent]
    elif flatten is True :
        return [label for token, postag, label in sent]
    elif flatten is False :
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
        print tagger.probability(y_pred)
        for t, y in enumerate(y_pred):
            # Output the predicted labels with their marginal probabilities.
            print '%s:%f' % (y, tagger.marginal(y, t))
        print


def bio_classification_report(y_true, y_pred): #funtion for evaluating the marginal probability
    """
    Classification report for a list of BIO-encoded sequences.
    It computes token-level metrics and discards "O" labels.

    Note that it requires scikit-learn 0.15+ (or a version from github master)
    to calculate averages properly!
    """
    lb = LabelBinarizer()
    y_true_combined = lb.fit_transform(list(chain.from_iterable(y_true)))
    y_pred_combined = lb.transform(list(chain.from_iterable(y_pred)))

    tagset = set(lb.classes_) - {'O'}
    tagset = sorted(tagset, key=lambda tag: tag.split('-', 1)[::-1])
    class_indices = {cls: idx for idx, cls in enumerate(lb.classes_)}

    return classification_report(
        y_true_combined,
        y_pred_combined,
        labels=[class_indices[cls] for cls in tagset],
        target_names=tagset,
    )

