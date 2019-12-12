def separate(active_dict, unlabeled_orisents, unlabeled_nesents, unlabeled_sents, X_unlabeled, y_pred, y_mar_prob):
    y_pred_including_act = []
    y_prob_including_act = []
    unlabeled_orisents_act = []
    unlabeled_nesents_act = []
    X_unlabeled_act = []
    y_pred_act = []
    y_prob_act = []
    unlabeled_orisents_ml = []
    unlabeled_nesents_ml = []
    X_unlabeled_ml = []
    y_pred_ml = []
    y_prob_ml = []
    dict_cnt = 0
    for s_idx in range(len(unlabeled_sents)):
        sent_key = gen_key_from_sent(unlabeled_sents[s_idx])
        if sent_key in active_dict :
            ypred_sent = active_dict[sent_key]
            yprob_sent = [1.0 for y in ypred_sent]
            unlabeled_orisents_act.append(unlabeled_orisents[s_idx])
            unlabeled_nesents_act.append(unlabeled_nesents[s_idx])
            X_unlabeled_act.append(X_unlabeled[s_idx])
            y_pred_act.append(ypred_sent)
            y_prob_act.append(yprob_sent)
            dict_cnt += 1
        else :
            ypred_sent = y_pred[s_idx]
            yprob_sent = y_mar_prob[s_idx]
            unlabeled_orisents_ml.append(unlabeled_orisents[s_idx])
            unlabeled_nesents_ml.append(unlabeled_nesents[s_idx])
            X_unlabeled_ml.append(X_unlabeled[s_idx])
            y_pred_ml.append(ypred_sent)
            y_prob_ml.append(yprob_sent)

        y_pred_including_act.append(ypred_sent)
        y_prob_including_act.append(yprob_sent)
    return y_pred_including_act, y_prob_including_act, unlabeled_orisents_act, unlabeled_nesents_act, X_unlabeled_act, y_pred_act, y_prob_act, unlabeled_orisents_ml, \
    unlabeled_nesents_ml, X_unlabeled_ml, y_pred_ml, y_prob_ml
def separate_hy(active_dict, unlabeled_sents, X_unlabeled, y_pred):
    unlabeled_sents_act = []
    X_unlabeled_act = []
    y_pred_act = []

    unlabeled_sents_ml = []
    X_unlabeled_ml = []
    y_pred_ml = []
    for s_idx in range(len(unlabeled_sents)):
        sent_key = gen_key_from_sent(unlabeled_sents[s_idx])
        if sent_key in active_dict :
            X_unlabeled_act.append(X_unlabeled[s_idx])
            y_pred_act.append(y_pred[s_idx])
            unlabeled_sents_act.append(unlabeled_sents[s_idx])
        else :
            X_unlabeled_ml.append(X_unlabeled[s_idx])
            y_pred_ml.append(y_pred[s_idx])
            unlabeled_sents_ml.append(unlabeled_sents[s_idx])
    return unlabeled_sents_act, X_unlabeled_act, y_pred_act,unlabeled_sents_ml, X_unlabeled_ml, y_pred_ml

def make_prediction(X_test, full_model_name):  # not used when this is component classifier
    tagger.open(full_model_name)
    y_preds = []
    for xseq in X_test:
        y_pred_ori = tagger.tag(xseq)
        y_pred_post, _ = utils._remove_I_without_B(y_pred_ori)
        y_preds.append(y_pred_post)
    tagger.close()
    return y_preds
def write_result_unlabeled(test_sents, y_pred,file_full_name, active_dict) :
    wf = codecs.open(file_full_name,'a', encoding='utf-8')
    dict_cnt = 0

    for s_idx in range(len(test_sents)):
        sent_key = gen_key_from_sent(test_sents[s_idx])
        if sent_key in active_dict :
            ypred_sent = active_dict[sent_key]
            dict_cnt += 1
        else :
            ypred_sent = y_pred[s_idx]
        #if len(utils._remove_all_o(ypred_sent,[],[])[0]) == 0 :
        #    continue
        for tup_idx in range(len(test_sents[s_idx])):
            out_str = test_sents[s_idx][tup_idx][0] + ' ' + test_sents[s_idx][tup_idx][1] + ' '+test_sents[s_idx][tup_idx][2] +' '+ ypred_sent[tup_idx] + '\n'
            try :
                wf.write(out_str)
            except :
                print(out_str)
        wf.write('\n'.encode('utf-8'))
    print (str(dict_cnt)+'/'+str(len(test_sents)) + 'sents are tagged manually.')
    wf.close()
'''def write_result(test_sents, y_pred,file_full_name) :
    with open(file_full_name, 'w') as wf:
        for s_idx in range(len(test_sents)):
            for tup_idx in range(len(test_sents[s_idx])):
                mark = ''
                if test_sents[s_idx][tup_idx][3] != y_pred[s_idx][tup_idx] :
                    mark = '$$'
                out_str = mark + test_sents[s_idx][tup_idx][0] + ' ' + test_sents[s_idx][tup_idx][1] + ' '+test_sents[s_idx][tup_idx][2] + ' ' \
                          + y_pred[s_idx][tup_idx] +'('+test_sents[s_idx][tup_idx][3]+')'+ '\n'
                wf.write(out_str.encode('utf-8'))
            wf.write('\n'.encode('utf-8'))'''
def gen_key_from_sent(sent) :
    key = []
    for tup_word in sent :
        key.append(tup_word[0])
    return tuple(key)
def gen_active_dict(active_sents, y_active) :
    active_dict = dict()
    for tup_sent, label_sent in zip(active_sents, y_active) :
        active_dict[gen_key_from_sent(tup_sent)] = label_sent
    return  active_dict