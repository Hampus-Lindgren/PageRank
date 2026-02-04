import operator, sys, cProfile, networkx
from utils import parse

class PageRank:
    def __init__(self, graph: networkx.Graph, directed: bool):
        """
        Args:
            graph (networkx.Graph): Graph object.
            directed (bool): Whether or not the graph is directed.
        """
        self.graph = graph
        self.V = len(self.graph)
        self.d = 0.85
        self.directed = directed
        self.ranks = dict()
    
    def rank(self):
        for key, node in self.graph.nodes(data=True):
            if self.directed:
                self.ranks[key] = 1/float(self.V)
            else:
                self.ranks[key] = node.get('rank')

        for _ in range(10):
            for key, node in self.graph.nodes(data=True):
                rank_sum = 0
                curr_rank = node.get('rank')
                if self.directed: # Graph is directed
                    neighbors = self.graph.out_edges(key)
                    for n in neighbors:
                        outlinks = len(self.graph.out_edges(n[1]))
                        if outlinks > 0:
                            rank_sum += (1 / float(outlinks)) * self.ranks[n[1]]
                else: # Graph is undirected
                    neighbors = self.graph[key]
                    for n in neighbors:
                        if self.ranks[n] is not None:
                            outlinks = len(list(self.graph.neighbors(n)))
                            rank_sum += (1 / float(outlinks)) * self.ranks[n]
            
                # actual page rank compution
                self.ranks[key] = ((1 - float(self.d)) * (1/float(self.V))) + self.d*rank_sum

        return p

if __name__ == '__main__':
    if len(sys.argv) == 1:
        print('Expected input format: python pageRank.py <data_filename> <directed OR undirected>')
    else:
        filename = sys.argv[1]
        isDirected = False
        if sys.argv[2] == 'directed':
            isDirected = True

        graph = parse(filename, isDirected)
        p = PageRank(graph, isDirected)
        cProfile.run('p.rank()', sort="cumtime")

        sorted_r = sorted(p.ranks.items(), key=operator.itemgetter(1), reverse=True)

        for tup in sorted_r:
            print('{0:30} :{1:10}'.format(str(tup[0]), tup[1]))
