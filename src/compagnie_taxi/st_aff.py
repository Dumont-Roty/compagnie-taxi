import streamlit as st
from compagnie_taxi.reseau_taxi import *
import compagnie_taxi.ville as ville
import matplotlib.pyplot as plt
import networkx as nx

def AfficherCarte(fluctuations):
    ville.defListEmplacement()
    ville.defListeRoutes()
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

    pos = nx.spring_layout(G, weight='duree')
    fig, ax = plt.subplots()
    nx.draw(G, pos, with_labels=True, ax=ax)
    edge_labels = nx.get_edge_attributes(G, 'duree')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, ax=ax)
    st.pyplot(fig)

def main():
    st.title("Compagnie Taxi - Visualisation du réseau")
    st.write("Choisissez les fluctuations pour certaines routes :")

    ralentissement_9_13 = st.slider("Ralentissement sur la route 9-13", 0.5, 3.0, 1.2, 0.1)
    fluidification_10_14 = st.slider("Fluidification sur la route 10-14", 0.5, 3.0, 0.8, 0.1)

    fluctuations = {
        (9, 13): ralentissement_9_13,
        (10, 14): fluidification_10_14
    }

    if st.button("Afficher la carte"):
        AfficherCarte(fluctuations)

if __name__ == "__main__":
    main()