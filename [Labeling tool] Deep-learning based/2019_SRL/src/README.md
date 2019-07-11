소속 서강대학교 자연어처리 연구실

작성자 : 박찬민(cksals302@gmail.com)
개발 : 박찬민(cksals302@gmail.com, 석사과정)
관리자 : 김주애(jju75474@gmail.com, 박사과정)

본 프로그램은 서강대학교 자연어처리 연구실의 소중한 자산입니다.

본 프로그램을 이용한 모든 결과물은 본 프로그램의 주소가 참조되어야 합니다.

참조 사이트 : https://github.com/sgnlplabeling/nlp_labeling

개발 환경 (src/requirements.txt 참조)


Pyhton==3.5.6

h5py==2.8.0

tensorflow_gpu==1.6.0

hanja==0.11.0

numpy==1.15.4

tensorflow==1.14.0

typing==3.7.4

*** 예시 문장 ***
 
 ※ 학습 시
 이/NP+와/JKB 관련/NNG+,/SP 정부/NNG+는/JX 내달/NNG 남북/NNP+교류협력추진/NNG 실무위원회/NNG+를/JKO 열/VV+어/EC 정부/NNG 차원/NNG+의/JKG 남북/NNP+경제공동체/NNG 건설/NNG 방안/NNG+을/JKO 마무리하/VV+ㄹ/ETM 방침/NNG+이/VCP+나/EC 4.13/SN+총선/NNG 때/NNG+까지는/JX 민간급/NNG 경제협력/NNG 활성화/NNG 방안/NNG 추진/NNG+에/JKB 주력하/VV+ㄹ/ETM 계획/NNG+이/VCP+다/EF+./SF
 
 ->
 
 (술어 index) (술어 원형 정보) (형태소 분석된 문장)|||(의미역 태그)
 
 6 yeol.01 이/NP+와/JKB 관련/NNG+,/SP 정부/NNG+는/JX 내달/NNG 남북/NNP+교류협력추진/NNG 실무위원회/NNG+를/JKO 열/VV+어/EC 정부/NNG 차원/NNG+의/JKG 남북/NNP+경제공동체/NNG 건설/NNG 방안/NNG+을/JKO 마무리하/VV+ㄹ/ETM 방침/NNG+이/VCP+나/EC 4.13/SN+총선/NNG 때/NNG+까지는/JX 민간급/NNG 경제협력/NNG 활성화/NNG 방안/NNG 추진/NNG+에/JKB 주력하/VV+ㄹ/ETM 계획/NNG+이/VCP+다/EF+./SF|||_	_	_	ARGM-TMP	_	ARG1	_	_	_	_	_	_	_	_	_	_	_	_	_	_	_	_	_
 
 12 ma-mu-ri.01 이/NP+와/JKB 관련/NNG+,/SP 정부/NNG+는/JX 내달/NNG 남북/NNP+교류협력추진/NNG 실무위원회/NNG+를/JKO 열/VV+어/EC 정부/NNG 차원/NNG+의/JKG 남북/NNP+경제공동체/NNG 건설/NNG 방안/NNG+을/JKO 마무리하/VV+ㄹ/ETM 방침/NNG+이/VCP+나/EC 4.13/SN+총선/NNG 때/NNG+까지는/JX 민간급/NNG 경제협력/NNG 활성화/NNG 방안/NNG 추진/NNG+에/JKB 주력하/VV+ㄹ/ETM 계획/NNG+이/VCP+다/EF+./SF|||_	_	ARG0	_	_	_	ARGM-MNR	_	_	_	_	ARG1	_	_	_	_	_	_	_	_	_	_	_
 
 21 cu-ryeok.01 이/NP+와/JKB 관련/NNG+,/SP 정부/NNG+는/JX 내달/NNG 남북/NNP+교류협력추진/NNG 실무위원회/NNG+를/JKO 열/VV+어/EC 정부/NNG 차원/NNG+의/JKG 남북/NNP+경제공동체/NNG 건설/NNG 방안/NNG+을/JKO 마무리하/VV+ㄹ/ETM 방침/NNG+이/VCP+나/EC 4.13/SN+총선/NNG 때/NNG+까지는/JX 민간급/NNG 경제협력/NNG 활성화/NNG 방안/NNG 추진/NNG+에/JKB 주력하/VV+ㄹ/ETM 계획/NNG+이/VCP+다/EF+./SF|||_	_	_	_	_	_	_	_	_	_	_	_	_	_	_	ARGM-TMP	_	_	_	_	ARG1	_	_

 ※ 태깅 시
 
 이/NP+와/JKB 관련/NNG+,/SP 정부/NNG+는/JX 내달/NNG 남북/NNP+교류협력추진/NNG 실무위원회/NNG+를/JKO 열/VV+어/EC 정부/NNG 차원/NNG+의/JKG 남북/NNP+경제공동체/NNG 건설/NNG 방안/NNG+을/JKO 마무리하/VV+ㄹ/ETM 방침/NNG+이/VCP+나/EC 4.13/SN+총선/NNG 때/NNG+까지는/JX 민간급/NNG 경제협력/NNG 활성화/NNG 방안/NNG 추진/NNG+에/JKB 주력하/VV+ㄹ/ETM 계획/NNG+이/VCP+다/EF+./SF
 
 ->
 
 6 yeol.01 이/NP+와/JKB 관련/NNG+,/SP 정부/NNG+는/JX 내달/NNG 남북/NNP+교류협력추진/NNG 실무위원회/NNG+를/JKO 열/VV+어/EC 정부/NNG 차원/NNG+의/JKG 남북/NNP+경제공동체/NNG 건설/NNG 방안/NNG+을/JKO 마무리하/VV+ㄹ/ETM 방침/NNG+이/VCP+나/EC 4.13/SN+총선/NNG 때/NNG+까지는/JX 민간급/NNG 경제협력/NNG 활성화/NNG 방안/NNG 추진/NNG+에/JKB 주력하/VV+ㄹ/ETM 계획/NNG+이/VCP+다/EF+./SF|||_	_	_	_	_	_	_	_	_	_	_	_	_	_	_	_	_	_	_	_	_	_	_
 
 12 ma-mu-ri.01 이/NP+와/JKB 관련/NNG+,/SP 정부/NNG+는/JX 내달/NNG 남북/NNP+교류협력추진/NNG 실무위원회/NNG+를/JKO 열/VV+어/EC 정부/NNG 차원/NNG+의/JKG 남북/NNP+경제공동체/NNG 건설/NNG 방안/NNG+을/JKO 마무리하/VV+ㄹ/ETM 방침/NNG+이/VCP+나/EC 4.13/SN+총선/NNG 때/NNG+까지는/JX 민간급/NNG 경제협력/NNG 활성화/NNG 방안/NNG 추진/NNG+에/JKB 주력하/VV+ㄹ/ETM 계획/NNG+이/VCP+다/EF+./SF|||_	_	_	_	_	_	_	_	_	_	_	_	_	_	_	_	_	_	_	_	_	_	_
 
 21 cu-ryeok.01 이/NP+와/JKB 관련/NNG+,/SP 정부/NNG+는/JX 내달/NNG 남북/NNP+교류협력추진/NNG 실무위원회/NNG+를/JKO 열/VV+어/EC 정부/NNG 차원/NNG+의/JKG 남북/NNP+경제공동체/NNG 건설/NNG 방안/NNG+을/JKO 마무리하/VV+ㄹ/ETM 방침/NNG+이/VCP+나/EC 4.13/SN+총선/NNG 때/NNG+까지는/JX 민간급/NNG 경제협력/NNG 활성화/NNG 방안/NNG 추진/NNG+에/JKB 주력하/VV+ㄹ/ETM 계획/NNG+이/VCP+다/EF+./SF|||_	_	_	_	_	_	_	_	_	_	_	_	_	_	_	_	_	_	_	_	_	_	_


*** 주의사항 ***

 1. 각 형태소는 특수 문자를 제외한 의미있는 형태소만을 취함.
 2. 입력 데이터가 존재하지 않거나, 예시 문장과 다른 포멧일 경우 작동하지 않을 수 있음.
 3. tagging시 출력 경로 : result/predict
 4. 술어 index는 0부터 시작
 5. 초기 학습시, 파라미터는 config.py에서 수정 가능
 6. 한국어 ELMo 소스코드는 https://github.com/allenai/bilm-tf를 참고하여 한국어 특성에 적합하게 수정함
 
*** 실행 방법 ***
 
 ※ train 모드 및 tagging 모드 선택은 src/config.py에 있는 mode를 통해 선택 가능.
 
 pip install -r requirements.txt
 
 python src/main.py