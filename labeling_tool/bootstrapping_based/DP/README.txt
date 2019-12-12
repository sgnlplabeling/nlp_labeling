<모델 소개>
	본 의존 파싱 모델은 Feed Forward Neural Network기반의 Trainstion Parser입니다.
	학습 데이터를 10개로 분할해서 10개의 서로 다른 모델을 학습하는 Bagging 기법을 사용하였습니다.
	각 bagging 결과를 Voting하였고 arc의 weight를 통해 CKY 알고리즘을 사용하였습니다.
	마지막으로 CKY 알고리즘으로 계산된 문장 내 각 arc의 평균 weight를 의존 파싱 결과의 score로 사용합니다.
	
	매 bagging iteration마다 의존 파싱 결과를 g_socre와 a_socre를 기준으로 분리합니다.
	사용자는 g_score와 a_socre를 기준으로 분리된 의존 파싱 결과(g_result.txt, a_result.txt, b_result.txt) 중 원하는 파싱 결과를 선택 할 수 있고
	선택된 결과 파일은 다음 bagging시 학습데이터에 추가되는 동시에 다음 bagging에서 사용될 test data에서 제거됩니다. 

	위와 같은 bootstrapping을 중단하고 초기 학습 데이터(../data/input_data/test_data)에 지금까지 학습된 모델로
	의존 파싱을 진행 하고 싶을 경우 "g_predict" 옵션으로 프로그램을 실행합니다.


<실행방법>
	최초 실행시, g_socre : 0.99, a_score 0.95
	> python Dependency_main.py -train_path ../data/input_data/training_data -mode train -bagging 0
	> python Dependency_main.py -test_path ../data/input_data/test_data -mode predict -bagging 0 -g 0.99 -a 0.95
	
	n번째 bagging 진행시 (학습), 이전 bagging에서 생성된 a grade를 부트스트래핑 (default = ..data/trainning_data/%sth_in)
	> python Dependency_main.py -train_path 폴더경로 -mode train -bagging n -scope a 혹은
	> python Dependency_main.py -train_path default -mode train -bagging n -scope a
	
	n번째 bagging 진행시, (파싱) g_score와 a_score를 지정하여 "graded_result.txt" 생성
	(default = ../data/test_data/%sth_test_data)
	> python Dependency_main.py -test_path 폴더경로 -mode predict -bagging n -g 0.99 -a 0.95 혹은
	> python Dependency_main.py -test_path default -mode predict -bagging n -g 0.99 -a 0.95
	
	※현재까지 학습된 n번째 모델을 사용하여 전체 데이터를 파싱 할 경우
	> python Dependency_main.py -test_path 폴더경로 -bagging n -mode g_predict -output_path 폴더경로 혹은
	> python Dependency_main.py -test_path default -bagging n -mode g_predict -output_path 폴더경로
	
	※ n번째 bagging 진행시 default 대신 경로를 직접 입력해주어도 됩니다.
	
	※현재 train epoch은 1로 설정되어 있습니다. config.py 에서 num_epochs를 변경하실 수 있습니다. (default = 30)
	
	※n번째 bagging 진행시, 의존 구문 파싱결과가 "a"(이어쓰기)되는 프로그램 특성상
	 ../data/tmp_data/%sth_tmp_data/before_voting 폴더에 파일이 저장되어 있으면 오류가 발생 할 수 있습니다.


<데이터 소개>
	train data로 사용되는 세종 코퍼스 + active learning 코퍼스(218문장)은 다음 경로에 있습니다. (구분자:"\n\n")
	../data/input_data/train
	
	test data로 사용되는 의존 구문 데이터의 형식은 다음 파일과 같습니다. (구분자:"\n\n")
	../data/input_data/test_data
	
	※/home/sogang/shared/Dependency/result 폴더에 의존 파싱된 대용량 데이터가 있습니다.
	
	※현재 ../data/input_data/test_data 경로에는 저용량의 toy data가 저장되어 있습니다.
	대용량 뉴스 코퍼스는 /home/sogang/shared/Dependency/tmp 폴더에 총 10개 파일로 분할 저장되어 있습니다.


<옵션 설명>
- train_path
	- 학습시 사용 할 training data의 폴더 경로입니다.
	"default"를 입력으로 사용하면 현재 bagging_iter에 알맞은 training 폴더로 설정됩니다.
	단, 0번째 bagging 시작시 폴더 경로를 필수적으로 입력해주어야 합니다 ex) ../data/input_data/training_data

- test_path
	- predict시 사용 할 data의 폴더 경로입니다.
	"default"를 입력으로 사용하면 현재 bagging_iter에 알맞은 test 폴더로 설정됩니다.
	단, 0번째 bagging 시작시 폴더 경로를 필수적으로 입력해주어야 합니다 ex) ../data/input_data/test_data

- bagging
	- 현재 bagging iteration의 num입니다. 초기 값은 0입니다.

- mode 
	- 프로그램의 mode 옵션이며 "train","predict","g_predict"가 존재합니다.
		-train : 일반적인 bagging 옵션입니다. 
		training data와 test data를 입력으로 모델 학습을 진행합니다.
		인자로 bootstrapping에 사용될 파일을 인자로("g", "a", "b") 받습니다.
		학습 모델은 "../data/f_model"과 "../data/ckpt"에 저장됩니다.
		
		-predict : train에서 학습된 모델로 의존 파싱을 시작합니다.
		총 10개의 모델로 배깅이 진행되며 결과는 "../data/tmp_data/%sth_tmp_data/"에 저장됩니다.
		인자로 g_score와 a_socre를 받아 이를 기준으로 "graded_result.txt"를 생성합니다.
	
		-g_predict : 현재까지 학습된 model로 초기 테스트 데이터(../data/input_data/test_data)에 대한 의존 파싱을 시작합니다.
		파싱 결과는 ../data/g_data/%sth_final_data 에 저장됩니다.

- g :
	- bootstrapping시 기준이 되는 g_score값입니다.

- a : 
	- bootstrapping시 기준이 되는 a_score값입니다.

- scope : 
	- 다음 부트스트래핑세 사용 할 폴더의 이름입니다.
	g_score와 a_score를 기준으로 생성된 "g_result.txt", "a_result.txt", "b_result.txt" 파일 중 사용자가 사용 할 파일을 선택합니다.
	Active learning을 진행 할 경우, Active learning이 완료된 파일을 인자로 넣어주면 됩니다.
	(기본 경로 : ../data/tmp_data/%sth_gab_data)
	
<폴더 설명>
-src : python 소스코드입니다.


-data : 입출력 데이터 및 모델
	- ckpt : MLP 학습 가중치 저장 파일(tensorflow checkpoint file)

	- f_model : 의존 파서 자질 추출 모델 폴더

	- input_data : bagging에 필요한 학습데이터/테스트데이터
		- training_data : 학습데이터 , 0번째 bagging시에만 사용
		- test_data : 테스트데이터, 0번째 bagging시, g옵션시 사용되는 전체 테스트 데이터이므로 삭제하면 안됩니다.

	- log : 
		- MLP 가중치 학습시, 세종기획 Test 데이터에 대한 성능 기록 
	
	- raw_data : 
		- training_data : 세종 기획 Train 데이터 + 액티브 데이터(218문장)
		- valid_data : 세종 기획 Test 데이터

	- tmp_data :
		
		- %s_g_tmp_data :
			- "g" 옵션으로 출력되는 결과의 임시 폴더입니다.
		- %sth_tmp_data :
			- before_voting : %s번째 bagging 모델의 출력결과, voting 전
			- after_voting : %s번째 bagging 모델의 출력결과, voting 후
		- %sth_gab_data :
			- %s번째 bagging 후, socre "g", "a", "b"를 단위로 파싱 결과를 저장
		
	- training_data :
		- %sth_out: %s번째 학습에 사용 할 데이터, 전처리 후
		- %sth_in : %s번째 학습에 사용 할 데이터, 전처리 전 

	- g_data :
		- 더 이상 bootstrapping을 진행하지 않고
		 전체 테스트 데이터에 대해 의존 구문 파싱을 진행한 결과가 저장되는 폴더입니다.
