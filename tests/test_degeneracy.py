import pytest

from geonet.network import SteinerTree
from geonet.degeneracy import degenerate_edges, is_degenerate, merged

@pytest.mark.parametrize("term_pos", [
    {'a':(0,0), 'b':(0,0), 'c':(0,0)},
    {'a':(1,0), 'b':(0,1), 'c':(0,0)},
])
def test_no_steiner(term_pos):
    '''nothing to do for tree with no steiner nodes'''
    tree = SteinerTree('abc', ['ab', 'bc'], term_pos)
    pos = {}
    assert not is_degenerate(tree, pos)
    assert degenerate_edges(tree, pos) == []

    mtree, mpos = merged(tree, pos)
    assert mtree == tree
    assert mpos == pos


@pytest.mark.parametrize("spos,deg,edg", [
    ((1, 1), False, []),
    ((0, 1), False, []),
    ((1, 0), False, []),
    ((0, 0), True, [('a', 's')]),
    ((2, 0), True, [('b', 's')]),
    ((0, 2), True, [('c', 's')]),
])
def test_one_proper_steiner(spos, deg, edg):
    tree = SteinerTree('abcs', ['as', 'bs', 'cs'],
                       {'a':(0,0), 'b':(2,0), 'c':(0,2)})
    pos = {'s': spos}

    assert is_degenerate(tree, pos) == deg
    assert degenerate_edges(tree, pos) == edg

    mtree, mpos = merged(tree, pos)
    if deg:
        assert mtree != tree
        assert len(mtree.get_nodes()) == 3
        assert len(mtree.get_arcs()) == 2
        assert mpos == {}
    else:
        assert mtree == tree
        assert mpos == pos


def test_merged_well():
    tree = SteinerTree('abcdst', ['as', 'bs', 'st', 'tc', 'td'],
                       {'a': (0,0), 'b':(0,2), 'c':(2,2), 'd':(2,0)})
    pos = {'s':(1,1), 't':(1,1)}

    assert is_degenerate(tree, pos)
    assert degenerate_edges(tree, pos) == [('s', 't')]

    mtree, mpos = merged(tree, pos)
    assert mtree != tree
    assert mtree.get_steiner_nodes() == ['s']
    assert set(mtree.get_arcs()) == \
        set([('a', 's'), ('b', 's'), ('s', 'c'), ('s', 'd')])
    assert mpos != pos
    assert mpos == {'s':(1,1)}


def test_merged_multi():
    tree = SteinerTree('abcdst', ['as', 'bs', 'st', 'tc', 'td'],
                       {'a': (0,0), 'b':(0,2), 'c':(2,2), 'd':(2,0)})
    pos = {'s':(0,0), 't':(0,0)}

    assert is_degenerate(tree, pos)
    assert set(degenerate_edges(tree, pos)) == set([('a', 's'), ('s', 't')])

    mtree, mpos = merged(tree, pos)
    assert mtree != tree
    assert mtree.get_steiner_nodes() == []
    assert set(mtree.get_arcs()) == \
        set([('b', 'a'), ('a', 'c'), ('a', 'd')])
    assert mpos != pos
    assert mpos == {}
