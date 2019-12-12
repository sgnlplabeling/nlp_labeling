#-*- coding:utf -*-
import pycrfsuite
import pickle as pickle
import os
import causality_utils as utils
import causality_settings as st
import sys
class BasicModel(object) :
    def __init__(self, model_path, model_name, save_path = None, start_iter = 0) :
        self.model_path = model_path
        self.model_name = model_name
        self.trainer = pycrfsuite.Trainer(verbose=False)
        self.tagger = pycrfsuite.Tagger()
        self.iter = start_iter
        self.save_path = save_path
        if not os.path.exists(self.model_path):
            os.makedirs(self.model_path)
        if self.save_path is not None :
            if not os.path.exists(self.save_path):
                os.makedirs(self.save_path)

    def make_prediction(self,X_test, remove_all_o = True, min_conf = 0.0): #not used when this is component classifier
        if self.iter <1 : return None
        latest_model_name = self.model_name + str(self.iter-1)
        self.tagger.open(self.model_path + latest_model_name + '.crfsuite')
        y_preds = []
        y_preds_mar_probs = []
        for seq_idx, xseq in enumerate(X_test):
            y_pred_ori = self.tagger.tag(xseq)
            y_pred_mar_prob = []
            for t, y in enumerate(y_pred_ori):
                y_pred_mar_prob.append(self.tagger.marginal(y, t))
            if st.FIXED_MIN_SEQ_PROB == None :
                y_pred_post, _1, y_pred_mar_prob = utils.post_process_y(y_pred_ori,y_pred_mar_prob, remove_all_o, min_conf )
            else :
                seq_prob = self.tagger.probability(y_pred_ori)
                y_pred_post, _1, y_pred_mar_prob = utils.post_process_y(y_pred_ori, y_pred_mar_prob, remove_all_o, min_conf, seq_prob = seq_prob)
            y_preds.append(y_pred_post)
            y_preds_mar_probs.append(y_pred_mar_prob)
        self.tagger.close()
        return y_preds, y_preds_mar_probs

    def add_n_train_CRF(self, X, y, yprob=None, clear_past_model=False):
        this_model_name = self.model_name + str(self.iter)
        added_cnt = 0
        X_added = []
        y_added = []
        yprob_added = []

        if yprob != None: ##_____
            for xseq, yseq, yseqprob in zip(X, y, yprob):
                if len(yseq) != 0:
                    added_cnt += 1
                    X_added.append(xseq)
                    y_added.append(yseq)
                    yprob_added.append(yseqprob)
                    self.trainer.append(xseq, yseq)
        else :
            for xseq, yseq in zip(X, y):
                if len(yseq) != 0:
                    added_cnt += 1
                    X_added.append(xseq)
                    y_added.append(yseq)
                    self.trainer.append(xseq, yseq)

        print('added : ' + str(added_cnt) + '/' + str(len(y)))
        if self.save_path is not None:
            print('writing added data file')
            if os.path.isfile(self.save_path + str(self.iter) + '.pkl') is False :
                with open(self.save_path + str(self.iter) + '.pkl', 'wb') as output:
                    pickle.dump(X_added, output, pickle.HIGHEST_PROTOCOL)
                    pickle.dump(y_added, output, pickle.HIGHEST_PROTOCOL)
                    if yprob != None :
                        pickle.dump(yprob_added, output, pickle.HIGHEST_PROTOCOL)

        if clear_past_model == True and self.iter > 0:
            if os.path.exists(self.model_path + self.model_name + str(self.iter - 1)+'.crfsuite') :
                os.remove(self.model_path + self.model_name + str(self.iter - 1)+'.crfsuite')
        self.trainer.set_params({
            'c1': 1.0,  # coefficient for L1 penalty
            'c2': 1e-3,  # coefficient for L2 penalty
            'max_iterations': st.CRF_ITER,  # stop earlier ****
            # include transitions that are possible, but not observed
            'feature.possible_transitions': True
        })
        self.trainer.params()
        self.trainer.train(self.model_path + this_model_name + '.crfsuite')  # model save
        self.trainer.logparser.last_iteration  # ???
        self.iter += 1


    def add_n_train_active_CRF(self, X_sents, X, y, yprob=None, clear_past_model=False):
        this_model_name = self.model_name + str(self.iter)
        added_cnt = 0
        X_sents_added = []
        X_added = []
        y_added = []
        yprob_added = []

        if yprob != None: ##_____
            for xsents, xseq, yseq, yseqprob in zip(X_sents, X, y, yprob):
                if len(yseq) != 0:
                    added_cnt += 1
                    X_sents_added.append(xsents)
                    X_added.append(xseq)
                    y_added.append(yseq)
                    yprob_added.append(yseqprob)
                    self.trainer.append(xseq, yseq)
        else :
            for xsents, xseq, yseq in zip(X_sents, X, y):
                if len(yseq) != 0:
                    added_cnt += 1
                    X_sents_added.append(xsents)
                    X_added.append(xseq)
                    y_added.append(yseq)
                    self.trainer.append(xseq, yseq)

        print('added : ' + str(added_cnt) + '/' + str(len(y)))
        # print(len(X_sents_added), len(X_added), len(y_added), len(yprob_added))
        
        
        # for i in yprob_added:
        #     sum = 0.0
        #     for j in i:
        #         sum+=j
        #     if sum/len(i) >= 0.8 :
        #         count+=1

        
        if self.save_path is not None:
            print('writing added data file')
            if os.path.isfile(self.save_path + str(self.iter) + '.pkl') is False :
                with open(self.save_path + str(self.iter) + '.pkl', 'wb') as output:
                    pickle.dump(X_added, output, pickle.HIGHEST_PROTOCOL)
                    pickle.dump(y_added, output, pickle.HIGHEST_PROTOCOL)
                    if yprob != None :
                        pickle.dump(yprob_added, output, pickle.HIGHEST_PROTOCOL)

        if clear_past_model == True and self.iter > 0:
            if os.path.exists(self.model_path + self.model_name + str(self.iter - 1)+'.crfsuite') :
                os.remove(self.model_path + self.model_name + str(self.iter - 1)+'.crfsuite')
        self.trainer.set_params({
            'c1': 1.0,  # coefficient for L1 penalty
            'c2': 1e-3,  # coefficient for L2 penalty
            'max_iterations': st.CRF_ITER,  # stop earlier ****
            # include transitions that are possible, but not observed
            'feature.possible_transitions': True
        })
        self.trainer.params()
        self.trainer.train(self.model_path + this_model_name + '.crfsuite')  # model save
        self.trainer.logparser.last_iteration  # ???
        self.iter += 1