'''
Utilities for network flow
'''

import networkx as nx
import numpy as np
import scipy as sp

from geonet.network import SteinerTree

def find_arc_flow(net, demand):
    '''Determine flow on arcs.

    Values are unique for tree networks.

    net: a (tree) network
    demand: maps node IDs to demand (or supply if negative)
    '''

    assert sum(demand.values()) == 0.0, 'flow not balanced'

    # TODO: is this still necessary?
    nods = sorted(net.dg.nodes())
    edgs = sorted(net.dg.edges())
    
    im = nx.incidence_matrix(net.dg, nodelist=nods, edgelist=edgs, oriented=True)
    im = im[1:, :] # skip any (redundant) row
    
    dem = np.array([demand.get(n, 0.0) for n in nods])
    dem = dem[1:] # skip same (redundant) row

    sol = sp.sparse.linalg.spsolve(im, dem)
    return dict(zip(edgs, sol))

def make_forward_flow(tree, flow):
    '''Create tree with arcs oriented for positive, forward flow.

    args:
    - tree: a SteinerTree
    - flow: a dict from arc to (signed) flow value

    returns:
    - a new SteinerTree
    - a new flow dict with only positive flow values
    '''
    new_nodes = tree.get_nodes()
    new_arcs = []
    new_pos = tree.get_terminal_positions()
    new_flow = {}

    for u, v in tree.get_arcs():
        if flow[u, v] >= 0.0:
            new_arcs.append((u, v))
            new_flow[u, v] = flow[u, v]
        else:
            new_arcs.append((v, u))
            new_flow[v, u] = -1.0 * flow[u, v]

    new_tree = SteinerTree(new_nodes, new_arcs, new_pos)
    return new_tree, new_pos
