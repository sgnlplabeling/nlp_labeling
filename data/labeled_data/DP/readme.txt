
데이터 : 세종 기획 의존 구문 분석 데이터

샘플 파일명: train_1.txt

파일 설명 : 의존 구문 분석 부트스트래핑시, 사용되는 입출력 데이터 형식입니다.

양식:

	(구분자) (입력 문장)
	(현재 단어의 인덱스)	(지배소의 인덱스)	(의존관계명)	(동아대 형터소 분석기)

예제:

	; 목욕가운부터 탁자보, 냅킨, 앞치마까지 그가 디자인한 작품들에서 두드러지는 것은 색의 조화다.
	1	4	NP_AJT	목욕/NNP+가운/NNG+부터/JX
	2	4	NP_CNJ	탁자보/NNG+,/SP
	3	4	NP_CNJ	냅킨/NNG+,/SP
	4	11	NP_AJT	앞치마/NNG+까지/JX
	5	6	NP_SBJ	그/NP+가/JKS
	6	7	VP_MOD	디자인하/VV+ㄴ/ETM
	7	8	NP_AJT	작품/NNG+들/XSN+에서/JKB
	8	9	VP_MOD	두드러지/VV+는/ETM
	9	11	NP_SBJ	것/NNB+은/JX
	10	11	NP_MOD	색/NNG+의/JKG
	11	0	VNP	조화/NNG+이/VCP+다/EF+./SF