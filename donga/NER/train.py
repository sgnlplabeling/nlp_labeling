# -*- coding: UTF-8 -*-
from __future__ import print_function
import optparse
import itertools
from collections import OrderedDict
import loader
import torch
import time
import cPickle
from torch.autograd import Variable
import sys
from utils import *
from loader import *
from model import BiLSTM_CRF
reload(sys)
sys.setdefaultencoding('utf-8')
t = time.time()
models_path = "models/"
eval_path = "output/"
eval_temp = os.path.join(eval_path, "temp")
eva_script = os.path.join(eval_path, "conlleval")

optparser = optparse.OptionParser()
optparser.add_option(
    "-T", "--train", default="",
    help="Train set location"
)
optparser.add_option(
    "-d", "--dev", default="",
    help="Dev set location"
)
optparser.add_option(
    "-t", "--test", default="",
    help="Test set location"
)
optparser.add_option(
    '--score', default='evaluation/temp/score.txt',
    help='score file location'
)
optparser.add_option(
    "-s", "--tag_scheme", default="iob",
    help="Tagging scheme (IOB or IOBES)"
)
optparser.add_option(
    "-l", "--lower", default="0",
    type='int', help="Lowercase words (this will not affect character inputs)"
)
optparser.add_option(
    "-z", "--zeros", default="1",
    type='int', help="Replace digits with 0"
)
optparser.add_option(
    "-g", "--plus_tag", default = "1",
    type = 'int', help = '1:word/tag, 0:word'
)
optparser.add_option(
    "-c", "--char_dim", default="32",
    type='int', help="Character embedding dimension"
)
optparser.add_option(
    "-C", "--char_emb", default="dataset/Syla_Embeddings_size32.pkl",
    help="Location of pretrained character embedding"
)
optparser.add_option(
    "--is_char_emb", default="1",
    type = "int", help="Decide to use pretrained character embedding 0:Random character embedding, 1:pre trained character embedding")

optparser.add_option(
    "-q", "--char_lstm_dim", default = "64",
    type = "int", help="character lstm dim")

optparser.add_option(
    "-b", "--char_bidirect", default="1",
    type='int', help="Use a bidirectional LSTM for chars"
)
optparser.add_option(
    "-w", "--word_dim", default="64",
    type='int', help="Token embedding dimension"
)
optparser.add_option(
    "-W", "--word_lstm_dim", default="128",
    type='int', help="Token LSTM hidden layer size"
)
optparser.add_option(
    "-B", "--word_bidirect", default="1",
    type='int', help="Use a bidirectional LSTM for words"
)
optparser.add_option(
    "-p", "--pre_emb", default="dataset/word_Embeddings_size64.pkl",
    help="Location of pretrained embeddings"
)
optparser.add_option(
    "--is_pre_emb", default="1",
    type='int', help="Decide to use pretrained word embeddings 0:Random Embedding, 1:pre trained embedding "
    )
optparser.add_option(
    "-A", "--all_emb", default="0",
    type='int', help="Load all embeddings"
)
optparser.add_option(
    "-a", "--cap_dim", default="0",
    type='int', help="Capitalization feature dimension (0 to disable)"
)
optparser.add_option(
    "-f", "--crf", default="1",
    type='int', help="Use CRF (0 to disable)"
)
optparser.add_option(
    "-D", "--dropout", default="0.5",
    type='float', help="Droupout on the input (0 = no dropout)"
)
optparser.add_option(
    "-r", "--reload", default="0",
    type='int', help="Reload the last saved model"
)
optparser.add_option(
    "-P", '--use_gpu', default='0',
    type='int', help='whether or not to ues gpu'
)
optparser.add_option(
    '--loss', default='loss.txt',
    help='loss file location'
)
optparser.add_option(
    '--name', default='test',
    help='model name'
)

optparser.add_option(
    '-m', '--mode', default='1',
    type='int', help='Select train mode or test mode, 1 = train mode, 0 = test mode'
)

opts = optparser.parse_args()[0]

parameters = OrderedDict()
parameters['tag_scheme'] = opts.tag_scheme
parameters['lower'] = opts.lower == 1
parameters['zeros'] = opts.zeros == 1
parameters['char_dim'] = opts.char_dim
parameters['char_emb'] = opts.char_emb
parameters['char_bidirect'] = opts.char_bidirect == 1
parameters['word_dim'] = opts.word_dim
parameters['word_lstm_dim'] = opts.word_lstm_dim
parameters['word_bidirect'] = opts.word_bidirect == 1
parameters['char_lstm_dim'] = opts.char_lstm_dim
parameters['is_char_emb'] = opts.is_char_emb
parameters['pre_emb'] = opts.pre_emb
parameters['is_pre_emb'] = opts.is_pre_emb
parameters['all_emb'] = opts.all_emb == 1
parameters['cap_dim'] = opts.cap_dim
parameters['crf'] = opts.crf == 1
parameters['dropout'] = opts.dropout
parameters['reload'] = opts.reload == 1
parameters['name'] = opts.name
parameters['mode'] = opts.mode

parameters['use_gpu'] = opts.use_gpu == 1 and torch.cuda.is_available()
use_gpu = parameters['use_gpu']
if opts.plus_tag ==1:
    parameters['plus_tag'] = True
else:
    parameters['plus_tag'] = False

mapping_file = 'models/mapping.pkl'

name = parameters['name']
model_name = models_path + name #get_name(parameters)
tmp_model = model_name + '.tmp'


assert os.path.isfile(opts.train)
assert os.path.isfile(opts.dev)
assert os.path.isfile(opts.test)
assert parameters['char_dim'] > 0 or parameters['word_dim'] > 0
assert 0. <= parameters['dropout'] < 1.0
assert parameters['tag_scheme'] in ['iob', 'iobes']
assert parameters['word_dim'] > 0
if parameters['is_pre_emb']:
    assert not parameters['pre_emb'] or os.path.isfile(parameters['pre_emb'])
if parameters['is_char_emb']:
    assert not parameters['char_emb'] or os.path.isfile(parameters['char_emb'])

if not os.path.isfile(eval_script):
    raise Exception('CoNLL evaluation script not found at "%s"' % eval_script)
if not os.path.exists(eval_temp):
    os.makedirs(eval_temp)
if not os.path.exists(models_path):
    os.makedirs(models_path)
 
lower = parameters['lower']
zeros = parameters['zeros']
tag_scheme = parameters['tag_scheme']
plus_tag = parameters['plus_tag']

#Load train, dev, test data
#Load sentences = [[word, feature, ..., feature, tag], ..., [word,feature, ..., feature, ..., tag]]
#sth_sentences = [sentence, sentence, ..., sentence]
#zeors 1이면 모든 숫자 0으로 변환
#lower 1이면 모두 소문자로 변환
#마지막 파라미터 True면 word를 word/pos로 변환 
train_sentences = loader.load_sentences(opts.train, lower, zeros, plus_tag)
dev_sentences = loader.load_sentences(opts.dev, lower, zeros, plus_tag)
test_sentences = loader.load_sentences(opts.test, lower, zeros, plus_tag)

#Decide tag scheme
#코퍼스에 있는 기존 태그형태를 iob 또는 iobes태그로 변
update_tag_scheme(train_sentences, tag_scheme)
update_tag_scheme(dev_sentences, tag_scheme)
update_tag_scheme(test_sentences, tag_scheme)

#Create a dictionary / mapping of words
#If we use pretrained embeddings, we add them to the dictionary.
# dico_words_train : key = word, value=tf
#'<UNK>'를 1000000 value를 갖도록 추가  -> UNK가 0번 id를 갖도록 함
#pre_emb하면 train data에 없는 단어의 value를 0으로 추가
#word_to_id : key = word, value = id 빈도수가 가장 높은 word의 id를 0으로 시작해서 순차적으로 매핑
#id_to_word: key = id, value = word
dico_words, word_to_id, id_to_word = word_mapping(train_sentences, lower)
dico_words_train = dico_words
dico_chars, char_to_id, id_to_char = char_mapping(train_sentences)
dico_tags, tag_to_id, id_to_tag = tag_mapping(train_sentences)
dico_mor, mor_to_id ,id_to_mor = mor_mapping(train_sentences)


#Make train, dev, test data
train_data = prepare_dataset(
    train_sentences, word_to_id, char_to_id, tag_to_id, mor_to_id, lower
)
dev_data = prepare_dataset(
    dev_sentences, word_to_id, char_to_id, tag_to_id, mor_to_id, lower
)
test_data = prepare_dataset(
    test_sentences, word_to_id, char_to_id, tag_to_id, mor_to_id, lower
)

print("%i / %i / %i sentences in train / dev / test." % (
    len(train_data), len(dev_data), len(test_data)))

all_word_embeds = {}
all_char_embeds = {}

#Initialize random embeddings
word_embeds = np.random.uniform(-np.sqrt(0.06), np.sqrt(0.06), (len(word_to_id), opts.word_dim))
char_embeds = np.random.uniform(-np.sqrt(0.06), np.sqrt(0.06), (len(char_to_id), opts.char_dim))

#pretrained 워드 임베딩이 존재한다면 적용하고 존재하지 않으면 랜덤 사용
if parameters['is_pre_emb']:
	with open(opts.pre_emb, 'rb') as wf:
		data_list = []
		while(True):
			try:
				data = cPickle.load(wf)
			except EOFError:
				break
			data_list.append(data)
	for i, line in enumerate(data_list):
		s = line.strip().split()
		if len(s) == parameters['word_dim'] +1:
			all_word_embeds[s[0]] = np.array([float(i) for i in s[1:]])
	for w in word_to_id:
		if w in all_word_embeds:
			word_embeds[word_to_id[w]] = all_word_embeds[w]
		elif w.lower() in all_word_embeds:
			word_embeds[word_to_id[w]] = all_word_embeds[w.lower()]
	print('Loaded %i pretrained word embeddings.' % len(all_word_embeds))
else:
	print('Not exist pretrained word embeddings')

#pretrained 음절 임베딩이 존재한다면 적용하고 존재하지 않으면 랜덤 사용
if parameters['is_char_emb']:
	with open(opts.char_emb, 'rb') as cf:
		data_list = []
		while(True):
			try:
				data = cPickle.load(cf)
			except EOFError:
				break
			data_list.append(data)
	for i, line in enumerate(data_list):
		s = line.strip().split()
		if len(s) == parameters['char_dim']+1:
			all_char_embeds[s[0]] = np.array([float(i) for i in s[1:]])
	for c in char_to_id:
		if c in all_char_embeds:
			char_embeds[char_to_id[c]] = all_char_embeds[c]
		elif c.lower() in all_char_embeds:
			char_embeds[char_to_id[c]] = all_char_embeds[c.lower()]
	print('Loaded %i pretrained char embeddings' % len(all_char_embeds))
else:
	print('Not exist pretrained character embeddings')

with open(mapping_file, 'wb') as f:
    mappings = {
        'word_to_id': word_to_id,
        'tag_to_id': tag_to_id,
        'char_to_id': char_to_id,
        'parameters': parameters,
	'mor_to_id' : mor_to_id,
        'word_embeds': word_embeds
    }
    cPickle.dump(mappings, f)

#Model Load
model = BiLSTM_CRF(word_to_ix=word_to_id, tag_to_ix=tag_to_id, char_to_ix = char_to_id, mor_to_ix = mor_to_id,
    embedding_dim=parameters['word_dim'], hidden_dim=parameters['word_lstm_dim'], char_lstm_dim=parameters['char_lstm_dim'],
    char_dim = parameters['char_dim'], pre_word_embeds=word_embeds,
    pre_char_embeds = char_embeds, use_gpu=parameters['use_gpu'], use_crf=parameters['crf'])


if parameters['reload']:
    model.load_state_dict(torch.load(model_name))
if use_gpu:
    model.cuda()
learning_rate = 0.001
optimizer = torch.optim.Adam(model.parameters(), lr=learning_rate)
losses = []
loss = 0.0
best_test = -np.inf
best_dev_F = -1.0
best_test_F = -1.0
best_train_F = -1.0
all_F = [[0, 0, 0]]
plot_every = 50
eval_every = 500
count = 0
dev_list = []
n_epoch = 100
sys.stdout.flush()

#성능 평가 함수
def evaluating(model, datas):
    prediction = []
    save = False
    new_F = 0.0
    confusion_matrix = torch.zeros((len(tag_to_id)-2, len(tag_to_id)-2))
    for data in datas:
        ground_truth_id = data['tags']
        words = data['str_words']
        caps = data['caps']
        mors = data['mor']
        chars2 = data['chars']

        chars2_sorted = sorted(chars2, key = lambda p: len(p), reverse=True)
        d = {}
        for i, ci in enumerate(chars2):
            for j, cj in enumerate(chars2_sorted):
                if ci == cj and not j in d and not i in d.values():
                    d[j] = i
                    continue
        chars2_length = [len(c) for c in chars2_sorted]
        char_maxl = max(chars2_length)
        chars2_mask = np.zeros((len(chars2_sorted), char_maxl), dtype = 'int')
        for i, c in enumerate(chars2_sorted):
            chars2_mask[i, :chars2_length[i]] = c
        chars2_mask = Variable(torch.LongTensor(chars2_mask))

        #Transform list data form to LongTensor data form
        dwords = Variable(torch.LongTensor(data['words']))
        dmor = Variable(torch.LongTensor(mors))
        dcaps = Variable(torch.LongTensor(caps))

        if use_gpu:
            val, out = model(dwords.cuda(), dmor.cuda(), dcaps.cuda(),
                chars2_mask.cuda(), chars2_length, d)
        else:
            val, out = model(dwords, dmor, dcaps,
                chars2_mask, chars2_length, d)

        predicted_id = out
        for (word, true_id, pred_id) in zip (words, ground_truth_id, predicted_id):
            line = ' '.join([word, id_to_tag[true_id], id_to_tag[pred_id]])
            prediction.append(line)
            confusion_matrix[true_id, pred_id] +=1
        prediction.append('')
    predf = eval_temp + '/pred.' + name
    scoref = eval_temp + '/score.' + name

    with open(predf, 'wb') as f:
        f.write('\n'.join(prediction))

    os.system('%s < %s > %s' %(eval_script, predf, scoref))
    eval_lines = [l.rstrip() for l in codecs.open(scoref, 'r', 'utf8')]

    for i, line in enumerate(eval_lines):
        print(line)
        if i==1:
            new_F = float(line.strip().split()[-1])

    print((("{: >2}{: >7}%s{: >9}") % ("{: >7}" * confusion_matrix.size(0))).format(
        "ID", "NE", "Total", * ([id_to_tag[i] for i in range(confusion_matrix.size(0))]+["Percent"])
        ))
    for i in range(confusion_matrix.size(0)):
        print(("{: >2}{: >7}%s{: >9}" % ("{: >7}" * confusion_matrix.size(0))).format(
            str(i), id_to_tag[i], str(confusion_matrix[i].sum()),
            *([confusion_matrix[i][j] for j in range(confusion_matrix.size(0))] + 
                ["%.3f" % (confusion_matrix[i][i] * 100. /max(1, confusion_matrix[i].sum()))])
            ))

    return new_F, save

#parameter['mode']가 1이면 Train Mode 0이면 Test Mode로 적용
if parameters['mode']:
    model.train(True)
    for epoch in range(1, n_epoch+1):
        start_epoch_tim = time.time()
        epoch_costs = []
        for i, index in enumerate(np.random.permutation(len(train_data))):
            tr = time.time()
            count += 1
            data = train_data[index]
            model.zero_grad()
            sentence_in = data['words']
            tags = data['tags']
            chars2 = data['chars']
            mors = data['mor']

            chars2_sorted = sorted(chars2, key=lambda p: len(p), reverse = True)
            d = {}
            for a, ci in enumerate(chars2):
                for j, cj in enumerate(chars2_sorted):
                    if ci == cj and not j in d and not a in d.values():
                        d[j] = a
                        continue
            chars2_length = [len(c) for c in chars2_sorted]
            char_maxl = max(chars2_length)
            chars2_mask = np.zeros((len(chars2_sorted), char_maxl), dtype = 'int')
            for a, c in enumerate(chars2_sorted):
                chars2_mask[a, : chars2_length[a]] = c

            #Transform list data form to Varialble(torch.LongTensor) data form
            chars2_mask = Variable(torch.LongTensor(chars2_mask))
            sentence_in = Variable(torch.LongTensor(sentence_in))
            mors = Variable(torch.LongTensor(mors))
            targets = torch.LongTensor(tags)
            caps = Variable(torch.LongTensor(data['caps']))
            if use_gpu:
                neg_log_likelihood = model.neg_log_likelihood(sentence_in.cuda(), targets.cuda(), mors.cuda(), caps.cuda(),
                    chars2_mask.cuda(), chars2_length, d)
            else:
                neg_log_likelihood = model.neg_log_likelihood(sentence_in, targets, mors, caps,
                    chars2_mask, chars2_length, d)
            loss += neg_log_likelihood.data[0] / len(data['words'])
            neg_log_likelihood.backward()
            torch.nn.utils.clip_grad_norm(model.parameters(), 5.0)
            optimizer.step()

            if i % plot_every == 0:
                loss /= plot_every
                print("%i, cost average: %f, %i/%i epoch" %(i, loss, epoch, n_epoch))
                if losses == []:
                    losses.append(loss)
                losses.append(loss)
                text = '<p>' + '</p><p>'.join([str(l) for l in losses[-9:]]) + '</p>'
                losswin = 'loss_' + name
                textwin = 'loss_text_' + name
                loss = 0.0
            if count % (eval_every) ==0 and count > (eval_every*20) or \
                count % (eval_every*4) == 0 and count < (eval_every * 20):
                model.train(False)
                dev_score, _ = evaluating(model, test_data)
		if dev_score > best_test:
			best_test = dev_score
			with open(models_path+parameters['name'], 'wb') as f:
				torch.save(model,f)
			print("New best score on Test.")
		print(("Test f1 : {}").format(dev_score))
                sys.stdout.flush()
                model.train(True)

            if count % len(train_data) == 0:
                adjust_learning_rate(optimizer, lr=learning_rate/(1+0.05*count/len(train_data)))
        dev_list.append(dev_score)
        end_epoch_time = time.time()
        print(dev_list)
        print("Epoch {} done. Average cost: {}, time: {:.3f} min".format(epoch, np.mean(losses), (end_epoch_time - start_epoch_tim)/60.0))
        print("Best test : {}".format(best_test))

    print(time.time() - t)
else:
    test_use_gpu = opts.use_gpu == 1 and torch.cuda.is_available()
    model1 = torch.load(models_path+'test_model/'+parameters['name'])
    if test_use_gpu:
        model1.cuda()
    model1.eval()
    model1_name = models_path+parameters['name'].split('/')[-1].split('.')[0]
    test_score, _ = evaluating(model1, test_data)
    print("test_score : {}".format(test_score))

