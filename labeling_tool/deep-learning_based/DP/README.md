[DP] RIGHT TO LEFT DEPENDENCY PARSER
======================

1. 소속 : 서강대학교 자연어처리 연구실  
1. 작성자 : 정영훈 <hoon2j@gmail.com>. 
1. 개발자 : 한장훈, 박영준, 정영훈, 이인권
1. 관리자 : 김주애 <jju75474@gmail.com>  

* 본 프로그램은 서강대학교 자연어처리 연구실의 소중한 자산입니다.  
* 본 프로그램을 이용한 모든 결과물은 본 프로그램의 주소가 참조되어야 합니다.  
* 참조 사이트 : <https://github.com/sgnlplabeling/nlp_labeling>  

## Referenced Codes
><https://github.com/XuezheMax/NeuroNLP2>  
><https://github.com/danifg/Left2Right-Pointer-Parser>  

## Referenced Papers
>Left-to-Right Dependency Parsing with Pointer Networks - Daniel Fernández-González et al  
>Stack-Pointer Networks for Dependency Parsing - Xuezhe Ma et al  

## Requirements
>python == 3.6.9  
>pytorch == 1.1.0  
>cuda == 10.0  

## Data Format
>CONLLX Format
~~~
예시문장 : 프랑스의 세계적인 의상 디자이너 엠마누엘 웅가로가 실내 장식용 직물 디자이너로 나섰다.  

ID FORM _ _ XPOS _ HEAD DEPREL _ _
-----------------------------------
1	프랑스/NNP|의/JKG	_	_	NNP+JKG	_	4	NP_MOD	_	_
2	세계/NNG|적/XSN|이/VCP|ㄴ/ETM	_	_	NNG+XSN+VCP+ETM	_	4	VNP_MOD	_	_
3	의상/NNG	_	_	NNG	_	4	NP	_	_
4	디자이너/NNG	_	_	NNG	_	6	NP	_	_
5	엠마누엘/NNP	_	_	NNP	_	6	NP	_	_
6	웅가로/NNP|가/JKS	_	_	NNP+JKS	_	11	NP_SBJ	_	_
7	실내/NNG	_	_	NNG	_	8	NP	_	_
8	장식/NNG|용/XSN	_	_	NNG+XSN	_	9	NP	_	_
9	직물/NNG	_	_	NNG	_	10	NP	_	_
10	디자이너/NNG|로/JKB	_	_	NNG+JKB	_	11	NP_AJT	_	_
11	나서/VV|었/EP|다/EF|./SF	_	_	VV+EP+EF+SF	_	0	VP	_	_
~~~

## Training
1. RIGHT-TO-LEFT Dependency Parser
./examples/run_RLParser.sh

2. Bi-Affine Dependency Parser
```
./examples/run_graphParser.sh
```

## Test
```
./examples/run_inference.sh
```

※ parameter 설정은 각각의 shell file의 option을 통해서 선택/수정 가능합니다.  
※ 현재 train, test 데이터는 예시 파일로, 일부만 업로드 되어있습니다.  
전체 데이터가 필요할 경우에는 작성자 및 관리자의 이메일로 요청바랍니다.  
