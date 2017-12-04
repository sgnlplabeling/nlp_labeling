import time
import os
from config import FLAGS
FILE_NUM = FLAGS.num_files
MODEL_NUM = FLAGS.num_models
class voting():
    def __init__(self, bagging_iter, mode):
        self._bagging_iter = bagging_iter
        self._before_dict = {}
        self._result_dict = {}
        self.mode = mode
        self.voting_start()


    def voting_start(self):
        if self.mode == 'g_predict':
            FILE_NUM = 1
            for file_idx in range(FILE_NUM):
                file_idx += 1
                self._before_dict = {}
                self._result_dict = {}

                for model_idx in range(MODEL_NUM):
                    model_idx += 1
                    before_voting_path = '../data/tmp_data/%s_g_tmp_data/before_voting/%sth_model_result_%sth_file.txt'

                    with open(before_voting_path % (self._bagging_iter, model_idx, file_idx), 'rb') as f:
                        sentences = f.read().split(b'\n\n')
                        for sentence_idx, sentence in enumerate(sentences):
                            try:
                                sentence = sentence.split('\n')
                            except:
                                print ('ENCODING ERROR : ')
                                with open('../data/log/%sth_bagging_encoding_error.txt' % (self._bagging_iter),
                                          'ab') as f:
                                    f.write(
                                        b'file : ' + str(file_idx).encode() + b'\t model : ' + str(model_idx).encode())
                                    f.write(sentence)
                                    f.write(b'\n\n')
                                    continue

                            if str(sentence_idx)+"$@$"+sentence[0].strip() not in self._before_dict:
                                self._before_dict[str(sentence_idx)+"$@$"+sentence[0].strip()] = {}
                            for line_idx, line in enumerate(sentence[1:]):
                                self._before_dict[str(sentence_idx)+"$@$"+sentence[0].strip()].update(
                                    {'model_' + str(model_idx) + '_' + str(line_idx + 1): line})
                            self._before_dict[str(sentence_idx)+"$@$"+sentence[0].strip()].update({"idx" : sentence_idx})
                self.voting(file_idx)
        else:
            FILE_NUM = FLAGS.num_files
            for file_idx in range(FILE_NUM):
                file_idx += 1
                self._before_dict = {}
                self._result_dict = {}

                for model_idx in range(MODEL_NUM):
                    model_idx += 1
                    if self.mode == 'g_predict':
                        before_voting_path = '../data/tmp_data/%s_g_tmp_data/before_voting/%sth_model_result_%sth_file.txt'
                    else:
                        before_voting_path = '../data/tmp_data/%sth_tmp_data/before_voting/%sth_model_result_%sth_file.txt'

                    with open(before_voting_path % (self._bagging_iter, model_idx, file_idx), 'rb') as f:
                        sentences = f.read().split(b'\n\n')
                        for sentence_idx, sentence in enumerate(sentences):
                            try:
                                sentence = sentence.split('\n')
                            except:
                                print ('ENCODING ERROR : ')
                                with open('../data/log/%sth_bagging_encoding_error.txt' % (self._bagging_iter), 'ab') as f:
                                    f.write(b'file : '+ str(file_idx).encode() + b'\t model : '+ str(model_idx).encode())
                                    f.write(sentence)
                                    f.write(b'\n\n')
                                    continue

                            if sentence[0].strip() not in self._before_dict:
                                self._before_dict[sentence[0].strip()] = {}
                            for line_idx, line in enumerate(sentence[1:]):
                                self._before_dict[sentence[0].strip()].update({'model_'+str(model_idx) + '_' +str(line_idx+1):line})

                self.voting(file_idx)

    def voting(self, file_idx):
        if self.mode == 'g_predict':
            for b_dict in self._before_dict:
                if b_dict.split("$@$")[1].strip() == "":
                    continue

                self._result_dict[b_dict] = self.CKY(self._before_dict[b_dict])

            if not os.path.isdir('../data/g_data/%s_g_tmp_data' % self._bagging_iter):
                os.mkdir('../data/g_data/%s_g_tmp_data' % self._bagging_iter)
            after_voting_path = '../data/g_data/%s_g_tmp_data/after_voting' % (self._bagging_iter)

            if not os.path.isdir(after_voting_path):
                os.mkdir(after_voting_path)

            with open(after_voting_path + '/%sth_file.txt' % (file_idx), 'w') as f:
                sorted_result = sorted(self._result_dict.items(), key=lambda x: x[1]["idx"], reverse=False)
                for r_dict in sorted_result:
                    # print ("r_dict : ", r_dict)
                    r_dict = tuple((r_dict[0].split("$@$")[1], r_dict[1]))

                    if r_dict[0].strip() == "":
                        continue
                    sum = 0.0
                    if len(r_dict[0]) == 0 or r_dict[0].strip() == '':
                        continue

                    for line_idx in r_dict[1]:
                        if line_idx == "idx":
                            continue
                        sum += r_dict[1][line_idx]['score']
                    avg_score = sum / (len(r_dict[1])-1)

                    f.write(r_dict[0] + '\tscore:' + str(avg_score) + '\n')
                    for line_idx in r_dict[1]:
                        if line_idx == "idx":
                            continue
                        f.write(str(r_dict[1][line_idx]['M']) + '\t' + str(
                            r_dict[1][line_idx]['H']) + \
                                '\t' + str(r_dict[1][line_idx]['tag']) + '\t' + str(
                            r_dict[1][line_idx]['token']) + '\n')
                    f.write('\n')
        else:
            for b_dict in self._before_dict:
                if b_dict =='':
                    continue

                self._result_dict[b_dict] = self.CKY(self._before_dict[b_dict])

            after_voting_path = '../data/tmp_data/%sth_tmp_data/after_voting' %(self._bagging_iter)

            if not os.path.isdir(after_voting_path):
                os.mkdir(after_voting_path)

            with open (after_voting_path + '/%sth_file.txt' % (file_idx), 'w') as f:
                for r_dict in self._result_dict:
                    sum = 0.0
                    if len(self._result_dict[r_dict]) == 0 or r_dict.strip() == '':
                        continue

                    for line_idx in self._result_dict[r_dict]:
                        sum += self._result_dict[r_dict][line_idx]['score']

                    avg_score = sum/len(self._result_dict[r_dict])
                    f.write(r_dict +'\tscore:'+str(avg_score)+'\n')
                    for line_idx in self._result_dict[r_dict]:
                        f.write(str(self._result_dict[r_dict][line_idx]['M']) + '\t' + str(self._result_dict[r_dict][line_idx]['H']) +\
                                '\t' + str(self._result_dict[r_dict][line_idx]['tag']) + '\t' + str(self._result_dict[r_dict][line_idx]['token']) +'\n')
                    f.write('\n')

    def CKY(self,sentence):
        k = 0
        if self.mode == "g_predict":
            idx = sentence["idx"]
            del sentence["idx"]

        size = len(sentence)/MODEL_NUM
        CKY_chart = [[{'score2':0.0, 'score':0.0, 'tag':{}} for col in range(size+1)] for row in range(size+1)]

        for i in range(size):
            for model_idx in range(10):
                model_idx+= 1

                M, H, TAG, TOKEN = sentence['model_'+str(model_idx)+'_'+str(i+1)].split('\t')
                CKY_chart[0][i]['token'] = TOKEN[:-1]
                CKY_chart[i][i]['terminal'] = True
                CKY_chart[i][int(H)-1]['score2'] += 0.1

                if TAG not in CKY_chart[i][int(H) - 1]['tag']:
                    CKY_chart[i][int(H) - 1]['tag'][TAG] = 0.1
                else:
                    CKY_chart[i][int(H) - 1]['tag'][TAG] += 0.1

        while (True):
            k += 1
            for i in range(0, size - k +1):
                path = []
                row = i
                col = i + k
                for j in range(i, col):
                    row1 = row
                    col1 = j

                    row2 = j + 1
                    col2 = col

                    cur_socre = CKY_chart[row1][col1]['score'] + CKY_chart[row2][col2]['score'] + \
                                CKY_chart[col1][col2]['score2']

                    if j == i:
                        max_score = cur_socre

                    if cur_socre >= max_score:
                        max_score = cur_socre
                        path.append([(row1, col1), (row2, col2)])

                if path != []:
                    CKY_chart[row][col]['score'] = max_score
                    CKY_chart[row][col]['path'] = path[-1]

            i = 1
            if i == 1 and i + k == len(CKY_chart[0]):
                break

        for arcs_idx, arcs in enumerate(CKY_chart):
            score_sum = 0.0
            for arc_idx, arc in enumerate(arcs):
                if arc_idx == 0 :
                    continue
                score_sum += float(arc['score'])

            if score_sum == 0.0:
                score_sum = 1.0

            for arc_idx, arc in enumerate(arcs):
                CKY_chart[arcs_idx][arc_idx]['score'] = float(arc['score'])/score_sum

        _parse_tree = {}
        _parse_tree = self.back_tracking(0, size - 1, 'ROOT', CKY_chart, _parse_tree)
        if self.mode == "g_predict":
            _parse_tree["idx"] = idx
        return _parse_tree

    def back_tracking(self, row, col, tree, chart, _parse_tree):

        if tree == 'ROOT':
            _parse_tree[col + 1] = {'M': col + 1, 'H': 0, 'token': chart[0][col]['token'], 'score':1.0, 'tag':'VP'}

        if 'path' in chart[row][col]:
            LHS, RHS = chart[row][col]['path']
            score = chart[LHS[1]][RHS[1]]['score2']

            _parse_tree[LHS[1] + 1] = {'M': LHS[1] + 1, 'H': RHS[1] + 1, 'token': chart[0][LHS[1]]['token']}
            _parse_tree[LHS[1] + 1]['score'] = score

            max_tag_id = ''
            max_tag_score = 0.0

            for arc in chart[LHS[1]]:
                tags = arc['tag']
                for tag in tags:
                    if tags[tag] >= max_tag_score:
                        max_tag_id = tag
                        max_tag_score = tags[tag]

            _parse_tree[LHS[1] + 1]['tag'] = max_tag_id
            _parse_tree = self.back_tracking(LHS[0], LHS[1], 'LEFT', chart, _parse_tree) # left tree
            _parse_tree = self.back_tracking(RHS[0], RHS[1], 'RIGHT', chart, _parse_tree) # right tree

        return _parse_tree


