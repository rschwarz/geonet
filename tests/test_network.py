from geonet.network import Net, SteinerTree

def test_Net():
    nodes = ['a', 'b', 'c', 'd']
    arcs = [('a', 'b'), ('b', 'c'), ('c', 'd'), ('a', 'c')]

    net = Net(nodes, arcs)
    assert set(net.get_nodes()) == set(nodes)
    assert set(net.get_arcs()) == set(arcs)

    assert net.get_degree('a') == 2
    assert net.get_degree('b') == 2
    assert net.get_degree('c') == 3
    assert net.get_degree('d') == 1

    assert set(net.get_neighbors('a')) == set('bc')
    assert set(net.get_neighbors('b')) == set('ac')
    assert set(net.get_neighbors('c')) == set('abd')
    assert set(net.get_neighbors('d')) == set(['c'])

def test_SteinerTree():
    nodes = ['a', 'b', 'c', 's']
    arcs = [('a', 's'), ('b', 's'), ('c', 's')]
    pos = {'a': (0,0), 'b': (1,0), 'c': (0,1)}

    tree = SteinerTree(nodes, arcs, pos)

    for n in 'abc':
        assert tree.is_terminal(n)
    assert tree.is_steiner('s')
