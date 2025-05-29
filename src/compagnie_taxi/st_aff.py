import streamlit as st
import networkx as nx
import compagnie_taxi.ville as ville
from compagnie_taxi.affichage import afficher_carte

# Initialisation de la ville et du graphe pour fixer les positions

ville.defListEmplacement()
ville.defListeRoutes()
for e1, e2, duree in ville.ListeRoutes:
    if e2 not in e1.voisins:
        e1.voisins.append(e2)
    if e1 not in e2.voisins:
        e2.voisins.append(e1)

G_base = nx.Graph()
for e1, e2, duree in ville.ListeRoutes:
    G_base.add_edge(e1.numero, e2.numero)
POS_FIXE = nx.spring_layout(G_base, seed=876)  # seed pour reproductibilité

def main():
    st.title("Compagnie Taxi - Visualisation du réseau")

    emplacements = ville.ListeEmplacement
    options = {f"Emplacement {e.numero}": e for e in emplacements}

    with st.sidebar:
        depart_label = st.selectbox("Point de départ", list(options.keys()), key="depart")
        destination_label = st.selectbox("Point d'arrivée", list(options.keys()), key="destination")
        depart = options[depart_label]
        destination = options[destination_label]
        ralentissement_9_13 = st.slider("Ralentissement sur la route 9-13", 0.5, 3.0, 1.0, 0.1)
        fluctuations = {
            (9, 13): ralentissement_9_13,
        }

    if st.button("Calculer le trajet optimal"):
        if depart != destination:
            chemin, distance = depart.TrajetOpti(destination, ville.ListeRoutes, fluctuations=fluctuations, fluctuation=True)
            st.success(f"Chemin optimal : {[e.numero for e in chemin]} | Distance : {distance}")
            fig = afficher_carte(ville, fluctuations, depart, destination, chemin, POS_FIXE)
            st.pyplot(fig)
        else:
            st.warning("Le départ et l'arrivée doivent être différents.")
    else:
        fig = afficher_carte(ville, fluctuations, depart, destination, None, POS_FIXE)
        st.pyplot(fig)

if __name__ == "__main__":
    main()