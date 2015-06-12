'''
Diameter selection for fixed topology and node positions.

Solved as linear program with cvxpy
'''

import cvxpy as cvx

from geonet.flow import make_forward_flow

def solve(tree, flow, steiner_pos, diams, costs, pres_bds, C=1.0, verbose=False):
    '''minimize diameter cost of a network with fixed node locations.

    args:
    - tree        : Steiner tree (fixed terminal positions)
    - flow        : dict from arc tuple (assumed positive)
    - steiner_pos : positions for Steiner nodes
    - diams       : diameter values (sorted increasingly)
    - costs       : diameter cost factors
    - pres_bds    : uniform pressure bounds
    - C           : constant coefficient in Weymouth equation
    - verbose     : show solver output

    returns:
    - equivalent diameters for each edge
    - pressures at nodes
    - objective value
    '''
    # prepare data
    tree, flow = make_forward_flow(tree, flow)

    N = tree.get_nodes()
    A = tree.get_arcs()
    I = range(len(diams))
    AI = [(a,i) for a in A for i in I]

    assert all(flow[a] > 0.0 for a in A)

    pos = {}
    pos.update(tree.get_terminal_positions())
    pos.update(steiner_pos)
    assert all(n in pos for n in N)

    L = {}
    for a in A:
        xu, xv = pos[a[0]], pos[a[1]]
        L[a] = ((xu[0] - xv[0])**2 + (xu[1] - xv[1])**2)**0.5

    # squared pressure at node
    pp = {n:cvx.Variable(1) for n in N}

    # relative length of pipe segment for differnet diameters
    l = {(a, i):cvx.Variable(1) for (a, i) in AI}

    conss = []

    # pressure in bounds
    for n in N:
        conss += [pres_bds[0]**2 <= pp[n], pp[n] <= pres_bds[1]**2]

    # relative lengths are convex combinations
    for a in A:
        conss += [sum(l[a, i] for i in I) == 1.0]
        conss += [0 <= l[a, i] for i in I]

    # Weymouth equation on pipes
    for a in A:
        u, v = a
        cvx_comb = sum(diams[i]**(-5) * l[a, i] for i in I)
        conss += [pp[u] - pp[v] == C * L[a] * flow[a]**2 * cvx_comb]

    # minimize total pipe cost
    obj = sum(L[a] * costs[i] * l[a,i] for (a,i) in AI)

    prob = cvx.Problem(cvx.Minimize(obj), conss)
    opt = prob.solve(solver=cvx.CVXOPT, verbose=verbose)

    if prob.status == cvx.OPTIMAL:
        pres = {n: pp[n].value**0.5 for n in N}
        diams = {a: sum(diams[i]**(-5)*l[a,i].value for i in I)**(-0.2) for a in A}
        return diams, pres, prob.value
    else:
        print 'Problem not solved:', prob.status
        return None, None. None
