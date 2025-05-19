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
    def __init__(self, numero:int, ralentissement : bool):
        self.numero : int = numero # numéro = emplacement de la ville
        self.voisins : List[emplacement] = [] # liste des voisins de l'emplacement
        self.travaux : bool = ralentissement
        
    def __str__(self):
        return "Numéro emplacement : " + self.numero # 
    
    def __eq__(self, other):
        return self.numero == other.numero # Equivalence de self est self 
    
    def __neq__(self, other):
        return self.numero != other.numero # Non équivalence de self n'est pas self
    
    def __hash__(self):
        return hash(self.numero) # Hash de l'emplacement, nécessaire pour le graphe et doit etre unique
        
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

        
    