from geonet.network import Net

def test_Net():
    nodes = ['a', 'b', 'c']
    arcs = [('a', 'b'), ('b', 'c'), ('a', 'c')]

    net = Net(nodes, arcs)
    assert set(net.get_nodes()) == set(nodes)
    assert set(net.get_arcs()) == set(arcs)
