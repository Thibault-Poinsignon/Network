
import numpy
import matplotlib.pyplot
import networkx
from itertools import combinations
from pyvis import network
from mpl_toolkits.mplot3d import Axes3D

#Fonctions misc


def ecdf(data):
    "give x and y values ready to plot"
    return numpy.sort(data), numpy.arange(1, len(data) + 1) / len(data)


#Fonctions de représentation graphique

def plot_degree(G):
    """plot of degree."""
    num_neighbors = [len(list(G.neighbors(n))) for n in G.nodes()]
    x, y = ecdf(num_neighbors)
    matplotlib.pyplot.scatter(x, y, marker='+')
    matplotlib.pyplot.xlabel("degree")
    matplotlib.pyplot.ylabel("cumulative fraction")

def plot_degree_centrality(G):
    """plot of degree centrality."""
    x, y = ecdf(list(networkx.degree_centrality(G).values()))
    matplotlib.pyplot.scatter(x, y, marker='+')
    matplotlib.pyplot.xlabel("degree centrality")
    matplotlib.pyplot.ylabel("cumulative fraction")

#Fonction de calcul de chemin

def path_exists(node1, node2, G):
    """
    This function checks whether a path exists between two nodes (node1,
    node2) in graph G.
    """

    visited_nodes = set()
    queue = [node1]

    while len(queue) > 0:
        node = queue.pop()
        neighbors = list(G.neighbors(node))
        if node2 in neighbors:
            return True
        else:
            visited_nodes.add(node)
            nbrs = [n for n in neighbors if n not in visited_nodes]
            queue = nbrs + queue

    return False

#Fonctions sur les triangles

def in_triangle(G, node):
    """
    Return whether a given node is present in a triangle relationship.
    """
    for nbr1, nbr2 in combinations(G.neighbors(node), 2):
        if G.has_edge(nbr1, nbr2):
            return True
    return False


def get_triangle_neighbors(G, node) -> set:
    """
    Return neighbors involved in triangle relationship with node.
    """
    neighbors1 = set(G.neighbors(node))
    neighbors1.remove(node)
    triangle_nodes = set()
    for nbr1, nbr2 in combinations(neighbors1, 2):
        if G.has_edge(nbr1, nbr2):
            triangle_nodes.add(nbr1)
            triangle_nodes.add(nbr2)
    return triangle_nodes


def plot_triangle_relations(G, node):
    """
    Plot all triangle relationships for a given node.
    """
    triangle_nbrs = get_triangle_neighbors(G, node)
    triangle_nbrs.add(node)
    g = G.subgraph(triangle_nbrs)
    t = network.Network(height="200px",
                    width="100%",
                    heading = 'Triangles around ' + str(node), notebook = True)
    t.from_nx(g)

    t.set_options("""
    options =
        {
    "nodes": {
        "color": {
        "highlight": {
            "border": "rgba(0,0,0,1)",
            "background": "rgba(90,255,84,1)"
        }
        }
    },
    "edges": {
        "arrows": {
        "to": {
            "enabled": false
        },
        "from": {
            "enabled": false
        }
        },
        "color": {
        "inherit": true
        },
        "smooth": false
    },
    "physics": {
        "minVelocity": 0.75

    }
    }
        """)

    return t.show('triangle.html')

