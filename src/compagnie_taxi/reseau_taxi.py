from typing import Tuple, List
from graphlib import *
from compagnie_taxi.ville import *
from dataclasses import dataclass


"""
Je définie chaque éléments de la problématique :
    - emplacement (point d'interet dans la ville)
        Point de base de l'exercice, c'est la liste de produit qui peut etre contenu dans notre recette. Tous les emplacements ne sont pas forcément bon à prendre mais il est necessaire d'en avoir.
        On va définir les points avec leurs voisins.
        EST CE QUE LES RALENTISSEMENTS SERONT DANS LES EMPLACEMENTS (je pense pas car ca ne change pas la relation entre les 2)
    - client (c'est le point d'arrivé et le point de départ mais n'indique pas les démarches à suivre)
        Il représente le début et la fin de la recette. je sais pas si faut le définir mais c'est aussi un questionnement future pour la problématique. (ajout du taxi plus tard ?)
    - Trajet (point A --> point B ==> OPTIMISATION)
        C'est la recette, or elle dépend du client et de sa destination (peut etre inutile je sais pas encore --> Trajet dans client peut etre ?)
    - reseau (Tout ce qui compose le reseau de la ville)
    - lignes (connexion entre les emplacements --> Chaque points et chaque durée ?)
"""


class Emplacement(object):  
    def __init__(self, numero : int, ralentissement : bool):
        self.numero : int = numero # numéro = emplacement de la ville
        self.voisins : list = [] # liste des voisins de l'emplacement
        
    def __str__(self):
        return str(self.numero)
    
    def __eq__(self, other):
        return self.numero == other.numero # Equivalence de self est self 
    
    def __neq__(self, other):
        return self.numero != other.numero # Non équivalence de self n'est pas self
    
    def __hash__(self):
        return hash(str(self.numero)) # Hash de l'emplacement, nécessaire pour le graphe et doit etre unique 
    
    def EstVoisin(self, other):
        """Retourne True si 'autre' est un voisin de self."""
        return any(voisin.numero == other.numero for voisin, _ in self.voisins)

    def __repr__(self):
        return f"Emplacement(numero={self.numero}, voisins={[v.numero for v in self.voisins]})"
    
    
# class Client(object):
#     """
#     Client de la compagnie de taxi
#     """
#     def __init__(self, id : int, pointDEP : Emplacement, pointARR : Emplacement):
#         self.id : int = id
#         self.depart : Emplacement = pointDEP
#         self.arrive : Emplacement = pointARR

class Route(object):
    """
    La Route est la liaisons des 2 emplacements. Ce sont des voisins
    """
    def __init__(self, emplacement1 : Emplacement, emplacement2 : Emplacement): #, durée : int):
        self.emplacement1 : Emplacement = emplacement1
        self.emplacement2 : Emplacement = emplacement2
        # self.temps : int = durée
    
    def __repr__(self):
        return f"Route(emplacement1={self.emplacement1.numero}, emplacement2={self.emplacement2.numero})"

class Reseau(object): # Reseau ouy trajet de la compagnie ?
    """
    Indique tout le réseau de transport de la compagnie
    """
    def __init__(self): # Pas sur pour le ralentissement --> bool d'un emplacement ?
        self.ListeEmplacement : List[Emplacement] = []
        self.ListeRoutes : List[Tuple[Emplacement, Emplacement]] = []
    
    def ajouter_emplacement(self, emplacement : int):
        self.ListeEmplacement.append(emplacement)
    
    def ajouter_routes(self, routes : Tuple[Emplacement,Emplacement]):
        self.ListeRoutes.append(routes)
    
    def initialiser_voisins(self):
        for emplacement in self.ListeEmplacement:
            emplacement.voisins = []
    
    def __eq__(self, other): # Equivalence entre le réseau
        if self.numero == other.numero and self.tempstrajet == other.tempstrajet:
            return True
        return False
    
    
# Est ce que on doit définir les voisins comme un objet ? Information immuable ?

# def EstVoisin(a, b):

