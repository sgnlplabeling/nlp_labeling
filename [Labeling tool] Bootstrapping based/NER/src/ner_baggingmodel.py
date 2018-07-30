import ner_preprocessing as pre
import ner_utils as utils
import ner_settings as st
from scipy.stats import entropy
import operator
from ner_basicmodel import BasicModel
from collections import Counter
TAG = ['B-DT','B-LC', 'B-OG','B-PS','B-TI','I-DT','I-LC','I-OG','I-PS','I-TI', 'O']
max_entropy = entropy([1.0 / st.NUM_BAGGING_MODEL for i in range(st.NUM_BAGGING_MODEL)])
class ComponentModel(BasicModel) :
    def __init__(self, model_path, model_name, X_fixed, y_fixed,save_path=None):
        self.X_fixed = X_fixed
        self.y_fixed = y_fixed
        super(ComponentModel,self).__init__(model_path, model_name,save_path)
        self._add_fixed_data_to_trainer()
    ## added for dicitionary##
    def set_X_fixed(self, X_fixed_new):
        self.X_fixed = X_fixed_new
        self.trainer.clear()
        self._add_fixed_data_to_trainer()
    ##########################
    def set_self_n_train_CRF(self,X, y, clear=False):
        self.trainer.clear()
        self._add_fixed_data_to_trainer()
        self.add_n_train_CRF(X,y, clear_past_model = clear)#add_n_train_CRF(self, X, y, clear_past_model = False, add_total = False, write_added = True):
    def _add_fixed_data_to_trainer(self):
        for xseq, yseq in zip(self.X_fixed, self.y_fixed):
            self.trainer.append(xseq, yseq)
    def _get_marginal_prob_distribution(self, y_idx):
        dist_lst = [self.tagger.marginal(tag, y_idx) for tag in TAG]
        return tuple(dist_lst)
    def make_prediction(self, X_test):
        if self.iter < 1: return None
        latest_model_name = self.model_name + str(self.iter - 1)
        #print('open : ' + latest_model_name)
        self.tagger.open(self.model_path + latest_model_name + '.crfsuite')
        y_preds = []
        y_preds_mar_prob_dists = []
        for xseq in X_test:
            y_pred = self.tagger.tag(xseq)
            y_pred_mar_prob_dist = []
            for t, y in enumerate(y_pred):
                y_pred_mar_prob_dist.append(self._get_marginal_prob_distribution(t))
            y_preds.append(y_pred)
            y_preds_mar_prob_dists.append(y_pred_mar_prob_dist)
        # y_pred = [self.tagger.tag(xseq) for xseq in X_test]
        self.tagger.close()
        # return y_pred
        return y_preds, y_preds_mar_prob_dists


class BaggingModel(object) :
    #(BAGGING_DATA_SAVE_PATH,BAGGING_MODEL_NAME, num_of_comp_mds=5,X_labeled = X_train,y_labeled = y_train,save_path=BAGGING_DATA_SAVE_PATH)
    def __init__(self, model_path, model_name, num_of_comp_mds,boot_sample_size,X_labeled, y_labeled, save_path=None, start_iter = 0):
        self.model_path = model_path
        self.model_name = model_name
        self.num_of_comp_mds = num_of_comp_mds
        self.boot_sample_size = boot_sample_size
        self.save_path = save_path
        self.iter = start_iter
        self.X_fixed = X_labeled
        self.y_fixed = y_labeled
        self.component_models = []
        self.X_selflabeled = []
        self.y_selflabeled = []
        for i in range(self.num_of_comp_mds) :
            self.component_models.append(ComponentModel(self.model_path+str(i)+'/',self.model_name+str(i),self.X_fixed,self.y_fixed, self.save_path+str(i)+'/' if self.save_path != None else None))

    ##added for dictionary##
    def set_X_fixed(self, X_fixed_new):
        self.X_fixed = X_fixed_new
        for cp_model in self.component_models :
            cp_model.set_X_fixed(self.X_fixed)
    ########################
    def set_selflabeled_data_n_train(self,X_new,y_new):
        self.X_selflabeled = X_new
        self.y_selflabeled = y_new
        #X_boot_samples = pre.split_set_w_size(X_new,self.boot_sample_size,self.num_of_comp_mds)
        #y_boot_samples = pre.split_set_w_size(y_new,self.boot_sample_size,self.num_of_comp_mds)
        X_boot_samples = pre.split_set(X_new, [1.0 / float(self.num_of_comp_mds) for i in range(self.num_of_comp_mds)])
        y_boot_samples = pre.split_set(y_new, [1.0 / float(self.num_of_comp_mds) for i in range(self.num_of_comp_mds)])
        for cp_idx in range(self.num_of_comp_mds):
            self.component_models[cp_idx].set_self_n_train_CRF(X_boot_samples[cp_idx],y_boot_samples[cp_idx], clear = True)
    ##added for ??##
    '''def add_selflabeled_data_n_train(self,X_new,y_new):
        self.X_selflabeled += X_new
        self.y_selflabeled += y_new
        #X_boot_samples = pre.split_set_w_size(X_new,self.boot_sample_size,self.num_of_comp_mds)
        #y_boot_samples = pre.split_set_w_size(y_new,self.boot_sample_size,self.num_of_comp_mds)
        X_boot_samples =  pre.split_set(X_new, [1.0/float(self.num_of_comp_mds) for i in range(self.num_of_comp_mds)])
        y_boot_samples = pre.split_set(y_new, [1.0/float(self.num_of_comp_mds) for i in range(self.num_of_comp_mds)])
        for cp_idx in range(self.num_of_comp_mds):
            self.component_models[cp_idx].add_n_train_CRF(X_boot_samples[cp_idx],y_boot_samples[cp_idx])#add_n_train_CRF(self, X, y, clear_past_model = False, add_total = False, write_added = True):'''
    ########################
    def make_prediction(self, X_test, remove_all_o = True, min_conf = 0.0, link_pos = None, replace_o = False, mul_ne_cnt = False):
        component_preds = []
        component_marginal_prob_dists = []
        for cp_idx in range(self.num_of_comp_mds) :
            cp_pred, cp_marginal_prob_dist = self.component_models[cp_idx].make_prediction(X_test)
            component_preds.append(cp_pred)
            component_marginal_prob_dists.append(cp_marginal_prob_dist)
        return self._vote_predictions(component_preds, component_marginal_prob_dists, remove_all_o, min_conf, link_pos, replace_o, mul_ne_cnt)
    def _vote_predictions(self,component_preds, component_marginal_prob_dists, remove_all_o, min_conf, link_pos, replace_o, mul_ne_cnt): #need to be modified
        vote_function = self._vote_on_dist

        voted_preds = []
        pred_scores = []
        for seq_idx in range(len(component_preds[0])) :
            voted_seq = []
            score_seq = []
            for bio_idx in range(len(component_preds[0][seq_idx])) :
                pred_4_one = [component_preds[cp_idx][seq_idx][bio_idx] for cp_idx in range(len(component_preds))]

                mar_prob_dist_4_one = [component_marginal_prob_dists[cp_idx][seq_idx][bio_idx] for cp_idx in range(len(component_preds))]
                #for cp_idx in range(len(component_preds)):
                #    pred_4_one.append(component_preds[cp_idx][seq_idx][bio_idx])
                #    mar_prob_4_one.append()
                result, score = vote_function(pred_4_one, mar_prob_dist_4_one)
                voted_seq.append(result)
                score_seq.append(score)
            if len(score_seq) != 0 :
                voted_seq, _, score_seq  = utils.post_process_y(voted_seq, score_seq, remove_all_o, min_conf, None if link_pos == None else link_pos[seq_idx], replace_o=replace_o, mul_ne_cnt=mul_ne_cnt)
            voted_preds.append(voted_seq)
            pred_scores.append(score_seq)
        return voted_preds, pred_scores
    def _vote_on_prob(self, preds, probs): #need to be fixed !!!!!
        vote_dic = dict()
        for p_idx in range(len(preds)) :
            vote_dic[preds[p_idx]] = vote_dic.get(preds[p_idx],0.0) + probs[p_idx]
        voted_bio, prob_sum = max(vote_dic.iteritems(), key=operator.itemgetter(1))
        return voted_bio, prob_sum/float(len(preds))
    def _vote_on_dist(self, preds, dist): #need to be fixed !!!!!
        ele_sum = []
        for tidx in range(len(TAG)) :
            s = 0.0
            for cp_idx in range(len(dist)) :
                s+=dist[cp_idx][tidx]
            ele_sum.append(s)
        idx, sum = max(enumerate(ele_sum), key=operator.itemgetter(1))
        return TAG[idx], sum/len(dist)
    def _vote_on_dist_entropy(self, preds, dist): #need to be fixed !!!!!
        ele_avg_with_ent = []
        for tidx in range(len(TAG)) :
            s = 0.0
            tag_dist = []
            for cp_idx in range(len(dist)) :
                s+=dist[cp_idx][tidx]
                tag_dist.append(dist[cp_idx][tidx])
            avg_with_ent = (s / len(preds)) * (entropy(tag_dist)/max_entropy)
            ele_avg_with_ent.append(avg_with_ent)
        idx, avg_with_ent = max(enumerate(ele_avg_with_ent), key=operator.itemgetter(1))
        return TAG[idx], avg_with_ent

    def _vote(self, preds, prob=None): #need to be modified
         count = Counter(preds)
         most_tag, most_cnt = count.most_common()[0]
         most_prob = float(most_cnt)/len(preds)
         return most_tag, most_prob