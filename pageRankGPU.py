import operator, sys, cProfile, timeit
from utilsGPU import parse
import cupy as cp
from numpy import argsort, array as numpyarray

class Graph:
    def __init__(self, graph: tuple[dict[str, int], dict[int, str], cp.ndarray, cp.ndarray], directed: bool):

        self.label_to_id, self.id_to_label, self.adjacency_matrix, self.outlinks = graph

        self.V = len(self.label_to_id) # Number of vertices in graph
        self.d = 0.85
        self.directed = directed
        self.const = ((1 - self.d) * (1/float(self.V))) # Constant factor used in computations

        self.ranks = cp.ones(self.V) / float(self.V) # Array to store each node's PageRank

    def rank(self, num_iterations):
        """Compute the PageRank of all the nodes in the graph"""
        for i in range(num_iterations):
            update_factors = self.ranks / self.outlinks # compute rank / outlinks for all vertices
            update_factors = cp.where(cp.isinf(update_factors), 0, update_factors) # fix cases where zero outlinks have caused division by zero
            rank_sums = self.const + self.d * (self.adjacency_matrix @ update_factors)
            self.ranks = rank_sums

def run(filename, directed, num_iterations):
    graph = parse(filename, directed)
    p = Graph(graph, directed)
    p.rank(num_iterations)

    ranks_cpu = p.ranks.get()
    labels = numpyarray([p.id_to_label[i] for i in range(p.V)])

    sorted_indices = argsort(ranks_cpu)[::-1]
    sorted_ranks = list(zip(labels[sorted_indices], ranks_cpu[sorted_indices]))

    return sorted_ranks

if __name__ == '__main__':
    if len(sys.argv) < 3:
        print('Expected input format: python pageRank.py <data_filename> <directed OR undirected> <number of iterations>')
    else:
        filename = sys.argv[1]
        isDirected = sys.argv[2] == 'directed'
        num_iterations = int(sys.argv[3])
        
        sorted_ranks = run(filename, isDirected, num_iterations)
        for tup in sorted_ranks[0:10]:
            print('{0:30} :{1:10}'.format(str(tup[0]), tup[1]))
