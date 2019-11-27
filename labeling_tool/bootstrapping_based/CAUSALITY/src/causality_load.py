import pickle as pickle
import os.path
import causality_settings as st
class Loader(object) :
    def __init__(self, data_path, data_max_iter) :
        self.X_loaded = []
        self.y_loaded = []
        self.yprob_loaded = []
        if data_max_iter < 0:
            data_max_iter = len(os.walk(data_path).next()[2])
            st.START_ITER = data_max_iter-1
        else:
            data_max_iter += 1
        for i in range(0, data_max_iter) :
            if os.path.exists(data_path + str(i) +'.pkl') :
                with open(data_path + str(i) +'.pkl', 'rb') as input:
                    self.X_loaded += pickle.load(input)
                    self.y_loaded += pickle.load(input)
                    self.yprob_loaded += pickle.load(input)

    def get_X(self):
        return self.X_loaded
    def get_y(self):
        return self.y_loaded
    def get_yprob(self):
        return self.yprob_loaded


