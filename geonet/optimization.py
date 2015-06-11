'''
Optimization methods for the layout of pipeline networks.
'''

from collections import namedtuple

from geonet.network import SteinerTree
import geonet.isomorph
import geonet.flow
import geonet.junction_loc

Instance = namedtuple('Instance', ['term_pos', 'demand', 'diams', 'costs',
                                   'pres_min', 'pres_max', 'C'])


Solution = namedtuple('Solution', ['tree', 'steiner_pos', 'obj'])


def enum_fsts(instance):
    '''Find best network by enumeration of all FST topologies.

    Returns all solutions, sorted by increasing cost.
    '''
    sols = []

    # enumerate all FST topologies
    trees = geonet.isomorph.enum(instance.term_pos)
    for label, tree in trees.iteritems():
        # determine arc flow and orientation
        flow = geonet.flow.find_arc_flow(tree, instance.demand)
        tree, flow = geonet.flow.make_forward_flow(tree, flow)

        # find optimal Steiner node positions
        pos, obj = geonet.junction_loc.steiner_pos(
            tree, flow, instance.diams, instance.costs,
            [instance.pres_min, instance.pres_max], instance.C)

        sols.append(Solution(tree, pos, obj))

    sols.sort(key=lambda s: s.obj)
    return sols
