from sklearn.base import BaseEstimator
from sklearn.base import TransformerMixin

from gensim.models import Word2Vec
import logging

class Seq2WordVecTransformer(object):
    """ Transforms a sequence of words into a sequence of word vectors. """
    def __init__(self):
        self._fit = False
        self._model = None
        logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
        pass

    def fit(self, X):
        self.__fit(X)
        return self

    def partial_fit(self, X):
        self.__fit(X)
        return self

    def fit_transform(self, X):
        self.__fit(X)
        return self.__transform(X)

    def transform(self, X):
        return self.__transform(X)

    def inverse_transform(self, y):
        transformed = [[
            self._model.most_similar(positive=[wv], topn=1)[0][0] for wv in seq] for seq in y]
        return transformed


    def __fit(self, X):
        # create and fit the model based on params
        self._model = Word2Vec(X, min_count=0, workers=4)
        self._fit = True

    def __transform(self, X):
        if not self._fit:
            raise RuntimeError('Must call fit before calling transform.')
        # replace each word with it's word vector
        transformed = [[self._model[w] for w in x] for x in X]
        
        return transformed
    


