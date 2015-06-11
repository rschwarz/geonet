import pytest

from geonet.network import Net, SteinerTree
from geonet.flow import find_arc_flow, make_forward_flow

def test_treeflow():
    '''Check that (unique) flow values are computed correctly.'''
    nodes = 'abcdef'
    arcs = ['ac', 'bc', 'cd', 'de', 'df']
    net = Net(nodes, arcs)

    demand = {'a': -7, 'b': -5, 'e':12}

    flows = find_arc_flow(net, demand)

    assert flows['a', 'c'] == 7
    assert flows['b', 'c'] == 5
    assert flows['c', 'd'] == 12
    assert flows['d', 'e'] == 12
    assert flows['d', 'f'] == 0

def test_imbalance():
    '''Check exception for unbalanced data'''
    net = Net('ab', ['ab'])
    demand = {'a':4}
    with pytest.raises(AssertionError) as e:
        flows = find_arc_flow(net, demand)
    assert 'flow not balanced' in str(e.value)

def test_make_forward_flow():
    O = (0, 0)
    tree = SteinerTree('abcs', ['as', 'bs', 'cs'], {'a':O, 'b':O, 'c':O})
    flow = {('a', 's'):20, ('b','s'):-5, ('c','s'):-15}

    new_tree, new_flow = make_forward_flow(tree, flow)
    assert set(tree.get_nodes()) == set(new_tree.get_nodes())
    assert set(tree.get_terminal_nodes()) == set(new_tree.get_terminal_nodes())
    assert len(tree.get_arcs()) == len(new_tree.get_arcs())
    assert tree.get_terminal_positions() == new_tree.get_terminal_positions()

    assert ('a', 's') in new_tree.get_arcs()
    assert ('s', 'a') not in new_tree.get_arcs()

    assert ('s', 'b') in new_tree.get_arcs()
    assert ('b', 's') not in new_tree.get_arcs()

    assert ('s', 'c') in new_tree.get_arcs()
    assert ('c', 's') not in new_tree.get_arcs()
