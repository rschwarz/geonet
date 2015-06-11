import pytest

from geonet.network import SteinerTree
from geonet.optimization import Instance, Solution, enum_fsts

def test_enum_fst():
    '''Call and check the structure of result (but not content).'''

    term_pos = {'a':(0,0), 'b':(10,0), 'c':(0,10)}
    demand = {'a':-30, 'b':20, 'c':10}
    diams = [0.4, 0.6, 0.8, 1., 1.2]
    costs = [680., 910., 1200., 1550., 1960.]
    pres = [40, 80]
    C = 1.0
    inst = Instance(term_pos, demand, diams, costs, pres[0], pres[1], C)

    sols = enum_fsts(inst)
    assert len(sols) == 1, 'there is just 1 topology on 3 terminals'

    sol = sols[0]
    assert isinstance(sol.tree, SteinerTree)
    assert sol.tree.is_full_steiner_topology()

    for term in term_pos:
        assert sol.tree.is_terminal(term)

    steins = sol.tree.get_steiner_nodes()
    assert len(steins) == 1
    st = steins[0]
    assert st in sol.steiner_pos
    pos = sol.steiner_pos[st]
    assert pos[0] >= 0 and pos[0] <= 10
    assert pos[1] >= 0 and pos[1] <= 10
