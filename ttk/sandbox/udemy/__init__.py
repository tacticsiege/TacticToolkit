
"""
    Udemy module. Contains code created while working along with Udemy courses.
    todo: handle citations
"""

import numpy as np

# manage flags for Theano and pygpu
# todo: handle this correctly
import os
os.environ['CPLUS_INCLUDE_PATH']='C:\\Program Files\\NVIDIA GPU Computing Toolkit\\CUDA\\v8.0\\include'
os.environ['DEVICE']='cuda0'

import theano
import theano.tensor as T

"""
    Utility functions for neural nets.
"""
def init_weight(Mi, Mo):
    return np.random.randn(Mi, Mo) / np.sqrt(Mi + Mo)


# elevate modules
from ttk.sandbox.udemy.HiddenLayer import *
from ttk.sandbox.udemy.GRU import *
from ttk.sandbox.udemy.LSTM import *
from ttk.sandbox.udemy.ANN import *
from ttk.sandbox.udemy.SimpleRNNClassifier import *