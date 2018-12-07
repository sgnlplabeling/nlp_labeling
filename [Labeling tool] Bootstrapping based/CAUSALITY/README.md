소속 : 동아대학교 지능형 시스템 연구실

개발 : 유홍연(HongYeon Yu, 석사과정), 이승욱(SeungWook Lee, 석사과정), 고영중(YoungJoong, Ko, 교수)

홈페이지 : http://islab.donga.ac.kr

E-Mail : seungwooklee76@gmail.com

본 프로그램은 동아대학교 지능형 시스템 연구실의 소중한 자산입니다.

본 프로그램을 이용한 어떠한 결과물일지라도 본 프로그램의 논문 혹은 주소가 참조되어야 합니다.

참조는 아래 논문 및 사이트를 참조하여 주시기 바랍니다.

이승욱, 유홍연, 고영중 "학습 데이터 확장을 통한 딥러닝 기반 인과관계 추출 모델." 한글 및 한국어 정보처리 학술 대회, p61-66, 2018.

https://github.com/sgnlplabeling/nlp_labeling

개발 환경

Python : 3.5 이상

Python-crfsuite : 0.9.6

UNLABED DATA 입력 형태

단어  품사태그 어절 순서  태그

이 	MM 	1 	O

현상 	NNG 	2 	O

이 	JKS 	2 	O

계속되 	VV 	3 	O

면 	EC 	3 	O

반복되 	VV 	4 	O

는 	ETM 	4 	O

변형 	NNG 	5 	O

으로 	JKB 	5 	O

타이어 	NNG 	6 	O

가 	JKS 	6 	O

단시간 	NNG 	7 	O

에 	JKB 	7 	O

파열되 	VV 	8 	O

ㅂ니다 	EF 	8 	O

. 	SF 	8 	O

결과 출력 형태

단어            예측 태그

이/MM 		B-C

현상/NNG 	I-C

이/JKS 		I-C

계속되/VV 	I-C

면/EC 		I-C

반복되/VV 	B-E

는/ETM 		I-E

변형/NNG 	I-E

으로/JKB 	I-E

타이어/NNG 	I-E

가/JKS 		I-E

단시간/NNG 	I-E

에/JKB 		I-E

파열되/VV 	I-E

ㅂ니다/EF 	I-E

./SF 		I-E

######################################################################################################################################
실행 방법

1. causality_setting.py에서 Train, Test, Unlabeled 데이터의 경로와 여러 파라메터를 셋팅한다.
2. python3 main_model_train.py로 실행하여 학습을 진행한다.
3. 학습이 다 완료되면 python3 main_model_test.py 실행하여 평가한다.

