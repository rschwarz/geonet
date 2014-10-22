'''
Data structures for (Steiner) tree networks
'''

import networkx as nx

class Net(object):
    '''Network'''

    def __init__(self, nodes, arcs):
        '''
        nodes: node IDs
        arcs: tuples of node IDs (tail, head)
        '''
        self.dg = nx.DiGraph()
        self.dg.add_nodes_from(nodes)
        self.dg.add_edges_from(arcs)

    def get_nodes(self):
        return self.dg.nodes()

    def get_arcs(self):
        return self.dg.edges()

class SteinerTree(Net):
    '''Steiner tree with some node positions fixed'''

    def __init__(self, nodes, arcs, pos):
        '''
        nodes: node IDs
        arcs: tuples of node IDs (tail, head)
        pos: map from (terminal) node IDs to position tuple
        '''
        super(SteinerTree, self).__init__(nodes, arcs)
        for k,v in pos.items():
            self.dg.node[k]['pos'] = v

    def is_steiner(self, n):
        return not self.is_terminal(n)

    def is_terminal(self, n):
        return 'pos' in self.dg.node[n]
