import operator, sys, cProfile, networkx as nx
from utils import parse, parseOriginal
from collections import defaultdict
import cupy as cp

class Graph:
    #@profile
    def __init__(self, graph: tuple[dict[str, int], dict[int, str], defaultdict[int, list]], directed: bool):

        self.label_to_id, self.id_to_label, self.outgoing_edges = graph[0], graph[1], graph[2]

        self.V = len(self.label_to_id)

        self.adjacency_matrix = cp.zeros((self.V, self.V), dtype=int)
        for i in range(self.V):
            self.adjacency_matrix[i][self.outgoing_edges[i]] = 1

        self.d = 0.85
        self.directed = directed
        self.const = ((1 - self.d) * (1/float(self.V)))
        
        self.outlinks = cp.array([len(self.outgoing_edges[i]) for i in range(self.V)]) # number of outgoing links from each vertex
        self.ranks = cp.ones(self.V) / float(self.V)

    
    #@profile
    def rank(self):
        for _ in range(10):
            # compute rank / outlinks for all vertices
            update_factors = self.ranks / self.outlinks
            update_factors = cp.where(cp.isinf(update_factors), 0, update_factors) # fix cases where the number of outlinks is zero

            rank_sums = self.const + self.d * (self.adjacency_matrix @ update_factors)
            self.ranks = rank_sums

            """for node in range(self.V): # iterate over all nodes
                current_outgoing = self.outgoing_edges[node] # get adjacency list of node
                rank_sum = cp.nansum(update_factors[current_outgoing]) # sum values of all adjacent nodes

                self.ranks[node] = self.const + self.d * rank_sum # update ranks with new values
            
            print(rank_sums[0:32] - self.ranks[0:32])"""

       # return p

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
        # it doesn't seem like there's any point in distinguishing between the directed and undirected case here, 
        # it just takes more time for the same result
        for key, _ in self.graph.nodes(data=True):
            self.ranks[key] = 1/float(self.V)
        
        for _ in range(10):
            for key, node in self.graph.nodes(data=True): # iterate over all nodes
                rank_sum = 0

                if self.directed: # Graph is directed
                    for n in self.adjacency[key]:
                        if (outlinks := len(self.adjacency[n])) > 0:
                            rank_sum += self.ranks[n] / outlinks

                else: # Graph is undirected
                    for n in self.graph[key]:
                        if self.ranks[n] is not None:
                            outlinks = self.degrees[n]
                            rank_sum += self.ranks[n] / outlinks
            
                # actual page rank compution
                self.ranks[key] = self.const + self.d * rank_sum

        return p

if __name__ == '__main__':
    if len(sys.argv) == 1:
        print('Expected input format: python pageRank.py <data_filename> <directed OR undirected>')
    else:
        filename = sys.argv[1]
        isDirected = sys.argv[2] == 'directed'

        graph = parse(filename, isDirected)
        p = Graph(graph, isDirected)
        p.rank()

        sorted_ranks = sorted([(p.id_to_label[i], p.ranks[i]) for i in range(p.V)], key=operator.itemgetter(1), reverse=True)

        #sorted_ranks = sorted(p.ranks.items(), key=operator.itemgetter(1), reverse=True)
        for tup in sorted_ranks:
            print('{0:30} :{1:10}'.format(str(tup[0]), tup[1]))
