




class Seq2IndexVectorizer(object):
    """ Transforms a sequence of words into a sequence of indices. """
    def __init__(self):
        self.start_idx = 0
        self.start_token = 'START'
        self.end_idx = 1
        self.end_token = 'END'

        # todo: make param
        self._process_token_func = self._process_token
        self._filter_token_func = self._filter_token

        

        # word2idx, idx2word and counts
        self.obj2idx = {
            self.start_token:self.start_idx,
            self.end_token:self.end_idx,
        }
        self.idx2obj = [self.start_token, self.end_token]
        self.obj_idx_count = {
            self.start_idx: float('inf'),
            self.end_idx: float('inf')
        }
        
        # track fit status for messages
        self._fit = False


    def fit(self, X):
        """
            Fits the model by creating an index of objects.

            param: X - list of sequences of objects.
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

        # option A (used): always fit when transforming, learns any new language that is encountered
        # option B: label new words as UNKNOWN, will not learn new language when encountered
        model, transformed_objects, obj_idx_counts = self._partial_fit_model(X)
        return transformed_objects
        

    def inverse_transform(self, y):
        """
            Reverses transformation.  
            Does not reconstruct exactly as words/punct is removed...

            params: list of sequences of indicies
            returns: list of sequences of words
        """
        untransformed = []
        for indexed_obj in y:
            u = []
            for idx in indexed_obj:
                t = self.idx2obj[idx]
                # todo: optionally remove START/END tokens
                u.append(t)
            untransformed.append(u)            

        return untransformed


    def _partial_fit_model(self, X):
        """
            returns: fitted model, transformed list of index sequences and counts.
        """
        i = len(self.idx2obj)
        indexed_objects = []

        for obj in self._iter_objects(X):
            indexed_obj = []
            # todo: make start/end optional
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

            # end and add transformed sentence to list
            # todo: make start/end optional
            indexed_obj.append(self.end_idx)
            indexed_objects.append(indexed_obj)

        # todo: optionally sort and limit

        # indicate the model has been fit
        self._fit = True

        # todo: optionally one-hot encode

        # returned fitted transformer, transformed input, counts
        return self, indexed_objects, self.obj_idx_count


    def _iter_objects(self, X):
        # s is a sequence of objects
        for s in X:
            # filter and process tokens for each sequence
            tokens = [self._process_token_func(t, s) 
                      for t in s 
                      if self._filter_token_func(t, s)]
            
            # yield valid processed tokens for each sequence
            yield tokens

    def _process_token(self, t, s):
        return t

    def _filter_token(self, t, s):
        return True

class SeqMappingTransformer(object):
    pass

class SeqPaddingTransformer(object):
    pass