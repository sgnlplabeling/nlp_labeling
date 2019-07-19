소속 동아대학교 지능형 시스템 연구실

작성자 : 이승욱(seungwooklee76@gmail.com)

개발 :이승욱(SeungWook Lee, 석사과정), 고영중(YoungJoong Ko, 교수)

홈페이지 : http://islab631.github.io

E-Mail : seungwooklee76@gmail.com

본 프로그램은 동아대학교 지능형 시스템 연구실의 소중한 자산입니다.

본 프로그램을 이용한 어떠한 결과물일지라도 본 프로그램의 논문 혹은 주소가 참조되어야 합니다.

참조는 아래 논문 및 사이트를 참조하여 주시기 바랍니다.

논문 : Hongyeon Yu, Youngjoong Ko. "Expansion of Word Representation for Named Entity Recognition Based on Bidirectional LSTM CRFs." Journal of KIISE, 44.3 (2017.3): 306-313.

사이트 : https://github.com/sgnlplabeling/nlp_labeling

환경

Python version = 3.5 이상

allennlp 최신버전

pytorch 1.0 이상

CUDA = 9.0

CUDNN = 7.1.3

Numpy = 1.15.4

ELMo bidirectional LSTM CRFs Model
워드임베딩, ELMo 임베딩 추가자질로 사용

입력 형태

단어   품사태그 어절 순서   태그
서호프	NNP	1	B-PS
와	JC	1	O
파사노	NNP	2	B-PS
에게	JC	2	O
연속	NNG	3	O
안타	NNG	4	O
를	JKO	4	O
내주	VV	5	O
며	EC	5	O

평가시 출력 형태

단어          정답 태그  예측 태그
박주영/NNP	B-PS	B-PS
,/		O	O
보카/NNP	O	B-PS
주니어스/NNG	O	O
전/NNG		O	O
준비/NNG	O	O
돌입/NNG	O	O

######################################################################################################################################

Options
  -h, --help show this help message and exit

  -T TRAIN, --train=TRAIN (Train 데이터의 위치를 정해줍니다)

  -d DEV, --dev=DEV(Dev 데이터의 위치를 정해줍니다)

  -t TEST, --test=TEST(Test 데이터의 위치를 정해줍니다)

  --score=SCORE         score file location

  -s TAG_SCHEME, --tag_scheme=TAG_SCHEME(IOB 혹은 IOBES Tagging scheme을 선택합니다)

  -l LOWER, --lower=LOWER(영어를 모두 소문자로 정규화 음절단에선 적용되지 않음)

  -z ZEROS, --zeros=ZEROS(모든 숫자들을 0으로 정규화 시킵니다.)

  -g PLUS_TAG, --plus_tag=PLUS_TAG
   (1:word/tag, 0:word
    Ex) 1:서호프/NNP, 0:서호프)

  -c CHAR_DIM, --char_dim=CHAR_DIM
   (음절 단위 입력 차원 값)

  -C CHAR_EMB, --char_emb=CHAR_EMB(음절 임베딩 파일 경로.)

  --is_char_emb=IS_CHAR_EMB
    (0:랜덤 음절 임베딩을 사용, 1:pre trained 음절 임베딩을 사용)

  -q CHAR_LSTM_DIM, --char_lstm_dim=CHAR_LSTM_DIM
   (음절 단위 LSTM 차원 값)

  -b CHAR_BIDIRECT, --char_bidirect,
   (음절 단위 LSTM의 단방향, 양방향 결정 '0' = 단방향, '1' = 양방향)

  -w WORD_DIM, --word_dim=WORD_DIM
   (단어 단위 입력 차원 값)

  -W WORD_LSTM_DIM, --word_lstm_dim=WORD_LSTM_DIM
   (단어 단위 LSTM 차원 값)

  -B WORD_BIDIRECT, --word_bidirect,
   (단어 단위 LSTM의 단방향, 양방향 결정 '0' = 단방향, '1' = 양방향)

  -p PRE_EMB, --pre_emb=PRE_EMB
   (pre trained 단어 임베딩 위치)

  --is_pre_emb=IS_PRE_EMB
   (0:랜덤 단어 임베딩 사용, 1:pre trained 단어 임베딩 사용)

  -A ALL_EMB, --all_emb=ALL_EMB
   (Load all embeddings)

  -a CAP_DIM, --cap_dim=CAP_DIM
                        Capitalization feature dimension (0 to disable)

  -f CRF, --crf=CRF     Use CRF
   (0:CRF Layer 사용하지 않음, 1:CRF Layer 사용)

  -D DROPOUT, --dropout=DROPOUT
   (입력단에 Dropout Layer 적용 0=no Dropout)

  -r RELOAD, --reload=RELOAD
                        Reload the last saved model

  -P USE_GPU, --use_gpu=USE_GPU
   (0:GPU를 사용하지 않음, 1:GPU 사용)

  --loss=LOSS           loss file location
  --name=NAME           model name(Train 이후 최고 성능 모델의 이름 지정)
  -m MODE, --mode=MODE(Train을 원할시 Train mode 적용을 위해 1, 학습된 모델로 데이터 평가만을 원할 땐 0)
  -E ELMO_OPTION_FILE --elmo_option elmo option file 경로 지정
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
1. 입력으로 품사태그가 없을 경우 plus_tag의 값을 0으로 수정
2. 입력 데이터가 존재하지 않을 시 모델 작동하지 않음
3. ELMo를 사용하지만, option, weight 파일이 존재하지 않으면 실행 되지 않음

######################################################################################################################################
