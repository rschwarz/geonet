'''
Find crossing edges in solutions.
'''

from itertools import combinations

import numpy as np
import numpy.linalg as la

from geonet.network import SteinerTree, merge_pos
from geonet.geometry import distance
from geonet.constants import abstol


def crossing_edges(tree, steiner_pos, abstol=abstol):
    '''Find crossing edges

    Compare all pairs of edges. The crossing point should not be too
    near one of the edges' end nodes (w.r.t. abstol).
    '''

    assert isinstance(tree, SteinerTree)
    pos = merge_pos(tree, steiner_pos)

    result = []

    for pair in combinations(tree.get_arcs(), 2):
        (a, b), (c, d) = pair
        if a == c or a == d or b == c or b == d:
            continue # skip adjacent edges

        d_ab, d_cd = distance(pos[a], pos[b]), distance(pos[c], pos[d])
        if d_ab < abstol or d_cd < abstol:
            continue # skip degenerate edges

        # solve linear system for intersection of two spanned lines
        # L x = r
        L = np.array([[pos[b][0] - pos[a][0], pos[c][0] - pos[d][0]],
                      [pos[b][1] - pos[a][1], pos[c][1] - pos[d][1]]])
        if la.matrix_rank(L) < 2:
            continue # skip parallel lines
        r = np.array([pos[c][0] - pos[a][0],
                      pos[c][1] - pos[a][1]])
        x = la.solve(L, r)

        reltol = abstol * 2.0 / (d_ab + d_cd)
        if x[0] < reltol or x[0] > 1 - reltol or \
           x[1] < reltol or x[1] > 1 - reltol:
            continue # intersection outside segments (or at boundary)

        result.append(pair)

    return result
