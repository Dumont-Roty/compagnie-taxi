from compagnie_taxi.reseau_taxi import *
import compagnie_taxi.ville as ville
import matplotlib.pyplot as plt
import networkx as nx

def afficher_carte(ville, fluctuations, depart=None, destination=None, chemin=None, pos_fixe=None, ax=None):
    """
    Affiche la carte du réseau avec les fluctuations et le chemin optimal si fourni.
    Retourne la figure matplotlib (pour Streamlit ou affichage direct).
    """
    G = nx.Graph()
    for e1, e2, duree in ville.ListeRoutes:
        coef = 1.0
        key = (e1.numero, e2.numero)
        key_inv = (e2.numero, e1.numero)
        if key in fluctuations:
            coef = fluctuations[key]
        elif key_inv in fluctuations:
            coef = fluctuations[key_inv]
        duree_mod = int(duree * coef)
        G.add_edge(e1.numero, e2.numero, duree=duree_mod)

    if ax is None:
        fig, ax = plt.subplots()
    node_colors = []
    for n in G.nodes():
        if depart and n == depart.numero:
            node_colors.append('green')
        elif destination and n == destination.numero:
            node_colors.append('red')
        elif chemin and n in [e.numero for e in chemin]:
            node_colors.append('orange')
        else:
            node_colors.append('skyblue')
    nx.draw(G, pos_fixe, with_labels=True, ax=ax, node_color=node_colors)
    edge_labels = nx.get_edge_attributes(G, 'duree')
    nx.draw_networkx_edge_labels(G, pos_fixe, edge_labels=edge_labels, ax=ax)
    return ax.figure

def AfficherCarte():
    ville.defListEmplacement()
    ville.defListeRoutes()
    fluctuations = {
        (9, 13): 1,   # Ralentissement
    }
    G = nx.Graph()
    edges = []
    for e1, e2, duree in ville.ListeRoutes:
        coef = 1.0
        key = (e1.numero, e2.numero)
        key_inv = (e2.numero, e1.numero)
        if key in fluctuations:
            coef = fluctuations[key]
        elif key_inv in fluctuations:
            coef = fluctuations[key_inv]
        duree_mod = int(duree * coef)
        edges.append((e1.numero, e2.numero, {'duree': duree_mod}))
    G.add_edges_from(edges)

    pos = nx.spring_layout(G, weight='duree')
    nx.draw(G, pos, with_labels=True)
    edge_labels = nx.get_edge_attributes(G, 'duree')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)
    plt.show()
    
def CalculTrajet():
    while True:
        try:
            depart_str = input("Séléctionnez un point de départ (1-16) : ")
            if not depart_str.isdigit():
                raise ValueError("Le numéro de l'emplacement renseigné n'est pas valide")
            depart = int(depart_str)
            if depart < 1 or depart > 16:
                raise ValueError("Veuillez renseigner un emplacement entre 1 et 16")
            depart = ville.ListeEmplacement[depart - 1]
            
            destination_str = input("Séléctionnez un point d'arrivée (1-16) : ")
            if not destination_str.isdigit():
                raise ValueError("Veuillez renseigner un emplacement entre 1 et 16")
            destination = int(destination_str)
            if destination < 1 or destination > 16:
                raise ValueError("Le numéro de l'emplacement renseigné n'est pas valide")  
            destination = ville.ListeEmplacement[destination - 1]
                
            if destination == depart:
                raise ValueError("Veuillez rensigner un autre emplacement que l'emplacement de départ")
            fluctuations = {
            (9, 13): 1,   # Ralentissement
            }
            chemin, distance = depart.TrajetOpti(destination, ville.ListeRoutes, fluctuations = fluctuations, fluctuation=True)
            print("Chemin optimal :", [e.numero for e in chemin], "Distance :", distance)
            return True
        except ValueError as e:
            print("Erreur :", e)
            return False

if __name__ == "__main__":
    ville.defListEmplacement()
    ville.defListeRoutes()
    # Initialisation des voisins pour chaque Emplacement
    for e1, e2, duree in ville.ListeRoutes:
        if e2 not in e1.voisins:
            e1.voisins.append(e2)
        if e1 not in e2.voisins:
            e2.voisins.append(e1)
    if CalculTrajet():
        AfficherCarte()
