'''
Detecting degeneracy and merging zero-length edges.
'''

from geonet.network import SteinerTree, merge_pos
from geonet.geometry import distance
from geonet.constants import abstol

def degenerate_edges(tree, steiner_pos, abstol=abstol):
    '''list of edges with (numerically) zero length'''
    assert isinstance(tree, SteinerTree)
    pos = merge_pos(tree, steiner_pos)

    return [(u,v) for (u,v) in tree.get_arcs()
            if (tree.is_steiner(u) or tree.is_steiner(v))
            and distance(pos[u], pos[v]) <= abstol]


def is_degenerate(tree, steiner_pos, abstol=abstol):
    return degenerate_edges(tree, steiner_pos, abstol) != []


def merged(tree, steiner_pos, abstol=abstol):
    '''build new tree that merges all degenerate edges.

    when merging an edge, the lexicographically smaller node will
    survive. returns a tree and a matching dict of steiner node
    positions.
    '''
    degedges = degenerate_edges(tree, steiner_pos, abstol)

    # key: removed node, value: remaining node (taking over)
    turn_into = {}
    for u, v in degedges:
        if tree.is_terminal(u) and tree.is_terminal(v):
            # don't merge terminals
            continue
        elif tree.is_terminal(u):
            # keep terminals
            pass
        elif tree.is_terminal(v):
            # keep terminals
            u, v = v, u
        elif v < u:
            # keep lexicographically smaller node
            u, v = v, u

        turn_into[v] = u

    # merge nodes into transitive end-point
    for v, u in turn_into.iteritems():
        while u in turn_into:
            u = turn_into[u]
        turn_into[v] = u

    # build new tree data
    new_nodes = [u for u in tree.get_nodes() if u not in turn_into]
    new_edges = []
    for u, v in tree.get_arcs():
        uu, vv = turn_into.get(u, u), turn_into.get(v, v)
        if uu != vv: # remove self-loops
            new_edges.append((uu, vv))
    new_tree = SteinerTree(new_nodes, new_edges, tree.get_terminal_positions())
    new_pos = {s:steiner_pos[s] for s in steiner_pos if s in new_nodes}

    return new_tree, new_pos
