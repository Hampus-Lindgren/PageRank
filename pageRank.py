import operator, sys, cProfile, networkx as nx
from utils import parse

class PageRank:
    #@profile
    def __init__(self, graph: nx.Graph | nx.DiGraph, directed: bool):
        """
        Args:
            graph (networkx.Graph | networkx.DiGraph): Graph object.
            directed (bool): Whether or not the graph is directed.
        """
        self.graph = graph
        self.V = len(self.graph)
        self.d = 0.85
        self.directed = directed
        self.ranks = dict()
        self.const = ((1 - self.d) * (1/float(self.V)))
        if directed:
            self.adjacency = nx.to_dict_of_lists(graph)
        else:
            self.degrees = dict(self.graph.degree)
    
    #@profile
    def rank(self):
        if self.directed:
            for key, _ in self.graph.nodes(data=True):
                self.ranks[key] = 1/float(self.V)
        else:
            for key, node in self.graph.nodes(data=True):
                self.ranks[key] = node.get('rank')
        
        for _ in range(10): # Why does it run 10 times?
            for key, node in self.graph.nodes(data=True):
                rank_sum = 0
                if self.directed: # Graph is directed
                    for n in self.adjacency[key]:
                        if (outlinks := len(self.adjacency[n])) > 0:
                            rank_sum += self.ranks[n] / outlinks
                else: # Graph is undirected
                    neighbors = self.graph[key]
                    for n in neighbors:
                        if self.ranks[n] is not None:
                            outlinks = self.degrees[n]
                            rank_sum += self.ranks[n] / outlinks
            
                # actual page rank compution
                self.ranks[key] = self.const + self.d*rank_sum

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
        #cProfile.run('p.rank()', sort="cumtime")
        p.rank()
        sorted_r = sorted(p.ranks.items(), key=operator.itemgetter(1), reverse=True)

        for tup in sorted_r:
            print('{0:30} :{1:10}'.format(str(tup[0]), tup[1]))
