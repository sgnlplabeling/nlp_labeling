#-*- coding: utf-8 -*-
from data_utils import load_vocab, \
    CoNLLDataset, load_word_embeddings

from model import BiAffineModel
from config import Config
import os

os.environ["CUDA_DEVICE_ORDER"]="PCI_BUS_ID"   # see issue #152
os.environ["CUDA_VISIBLE_DEVICES"]="1"

# create instance of config
config = Config()

# load vocabs

word2idx  = load_vocab(config.words_filename)
char2idx  = load_vocab(config.chars_filename)
pumsa2idx = load_vocab(config.pumsas_filename)
rel2idx  = load_vocab(config.rels_filename)

# pos_embedding = load_embeddings(config.pos_embedding_filename, pumsa2idx, "pos")
pos_embedding = None
default_NNLM = load_word_embeddings(word2idx)

# create dataset
dev = CoNLLDataset(filename=config.dev_filename, word2idx=word2idx, pumsa2idx=pumsa2idx, rel2idx=rel2idx, char2idx=char2idx, shuffle=False)
# test = CoNLLDataset(filename=config.test_filename, word2idx=word2idx, pos2idx=pos2idx, rel2idx=rel2idx, char2idx=char2idx, shuffle=False)
train = CoNLLDataset(filename=config.train_filename, word2idx=word2idx, pumsa2idx=pumsa2idx, rel2idx=rel2idx, char2idx=char2idx, shuffle=config.shuffle)
unlabeled = CoNLLDataset(filename=config.unlabeled_filename, word2idx=word2idx, pumsa2idx=pumsa2idx, rel2idx=rel2idx, char2idx=char2idx, shuffle=False)

model = BiAffineModel(default_NNLM = default_NNLM,
                 pos_embedding = pos_embedding,
                 word2idx = word2idx,
                pumsa2idx = pumsa2idx,
                 rel2idx = rel2idx,
                 char2idx = char2idx)


model.build()

# train, evaluate and interact
if config.mode == "train":
    model.train(train, dev)

elif config.mode == "tagging":
    model.tagging(unlabeled)


