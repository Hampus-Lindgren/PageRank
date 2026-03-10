import operator, sys, cProfile, timeit
from utils import parse
from collections import defaultdict
import cupy as np
#import numpy as np
from numpy import argsort, array as numpyarray

class Graph:
    def __init__(self, graph: tuple[dict[str, int], dict[int, str], np.ndarray, np.ndarray], directed: bool):

        self.label_to_id, self.id_to_label, self.adjacency_matrix, self.outlinks = graph

        self.V = len(self.label_to_id) # Number of vertices in graph

        self.d = 0.85
        self.directed = directed
        self.const = ((1 - self.d) * (1/float(self.V))) # Constant factor used in computations

        self.ranks = np.ones(self.V) / float(self.V) # Array to store each node's PageRank

    def rank(self):
        """Compute the PageRank of all the nodes in the graph"""
        for i in range(100):
            update_factors = self.ranks / self.outlinks # compute rank / outlinks for all vertices
            update_factors = np.where(np.isinf(update_factors), 0, update_factors) # fix cases where zero outlinks have caused division by zero
            rank_sums = self.const + self.d * (self.adjacency_matrix @ update_factors)
            self.ranks = rank_sums

if __name__ == '__main__':
    if len(sys.argv) == 1:
        print('Expected input format: python pageRank.py <data_filename> <directed OR undirected>')
    else:
        filename = sys.argv[1]
        isDirected = sys.argv[2] == 'directed'

        start_time = timeit.default_timer()
        graph = parse(filename, isDirected)
        p = Graph(graph, isDirected)
        p.rank()

        ranks_cpu = p.ranks.get()
        #ranks_cpu = p.ranks
        labels = numpyarray([p.id_to_label[i] for i in range(p.V)])

        sorted_indices = argsort(ranks_cpu)[::-1]
        sorted_ranks = list(zip(labels[sorted_indices], ranks_cpu[sorted_indices]))

        print(timeit.default_timer() - start_time)
        
        """for tup in sorted_ranks[0:100]:
            print('{0:30} :{1:10}'.format(str(tup[0]), tup[1]))"""
