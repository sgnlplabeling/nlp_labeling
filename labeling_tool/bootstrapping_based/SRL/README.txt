디렉토리/파일 설명

-src
	-config.py
	: 학습 변수 및 파일 경로 설정 파일
	
	-srl_main.py
	: main 파일
	
	-sogang_srl_predict.py
	: predict 전용 main 파일
	
	-data_utils.py
	: 데이터 전처리 및 utils
	
	-tagger.py
	: crfsuite model 학습 및 태깅과 관련된 파일
	
	-feature_func.py
	: 자질 추출 함수
	
-data
	-PIC_train
	: PIC 모델 학습셋 저장 경로
	
	-PIC_tset
	: PIC 모델 검증셋 저장 경로
	
	-PIC_model
	: PIC 모델 저장 경로
	
	-AIC_train
	: 부트스트래핑 과정에서 사용/생성되는 AIC 학습셋 저장 경로
		-main_model
		: main crf 모델에 사용되는 학습셋 저장 경로
		
		-bagging_model
		: 각 bagging 모델에 사용되는 학습셋 저장 경로
		: 매 iteration 마다 별도의 폴더 저장 
		
	-AIC_test
	: AIC 모델 검증셋 저장 경로
	
	-AIC_model
	: 부트스트래핑 과정에서 사용/생성되는 crf model 저장 경로
		-main_model
		: main crf 모델 저장 경로
		
		-bagging_model
		: 각 bagging 모델 저장 경로
		: 매 iteration 마다 별도의 폴더 저장 
		
	-utils
	: 각종 utils 파일 저장
	
주요 변수 설명
	-iter : 학습 iteration index (default=1)
	-model : ["AIC", "PIC"]
	-mode 
		-"AIC_predict" : 학습된 crf 모델을 사용하여 raw sentence를 태깅
		-"AIC_train" : 부트스트래핑 진행
		-"PIC_train" : PIC 모델 학습
		-"PIC_predict" : bootstrapping에 사용될 대용량 코퍼스를 생성하기 위해
						학습된 PIC 모델을 사용하여 raw sentence에 PIC 처리
	
	boot_iter = bootstrapping의 최대 iteration
    sample_num = bootstrapping시, unlabled data read하는 정도 , (default=5000)
	model_num = bootstrapping에 사용되는 bagging model의 갯수
    confidence_socre = bagging data로 추가되는 결과의 제약 조건, (default=0.9)
    constraint_tag = bagging data로 추가되는 결과의 제약 조건, (default=1)
	
	
	
※ 사용법

pip install -r requirements.txt

※ sogang_srl_predict.py 사용법
	python src/sogang_srl_predict.py
	
	- 프로그램 변수는 config.py에 설정되어 있습니다.


※ main.py 사용법

1)AIC_predict 
: 사전에 학습된 main crf 모델을 사용하여 raw sentence 태깅, config.py를 다음과 같이 설정
: iter=1, model = "AIC", mode = "AIC_predict",
  result_input_path = raw sentence 경로 (default="../data/unlabeled_corpus/smaple.txt"),
  result_output_path = 태깅 출력 경로 (default="../data/result/AIC/result.txt"),
  result_model_path = crfsuite 모델 경로 (default="")

2)AIC_train(bootstrapping)
: 특정 iteration부터 bootstrapping 학습 진행 (default=1), config.py를 다음과 같이 설정
: iter=1, model = "AIC", mode = "AIC_train",
 main_model_AIC_path = main crf model 경로, (default="../data/AIC_train/bagging_model/%s_iter/bagging_model_%s.txt")
 main_corpus_AIC_path = main crf model 학습 데이터 경로, (default="../data/AIC_model/bagging_model/%s_iter/bagging_model_%s.pysuite")
 
 bagging_model_path = 배깅 crf model 경로,(default="../data/AIC_model/bagging_model/%s_iter/bagging_model_%s.pysuite")
 bagging_corpus_path = 배깅 crf model 학습 데이터 경로,(default="../data/AIC_train/bagging_model/%s_iter/bagging_model_%s.txt")
 

3)PIC_training
: raw sentence에 PIC 적용, config.py를 다음과 같이 설정
: model = "PIC", mode = "PIC_train",
  trainPIC_path = train set (default="../data/PIC_train/PIC_train.txt")
  testPIC_path = test set (default="../data/PIC_test/PIC_test.txt")
  modelPIC_path = PIC crf model 경로 (default="../data/PIC_model/PIC.crfsuite")


4)PIC_tagging
: bootstrapping 학습에 사용될 대용량 코퍼스에 PIC를 태깅, config.py를 다음과 같이 설정
: model = "PIC", mode = "PIC_tagging",
  modelPIC_path = PIC crf model 경로 (default="../data/PIC_model/PIC.crfsuite")
  tagging_input_path = raw sentence 경로 (default="../data/unlabeled_corpus/PIC_sample.txt")
  tagging_output_path = PIC 태깅 후 결과 파일 경로 (default="../data/result/PIC/result.txt")
  
데이터 포멧 설명

- 모든 raw sentence는 1개 이상의 predicate를 갖고 있습니다. 아래 PIC 예제의 경우 "Pn"은 문장에서 predicate를 의미합니다.
 이때, predicate에 대한 argument를 찾기 위해, 각 predicate에 AIC crf model을 진행하여 AIC 예제와 같은 결과를 얻습니다.

PIC 예제)
	프랑스/NNP+의/JKG 르노/NNP 자동차/NNG 그룹/NNG+은/JX 다음주/NNG 김대중/NNP 대통령/NNG+의/JKG 프랑스/NNP 방문/NNG 중/NNB 한국/NNP 삼성자동차/NNP 인수/NNG+를/JKO 공식/NNG 제의하/VV+ㄹ지/EC 모르/VV+ㄴ다고/EC 르노사/NNP+의/JKG 한/MM 관계자/NNG+가/JKS 1/SN+일/NNB 밝히/VV+었/EP+다/EF+./SF|||O O O O O O O O O O O O O O P1 P1 O O O O P1

AIC 예제)
	14 P1 프랑스/NNP+의/JKG 르노/NNP 자동차/NNG 그룹/NNG+은/JX 다음주/NNG 김대중/NNP 대통령/NNG+의/JKG 프랑스/NNP 방문/NNG 중/NNB 한국/NNP 삼성자동차/NNP 인수/NNG+를/JKO 공식/NNG 제의하/VV+ㄹ지/EC 모르/VV+ㄴ다고/EC 르노사/NNP+의/JKG 한/MM 관계자/NNG+가/JKS 1/SN+일/NNB 밝히/VV+었/EP+다/EF+./SF|||O O O ARG0 ARGM-TMP O O O O ARGM-TMP O O ARG1 ARGM-MNR O O O O O O O
	15 P1 프랑스/NNP+의/JKG 르노/NNP 자동차/NNG 그룹/NNG+은/JX 다음주/NNG 김대중/NNP 대통령/NNG+의/JKG 프랑스/NNP 방문/NNG 중/NNB 한국/NNP 삼성자동차/NNP 인수/NNG+를/JKO 공식/NNG 제의하/VV+ㄹ지/EC 모르/VV+ㄴ다고/EC 르노사/NNP+의/JKG 한/MM 관계자/NNG+가/JKS 1/SN+일/NNB 밝히/VV+었/EP+다/EF+./SF|||O O O O O O O O O O O O O O ARG1 O O O O O O
	20 P1 프랑스/NNP+의/JKG 르노/NNP 자동차/NNG 그룹/NNG+은/JX 다음주/NNG 김대중/NNP 대통령/NNG+의/JKG 프랑스/NNP 방문/NNG 중/NNB 한국/NNP 삼성자동차/NNP 인수/NNG+를/JKO 공식/NNG 제의하/VV+ㄹ지/EC 모르/VV+ㄴ다고/EC 르노사/NNP+의/JKG 한/MM 관계자/NNG+가/JKS 1/SN+일/NNB 밝히/VV+었/EP+다/EF+./SF|||O O O O O O O O O O O O O O O ARG1 O O ARG0 ARGM-TMP O



담당자
- 박찬민 (서강대학교 자연어처리 연구실 석사과정)
- cksals302@gmail.com

