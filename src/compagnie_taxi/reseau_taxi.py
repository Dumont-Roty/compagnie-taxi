from typing import Tuple, List
from graphlib import *
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
    def __init__(self, numero : int, *destination : int):
        self.numero : int = numero # numéro = emplacement de la ville
        self.voisins : list = [] # liste des voisins de l'emplacement
        # Dans le principe des gares, on différencie les lignes des voisins mais pas ici car on prends la route.
        self.destination = destination
        
    def __str__(self):
        return str(self.numero)
    
    def __eq__(self, other):
        return self.numero == other.numero # Equivalence de self est self 
    
    def __neq__(self, other):
        return self.numero != other.numero # Non équivalence de self n'est pas self
    
    def __hash__(self):
        return hash(str(self.numero)) # Hash de l'emplacement, nécessaire pour le graphe et doit etre unique 
    
    def __lt__(self, other):
        return self.numero < other.numero
    
    def EstVoisin(self, other):
        """Retourne True si 'autre' est un voisin de self."""
        return any(voisin.numero == other.numero for voisin in self.voisins)

    def CalculerTrajetVoisins(self, other, destination):
        """
        Calculer le temps de trajet entre 2 emplacements.
        On fixe le trajet à 1 pour le graph
        """
        if not self.EstVoisin(other):
            raise ValueError(f"Il n'y a pas de routes qui relie l'emplacement : {other} de l'emplacement {self}")
        if ( other.numero == destination.numero):
            return 1
        EmplacementActuelle = []
        EmplacementsVisites = []
        for emp2 in other.Route:
            for emp1 in self.Route:
                if ( emp1 == emp2 ):
                    EmplacementActuelle.append(emp1)
                    
            for emp3 in self.Route:
                if ( emp3 == emp2 ):
                    EmplacementsVisites.append(emp3)
                    
        for emp in EmplacementsVisites:
            if emp in EmplacementActuelle:
                return 1
        return 30
    
   
    def TrajetOpti(self, destination, ListeRoutes, fluctuations = None, fluctuation: bool = False):
        """
        Calcule le chemin optimal (plus court) entre self et destination en utilisant un algorithme de type Dijkstra.
        fluctuations : dict optionnel, clé=(e1, e2), valeur=coefficient multiplicateur
        """
        # Création d'un dictionnaire pour retrouver la durée entre deux emplacements
        durees = {}
        for e1, e2, duree in ListeRoutes:
            coef = 1.0
            if fluctuations and fluctuation:
                key = (e1.numero, e2.numero)
                key_inv = (e2.numero, e1.numero)
                if key in fluctuations:
                    coef = fluctuations[key]
                elif key_inv in fluctuations:
                    coef = fluctuations[key_inv]
            durees[(e1, e2)] = int(duree * coef)
                    
        # Initialisation
        parcourus = set()
        valeur_dict = {self: 0}
        previous = {self: None}
        a_explorer = [self]

        while a_explorer:
            # On prend le noeud avec la plus petite valeur actuelle
            courant = min(a_explorer, key=lambda x: valeur_dict.get(x, float('inf')))
            a_explorer.remove(courant)
            parcourus.add(courant)

            if courant == destination:
                break

            for voisin in courant.voisins:
                if voisin in parcourus:
                    continue
                cout = valeur_dict[courant] + durees.get((courant, voisin), float('inf'))
                if cout < valeur_dict.get(voisin, float('inf')):
                    valeur_dict[voisin] = cout
                    previous[voisin] = courant
                    if voisin not in a_explorer:
                        a_explorer.append(voisin)

        # Reconstruction du chemin
        chemin = []
        curr = destination
        if curr not in valeur_dict:
            return [], float('inf')  # Pas de chemin trouvé
        while curr is not None:
            chemin.append(curr)
            curr = previous.get(curr)
        chemin.reverse()
        return chemin, valeur_dict[destination]
            
            
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

@dataclass( frozen = True, unsafe_hash=True )
class Route:
    emplacement : List[Emplacement]
    numero : str
