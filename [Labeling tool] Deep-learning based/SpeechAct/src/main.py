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
from sklearn.model_selection import train_test_split

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
    x_, y_, vocabulary, embedding_mat, labels, new_x, new_y = data_helper.load_data(in_file, out_dir)

    # split data
    x, x_test, y, y_test = train_test_split(x_, y_, test_size=0.1)
    x_train, x_dev, y_train, y_dev = train_test_split(x, y,test_size=0.2)

    # add new_data to train data

    x_train = np.r_[x_train, new_x]
    y_train = np.r_[y_train, new_y]

    logging.info('x_train: {}, x_dev: {}, x_test: {}'.format(len(x_train), len(x_dev), len(x_test)))
    logging.info('y_train: {}, y_dev: {}, y_test: {}'.format(len(y_train), len(y_dev), len(y_test)))

    train.train_cnn_rnn(embedding_mat, x_train, x_dev, y_train, y_dev, labels, vocabulary, out_dir)
    predict_labels, accuracy = predict.predict_cnn_rnn(x_test, y_test, out_dir)

    print('accuracy', accuracy)

if __name__=='__main__':
    main_func(sys.argv[1:])