Requirement : 
	pip install requirements.txt
	word_Embeddings_size64.pkl ������ python ���ϵ�� ���� ���� ���� �д�. (��� ��ġ ������ data_helper.py -> �Լ� load_pretrained_embeddings���� �����ϴ�.)

Data : 
	labeled_data dir

	1. donga_pos_hotel_corpus.txt
	ex) Speaker	Utterance	Dialogue act (old)	Dialogue act (new)
	    Agent	�ȳ���/VA|����/EF|?/SF	opening	opening
	    Agent	���/NNP|����/NNG|��/VCP|�ϴ�/EF|./SF	introducing-oneself	introduce
	    User	��/NNP|��/NP|��/JX|���ǻ�/NNP|��/JC|�Ӹ���/NNG|��/JKO|������/VV|��/EC|��/VX|����/EF|��/JX|./SF	inform	inform

	2. donga_pos_schedule_corpus.txt
	ex) Speaker	Utterance	Dialogue act (old)	Dialogue act (new)
	    user	�Ƹ�/VA|��/EC|��/MAG|��/VV|��/EF|?/SF	greeting	opening
	    system	��/IC|,/SP|��/MAG|��/VV|���ϴ�/EF|./SF	greeting	opening
	    user	�Ƹ�/VA|��/EC|����/NNG|Ȯ��/NNG|��/MAG|����/VV|./SF	request	request

	3. donga_pos_active_3000_data.txt
	ex) ��/NP|���/NNP|�Ǻ�/NNG
	    ����ü/MAG|���/NNG|��/JKS|��/NP|��/JKB|��/JX|~/SO|��/NP|����/JKB|��/JX|��/MAG|�˷���/VV|��/EF|~/SO
	    �����ҵ�/NNG|��/VCP|��/VA|�����/EC

	4. active_3000_label.txt
	ex) wh-question
	    inform
	    wh-question
	
	5. donga_pos_train_data.txt
	���� 1~4 ������ ������ ������ ����
	ex) �ȳ���/VA|����/EF|?/SF	opening
	    ���/NNP|����/NNG|��/VCP|�ϴ�/EF|./SF	introduce
	    ��/NNP|��/NP|��/JX|���ǻ�/NNP|��/JC|�Ӹ���/NNG|��/JKO|������/VV|��/EC|��/VX|����/EF|��/JX|./SF	inform

	unlabeled_data dir

	1. donga_pos_unlabeled_data.txt
	ex) ��/NNG|��/JX|��/VV|��/EP|��/EF|?/SF
	    ��/NNG|��/VV|��/EP|���/EF|!/SF
	    ��/VV|��/EC

File List : 
1. main.py 
	train�� predict�� ���Ͽ� �����ؾ� �� ����
	���� ��� : python main.py -i <input(train) file path> (-o <output dir path>)
	-o <output dir path> �������� ������ 'trained_results'�̸��� ���丮�� ����ȴ�.
	
	����� : trained_results ���丮
		
	��� ��Ȯ�� : �������� ����Ʈ�Ǵ� "The prediction accuracy is : XXX"

2. train.py
	CNN-RNN ���� �н���Ű�� ����
	���� ��� : main.py���� ȣ��Ǿ� ����ȴ�.
	�Ķ���� ���� : params ������ ���� �Ǿ��ִ� ������ �����ϸ� �ȴ�.
		       ��ġ ������ ����, �Ӻ��� ����, ����ƿ� Ȯ��, CNN filter ������ ��� ������ �� �ִ�.	       
	����� : trained_results ���丮�� 5���� ���ϰ� checkpoint ������ ����� ����.
		labels.json (label set�� ����)
		trained_parameters.json (�Ķ���� ����)
		words_index.json (vocabulary ����)
		embedding_mat.pickle (���� �Ӻ��� ����)
		embedding_pre.pickle (���� ȭ�� ���� �Ӻ��� ����)

3. predict.py
	�н��� CNN-RNN ���� �̿��Ͽ� �����ϴ� ����
	���� ��� : main.py���� ȣ��Ǿ� ����ȴ�.
	�Լ� ���ϰ� : ������ labels ����, ��Ȯ��
	��� ��Ȯ�� : �������� ����Ʈ�Ǵ� "The prediction accuracy is : XXX"

4. text_cnn_rnn.py
	CNN-RNN ��
	�Ķ���� : embedding_mat (���� pretrained embedding matrix),
		 embedding_pre (���� ȭ�� ���� pretrained embedding matrix)
		 non_static (True : Pretrained embedding ���, False : randomly initialized embedding ���)
		 �̿ܿ��� hidden_unit, sequence_length, max_pool_size, num_classes, embedding_size, filter_sizes, num_filters, l2_reg_lambda�� �ִ�.
	
5. cnn_attention.py
	CNN �Է� �� ȣ��Ǵ� �Լ�
	���� ȭ�� ������ �Է� ��ȭ ���� ���ټ� ����� �����Ѵ�.

6. data_helper.py
	������ ��ó���� ����ϴ� ����
	load_data : �н��� �׽�Ʈ�� ���Ǵ� �����͸� �ҷ��´�. 
	load_embeddings : pretrained embedding matrix�� ���� vocabulary�� �ִ� �ܾ���� �ҷ��´�
	load_pretrained_embeddings : pretrained embedding matrix�� �ҷ��´�.
	pad_sentences : �Է� �����͸� ������ ���̿� ���� padding ó���� �Ѵ�.
	build_vocab : �����Ϳ� ���Ǵ� vocabulary�� �����.
	morp_data : ���¼� �м��ϴ� ����̴�.
	batch_iter : epoch���� batch data�� �����Ѵ�.
	

7. predict_rawtext.py
	���� ��� : python predict_rawtext.py -i <input file path> -o <output file path> (-t <rained_dir>)
	ex) python predict_rawtext.py -i '../data/unlabeled_data/donga_pos_unlabeled_data.txt' -o 'DailyLife_MachineLabeled_SG_DNN.txt'

	-t <trained_dir> �������� ������ './trained_results/' �̸��� ���丮�� �����ȴ�.
		trained_dir : train ���(best_model.ckpt ����, embedding_mat.pickle, embedding_pre.pickle,
		labels.json, trained_parameters.json, words_index.json)�� ��� ����

	���ǻ��� : input file�� ��� unlabeled �����̿��� �Ѵ�.
		
	��� ���� : 
		���� ��� ���� label�� <output file>�� ����ȴ�.
		ex) ��/NNG|��/JX|��/VV|��/EP|��/EF|?/SF	yn-question	49.17
		    ��/NNG|��/VV|��/EP|���/EF|!/SF	inform	72.3
		    ��/VV|��/EC	expressive	41.48
		