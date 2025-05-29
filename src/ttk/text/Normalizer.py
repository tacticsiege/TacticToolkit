from nltk.stem.porter import PorterStemmer

class Normalizer(object):
    """ 
        Normalizer to standardize text.
    """
    def __init__(self, stemmer=PorterStemmer()):
        self._stemmer = stemmer

    def apply_to_sent(self, sent):
        s = [self.apply(w) for w in sent]
        return s
        
    def apply(self, word):
        w = self.apply_format(word)
        w = self.apply_stemming(w)
        w = self.apply_substitutions(w)
        return w
        
    def apply_format(self, word):
        return word.lower()
    
    def apply_stemming(self, word):
        if self._stemmer:
            return self._stemmer.stem(word)
        return word
    
    def apply_substitutions(self, word):
        return word;