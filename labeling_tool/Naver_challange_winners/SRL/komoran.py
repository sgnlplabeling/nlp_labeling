from konlpy.tag import Komoran
result = []
komoran = Komoran()
with open("/home/nlpgpu4/data/cm/Attetion_SRL/[naver]train_data.txt") as f:
    for line in f.readlines():

        if line.strip() == "" :
            result.append("\n")
            continue
        idx, raw_word, label = line.split()
        tmp_word = komoran.pos(raw_word.decode("utf-8"))
        word = ""
        for w in tmp_word:
            word += w[0]+"/"+w[1] + "|"

        new_line = idx + "\t" + word[:-1] + "\t" + raw_word.decode("utf-8") +"\t"+ label.strip() + "\n"
        result.append(new_line)
        # break

with open("/home/nlpgpu4/data/cm/Attetion_SRL/[naver]komoran_train_data.txt", "w") as f:
    for r in result:
        f.write(r.encode("utf-8"))

		34857