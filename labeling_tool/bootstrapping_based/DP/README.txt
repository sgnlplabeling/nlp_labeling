<�� �Ұ�>
	�� ���� �Ľ� ���� Feed Forward Neural Network����� Trainstion Parser�Դϴ�.
	�н� �����͸� 10���� �����ؼ� 10���� ���� �ٸ� ���� �н��ϴ� Bagging ����� ����Ͽ����ϴ�.
	�� bagging ����� Voting�Ͽ��� arc�� weight�� ���� CKY �˰����� ����Ͽ����ϴ�.
	���������� CKY �˰������� ���� ���� �� �� arc�� ��� weight�� ���� �Ľ� ����� score�� ����մϴ�.
	
	�� bagging iteration���� ���� �Ľ� ����� g_socre�� a_socre�� �������� �и��մϴ�.
	����ڴ� g_score�� a_socre�� �������� �и��� ���� �Ľ� ���(g_result.txt, a_result.txt, b_result.txt) �� ���ϴ� �Ľ� ����� ���� �� �� �ְ�
	���õ� ��� ������ ���� bagging�� �н������Ϳ� �߰��Ǵ� ���ÿ� ���� bagging���� ���� test data���� ���ŵ˴ϴ�. 

	���� ���� bootstrapping�� �ߴ��ϰ� �ʱ� �н� ������(../data/input_data/test_data)�� ���ݱ��� �н��� �𵨷�
	���� �Ľ��� ���� �ϰ� ���� ��� "g_predict" �ɼ����� ���α׷��� �����մϴ�.


<������>
	���� �����, g_socre : 0.99, a_score 0.95
	> python Dependency_main.py -train_path ../data/input_data/training_data -mode train -bagging 0
	> python Dependency_main.py -test_path ../data/input_data/test_data -mode predict -bagging 0 -g 0.99 -a 0.95
	
	n��° bagging ����� (�н�), ���� bagging���� ������ a grade�� ��Ʈ��Ʈ���� (default = ..data/trainning_data/%sth_in)
	> python Dependency_main.py -train_path ������� -mode train -bagging n -scope a Ȥ��
	> python Dependency_main.py -train_path default -mode train -bagging n -scope a
	
	n��° bagging �����, (�Ľ�) g_score�� a_score�� �����Ͽ� "graded_result.txt" ����
	(default = ../data/test_data/%sth_test_data)
	> python Dependency_main.py -test_path ������� -mode predict -bagging n -g 0.99 -a 0.95 Ȥ��
	> python Dependency_main.py -test_path default -mode predict -bagging n -g 0.99 -a 0.95
	
	��������� �н��� n��° ���� ����Ͽ� ��ü �����͸� �Ľ� �� ���
	> python Dependency_main.py -test_path ������� -bagging n -mode g_predict -output_path ������� Ȥ��
	> python Dependency_main.py -test_path default -bagging n -mode g_predict -output_path �������
	
	�� n��° bagging ����� default ��� ��θ� ���� �Է����־ �˴ϴ�.
	
	������ train epoch�� 1�� �����Ǿ� �ֽ��ϴ�. config.py ���� num_epochs�� �����Ͻ� �� �ֽ��ϴ�. (default = 30)
	
	��n��° bagging �����, ���� ���� �Ľ̰���� "a"(�̾��)�Ǵ� ���α׷� Ư����
	 ../data/tmp_data/%sth_tmp_data/before_voting ������ ������ ����Ǿ� ������ ������ �߻� �� �� �ֽ��ϴ�.


<������ �Ұ�>
	train data�� ���Ǵ� ���� ���۽� + active learning ���۽�(218����)�� ���� ��ο� �ֽ��ϴ�. (������:"\n\n")
	../data/input_data/train
	
	test data�� ���Ǵ� ���� ���� �������� ������ ���� ���ϰ� �����ϴ�. (������:"\n\n")
	../data/input_data/test_data
	
	��/home/sogang/shared/Dependency/result ������ ���� �Ľ̵� ��뷮 �����Ͱ� �ֽ��ϴ�.
	
	������ ../data/input_data/test_data ��ο��� ���뷮�� toy data�� ����Ǿ� �ֽ��ϴ�.
	��뷮 ���� ���۽��� /home/sogang/shared/Dependency/tmp ������ �� 10�� ���Ϸ� ���� ����Ǿ� �ֽ��ϴ�.


<�ɼ� ����>
- train_path
	- �н��� ��� �� training data�� ���� ����Դϴ�.
	"default"�� �Է����� ����ϸ� ���� bagging_iter�� �˸��� training ������ �����˴ϴ�.
	��, 0��° bagging ���۽� ���� ��θ� �ʼ������� �Է����־�� �մϴ� ex) ../data/input_data/training_data

- test_path
	- predict�� ��� �� data�� ���� ����Դϴ�.
	"default"�� �Է����� ����ϸ� ���� bagging_iter�� �˸��� test ������ �����˴ϴ�.
	��, 0��° bagging ���۽� ���� ��θ� �ʼ������� �Է����־�� �մϴ� ex) ../data/input_data/test_data

- bagging
	- ���� bagging iteration�� num�Դϴ�. �ʱ� ���� 0�Դϴ�.

- mode 
	- ���α׷��� mode �ɼ��̸� "train","predict","g_predict"�� �����մϴ�.
		-train : �Ϲ����� bagging �ɼ��Դϴ�. 
		training data�� test data�� �Է����� �� �н��� �����մϴ�.
		���ڷ� bootstrapping�� ���� ������ ���ڷ�("g", "a", "b") �޽��ϴ�.
		�н� ���� "../data/f_model"�� "../data/ckpt"�� ����˴ϴ�.
		
		-predict : train���� �н��� �𵨷� ���� �Ľ��� �����մϴ�.
		�� 10���� �𵨷� ����� ����Ǹ� ����� "../data/tmp_data/%sth_tmp_data/"�� ����˴ϴ�.
		���ڷ� g_score�� a_socre�� �޾� �̸� �������� "graded_result.txt"�� �����մϴ�.
	
		-g_predict : ������� �н��� model�� �ʱ� �׽�Ʈ ������(../data/input_data/test_data)�� ���� ���� �Ľ��� �����մϴ�.
		�Ľ� ����� ../data/g_data/%sth_final_data �� ����˴ϴ�.

- g :
	- bootstrapping�� ������ �Ǵ� g_score���Դϴ�.

- a : 
	- bootstrapping�� ������ �Ǵ� a_score���Դϴ�.

- scope : 
	- ���� ��Ʈ��Ʈ���μ� ��� �� ������ �̸��Դϴ�.
	g_score�� a_score�� �������� ������ "g_result.txt", "a_result.txt", "b_result.txt" ���� �� ����ڰ� ��� �� ������ �����մϴ�.
	Active learning�� ���� �� ���, Active learning�� �Ϸ�� ������ ���ڷ� �־��ָ� �˴ϴ�.
	(�⺻ ��� : ../data/tmp_data/%sth_gab_data)
	
<���� ����>
-src : python �ҽ��ڵ��Դϴ�.


-data : ����� ������ �� ��
	- ckpt : MLP �н� ����ġ ���� ����(tensorflow checkpoint file)

	- f_model : ���� �ļ� ���� ���� �� ����

	- input_data : bagging�� �ʿ��� �н�������/�׽�Ʈ������
		- training_data : �н������� , 0��° bagging�ÿ��� ���
		- test_data : �׽�Ʈ������, 0��° bagging��, g�ɼǽ� ���Ǵ� ��ü �׽�Ʈ �������̹Ƿ� �����ϸ� �ȵ˴ϴ�.

	- log : 
		- MLP ����ġ �н���, ������ȹ Test �����Ϳ� ���� ���� ��� 
	
	- raw_data : 
		- training_data : ���� ��ȹ Train ������ + ��Ƽ�� ������(218����)
		- valid_data : ���� ��ȹ Test ������

	- tmp_data :
		
		- %s_g_tmp_data :
			- "g" �ɼ����� ��µǴ� ����� �ӽ� �����Դϴ�.
		- %sth_tmp_data :
			- before_voting : %s��° bagging ���� ��°��, voting ��
			- after_voting : %s��° bagging ���� ��°��, voting ��
		- %sth_gab_data :
			- %s��° bagging ��, socre "g", "a", "b"�� ������ �Ľ� ����� ����
		
	- training_data :
		- %sth_out: %s��° �н��� ��� �� ������, ��ó�� ��
		- %sth_in : %s��° �н��� ��� �� ������, ��ó�� �� 

	- g_data :
		- �� �̻� bootstrapping�� �������� �ʰ�
		 ��ü �׽�Ʈ �����Ϳ� ���� ���� ���� �Ľ��� ������ ����� ����Ǵ� �����Դϴ�.
