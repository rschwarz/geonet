import pytest

from geonet.network import SteinerTree
from geonet.flow import find_arc_flow
from geonet.diameter import solve

TOL = 1e-5

def test_solve():
    '''Solve model and check some solution properties'''
    tree = SteinerTree('abcs', ['as', 'bs', 'cs'],
                       {'a':(0,0), 'b':(10,0), 'c':(0,10)})
    demand = {'a':-30, 'b':20, 'c':10}
    diams = [0.4, 0.6, 0.8, 1., 1.2]
    costs = [680., 910., 1200., 1550., 1960.]
    pres = [40, 80]
    C = 1.0
    steiner_pos = {'s':(5, 5)}

    flow = find_arc_flow(tree, demand)

    ds, ps, obj = solve(tree, flow, steiner_pos, diams, costs, pres, C)
    assert obj is not None

    for n, p in ps.items():
        assert p >= min(pres) - TOL
        assert p <= max(pres) + TOL

    for a, d in ds.items():
        assert d >= min(diams) - TOL
        assert d <= max(diams) + TOL
