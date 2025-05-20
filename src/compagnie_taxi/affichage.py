from typing import List
from compagnie_taxi.reseau import *
import compagnie_taxi.ville as ville
import matplotlib.pyplot as plt
import networkx as nx


def AfficherCarte():
    G = nx.Graph()
    
    G.add_nodes_from(ville.defListEmplacement)

    G.add_edges_from(ville.defListeRoutes)

    #On dessine le graphe
    nx.draw(G, with_labels=True)

    plt.show()