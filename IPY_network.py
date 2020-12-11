# -*- coding: utf-8 -*-
# ---
# jupyter:
#   jupytext:
#     formats: ipynb,py:light
#     text_representation:
#       extension: .py
#       format_name: light
#       format_version: '1.5'
#       jupytext_version: 1.7.1
#   kernelspec:
#     display_name: Python 3
#     language: python
#     name: python3
# ---

# # Création d'un réseau sur Ipycytoscape

# # I- Initialisation

# ## 1) Importation des packages nécessaires

import networkx as nx
import matplotlib.pyplot as plt
import pandas as pd
from ipycytoscape import *
from fonctions import *
from ipywidgets import Output
from IPython.display import display
from pprint import pformat

# ## 2) Importation des données

# Les données sont stockées sous forme d'une liste de connexions dans un fichier .csv. Lors de l'importation, elle sont transférées dans un tableau de format 'panda'.

# +
edges = pd.read_csv('mini_multi_omi.csv')

#print(edges)

# ## 3) Création du réseau

# Le réseau en lui-même est créé grâce au package NetworkX. L'information sur le nombre de vérifications expérimentales (de la colonne 'ExpEvidences' du fichier .csv) est récupérée comme un attribut des connexions.

# +
G = nx.from_pandas_edgelist(
    edges,
    source="Name_A",
    target="Name_B",
    edge_attr=["ExpEvidences","EdgeType"],
    #create_using=nx.Graph()
    )


for s, t, data in G.edges(data=True):
    if G[s][t]['EdgeType'] == 'GPI':
        G[s][t]['classes'] = 'directed'
# -

for i in G.nodes :
    if i[:4] == 'gene' :
        G.nodes[i]['classes'] = 'class1'
    else :
        G.nodes[i]['classes'] = 'class2'

# # II- Représentation graphique 2D

# +
g = CytoscapeWidget()
g.graph.add_graph_from_networkx(G)
    
g.set_style([
                        {
                            'selector': 'node.class1',
                            'style':{
                                'background-color': 'red',
                                'font-family': 'arial',
                                'font-size': '20px',
                                'label': 'data(id)',
                                'color': 'blue',
                                'text-valign': 'bottom',
                                'text-halign': 'center'
                            }
                        },
                        {
                            'selector': 'node.class2',
                            'style':{
                                'background-color': 'blue',
                                'font-family': 'helvetica',
                                'font-size': '20px',
                                'label': 'data(id)',
                                'color': 'green',
                                'text-valign': 'bottom',
                                'text-halign': 'center'
                            }
                        }])


out = Output()

def log_clicks(node):
    with out:
        print(node['data']['id'])
        out.clear_output(wait = True)

def log_mouseovers(node):
    with out:
        print(f'mouseover: {pformat(node)}')
        out.clear_output(wait = True)

g.on('node', 'click', log_clicks)
g.on('node', 'mouseover', log_mouseovers)

display(g)
display(out)


# -


# # III- Exploration

# ## 1) Paramètres généraux

# NetworkX permet de récupérer facilement un certain nombre d'informations : le nombre de connexions, le nombre de noeuds ou encore le degré ou les voisins de chaque noeud.

# +
print('nombre de noeuds :',G.number_of_nodes())
#print(G.nodes(data = True))

print('nombre de connexions :',G.number_of_edges(),'\n')
#print(G.edges(data = True))

#Liste des degrés.
G.degree()

#Liste des noms des voisins d'un certain noeud.
print('voisins du noeud CDKI_CANAL :','\n',list(G.neighbors('CDK1_CANAL')),'\n')

#Liste des 'betweenness centrality'
#pd.Series(nx.betweenness_centrality(G))
# -

# Il est plus clair de représenter le degré sont forme de graphiques.

# +
centralities = pd.Series(nx.degree_centrality(G))
centralities.sort_values(ascending=False)
#print(centralities)

plt.figure(figsize=(12, 3))
plt.subplot(1, 2, 1)
plot_degree(G)
plt.subplot(1, 2, 2)
plot_degree_centrality(G)
# -

# ## 2) Chemin le plus court

# NetworkX permet également de sélectionner la liste des noeuds pour aller d'un noeud A à un noeud B. Il est aussi possible de simplement vérifier si un chemin existe ou non.

# +
print(nx.shortest_path(G, 'CDK1_CANAL', 'Q5ADN1_CANAL'))

print(path_exists('CDK1_CANAL', 'Q5ADN1_CANAL', G))
# -

# ## 3) Structures secondaires

# Les triangles sont les cliques les plus simples qui existent.

# +
#Cherche si un noeud donné fait parti ou non d'un triangle.
in_triangle(G, 'CDC11_CANAL')

get_triangle_neighbors(G, 'CDC11_CANAL')

#plot_triangle_relations(G, 'CDC11_CANAL')
