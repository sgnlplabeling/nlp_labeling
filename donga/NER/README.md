작성자 : 유홍연(hongyeon1408@gmail.com), 이승욱(seungwooklee76@gmail.com)

날짜 : 2018년 4월 2일 




환경

Python : 2.7.0

PyTorch : 0.3.0

Numpy : 1.14.0

SciPy : 1.0.0




bidirectional LSTM CRFs Model
음절 LSTM 임베딩, 워드임베딩, POS Onehot임베딩 추가자질로 사용


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

단어       정답태그   예측 태그

박주영/NNP  B-PS	   B-PS

,/         O        O

보카/NNP    O        B-PS

주니어스/NNG O        O

전/NNG      O        O

준비/NNG     O       O

돌입/NNG     O       O


######################################################################################################################################


Options

1  -h, --help show this help message and exit

2  -T TRAIN, --train=TRAIN (Train 데이터의 위치를 정해줍니다)

3  -d DEV, --dev=DEV(Dev 데이터의 위치를 정해줍니다)

4  -t TEST, --test=TEST(Test 데이터의 위치를 정해줍니다)

5  --score=SCORE         score file location

6  -s TAG_SCHEME, --tag_scheme=TAG_SCHEME(IOB 혹은 IOBES Tagging scheme을 선택합니다)

7  -l LOWER, --lower=LOWER(영어를 모두 소문자로 정규화 음절단에선 적용되지 않음)

8  -z ZEROS, --zeros=ZEROS(모든 숫자들을 0으로 정규화 시킵니다.)

9  -g PLUS_TAG, --plus_tag=PLUS_TAG

   (1:word/tag, 0:word
   
    Ex) 1:서호프/NNP, 0:서호프)

10  -c CHAR_DIM, --char_dim=CHAR_DIM
   
   (음절 단위 입력 차원 값)

11  -C CHAR_EMB, --char_emb=CHAR_EMB(음절 임베딩의 위치를 정해줍니다.)

12  --is_char_emb=IS_CHAR_EMB
    
    (0:랜덤 음절 임베딩을 사용, 1:pre trained 음절 임베딩을 사용)

13  -q CHAR_LSTM_DIM, --char_lstm_dim=CHAR_LSTM_DIM
   
   (음절 단위 LSTM 차원 값)

14  -w WORD_DIM, --word_dim=WORD_DIM
   
   (단어 단위 입력 차원 값)

15  -W WORD_LSTM_DIM, --word_lstm_dim=WORD_LSTM_DIM
   
   (단어 단위 LSTM 차원 값)

16  -p PRE_EMB, --pre_emb=PRE_EMB
   
   (pre trained 단어 임베딩 위치)

17  --is_pre_emb=IS_PRE_EMB
   
   (0:랜덤 단어 임베딩 사용, 1:pre trained 단어 임베딩 사용)

18  -A ALL_EMB, --all_emb=ALL_EMB
   
   (Load all embeddings)

19  -a CAP_DIM, --cap_dim=CAP_DIM
                        Capitalization feature dimension (0 to disable)

20  -f CRF, --crf=CRF     Use CRF
   
   (0:CRF Layer 사용하지 않음, 1:CRF Layer 사용)

21  -D DROPOUT, --dropout=DROPOUT
   
   (입력단에 Dropout Layer 적용 0=no Dropout)

22  -r RELOAD, --reload=RELOAD
                        Reload the last saved model

23  -P USE_GPU, --use_gpu=USE_GPU
   
   (0:GPU를 사용하지 않음, 1:GPU 사용)

24  --loss=LOSS           loss file location

25  --name=NAME           model name(Train 이후 최고 성능 모델의 이름 지정)

26  -m MODE, --mode=MODE(Train을 원할시 Train mode 적용을 위해 1, 학습된 모델로 데이터 평가만을 원할 땐 0)


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
3. 기존의 학습된 모델 대신 직접 학습한 모델을 사용시에는 test mode에서 저장된 모델을 적용하는 부분에서 경로를 확인하시기 바랍니다.

######################################################################################################################################
