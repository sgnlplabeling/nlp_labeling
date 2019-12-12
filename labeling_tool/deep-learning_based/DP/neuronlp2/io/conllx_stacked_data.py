#-*- coding:utf-8 -*-
__author__ = 'max'

import numpy as np
import torch
from torch.autograd import Variable
from .conllx_data import _buckets, _no_buckets, PAD_ID_WORD, PAD_ID_CHAR, PAD_ID_TAG, UNK_ID, NONE_ID_TAG, NONE_ID_WORD
from .conllx_data import NUM_SYMBOLIC_TAGS
from .conllx_data import create_alphabets
from . import utils
from .reader import CoNLLXReader, etriCoNLLXReader


def _obtain_child_index_for_left2right(heads):
    child_ids = [[] for _ in range(len(heads))]
    # skip the symbolic root.
    for child in range(1, len(heads)):
        head = heads[child]
        child_ids[head].append(child)
    return child_ids


def _obtain_child_index_for_inside_out(heads):
    # heads mean head of that index
    child_ids = [[] for _ in range(len(heads))]
    for head in range(len(heads)):
        # first find left children inside-out
        for child in reversed(list(range(1, head))):
            if heads[child] == head:
                child_ids[head].append(child)
        # second find right children inside-out
        for child in range(head + 1, len(heads)):
            if heads[child] == head:
                child_ids[head].append(child)
    return child_ids


def _obtain_child_index_for_depth(heads, reverse):
    def calc_depth(head):
        children = child_ids[head]
        max_depth = 0
        for child in children:
            depth = calc_depth(child)
            child_with_depth[head].append((child, depth))
            max_depth = max(max_depth, depth + 1)
        child_with_depth[head] = sorted(child_with_depth[head], key=lambda x: x[1], reverse=reverse)
        return max_depth

    child_ids = _obtain_child_index_for_left2right(heads)
    child_with_depth = [[] for _ in range(len(heads))]
    calc_depth(0)
    return [[child for child, depth in child_with_depth[head]] for head in range(len(heads))]


# TODO: 이거 이해하기
def _generate_stack_inputs(heads, types, prior_order, sent):
    # L2R
    # heads is a list
    stacked_heads = []
    children = [0 for _ in range(len(heads) - 1)]
    siblings = []
    previous = []
    nexts = []
    stacked_types = []
    skip_connect = []
    prev = [0 for _ in range(len(heads))]
    sibs = [0 for _ in range(len(heads))]
    newheads = [-1 for _ in range(len(heads))]
    newheads[0] = 0
    position = 1

    for child in range(len(heads)):
        if child == 0: continue
        stacked_heads.append(child)
        if child == len(heads) - 1:
            nexts.append(0)
        else:
            nexts.append(child + 1)
        previous.append(child - 1)
        head = heads[child]
        newheads[child] = head
        siblings.append(sibs[head])
        skip_connect.append(prev[head])
        prev[head] = position
        children[child - 1] = head
        sibs[head] = child
        stacked_types.append(types[child])
        # stacked_types.append(types[0])
        position += 1

    return stacked_heads, children, siblings, stacked_types, skip_connect, previous, nexts

def read_stacked_data(source_path, word_alphabet, char_alphabet, pos_alphabet, type_alphabet, max_size=None,
                      normalize_digits=True, prior_order='deep_first', type=None, elmo=False, bert=False, etri_path=None):
    """
    from data path to list
    """
    buckets = _buckets if type == 'train' else _no_buckets
    is_test = True if type == 'test' else False

    #data = [[] for _ in _buckets]
    #max_char_length = [0 for _ in _buckets]
    data = [[] for _ in buckets]
    max_char_length = [0 for _ in buckets]
    print(('Reading data from %s' % source_path))
    counter = 0
    reader = CoNLLXReader(source_path, word_alphabet, char_alphabet, pos_alphabet, type_alphabet)
    inst = reader.getNext(normalize_digits=normalize_digits, symbolic_root=True, symbolic_end=False, is_test=is_test)    # 한 문장 parsing한 instance

    while inst is not None and (not max_size or counter < max_size):
        counter += 1
        if counter % 10000 == 0:
            print(("reading data: %d" % counter))

        inst_size = inst.length()
        sent = inst.sentence
        #for bucket_id, bucket_size in enumerate(_buckets):
        for bucket_id, bucket_size in enumerate(buckets):
            if inst_size < bucket_size:
                stacked_heads, children, siblings, stacked_types, skip_connect, previous, nexts = _generate_stack_inputs(inst.heads, inst.type_ids, prior_order, sent)
                if elmo:
                    data[bucket_id].append([sent.word_ids, sent.char_id_seqs, inst.pos_ids, inst.heads, inst.type_ids, sent.words,
                                            stacked_heads, children, siblings, stacked_types, skip_connect, previous, nexts])
                else:
                    data[bucket_id].append([sent.word_ids, sent.char_id_seqs, inst.pos_ids, inst.heads, inst.type_ids,
                                            stacked_heads, children, siblings, stacked_types, skip_connect, previous, nexts])
                max_len = max([len(char_seq) for char_seq in sent.char_seqs])
                if max_char_length[bucket_id] < max_len:
                    max_char_length[bucket_id] = max_len
                break

        # QUESTION: why symbols manually..?
        inst = reader.getNext(normalize_digits=normalize_digits, symbolic_root=True, symbolic_end=False, is_test=is_test)
    reader.close()

    # hoon : etri reader for bert
    etri_data = None
    if bert:
        etri_data = [[] for _ in buckets]
        etri_counter = 0
        etri_reader = etriCoNLLXReader(etri_path)
        etri_inst = etri_reader.getNext(normalize_digits=normalize_digits, symbolic_root=True, symbolic_end=False)
        while etri_inst is not None:
            etri_counter += 1
            if etri_counter % 10000 == 0:
                print("reading etri data: %d" % etri_counter)
            etri_size = etri_inst.length()

            for bucket_id, bucket_size in enumerate(buckets):
                if etri_size < bucket_size:
                    etri_data[bucket_id].append(etri_inst.words)
                    break
            etri_inst = etri_reader.getNext(normalize_digits=normalize_digits, symbolic_root=True, symbolic_end=False)
        etri_reader.close()

    print(("Total number of data: %d" % counter))
    if bert:
        print("Total number of etri data: %d" % etri_counter)

    return data, etri_data, max_char_length


def read_stacked_data_to_variable(source_path, word_alphabet, char_alphabet, pos_alphabet, type_alphabet, pos_embedding,
                                  max_size=None, normalize_digits=True, prior_order='deep_first', use_gpu=False, volatile=False, is_test=False, elmo=False, bert=False, etri_path=None):
    """
    from list to numpy -> tensor
    """
    # data is a list
    if not volatile:
        type = 'train'
    elif is_test:
        type = 'test'
    else:
        type = 'dev'
    #type = 'dev' if volatile else 'train'
    buckets = _no_buckets if volatile else _buckets

    data, etri_data, max_char_length = read_stacked_data(source_path, word_alphabet, char_alphabet, pos_alphabet, type_alphabet,
                                              max_size=max_size, normalize_digits=normalize_digits, prior_order=prior_order, type=type, elmo=elmo, bert=bert, etri_path=etri_path)
    #bucket_sizes = [len(data[b]) for b in range(len(_buckets))]
    bucket_sizes = [len(data[b]) for b in range(len(buckets))]

    data_variable = []

    word_elmo = [[] for _ in buckets]

    #for bucket_id in range(len(_buckets)):
    for bucket_id in range(len(buckets)):
        bucket_size = bucket_sizes[bucket_id]
        if bucket_size == 0:
            data_variable.append((1, 1))
            continue

        #bucket_length = _buckets[bucket_id]
        bucket_length = buckets[bucket_id]
        char_length = min(utils.MAX_CHAR_LENGTH, max_char_length[bucket_id] + utils.NUM_CHAR_PAD)
        wid_inputs = np.empty([bucket_size, bucket_length, pos_embedding], dtype=np.int64)    # NOTE: pos_embedding! # of word and pos used same!
        cid_inputs = np.empty([bucket_size, bucket_length, char_length], dtype=np.int64)
        pid_inputs = np.empty([bucket_size, bucket_length, pos_embedding], dtype=np.int64)
        hid_inputs = np.empty([bucket_size, bucket_length], dtype=np.int64)
        tid_inputs = np.empty([bucket_size, bucket_length], dtype=np.int64)

        masks_e = np.zeros([bucket_size, bucket_length], dtype=np.float32)
        single = np.zeros([bucket_size, bucket_length, pos_embedding], dtype=np.int64)
        lengths_e = np.empty(bucket_size, dtype=np.int64)

        stack_hid_inputs = np.empty([bucket_size, bucket_length - 1], dtype=np.int64)
        chid_inputs = np.empty([bucket_size, bucket_length - 1], dtype=np.int64)
        ssid_inputs = np.empty([bucket_size, bucket_length - 1], dtype=np.int64)
        stack_tid_inputs = np.empty([bucket_size, bucket_length - 1], dtype=np.int64)
        skip_connect_inputs = np.empty([bucket_size, bucket_length - 1], dtype=np.int64)
        previous_inputs = np.empty([bucket_size, bucket_length - 1], dtype=np.int64)
        nexts_inputs = np.empty([bucket_size, bucket_length - 1], dtype=np.int64)

        masks_d = np.zeros([bucket_size, bucket_length - 1], dtype=np.float32)
        lengths_d = np.empty(bucket_size, dtype=np.int64)

        for i, inst in enumerate(data[bucket_id]):    # data is a list
            if elmo:
                wids, cid_seqs, pids, hids, tids, w, stack_hids, chids, ssids, stack_tids, skip_ids, previous_ids, nexts_ids = inst
                word_elmo[bucket_id].append(w)
            else:
                wids, cid_seqs, pids, hids, tids, stack_hids, chids, ssids, stack_tids, skip_ids, previous_ids, nexts_ids = inst

            inst_size = len(wids)
            lengths_e[i] = inst_size

            # NOTE: padding can be done with pad_sequence
            # and packing is also possible!
            # word ids
            if pos_embedding == 2:
                for j in range(inst_size):
                    wid_inputs[i, j, 0] = wids[j][0]
                    wid_inputs[i, j, 1] = wids[j][-1]
                wid_inputs[i, inst_size:, :] = PAD_ID_WORD
            elif pos_embedding == 4:
                for j in range(inst_size):
                    if len(wids[j]) <= 2:
                        wid_inputs[i, j, 0] = wids[j][0]
                        wid_inputs[i, j, 1] = NONE_ID_WORD
                        wid_inputs[i, j, 2] = NONE_ID_WORD
                        wid_inputs[i, j, 3] = wids[j][-1]
                    else:
                        wid_inputs[i, j, 0] = wids[j][0]
                        wid_inputs[i, j, 1] = wids[j][1]
                        wid_inputs[i, j, 2] = wids[j][-2]
                        wid_inputs[i, j, 3] = wids[j][-1]
                wid_inputs[i, inst_size:, :] = PAD_ID_WORD

            for c, cids in enumerate(cid_seqs):
                cid_inputs[i, c, :len(cids)] = cids
                cid_inputs[i, c, len(cids):] = PAD_ID_CHAR
            cid_inputs[i, inst_size:, :] = PAD_ID_CHAR

            # pos ids
            if pos_embedding == 2:
                for j in range(inst_size):
                    pid_inputs[i, j, 0] = pids[j][0]
                    pid_inputs[i, j, 1] = pids[j][-1]
                pid_inputs[i, inst_size:, :] = PAD_ID_TAG
            elif pos_embedding == 4:
                for j in range(inst_size):
                    if len(pids[j]) <= 2:
                        pid_inputs[i, j, 0] = pids[j][0]
                        pid_inputs[i, j, 1] = NONE_ID_TAG    # FIXME: 뭘로 채운다고?
                        pid_inputs[i, j, 2] = NONE_ID_TAG
                        pid_inputs[i, j, 3] = pids[j][-1]
                    else:
                        pid_inputs[i, j, 0] = pids[j][0]
                        pid_inputs[i, j, 1] = pids[j][1]
                        pid_inputs[i, j, 2] = pids[j][-2]
                        pid_inputs[i, j, 3] = pids[j][-1]
                pid_inputs[i, inst_size:, :] = PAD_ID_TAG

            if not is_test:
                # type ids
                tid_inputs[i, :inst_size] = tids
                tid_inputs[i, inst_size:] = PAD_ID_TAG
                # heads
                hid_inputs[i, :inst_size] = hids
                hid_inputs[i, inst_size:] = PAD_ID_TAG
            # masks_e
            masks_e[i, :inst_size] = 1.0
            for j, wid in enumerate(wids):
                # if word_alphabet.is_singleton(wid):
                #     single[i, j] = 1
                if pos_embedding == 2:
                    if word_alphabet.is_singleton(wid[0]):
                        single[i, j, 0] = 1
                    if word_alphabet.is_singleton(wid[-1]):
                        single[i, j, 1] = 1
                elif pos_embedding == 4:
                    if len(wids[j]) <= 2:
                        if word_alphabet.is_singleton(wid[-1]):
                            single[i, j, 0] = 1
                        # single[i, j, 1] =             # FIXME: pad는 singleton 아니지?
                        # single[i, j, 2] =
                        if word_alphabet.is_singleton(wid[-1]):
                            single[i, j, 3] = 1
                    else:
                        if word_alphabet.is_singleton(wid[0]):
                            single[i, j, 0] = 1
                        if word_alphabet.is_singleton(wid[1]):
                            single[i, j, 1] = 1
                        if word_alphabet.is_singleton(wid[-2]):
                            single[i, j, 2] = 1
                        if word_alphabet.is_singleton(wid[-1]):
                            single[i, j, 3] = 1
            
            # L2R
            inst_size_decoder = inst_size - 1
            lengths_d[i] = inst_size_decoder
            # masks_d
            masks_d[i, :inst_size_decoder] = 1.0

            # L2R
            # stacked heads
            stack_hid_inputs[i, :inst_size_decoder] = stack_hids
            stack_hid_inputs[i, inst_size_decoder:] = PAD_ID_TAG
            previous_inputs[i, :inst_size_decoder] = previous_ids
            previous_inputs[i, inst_size_decoder:] = PAD_ID_TAG
            nexts_inputs[i, :inst_size_decoder] = nexts_ids
            nexts_inputs[i, inst_size_decoder:] = PAD_ID_TAG

            if not is_test:
                # stacked types
                stack_tid_inputs[i, :inst_size_decoder] = stack_tids
                stack_tid_inputs[i, inst_size_decoder:] = PAD_ID_TAG
                # children
                chid_inputs[i, :inst_size_decoder] = chids
                chid_inputs[i, inst_size_decoder:] = PAD_ID_TAG
                # siblings
                ssid_inputs[i, :inst_size_decoder] = ssids
                ssid_inputs[i, inst_size_decoder:] = PAD_ID_TAG
                # skip connects
                skip_connect_inputs[i, :inst_size_decoder] = skip_ids
                skip_connect_inputs[i, inst_size_decoder:] = PAD_ID_TAG

        # 2to3
        if volatile:
            with torch.no_grad():
                # from instance
                words = Variable(torch.from_numpy(wid_inputs))
                chars = Variable(torch.from_numpy(cid_inputs))
                pos = Variable(torch.from_numpy(pid_inputs))
                heads = Variable(torch.from_numpy(hid_inputs))
                types = Variable(torch.from_numpy(tid_inputs))
                masks_e = Variable(torch.from_numpy(masks_e))
                single = Variable(torch.from_numpy(single))
                # from stackptr
                stacked_heads = Variable(torch.from_numpy(stack_hid_inputs))
                children = Variable(torch.from_numpy(chid_inputs))
                siblings = Variable(torch.from_numpy(ssid_inputs))
                stacked_types = Variable(torch.from_numpy(stack_tid_inputs))
                previous = Variable(torch.from_numpy(previous_inputs))
                nexts = Variable(torch.from_numpy(nexts_inputs))
                masks_d = Variable(torch.from_numpy(masks_d))
        else:
            # from instance
            words = Variable(torch.from_numpy(wid_inputs))
            chars = Variable(torch.from_numpy(cid_inputs))
            pos = Variable(torch.from_numpy(pid_inputs))
            heads = Variable(torch.from_numpy(hid_inputs))
            types = Variable(torch.from_numpy(tid_inputs))
            masks_e = Variable(torch.from_numpy(masks_e))
            single = Variable(torch.from_numpy(single))
            # from stackptr
            stacked_heads = Variable(torch.from_numpy(stack_hid_inputs))
            children = Variable(torch.from_numpy(chid_inputs))
            siblings = Variable(torch.from_numpy(ssid_inputs))
            stacked_types = Variable(torch.from_numpy(stack_tid_inputs))
            previous = Variable(torch.from_numpy(previous_inputs))
            nexts = Variable(torch.from_numpy(nexts_inputs))
            masks_d = Variable(torch.from_numpy(masks_d))

        # from instance
        lengths_e = torch.from_numpy(lengths_e)
        # from stackptr
        skip_connect = torch.from_numpy(skip_connect_inputs)
        lengths_d = torch.from_numpy(lengths_d)

        if use_gpu:
            words = words.cuda()
            chars = chars.cuda()
            pos = pos.cuda()
            heads = heads.cuda()
            types = types.cuda()
            masks_e = masks_e.cuda()
            single = single.cuda()
            lengths_e = lengths_e.cuda()
            stacked_heads = stacked_heads.cuda()
            children = children.cuda()
            siblings = siblings.cuda()
            stacked_types = stacked_types.cuda()
            skip_connect = skip_connect.cuda()
            previous = previous.cuda()
            nexts = nexts.cuda()
            masks_d = masks_d.cuda()
            lengths_d = lengths_d.cuda()

        if elmo:
            data_variable.append(((words, chars, pos, heads, types, masks_e, single, lengths_e, word_elmo[bucket_id]),
                                  (stacked_heads, children, siblings, stacked_types, skip_connect, previous, nexts, masks_d, lengths_d)))

        else:
            data_variable.append(((words, chars, pos, heads, types, masks_e, single, lengths_e),
                              (stacked_heads, children, siblings, stacked_types, skip_connect, previous, nexts, masks_d, lengths_d)))

    return data_variable, etri_data, bucket_sizes

# NOTE: train시 데이터 불러오기로 사용!
def get_batch_stacked_variable(data, batch_size, pos_embedding, unk_replace=0., elmo=False, bert=False):
    data_variable, word_bert, bucket_sizes = data
    total_size = float(sum(bucket_sizes))
    # A bucket scale is a list of increasing numbers from 0 to 1 that we'll use
    # to select a bucket. Length of [scale[i], scale[i+1]] is proportional to
    # the size if i-th training bucket, as used later.
    buckets_scale = [sum(bucket_sizes[:i + 1]) / total_size for i in range(len(bucket_sizes))]

    # Choose a bucket according to data distribution. We pick a random number
    # in [0, 1] and use the corresponding interval in train_buckets_scale.
    random_number = np.random.random_sample()
    bucket_id = min([i for i in range(len(buckets_scale)) if buckets_scale[i] > random_number])
    bucket_length = _buckets[bucket_id]

    data_encoder, data_decoder = data_variable[bucket_id]

    if elmo:
        words, chars, pos, heads, types, masks_e, single, lengths_e, word_elmo = data_encoder
    else:
        words, chars, pos, heads, types, masks_e, single, lengths_e = data_encoder

    stacked_heads, children, siblings, stacked_types, skip_connect, previous, nexts, masks_d, lengths_d = data_decoder
    bucket_size = bucket_sizes[bucket_id]
    batch_size = min(bucket_size, batch_size)

    index = torch.randperm(bucket_size).long()[:batch_size]
    if words.is_cuda:
        index = index.cuda()

    # index가 1차원 tensor니까 인덱싱해도 words는 3차원!
    words = words[index]
    index_int_list = index.tolist()
    word_elmo_input = []
    if elmo:
        for index_int in index_int_list:
            word_elmo_input.append(word_elmo[index_int])

    #hoon: bert
    word_bert_input = []
    word_bert = word_bert[bucket_id]
    if bert:
        for index_int in index_int_list:
            word_bert_input.append(word_bert[index_int])

    if unk_replace:
        ones = Variable(single.data.new(batch_size, bucket_length, pos_embedding).fill_(1))
        noise = Variable(masks_e.data.new(batch_size, bucket_length, pos_embedding).bernoulli_(unk_replace).long())
        words = words * (ones - single[index] * noise)

    # returns input_encoder, input_decoder
    if elmo:
        return (words, chars[index], pos[index], heads[index], types[index], masks_e[index], lengths_e[index], word_elmo_input, word_bert_input), \
               (stacked_heads[index], children[index], siblings[index], stacked_types[index], skip_connect[index], previous[index], nexts[index], masks_d[index], lengths_d[index])
    else:
        return (words, chars[index], pos[index], heads[index], types[index], masks_e[index], lengths_e[index], word_bert_input), \
               (stacked_heads[index], children[index], siblings[index], stacked_types[index], skip_connect[index], previous[index], nexts[index], masks_d[index], lengths_d[index])

# dev, test load시 사용
def iterate_batch_stacked_variable(data, batch_size, pos_embedding, unk_replace=0., shuffle=False, type=None, elmo=False, bert=False):
    buckets = _no_buckets if type =='dev' else _buckets

    data_variable, word_bert, bucket_sizes = data

    #bucket_indices = np.arange(len(_buckets))
    bucket_indices = np.arange(len(buckets))
    if shuffle:
        np.random.shuffle((bucket_indices))

    for bucket_id in bucket_indices:
        bucket_size = bucket_sizes[bucket_id] # bucket 안에 개수
        #bucket_length = _buckets[bucket_id] # ~ 최대 길이
        bucket_length = buckets[bucket_id]  # ~ 최대 길이
        if bucket_size == 0:
            continue
        data_encoder, data_decoder = data_variable[bucket_id]

        if elmo :
            words, chars, pos, heads, types, masks_e, single, lengths_e, word_elmo = data_encoder
        else :
            words, chars, pos, heads, types, masks_e, single, lengths_e = data_encoder

        input_word_bert = None
        if bert:
            input_word_bert = word_bert[bucket_id]

        stacked_heads, children, siblings, stacked_types, skip_connect, previous, nexts, masks_d, lengths_d = data_decoder
        if unk_replace:
            ones = Variable(single.data.new(bucket_size, bucket_length, pos_embedding).fill_(1))
            noise = Variable(masks_e.data.new(bucket_size, bucket_length, pos_embedding).bernoulli_(unk_replace).long())
            words = words * (ones - single * noise)


        indices = None
        if shuffle:
            indices = torch.randperm(bucket_size).long()
            if words.is_cuda:
                indices = indices.cuda()
        for start_idx in range(0, bucket_size, batch_size):
            if shuffle:
                excerpt = indices[start_idx:start_idx + batch_size]
            else:
                excerpt = slice(start_idx, start_idx + batch_size)

            if elmo:
                yield (words[excerpt], chars[excerpt], pos[excerpt], heads[excerpt], types[excerpt], masks_e[excerpt],
                       lengths_e[excerpt], word_elmo[excerpt], input_word_bert[excerpt]), \
                      (stacked_heads[excerpt], children[excerpt], siblings[excerpt], stacked_types[excerpt],
                       skip_connect[excerpt], previous[excerpt], nexts[excerpt], masks_d[excerpt], lengths_d[excerpt])
            else:
                yield (words[excerpt], chars[excerpt], pos[excerpt], heads[excerpt], types[excerpt], masks_e[excerpt],
                       lengths_e[excerpt], input_word_bert[excerpt]), \
                      (stacked_heads[excerpt], children[excerpt], siblings[excerpt], stacked_types[excerpt],
                       skip_connect[excerpt], previous[excerpt], nexts[excerpt], masks_d[excerpt], lengths_d[excerpt])
