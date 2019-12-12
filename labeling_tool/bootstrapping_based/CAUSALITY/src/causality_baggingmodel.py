import causality_utils as utils
import causality_settings as st
import operator
from causality_basicmodel import BasicModel
from collections import Counter
class ComponentModel(BasicModel) :
    def __init__(self, model_path, model_name, X_fixed, y_fixed,save_path=None):
        self.X_fixed = X_fixed
        self.y_fixed = y_fixed
        super(ComponentModel,self).__init__(model_path, model_name,save_path)
        self._add_fixed_data_to_trainer()
    def set_self_n_train_CRF(self,X_sents, X, y, y_probs, clear=False):
        self.trainer.clear()
        self._add_fixed_data_to_trainer()
        self.add_n_train_active_CRF(X_sents, X,y, y_probs, clear_past_model = clear)#add_n_train_CRF(self, X, y, clear_past_model = False, add_total = False, write_added = True):
    def _add_fixed_data_to_trainer(self):
        for xseq, yseq in zip(self.X_fixed, self.y_fixed):
            self.trainer.append(xseq, yseq)
    def _get_marginal_prob_distribution(self, y_idx):
        dist_lst = [self.tagger.marginal(tag, y_idx) for tag in st.TAG]
        return tuple(dist_lst)
    def make_prediction(self, X_test):
        if self.iter < 1: return None
        latest_model_name = self.model_name + str(self.iter - 1)
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
        self.tagger.close()
        return y_preds, y_preds_mar_prob_dists
class BaggingModel(object) :
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

    def set_selflabeled_data_n_train(self,X_sents,X_new,y_new, y_new_probs):
        self.X_sents = X_sents
        self.X_selflabeled = X_new
        self.y_selflabeled = y_new

        X_sents_boot_samples = utils.split_set(X_sents, [1.0 / float(self.num_of_comp_mds) for i in range(self.num_of_comp_mds)])
        X_boot_samples = utils.split_set(X_new, [1.0 / float(self.num_of_comp_mds) for i in range(self.num_of_comp_mds)])
        y_boot_samples = utils.split_set(y_new, [1.0 / float(self.num_of_comp_mds) for i in range(self.num_of_comp_mds)])
        y_probs_boot_samples = utils.split_set(y_new_probs, [1.0 / float(self.num_of_comp_mds) for i in range(self.num_of_comp_mds)])
        # print "example"
        # print len(X_sents_boot_samples[0]), len(X_boot_samples[0]), len(y_boot_samples[0]), len(y_probs_boot_samples[0])
        for cp_idx in range(self.num_of_comp_mds):
            self.component_models[cp_idx].set_self_n_train_CRF(X_sents_boot_samples[cp_idx], X_boot_samples[cp_idx], y_boot_samples[cp_idx], y_probs_boot_samples[cp_idx], clear = True)

    def make_prediction(self, X_test, remove_all_o = True, min_conf = 0.0):
        component_preds = []
        component_marginal_prob_dists = []
        for cp_idx in range(self.num_of_comp_mds) :
            cp_pred, cp_marginal_prob_dist = self.component_models[cp_idx].make_prediction(X_test)
            component_preds.append(cp_pred)
            component_marginal_prob_dists.append(cp_marginal_prob_dist)
        return self._vote_predictions(component_preds, component_marginal_prob_dists, remove_all_o, min_conf)

    def _vote_predictions(self,component_preds, component_marginal_prob_dists, remove_all_o, min_conf): #need to be modified
        if st.VOTE_ON_DIST is True :
            vote_function = self._vote_on_dist
        else :
            vote_function = self._vote
        voted_preds = []
        pred_scores = []
        for seq_idx in range(len(component_preds[0])) :
            voted_seq = []
            score_seq = []
            for bio_idx in range(len(component_preds[0][seq_idx])) :
                pred_4_one = [component_preds[cp_idx][seq_idx][bio_idx] for cp_idx in range(len(component_preds))]
                mar_prob_dist_4_one = None
                if st.VOTE_ON_DIST is True :
                    mar_prob_dist_4_one = [component_marginal_prob_dists[cp_idx][seq_idx][bio_idx] for cp_idx in range(len(component_preds))]
                result, score = vote_function(pred_4_one, mar_prob_dist_4_one)
                voted_seq.append(result)
                score_seq.append(score)
            if len(score_seq) != 0 :
                voted_seq, _, score_seq  = utils.post_process_y(voted_seq, score_seq, remove_all_o, min_conf)
            voted_preds.append(voted_seq)
            pred_scores.append(score_seq)
        return voted_preds, pred_scores

    def _vote_on_dist(self, preds, dist):
        ele_sum = []
        for tidx in range(len(st.TAG)) :
            s = 0.0
            for cp_idx in range(len(dist)) :
                s+=dist[cp_idx][tidx]
            ele_sum.append(s)
        idx, sum = max(enumerate(ele_sum), key=operator.itemgetter(1))
        return st.TAG[idx], sum/len(dist)

    def _vote(self, preds, prob=None):
         count = Counter(preds)
         most_tag, most_cnt = count.most_common()[0]
         most_prob = float(most_cnt)/len(preds)
         return most_tag, most_prob