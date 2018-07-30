"""
main.py
"""


import argparse
from gen_training import save_model
from parserTrain import YM_parser
from predict_main import predict
from voting_main import voting
from prepare_next_bagging import prepare
from sorting import sorting

if __name__ == '__main__':
    # PARSER = argparse.ArgumentParser()
    # PARSER.add_argument("-mode", required=True)
    # PARSER.add_argument("-train_path", required=False)
    # PARSER.add_argument("-test_path", required=False)
    # PARSER.add_argument("-output_path", required=False)
    # PARSER.add_argument("-bagging", required=True)
    # PARSER.add_argument("-g", default=0.98, type=float, required=False)
    # PARSER.add_argument("-a", default=0.94, type=float, required=False)
    # PARSER.add_argument("-scope", required=False)
    #
    # ARGS = PARSER.parse_args()
    # MODE = ARGS.mode
    # TRAIN_PATH = ARGS.train_path
    # TEST_PATH = ARGS.test_path
    # OUTPUT_PATH = ARGS.output_path
    # BAGGING_ITER = ARGS.bagging
    # G_SCORE = ARGS.g
    # A_SCORE = ARGS.a
    # SCOPE = ARGS.scope

    MODE = "g_predict"
    BAGGING_ITER = "1"
    # TEST_PATH = "../data/input_data/input.txt"
    TEST_PATH = "../data/input_data/input.txt"
    OUTPUT_PATH = "../data/"
    G_SCORE = "0.98"
    A_SCORE = "0.94"

    if MODE == 'train':
        if BAGGING_ITER == "0":
            # Data preprocess step
            save_model(bagging_iter=BAGGING_ITER, input_path=TRAIN_PATH)
            # MODEl train step
            YM_parser(BAGGING_ITER)
        else:
            prepare(bagging_iter=BAGGING_ITER, train_path=TRAIN_PATH, test_path=TEST_PATH,\
                    g_score=G_SCORE,
                    a_score=A_SCORE, scope=SCOPE, mode=MODE)
            # Data preprocess step
            save_model(bagging_iter=BAGGING_ITER, input_path=TRAIN_PATH)
            # MODEl train step
            YM_parser(BAGGING_ITER)

    elif MODE == 'predict':
        # Data predict step
        predict(bagging_iter=BAGGING_ITER, input_path=TEST_PATH, mode=MODE)
        # #Weighted voting & CKY
        voting(bagging_iter=BAGGING_ITER, mode=MODE)
        # Prepare next bagging
        prepare(bagging_iter=BAGGING_ITER, train_path=TRAIN_PATH, test_path=TEST_PATH,\
                g_score=G_SCORE, a_score=A_SCORE,
                scope=SCOPE, mode=MODE)

    elif MODE == 'g_predict':
        # Data predict step
        predict(bagging_iter=BAGGING_ITER, input_path=TEST_PATH, mode=MODE)
        # #Weighted voting & CKY
        voting(bagging_iter=BAGGING_ITER, mode=MODE)
        sorting(bagging_iter=BAGGING_ITER, output_path=OUTPUT_PATH, mode=MODE,\
                g_score=G_SCORE, a_score=A_SCORE)
				