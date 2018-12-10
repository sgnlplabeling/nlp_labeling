# -*- coding: utf-8 -*-
from __future__ import print_function
import optparse
import itertools
from collections import OrderedDict
import loader
import torch
import time
from torch.autograd import Variable
import sys
from utils import *
from loader import *
from model import BiLSTM_CRF
import torch
import pickle

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
    "-t", "--test", default="",
    help="Test set location"
)
optparser.add_option(
    '--score', default='evaluation/temp/score.txt',
    help='score file location'
)

optparser.add_option(
    "-l", "--lower", default="1",
    type='int', help="Lowercase words (this will not affect character inputs)"
)
optparser.add_option(
    "-z", "--zeros", default="1",
    type='int', help="Replace digits with 0"
)

optparser.add_option(
    "-w", "--word_dim", default="64",
    type='int', help="Token embedding dimension"
)
optparser.add_option(
    "-W", "--word_lstm_dim", default="126",
    type='int', help="Token LSTM hidden layer size"
)
optparser.add_option(
    "-p", "--pre_emb", default="",
    help="Location of pretrained embeddings"
)

optparser.add_option(
    "--is_pre_emb", default="0",
    type='int', help="Decide to use pretrained word embeddings 0:Random Embedding, 1:pre trained embedding "
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

opts = optparser.parse_args()[0]
parameters = OrderedDict()

parameters['lower'] = opts.lower == 1
parameters['zeros'] = opts.zeros == 0
parameters['word_dim'] = opts.word_dim
parameters['word_lstm_dim'] = opts.word_lstm_dim
parameters['pre_emb'] = opts.pre_emb
parameters['is_pre_emb'] = opts.is_pre_emb
parameters['crf'] = opts.crf == 1
parameters['dropout'] = opts.dropout
parameters['name'] = opts.name
parameters['use_gpu'] = opts.use_gpu == 1 and torch.cuda.is_available()
use_gpu = parameters['use_gpu']

mapping_file = 'models/mapping.pkl'

name = parameters['name']
model_name = models_path + name
tmp_model = model_name + '.tmp'

assert os.path.isfile(opts.train)
assert os.path.isfile(opts.test)

assert parameters['word_dim'] > 0
assert 0. <= parameters['dropout'] < 1.0

assert parameters['word_dim'] > 0
if parameters['is_pre_emb']:
    assert not parameters['pre_emb'] or os.path.isfile(parameters['pre_emb'])


if not os.path.isfile(eval_script):
    raise Exception('CoNLL evaluation script not found at "%s"' % eval_script)
if not os.path.exists(eval_temp):
    os.makedirs(eval_temp)
if not os.path.exists(models_path):
    os.makedirs(models_path)
 
lower = parameters['lower']
zeros = parameters['zeros']

train_sentences = loader.load_sentences(opts.train, lower, zeros)
test_sentences = loader.load_sentences(opts.test, lower, zeros)

if parameters['is_pre_emb']:
    dico_words_train = word_mapping(train_sentences,parameters['lower'])[0]
    dico_words, word_to_id, id_to_word = augment_with_pretrained(
            dico_words_train.copy(),
            parameters['pre_emb'],
            list(itertools.chain.from_iterable(
                    [[x[0] for x in s] for s in test_sentences] + [[x[1] for x in s] for s in test_sentences]
                    )
                )
            )
else:
    dico_words, word_to_id, id_to_word = word_mapping(train_sentences,parameters['lower'])

dico_words_train = dico_words
dico_tags, tag_to_id, id_to_tag = tag_mapping(train_sentences+test_sentences)



train_data = prepare_dataset(
    train_sentences, word_to_id,tag_to_id, lower)
test_data = prepare_dataset(
    test_sentences, word_to_id, tag_to_id, lower)

print("%i  / %i sentences in train /  test." % (
    len(train_data), len(test_data)))




word_embeds = init_word_embeddings(parameters, id_to_word, opts.pre_emb, opts.word_dim)



model = BiLSTM_CRF(word_to_ix=word_to_id, tag_to_ix=tag_to_id,
    embedding_dim=parameters['word_dim'], hidden_dim=parameters['word_lstm_dim'], pre_word_embeds=word_embeds,dropout=parameters['dropout'],use_gpu=parameters['use_gpu'], use_crf=parameters['crf'])



if use_gpu:
    model.cuda()

singletons = set([word_to_id[k] for k, v
                  in dico_words.items() if v == 1])


learning_rate = 0.0005
optimizer = torch.optim.Adam(model.parameters(), lr=learning_rate)

losses = []
loss = 0.0
best_test = -np.inf
best_test_F = -1.0
best_train_F = -1.0
all_F = [[0, 0, 0]]
plot_every = 50
eval_every = 500
count = 0
test_list = []
n_epoch = 50
sys.stdout.flush()


def evaluating(model, datas):
    prediction = []
    new_F = 0.0
    confusion_matrix = torch.zeros((len(tag_to_id)-2, len(tag_to_id)-2))
    for data in datas:
        ground_truth_id = data['tags']
        words = data['str_words']
        words1 = data['str_words1']
        words2 = data['str_words2']
        words3 = data['str_words3']


        dwords = Variable(torch.LongTensor(data['words']))
        dwords1 = Variable(torch.LongTensor(data['words1']))
        dwords2 = Variable(torch.LongTensor(data['words2']))
        dwords3 = Variable(torch.LongTensor(data['words3']))

        if use_gpu:
            val, out = model(dwords.cuda(), dwords1.cuda(), dwords2.cuda(), dwords3.cuda())
        else:

            val, out = model(dwords, dwords1, dwords2, dwords3)
        predicted_id = out
        for (word,word1,word2,word3, true_id, pred_id) in zip (words,words1,words2,words3, ground_truth_id, predicted_id):
            line = ' '.join([word,word1,word2,word3, id_to_tag[true_id], id_to_tag[pred_id]])
            prediction.append(line)
            confusion_matrix[true_id, pred_id] +=1
        prediction.append('')
    predf = eval_temp + '/pred.' + name
    scoref = eval_temp + '/score.' + name

    with open(predf, 'w') as f:

        f.write('\n'.join(prediction))

    os.system('%s -r < %s > %s' %(eval_script, predf, scoref))
    eval_lines = [l.rstrip() for l in codecs.open(scoref, 'r', 'utf8')]

    for i, line in enumerate(eval_lines):
        print(line)
        if i==1:
            new_F = float(line.strip().split()[-1])

    return new_F



model.train(True)
for epoch in range(1, n_epoch+1):

    start_epoch_tim = time.time()
    epoch_costs = []
    for i, index in enumerate(np.random.permutation(len(train_data))):

        tr = time.time()
        count += 1

        input = create_input(train_data[index],singletons)
        data = train_data[index]
        model.zero_grad()
        words = data['words']
        words1 = data['words1']
        words2 = data['words2']
        words3 = data['words3']
        tags = data['tags']

        words = Variable(torch.LongTensor(words))
        words1 = Variable(torch.LongTensor(words1))
        words2 = Variable(torch.LongTensor(words2))
        words3 = Variable(torch.LongTensor(words3))
        targets = torch.LongTensor(tags)

        if use_gpu:
            neg_log_likelihood = model.neg_log_likelihood(words.cuda(),words1.cuda(),words2.cuda(),words3.cuda(),targets.cuda())
        else:
            neg_log_likelihood = model.neg_log_likelihood(words,words1,words2,words3,targets)
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

        if count % len(train_data) == 0:
            adjust_learning_rate(optimizer, lr=learning_rate/(1+0.05*count/len(train_data)))

    model.train(False)

    best_test_F = evaluating(model, test_data)
    if best_test_F > best_test:
        best_test = best_test_F
        with open(models_path+parameters['name'], 'wb') as f:
            torch.save(model, f)
        print("New best score on Test")
    sys.stdout.flush()
    model.train(True)

    print(("test f1 : {}").format(best_test_F))

    test_list.append(best_test_F)
    end_epoch_time = time.time()
    print(test_list)
    print("Epoch {} done. Average cost: {}, time: {:.3f} min".format(epoch, np.mean(losses), (end_epoch_time - start_epoch_tim)/60.0))
    print("Best test : {}".format(best_test))

print("time",time.time() - t)


