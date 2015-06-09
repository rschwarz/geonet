from itertools import combinations

import pytest

from geonet.network import Net
from geonet.isomorph import are_isomorphic

graphs = [
    Net([], []),
    Net('a', []),
    Net('ab', []),
    Net('ab', [('a', 'b')]),
    Net('abc', [('a', 'b')]),
    Net('abc', [('a', 'b'), ('a', 'c')]),
    Net('abcd', [('a', 'b'), ('c', 'd')]),
    Net('abcd', [('a', 'b'), ('b', 'c'), ('c', 'd')]),
    Net('abcd', [('a', 'b'), ('a', 'c'), ('a', 'd')]),
    Net('abcde', [('a', 'b'), ('b', 'c'), ('c', 'd'), ('d', 'e')]),
    Net('abcde', [('a', 'b'), ('a', 'c'), ('a', 'd'), ('a', 'e')]),
    Net('abcde', [('a', 'b'), ('a', 'c'), ('a', 'e'), ('d', 'e')]),
]

def test_non_isomorphic_cases():
    '''Compare some non-isomorphic graphs.'''
    for g1, g2 in combinations(graphs, 2):
        assert not are_isomorphic(g1, g2)

def test_rename_is_isomorphic():
    '''Renaming nodes and arcs gives isomorphic graphs.'''
    def uppercase(net):
        ucnodes = [n.upper() for n in net.get_nodes()]
        ucarcs = [(t.upper(), h.upper()) for (t, h) in net.get_arcs()]
        return Net(ucnodes, ucarcs)

    for net in graphs:
        assert are_isomorphic(net, uppercase(net))
