import os
from config import FLAGS

def sorting(bagging_iter, output_path=None, mode=None, g_score=None, a_score=None):
    """
    :param bagging_iter:
    :param output_path:
    :param mode:
    :param g_score:
    :param a_score:
    :return: sorted result
    """

    if mode == 'g_predict':
        before_sorting_path = '../data/g_data/%s_g_tmp_data/after_voting/1th_file.txt' \
                              % (bagging_iter)
        with open(before_sorting_path, 'r') as f:
            lines = f.read()
            lines = lines.split('\n\n')

        after_sorting_path = output_path + '/output_file.txt'
        with open(after_sorting_path, 'w') as f:
            for sentence in lines:
                if sentence.strip() == "":
                    continue
                iter_sentence = sentence.split('\n')
                for line_idx, line in enumerate(iter_sentence):
                    if line_idx == 0:
                        score = sentence.split("\n")[0].split("score:")[1]

                        if float(score) >= float(g_score):
                            grade = 'g'
                        elif float(score) >= float(a_score):
                            grade = 'a'
                        else:
                            grade = 'b'
                        f.write(line + '\tgrade:'+grade +'\n')
                    else:
                        f.write(line+'\n')
                f.write('\n')

    else:
        result = {}
        num_files = FLAGS.num_files
        for file_idx in range(num_files):
            file_idx += 1
            before_sorting_path = '../data/g_data/%s_g_tmp_data/after_voting/%sth_file.txt' \
                                  % (bagging_iter, file_idx)
            with open(before_sorting_path, 'r') as f:
                lines = f.read()
                lines = lines.split('\n\n')

                for line in lines:
                    if line.strip() == '':
                        continue
                    key = ''
                    for l_idx, l_tmp in enumerate(line.split('\n')):
                        if l_idx == 0:
                            key = l_tmp.split('score:')[0] + '\n'
                        else:
                            key += l_tmp + '\n'

                    result[key.strip()] = float(line.split('\n')[0].split('score:')[1])

        del lines
        sorted_result = sorted(result.items(), key=lambda x: x[1], reverse=True)
        del result

        len_sorted_result = len(sorted_result)

        if not os.path.isdir('../data/g_data/%s_g_final_data'%(bagging_iter)):
            os.mkdir('../data/g_data/%s_g_final_data'%(bagging_iter))

        num_files = FLAGS.num_files
        for file_idx in range(num_files):
            file_idx += 1
            after_sorting_path = '../data/g_data/%s_g_final_data/%s_file.txt' % (bagging_iter, file_idx)
            with open(after_sorting_path, 'w') as f:
                for sentence in sorted_result[int(len_sorted_result * (0.1 * (file_idx - 1))):\
                        int(len_sorted_result * (0.1 * (file_idx)))]:
                    for line_idx, line in enumerate(sentence[0].split('\n')):
                        if line_idx == 0:
                            f.write(line + '\tscore:' + str(sentence[1])+'\n')
                        else:
                            f.write(line+'\n')
                    f.write('\n')
