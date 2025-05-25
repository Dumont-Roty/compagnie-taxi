from compagnie_taxi.reseau_taxi import *
import compagnie_taxi.ville as ville
import matplotlib.pyplot as plt
import networkx as nx



def AfficherCarte():
    ville.defListEmplacement()
    ville.defListeRoutes()
    
    G = nx.Graph()
    
    #G.add_nodes_from(ville.ListeEmplacement)
    # Pas besoin de faire ca, on peut directement ajouter les routes car les emplacements sont déjà ajoutés dans la liste des routes

    G.add_edges_from([(e1.numero, e2.numero, {'duree': duree}) for e1, e2, duree in ville.ListeRoutes])

    #Pour afficher les poids sur les arêtes :
    pos = nx.spring_layout(G)
    nx.draw(G, pos, with_labels=True)
    edge_labels = nx.get_edge_attributes(G, 'duree')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)

    plt.show()
    
def CalculTrajet():
    print("Séléctionnez un point de départ (1-16) : ")
    depart = ville.ListeEmplacement[int(input()) - 1]
    print("Séléctionnez un point d'arrivée (1-16) : ")
    destination = ville.ListeEmplacement[int(input()) - 1]
    chemin, distance = depart.TrajetOpti(destination, ville.ListeRoutes)
    print("Chemin optimal :", [e.numero for e in chemin], "Distance :", distance)

if __name__ == "__main__":
    ville.defListEmplacement()
    ville.defListeRoutes()
    # Initialisation des voisins pour chaque Emplacement
    for e1, e2, duree in ville.ListeRoutes:
        if e2 not in e1.voisins:
            e1.voisins.append(e2)
        if e1 not in e2.voisins:
            e2.voisins.append(e1)
    CalculTrajet()
    AfficherCarte()
