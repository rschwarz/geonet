from itertools import combinations

import pytest

import networkx as nx

from geonet.network import Net, SteinerTree
from geonet.isomorph import are_isomorphic, enum_Steiner_only, label_fst, \
    default_steiner_ids

def test_default_steiner_ids():
    '''Check some valid properties of IDs'''
    assert len(default_steiner_ids(0)) == 0
    assert len(default_steiner_ids(1)) == 0
    assert len(default_steiner_ids(2)) == 0

    id3 = default_steiner_ids(3)
    assert len(id3) == 1
    assert sorted(id3) == id3
    assert len(set(id3)) == len(id3)

    id4 = default_steiner_ids(4)
    assert len(id4) == 2
    assert sorted(id4) == id4
    assert len(set(id4)) == len(id4)

    id5 = default_steiner_ids(5)
    assert len(id5) == 3
    assert sorted(id5) == id5
    assert len(set(id5)) == len(id5)

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

# tests for label_fst

def test_label_fst():
    '''Label small FSTs and check results'''
    O = (0, 0) # dummy location

    Y = SteinerTree('abcs', ['as', 'bs', 'cs'], {'a':O, 'b':O, 'c':O})
    assert label_fst(Y) == ('b', 'c')

    H = SteinerTree('abcdst', ['as', 'bs', 'st', 'tc', 'td'],
                    {'a':O, 'b':O, 'c':O, 'd': O})
    assert label_fst(H) == ('b', ('c', 'd'))

    # from Fampa, figure 4
    t8 = SteinerTree('123456789abcdefg',
                     ['1a', 'ab', 'ac', 'bd', 'b2', 'ce', 'cf', 'd3', 'd4',
                      'eg', 'e5', 'f6', 'f7', 'g8', 'g9'],
                     {'1':O, '2':O, '3':O, '4':O, '5':O, '6':O, '7':O,
                      '8':O, '9':O})
    assert label_fst(t8) == ((('2', ('3', '4')), (('5', ('8', '9')), ('6', '7'))))
