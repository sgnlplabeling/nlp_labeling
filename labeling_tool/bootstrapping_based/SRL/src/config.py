#-*- coding: utf-8 -*-

class Config():
    def __init__(self):
        pass

    iter = 1
    mode = "AIC_train"
    model = "AIC"

    # Crfsuite options
    c1 = 0.1
    c2 = 0.1
    maxiter = 100
    possible_transitions = True
    verbose = True

    # Predicate options
    V_PUMSA = ["VV", "VX", "VA", "VCN"]
    N_PUMSA = ["NNB", "NNG", "NNP", "NP"]

    # Bootstrapping options
    boot_iter = 2
    sample_num = str(500)
    confidence_socre = 0.8
    constraint_tag = 1
    model_num = 5

    modelPIC_path = "../data/PIC_model/PIC.crfsuite"
    labelPIC_path = "../data/utils/vocab/PIC_label2idx.txt"

    trainPIC_path = "../data/PIC_train/PIC_train.txt"
    testPIC_path = "../data/PIC_test/PIC_test.txt"

    testAIC_path = "../data/AIC_test/valid_corpus.txt"
    label_path = "../data/utils/vocab/label2idx.txt"

    cluter_path = "../data/utils/predicate_cluster.txt"
    regression_path = "../data/utils/regression.txt"

    main_corpus_AIC_path = "../data/AIC_train/main_model/main_model_%s.txt"
    main_model_AIC_path = "../data/AIC_model/main_model/main_model_%s.pysuite"

    unlabeled_corpus_path = "../data/unlabeled_corpus/smaple.txt"
    bagging_corpus_path = "../data/AIC_train/bagging_model/%s_iter/bagging_model_%s.txt"
    bagging_model_path= "../data/AIC_model/bagging_model/%s_iter/bagging_model_%s.pysuite"

    result_input_path = "../data/unlabeled_corpus/PIC_sample.txt"
    result_processed_path = "../data/result/input/PIC_result.txt"
    result_output_path = "../data/result/AIC/result.txt"
    result_model_path = "../data/result/model/result.pysuite"

    tagging_input_path = "../data/unlabeled_corpus/PIC_sample.txt"
    tagging_output_path = "../data/result/PIC/result.txt"
