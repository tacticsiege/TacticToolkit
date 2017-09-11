
import matplotlib.pyplot as plt
import pandas as pd

from ttk.text import Normalizer

from ttk.plotting import SortOptions
from ttk.plotting import PlotLabels
from ttk.plotting import PlotOptions

from ttk.corpus import CategorizedDatedCorpusReader
from ttk.corpus import CategorizedDatedCorpusReporter

from ttk.plotting import plot_counts


class CategorizedDatedCorpusPlotter(object):
    """
        Corpus plotting utility.
    """
    def __init__(self):
        self.normalizer = Normalizer(stemmer=None)
        self.reporter = CategorizedDatedCorpusReporter()

    """
        Plotting API
    """
    def plot_category_summary(self, 
                         corpus, 
                         ax, 
                         categories=None, 
                         dates=None,
                         plot_column='sentences',
                         normalize=False,
                         plot_labels=None,
                         plot_options=None,
                         sort_options=None,
                         verbose=False,
                         ):
        # todo: support normalization at summary level
        # get data
        summaries = self.reporter.category_summary(corpus,
                                                   categories=categories,
                                                   dates=dates,
                                                   output='dataframe')
        if verbose == 'debug':
            print ('summaries type:', type(summaries))
        summaries = self._sort_summaries(sort_options, summaries, verbose=verbose)
        if verbose == 'debug':
            print ('summaries type:', type(summaries))


        plot_labels = self._create_plot_labels(plot_labels, summaries, verbose=verbose)
        plot_options = self._create_plot_options(plot_options, summaries, verbose=verbose)

        counts = summaries[plot_column].values.astype(int)
        
        ax =  plot_counts(ax, counts, plot_labels=plot_labels, plot_options=plot_options)
        return ax


    """
        Helpers
    """
    def _sort_summaries(self, sort_options, summaries, verbose=False):
        if sort_options is None:
            if verbose == 'debug':
                print ('Creating default sort options.')
            sort_options = SortOptions()        

        if sort_options.should_sort:
            if verbose == 'debug':
                print ('Sorting by \"%s\". Before:' % sort_options.sort_by)
                print (summaries.head())

            summaries = summaries.sort_values(
                str(sort_options.sort_by))

            if verbose == 'debug':
                print ('Done sorting. After:')
                print (summaries.head())
        
        if sort_options.cumulative:
            # todo: how to handle cumulative? just the plot col?
            pass

        return summaries

    def _create_plot_labels(self, plot_labels, summaries, verbose=False):
        if verbose == 'debug':
            print ('Creating plot labels...')
        # create default labels if None were provided
        if plot_labels is None:
            if verbose == 'debug':
                print ('Creating default PlotLabels...')
            plot_labels = PlotLabels(xlabel='category', xticklabel_by='category')
        
        # set xtick labels if None were set and a label_by was provided    
        if plot_labels.xticklabels is None and plot_labels.xticklabel_by is not None:
            if verbose == 'debug':
                print ('No xticklabels were set, but xticklabel_by is set to %s.  Setting labels...' % (plot_labels.xticklabel_by))
                print ('type of xticklabel_by: %s, len: %i, type of elem[0]: %s' %
                      (type(plot_labels.xticklabel_by), len(plot_labels.xticklabel_by), type(plot_labels.xticklabel_by[0])))
            plot_labels.xticklabels = summaries[str(plot_labels.xticklabel_by[0])].values.astype(str)

        return plot_labels

    def _create_plot_options(self, plot_options, summaries, verbose=False):
        if verbose == 'debug':
            print ('Creating plot options...')
        if plot_options is None:
            plot_options = PlotOptions()

        return plot_options
