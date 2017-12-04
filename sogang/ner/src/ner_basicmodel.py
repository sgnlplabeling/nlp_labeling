import pycrfsuite
import cPickle as pickle
import ner_settings as st
import os
import ner_utils as utils
import ner_settings as st
class BasicModel(object) :
    def __init__(self, model_path, model_name, save_path = None, start_iter = 0) :
        self.model_path = model_path
        self.model_name = model_name
        self.trainer = pycrfsuite.Trainer(verbose=False)
        self.tagger = pycrfsuite.Tagger()
        self.iter = start_iter #
        self.save_path = save_path
        if not os.path.exists(self.model_path):
            os.makedirs(self.model_path)
        if self.save_path is not None :
            if not os.path.exists(self.save_path):
                os.makedirs(self.save_path)
        if st.DICTIONARY is True or st.SELF_ITER_N > 1:
            self.X_total = []  ## added for dicionary
            self.y_total = []
        #if st.RELOAD is True : ###
        #    added_data = self._load_data(save_path)
        #    self.trainer.append(added_data)
        #    self.iter += 1
    def make_prediction(self,X_test, remove_all_o = True, min_conf = 0.0, link_pos = None): #not used when this is component classifier
        if self.iter <1 : return None
        latest_model_name = self.model_name + str(self.iter-1)
        #print('open : '+latest_model_name)
        self.tagger.open(self.model_path + latest_model_name + '.crfsuite')
        y_preds = []
        y_preds_mar_probs = []
        for seq_idx, xseq in enumerate(X_test):
            y_pred_ori = self.tagger.tag(xseq) # ????????????
            #if self.tagger.probability(y_pred_ori) < min_conf :
            #    y_preds.append([])
            #    y_preds_mar_probs.append([])
            #    continue
            y_pred_mar_prob = []
            for t, y in enumerate(y_pred_ori):
                y_pred_mar_prob.append(self.tagger.marginal(y, t))
            if st.FIXED_MIN_SEQ_PROB == None :
                y_pred_post, _1, y_pred_mar_prob = utils.post_process_y(y_pred_ori,y_pred_mar_prob, remove_all_o, min_conf, None if link_pos == None else link_pos[seq_idx])
            else :
                seq_prob = self.tagger.probability(y_pred_ori)
                y_pred_post, _1, y_pred_mar_prob = utils.post_process_y(y_pred_ori, y_pred_mar_prob, remove_all_o, min_conf,
                                                                    None if link_pos == None else link_pos[seq_idx], seq_prob = seq_prob)
            #y_pred_mar_prob = []
            #if len(y_pred_post) >0 :
            #    for t, y in enumerate(y_pred_ori) :
            #        y_pred_mar_prob.append(self.tagger.marginal(y, t))
            y_preds.append(y_pred_post)
            y_preds_mar_probs.append(y_pred_mar_prob)
        #y_pred = [self.tagger.tag(xseq) for xseq in X_test]
        self.tagger.close()
        #return y_pred
        return y_preds, y_preds_mar_probs
    def temp_add_n_train_CRF(self, X, y, sub_iter):
        clear_past_model = False if sub_iter == 1 else True
        self.add_n_train_CRF(X,y,clear_past_model=clear_past_model, add_total=False, write_added=False)
        self._recover_trainer_with_total()
    def _recover_trainer_with_total(self):
        self.trainer.clear()
        for xseq, yseq in zip(self.X_total, self.y_total):
            self.trainer.append(xseq, yseq)
    def remove_latest_model(self):
        if os.path.exists(self.model_path + self.model_name + str(self.iter - 1) + '.crfsuite'):
            os.remove(self.model_path + self.model_name + str(self.iter - 1) + '.crfsuite')
    def get_first_model_name(self):
        return self.model_path + self.model_name + str(0) + '.crfsuite'
    def add_n_train_CRF(self, X, y, yprob = None,clear_past_model = False, add_total = False, write_added = True):
        this_model_name = self.model_name + str(self.iter)
        added_cnt = 0
        X_added = []
        y_added = []
        yprob_added = []
        if yprob != None :
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
        if add_total is True:
            self.X_total += X_added #added for dic
            self.y_total += y_added
        #st.write_log('added : ' + str(added_cnt) + '/' + str(len(y)), open=True, close=True, std_print=False)
        if self.save_path is not None and write_added is True:
            st.write_log('writing added data file', open=True,close=True,std_print=False)
            if os.path.isfile(self.save_path + str(self.iter) + '.pkl')  :
                save_path = self.save_path + 'R'
            else :
                save_path = self.save_path
            with open(save_path + str(self.iter) + '.pkl', 'wb') as output:
                pickle.dump(X_added, output, pickle.HIGHEST_PROTOCOL)
                pickle.dump(y_added, output, pickle.HIGHEST_PROTOCOL)
                if yprob != None :
                    pickle.dump(yprob_added, output, pickle.HIGHEST_PROTOCOL)
        if clear_past_model == True and self.iter > 0:
            if os.path.exists(self.model_path + self.model_name + str(self.iter - 1)+'.crfsuite') :
                os.remove(self.model_path + self.model_name + str(self.iter - 1)+'.crfsuite')
        self.trainer.set_params({
            'c1': 0.0,  # coefficient for L1 penalty
            'c2': 0.0,  # coefficient for L2 penalty
            'max_iterations': st.CRF_ITER,  # stop earlier ****
            # include transitions that are possible, but not observed
            'feature.possible_transitions': True
        })
        self.trainer.params()
        self.trainer.train(self.model_path + this_model_name + '.crfsuite')  # model save
        self.trainer.logparser.last_iteration  # ???
        self.iter += 1
    def _add_n_train_CRF(self, X, y,yprob = None, clear = False):
        this_model_name = self.model_name + str(self.iter)
        added_cnt = 0
        X_added = []
        y_added = []
        yprob_added = []
        if yprob!= None :
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
        if st.DICTIONARY is True:
            self.X_total += X_added #added for dic
            self.y_total += y_added
        #st.write_log('added : ' + str(added_cnt) + '/' + str(len(y)), open=True,close=True, std_print=False)
        if self.save_path is not None :
            st.write_log('writing added data file', open=True, close=True, std_print=False)
            if os.path.isfile(self.save_path + str(self.iter) + '.pkl')  :
                save_path = self.save_path + 'R'
            else :
                save_path = self.save_path
            with open(save_path + str(self.iter) + '.pkl', 'wb') as output:
                pickle.dump(X_added, output, pickle.HIGHEST_PROTOCOL)
                pickle.dump(y_added, output, pickle.HIGHEST_PROTOCOL)
                if yprob != None :
                    pickle.dump(yprob_added, output, pickle.HIGHEST_PROTOCOL)
        if clear == True and self.iter > 0:
            os.remove(self.model_path + self.model_name + str(self.iter - 1)+'.crfsuite')
        self.trainer.set_params({
            'c1': 0.0,  # coefficient for L1 penalty
            'c2': 0.0,  # coefficient for L2 penalty
            'max_iterations': st.CRF_ITER,  # stop earlier ****
            # include transitions that are possible, but not observed
            'feature.possible_transitions': True
        })
        self.trainer.params()
        self.trainer.train(self.model_path + this_model_name + '.crfsuite')  # model save
        self.trainer.logparser.last_iteration  # ???
        self.iter += 1
    ## added for dictionary ##
    #this methond only allows X_total_new whose origianl seq is same with the older one but the feature value is different
    def set_X_total(self, X_total_new):
        self.X_total = X_total_new
        self.trainer.clear()
        for xseq, yseq in zip(self.X_total, self.y_total) :
            self.trainer.append(xseq, yseq)
    ##########################