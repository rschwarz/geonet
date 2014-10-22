from geonet.network import Net, SteinerTree

def test_Net():
    nodes = ['a', 'b', 'c']
    arcs = [('a', 'b'), ('b', 'c'), ('a', 'c')]

    net = Net(nodes, arcs)
    assert set(net.get_nodes()) == set(nodes)
    assert set(net.get_arcs()) == set(arcs)

def test_SteinerTree():
    nodes = ['a', 'b', 'c', 's']
    arcs = [('a', 's'), ('b', 's'), ('c', 's')]
    pos = {'a': (0,0), 'b': (1,0), 'c': (0,1)}

    tree = SteinerTree(nodes, arcs, pos)

    for n in 'abc':
        assert tree.is_terminal(n)
    assert tree.is_steiner('s')
