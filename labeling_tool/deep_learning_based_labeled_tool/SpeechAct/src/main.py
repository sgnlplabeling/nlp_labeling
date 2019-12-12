import os
import sys
import getopt
import shutil
import logging
import data_helper
import numpy as np
import tensorflow as tf
from text_cnn_rnn import TextCNNRNN
import train
import predict

from sklearn.model_selection import train_test_split, KFold

logging.getLogger().setLevel(logging.INFO)

# Create a directory, everything related to the training will be saved in this directory

def main_func(argv):
    in_file = ''
    out_dir = ''

    try:
        opts, args = getopt.getopt(argv, "h:i:o:", ["in_filepath=", "out_dir="])
    except getopt.GetoptError:
        print("python main.py -i <in_filepath> -o <out_dir>")
        sys.exit(2)

    for opt, arg in opts:
        if opt == '-h':
            print("python main.py -i <in_filepath> -o <out_dir>")
            sys.exit()
        elif opt in ("-i", "--in_filepath"):
            in_file = arg
        elif opt in ("-o", "--out_dir"):
            out_dir = arg

    if out_dir == '':
        out_dir = './trained_results/'
    if not out_dir.endswith('/'):
        out_dir += '/'
    if os.path.exists(out_dir):
        shutil.rmtree(out_dir)
    os.makedirs(out_dir)

    # x_, y_ is planning and booking system data set
    # new_x, new_y is chatting system data set
    x_, y_, pre_y_, vocabulary, embedding_mat, pre_y_dict, labels, new_x, new_y, new_pre_y = data_helper.load_data(in_file, out_dir)

    embedding_pre = [pre_y_dict[y] for y in pre_y_dict.keys()]
    embedding_pre = np.array(embedding_pre, dtype=np.float32)

    # split data
    x, x_dev, y, y_dev, pre_y, pre_y_dev = train_test_split(x_, y_, pre_y_, test_size=0.2)
    x_train, x_test, y_train, y_test, pre_y_train, pre_y_test = train_test_split(x, y, pre_y, test_size=0.08)

    # add new_data to train data
    x_train = np.r_[x_train, new_x]
    y_train = np.r_[y_train, new_y]
    pre_y_train = np.r_[pre_y_train, new_pre_y]

    logging.info('x_train: {}, x_dev: {}, x_test: {}'.format(len(x_train), len(x_dev), len(x_test)))
    logging.info('y_train: {}, y_dev: {}, y_test: {}'.format(len(y_train), len(y_dev), len(y_test)))

    train.train_cnn_rnn(embedding_mat, embedding_pre, x_train, x_dev, y_train, y_dev, pre_y_train, pre_y_dev, labels, vocabulary, out_dir)
    predict_labels, accuracy = predict.predict_cnn_rnn(x_test, y_test, pre_y_test, out_dir)

    print('accuracy', accuracy)
if __name__=='__main__':
    main_func(sys.argv[1:])