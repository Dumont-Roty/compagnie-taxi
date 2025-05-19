from typing import List
from compagnie_taxi.reseau import *
import matplotlib.pyplot as plt
import networkx as nx

ListeEmplacement = [emplacement(i, False) for i in range(1, 17)]

# Création des voisins (à adapter si déjà fait dans reseau.py)
voisinages = [
    (1, 2, 5), (1, 3, 9), (1, 4, 4),
    (2, 5, 3), (2, 6, 2),
    (3, 4, 4), (3, 6, 1),
    (4, 7, 7),
    (5, 8, 4), (5, 9, 2), (5, 10, 9),
    (6, 7, 3), (6, 10, 9), (6, 11, 6),
    (7, 11, 8), (7, 15, 5),
    (8, 12, 5),
    (9, 8, 3), (9, 13, 10),
    (10, 9, 6), (10, 13, 5), (10, 14, 1),
    (11, 14, 2),
    (12, 16, 9),
    (13, 12, 4), (13, 14, 3),
    (14, 16, 4),
    (15, 14, 4), (15, 16, 3)
]
for x, y, duree in voisinages:
    ListeEmplacement[x-1].voisins.append((ListeEmplacement[y-1], duree))
    ListeEmplacement[y-1].voisins.append((ListeEmplacement[x-1], duree))

G = nx.Graph()
G.add_nodes_from(ListeEmplacement)

# Ajout des arêtes (routes)
ListeRoutes = []
for index, Emplacement in enumerate(ListeEmplacement):
    for Voisin in ListeEmplacement[(index + 1):]:
        if Emplacement.EstVoisin(Voisin):
            ListeRoutes.append((Emplacement, Voisin))
G.add_edges_from(ListeRoutes)


#On dessine le graphe
nx.draw(G, )

plt.show()