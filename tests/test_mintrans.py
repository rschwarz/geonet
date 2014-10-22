import numpy as np
from numpy.testing import assert_allclose

from geonet.flow import find_arc_flow
from geonet.geometry import star_angles
from geonet.mintrans import steiner_pos
from geonet.network import SteinerTree



def test_length():
    '''check Steiner tree geometric property for minimized length'''
    nodes = 'abcs'
    arcs = ['as', 'bs', 'cs']
    terminals = {'a': (0,0), 'b': (1,0), 'c': (0,1)}
    tree = SteinerTree(nodes, arcs, terminals)

    flow = find_arc_flow(tree, {'a':-4, 'b':2, 'c':2})

    pos = steiner_pos(tree, flow, flow_exp=0.0)

    # check that fixed positions are kept
    for k,v in terminals.items():
        assert_allclose(pos[k], v, atol=1e-7)

    # check (known) optimal position
    assert_allclose(pos['s'], (0.211, 0.211), atol=1e-3)

    # check angle property of Steiner node position
    # all angles are equal (to 120 deg = 2/3 pi)
    angles = star_angles('s', 'abc', pos)
    assert_allclose(angles, [2.0/3.0*np.pi]*3, atol=1e-4)
