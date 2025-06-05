import streamlit as st
import src.compagnie_taxi.ville as ville
from src.compagnie_taxi.affichage import afficher_carte
from src.compagnie_taxi.analyse_frequentation import get_frequentation
import networkx as nx

ville.defListEmplacement()
ville.defListeRoutes()
ville.initialiser_voisins()

G_base = nx.Graph()
for e1, e2, duree in ville.ListeRoutes:
    G_base.add_edge(e1.numero, e2.numero)
POS_FIXE = nx.spring_layout(G_base, seed=876)

def main():
    st.markdown("# 🚕 Compagnie Taxi")
    st.markdown("**Analyse de la fréquentation du réseau et aide à la décision pour le placement des taxis.**")
    st.markdown("---")

    emplacements = ville.ListeEmplacement
    options = {f"Emplacement {e.numero}": e for e in emplacements}

    # Sidebar
    with st.sidebar:
        st.title("Paramètres")
        depart_label = st.selectbox("🚦 Point de départ", list(options.keys()))
        destination_label = st.selectbox("🏁 Point d'arrivée", list(options.keys()))
        depart = options[depart_label]
        destination = options[destination_label]
        ralentissement_9_13 = st.slider("⏱️ Ralentissement sur la route 9-13", 0.5, 3.0, 1.0, 0.1)
        st.divider()
        st.markdown("### 🚧 Emplacements en travaux")
        all_travaux = st.checkbox("Tous les emplacements en travaux", value=False)
        if all_travaux:
            travaux = [e.numero for e in emplacements]
        else:
            travaux = st.multiselect("Sélectionnez les emplacements en travaux", [e.numero for e in emplacements], default=[3, 5, 7, 9, 11])
        st.divider()

    fluctuations = {(9, 13): ralentissement_9_13}
    etats = {num: "travaux" for num in travaux}

    for e in emplacements:
        e.etat = "travaux" if e.numero in travaux else "normal"

    with st.spinner("Calcul de la fréquentation..."):
        emp_freq, top3 = get_frequentation(fluctuations, etats)

    with st.sidebar:
        st.markdown("### 🏆 Top 3 emplacements les plus fréquentés")
        for i, (num, freq) in enumerate(top3, 1):
            travaux_emoji = " 🚧" if num in travaux else ""
            st.success(f"#{i} : Emplacement {num}{travaux_emoji} — {freq} passages")

    st.markdown("## 🗺️ Carte du réseau taxi")
    st.markdown("**Légende** : Gris = travaux, Vert = départ, Rouge = arrivée, Orange = trajet optimal, Bleu = normal.")

    if st.button("Calculer le trajet optimal"):
        if depart != destination:
            chemin, distance = depart.TrajetOpti(destination, ville.ListeRoutes, fluctuations=fluctuations, fluctuation=True)
            st.success(f"Chemin optimal : {' → '.join(str(e.numero) for e in chemin)} | Distance : {distance} min")
            fig = afficher_carte(ville, fluctuations, depart, destination, chemin, POS_FIXE, node_size=800, font_size=14, figsize=(8, 6))
            st.pyplot(fig)
        else:
            st.warning("Le départ et l'arrivée doivent être différents.")
    else:
        fig = afficher_carte(ville, fluctuations, depart, destination, None, POS_FIXE, node_size=800, font_size=14, figsize=(8, 6))
        st.pyplot(fig)

if __name__ == "__main__":
    main()