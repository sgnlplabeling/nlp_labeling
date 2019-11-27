import cPickle as pickle
import os.path
class Loader(object) :
    def __init__(self, data_path, data_max_iter, active_data_save_path, active_data_max_name) :
        self.X_loaded = []
        self.y_loaded = []
        self.yprob_loaded = []
        self.X_bf_active = []
        self.y_bf_active = []
        for i in range(0, data_max_iter + 1) :
            if os.path.exists(data_path + str(i) +'.pkl') :
                with open(data_path + str(i) +'.pkl', 'rb') as input:
                    self.X_loaded += pickle.load(input)
                    self.y_loaded += pickle.load(input)
                    self.yprob_loaded += pickle.load(input)
        if active_data_max_name!= None :
            act_boot_iter_str = active_data_max_name.split('_')[0]
            act_put_count = int(active_data_max_name.split('_')[1].split('.')[0])
            for i in range(act_put_count+1) :
                if os.path.exists(active_data_save_path+ act_boot_iter_str + '_'+ str(i)+'.pkl'):
                    with open(active_data_save_path+ act_boot_iter_str + '_'+ str(i)+'.pkl', 'rb') as input:
                        self.X_bf_active += pickle.load(input)
                        self.y_bf_active += pickle.load(input)
    def get_X(self):
        return self.X_loaded
    def get_y(self):
        return self.y_loaded
    def get_yprob(self):
        return self.yprob_loaded


