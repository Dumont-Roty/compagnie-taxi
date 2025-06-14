from typing import Dict, Tuple, Optional
from compagnie_taxi.ville import (
    ListeEmplacement,
    ListeRoutes,
    defListEmplacement,
    defListeRoutes,
    initialiser_voisins,
)
import streamlit as st


class AnalyseFrequentation:
    """
    Permet d'analyser la fréquentation des emplacements du réseau de taxis.

    Attributs :
        fluctuations (dict): Ralentissements appliqués sur certaines routes.
        etats_emplacements (dict): États particuliers des emplacements.
    """

    def __init__(
        self,
        fluctuations: Optional[Dict[Tuple[int, int], float]] = None,
        etats_emplacements: Optional[Dict[int, str]] = None,
    ):
        """
        Initialise l'analyseur de fréquentation.

        Args:
            fluctuations (dict, optional): Ralentissements sur certaines routes.
            etats_emplacements (dict, optional): États des emplacements.
        """
        self.fluctuations = fluctuations if fluctuations else {}
        self.etats_emplacements = etats_emplacements if etats_emplacements else {}

    def calculer_tous_trajets(self):
        """
        Calcule tous les trajets optimaux entre chaque paire d'emplacements.

        Returns:
            dict: Dictionnaire {(départ, arrivée): (chemin, distance)}
        """
        defListEmplacement()
        defListeRoutes()
        initialiser_voisins()
        self._appliquer_etats()
        trajets = {}
        for depart in ListeEmplacement:
            for arrivee in ListeEmplacement:
                if depart != arrivee:
                    chemin, distance = depart.TrajetOpti(
                        arrivee,
                        ListeRoutes,
                        fluctuations=self.fluctuations,
                        fluctuation=bool(self.fluctuations),
                    )
                    distance += sum(
                        1 for e in chemin if getattr(e, "etat", "normal") == "travaux"
                    )
                    trajets[(depart.numero, arrivee.numero)] = (chemin, distance)
        return trajets

    def frequentation_emplacements(self, trajets):
        """
        Calcule la fréquentation de chaque emplacement à partir des trajets.

        Args:
            trajets (dict): Dictionnaire des trajets calculés.

        Returns:
            dict: Dictionnaire {numero_emplacement: fréquentation}
        """
        emp_freq = {e.numero: 0 for e in ListeEmplacement}
        for (depart, arrivee), (chemin, distance) in trajets.items():
            for emp in chemin:
                emp_freq[emp.numero] += 1
        return emp_freq

    def _appliquer_etats(self):
        for e in ListeEmplacement:
            e.etat = self.etats_emplacements.get(e.numero, "normal")

    def top_emplacements(self, emp_freq, n=3):
        """
        Retourne les n emplacements les plus fréquentés.

        Args:
            emp_freq (dict): Dictionnaire des fréquentations.
            n (int): Nombre d'emplacements à retourner.

        Returns:
            list: Liste triée des n emplacements les plus fréquentés.
        """
        return sorted(emp_freq.items(), key=lambda x: x[1], reverse=True)[:n]


@st.cache_data
def get_frequentation(fluctuations, etats):
    analyseur = AnalyseFrequentation(
        fluctuations=fluctuations, etats_emplacements=etats
    )
    trajets = analyseur.calculer_tous_trajets()
    emp_freq = analyseur.frequentation_emplacements(trajets)
    top3 = analyseur.top_emplacements(emp_freq, n=3)
    return emp_freq, top3
