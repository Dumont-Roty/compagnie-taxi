# je crée la ville comme on a crée le réseau RATP dans le projet RATP.

from compagnie_taxi.reseau_taxi import Emplacement
from typing import List, Tuple

#ListeEmplacement : List[Emplacement.numero] = [] # 1 emplacement est 1 point d'arret du taxi
ListeEmplacement : List[int] = [] # 1 emplacement est 1 point d'arret du taxi

# Test si ListeRoutes prends comme source la class Emplacement (en enlevant la duree)

ListeRoutes : List[Tuple[int, int]] = []

#ListeRoutes : List[(Tuple[Reseau.emplacement, Reseau.emplacement], int)] = [] # Les routes sont ce qui relie 2 emplacement (Tuple) et ça en un temps variable

def defListEmplacement() -> None:
    """
    Fonction qui permet de définir la liste des emplacements
    """
    
    emplacements = [Emplacement(i) for i in range(1, 17)] # les empalcements vont de 1 à 16 => range(1,17)
    for point in emplacements : # Pour chaque points, on les mets dans la liste des emplacements
        ListeEmplacement.append(point)
        
def defListeRoutes() -> None : 
    """
    Fonction qui va nous permettre de définir la liste des routes qui connectent les emplacements. Chaque emplacements n'a pas forcément de routes qui le relie à son voisin (de numéro).
    On va en profiter pour ajouter le temps de trajet entre les points.
    """
    voisinages = [
    (1, 2), (1, 3), (1, 4),
    (2, 5), (2, 6),
    (3, 4), (3, 6),
    (4, 7),
    (5, 8), (5, 9), (5, 10),
    (6, 7), (6, 10), (6, 11),
    (7, 11), (7, 15),
    (8, 12),
    (9, 8), (9, 13),
    (10, 9), (10, 13), (10, 14),
    (11, 14),
    (12, 16),
    (13, 12), (13, 14),
    (14, 16),
    (15, 14), (15, 16)
    ]
    
    # voisinages = [
    #     (1, 2, 5), (1, 3, 9), (1, 4, 4),
    #     (2, 5, 3), (2, 6, 2),
    #     (3, 4, 4), (3, 6, 1),
    #     (4, 7, 7),
    #     (5, 8, 4), (5, 9, 2), (5, 10, 9),
    #     (6, 7, 3), (6, 10, 9), (6, 11, 6),
    #     (7, 11, 8), (7, 15, 5),
    #     (8, 12, 5),
    #     (9, 8, 3), (9, 13, 10),
    #     (10, 9, 6), (10, 13, 5), (10, 14, 1),
    #     (11, 14, 2),
    #     (12, 16, 9),
    #     (13, 12, 4), (13, 14, 3),
    #     (14, 16, 4),
    #     (15, 14, 4), (15, 16, 3)
    # ]
    
    # Ajout des voisins en fonction de la liste voisinages
    for x, y in voisinages:
        ListeEmplacement[x-1].voisins.append(ListeEmplacement[y-1])
        ListeEmplacement[y-1].voisins.append(ListeEmplacement[x-1])

    # Ajout des routes
    for index, emplacement in enumerate(ListeEmplacement):
        for voisin in emplacement.voisins:
            if emplacement.EstVoisin(voisin):
                ListeRoutes.append((emplacement, voisin))


def init_ville(G):
    defListEmplacement()
    defListeRoutes()

    G.add_nodes_from(ListeEmplacement)
    G.add_edges_from([(e1.numero, e2.numero) for e1, e2, _ in ListeRoutes])