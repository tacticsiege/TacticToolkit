
import numpy as np

import theano
import theano.tensor as T

from ttk.sandbox.udemy import init_weight
from ttk.sandbox.udemy import HiddenLayer

from sklearn.utils import shuffle

import matplotlib.pyplot as plt

class ANN(object):
    def __init__(self, hidden_layer_sizes):
        self.hidden_layer_sizes = hidden_layer_sizes
        
    def fit(self, X, Y, 
            learning_rate=10e-3, 
            mu=0.99, reg=10e-12, eps=10e-10, 
            epochs=400, batch_sz=20, 
            print_period=10, show_fig=False):
        Y = Y.astype(np.int32)
        
        N, D = X.shape
        K = len(set(Y))
        self.hidden_layers = []
        M1 = D
        count = 0
        for M2 in self.hidden_layer_sizes:
            h = HiddenLayer(M1, M2, count)
            self.hidden_layers.append(h)
            M1 = M2
            count += 1
        W = init_weight(M1, K)
        b = np.zeros(K)
        self.W = theano.shared(W, 'W_logreg')
        self.b = theano.shared(b, 'b_logreg')
        
        self.params = [self.W, self.b]
        for h in self.hidden_layers:
            self.params += h.params
            
        dparams = [theano.shared(np.zeros(p.get_value().shape)) for p in self.params]
        
        thX = T.matrix('X', dtype='float32')
        thY = T.ivector('Y')
        pY = self.forward(thX)
        
        rcost = reg*T.sum([(p*p).sum() for p in self.params])
        cost = -T.mean(T.log(pY[T.arange(thY.shape[0]), thY])) + rcost
        prediction = self.predict(thX)
        
        grads = T.grad(cost, self.params)
        
        updates = [
            (p, p + mu*dp - learning_rate*g) for p, dp, g in zip(self.params, dparams, grads)
        ] + [
            (dp, mu*dp - learning_rate*g) for dp, g in zip(dparams, grads)
        ]
        
        train_op = theano.function(
            inputs=[thX, thY],
            outputs=[cost, prediction],
            updates=updates,
        )
        
        n_batches = int(N / batch_sz)
        costs = []
        for i in range(epochs):
            X, Y = shuffle(X.astype('float32'), Y)
            for j in range(n_batches):
                Xbatch = X[j*batch_sz:(j*batch_sz + batch_sz)]
                Ybatch = Y[j*batch_sz:(j*batch_sz + batch_sz)]
                
                c, p = train_op(Xbatch, Ybatch)
                
                if j % print_period == 0:
                    costs.append(c)
                    e = np.mean(Ybatch != p)
                    print ('i:', i, 'j:', j, 'cost', c, 'error', e)
        
        if show_fig:
            plt.plot(costs)
            plt.show()
           
        
    def forward(self, X):
        Z = X
        for h in self.hidden_layers:
            Z= h.forward(Z)
        return T.nnet.softmax(Z.dot(self.W) + self.b)
    
    def predict(self, X):
        pY = self.forward(X)
        return T.argmax(pY, axis=1)


