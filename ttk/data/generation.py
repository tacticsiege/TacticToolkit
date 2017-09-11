import numpy as np

def all_parity_pairs(nbit):
    N = 2**nbit
    remainder = 100 - (N % 100)
    Ntotal = N + remainder
    X = np.zeros((Ntotal, nbit))
    Y = np.zeros(Ntotal)
    for ii in range(Ntotal):
        i = ii % N
        # generate the ith sample
        for j in range(nbit):
            if i % (2**(j+1)) != 0:
                i -= 2**j
                X[ii, j] = 1
        Y[ii] = X[ii].sum() % 2
    return X, Y

def parity_sequence_bits(X, y):
    # figure out each y(t) in a sequence of bits
    # y(t) is a series of bits in this example, would be a series of words in a sentence
    
    N, t = X.shape
    Y_t = np.zeros(X.shape, dtype=np.int32)
    for n in range(N):
        ones_count = 0
        for i in range(t):
            if X[n,i] == 1:
                ones_count += 1
            if ones_count % 2 == 1:
                Y_t[n,i] = 1
    return Y_t