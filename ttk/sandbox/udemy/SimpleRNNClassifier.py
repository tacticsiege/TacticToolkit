import theano
import theano.tensor as T

import numpy as np

from ttk.sandbox.udemy import init_weight

import matplotlib.pyplot as plt

from sklearn.utils import shuffle

import time

class SimpleRNNClassifier(object):
    def __init__(self, M):
        self.M = M
        
    def fit(self, X, Y, learning_rate=10e-1, mu=0.99, reg=1.0, activation=T.tanh, epochs=100, show_fig=False):
        D = X[0].shape[1] # X is of size N x T(n) x D
        K = len(set(Y.flatten()))
        N = len(Y)
        M = self.M
        self.f = activation

        print ('D, K, N, M:', D, K, N, M)

        # initial weights
        Wx = init_weight(D, M)
        Wh = init_weight(M, M)
        bh = np.zeros(M)
        h0 = np.zeros(M)
        Wo = init_weight(M, K)
        bo = np.zeros(K)

        # make them theano shared
        self.Wx = theano.shared(Wx)
        self.Wh = theano.shared(Wh)
        self.bh = theano.shared(bh)
        self.h0 = theano.shared(h0)
        self.Wo = theano.shared(Wo)
        self.bo = theano.shared(bo)
        self.params = [self.Wx, self.Wh, self.bh, self.h0, self.Wo, self.bo]
        
        # theano inputs/outputs
        thX = T.fmatrix('X')
        thY = T.ivector('Y')
        #thY = T.fmatrix('Y')
        
        def recurrence(x_t, h_t1):
            # returns h(t), y(t)
            h_t = self.f(x_t.dot(self.Wx) + h_t1.dot(self.Wh) + self.bh)
            y_t = T.nnet.softmax(h_t.dot(self.Wo) + self.bo)
            return h_t, y_t
        
        [h, y], _ = theano.scan(
            fn=recurrence,
            outputs_info=[self.h0, None],
            sequences=thX,
            n_steps=thX.shape[0]
        )
        
        #print ('Shape y:', y.shape)
        #print ('y[0, 0, 0]:', y[0,0,0])

        py_x = y[:, 0, :]
        prediction = T.argmax(py_x, axis=1)
        
        cost = -T.mean(T.log(py_x[T.arange(thY.shape[0]), thY]))
        grads = T.grad(cost, self.params)
        # easy way to get shared var in shape of p...
        dparams = [theano.shared(p.get_value()*0) for p in self.params]
        
        updates = [
            (p, p + mu*dp - learning_rate*g) for p, dp, g in zip(self.params, dparams, grads)
        ] + [
            (dp, mu*dp - learning_rate*g) for dp, g in zip(dparams, grads)
        ]
        
        self.predict_op = theano.function(
            inputs=[thX],
            outputs=prediction
        )
        self.train_op = theano.function(
            inputs=[thX, thY],
            outputs=[cost, prediction, y],
            updates=updates,
        )
        
        # training loop
        costs = []
        for i in range(epochs):
            start_time = time.time()
            print ('iteration:', i)
            X, Y = shuffle(X, Y)
            n_correct = 0
            cost = 0
            for j in range(N):
                #print ('X[j]:', X[j], 'Y[j]:', Y[j])
                
                c, p, rout = self.train_op(X[j], Y[j])
                #print ('c:', c)
                cost += c
                #print ('p[-1]:', p[-1], 'Y[j,-1]:', Y[j,-1])
                if p[-1] == Y[j, -1]:
                    n_correct += 1
            print ('shape y:', rout.shape)
            print ('i:', i, 'cost:', cost, 'classification rate:', (float(n_correct) / N))
            costs.append(cost)
            end_time = time.time()
            duration = end_time - start_time
            print ('duration:', duration)
            
        if show_fig:
            plt.plot(costs)
            plt.show()
        


