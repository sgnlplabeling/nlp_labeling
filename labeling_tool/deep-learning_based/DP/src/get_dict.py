from config import Config
# from konlpy.tag import Hannanum
# import nltk
# hannanum = Hannanum()
# config = Config()
word2idx = {}
pos2idx = {}
rel2idx = {}
char2idx = {}
morph2idx = {}
eojeol2tag = {}
tag2idx = {}
# nltk.download('punkt')
# nltk.download('averaged_perceptron_tagger')
# with open("../data/sejong/raw/train.txt", "rb") as f:
with open("../data/sejong/knu/train.txt", "rb") as f:
    for line in f.readlines():

        # line = line.decode("euc-kr").strip()
        # line = line.decode("utf-8").strip()
        line = line.strip().decode("utf-8")
        # line = line.strip()
        if line.strip() == "":
            continue
        if line.strip()[0] == ";" :
            continue
        #     # a = hannanum.analyze(line)
        #
        #     tokens = nltk.word_tokenize(line[1:].strip().decode("utf-8"))
        #     tokens = nltk.pos_tag(tokens)
        #     for eojeol in tokens:
        #         eojeol, tag = eojeol
        #         eojeol = eojeol.encode("utf-8")
        #         if eojeol not in eojeol2tag:
        #             eojeol = eojeol
        #             eojeol2tag[eojeol] = tag
        #         if tag not in tag2idx:
        #             tag2idx[tag]= len(tag)
        #     continue


        eojeol = line.split("\t")[-1].split("|")
        # eojeol = line.split("\t")[-1].split("+")
        rel = line.split("\t")[2]

        chars = ""
        tmp_word = ""
        tmp_pos = ""
        for e in eojeol:
            idx = e.rfind('/')
            lex = e[:idx]
            tmp_word += lex
            tmp_pos+=e[idx+1:]+"+"

        if tmp_pos[:-1] not in pos2idx:
            pos2idx[tmp_pos[:-1]] = len(pos2idx)

        if tmp_word not in word2idx:
            word2idx[tmp_word] = len(word2idx)

        # for e in eojeol:
        #     pos = e.split("/")[-1].strip()
        #     morph = e.split("/")[0].strip()
        #     word = e.strip()
        #
        #     chars = e.split("/")[0].strip()
        #     # chars = unicode(chars, 'euc-kr')
        #     # chars = chars.decode("utf-8")
        #     for char in chars:
        #         if char not in char2idx:
        #             char2idx[char] = 1
        #         else:
        #             char2idx[char] += 1
        #
        #
        #     if e in word2idx:
        #         word2idx[e] += 1
        #     else:
        #         word2idx[e] = 1
        #
        #         # word2idx[e] = len(word2idx)
        #     if pos not in pos2idx:
        #         pos2idx[pos] = len(pos2idx)
        #     if morph not in morph2idx:
        #         morph2idx[morph] = len(morph2idx)

        if rel not in rel2idx:
            rel2idx[rel] = len(rel2idx)

# with open("../data/sejong/knu/test.txt", "rb") as f:
#     for line in f.readlines():
#
#         # line = line.decode("euc-kr").strip()
#         # line = line.strip()
#         line = line.strip().decode("utf-8")
#         if line.strip() == "":
#             continue
#         if line.strip()[0] == ";" :
#             continue
#         if line.strip()[1] == ";" :
#             continue
#
#         # eojeol = line.split("\t")[-1].split("+")
#         eojeol = line.split("\t")[-1].split("|")
#
#         rel = line.split("\t")[2]
#
#         chars = ""
#         for e in eojeol:
#             pos = e.split("/")[-1].strip()
#             morph = e.split("/")[0].strip()
#             word = e.strip()
#
#             chars = e.split("/")[0].strip()
#             # chars = unicode(chars, 'utf-8')
#             for char in chars:
#                 if char not in char2idx:
#                     char2idx[char] = 1
#                 else:
#                     char2idx[char] += 1
#
#
#             if e in word2idx:
#                 word2idx[e] += 1
#             else:
#                 word2idx[e] = 1



with open("../data/init/1_1words.txt", "w") as f:
    for word in word2idx:
        if word.strip() == "":
            continue
        f.write(word.strip())
        f.write("\n")
with open("../data/init/1_1pos.txt", "w") as f:
    for word in pos2idx:
        if word.strip() == "":
            continue
        f.write(word.strip())
        f.write("\n")

# with open("../data/init/rels.txt", "w") as f:
#     for word in rel2idx:
#         if word.strip() == "":
#             continue
#         f.write(word.strip())
#         f.write("\n")
#
#
#
# with open("../data/init/char.txt", "w") as f:
#     for word in char2idx:
#         if word.strip() == "":
#             continue
#         # f.write(word.encode("utf-8").strip())
#         f.write(word.strip())
#         f.write("\n")
#
# with open("../data/init/morphs.txt", "w") as f:
#     for word in morph2idx:
#         if word.strip() == "":
#             continue
#         f.write(word)
#         f.write("\n")
#
# with open("../data/init/eojeols_train.txt", "w") as f:
#     for word in eojeol2tag:
#         if word.strip() == "":
#             continue
#         f.write(word)
#         f.write("\n")
#
# with open("../data/init/tags.txt", "w") as f:
#     for word in tag2idx:
#         if word.strip() == "":
#             continue
#         f.write(word)
#         f.write("\n")
