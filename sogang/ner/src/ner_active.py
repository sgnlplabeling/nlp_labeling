import os, os.path
import glob
import cPickle as pickle
import ner_utils as utils
import ner_settings as st
class Active_Assistant(object) :
    def __init__(self, min_prob, max_prob,good_dir, active_dir, boot_iter = 0) :
        self.X_bf_active = []
        self.y_bf_active = []
        self.min_prob = min_prob
        self.max_prob = max_prob
        self.boot_iter = boot_iter
        self.active_put_count = 0
        self.good_dir = good_dir
        self.active_dir = active_dir
    def _save(self,X, y):
        save_path = self.active_dir+'save/'
        if os.path.exists(save_path) is False :
            os.makedirs(save_path)
        file_name = save_path+str(self.boot_iter) + '_' + str(self.active_put_count) + '.pkl'
        if os.path.exists(file_name) :
            file_name = save_path+str(self.boot_iter) + '_' + str(self.active_put_count) +'R'+ '.pkl'
        with open(file_name, 'wb') as output:
            pickle.dump(X, output, pickle.HIGHEST_PROTOCOL)
            pickle.dump(y, output, pickle.HIGHEST_PROTOCOL)
        file_names = os.listdir(save_path)
        if len(file_names) > st.ACTIVE_SAVE_NUM :
            file_names_boot_iter = [int(name.split('_')[0]) for name in file_names]
            min_boot_iter = min(file_names_boot_iter)
            for del_filename in glob.glob(save_path + str(min_boot_iter) +'_*'):
                os.remove(del_filename)
    def write_ML_data(self,orisents, nesents, X_auto, y_auto, y_mar_prob) :
        orisents_selected, nesents_selected, X_selected, y_selected,yprob_selected, orisents_remain, nesents_remain, X_remain, y_remain, yprob_remain = self._select_in_range(orisents, nesents, X_auto,y_auto,y_mar_prob)
        # orisents_remain, nesents_remain, X_remain, y_remain, yprob_remain remove all o
        st.write_log(str(len(X_selected))+':'+str(len(X_remain))+' = active : good', open=True,close=True,std_print=True)
        if st.PROB_OUT == True :
            print('writing : ' + self.active_dir + str(self.boot_iter) +'_active'+ '.txt')
            utils.write_result_from_ft(orisents_selected, nesents_selected, X_selected, y_selected, self.active_dir + str(self.boot_iter) +'_active'+ '.txt', yprob = yprob_selected)
            print('writing : ' + self.good_dir + str(self.boot_iter) + '_good'+'.txt')
            utils.write_result_from_ft(orisents_remain, nesents_remain, X_remain, y_remain, self.good_dir + str(self.boot_iter) + '_good'+'.txt', yprob = yprob_remain)
        else :
            print('writing : ' + self.active_dir + str(self.boot_iter) + '_active' + '.txt')
            utils.write_result_from_ft(orisents_selected,nesents_selected, X_selected, y_selected,
                                       self.active_dir + str(self.boot_iter) + '_active' + '.txt')
            print('writing : ' + self.good_dir + str(self.boot_iter) + '_good' + '.txt')
            utils.write_result_from_ft(orisents_remain, nesents_remain,X_remain, y_remain, self.good_dir + str(self.boot_iter) + '_good' + '.txt')
        return self.active_dir + str(self.boot_iter) +'_active'+ '.txt', self.good_dir + str(self.boot_iter) + '_good'+'.txt'
    def put_act_n_get_remain(self, X_auto, y_auto, y_mar_prob) :
        X_selected, y_selected,yprob_selected, X_remain, y_remain,yprob_remain = self._select_in_range(X_auto,y_auto,y_mar_prob)
        st.write_log(str(len(X_selected))+' sents are added to active data.', open=True,close=True,std_print=True)
        #write file(str(boot_iter) + '_' + str(self.active_put_count)+'.pkl)
        #if os.paty.size >50 , name = get, boot_names = for name.split(_),, remove_start_with( boot_name.int.sort.getfirst)
        self._save(X_selected, y_selected)
        self.X_bf_active += X_selected
        self.y_bf_active += y_selected
        self.active_put_count += 1
        #debug
        #X_remain = X_auto
        #y_remain = y_auto
        #yprob_remain = y_mar_prob
        return  X_remain, y_remain, yprob_remain
    def out_act_in_golden(self, boot_iter):
        self.boot_iter = boot_iter
        if os.path.exists(self.active_dir) is False :
            os.makedirs(self.active_dir)
        utils.write_result_from_ft(self.X_bf_active,self.y_bf_active,self.active_dir + str(boot_iter)+'.out')
        while True :
            print('ready?')
            ready = raw_input()
            active_in_fn = self.active_dir+ str(boot_iter)+'.in'
            if st.ACTIVE_DEBUG == True :
                active_in_fn = self.active_dir + str(boot_iter)+'.out'
            if os.path.exists(active_in_fn) :
                act_sents, X_golden, y_golden = utils.read_labeled_text_data(active_in_fn, encoding=st.ENCODING,flatten=st.FLATTEN)
                st.write_log(str(len(act_sents)) + ' sents are read from active data.', open=True, close=True,
                             std_print=True)
                y_golden,_,_ = utils._remove_all_o(y_golden,[],[])
                break
        print(active_in_fn)
        yprob_golden = utils.generate_all(y_golden, 1)
        if st.ACTIVE_DEBUG == True :
            idx = 0
            for x_b, x_a in zip(self.X_bf_active, X_golden) :
                idx += 1
                for x_ft_B, x_ft_A in zip(x_b, x_a) :
                    if tuple(x_ft_A) != tuple(x_ft_B) :
                        print('error!!!')
        self.X_bf_active = []
        self.y_bf_active = []
        self.active_put_count = 0
        return  X_golden, y_golden, yprob_golden
    def _select_in_range(self,orisents, nesents, X_auto,y_auto,y_mar_prob):
        oris_selected = []
        nes_selected = []
        X_selected = []
        y_selected = []
        yprob_selected = []
        oris_remain = []
        nes_remain = []
        X_remain = []
        y_remain = []
        yprob_remain =[]
        for ori_sent, ne_sent, X_sent, y_sent, yprob_sent in zip(orisents, nesents, X_auto, y_auto, y_mar_prob) :
            if len(y_sent) == 0 :
                oris_remain.append(ori_sent)
                nes_remain.append(ne_sent)
                X_remain.append(X_sent)
                y_remain.append(y_sent)
                yprob_remain.append(yprob_sent)
                continue
            sent_conf = min(yprob_sent)
            if sent_conf >= self.min_prob and sent_conf<=self.max_prob :
                oris_selected.append(ori_sent)
                nes_selected.append(ne_sent)
                X_selected.append(X_sent)
                y_selected.append(y_sent)
                yprob_selected.append(yprob_sent)
                #X_remain.append([])
                #y_remain.append([])
                #yprob_remain.append([])
            else :
                oris_remain.append(ori_sent)
                nes_remain.append(ne_sent)
                X_remain.append(X_sent)
                y_remain.append(y_sent)
                yprob_remain.append(yprob_sent)
        return oris_selected, nes_selected, X_selected, y_selected, yprob_selected, oris_remain, nes_remain, X_remain, y_remain, yprob_remain



