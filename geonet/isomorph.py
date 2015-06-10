'''
Graph ismorphism for (full Steiner) tress.
'''

import networkx as nx

from geonet.network import Net, SteinerTree

def are_isomorphic(tree1, tree2):
    '''checks isomorphism for two given (undirected) trees

    Implemented by uncritical copy from "Fampa et al.: A specialized
    branch-and-bound algorithm for the Euclidean Steiner tree problem
    in n-space", algorithm 2.
    '''
    t1 = tree1.dg.to_undirected()
    t2 = tree2.dg.to_undirected()

    label1 = {}
    label2 = {}
    label = 1

    # TODO: What about singletons? It seems to "just work".

    # begin by labeling all leaves the same
    leaves1 = [n for n in t1.nodes() if t1.degree(n) == 1]
    leaves2 = [n for n in t2.nodes() if t2.degree(n) == 1]
    if len(leaves1) != len(leaves2):
        return False
    for n in leaves1:
        label1[n] = label
    for n in leaves2:
        label2[n] = label
    label += 1

    # add labels until difference or isomorphism found
    while True:
        # find unlabeled nodes with at most one unlabeled neighbor
        next1, next2 = [], []
        for n in t1.nodes():
            if n in label1:
                continue
            if sum(m not in label1 for m in t1.neighbors(n)) <= 1:
                next1.append(n)
        for n in t2.nodes():
            if n in label2:
                continue
            if sum(m not in label2 for m in t2.neighbors(n)) <= 1:
                next2.append(n)
        if len(next1) != len(next2):
            return False

        if next1 == []:
            return True

        # compute tentative labels as multiset of neighbors' labels
        tent1, tent2 = [], []
        for n in next1:
            labels = [label1[m] for m in t1.neighbors(n) if m in label1]
            tent1.append((sorted(labels), n))
        for n in next2:
            labels = [label2[m] for m in t2.neighbors(n) if m in label2]
            tent2.append((sorted(labels), n))

        # compare tentative labels
        tent1.sort()
        tent2.sort()
        if any(t1[0] != t2[0] for t1, t2 in zip(tent1, tent2)):
            return False

        # add new labels
        smallest = tent1[0][0]
        for tl, n in tent1:
            if tl == smallest:
                label1[n] = label
            else:
                break
        for tl, n in tent2:
            if tl == smallest:
                label2[n] = label
            else:
                break
        label += 1


def enum_Steiner_only(n, steiner_ids=None):
    '''Enumerate all representative trees.

    This considers only the trees interconnecting the Steiner nodes
    for full Steiner trees of n terminals.

    Following "Fampa et al.: A specialized branch-and-bound algorithm
    for the Euclidean Steiner tree problem in n-space", algorithm 1.
    '''
    # optional node IDs for Steiner nodes
    if steiner_ids is None:
        steiner_ids = ['s%02d' % d for d in range(1, n - 1)]
    assert len(steiner_ids) == n - 2

    # resulting data structures
    nclasses = {} # key: number of Steiner nodes
    reprtree = {} # key: (number of Steiner nodes, class id)

    # initialize with single representative for 2 Steiner nodes
    cur_nodes = steiner_ids[:2]
    cur_edges = [tuple(cur_nodes)]
    nclasses[2] = 1
    reprtree[2, 0] = Net(cur_nodes, cur_edges)

    # incrementally add another Steiner node
    for j in range(3, n - 2 + 1):
        nclasses[j] = 0
        cur_nodes.append(steiner_ids[j - 1])

        # for each (smaller) representative tree
        for k in range(nclasses[j - 1]):
            # for each possible connection point
            for i in range(1, j):
                # enforce maximum degree of 3
                if reprtree[j - 1, k].get_degree(steiner_ids[i - 1]) == 3:
                    continue

                # tentatively build new representative
                new_edge = (steiner_ids[i - 1], steiner_ids[j - 1])
                cur_edges = reprtree[j - 1, k].get_arcs() + [new_edge]
                cur_tree = Net(cur_nodes, cur_edges)

                # skip tree if isomorphic to other representative
                if any(are_isomorphic(cur_tree, reprtree[j, l])
                       for l in range(nclasses[j])):
                    continue

                # add representative for new class
                reprtree[j, nclasses[j]] = cur_tree
                nclasses[j] += 1

    return nclasses, reprtree


def label_fst(tree):
    '''Computes a labeling of a Full Steiner Tree.

    This can be used to check for isomorphic trees (having same
    label).

    Following "Fampa et al.: A specialized branch-and-bound algorithm
    for the Euclidean Steiner tree problem in n-space", algorithm 4.
    '''
    assert isinstance(tree, SteinerTree)
    terms = tree.get_terminal_nodes()
    stein = tree.get_steiner_nodes()

    # build rooted (binary) tree with lexicographical ordering
    label = {}
    for t in terms:
        label[t] = t

    root = min(terms)

    # set labels for all Steiner nodes
    g = tree.dg.to_undirected()
    bfs = list(nx.bfs_edges(g, root))[::-1]
    for i in range(len(bfs)/2):
        t1, h1 = bfs[2*i]
        t2, h2 = bfs[2*i + 1]
        assert t1 == t2
        assert tree.is_steiner(t1)
        assert t1 not in label
        l1, l2 = label[h1], label[h2]
        label[t1] = (l1, l2) if l1 < l2 else (l2, l1)

    # return label of Steiner node adjacent to root
    t, h = bfs[-1]
    assert t == root
    assert tree.is_steiner(h)
    return label[h]
