Requirement : 
	pip install requirements.txt
	word_Embeddings_size64.pkl 파일을 python 파일들과 같은 폴더 내에 둔다. (경로 위치 변경은 data_helper.py -> 함수 load_pretrained_embeddings에서 가능하다.)

Data : 
	labeled_data dir

	1. donga_pos_hotel_corpus.txt
	ex) Speaker	Utterance	Dialogue act (old)	Dialogue act (new)
	    Agent	안녕하/VA|세요/EF|?/SF	opening	opening
	    Agent	명산/NNP|관광/NNG|입/VCP|니다/EF|./SF	introducing-oneself	introduce
	    User	네/NNP|저/NP|는/JX|설악산/NNP|과/JC|속리산/NNG|을/JKO|여행하/VV|고/EC|싶/VX|은데/EF|요/JX|./SF	inform	inform

	2. donga_pos_schedule_corpus.txt
	ex) Speaker	Utterance	Dialogue act (old)	Dialogue act (new)
	    user	아름/VA|아/EC|잘/MAG|잤/VV|니/EF|?/SF	greeting	opening
	    system	네/IC|,/SP|잘/MAG|잤/VV|습니다/EF|./SF	greeting	opening
	    user	아름/VA|아/EC|일정/NNG|확인/NNG|좀/MAG|해줘/VV|./SF	request	request

	3. donga_pos_active_3000_data.txt
	ex) 내/NP|고운/NNP|피부/NNG
	    도대체/MAG|비결/NNG|이/JKS|뭐/NP|에/JKB|요/JX|~/SO|나/NP|에게/JKB|도/JX|좀/MAG|알려줘/VV|요/EF|~/SO
	    저축할돈/NNG|이/VCP|있/VA|어야지/EC

	4. active_3000_label.txt
	ex) wh-question
	    inform
	    wh-question
	
	5. donga_pos_train_data.txt
	위의 1~4 데이터 파일을 통합한 파일
	ex) 안녕하/VA|세요/EF|?/SF	opening
	    명산/NNP|관광/NNG|입/VCP|니다/EF|./SF	introduce
	    네/NNP|저/NP|는/JX|설악산/NNP|과/JC|속리산/NNG|을/JKO|여행하/VV|고/EC|싶/VX|은데/EF|요/JX|./SF	inform

	unlabeled_data dir

	1. donga_pos_unlabeled_data.txt
	ex) 밥/NNG|은/JX|먹/VV|었/EP|니/EF|?/SF
	    응/NNG|먹/VV|었/EP|어요/EF|!/SF
	    맞/VV|아/EC

File List : 
1. main.py 
	train과 predict를 위하여 실행해야 할 파일
	실행 방법 : python main.py -i <input(train) file path> (-o <output dir path>)
	-o <output dir path> 지정하지 않으면 'trained_results'이름의 디렉토리에 저장된다.
	
	결과물 : trained_results 디렉토리
		
	결과 정확도 : 마지막에 프린트되는 "The prediction accuracy is : XXX"

2. train.py
	CNN-RNN 모델을 학습시키는 파일
	실행 방법 : main.py에서 호출되어 실행된다.
	파라미터 조정 : params 변수로 선언 되어있는 곳에서 수정하면 된다.
		       배치 사이즈 조정, 임베딩 차원, 드랍아웃 확률, CNN filter 사이즈 등등 조정할 수 있다.	       
	결과물 : trained_results 디렉토리에 3개의 파일과 checkpoint 파일이 만들어 진다.
		labels.json (label set을 저장)
		trained_parameters.json (파라미터 저장)
		words_index.json (vocabulary 저장)

3. predict.py
	학습된 CNN-RNN 모델을 이용하여 예측하는 파일
	실행 방법 : main.py에서 호출되어 실행된다.
	함수 리턴값 : 예측된 labels 벡터, 정확도
	결과 정확도 : 마지막에 프린트되는 "The prediction accuracy is : XXX"

4. text_cnn_rnn.py
	CNN-RNN 모델
	파라미터 : embedding_mat (사용될 pretrained embedding matrix)
		 non_static (True : Pretrained embedding 사용, False : randomly initialized embedding 사용)
		 이외에도 hidden_unit, sequence_length, max_pool_size, num_classes, embedding_size, filter_sizes, num_filters, l2_reg_lambda가 있다.
	
5. data_helper.py
	데이터 전처리를 담당하는 파일
	load_data : 학습과 테스트에 사용되는 데이터를 불러온다. 
	load_embeddings : pretrained embedding matrix로 부터 vocabulary에 있는 단어들을 불러온다
	load_pretrained_embeddings : pretrained embedding matrix를 불러온다.
	pad_sentences : 입력 데이터를 정해진 길이에 맞춰 padding 처리를 한다.
	build_vocab : 데이터에 사용되는 vocabulary를 만든다.
	morp_data : 형태소 분석하는 모듈이다.
	batch_iter : epoch마다 batch data를 생성한다.
	

5. predict_rawtext.py
	실행 방법 : python predict_rawtext.py -i <input file path> -o <output file path> (-t <rained_dir>)
	ex) python predict_rawtext.py -i '../data/unlabeled_data/donga_pos_unlabeled_data.txt' -o 'DailyLife_MachineLabeled_SG_DNN.txt'

	-t <trained_dir> 지정하지 않으면 './trained_results/' 이름의 디렉토리로 지정된다.
		trained_dir : train 결과(best_model.ckpt 파일, embeddings.pickle,
		labels.json, trained_parameters.json, words_index.json)가 담긴 파일

	유의사항 : input file의 경우 unlabeled 파일이여야 한다.
		
	결과 파일 : 
		실행 결과 예측 label은 <output file>에 저장된다.
		ex) 밥/NNG|은/JX|먹/VV|었/EP|니/EF|?/SF	yn-question	49.17
		    응/NNG|먹/VV|었/EP|어요/EF|!/SF	inform	72.3
		    맞/VV|아/EC	expressive	41.48
		