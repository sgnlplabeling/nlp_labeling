from data_utils import  load_cluster, load_weight_matrix
from config import Config
from tagger import Tagger

config = Config

# config.word2cluster : K-Means 알고리즘을 사용하여 사전에 분류된 술어 군집 dict
# config.weight_matrix : weighted voting 에서 사용되는 각 weight_matrix
# config.label2idx, config.idx2label : 정답 dict
config.word2cluster = load_cluster()
config.weight_matrix, config.label2idx, config.idx2label = load_weight_matrix()


# 형태소분석된 raw_sentence에 PIC 처리
# input : config.result_input_path
# output : config.result_processed_path
print("iter : ", config.iter)
main_tagger_PIC = Tagger()
main_tagger_PIC.taggingPIC("result_tagging")

# PIC 처리된 raw_sentence에 AIC 적용
# input : config.result_processed_path
# output : config.result_output_path
main_tagger_AIC = Tagger()
main_tagger_AIC.evaluateAIC("result")
main_tagger_AIC.main_taggingAIC(mode="result_tagging")