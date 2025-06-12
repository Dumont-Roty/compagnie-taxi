from typing import Tuple, List, Dict, Optional

"""
Je définis chaque élément de la problématique :
    - emplacement (point d'intérêt dans la ville)
    - client (c'est le point d'arrivée et le point de départ)
    - Trajet (point A --> point B ==> OPTIMISATION)
    - reseau (Tout ce qui compose le réseau de la ville)
    - lignes (connexion entre les emplacements --> Chaque point et chaque durée ?)
"""

class Emplacement:
    """
    Représente un point d'arrêt de taxi dans la ville.

    Attributs :
        numero (int) : Identifiant unique de l'emplacement.
        voisins (List[Emplacement]) : Liste des emplacements voisins.
        etat (str) : État de l'emplacement ('normal', 'travaux', etc.).
    """

    def __init__(self, numero: int):
        """
        Initialise un nouvel emplacement.

        Args:
            numero (int): Identifiant unique de l'emplacement.
        """
        self.numero : int = numero
        self.voisins : List['Emplacement'] = []
        self.etat: str = "normal"  # Ajout de l'attribut etat

    def __str__(self):
        return str(self.numero)
    
    def __eq__(self, other):
        return isinstance(other, Emplacement) and self.numero == other.numero
    
    def __ne__(self, other):
        return not self.__eq__(other)
    
    def __hash__(self):
        return hash(self.numero)
    
    def __lt__(self, other):
        return self.numero < other.numero
    
    def EstVoisin(self, autre: "Emplacement") -> bool:
        """
        Vérifie si un autre emplacement est voisin de celui-ci.

        Args:
            autre (Emplacement): L'emplacement à tester.

        Returns:
            bool: True si 'autre' est un voisin, False sinon.
        """
        return any(voisin.numero == autre.numero for voisin in self.voisins)

    def TrajetOpti(
        self,
        destination: 'Emplacement',
        ListeRoutes: List[Tuple['Emplacement', 'Emplacement', int]],
        fluctuations: Optional[Dict[Tuple[int, int], float]] = None,
        fluctuation: bool = False
    ):
        """
        Calcule le trajet optimal vers une destination.

        Args:
            destination (Emplacement): Emplacement d'arrivée.
            ListeRoutes (List[Tuple[Emplacement, Emplacement, int]]): Liste des routes disponibles.
            fluctuations (dict, optional): Dictionnaire des ralentissements sur certaines routes.
            fluctuation (bool, optional): Active la prise en compte des fluctuations.

        Returns:
            Tuple[List[Emplacement], int]: Chemin optimal et distance totale.
        """
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
                    
        parcourus = set()
        valeur_dict: Dict[Emplacement, float] = {self: 0}
        previous: Dict[Emplacement, Optional[Emplacement]] = {self: None}
        a_explorer: List[Emplacement] = [self]

        while a_explorer:
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

        chemin = []
        curr = destination
        if curr not in valeur_dict:
            return [], float('inf')
        while curr is not None:
            chemin.append(curr)
            curr = previous.get(curr)
        chemin.reverse()
        return chemin, valeur_dict[destination]
            
    def __repr__(self):
        return f"Emplacement(numero={self.numero}, voisins={[v.numero for v in self.voisins]})"

class Reseau(object):
    """
    Indique tout le réseau de transport de la compagnie.
    """

    def __init__(self):
        """
        Initialise un nouveau réseau de transport.
        """
        self.ListeEmplacement : List[Emplacement] = []
        self.ListeRoutes : List[Tuple[Emplacement, Emplacement, int]] = []
    
    def ajouter_emplacement(self, emplacement : 'Emplacement'):
        """
        Ajoute un nouvel emplacement au réseau.

        Args:
            emplacement (Emplacement): L'emplacement à ajouter.
        """
        self.ListeEmplacement.append(emplacement)
    
    def ajouter_routes(self, route : Tuple['Emplacement', 'Emplacement', int]):
        """
        Ajoute une nouvelle route au réseau.

        Args:
            route (Tuple[Emplacement, Emplacement, int]): La route à ajouter.
        """
        self.ListeRoutes.append(route)
    
    def initialiser_voisins(self):
        """
        Met à jour les voisins de chaque emplacement du réseau.
        """
        for emplacement in self.ListeEmplacement:
            emplacement.voisins.clear()
        for e1, e2, duree in self.ListeRoutes:
            if e2 not in e1.voisins:
                e1.voisins.append(e2)
            if e1 not in e2.voisins:
                e2.voisins.append(e1)

    def __eq__(self, other):
        if not isinstance(other, Reseau):
            return False
        return self.ListeEmplacement == other.ListeEmplacement and self.ListeRoutes == other.ListeRoutes
