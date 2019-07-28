"""graphs2nx.py"""
__author__ = 'Carel van Niekerk'
__version__ = '0.1'
__date__ = '28/07/2019'


# Load Packages
import networkx as nx


def graphs2nx(Graph):
    # Extracting all info from the pulse graph
    node_names = Graph.Scale.keys()
    node_scales = Graph.Scale.values()
    node_values = Graph.Value.values()
    node_neighbours = Graph.Neighbours.values()

    # Define new Graph and add in nodes
    G = nx.Graph()
    for name, scale, value in zip(node_names, node_scales, node_values):
        G.add_node(name, scale=scale, value=value)

    # Define all edges
    edges = [(str(i+1),str(j)) for i,neigh in enumerate(node_neighbours) for j in neigh]
    G.add_edges_from(edges)

    return G