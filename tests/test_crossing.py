import py.test

from geonet.network import SteinerTree
from geonet.crossing import crossing_edges

def test_no_crossings():
    no_edge = SteinerTree('a', [], {'a':(0, 0)})
    assert crossing_edges(no_edge, {}) == []

    edge = SteinerTree('ab', ['ab'], {'a':(0, 0), 'b':(0, 1)})
    assert crossing_edges(edge, {}) == []

    path = SteinerTree('abc', ['ab', 'bc'], {'a':(0, 0), 'b':(0, 1), 'c':(0, 2)})
    assert crossing_edges(edge, {}) == []

    star = SteinerTree('abcs', ['as', 'bs', 'cs'],
                       {'a':(0, 0), 'b':(2, 0), 'c':(0, 2)})
    assert crossing_edges(star, {'s': (1, 1)}) == []

def test_crossings():
    pair = SteinerTree('abcd', ['ab', 'cd'],
                       {'a': (0, 1), 'b': (2, 1), 'c': (1, 0), 'd': (1, 2)})
    edges = crossing_edges(pair, {})
    assert len(edges) == 1
    assert set(edges[0]) == set([('a', 'b'), ('c', 'd')])

    path = SteinerTree('abcde', ['ab', 'bc', 'cd', 'de'],
                       {'a': (1, 0), 'b': (1, 1), 'c': (2, 0), 'e': (0, 0)})
    edges = crossing_edges(path, {'d': (2, 1)})
    assert len(edges) == 2
    for p in edges:
        assert ('d', 'e') in p
        assert ('a', 'b') in p or ('b', 'c') in p
    assert edges[0] != edges[1]
