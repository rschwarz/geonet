from geonet.network import Net
from geonet.flow import find_arc_flow

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
