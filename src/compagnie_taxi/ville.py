"""Module de gestion de la ville, des emplacements et des routes pour la compagnie de taxi."""

# je crée la ville comme on a crée le réseau RATP dans le projet RATP.
from compagnie_taxi.reseau_taxi import Emplacement
from typing import List, Tuple

ListeEmplacement: List[Emplacement] = []  # 1 emplacement est 1 point d'arret du taxi
ListeRoutes: List[Tuple[Emplacement, Emplacement, int]] = []


def defListEmplacement() -> None:
    """
    Initialise la liste globale des emplacements de la ville.

    Cette fonction crée et ajoute tous les objets Emplacement représentant les arrêts de taxi dans la ville.
    Elle doit être appelée avant toute opération sur les emplacements.
    """

    ListeEmplacement.clear()
    emplacements = [
        Emplacement(i) for i in range(1, 17)
    ]  # les empalcements vont de 1 à 16 => range(1,17)
    for (
        point
    ) in emplacements:  # Pour chaque points, on les mets dans la liste des emplacements
        ListeEmplacement.append(point)


def defListeRoutes() -> None:
    """
    Initialise la liste globale des routes reliant les emplacements.

    Cette fonction crée et ajoute tous les tuples (Emplacement, Emplacement, durée) représentant les routes de la ville.
    Elle doit être appelée après defListEmplacement().
    """

    ListeRoutes.clear()
    # Remplace la liste voisinages par celle avec les durées :
    voisinages = [
        (1, 2, 5),
        (1, 3, 9),
        (1, 4, 4),
        (2, 5, 3),
        (2, 6, 2),
        (3, 4, 4),
        (3, 6, 1),
        (4, 7, 7),
        (5, 8, 4),
        (5, 9, 2),
        (5, 10, 9),
        (6, 7, 3),
        (6, 10, 9),
        (6, 11, 6),
        (7, 11, 8),
        (7, 15, 5),
        (8, 12, 5),
        (9, 8, 3),
        (9, 13, 10),
        (10, 9, 6),
        (10, 13, 5),
        (10, 14, 1),
        (11, 14, 2),
        (12, 16, 9),
        (13, 12, 4),
        (13, 14, 3),
        (14, 16, 4),
        (15, 14, 4),
        (15, 16, 3),
    ]

    # Ajout des voisins en fonction de la liste voisinages
    for e1, e2, duree in voisinages:
        ListeRoutes.append((ListeEmplacement[e1 - 1], ListeEmplacement[e2 - 1], duree))
        ListeRoutes.append((ListeEmplacement[e2 - 1], ListeEmplacement[e1 - 1], duree))


def initialiser_voisins() -> None:
    """
    Met à jour les voisins de chaque emplacement.

    Pour chaque route, ajoute les emplacements connectés comme voisins respectifs.
    À appeler après l'initialisation des emplacements et des routes.
    """
    for e in ListeEmplacement:
        e.voisins.clear()
    for e1, e2, duree in ListeRoutes:
        if e2 not in e1.voisins:
            e1.voisins.append(e2)
        if e1 not in e2.voisins:
            e2.voisins.append(e1)
