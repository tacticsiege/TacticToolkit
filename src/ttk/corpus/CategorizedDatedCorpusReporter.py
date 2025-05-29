import pandas as pd
import numpy as np

from ttk.corpus.CategorizedDatedCorpusReader import CategorizedDatedCorpusReader

class CategorizedDatedCorpusReporter(object):
    """ Reporting utility for CategorizedDatedCorpusReporter corpora. """
    def __init__(self):
        self._output_formats = ['list', 'str', 'dataframe']
            
    def summary(self, corpus, categories=None, dates=None, output='str', verbose=False):
        
        if not self._is_valid_output(output, verbose=verbose):
            return None
        
        # get summary data
        num_categories = len(corpus.categories(categories=categories, dates=dates))
        num_dates = len(corpus.dates(categories=categories, dates=dates))
        num_uniq_words = len(set(corpus.words(categories=categories, dates=dates)))
        num_sents = len(corpus.sents(categories=categories, dates=dates))
        num_words = len(corpus.words(categories=categories, dates=dates))
        num_files = len(corpus.fileids(categories=categories, dates=dates))

        # store in dict for consistency
        summary = {
                'categories':num_categories,
                'dates':num_dates,
                'sentences':num_sents,
                'words':num_words,
                'uniq_words':num_uniq_words,
                'files':num_files,
            }

        # convert to output
        if output == 'str' or output == 'list':
            summary = self._get_summary_formatted_list(summary)
            if output == 'str':
                summary = '\n'.join(summary)
        elif output == 'dataframe':
            summary = pd.DataFrame([summary])
        else:
            print ('Output mode %s is not supported by %s, use one of the following:\n%s'
                   % (output, 'summary', self._output_formats))
            return None

        return summary
    
    def date_summary(self, corpus, categories=None, dates=None, output='str', display_zeros=True, verbose=False):
        
        if not self._is_valid_output(output, verbose=verbose):
            return None

        # generate a list of summary dictionaries
        summaries = (s for s in self._iter_date_summaries(
            corpus, dates=dates, categories=categories, display_zeros=display_zeros, verbose=verbose))

        # convert to output type
        if output == 'str':
            summaries = self._get_formatted_date_summary_string(summaries)
        elif output == 'dataframe':
            summaries = pd.DataFrame(summaries)
        elif output == 'list':
            summaries = list(summaries)
        else:
            print ('Output mode %s is not supported by %s, use one of the following:\n%s'
                   % (output, 'date_summary', self._output_formats))
            return None

        return summaries        
    
    def category_summary(self, corpus, categories=None, dates=None, output='str', display_zeros=True, verbose=False):
        
        if not self._is_valid_output(output, verbose=verbose):
            return None

        # generate category summaries
        summaries = (s for s in self._iter_category_summaries(corpus,
                                                             categories=categories,
                                                             dates=dates,
                                                             display_zeros=display_zeros,
                                                             verbose=verbose))

        # convert to output type
        if output == 'str':
            summaries = self._get_formatted_category_summary_string(summaries)
        elif output == 'dataframe':
            summaries = pd.DataFrame(summaries)
        elif output == 'list':
            summaries = list(summaries)
        else:
            print ('Output mode %s is not supported by %s, use one of the following:\n%s'
                   % (output, 'category_summary', self._output_formats))
            return None

        return summaries

    def sample(self, corpus, categories=None, dates=None):
        pass

    def to_data_frame(self, corpus, categories=None, dates=None, content_scope='sents', verbose=False):
        return corpus.to_data_frame(categories=categories, dates=dates, content_scope=content_scope, verbose=verbose)
        
    """
        Iterators
    """
    def _iter_date_summaries(self, corpus, dates=None, categories=None, display_zeros=True, verbose=False):
        # don't filter categories to display dates with 0 records
        if display_zeros:
            cat_filter = None
        else:
            cat_filter = categories

        for date in corpus.dates(dates=dates, categories=cat_filter):
            # get date summary data 
            words = corpus.words(categories=categories, dates=[date])
            num_words = len(words)
            num_uniq_words = len(set(words))
            num_categories = len(corpus.categories(categories=categories, dates=[date]))
            num_sents = len(corpus.sents(categories=categories, dates=[date]))
            num_files = len(corpus.fileids(categories=categories, dates=[date]))

            # yield dictionary of summary data
            summary = {'date':date,
                       'categories':num_categories,
                       'sentences':num_sents,
                       'words':num_words,
                       'uniq_words':num_uniq_words,
                       'files':num_files,
                       }
            yield summary

    def _iter_category_summaries(self, corpus, categories=None, dates=None, display_zeros=True, verbose=False):
        # don't filter dates to display categories with 0 records
        if display_zeros:
            date_filter = None
        else:
            date_filter = dates

        for cat in corpus.categories(categories=categories, dates=date_filter):
            # get category summary data
            words = corpus.words(categories=[cat], dates=dates)
            num_words = len(words)
            num_uniq_words = len(set(words))
            num_date = len(corpus.dates(categories=[cat], dates=dates))
            num_sents = len(corpus.sents(categories=[cat], dates=dates))
            num_files = len(corpus.fileids(categories=[cat], dates=dates))

            # yield dictionary of summary data
            summary = {'category':cat,
                       'dates':num_date,
                       'sentences':num_sents,
                       'words':num_words,
                       'uniq_words':num_uniq_words,
                       'files':num_files,
                       }
            yield summary

    """
        Formatting
    """
    def _get_summary_formatted_list(self, summary):
        formatted = []
        formatted.append('Summary for %i categories and %i dates' 
                         % (summary['categories'], summary['dates']))
        formatted.append('{:8} sentences'.format(summary['sentences']))
        formatted.append('{:8} total words'.format(summary['words']))
        formatted.append('{:8} unique words'.format(summary['uniq_words']))
        formatted.append('{:8} files'.format(summary['files']))
        return formatted

    def _get_formatted_date_summary_string(self, summaries):
        formatted = []
        for s in summaries:
            date_summary = str(
                '{}: {:2} categories {:4} sentences {:5} words {:5} unique words {:3} files'
                .format(s['date'], s['categories'], s['sentences'], s['words'], s['uniq_words'], s['files']))
            formatted.append(date_summary)
        summaries = '\n'.join(formatted)
        return summaries

    def _get_formatted_category_summary_string(self, summaries):
        formatted = []
        for s in summaries:
            category_summary = str(
                "{:20} {:3} dates {:6} sentences {:7} words {:6} unique words {:3} files"
                .format(s['category'], s['dates'], s['sentences'], s['words'], s['uniq_words'], s['files']))
            formatted.append(category_summary)
        return '\n'.join(formatted)

    """
        Private helpers
    """
    def _is_valid_output(self, output, verbose=False):
        if output in self._output_formats:
            return True
        else:
            print ('Output mode %s is not supported, use one of the following:\n%s'
                   % (output, self._output_formats))
            return False