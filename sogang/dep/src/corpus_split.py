import random
import tensorflow as tf

# with open ('data/knu/train.txt', 'r') as f:
with open('data/bagging_1st/cm_train_edit_VV.txt', 'r') as f:
    lines = f.read()



lines = lines.split('\n\r\n')
# print (lines)

random.shuffle(lines)

length = len(lines)

for i in range(10):
    i += 1
    with open('data/bagging_1st_donga_10splited_corpus/' +'train_' + str(i) + '.txt', 'w') as f:
        # t = int(length*(i-1)*0.1)
        # tt = int(length*i*0.1)
        # tmp =lines[int(length*(i-1)*0.1):int(length*i*0.1)]
        for line in lines[int(length*(i-1)*0.1):int(length*i*0.1)]:
            f.write(line)
            f.write('\n')
            f.write('\n')



import random
import tensorflow as tf
#
# # with open ('data/knu/train.txt', 'r') as f:
# with open('data/news_data/parsing_set.txt', 'r') as f:
#     lines = f.read()
#
#
#
# lines = lines.split('\n\n')
# # print (lines)
#
# random.shuffle(lines)
#
# length = len(lines)
#
# for i in range(10):
#     i += 1
#     with open('data/news_10splited_corpus/' +'news_' + str(i) + '.txt', 'w') as f:
#         # t = int(length*(i-1)*0.1)
#         # tt = int(length*i*0.1)
#         # tmp =lines[int(length*(i-1)*0.1):int(length*i*0.1)]
#         sentence = ''
#         for line in lines[int(length*(i-1)*0.1):int(length*i*0.1)]:
#             l = line.split('\n')
#             for token in l:
#                 if token.strip() == '':
#                     continue
#                 sentence += token.split()[0] +' '
#
#             f.write('; ' + sentence + '\n')
#             for token in l:
#                 if token.strip() == '':
#                     continue
#                 f.write('0\t0\tTAG\t'+token.split()[1])
#                 f.write('\n')
#             f.write('\n')
#
#             sentence = ''