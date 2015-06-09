'''
Graph ismorphism for (full Steiner) tress.
'''

def are_isomorphic(tree1, tree2):
    '''checks isomorphism for two given (undirected) trees

    Implemented by uncritical copy from "Fampa et al.: A specialized
    branch-and-bound algorithm for the Euclidean Steiner tree problem
    in n-space"
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
