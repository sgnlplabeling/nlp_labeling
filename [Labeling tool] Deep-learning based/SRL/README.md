소속 동아대학교 지능형 시스템 연구실

작성자 : 윤정민(yjungmin2@gmail.com)

개발 : 윤정민(JeongMin Yoon, 석사과정), 이승욱(SeungWook Lee, 석사과정), 고영중(YoungJoong Ko, 교수)

홈페이지 : http://islab.donga.ac.kr/



본 프로그램은 동아대학교 지능형 시스템 연구실의 소중한 자산입니다.

본 프로그램을 이용한 어떠한 결과물일지라도 본 프로그램의 주소가 참조되어야 합니다.


참조 사이트 : https://github.com/sgnlplabeling/nlp_labeling


환경

Python version = 3.5 이상

pytorch 0.3.1

CUDA = 8.0

CUDNN = 7.1.3

Numpy = 1.15.4

학습시 입력 형태

입력 형태 순서 (현재어절 첫번째형태소, 현재어절 두번째형태소, 술어어절 첫번째형태소, 술어어절 두번째형태소, 정답태그)


그/NP             는/JX        남/VV         아/EC      O

김대중/NNP       <none!#>      남/VV         아/EC      O

정부/NNG          가/JKS       남/VV         아/EC      O

많/VA             은/ETM       남/VV         아/EC      O

것/NNB            을/JKO       남/VV         아/EC      O

하/VV             지만/EC      남/VV         아/EC   ARGM-DIS

아직/MAG          도/JX        남/VV         아/EC      O

하/VV             여야/EC      남/VV         아/EC      O

하/VX             ㄹ/ETM       남/VV         아/EC      O

일/NNG            이/JKS       남/VV         아/EC     ARG1

많이/MAG          <none!#>     남/VV         아/EC   ARGM-EXT

남/VV             아/EC        남/VV         아/EC      O

있/VX             다고/EC      남/VV         아/EC      AUX

강조하/VV          다/EF        남/VV         아/EC      O




평가시 출력 형태

출력 형태 순서 (현재어절 첫번째형태소, 현재어절 두번째형태소, 술어어절 첫번째형태소, 술어어절 두번째형태소, 정답태그, 예측태그)


그/NP             는/JX        남/VV         아/EC      O

김대중/NNP       <none!#>      남/VV         아/EC      O

정부/NNG          가/JKS       남/VV         아/EC      O

많/VA             은/ETM       남/VV         아/EC      O

것/NNB            을/JKO       남/VV         아/EC      O

하/VV             지만/EC      남/VV         아/EC   ARGM-DIS

아직/MAG          도/JX        남/VV         아/EC      O

하/VV             여야/EC      남/VV         아/EC      O

하/VX             ㄹ/ETM       남/VV         아/EC      O

일/NNG            이/JKS       남/VV         아/EC     ARG1

많이/MAG          <none!#>     남/VV         아/EC   ARGM-EXT

남/VV             아/EC        남/VV         아/EC      O

있/VX             다고/EC      남/VV         아/EC      AUX

강조하/VV          다/EF        남/VV         아/EC      O


bidirectional LSTM CRFs Model


##############################################################

Options


  -h, --help show this help message and exit


  -T TRAIN, --train=TRAIN (Train 데이터의 위치를 정해줍니다)


  -t TEST, --test=TEST (Test 데이터의 위치를 정해줍니다)


  --score=SCORE         score file location


  -l LOWER, --lower=LOWER (영어를 모두 소문자로 정규화 음절단에선 적용되지 않음)

   default = 1
 

  -z ZEROS, --zeros=ZEROS (모든 숫자들을 0으로 정규화 시킵니다.)

   default = 1


  -w WORD_DIM, --word_dim=WORD_DIM (단어 단위 입력 차원 값)

   default = 64
  


  -W WORD_LSTM_DIM, --word_lstm_dim=WORD_LSTM_DIM (LSTM hidden 차원 값)

   default = 64


  -p PRE_EMB, --pre_emb=PRE_EMB (pre trained 단어 임베딩 위치)


  --is_pre_emb=IS_PRE_EMB (0:랜덤 단어 임베딩 사용, 1:pre trained 단어 임베딩 사용)

   default = 0


  -f CRF, --crf=CRF     Use CRF (0:CRF Layer 사용하지 않음, 1:CRF Layer 사용)
  
   default = 1


  -D DROPOUT, --dropout=DROPOUT (입력단에 Dropout Layer 적용 0=no Dropout)

   default = 0.5


  -P USE_GPU, --use_gpu=USE_GPU (0:GPU를 사용하지 않음, 1:GPU 사용)

   default = 0


  --loss=LOSS           loss file location


  --name=NAME           model name(Train 이후 최고 성능 모델의 이름 지정)

##############################################################

*** 기본 파라미터로 Train Mode bi-LSTM-CRFs 실행 방법 ***

gpu 사용시

python3 train.py -T train_data_path -t test_data_path -P 1

gpu 미사용시

python3 train.py -T train_data_path -t test_data_path



*** 기본 파라미터에 pre trained 추가한 bi-LSTM-CRFs 실행 방법 ***

gpu 사용시

python3 train.py -T train_data_path -t test_data_path --is_pre_emb 1 -P 1 -p word_embedding_path

gpu 미사용시

python3 train.py -T train_data_path -t test_data_path --is_pre_emb 1 -p word_embedding_path


##############################################################

*** 주의사항 ***
1. 각 어절의 형태소는 특수문자를 제외한 의미있는 형태소만을 취함 (<none!#>은 패딩을 의미함)
2. 입력 데이터가 존재하지 않을 시 모델이 작동하지 않음
3. 평가 시 출력 경로 : evaluation/temp

