
from ttk.sandbox.udemy import init_weight

import numpy as np

import theano
import theano.tensor as T

"""
def init_weights(Mi, Mo):
    return np.random.randn(Mi, Mo) / np.sqrt(Mi + Mo)
    """

class HiddenLayer(object):
    def __init__(self, M1, M2, an_id):
        self.id = an_id
        self.M1 = M1
        self.M2 = M2
        W = init_weight(M1, M2)
        b = np.zeros(M2)
        self.W = theano.shared(W, 'W_%s' % self.id)
        self.b = theano.shared(b, 'b_%s' % self.id)
        self.params = [self.W, self.b]
        
    def forward(self, X):
        return T.nnet.relu(X.dot(self.W) + self.b)


