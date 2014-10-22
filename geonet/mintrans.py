'''
Minimize transport (momentum).
'''

import cvxpy as cvx
import numpy as np

def steiner_pos(tree, flows, flow_exp=1.0, verbose=False):
    '''minimize flow-weighted length of network with steiner positions

    args:
    - tree: steiner tree (with terminal positions)
    - flows: dict from arc tuple
    - flow_exp: exponent of flow in objective coefficients

    returns dict of positions from node to tuple
    '''
    # TODO: rewrite with vector notation an no loops

    nodes = sorted(tree.get_nodes())
    arcs = sorted(tree.get_arcs())

    # create variables for 2d-positions
    x = {n:cvx.Variable(2) for n in nodes}
    
    # fix positions of terminals
    fixed_pos = [x[n] == np.array(tree.dg.node[n]['pos'])
                 for n in nodes
                 if tree.is_terminal(n)]

    constraints = fixed_pos
    
    obj = sum(flows[u,v]**flow_exp * cvx.norm2(x[u] - x[v]) for u,v in arcs)
    prob = cvx.Problem(cvx.Minimize(obj), constraints)

    opt = prob.solve(solver=cvx.CVXOPT, verbose=verbose)
    sol = {n:np.array(x[n].value)[:, 0].tolist() for n in nodes}
    return sol
