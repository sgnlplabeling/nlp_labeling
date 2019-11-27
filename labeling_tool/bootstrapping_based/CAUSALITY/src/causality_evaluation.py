#-*- coding:utf-8 -*-
import pycrfsuite
import causality_settings as st
import codecs
import os
import sys
eval_path = "../evaluation"
eval_temp = os.path.join(eval_path, "temp")
eval_script = os.path.join(eval_path, "conlleval")

class myTagger(object) :
    #def __init__(self, X_test, y_test = None,X_4conf = None,y_4conf=None, test_sents = None,conf = False ,conf_init = 1.0, conf_step = 0.0, conf_limit= 1.0, link_positions = None, link_iter = -1):
    def __init__(self, X_test, y_test=None, test_sents=None):
        self.tagger = pycrfsuite.Tagger()
        self.X_test = X_test
        self.y_test=y_test
        self.test_sents = test_sents  # test sent can be none.
        self.Best_F = 0.0

    def find_ith(self,float_list, ith):
        float_list.sort(reverse=True)
        if ith < len(float_list) :
            return float_list[ith]
        else : return float_list[-1]

    def make_tag_idx(self, ans_seq):
        B_num = 0
        all_answer_start = []
        all_answer_end = []
        all_answer_tag = []

        for sent in ans_seq:
            start_idx = []
            end_idx = []
            tag_set = []
            tag_num = 0
            flag = 0

            for tag in sent:
                try :
                    if flag == 1 and tag[0] != 'I':
                        end_idx.append(tag_num - 1)
                        flag = 0
                except :
                    print()

                if tag[0] == 'B':
                    B_num = B_num + 1
                    start_idx.append(tag_num)
                    tag_set.append(tag[2:4])
                    flag = 1
                tag_num = tag_num + 1

            if flag == 1:
                end_idx.append(tag_num - 1)

            all_answer_start.append(start_idx)
            all_answer_end.append(end_idx)
            all_answer_tag.append(tag_set)

        return (all_answer_start, all_answer_end, all_answer_tag, B_num)
    def eval(self, pred_seq, ans_seq = None):  #changed
        if ans_seq == None : ans_seq = self.y_test

        correct_num = 0

        (all_answer_start, all_answer_end, all_answer_tag, answer_num) = self.make_tag_idx(ans_seq)
        (all_pred_start, all_pred_end, all_pred_tag, pred_num) = self.make_tag_idx(pred_seq)

        for i in range(0, len(ans_seq)):
            for j in range(0, len(all_pred_start[i])):
                for k in range(0, len(all_answer_start[i])):
                    if all_pred_start[i][j] == all_answer_start[i][k] and all_pred_end[i][j] == all_answer_end[i][k] and \
                                    all_pred_tag[i][j] == all_answer_tag[i][k]: correct_num = correct_num + 1
        return (correct_num, pred_num, answer_num)

    def eval1(self, sents, preds):
        prediction = []
        new_F = 0.0
        predf = eval_temp + '/pred.' + 'test'
        scoref = eval_temp+ '/score.' + 'test'
        Best_scoref = eval_temp+ '/Best_score.' + 'test'
        with codecs.open(predf, 'w', 'utf-8') as f:
            for s, s_p in zip(sents, preds):
                for t, p in zip(s, s_p):
                    f.write(t[0] + '/' + t[1] + ' ' +t[-1]+ ' ' + p + '\n')
                f.write('\n')
        os.system('%s < %s > %s' %(eval_script, predf, scoref))
        eval_lines = [l.rstrip() for l in codecs.open(scoref, 'r', "utf-8")]

        for i, line in enumerate(eval_lines):
            print(line)
            if i ==1:
                new_F = float(line.strip().split()[-1])

        return new_F

    def _draw_confusion_table(self, pred, tag) :
        TN = 0
        FP = 0
        FN = 0
        TP = 0
        out_str = 'confusion table for ' + tag + '\n'
        for y_tr_st, y_prediction in zip(self.y_test, pred) :
            for bio_tr_st, bio_pred in zip(y_tr_st, y_prediction) :
                if tag != bio_pred  and tag != bio_tr_st :
                    TN += 1
                elif tag != bio_pred and tag ==bio_tr_st :
                    FN += 1
                elif tag == bio_pred and tag != bio_tr_st :
                    FP += 1
                elif tag == bio_pred and tag == bio_tr_st :
                    TP += 1
        out_str += 'TN : ' + str(TN) + ', FN : ' + str(FN) + ', FP : ' + str(FP) + ', TP : ' + str(TP) + '\n'
        precision = 0.0
        if float(TP + FP) != 0.0:
            precision = float(TP) / float(TP + FP)
        recall = 0.0
        if float(FN + TP) != 0.0:
            recall = float(TP) / float(FN + TP)
        f1score = 0.0
        if float(precision) + recall != 0.0:
            f1score = 2.0 * (precision * recall) / (precision + recall)
        out_str += 'precision : ' + str(precision) + ', recall : ' + str(recall) + ', f1score : ' + str(f1score) + '\n'
        print(out_str)

    def eval_prediction(self, sents, ypred, tag_conf_table = False, log = False):
        out_str = 'evaluation\n'
        Test_F = 0.0
        cor, pred, ans = self.eval(ypred)
        if tag_conf_table == True :
            for tag in st.TAG :
                self._draw_confusion_table(ypred, tag)
        #precision = float(cor) / pred
        #recall = float(cor) / ans
        #f1score = 2.0 * (precision * recall) / (precision + recall)
        #out_str += 'NEs : ' + str(pred) + ', precision : ' + str(precision) + ', recall : ' + str(
        #    recall) + ', f1score : ' + str(f1score) + '\n'
        #print(out_str)
        print("\n")
        Test_F = self.eval1(sents, ypred)
        print(("F1 Socre =  {}%").format(Test_F))
        if Test_F > self.Best_F:
            self.Best_F = Test_F
            print(("Best F1 Socre =  {}%").format(self.Best_F))
        else:
            print(("Best F1 Socre =  {}%").format(self.Best_F))

        return self.Best_F
