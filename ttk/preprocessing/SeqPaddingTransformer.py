import numpy as np

class SeqPaddingTransformer(object):
    """ Transforms a varying length set of sequences by padding with zeros. """
    def __init__(self):
        self._fit = False
        self.max_length = 0

    def fit_transform(self, X):        
        self.__fit(X)
        return self.__transform(X)
           

    def fit(self, X):
        self.__fit(X)
        return self

    def transform(self, X):
        transformed = self.__transform(X)
        return transformed

    def inverse_transform(self, y):
        transformed = []
        for seq in y:
            i = 0
            token = seq[i]
            transformed_seq = []
            seq_length = len(seq)
            while token != 0.0:
                transformed_seq.append(token)
                i += 1
                if i < seq_length:
                    token = seq[i]
                else:
                    token = 0.0
            
            transformed.append(transformed_seq)

        return transformed
    

    def __fit(self, X):
        # find longest sequence in set and save
        self.max_length = len(max(X, key=len))
        self._fit = True

    def __transform(self, X):
        X_padded = []
        for seq in X:
            x = []
            seq_length = len(seq)

            # grab first token to determine type and dim
            t0 = seq[0]

            using_vect = False
            if type(t0) is type(np.ndarray(1)):
                dim = t0.shape
                using_vect = True

            for i in range(self.max_length):
                if i < seq_length:
                    x.append(seq[i])
                else:
                    if using_vect:
                        x.append(np.zeros_like(t0))
                    else:
                        x.append(0.0)
            X_padded.append(x)
        return np.array(X_padded)


