from numpy.testing import assert_allclose

from geonet.geosteiner import geosteiner
from geonet.network import SteinerTree

def test_geosteiner():
    '''call external program and check parsed output'''
    terminals = {'a': (0,0), 'b': (1,0), 'c': (0,1)}
    tree, steiner_pos = geosteiner(terminals)

    assert isinstance(tree, SteinerTree)
    _nodes = tree.get_nodes()
    _arcs = tree.get_arcs()

    assert len(_nodes) == 3 + 1
    assert len(_arcs) == 3
    assert len(steiner_pos) == 1

    for k in terminals:
        assert tree.is_terminal(k)
    for k in steiner_pos:
        assert tree.is_steiner(k)

    s = '_0'
    assert s in steiner_pos
    assert_allclose(steiner_pos[s], (0.211, 0.211), atol=1e-3)
