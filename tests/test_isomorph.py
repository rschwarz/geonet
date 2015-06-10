from itertools import combinations

import pytest

import networkx as nx

from geonet.network import Net
from geonet.isomorph import are_isomorphic, enum_Steiner_only

# tests for are_isomorphic

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

# tests for enum_Steiner_only

def test_enum_Steiner_only_small():
    '''Enumerate small trees and check results.'''

    # compute all trees connecting up to 6 Steiner nodes (for up to 8
    # terminals) and compare with results from paper
    nclasses, reprtree = enum_Steiner_only(8)
    assert 0 not in nclasses
    assert 1 not in nclasses
    assert nclasses[2] == 1
    assert nclasses[3] == 1
    assert nclasses[4] == 2
    assert nclasses[5] == 2
    assert nclasses[6] == 4
    assert 7 not in nclasses

    # check properties valid for (subtrees of) FSTs
    for t in reprtree.values():
        g = t.dg.to_undirected()
        assert nx.is_connected(g)
        assert max(nx.degree(g).values()) <= 3

    for t1, t2 in combinations(reprtree.values(), 2):
        assert not are_isomorphic(t1, t2)
