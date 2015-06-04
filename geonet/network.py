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

    def get_degree(self, n):
        return self.dg.degree(n)

    def get_neighbors(self, n):
        return self.dg.predecessors(n) + self.dg.successors(n)


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

    def get_terminal_nodes(self):
        return [n for n in self.get_nodes() if self.is_terminal(n)]

    def get_steiner_nodes(self):
        return [n for n in self.get_nodes() if self.is_steiner(n)]

    def is_full_steiner_topology(self):
        '''or is the tree degenerate?

        three criteria are applied:
        1. number of Steiner nodes equals the number of terminals - 2
        2. Steiner nodes have degree 3
        3. Terminals have degree 1 and are connected to Steiner nodes
        '''
        terms = self.get_terminal_nodes()
        steins = self.get_steiner_nodes()

        # special cases for n < 3
        if len(terms) < 3 and len(steins) == 0:
            return True
        # general case
        if len(steins) != len(terms) - 2:
            return False
        if any(self.get_degree(s) != 3 for s in steins):
            return False
        if any(self.get_degree(t) != 1 for t in terms):
            return False
        for t in terms:
            neighbors = self.get_neighbors(t)
            assert len(neighbors) == 1
            n = neighbors[0]
            if self.is_terminal(n):
                return False
        return True
