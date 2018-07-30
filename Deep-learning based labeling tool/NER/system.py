# -*- codng: UTF-8 -*-
from __future __ import print_function
import torch
import time
import cPickle
from torch.autograd import Variable

from loader import *
from utils import *

t = time.time()

def eval(model, datas, maxl=1):
