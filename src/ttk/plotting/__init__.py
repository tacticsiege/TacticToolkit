
"""
   Plotting module.  
   
   Common and helpful utilty functions.

   Many operations take a figure, do their work then return the figure for
   further formatting.

"""

import numpy as np
import matplotlib.pyplot as plt

###############################################################################
def set_dynamic_xticklabels(ax, classes, verbose=False):
    num_classes = len(classes)
    label_rotation_threshold = 5
    label_vertical_threshold = 16
    if num_classes <= label_rotation_threshold:
        ax.set_xticklabels(list(classes))
    else:
        if num_classes <= label_vertical_threshold:
            rotation = 45
        else:
            rotation = 'vertical'
    
        if verbose:
            print ('Rotating xlabels %s' % str(rotation))
        ax.set_xticklabels(list(classes), rotation=rotation)
    
    return ax

###############################################################################
def telescope_plot_limit(ax, counts, axis='y', padding_factor=4):
        _min = np.min(counts)
        _max = np.max(counts)
        padding = (_max - _min) / padding_factor
        if axis == 'y':
            ax.set_ylim(_min - padding, _max + padding)
        else:
            ax.set_xlim(_min - padding, _max + padding)

        return ax

###############################################################################
def colorize(cmap_name='tab20c', count=20):
        cmap = plt.get_cmap(cmap_name)
        num_c = min(20, count)
        colors = cmap(np.linspace(0, 1.0, num_c))
        return colors

###############################################################################
class SortOptions(object):
    def __init__(self, should_sort=False, sort_by='category', ascending=False, cumulative=False):
        self.should_sort = should_sort
        self.sort_by=sort_by
        self.ascending=ascending
        self.cumulative=cumulative

###############################################################################
class PlotOptions(object):
    def __init__(self, set_labels=True, plot_type='bar', colors=None, colorize=False, show_yerr=False):
        self.set_labels = set_labels
        self.plot_type = plot_type
        self.colors = colors
        self.colorize = colorize
        self.show_yerr = show_yerr

###############################################################################
class PlotLabels(object):
    def __init__(self, 
                title='Title',
                xlabel='x-label',
                ylabel='y-label',
                xticklabels=None,
                xticklabel_by=None,
                yticklabels=None,
                yticklabel_by=None):
        self.title = title
        self.xlabel = xlabel
        self.ylabel = ylabel
        self.xticklabels=xticklabels
        self.xticklabel_by=xticklabel_by,
        self.yticklabels=yticklabels
        self.yticklabel_by=yticklabel_by

        
"""
    Plotting functions
"""
###############################################################################
def plot_counts(ax, counts, plot_labels=PlotLabels(), plot_options=PlotOptions()):
    # get index for classes
    index = range(len(plot_labels.xticklabels))
    
    if plot_options.set_labels:
        # set title and labels
        ax = _set_plot_labels(ax, plot_labels.title, plot_labels.ylabel, plot_labels.xlabel, index, plot_labels.xticklabels)
    
    if plot_options.colorize and not plot_options.colors:
        plot_options.colors = colorize('tab20', len(plot_labels.xticklabels))

    # plot
    if plot_options.plot_type == 'pie':
        pass
    else:
        ax = _additive_plot(ax, index, counts, plot_type=plot_options.plot_type, colors=plot_options.colors)            
    
    return ax

###############################################################################
def plot_avgs(ax, labels, avgs, stds, title, plot_options=PlotOptions()):        
    # get index for classes
    index = range(len(plot_labels.xticklabels))
        
    if plot_options.set_labels:
        # set title and labels            
        ax = _set_plot_labels(ax, plot_labels.title, plot_labels.ylabel, plot_labels.xlabel, index, plot_labels.xticklabels)

    if plot_options.colorize and not plot_options.colors:
        plot_options.colors = colorize('tab20c', len(plot_labels.xticklabels))
        
    # plot
    if show_yerr:
        ax = _additive_plot(ax, index, avgs, plot_type=plot_options.plot_type, yerr=stds, colors=plot_options.colors)
    else:
        ax = _additive_plot(ax, index, avgs, plot_type=plot_options.plot_type, colors=plot_options.colors)
        
    return ax

###############################################################################
def _additive_plot(ax, index, counts, plot_type='bar', yerr=None, colors=None):
    if colors is None:
        color = None
    else:
        color = colors[0]

    if plot_type == 'bar':
        ax.bar(index, counts, yerr=yerr, color=colors)
    elif plot_type == 'step':
        ax.step(index, counts, color=color)
    else:
        ax.plot(index, counts, color=color)

    return ax

###############################################################################
def _set_plot_labels(ax, title, ylabel, xlabel, xticks, xtick_labels):
    ax.set_title(title)
    ax.set_ylabel(ylabel)
    ax.set_xlabel(xlabel)
    # create ticks per class and label
    ax.set_xticks(xticks)    
    ax = set_dynamic_xticklabels(ax, xtick_labels)
    return ax


# elevate classes
from ttk.plotting.CategorizedDatedCorpusPlotter import *