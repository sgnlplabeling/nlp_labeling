요구사항:
    pip install -r requirements.txt

개발환경:
    python 3.6.1

데이터:
    Golden set의 경우 labeled_data 폴더 안에donga_pos_hotel_corpus.txt와 donga_pos_schedule_corpus.txt가 있습니다.
    이 데이터들은 Speaker   Utterance   Dialogue act(old)   Dialogue act(new)   의 형태를 띄고 있으며
    각 feature들간의 구분자는 '\t'입니다. 다른 파일이름으로 변경하고 싶으시면 data_preprocessing.py의
    initializing에서 바꿀 수 있습니다. Utterance의 경우 형태소 분석이 완료된 상태이며
    형태소와 태그의 구분자는 '/',  형태소끼리의 구분자는 '|' 입니다.

    데이터 예시)
    user  아름/VA|아/EC|잘/MAG|잤/VV|니/EF|?/SF     greeting    opening
    system  네/IC|,/SP|잘/MAG|잤/VV|습니다/EF|.SF   greeting    opening

    채팅 데이터(unlabeled_data)의 경우 unlabeled_data 폴더 안에 donga_pos_unlabeled_data가  있습니다.
    이 데이터는 txt 형식으로 이루어져 있으며 question과  answer쌍으로 이루어져 있습니다.
    이미 형태소 분석이 완료된 상황이며, 다른 파일이름으로 변경하고 싶으시면 softmax_hier_bootstrap.py의 main함수에서 바꿀 수 있습니다.

    bootstrapped_data 폴더에는 부트스트랩핑이 종료된 이후, 기존 Golden set에 machine labeled 데이터가 추가된
    최종 데이터가 들어가게 됩니다. data.txt는 문장들이 한 줄에 한 문장씩 써있고, label.txt에는 각 문장의 화행에
    해당하는 라벨이 한줄에 한개씩 써있습니다.
    data.txt 예시)
    밥/NNG|은/JX|먹/VV|었/EP|니/EF|?/SF


    result 폴더에는 부트스트랩핑이 모두 완료된 데이터(data.txt와 label.txt)를 가지고 전체 채팅 데이터에 대해
    machine labeled 라벨이 들어있습니다. 마찬가지로 한 줄에 한 라벨씩 써있습니다.

실행방법:
    우선 부트스트랩핑을 진행하기 위해 python softmax_hier_bootstrap.py 를 실행하면 됩니다.
    프로그램이 완료 된 후, 추가된 데이터를 가지고 새로운 데이터에 machine labeled label만 찍고 싶으면
    python predict.py를 실행하면 됩니다.

세부사항:
    Bootstrapping의 Batch size는 초기에 5000으로 설정되어 있습니다. softmax_hier_bootstrap.py의 main함수에서 수정 가능합니다.

