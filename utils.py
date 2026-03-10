import csv
import cython_string
from collections import defaultdict
import cupy as cp
import numpy as np
import cupyx.scipy.sparse as csp
import scipy.sparse as sparse
#@profile
def parse(filename: str, is_directed: bool):
    """
    Parses an input CSV file into the necessary data structures.

    :param filename: The name of the file.
    :type filename: str
    :param is_directed: Whether the file should be interpreted as a directed or undirected graph.
    :type is_directed: bool
    :returns: Data structures representing graph.
    :rtype: dict[str, int], dict[int, str], defaultdict[int, list]
    """

    label_to_id: dict[str, int] = {}
    id_to_label: dict[int, str] = {}
    #adjacency_list: defaultdict[int, list] = defaultdict(list)
    rows: list[int] = []
    cols: list[int] = []
    next_id = [0]

    def get_or_create_id(label: str, next_id: list[int]) -> int:
        """
        Returns an ID for the input label, assigning a new one if the label has not already been recorded.

        :param label: The label of the node.
        :type label: str
        :param next_id: One-element list containing the ID to assign if the label has not already been recorded.
        :type next_id: list[int]
        :returns: The ID corresponding to the label.
        :rtype: int
        """
        if label not in label_to_id:
            label_to_id[label] = next_id[0]
            id_to_label[next_id[0]] = label
            next_id[0] += 1
        return label_to_id[label]

    print("Reading data from file...")
    with open(filename, 'r') as file:
        reader = csv.reader(file, delimiter=',')
        for row in reader:
            src_label = cython_string.format_key(row[0])
            dst_label = cython_string.format_key(row[2])

            src_id = get_or_create_id(src_label, next_id)
            dst_id = get_or_create_id(dst_label, next_id)

            val_a = cython_string.digits(row[1])
            val_b = cython_string.digits(row[3])
            
            if is_directed:
                if val_a >= val_b:
                    rows.append(src_id)
                    cols.append(dst_id)
                else:
                    rows.append(dst_id)
                    cols.append(src_id)
            else: # undirected
                rows.append(src_id)
                cols.append(dst_id)
                rows.append(dst_id)
                cols.append(src_id)
    
    print("Data read complete. Building adjacency matrix.")
    assert len(rows) == len(cols)
    data = np.ones(len(rows), dtype=np.bool)
    adjacency_matrix = sparse.coo_array((data, (rows, cols)), shape=(next_id[0], next_id[0])).tocsr()

    #print("Adjacency matrix constructed. Computing outlinks...")


    outlinks = cp.array(adjacency_matrix.sum(axis=1))
    
    adjacency_matrix = csp.csr_matrix(adjacency_matrix)
    #print(adjacency_matrix)

    #print("Outlinks computed. Creating sparse matrix...")

    #adjacency_matrix = csp.csr_matrix(adjacency_matrix)
    #print(adjacency_matrix)

    #print("Sparse matrix complete. Initializing graph...")
    

    return (label_to_id, id_to_label, adjacency_matrix, outlinks)
