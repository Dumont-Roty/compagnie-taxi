from typing import List
from compagnie_taxi.reseau_taxi import *
import compagnie_taxi.ville as ville
import matplotlib.pyplot as plt
import networkx as nx


def AfficherCarte():
    ville.defListEmplacement()
    ville.defListeRoutes()
    
    G = nx.Graph()
    
    G.add_nodes_from(ville.ListeEmplacement)

    G.add_edges_from([(e1.numero, e2.numero, {'weight': duree}) for e1, e2, duree in ville.ListeRoutes])

    #On dessine le graphe
    nx.draw(G, with_labels=True)
    
    edge_labels = nx.get_edge_attributes(G, 'weight')
    nx.draw_networkx_edge_labels(G, pos=nx.spring_layout(G), edge_labels=edge_labels)

    plt.show()