'''
Junction location with minimized diameter cost.

Solved as second-order cone program with cvxpy.
'''

import cvxpy as cvx
import numpy as np

def steiner_pos(tree, flow, diams, costs, pres_bds, C=1.0, verbose=False):
    '''minimize diameter cost of network with junction locations.

    args:
    - tree     : Steiner tree (fixed terminal positions)
    - flow     : dict from arc tuple (assumed positive)
    - diams    : diameter values (sorted increasingly)
    - costs    : diameter cost factors
    - pres_bds : uniform pressure bounds
    - C        : constant coefficient in Weymouth equation
    - verbose  : show solver output
    '''
    assert all(flow[a] > 0.0 for a in tree.get_arcs())

    # Node positions
    x = {n:cvx.Variable(2) for n in tree.get_nodes()}

    # Node pressures (squared)
    pp = {n:cvx.Variable(1) for n in tree.get_nodes()}

    # Arc costs
    t = {a:cvx.Variable(1) for a in tree.get_arcs()}

    # fix positions of terminals
    fixed_pos = [x[n] == np.array(tree.dg.node[n]['pos'])
                for n in tree.get_nodes() if tree.is_terminal(n)]

    # second order cone constraints
    socs = []

    N = len(diams)
    J = list(range(N - 1))
    gg = [(costs[j+1]*diams[j]**-5 - costs[j]*diams[j+1]**-5) for j in J]
    ee = [(costs[j+1] - costs[j])/gg[j] for j in J]
    ff = [(diams[j]**-5 - diams[j+1]**-5)/gg[j] for j in J]

    for a in tree.get_arcs():
        u, v = a

        # for the diameter segments
        for j in J:
            e = ee[j] / (C*flow[a]**2)
            socs.append(cvx.norm2(x[u] - x[v]) <= e*pp[u] - e*pp[v] + ff[j]*t[a])

        # for the lower bound on y
        h = diams[-1]**5 / (C*flow[a]**2)
        socs.append(cvx.norm2(x[u] - x[v]) <= h*pp[u] - h*pp[v])

        # for the lower bound on z
        i = 1.0 / costs[0]
        socs.append(cvx.norm2(x[u] - x[v]) <= i*t[a])

    # pressure bounds
    pres_lower = [pp[n] >= min(pres_bds)**2 for n in tree.get_nodes()]
    pres_upper = [pp[n] <= max(pres_bds)**2 for n in tree.get_nodes()]

    # collect constraints
    conss = []
    for c in [fixed_pos, socs, pres_lower, pres_upper]:
        conss += c

    # minimize total cost
    obj = sum(t[a] for a in tree.get_arcs())
    prob = cvx.Problem(cvx.Minimize(obj), conss)
    opt = prob.solve(solver=cvx.CVXOPT, verbose=verbose)

    if prob.status == cvx.OPTIMAL:
        pos = {n:np.array(x[n].value)[:, 0].tolist() for n in tree.get_nodes()}
        return pos
    else:
        print 'Problem not solved:', prob.status
        return None
