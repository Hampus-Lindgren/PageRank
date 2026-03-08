import csv, networkx as nx
import cython_string
from collections import defaultdict

#@profile
def parseOriginal(filename, isDirected):
    with open(filename, 'r') as file:
        reader = csv.reader(file, delimiter=',')
        data = [row for row in reader]
        file.close()
    if isDirected:
        return parse_directed(data)
    else:
        return parse_undirected(data)

#@profile
def parse(filename, isDirected):

    label_to_id: dict[str, int] = {}
    id_to_label: dict[int, str] = {}
    outlinks: defaultdict[int, list] = defaultdict(list)
    next_id = [0]

    def get_or_create_id(label: str, next_id: list) -> int:
        if label not in label_to_id:
            label_to_id[label] = next_id[0]
            id_to_label[next_id[0]] = label
            next_id[0] += 1
        return label_to_id[label]

    with open(filename, 'r') as file:
        reader = csv.reader(file, delimiter=',')
        for row in reader:
            src_label = row[0]
            dst_label = row[2]

            src_id = get_or_create_id(src_label, next_id)
            dst_id = get_or_create_id(dst_label, next_id)

            outlinks[src_id].append(dst_id)
            if not isDirected:
                outlinks[dst_id].append(src_id)
    
    return (label_to_id, id_to_label, outlinks)


#@profile
def parse_undirected(data):
    G = nx.Graph()
    edges = [(row[0], row[2]) for row in data]
    G.add_edges_from(edges)

    return G


#@profile
def parse_directed(data):
    DG = nx.DiGraph()

    for row in data:

        node_a = cython_string.format_key(row[0])
        node_b = cython_string.format_key(row[2])
        val_a = cython_string.digits(row[1])
        val_b = cython_string.digits(row[3])

        if val_a >= val_b:
            DG.add_edge(node_a, node_b)
        else:
            DG.add_edge(node_b, node_a)

    return DG

def parse_directed2(data):
    DG = nx.DiGraph()

    for row in data:

        node_a = cython_string.format_key(row[0])
        node_b = cython_string.format_key(row[2])
        val_a = cython_string.digits(row[1])
        val_b = cython_string.digits(row[3])

        if val_a >= val_b:
            nx.add_path(DG, [node_a, node_b])
        else:
            nx.add_path(DG, [node_b, node_a])

    return DG