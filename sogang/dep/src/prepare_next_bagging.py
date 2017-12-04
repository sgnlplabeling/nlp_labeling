import os
import random
from config import FLAGS

class prepare():
    def __init__(self, bagging_iter, train_path, test_path, g_score, a_score, scope, mode):
        self.bagging_iter = bagging_iter
        self.g_score = g_score
        self.a_score = a_score
        self.input_path = train_path
        self.test_path = test_path
        self.scope = scope
        self.mode = mode
        self.graded_result = []
        self.prepare_next_bagging()

    def prepare_next_bagging(self):
        if self.mode == 'train':
            self.add_next_bagging_training()
            self.sub_next_bagging_test()
        elif self.mode == 'predict':
            self.voting()
            self.save_gab_result()

    def save_gab_result(self):
        gab_path = '../data/tmp_data/%sth_graded_data' % (int(self.bagging_iter))
        if not os.path.isdir(gab_path):
            os.mkdir(gab_path)

        with open(gab_path+'/graded_result.txt', 'w') as f:
            for g_sentence in self.g_result:
                f.write(g_sentence[0].split('\n')[0] + '\tscore:' + str(g_sentence[1]) + '\tgrade:g\n')
                for sentence in g_sentence[0].split('\n')[1:]:
                    f.write(sentence.strip() +'\n')
                f.write('\n')

            for a_sentence in self.a_result:
                f.write(a_sentence[0].split('\n')[0] + '\tscore:' + str(a_sentence[1]) + '\tgrade:a\n')
                for sentence in a_sentence[0].split('\n')[1:]:
                    f.write(sentence.strip() +'\n')
                f.write('\n')

            for b_sentence in self.b_result:
                f.write(b_sentence[0].split('\n')[0] + '\tscore:' + str(b_sentence[1]) + '\tgrade:b\n')
                for sentence in b_sentence[0].split('\n')[1:]:
                    f.write(sentence.strip() +'\n')
                f.write('\n')

    def voting(self):
        before_sorting = []
        total_sentence = {}

        # read all of after_voting_files
        for file_idx in range(FLAGS.num_files):
            file_idx += 1
            after_voting_path = '../data/tmp_data/%sth_tmp_data/after_voting/%sth_file.txt' % (
            self.bagging_iter, file_idx)
            with open(after_voting_path, 'r') as f:
                lines = f.read()
                lines = lines.split('\n\n')
                before_sorting += lines
        del lines

        # sorting by avg_score
        for line in before_sorting:
            if line.strip() == '':
                continue
            key = ''
            for l_idx, l in enumerate(line.split('\n')):
                # print l
                if l_idx == 0:
                    key = l.split('score:')[0] + '\n'
                # elif l_idx + 1 == len(line.split('\n')):
                #     key += l
                else:
                    key += l + '\n'
            total_sentence[key.strip()] = float(line.split('\n')[0].split('score:')[1])

        del before_sorting
        self.sorted_sentence = sorted(total_sentence.items(), key=lambda x: x[1], reverse=True)
        del total_sentence

        # extract using the alpha
        self.g_result = []
        self.a_result = []
        self.b_result = []
        for sentence in self.sorted_sentence:
            if self.g_score <= float(sentence[1]):
                self.g_result.append((sentence[0], sentence[1]))
                continue

            if self.g_score > float(sentence[1]) and self.a_score <= float(sentence[1]):
                self.a_result.append((sentence[0], sentence[1]))
                continue

            self.b_result.append((sentence[0], sentence[1]))
        del self.sorted_sentence

    def add_next_bagging_training(self):
        training_data = []

        if not os.path.isdir('../data/training_data/% sth_in' % (int(self.bagging_iter))):
            os.mkdir('../data/training_data/% sth_in' % (int(self.bagging_iter)))

        for file_idx in range(FLAGS.num_files):
            file_idx += 1

            if self.bagging_iter == str(1):
                self.input_path = '../data/input_data/training_data'

            if self.input_path == 'default':
                self.input_path = '../data/training_data/%sth_in' % (int(self.bagging_iter)-1)

            cur_bagging_training_path = (self.input_path + '/train_%s.txt') % (file_idx)
            with open(cur_bagging_training_path, 'r') as f:
                lines = f.read().split('\n\n')
                training_data += lines

        del lines

        gab_path = '../data/tmp_data/%sth_graded_data' % (int(self.bagging_iter) - 1)
        with open(gab_path + '/graded_result.txt', 'r') as f:
           lines = f.read().split('\n\n')
        for line in lines:
            if line.strip() == '':
                continue
            grade = line.split('\n')[0].split('grade:')[1]
            if grade == self.scope:
                tmp_line = ''
                for line_idx, l in enumerate(line.split('\n')):
                    if line_idx == 0:
                        tmp_line += str(l.split('score:')[0]) + '\n'
                    else:
                        tmp_line += l +'\n'

                self.graded_result.append(tmp_line)

        training_data += [g for g in self.graded_result]

        random.shuffle(training_data)
        len_training_data = len(training_data)

        next_bagging_training_path = '../data/training_data/%sth_in' % (int(self.bagging_iter))

        if not os.path.isdir(next_bagging_training_path):
            os.mkdir(next_bagging_training_path)

        for file_idx in range(FLAGS.num_files):
            file_idx += 1

            next_bagging_training_path = '../data/training_data/%sth_in/train_%s.txt' % (
            int(self.bagging_iter), file_idx)
            with open(next_bagging_training_path, 'w') as f:
                for sentence in training_data[int(len_training_data * (0.1 * (file_idx - 1))):int(
                                len_training_data * (0.1 * (file_idx)))]:

                    if sentence.strip() == '':
                        continue

                    f.write(sentence.strip())
                    f.write('\n\n')

        del training_data

    def sub_next_bagging_test(self):
        test_data = {}
        # next_bagging_test = cur_bagging_test - top_of_result
        for file_idx in range(FLAGS.num_files):
            file_idx += 1

            if self.test_path == 'default':
                self.test_path = '../data/test_data/%sth_test_data' % (int(self.bagging_iter)-1)
            cur_bagging_test_path = (self.test_path + '/test_%s.txt') % (file_idx)
            with open(cur_bagging_test_path, 'r') as f:
                lines = f.read()
                lines = lines.split('\n\n')
                for line in lines:
                    sentence = line.split('\n')[0]
                    test_data[sentence.strip()] = (line, len(sentence.split()))

        del lines
        scope_result = []
        scope_result += [graded for graded in self.graded_result]


        for tor in scope_result:
            if tor.split('\n')[0].strip() in test_data:
                del test_data[tor.split('\n')[0].strip()]
            else:
                continue

        del self.graded_result

        sorted_test = sorted(test_data.items(), key=lambda x: x[1][1], reverse=True)
        len_sorted_test = len(sorted_test)
        del test_data

        if not os.path.isdir('../data/test_data/%sth_test_data' % (int(self.bagging_iter))):
            os.mkdir('../data/test_data/%sth_test_data' % (int(self.bagging_iter)))

        for file_idx in range(FLAGS.num_files):
            file_idx += 1
            next_bagging_test_path = '../data/test_data/%sth_test_data/test_%s.txt' % (
            int(self.bagging_iter), file_idx)

            with open(next_bagging_test_path, 'w') as f:
                for st in sorted_test[
                          int(len_sorted_test * (0.1 * (file_idx - 1))):int(len_sorted_test * (0.1 * (file_idx)))]:
                    if st[1][0].strip() == '':
                        continue

                    f.write(st[1][0].strip())
                    f.write('\n\n')

