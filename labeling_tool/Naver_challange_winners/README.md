[SRL], [NER] 2018 Naver Challenge code
======================

1. 소속 : 서강대학교 자연어처리 연구실
2. 작성자 : 박영준 <yeongjoon1227@gmail.com>
3. 개발자 : 박찬민, 박영준
4. 관리자 : 김주애 <jju75474@gmail.com>

* 본 프로그램은 서강대학교 자연어처리 연구실의 소중한 자산입니다.  
* 본 프로그램을 이용한 모든 결과물은 본 프로그램의 주소가 참조되어야 합니다.  
* 참조 사이트 : <https://github.com/sgnlplabeling/nlp_labeling>  

## Referenced Codes
><https://github.com/naver/nlp-challenge/tree/master/missions/srl>

## Requirements
>python >= 3.6  
>tensorflow == 1.4.1
>konlpy == 0.5.1
>cuda == 8.0  

## Data format
~~~
SRL 예시문장 : 그는 경찰에게 신분증을 보였다.

0	그는	ARG0
1	경찰에게	ARG3
2	신분증을	ARG1
3	보였다.	-
~~~

~~~
NER 예시문장 : 나는 창원대학교에서 열린 대동제를 구경하러 갔다.
0	나는	-
1	창원대학교에서	LOC_B
2	열린	-
3	대동제를	EVT_B
4	구경하러	-
5	갔다.	-
~~~

## Training
```
python main.py
```

## Test
```
NSML을 사용하는 코드로서 NSML을 통해서만 Inference가 가능합니다.
```

※ parameter 설정은 main.py 내의 option을 통해서 선택/수정 가능합니다.

※ Train 데이터 : <https://github.com/naver/nlp-challenge/tree/master/missions/srl/data/train>
