import streamlit as st
from compagnie_taxi.reseau_taxi import *
import compagnie_taxi.ville as ville
import matplotlib.pyplot as plt
import networkx as nx

# Initialisation de la ville et du graphe pour fixer les positions
ville.defListEmplacement()
ville.defListeRoutes()
G_base = nx.Graph()
for e1, e2, duree in ville.ListeRoutes:
    G_base.add_edge(e1.numero, e2.numero)
POS_FIXE = nx.spring_layout(G_base, seed=876)  # seed pour reproductibilité

def AfficherCarte(fluctuations, depart=None, destination=None, chemin=None):
    G = nx.Graph()
    edges = []
    for e1, e2, duree in ville.ListeRoutes:
        coef = 1.0
        key = (e1.numero, e2.numero)
        key_inv = (e2.numero, e1.numero)
        if key in fluctuations:
            coef = fluctuations[key]
        elif key_inv in fluctuations:
            coef = fluctuations[key_inv]
        duree_mod = int(duree * coef)
        edges.append((e1.numero, e2.numero, {'duree': duree_mod}))
    G.add_edges_from(edges)

    fig, ax = plt.subplots()
    node_colors = []
    for n in G.nodes():
        if depart and n == depart.numero:
            node_colors.append('green')
        elif destination and n == destination.numero:
            node_colors.append('red')
        elif chemin and n in [e.numero for e in chemin]:
            node_colors.append('orange')
        else:
            node_colors.append('skyblue')
    nx.draw(G, POS_FIXE, with_labels=True, ax=ax, node_color=node_colors)
    edge_labels = nx.get_edge_attributes(G, 'duree')
    nx.draw_networkx_edge_labels(G, POS_FIXE, edge_labels=edge_labels, ax=ax)
    st.pyplot(fig)

def main():
    st.title("Compagnie Taxi - Visualisation du réseau")

    emplacements = ville.ListeEmplacement
    options = {f"Emplacement {e.numero}": e for e in emplacements}

    col1, col2 = st.columns(2)
    with col1:
        depart_label = st.selectbox("Point de départ", list(options.keys()), key="depart")
    with col2:
        destination_label = st.selectbox("Point d'arrivée", list(options.keys()), key="destination")

    depart = options[depart_label]
    destination = options[destination_label]

    st.write("Choisissez les fluctuations pour certaines routes :")
    ralentissement_9_13 = st.slider("Ralentissement sur la route 9-13", 0.5, 3.0, 1.2, 0.1)
    fluctuations = {
        (9, 13): ralentissement_9_13,
    }

    if "trajet_valide" not in st.session_state:
        st.session_state.trajet_valide = False
    if "chemin" not in st.session_state:
        st.session_state.chemin = None
    if "distance" not in st.session_state:
        st.session_state.distance = None
    if "last_depart" not in st.session_state:
        st.session_state.last_depart = depart
    if "last_destination" not in st.session_state:
        st.session_state.last_destination = destination
    if "last_fluctuations" not in st.session_state:
        st.session_state.last_fluctuations = fluctuations.copy()

    if st.button("Valider le trajet"):
        if depart != destination:
            chemin, distance = depart.TrajetOpti(destination, ville.ListeRoutes, fluctuations)
            st.session_state.chemin = chemin
            st.session_state.distance = distance
            st.session_state.last_depart = depart
            st.session_state.last_destination = destination
            st.session_state.last_fluctuations = fluctuations.copy()
            st.session_state.trajet_valide = True
        else:
            st.warning("Le départ et l'arrivée doivent être différents.")
            st.session_state.trajet_valide = False

    # Affiche le chemin seulement si validé
    if st.session_state.trajet_valide and st.session_state.chemin:
        st.success(f"Chemin optimal : {[e.numero for e in st.session_state.chemin]} | Distance : {st.session_state.distance}")
        st.markdown(f"**Chemin parcouru :** {' → '.join(str(e.numero) for e in st.session_state.chemin)}")
        AfficherCarte(fluctuations, st.session_state.last_depart, st.session_state.last_destination, st.session_state.chemin)
    else:
        AfficherCarte(fluctuations, depart, destination, None)

if __name__ == "__main__":
    main()