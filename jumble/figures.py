"""
Created on Sat Nov 15 16:57:25 2014

@author: vsanni
"""

import os
from jumble.vprint     import vprint
from jumble.type_extra import length
from math              import sqrt

import jumble.file_location as floc
import matplotlib.pyplot    as pl
from matplotlib        import _pylab_helpers as plh

import seaborn as sns
sns.set(style="darkgrid")


def current():
    """
    Gets figure reference to the current figure if exist.
    """

    figures_manager = plh.Gcf.get_active()
    if figures_manager is not None: return figures_manager.canvas.figure
    else                          : return None



def axes(N=1, sharex=False, sharey=False, squeeze=True, subplot_kw=None, gridspec_kw=None, title= None, **fig_kw):

    if length(N) ==1:
        rows = int(sqrt(N))
        cols = rows

        if N == 3:
            rows, cols = 3, 1
        else:
            while N > rows*cols:
                if cols < rows: cols += 1
                else          : rows += 1
    else:
        rows, cols = N

    figure = pl.figure(**fig_kw)
    axis   = figure.subplots(nrows=rows, ncols=cols, sharex=sharex, sharey=sharey, squeeze=squeeze, subplot_kw=subplot_kw, gridspec_kw=gridspec_kw)

    if rows > 1  or cols > 1:
        if   length(N) == 2: axis = axis.reshape(rows, cols)
        elif length(N) == 1: axis = axis.reshape(rows*cols )

    if title: set_title(figure=figure, title=title)

    return figure, axis



def close(figure=None):
    if figure is None: figure = current()
    plh.Gcf.destroy_fig(figure)



def close_all():
    plh.Gcf.destroy_all()



def export(figure=None, file_location="", formats=[ "png"], dpi=200, verbose=1, image_only=False):

    if figure is None: figure= current()

    if figure is None:  raise ValueError("figures.export: error, couldn't find any current figure to export")

    if image_only:
        axis         = current_axis(figure)
        bounding_box = axis.get_window_extent().transformed(figure.dpi_scale_trans.inverted())
        axis.set_axis_off()

    else:
        bounding_box = None

    figure.tight_layout()

    file_location = floc.good( file_location, replacement=".")

    path = floc.path(file_location)
    if not os.path.exists(path) and path != "" : os.makedirs(path)

    for e in formats:
        fl = floc.good("%s.%s" % (file_location, e.lower()))
        vprint(verbose,1,"export: printing figure into \"%s\"..." % fl)
        figure.savefig(fl, dpi=dpi, bbox_inches=bounding_box)
        vprint(verbose,1," done\n")



def set_title(figure=None, title=""):

    if figure is None: figure = current()

    if figure is not None:
        figure.canvas.set_window_title(title)

    else:
        raise ValueError("figures.set_title: couldn't find any current figure to set its title")



def current_axis(figure=None):

    if figure is None: figure = current()

    if figure is not None: return figure._axstack.current_key_axes()[1]
    else                 : return None



def draw(figure=None):

    if figure is None: figure = current()

    figure.canvas.draw()



def figure_axis_resolve(axis=None,*v, **kv):

    if "figsize" not in kv.keys(): kv["figsize"] = (9.5,5)

    if axis is None: return axes(*v,**kv)
    else           : return current(), axis



def plot(x=None, y=None, axis= None, xlabel = None, ylabel= None, title= None, **kv):

    fig, ax = figure_axis_resolve(axis,figsize=(9.5,5))

    if x is None: ax.plot(y, **kv)
    else        : ax.plot(x, y, **kv)
    ax.grid(True)

    if "label" in kv.keys(): ax.legend()
    if xlabel is not None  : ax.set_xlabel(xlabel)
    if ylabel is not None  : ax.set_ylabel(ylabel)
    if title  is not None  : ax.set_title(title)

    return fig, ax
