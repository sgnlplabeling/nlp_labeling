<실행방법>
src 디렉토리에서 아래 명령 입력
명령) python main.py [부트스트래핑 이터레이션 번호] [옵션]
- [부트스트래핑 이터레이션 번호] 
	* 0 부터 시작, 즉 첫 부트스트래핑 이터레이션을 실행하고자 할 때 0을 입력해야함.
	* 반드시 입력해야 함.
	* i 번째 부스트스래핑 이터레이션 일 경우, unlabeled raw data 전체 중 2500*(i) 번째 문장부터, 2500*(i+1) 번째 문장 을 대상으로, 손으로 수정할만 한 active data 와 바로 다음 i+1번째 부트스트래핑 이터레이션에 추가할만 한 machine labeled good data 를 생성(output 디렉토리)
- [옵션]
	* -s : save model, 모델 저장, 학습시킨 CRF 모델을 지우지 않고 models 디렉토리 안에 저장, 자세한 모델 경로는 stdout으로 출력됨
	* -g : genterate, full machine-labeled data 생성, input 디렉토리 내 unlabeled raw data 디렉토리 안에 있는 모든 데이터 읽어서, 해당 부트스트래핑 이터레이션 때 학습시킨 모델을 사용, machine-labeled data 생성 (output 디렉토리 내 full_data 디렉토리)
- 명령 예시
	ex1) python main.py 32 -s -g
	ex2) python main.py 0

<디렉토리 및 파일 설명>
- src : 소스코드
	* main.py : 메인
	* ner_setting : CRF iteration, 부트스트래핑 사이즈, 배깅의 컴포넌트 모델 갯수 등 hyper parameters 변경 가능
- input : 프로그램 실행시, 입력으로 들어가는 파일들이 있는 디렉토리
	- unlabeled_raw_data : 
          프로그램 실행시, 이 디렉토리에 있는 모든 파일을 읽어서 unlabeled raw data로 사용. 부트스트래핑이 모두 끝날 때 까지 (부트스트래핑 이터레이션 0번째, 1번째, 2번째, ...., N번째 -종료, 종료될 때 까지!) 부트스트래핑 중 unlabeled raw data가 바뀌면 안되기 때문에, 
          부트스트래핑 중 이 디렉토리의 파일 수, 파일 이름 등이 바뀌면 안됨. 
	- original_labeled_data :
	  프로그램 실행시, 이 디렉토리에 있는 모든 파일을 읽어서 CRF 학습에 사용되는 초기 labeled data로 사용 (active data나 machine labeled data가 아닌 golden data). 
	  부트스트래핑이 모두 끝날 때 까지 부트스트래핑 중 golden data가 바뀌면 안되기 때문에, 
          부트스트래핑 중 이 디렉토리의 파일 수, 파일 이름 등이 바뀌면 안됨. 
	  * added_sentence_expo_train_sgedit.txt : 국어처리 경진대회 train data(수정됨)
	- optional_test_data : 
	  모델 성능을 평가할 수 있는 데이터, 현재 모델 성능 평가 기능은 off 되어있음(ner_settings.py에서 ALL_TEST를 True 로 변경하면 모델 성능 평가가 됨)
	  모델 성능 평가 기능을 on 하고, 프로그램 실행시, 이 디렉토리에 있는 모든 파일을 읽어서 test data로 사용
	  * added_sentence_expo_dev_sgedit.txt : 국어처리 경진대회 development data(수정됨)
	- machine_labeled_data :
	  CRF 학습에 사용될 machine labeled train data, 프로그램 실행시, 이 디렉토리에 있는 모든 파일을 읽어서 CRF 학습에 사용
	  예를 들어 3번 부트스트래핑 이터레이션을 실행하고 싶을때에는, 앞서 0번, 1번, 2번 부트스트래핑 이터레이션 결과로 생성된  machine labeled data를 train 에 사용해야하기 때문에, 
	  앞서 0번, 1번, 2번 부트스트래핑 이터레이션 결과로 생성된  machine labeled data 파일들(예, 0_good.txt, 1_good.txt, 2_good.txt)이 이 디렉토리에 있어야 함.
	- active_data :
	  CRF 학습에 사용될 손으로 수정된 active data, 프로그램 실행시, 이 디렉토리에 있는 모든 파일을 읽어서 CRF 학습에 사용
	  예를 들어 3번 부트스트래핑 이터레이션을 실행하고 싶을때에는, 앞서 0번, 1번, 2번 부트스트래핑 이터레이션 결과로 생성된  machine labeled active data를 사용자가 수정한 data를 train 에 사용해야하기 때문에, 
	  앞서 0번, 1번, 2번 부트스트래핑 이터레이션 결과로 생성된  machine labeled data 파일들(예, 0_active.txt, 1_active.txt, 2_active.txt)을 사용자가 수정한(예, 0_active_mod.txt, 1_active_mod.txt, 2_active_mod.txt)가 이 디렉토리에 있어야 함.
- output : 프로그램 실행시 생성된 output 파일들이 있는 디렉토리
	- machine_labeled_good_data :
	  각 부트스트래핑 이터레이션 하나가 종료 될 때 마다 생성되는, 신뢰도가 높은 machine labeled data 파일이 저장되는 디렉토리. 
	  생성된 machine labeled data 를 다음 부트스트래핑 이터레이션에 학습데이터로 사용하기 위해서는 해당 파일을 input/machine_labeled_data/ 디렉토리로 이동시키고, 그 다음 부트스트래핑 이터레이션을 실행해야함 (python main.py [다음 부트스트래핑 이터레이션 번호] [옵션])
	- active_data : 
	  각 부트스트래핑 이터레이션 하나가 종료 될 때 마다 생성되는, ambiguous한 machine labeled data 파일이 저장되는 디렉토리. 
	  생성된 ambiguous machine labeled data 를 다음 부트스트래핑 이터레이션에 학습데이터로 사용하기 위해서는, 사용자가 직접 해당 파일을 수정하게 하도록 한 뒤, 
	  수정된 파일을 input/active_data/ 디렉토리에 저장, 그 다음 부트스트래핑 이터레이션을 실행해야함 (python main.py [다음 부트스트래핑 이터레이션 번호] [옵션])
	- full_data : 
	  '-g' 옵션을 주고, 프로그램을 실행하였을 때 생성되는, 전체 unlabeled raw data에 대해 모델이 생성한 machine-labeled data가 저장되는 디렉토리
	  *active_[모델번호].txt : [모델번호]에 해당하는 모델이 학습될 때 사용된, 사용자가 직접 수정한 active data만 별도로 출력한 파일.
	  *machine_[모델번호].txt : 사용자가 직접 수정한 active data를 제외하고, 모델이 생성한 machine-labeled data가 
	  *actNmachine_[모델번호].txt : 전체 unlabeled raw data에 대해 모델이 생성한 machine-labeled data, 만일 사용자가 직접 수정한 적이 있는 문장일 경우, 사용자가 입력했던 레이블로 출력
- output : 모델 학습중 일시적으로 모델이 생기고 지워지는 디렉토리, '-s' 옵션이 있을경우 기본 모델이 지워지지 않고 남음
	
<out 파일 양식>
- 기본적으로, 이미 배포된 예시 파일의 양식과 동일하지만 output의 경우 5열(주변확률)이 추가됨. input 의 경우 5열(주변확률)이 있든 없든 상관 없음.
;2007년 루슨트 테크놀로지의 시스템 소프트웨어 연구부장으로 은퇴했다.     <-- 원본 문장
2007 SN 0 B-DT 1.0     <-- 5열의 경우 해당 태그 (B-DT)의 주변 확률이다. 만일 사용자가 직접 입력한 태그일 경우 확률은 1.0으로 출력된다.

<std out>
- 프로그램 종료시, summary로 생성된 데이터 혹은 저장된 모델의 경로를 출력함.
