import pycrfsuite
import math
import ner_settings as st
import codecs
import ner_preprocessing as pre #for defaut
class myTagger(object) :
    def __init__(self, X_test, y_test = None,X_4conf = None,y_4conf=None, test_sents = None,conf = False ,conf_init = 1.0, conf_step = 0.0, conf_limit= 1.0, link_positions = None, link_iter = -1):
        self.tagger = pycrfsuite.Tagger()
        self.X_test = X_test
        self.y_test=y_test #can be none
        self.X_4conf=X_4conf  #can be none
        self.y_4conf = y_4conf #can be none
        self.test_sents = test_sents  # test sent can be none.
        self.conf = conf
        self.conf_init = conf_init
        self.conf_step = conf_step
        self.conf_limit = conf_limit
        self.link_positions = link_positions
        self.link_iter = link_iter

    ###added for dic###
    def set_X_test(self, X_test_new):
        self.X_test = X_test_new
    ###################
    def remove_I_without_B(self,yseq):
        for y_idx in range(len(yseq)):
            if yseq[y_idx][0] is 'I':
                if y_idx is 0:
                    yseq[y_idx] = 'O'
                elif yseq[y_idx - 1] != 'B' + yseq[y_idx][1:] and yseq[y_idx - 1] != yseq[y_idx]:
                    yseq[y_idx] = 'O'
        return yseq
    def remove_not_candidates(self, seq_idx,yseq):
        copy_yseq = list(yseq)
        if self.link_positions is not None :
            candidate = self.link_positions[seq_idx]
            for i in range(len(copy_yseq)) :
                if i not in candidate :
                    copy_yseq[i] = 'O'
        return copy_yseq
    def post_process(self, min_conf,seq_idx, yseq):
        if self.tagger.probability(yseq) >= min_conf:
            return self.remove_I_without_B(self.remove_not_candidates(seq_idx,yseq))
        else:
            return []

    '''def _make_predictoin(self, model_name, s_point = 0, e_point = -1): #needed to be conf
        if e_point == -1 :
            e_point = len(self.X_test)
        self.tagger.open(model_name)
        y_pred = [self.remove_I_without_B(self.tagger.tag(xseq)) for xseq in self.X_test[s_point : e_point]]
        self.tagger.close()
        return y_pred'''

    def calc_min_prob(self, model_name):
        X_train = self.X_4conf
        y_train = self.y_4conf
        tagger = self.tagger

        # if bootstrap is false return
        tagger.open(model_name)
        probs_y = []
        for xseq, yseq in zip(X_train, y_train):
            ypred = tagger.tag(xseq)
            #probs_y.append(tagger.probability(yseq))
            if ypred == yseq:
                probs_y.append(tagger.probability(yseq))
        tagger.close()
        tmp_min = min(probs_y)
        # ho! feel my magic
        # tmp_min = 0.7
        print('min : ' + str(tmp_min))
        return tmp_min
    def find_ith(self,float_list, ith):
        float_list.sort(reverse=True)
        if ith < len(float_list) :
            return float_list[ith]
        else : return float_list[-1]
    def calc_moving_threshold(self, model_name, prob):
        X_train = self.X_4conf
        y_train = self.y_4conf
        tagger = self.tagger

        # if bootstrap is false return
        tagger.open(model_name)
        probs_y = []
        for xseq, yseq in zip(X_train, y_train):
            ypred = tagger.tag(xseq)
            #probs_y.append(tagger.probability(yseq))
            if ypred == yseq:
                probs_y.append(tagger.probability(yseq))
        tagger.close()
        threshold = self.find_ith(probs_y, int(math.ceil(len(probs_y)*prob)))
        # ho! feel my magic
        # tmp_min = 0.7
        print('threshold : ' + str(threshold))
        return threshold

    def bound(self, fnum):
        if fnum<self.conf_init : return self.conf_init
        elif fnum>self.conf_limit : return self.conf_limit
        else : return fnum
    def stop_link(self):
        self.link_positions = None
    def make_predictoin(self, model_name, s_point = 0, e_point = -1, bootiter = None) :
        model_name = '../model/'+model_name+'.crfsuite'
        if e_point == -1 :
            e_point = len(self.X_test)
        min_conf = 0.0
        if self.conf is True :
            conf_cover_ratio = self.bound(self.conf_init+bootiter*self.conf_step)
            print('confidence cover ratio : ' + str(conf_cover_ratio))
            if conf_cover_ratio == 1.0:
                min_conf = self.calc_min_prob(model_name)
            else :
                min_conf = self.calc_moving_threshold(model_name,conf_cover_ratio)
        self.tagger.open(model_name)
        #if min_conf is 0.0:
        #    y_pred = [self.remove_I_without_B(self.tagger.tag(xseq)) for xseq in self.X_test[s_point : e_point]]
        #else:
        #    y_pred = [self.post_process(min_conf, self.tagger.tag(xseq)) for xseq in self.X_test[s_point : e_point]]
        y_pred = [self.post_process(min_conf,xseq_idx, self.tagger.tag(self.X_test[xseq_idx])) for xseq_idx in range(s_point, e_point)]
        self.tagger.close()
        return y_pred

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

    def eval_prediction(self, ypred, tag_conf_table = False, log = True):
        out_str = 'evaluation\n'
        cor, pred, ans = self.eval(ypred)
        if tag_conf_table == True :
            for tag in st.TAG :
                self._draw_confusion_table(ypred, tag)
        precision = float(cor) / pred
        recall = float(cor) / ans
        f1score = 2.0 * (precision * recall) / (precision + recall)
        out_str += 'NEs : ' + str(pred) + ', precision : ' + str(precision) + ', recall : ' + str(
            recall) + ', f1score : ' + str(f1score) + '\n'
        if log == True :
            st.write_log(out_str,open=True,close=True, std_print=True)
        else :
            print(out_str)
        return f1score
        #return f1score

    '''def eval_prediction(self, pred):
        out_str = 'evaluation\n'
        cor, pred, ans = self.eval(pred)
        precision = float(cor) / pred
        recall = float(cor) / ans
        f1score = 2.0*(precision*recall)/(precision + recall)
        out_str += 'NEs : '+ str(pred)+', precision : ' + str(precision) + ', recall : ' + str(recall) + ', f1score : ' + str(f1score) + '\n'
        print(out_str)'''

    def eval_n_compare_models(self, base_line_name,final_model_name, model_spec): #called
        base_line_name = '../model/' + base_line_name + '.crfsuite'
        final_model_name = '../model/' + final_model_name + '.crfsuite'

        y_base_pred_test = self.make_predictoin(base_line_name)
        y_fin_pred_test = self.make_predictoin(final_model_name)

        self.write_labeled_file(y_base_pred_test, '../summary/' + model_spec + '_base.bio')
        self.write_labeled_file(y_fin_pred_test, '../summary/' + model_spec + '_fin.bio')

        ####tmp comparing
        '''
        print('tmp comparing : y_base/y_fin , y_test/y_base, y_test/y_fin')
        compare_label(X_test, y_base_pred_test, y_fin_pred_test, './compare/'+model_spec+'base_fin'+'.compare')
        compare_label(X_test, y_test, y_base_pred_test,
                      './compare/test_base' + model_spec + '.compare')
        compare_label(X_test, y_test, y_fin_pred_test, './compare/'+model_spec+'test_fin'+'.compare')
        #####
        '''
        # evaluation
        out_str = model_spec + ' evaluation\n'
        t_in_both, t_in_fin, t_in_base = self.eval(ans_seq=y_base_pred_test, pred_seq=y_fin_pred_test)
        out_str += 'NEs in both : ' + str(t_in_both) + ', in base : ' + str(t_in_base) + ', in fin : ' + str(
            t_in_fin) + '\n'
        cor, pred, ans = self.eval(y_base_pred_test)
        out_str += 'baseline precision : ' + str(float(cor) / pred) + ', recall : ' + str(float(cor) / ans) + '\n'
        cor, pred, ans = self.eval(y_fin_pred_test)
        out_str += 'final precision : ' + str(float(cor) / pred) + ', recall : ' + str(float(cor) / ans) + '\n'
        summary_file_name = '../summary/' + model_spec + '.summary'
        print(out_str)

    def write_labeled_file(self, new_label, filepath):
        sents = self.test_sents
        with open(filepath, 'w') as wf:
            for s_idx in range(len(sents)):
                for tup_idx in range(len(sents[s_idx])):
                    out_str = sents[s_idx][tup_idx][0] + ' ' + sents[s_idx][tup_idx][1] + ' 1 ' + new_label[s_idx][
                        tup_idx] + '\n'
                    wf.write(out_str.encode('utf-8'))
                #wf.write(out_str.encode('utf-8'))

    def eval_model(self, model_name):
        print('!!!!'+model_name)
        y_pred_test = self.make_predictoin(model_name)
        self.write_labeled_file(y_pred_test, '../summary/' + model_name + '.bio')
        ####tmp comparing
        '''
        print('tmp comparing : y_base/y_fin , y_test/y_base, y_test/y_fin')
        compare_label(X_test, y_base_pred_test, y_fin_pred_test, './compare/'+model_spec+'base_fin'+'.compare')
        compare_label(X_test, y_test, y_base_pred_test,
                      './compare/test_base' + model_spec + '.compare')
        compare_label(X_test, y_test, y_fin_pred_test, './compare/'+model_spec+'test_fin'+'.compare')
        #####
        '''
        # evaluation
        out_str = model_name + ' evaluation\n'
        cor, pred, ans = self.eval(y_pred_test)
        precision = float(cor) / pred
        recall = float(cor) / ans
        f1score = 2.0*(precision*recall)/(precision + recall)
        out_str += 'NEs : '+ str(pred)+', precision : ' + str(precision) + ', recall : ' + str(recall) + ', f1score : ' + str(f1score) + '\n'
        #summary_file_name = '../summary/' + model_name + '.summary'
        print(out_str)
        #with open(summary_file_name, 'w') as wf:
        #    wf.write(out_str)

'''
print('Reading files')
f = codecs.open('../data/' + 'test_iob.txt', 'r', encoding='utf-8')
test_sents = pre.read_labeled_file(f)
X_test = [pre.sent2features(s) for s in test_sents]
y_test = [pre.sent2labels(s) for s in test_sents]
tagger = myTagger(test_sents, X_test, y_test)
model_spec = '20170801-162734ner_Biter3'
base_line_name = '../model/_tr_train_iob.txt_u_unlabeled.pkl_bootsize_20000020170801-162734ner_base.crfsuite'
final_model_name = '../model/_tr_train_iob.txt_u_unlabeled.pkl_bootsize_20000020170801-162734ner_Biter3.crfsuite'
tagger.eval_n_compare_models(base_line_name, final_model_name, model_spec)'''
