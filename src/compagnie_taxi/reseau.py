from typing import Tuple, List
from graphlib import *

"""
Je définie chaque éléments de la problématique :
    - emplacement (point d'interet dans la ville)
    - reseau (Tout ce qui compose le reseau de la ville)
    - lignes (connexion entre les emplacements --> Chaque points et chaque durée ?)
    - Trajet (point A --> point B ==> OPTIMISATION)
"""
class emplacement(object):
    def __init__(self, numero : int, ralentissement : bool):
        self.numero : int = numero # numéro = emplacement de la ville
        self.voisins : list = [] # liste des voisins de l'emplacement
        self.travaux : bool = ralentissement
        
    def __str__(self):
        return str(self.numero) # 
    
    def __eq__(self, other):
        return self.numero == other.numero # Equivalence de self est self 
    
    def __neq__(self, other):
        return self.numero != other.numero # Non équivalence de self n'est pas self
    
    def __hash__(self):
        return hash(str(self.numero)) # Hash de l'emplacement, nécessaire pour le graphe et doit etre unique 
    
    def EstVoisin(self, autre):
        """Retourne True si 'autre' est un voisin de self."""
        return any(voisin.numero == autre.numero for voisin, _ in self.voisins)

    @staticmethod
    def EstVoisinStatic(a, b) -> bool:
        """
        Fonction qui permet de savoir si deux emplacements sont voisins
        :param a: numéro du premier emplacement
        :param b: numéro du deuxième emplacement
        :return: True si les emplacements sont voisins, False sinon
        """
        emplacements = [None] + [emplacement(i, False) for i in range(1, 17)]
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
            emplacements[x].voisins.append((emplacements[y], duree))
            emplacements[y].voisins.append((emplacements[x], duree))

        # Vérifie si emplacements[a] est voisin de emplacements[b]
        est_voisin = any(voisin.numero == a for voisin, _ in emplacements[b].voisins)
        if est_voisin:
            #print(f"{a} et {b} sont voisins")
            return True
        else:
            #print(f"{a} et {b} ne sont pas voisins")
            return False
class reseau(object): # Reseau ouy trajet de la compagnie ?
    """
    Indique tout le réseau de transport de la compagnie
    """
    def __init__(self, emplacement : str, routes : str, duree : int, compagnie : int, ralentissment : bool=False): # Pas sur pour le ralentissement --> bool d'un emplacement ?
        self.numero : str = emplacement 
        self.connexion : str = routes
        self.tempstrajet : int = duree
        self.taxi : int = compagnie # Taxi de la compagnie dans la ville (int car plusieurs taxi ?)
        self.ralentissement : bool = ralentissment
        
    def __eq__(self, other): # Equivalence entre le réseau
        if self.numero == other.numero and self.tempstrajet == other.tempstrajet:
            return True
        return False
    
    
class trajet(object):
    """
    Je cherche à ce que le trajet relie 2 points
    """
    def __init__(self, départ : emplacement, arrivé : emplacement, durée : int):
        self.départ : emplacement = départ
        self.arrivé : emplacement = arrivé
    
    def __str__(self): # indique le temps de trajet 
        "Le temps de trajet entre le point " + self.départ + " et le point d'arrivé "+ self.arrivé+ " est de "
        T = "____durée___"
        return T

# Est ce que on doit définir les voisins comme un objet ? Information immuable ?

# def EstVoisin(a, b):

