<실행방법 :  옵션 추가>
부트스트래핑 없이, 기본 CRF 모델만 학습해서, 대량 unlabeled data에 prediction하여, 결과만 출력하고자 할 경우
python main.py -g -na -i <unlabeled raw data input file name> -o <machine-labeled data output file name>

 [추가된 옵션설명]
  * -na : non-active, active train을 위한 부트스트래핑 데이터 생성하지 않음. 부트스트래핑 데이터 생성을 위한 sub iteration, bagging 모두 생략
  * -i : unlabeled raw data input file name 경로 지정 가능, 경로지정하지 않을경우 input 디렉토리의 unlabeld _raw_data  디렉토리 아래있는 모든 파일을 읽어서 unlabeled raw data로 사용
  * -o : unlabeled raw data에 prediction을 부여한 machine-labeled data가 써질 file nmae, 따로지정하지 않으면 output 내 full_data 아래에 생성
  * -boot_iter : boot iter 를 꼭 입력하게 했었는데 active train 안하신다셔서 따로 지정하지 않으면 0으로 돌게 해두었습니다. 
<출력양식 수정>
 active train 안하신다기에 active train용 데이터 출력양식은 바꾸지 않았습니다.
 machine-labeled data output file ( full data )의 양식엔 문장의 확률이 아래와 예시 같이 추가되었습니다. 문장과 확률사이 구분은 탭입니다.

 ;지미 카터는 조지아 주 섬터 카운티 플레인스 마을에서 태어났다.  0.986828040801
 지미 NNP 0 B-PS 1.0
 카터 NNP 0 I-PS 0.99999999996
