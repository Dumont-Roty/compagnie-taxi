from src.compagnie_taxi.reseau import *

# Ecriture des voisins sous format de liste.

emplacements = {i: emplacement(i, False) for i in range(1, 17)}

voisinages = [
    (1, 2, 5), (1, 3, 9), (1, 4, 4),
    (2, 5, 3), (2, 6, 2),
    (3, 4, 4), (3, 6, 1),
    (4, 7, 7),
    (5, 8, 4), (5, 9, 2), (5, 10, 9),
    (6, 7, 3), (6, 10, 9), (6, 11, 6),
    (7, 11, 8), (7, 15, 5),
    (8, 12, 5),
    (9, 8, 3), (9, 13, 10),
    (10, 9, 6), (10, 13, 5), (10, 14, 1),
    (11, 14, 2),
    (12, 16, 9),
    (13, 12, 4), (13, 14, 3),
    (14, 16, 4),
    (15, 14, 4), (15, 16, 3)
]

for a, b, duree in voisinages:
    emplacements[a].voisins.append((emplacements[b], duree))
    emplacements[b].voisins.append((emplacements[a], duree))
    
