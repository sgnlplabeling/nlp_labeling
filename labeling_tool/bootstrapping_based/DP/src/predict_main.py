"""
parsing predict main file
"""

import Queue
import time
from config import FLAGS
from predict_parser import YM_PARSER

def predict(bagging_iter=None, input_path=None, mode=None):
    """
    :param bagging_iter:
    :param input_path:
    :param mode:
    :return:
    """
    tmp_time = time.time()
    thread_queue = Queue.Queue()
    pos = FLAGS.pos
    if mode == 'g_predict':
        num_files = 1
    else:
        num_files = FLAGS.num_files

    for file_idx in range(num_files):
        file_idx += 1
        for mode_idx in range(FLAGS.num_models):
            mode_idx += 1

            parser = YM_PARSER(None, mode_idx, pos, file_idx, bagging_iter, input_path, mode=mode)
            thread_queue.put(parser)

        tmp_time = time.time()
        for _q in thread_queue.queue:
            _q.start()

        for _q in thread_queue.queue:
            _q.join()
        print ('1 predict file time , ', time.time() - tmp_time)
        thread_queue = Queue.Queue()

    print ('%sth bagging TOTAL PREDICT TIME : ' % (bagging_iter), time.time() - tmp_time)
