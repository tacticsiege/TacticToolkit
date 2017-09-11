import pandas as pd
import numpy as np

import nltk
from nltk.tokenize import LineTokenizer
from nltk.corpus import CategorizedPlaintextCorpusReader

from nltk.corpus import CorpusReader
from nltk import PorterStemmer

import re

import glob


class CategorizedDatedCorpusReader(object):
    """
        Categorized corpus with date awareness.
    """
    def __init__(self,
                 corpus_root,
                 *args,
                 file_pattern=r'.*_corpus\.txt',
                 cat_pattern=r'(.*)/',
                 sent_tokenizer=LineTokenizer(),
                 verbose=False,
                 **kwargs):
        self._corpus_map = self._create_corpora(corpus_root,
                                                file_pattern,
                                                cat_pattern,
                                                verbose,
                                                **kwargs)
        

    def dates(self, categories=None, dates=None, verbose=False):
        date_list = []
        for date in self._corpus_map.keys():
            if dates is None or date in dates:           
                if categories is None:
                    # every date in corpus will be valid when considering all categories
                    date_list.append(date)
                else:
                    # only add this date if there are any sentences
                    # for this date from the categories we want
                    dated_corpus = self._corpus_map[date]
                    include_date = False
                    for cat in categories:
                        try:
                            if len(dated_corpus.sents(categories=[cat])) > 0:
                                include_date = True
                                break
                        except ValueError:
                            continue
                        except:
                            continue
                
                    if include_date:
                        date_list.append(date)                
        
        return date_list

    def categories(self, fileids=None, dates=None, categories=None, verbose=False):
        category_list = []
        # only check corpora for dates we care about
        for date, dated_corpus in self.iter_dated_corpora(dates, verbose=verbose):
            try:
                potentially_valid = []
                if categories is None:
                    # all categories are potentially valid
                    potentially_valid = dated_corpus.categories(fileids=fileids)
                else:
                    # only param categories are potentially valid
                    potentially_valid = categories
                
                for cat in potentially_valid:
                    include_cat = False
                    try:
                        # only add category if there are sentences for this date
                        if len(dated_corpus.sents(categories=[cat])) > 0:
                            include_cat = True                                                        
                    except:
                        continue

                    if include_cat:
                        category_list.append(cat)

                if verbose == 'debug':
                    print ('Found %i categories for %s' % (len(cats), date))
            except:
                if verbose:
                    print ('Exception thrown getting categories for', date)
        
        return list(set(category_list))

    def words(self, categories=None, dates=None, verbose=False):        
        word_list = []
        for date, dated_corpus in self.iter_dated_corpora(dates, verbose=verbose):
            try:
                words = dated_corpus.words(categories=categories)
                word_list.extend(words)
                if verbose == 'debug':
                    print ('Added %i words for %s' % (len(words), date))
            except:
                if verbose:
                    print ('Exception thrown getting words for %s and the following categories: %s' %(date, categories))

        return word_list

    def sents(self, categories=None, dates=None, verbose=False):
        sent_list = []
        for date, dated_corpus in self.iter_dated_corpora(dates, verbose=verbose):
            try:
                sents = dated_corpus.sents(categories=categories)
                sent_list.extend(sents)
                if verbose == 'debug':
                    print ('Added %i sents for %s' % (len(sents), date))
            except:
                if verbose:
                    print ('Exception thrown getting sents for % and the following categories: %s' %
                           (date, categories))

        return sent_list

    def raw(self, fileids=None, categories=None, dates=None, verbose=False):
        raw_list = []
        for date, dated_corpus in self.iter_dated_corpora(dates, verbose=verbose):
            try:
                raw = dated_corpus.raw(fileids=fileids, categories=categories)
                raw_list.append(raw)
                if verbose == 'debug':
                    print ('Added raw text for', date)
            except:
                if verbose:
                    print ('Exception thrown getting raw text for %s and the following:' % (date))
                    print ('Fileids:', fileids)
                    print ('Categories:', categories)

        return " ".join(raw_list)

    def fileids(self, categories=None, dates=None, verbose=False):
        id_list = []
        for date, dated_corpus in self.iter_dated_corpora(dates=dates):

            if verbose == 'debug':
                print ('Getting fileids for', date)
        
            try:
                ids = dated_corpus.fileids(categories=categories)
                id_list.extend(ids)
                if verbose =='debug':
                    print ('Added %i fileids for %s' % (len(ids), date))
            except:
                if verbose:
                    print ('Exception thrown getting fileids for %s and the following categories: %s' % 
                           (date, categories))

        return id_list     
       
    ## formatters
    def to_data_frame(self, categories=None, dates=None, content_scope='sents', verbose=False):
        d = []
        for date, cat, content in self.iter_content(
            dates=dates, categories=categories, content_scope=content_scope, verbose=verbose):

            d.append({'date':date, 'category':cat, 'content':content})

        df = pd.DataFrame(d)
        return df


    ## iterators
    def iter_dated_corpora(self, dates=None, categories=None, verbose=False):
        for date in self.dates(dates=dates, categories=categories):
            dated_corpus = self._corpus_map[date]
            if dated_corpus is not None:
                yield date, dated_corpus
            else:
                if verbose:
                    print ('No corpus found in corpus_map for', date) 

    def iter_content(self, dates=None, categories=None, content_scope='sents', verbose=False):
        valid_categories = self._get_valid_categories(categories, dates=dates)

        # iterate over every corpus date
        for date, dated_corpus in self.iter_dated_corpora(dates=dates, categories=categories):
            # iterate over valid categories with content on this date
            if verbose =='debug':
                print ('Iterating content for', date)
            for cat in valid_categories:
                try:
                    if(len(dated_corpus.sents(categories=[cat])) == 0):
                        # there is no content on this day for this category
                        if verbose == 'debug':
                            print ('No content on %s for %s' % (date, cat))
                        continue

                    content = ''
                    if content_scope == 'sents':
                        if verbose == 'debug':
                            print ('Iterating sentences for %s from %s' % (date, cat))
                        # use sents for content
                        for sent in dated_corpus.sents(categories=[cat]):
                            content = ' '.join(sent)
                            yield date, cat, content
                    else:
                        raise ValueError(content_scope)
                except:
                    continue

    def _get_valid_categories(self, categories, dates=None):
        valid_categories = []
        if categories is None:
            valid_categories = self.categories(dates=dates)
        else:
            valid_categories = categories
        return valid_categories

    
    ## === Private Functions === 
    def _create_corpora(self, corpus_root, file_pattern, cat_pattern, date_regex, verbose=False, **kwargs):
        corpus_map = dict()
        for date in self._get_unique_dates(corpus_root, file_pattern, verbose):
            date = str(date.date()) # more string friendly
            corpus_map[date] = self._create_date_corpus(corpus_root, 
                                                        file_pattern, 
                                                        cat_pattern, 
                                                        date, 
                                                        verbose,
                                                        **kwargs)
            
        if verbose:
            print ('Created all corpora.')
        
        return corpus_map
    
    def _create_date_corpus(self, corpus_root, file_pattern, cat_pattern, date, verbose=False, **kwargs):
        date_file_pattern = '.*%s_%s' % (date, file_pattern) # anything <Date>_<OriginalPattern>
        if verbose == 'debug':
            print ('date_file_pattern:', date_file_pattern)

        corpus = CategorizedPlaintextCorpusReader(
            corpus_root,
            date_file_pattern,
            cat_pattern=cat_pattern,
            sent_tokenizer=LineTokenizer(),
            **kwargs)

        if verbose == 'debug':
            print ('Created corpus for', date)
            print ('Categories: %i' % len(corpus.categories()))
            print ('Sentences: %i' % len(corpus.sents()))
            print ('Uniq. Words: %i, Total Words: %i\n' % (len(set(corpus.words())), len(corpus.words())))

        return corpus
    
    def _get_unique_dates(self, corpus_root, file_pattern, verbose=False):
        # get all matching filenames
        filenames = glob.glob(corpus_root + '/**/*_corpus.txt' , recursive=True)
        if verbose == 'debug':
            print ('Found %i files' % (len(filenames)))

        date_regex = re.compile(r'\d{4}-\d{2}-\d{2}')
        all_dates = []
        for filename in filenames:
            all_dates.append(self._get_date_from_fileid(filename, date_regex))

        return np.unique(all_dates)

    def _get_date_from_fileid(self, fileid, date_regex):
        #print ('id:', fileid)
        date_str = date_regex.search(fileid).group(0)
        return pd.to_datetime(date_str)

