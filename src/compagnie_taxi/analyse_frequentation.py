from typing import Dict, Tuple, List
from src.compagnie_taxi.ville import ListeEmplacement, ListeRoutes, defListEmplacement, defListeRoutes, initialiser_voisins
from src.compagnie_taxi.reseau_taxi import Emplacement
import streamlit as st

class AnalyseFrequentation:
    def __init__(self, fluctuations: Dict[Tuple[int, int], float] = None, etats_emplacements: Dict[int, str] = None):
        self.fluctuations = fluctuations if fluctuations else {}
        self.etats_emplacements = etats_emplacements if etats_emplacements else {}

    def calculer_tous_trajets(self):
        defListEmplacement()
        defListeRoutes()
        initialiser_voisins()
        self._appliquer_etats()
        trajets = {}
        for depart in ListeEmplacement:
            for arrivee in ListeEmplacement:
                if depart != arrivee:
                    chemin, distance = depart.TrajetOpti(
                        arrivee, ListeRoutes, fluctuations=self.fluctuations, fluctuation=bool(self.fluctuations)
                    )
                    distance += sum(1 for e in chemin if getattr(e, "etat", "normal") == "travaux")
                    trajets[(depart.numero, arrivee.numero)] = (chemin, distance)
        return trajets

    def frequentation_emplacements(self, trajets):
        emp_freq = {e.numero: 0 for e in ListeEmplacement}
        for (depart, arrivee), (chemin, distance) in trajets.items():
            for emp in chemin:
                emp_freq[emp.numero] += 1
        return emp_freq

    def _appliquer_etats(self):
        for e in ListeEmplacement:
            e.etat = self.etats_emplacements.get(e.numero, "normal")

    def top_emplacements(self, emp_freq, n=3):
        return sorted(emp_freq.items(), key=lambda x: x[1], reverse=True)[:n]

@st.cache_data
def get_frequentation(fluctuations, etats):
    analyseur = AnalyseFrequentation(fluctuations=fluctuations, etats_emplacements=etats)
    trajets = analyseur.calculer_tous_trajets()
    emp_freq = analyseur.frequentation_emplacements(trajets)
    top3 = analyseur.top_emplacements(emp_freq, n=3)
    return emp_freq, top3