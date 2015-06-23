'''
Visualization of problem instances and solutions.

For detailed control, matplotlib is used directly, instead of
networkx' wrapper functions.
'''

import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection
from matplotlib.colorbar import ColorbarBase
from matplotlib.colors import Normalize
import numpy as np

from geonet.network import SteinerTree, merge_pos
from geonet.constants import diam_min, diam_max

_diam_cmap = plt.cm.YlGnBu
_fig_size = 10

def new_fig():
    fig = plt.figure(figsize=(_fig_size, _fig_size))
    ax = plt.gca()
    ax.set_aspect('equal')
    return fig, ax


def draw_nodes(nodes, pos, demand=None, fig=None, ax=None):
    '''Draw nodes with given positions.

    Optionally visualize demand vector with size and color.
    '''
    if fig is None:
        fig, ax = new_fig()
    if demand is None:
        demand = dict((n,0) for n in nodes)

    x = np.array([pos[n][0] for n in nodes])
    y = np.array([pos[n][1] for n in nodes])
    d = np.array([demand.get(n, 0) for n in nodes])

    # color should be red for entries, blue for exits, white for Steiner
    cmap = {-1.0: (1,0,.5), 1.0: (.5,0,1), 0.0: (.8, .8, .8)}
    c = np.array([cmap[v] for v in np.sign(d)])

    # size depends on amount of in-/outflow
    s = 100 * np.sqrt(np.abs(d)) + 80.0

    im = ax.scatter(x, y, c=c, s=s, zorder=2)


def draw_edges(tree, steiner_pos, diams=None, fig=None, ax=None, lim=None,
               colorbar=True):
    '''Draw edges with given positions.'''
    if fig is None:
        fig, ax = new_fig()
    if lim is None:
        lim = diam_min, diam_max

    pos = merge_pos(tree, steiner_pos)
    nodes = tree.get_nodes()
    arcs = tree.get_arcs()
    x = np.array([pos[n][0] for n in nodes])
    y = np.array([pos[n][1] for n in nodes])

    segments = [(pos[u], pos[v]) for (u,v) in arcs]

    if diams is None:
        lines = LineCollection(segments, colors='k', zorder=1)
    else:
        diams = np.array([diams[a] for a in arcs])
        lw = 7*diams + 1
        lines = LineCollection(segments, linewidths=lw, zorder=1)
        # set colors
        lines.set_array(diams)
        lines.set_cmap(_diam_cmap)
        lines.set_clim(*lim)
        if colorbar:
            plt.colorbar(lines, orientation='horizontal')
    ax.add_collection(lines)


def draw_network(tree, steiner_pos, demand=None, diams=None, fig=None, ax=None,
                 lim=None, colorbar=True):
    '''Draw network with nodes and edges.'''
    if fig is None:
        fig, ax = new_fig()

    pos = merge_pos(tree, steiner_pos)
    nodes = tree.get_nodes()

    draw_nodes(nodes, pos, demand, fig, ax)
    draw_edges(tree, steiner_pos, diams, fig, ax, lim, colorbar)
