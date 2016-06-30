'''
Wrapper for GeoSteiner program
'''

from itertools import dropwhile, takewhile, ifilter
import os
from subprocess import Popen, PIPE

from geonet.network import SteinerTree

# TODO: check if GeoSteiner is available

def geosteiner(pos):
    '''Call geosteiner to compute and return'''
    def parse_ps(output):
        lines = output.splitlines()
        no_pre = dropwhile(lambda l:' % fs' not in l, lines)
        end_kwds = ['Euclidean SMT', '(Steiner Minimal']
        no_post = takewhile(lambda l: all(kw not in l for kw in end_kwds), no_pre)
        filter_comments = ifilter(lambda l: ' % fs' not in l, no_post)
        arcs = [l.split()[:4] for l in filter_comments]
        return arcs

    def build_tree(nodes, raw_arcs, pos):
        _nodes = list(nodes)
        _arcs = []
        _steiner_pos = {}

        num = 0
        for ra in raw_arcs:
            if ra[1] == 'T':
                tail = nodes[int(ra[0])]
            else: # must be Steiner node
                coords = '_'.join(ra[0:2])
                if coords in _steiner_pos:
                    tail = _steiner_pos[coords]
                else:
                    node = '_%d' % num
                    _nodes.append(node)
                    tail = _steiner_pos.setdefault(coords, node)
                    num += 1
            if ra[3] == 'T':
                head = nodes[int(ra[2])]
            else: # must be Steiner node
                coords = '_'.join(ra[2:4])
                if coords in _steiner_pos:
                    head = _steiner_pos[coords]
                else:
                    node = '_%d' % num
                    _nodes.append(node)
                    head = _steiner_pos.setdefault(coords, node)
                    num += 1

            _arcs.append((tail, head))

        tree = SteinerTree(_nodes, _arcs, pos)

        steiner_pos = {}
        for k,v in _steiner_pos.items():
            node = v
            coords = k.split('_')
            steiner_pos[node] = float(coords[0]), float(coords[1])

        return tree, steiner_pos

    nodes = list(sorted(pos.keys()))
    nodeset = ''.join('%4d %4d\n' % pos[n] for n in nodes)
    efst = Popen(['efst'], stdin=PIPE, stdout=PIPE)
    efst_output, _ = efst.communicate(nodeset)
    bb = Popen(['bb'], stdin=PIPE, stdout=PIPE)
    output, _ = bb.communicate(efst_output)
    raw_arcs = parse_ps(output)
    tree, steiner_pos = build_tree(nodes, raw_arcs, pos)

    return tree, steiner_pos
