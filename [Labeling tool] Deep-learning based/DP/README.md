소속 서강대학교 자연어처리 연구실

작성자 : 박찬민(cksals302@gmail.com)

개발 : 박찬민(cksals302@gmail.com, 석사과정)

관리자 : 김주애(jju75474@gmail.com, 박사과정)

본 프로그램은 서강대학교 자연어처리 연구실의 소중한 자산입니다.

본 프로그램을 이용한 모든 결과물은 본 프로그램의 주소가 참조되어야 합니다.

참조 사이트 : https://github.com/sgnlplabeling/nlp_labeling

개발 환경 (src/requirements.txt 참조)


Pyhton==3.5.6

tensorflow_gpu==1.13.0rc1

numpy==1.15.1

tensorflow==1.14.0

typing==3.7.4



*** 예시 문장 ***
 
 그러나 수천 수만의 모략꾼, 협잡꾼, 사기꾼을 상대해야 하는 정치인이 정직하기란 심히 어려운 일일 것이다.
 
 ->
 
의존소 index // 지배소 index // 의존관계명 // 형태소 분석된 입력 어절
 
 ※ 학습 시 (../data/corpus/smaple_train.txt)

 ; 그러나 수천 수만의 모략꾼, 협잡꾼, 사기꾼을 상대해야 하는 정치인이 정직하기란 심히 어려운 일일 것이다.
 
1	12	AP	수천/NR

2	3	NP	수만/NR|의/JKG

3	6	NP	모략/NNG|꾼/XSN|,/SP

4	6	NP_CNJ	협잡/NNG|꾼/XSN|,/SP

5	9	NP_CNJ	사기/NNG|꾼/XSN|을/JKO

6	7	NP	상대/NNG|하/XSV|아야/EC

7	8	VP	하/VX|는/ETM

8	9	VP	정치인/NNG|이/JKS

9	10	NP	정직/NNG|하/XSA|기/ETN|란/JX

10	12	VP_SBJ	심히/MAG

11	12	AP	어렵/VA|ㄴ/ETM

12	13	VP	일/NNG|이/VCP|ㄹ/ETM

13	14	NP	것/NNB|이/VCP|다/EF|./SF


 
 ※ 태깅 시 (../data/corpus/smaple_test.txt)
 
; 그러나 수천 수만의 모략꾼, 협잡꾼, 사기꾼을 상대해야 하는 정치인이 정직하기란 심히 어려운 일일 것이다.
1	0	$UNK$		그러나[MAJ]그러나/MAJ

2	0	$UNK$		수천[NR]수천/NR

3	0	$UNK$		수만[NR]|의[JKG]수만/NR|의/JKG

4	0	$UNK$		모략[NNG]|꾼[XSN]|,[SP]모략/NNG|꾼/XSN|,/SP

5	0	$UNK$		협잡[NNG]|꾼[XSN]|,[SP]협잡/NNG|꾼/XSN|,/SP

6	0	$UNK$		사기[NNG]|꾼[XSN]|을[JKO]사기/NNG|꾼/XSN|을/JKO

7	0	$UNK$		상대[NNG]|하[XSV]|아야[EC]상대/NNG|하/XSV|아야/EC

8	0	$UNK$		하[VX]|는[ETM]하/VX|는/ETM

9	0	$UNK$		정치인[NNG]|이[JKS]정치인/NNG|이/JKS

10	0	$UNK$		정직[NNG]|하[XSA]|기[ETN]|란[JX]정직/NNG|하/XSA|기/ETN|란/JX

11	0	$UNK$		심히[MAG]심히/MAG

12	0	$UNK$		어렵[VA]|ㄴ[ETM]어렵/VA|ㄴ/ETM

13	0	$UNK$		일[NNG]|이[VCP]|ㄹ[ETM]일/NNG|이/VCP|ㄹ/ETM

14	0	$UNK$		것[NNB]|이[VCP]|다[EF]|.[SF]것/NNB|이/VCP|다/EF|./SF


*** 주의사항 ***

 1. 각 형태소는 특수 문자를 제외한 의미있는 형태소만을 취함.
 2. 입력 데이터가 존재하지 않거나, 예시 문장과 다른 포멧일 경우 작동하지 않을 수 있음.
 3. tagging시 출력 경로 : data/result/tagging
 4. 초기 학습시, 파라미터는 config.py에서 수정 가능
 
*** 실행 방법 ***
 
 ※ train 모드 및 tagging 모드 선택은 src/config.py에 있는 mode를 통해 선택 가능.
 
 pip install -r requirements.txt
 
 python src/build_data.py
 python src/main.py