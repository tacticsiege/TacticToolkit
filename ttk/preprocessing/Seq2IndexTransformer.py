from sklearn.preprocessing import OneHotEncoder
import numpy as np

from sklearn.base import BaseEstimator
from sklearn.base import TransformerMixin

class Seq2IndexTransformer(BaseEstimator, TransformerMixin):
    """ Transforms a sequence of words into a sequence of indices. """
    def __init__(self, 
                 token_mapping_func=None, 
                 token_filter_func=None, 
                 limit_size=None, 
                 add_delimiters=True,
                 one_hot=False):

        # token mapping is executed on each element in sequence
        #   and takes the entire sequence as a param.
        if token_mapping_func is None:
            token_mapping_func = self._process_token    
        self._token_mapping_func = token_mapping_func

        # token filtering is executed on each element and returns
        #   True is the token should be kept.  Also takes the entire
        #   sequence as a param.
        if token_filter_func is None:
            token_filter_func = self._filter_token        
        self._filter_token_func = token_filter_func

        # limit size of index?
        self._limit = limit_size

        # setup delimiters
        self._delimiters = add_delimiters
        self.start_idx = 0
        self.start_token = 'START'
        self.end_idx = 1
        self.end_token = 'END'

        # represent index as one-hot vectors?
        self._one_hot = one_hot
        self._one_hot_enc = OneHotEncoder(dtype=int)

        # track fit state for messages
        self._fit = False
        
        # dict(obj2idx), list(idx2obj) and dict(counts)
        self.obj2idx = {
            self.start_token:self.start_idx,
            self.end_token:self.end_idx,
        }
        self.idx2obj = [self.start_token, self.end_token]

        start_end_counts = float(0)
        if self._delimiters:
            start_end_counts = float('inf')

        self.obj_idx_count = {
            self.start_idx: start_end_counts,
            self.end_idx: start_end_counts,
        }


    def fit(self, X):
        """
            Fits the model by creating an index of objects.

            params: X - list of sequences of objects.
            returns: fitted vectorizer.
        """
        model, transformed_objects, obj_idx_counts = self._partial_fit_model(X)
        return model

    def partial_fit(self, X):
        model, transformed_objects, obj_idx_counts = self._partial_fit_model(X)
        return model

    def fit_transform(self, X):
        """
            Fits a model and transforms input.

            returns: fitted transformer, transformed list of index sequences.

        """
        model, transformed_objects, obj_idx_counts = self._partial_fit_model(X)
        return model, transformed_objects


    def transform(self, X):
        """
            Transforms the input using the fitted model. 
        
            returns: list (N) of sequences (T) of indicies (1).        
        
        """
        if not self._fit:
            print ('Must call fit or fit_transform before calling transform.')
            return None

        # option A (used): always fit when transforming, learns any new object that is encountered
        # option B: label new words as UNKNOWN, will not learn new object when encountered
        model, transformed_objects, obj_idx_counts = self._partial_fit_model(X)
        return transformed_objects
        

    def inverse_transform(self, y):
        """
            Reverses transformation.              

            params:  y - list of sequences of indicies
            returns: list of sequences of objects
        """
        untransformed = []
        for indexed_obj in y:
            u = []
            print ('len of idx2obj:', len(self.idx2obj))
            for idx in indexed_obj:
                print ('looking up idx:', idx)
                t = self.idx2obj[idx]
                # todo: optionally remove START/END tokens
                u.append(t)
            untransformed.append(u)            

        return untransformed


    def one_hot_sequences(self, i, indexed_objects):
        one_hots = [] # list of sequences of one-hot encoded index vectors
        # fit the encoder on all sequences
        oh_training_data = [[i] for i in range(len(self.idx2obj))]
        self._one_hot_enc = self._one_hot_enc.fit(oh_training_data)
        # iterate over all sequences and encode each token
        for seq in indexed_objects:
            one_hot_seq = []
            for token in seq:
                oh = self._one_hot_enc.transform([[token]])[0].toarray()[0] # immedately take the first (only) element
                one_hot_seq.append(list(oh))
            one_hots.append(one_hot_seq)
        
        # constructed one_hot vectors, assign them back to indexed_objects
        indexed_objects = one_hots
        return indexed_objects

    def _partial_fit_model(self, X):
        """
            params: X - list of sequences of objects.
            returns: fitted model, transformed list of index sequences and counts.
        """
        i = len(self.idx2obj)
        indexed_objects = []

        for obj in self._iter_objects(X):
            indexed_obj = []
            if self._delimiters:
                indexed_obj.append(self.start_idx)

            for token in obj:
                if token not in self.obj2idx:
                    self.idx2obj.append(token)
                    self.obj2idx[token] = i
                    i += 1

                # keep track of counts
                idx = self.obj2idx[token]
                self.obj_idx_count[idx] = self.obj_idx_count.get(idx, 0) + 1
                
                # add to output (transformed X)
                indexed_obj.append(idx)
                            
            if self._delimiters:
                indexed_obj.append(self.end_idx)

            # add it to list of indexed objects
            indexed_objects.append(indexed_obj)

        # todo: sort and limit
        if self._limit is not None:
            pass
        
        # indicate the model has been fit
        self._fit = True

        # todo: optionally one-hot encode
        if self._one_hot:
            indexed_objects = self.one_hot_sequences(i, indexed_objects)

        # returned fitted transformer, transformed input, counts
        return self, indexed_objects, self.obj_idx_count


    def _iter_objects(self, X):
        # s is a sequence of objects
        for s in X:
            # filter and process tokens for each sequence
            tokens = [self._token_mapping_func(t, s) 
                      for t in s 
                      if self._filter_token_func(t, s)]
            
            # yield valid processed tokens for each sequence
            yield tokens

    def _process_token(self, t, s):
        print ('processing:', t, 'from:', s)
        return t

    def _filter_token(self, t, s):
        return True