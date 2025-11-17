from collections import defaultdict


def bron_kerbosch(graph, R=set(), P=set(), X=set()):
    # Implemented the algorithm from pseudocode.
    # P = set(self.graph.keys())
    # largest_clique = max(cliques, key=len)
    cliques = []
    if not P and not X:
        cliques.append(",".join(map(str, sorted(R))))
        return
    for v in list(P):  # Making P a list to allow modifications in loop
        bron_kerbosch(
            graph, R.union({v}), P.intersection(graph[v]), X.intersection(graph[v])
        )
        P.remove(v)
        X.add(v)
