# /home/nlpgpu3/data/cm/nlp-challenge/missions/srl/data/train/[naver]komoran_train_data.txt

sentences = []
sentence = ""
with open("./data/cm/nlp-challenge/missions/srl/data/train/train_data_morph") as f:
    for line in f.readlines():

        if line.strip() == "" :
            sentences.append(sentence.strip())
            sentence = ""
            continue

        # _, eojoel, _, _ = line.split()
        _, _, eojoel = line.split()
        for morph in eojoel.split("|"):
            sentence += morph + " "


with open("./data/cm/nlp-challenge/missions/srl/data/train/elmo_ner_train.txt", "w") as f:
    for sentence in sentences:
        f.write(sentence+"\n")
