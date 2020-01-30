소속 동아대학교 지능형 시스템 연구실

작성자 : 이승욱(seungwooklee76@gmail.com)

개발 :이승욱(SeungWook Lee, 석사과정), 고영중(YoungJoong Ko, 교수)

홈페이지 : http://islab631.github.io

E-Mail : seungwooklee76@gmail.com

위 이메일과 연락이 되지 않으실 땐 아래 보조 담당자에게 연락주시길 바랍니다.

보조 담당자 : 김기환(kimgihwan3364@gmail.com)

본 프로그램은 동아대학교 지능형 시스템 연구실의 소중한 자산입니다.

본 프로그램을 이용한 어떠한 결과물일지라도 본 프로그램의 논문 혹은 주소가 참조되어야 합니다.

참조는 아래 논문 및 사이트를 참조하여 주시기 바랍니다.

논문 : 이승욱, 유홍연, 고영중 "학습 데이터 확장을 통한 딥러닝 기반 인과관계 추출 모델." 한글 및 한국어 정보처리 학술 대회, p61-66, 2018.

사이트 : https://github.com/sgnlplabeling/nlp_labeling

환경

Python version = 3.5 이상

pytorch 1.0 이상

allennlp 최신버전

CUDA = 9.0

CUDNN = 7.1.3

Numpy = 1.15.4

학습시 입력 형태

단어 품사태그 어절 순서 태그

이 MM 1 B-C

현상 NNG 2 I-C

이 JKS 2 I-C

계속되 VV 3 I-C

면 EC 3 I-C

반복되 VV 4 B-E

는 ETM 4 I-E

변형 NNG 5 I-E

으로 JKB 5 I-E

타이어 NNG 6 I-E

가 JKS 6 I-E

단시간 NNG 7 I-E

에 JKB 7 I-E

파열되 VV 8 I-E

ㅂ니다 EF 8 I-E

. SF 8 I-E

평가시 입력형태

단어 품사태그 어절 순서 태그

이 MM 1 O

현상 NNG 2 O

이 JKS 2 O

계속되 VV 3 O

면 EC 3 O

반복되 VV 4 O

는 ETM 4 O

변형 NNG 5 O

으로 JKB 5 O

타이어 NNG 6 O

가 JKS 6 O

단시간 NNG 7 O

에 JKB 7 O

파열되 VV 8 O

ㅂ니다 EF 8 O

. SF 8 O

평가시 출력 형태

단어 예측 태그

이/MM B-C

현상/NNG I-C

이/JKS I-C

계속되/VV I-C

면/EC I-C

반복되/VV B-E

는/ETM I-E

변형/NNG I-E

으로/JKB I-E

타이어/NNG I-E

가/JKS I-E

단시간/NNG I-E

에/JKB I-E

파열되/VV I-E

ㅂ니다/EF I-E

./SF I-E

bidirectional LSTM CRFs Model

워드임베딩

############################################################################################################################ ##########

Options

-h, --help show this help message and exit

-T TRAIN, --train=TRAIN (Train 데이터의 위치를 정해줍니다)

-t TEST, --test=TEST(Test 데이터의 위치를 정해줍니다)

--score=SCORE score file location

-s TAG_SCHEME, --tag_scheme=TAG_SCHEME(IOB 혹은 IOBES Tagging scheme을 선택합니다)

-l LOWER, --lower=LOWER(영어를 모두 소문자로 정규화 음절단에선 적용되지 않음)

-z ZEROS, --zeros=ZEROS(모든 숫자들을 0으로 정규화 시킵니다.)

-g PLUS_TAG, --plus_tag=PLUS_TAG (1:word/tag, 0:word Ex) 1:서호프/NNP, 0:서호프)

-w WORD_DIM, --word_dim=WORD_DIM (단어 단위 입력 차원 값)

-W WORD_LSTM_DIM, --word_lstm_dim=WORD_LSTM_DIM (단어 단위 LSTM 차원 값)

-p PRE_EMB, --pre_emb=PRE_EMB (pre trained 단어 임베딩 위치)

--is_pre_emb=IS_PRE_EMB (0:랜덤 단어 임베딩 사용, 1:pre trained 단어 임베딩 사용)

-A ALL_EMB, --all_emb=ALL_EMB (Load all embeddings)

-a CAP_DIM, --cap_dim=CAP_DIM Capitalization feature dimension (0 to disable)

-f CRF, --crf=CRF Use CRF (0:CRF Layer 사용하지 않음, 1:CRF Layer 사용)

-D DROPOUT, --dropout=DROPOUT (입력단에 Dropout Layer 적용 0=no Dropout)

-r RELOAD, --reload=RELOAD Reload the last saved model

-P USE_GPU, --use_gpu=USE_GPU (0:GPU를 사용하지 않음, 1:GPU 사용)

--loss=LOSS loss file location --name=NAME model name(Train 이후 최고 성능 모델의 이름 지정) 

-m MODE, --mode=MODE(Train을 원할시 Train mode 적용을 위해 1, 학습된 모델로 데이터 평가만을 원할 땐 0)

-E ELMO_OPTOIN_FILE --elmo_option elmo option file 경로 지정

-H ELMO_WEIGHT_FILE --elmo_weight elmo weight file 경로 지정

-e USE_ELMO --use_elmo
(ELMo를 사용할지 말지 결정 '0' ELMo 사용하지 않음, '1' ELMo 사용)
######################################################################################################################################

*** 기본 파라미터로 Train Mode bi-LSTM-CRFs 실행 방법 ***

train.py 파일을 python으로 실행하면서 파라미터로 train, dev, test 입력과 Train Mode 선택

gpu 사용시

python train.py -m 1 -T train_data_path -d dev_data_path -t test_data_path --is_char_emb 0 --is_pre_emb 0 -P 1

gpu 미사용시

python train.py -m 1 -T train_data_path -d dev_data_path -t test_data_path --is_char_emb 0 --is_pre_emb 0 -P 0

***기본 파라미터로 Test Mode bi-LSTM-CRFs 실행 방법 ***

gpu 사용시

python train.py -m 0 -T train_data_path -d dev_data_path -t test_data_path --is_char_emb 0 --is_pre_emb 0 -P 1

gpu 미사용시

python train.py -m 0 -T train_data_path -d dev_data_path -t test_data_path --is_char_emb 0 --is_pre_emb 0 -P 0

*** 기본 파라미터에 pre trained 추가한 bi-LSTM-CRFs 실행 방법 ***

gpu 사용시

python train.py -T train_data_path -d dev_data_path -t test_data_path -p word_embedding_path -C Character_embedding_path -P 1

gpu 미사용시

python train.py -T train_data_path -d dev_data_path -t test_data_path -p word_embedding_path -C Character_embedding_path -P 0

*** 기본 파라미터로 Train Mode bi-LSTM 실행 방법 ***

train.py 파일을 python으로 실행하면서 파라미터로 train, dev, test 입력과 Train Mode 선택

gpu 사용시

python train.py -m 1 -T train_data_path -d dev_data_path -t test_data_path --is_char_emb 0 --is_pre_emb 0 -P 1 -f 0

gpu 미사용시

python train.py -m 1 -T train_data_path -d dev_data_path -t test_data_path --is_char_emb 0 --is_pre_emb 0 -P 0 -f 0

######################################################################################################################################

*** 주의사항 ***

입력으로 품사태그가 없을 경우 plus_tag의 값을 0으로 수정

입력 데이터가 존재하지 않을 시 모델 작동하지 않음

평가시 출력 경로는 evaluation/temp

ELMo를 사용하지만, option, weight 파일이 존재하지 않으면 모델 실행되지 않음

######################################################################################################################################
