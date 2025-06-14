import unittest
import compagnie_taxi.ville as ville
from compagnie_taxi.reseau_taxi import Emplacement


class TestVille(unittest.TestCase):
    def setUp(self):
        ville.ListeEmplacement.clear()
        ville.ListeRoutes.clear()
        ville.defListEmplacement()
        ville.defListeRoutes()
        ville.initialiser_voisins()

    def test_nb_emplacements(self):
        # Vérifie qu'il y a bien 16 emplacements
        self.assertEqual(len(ville.ListeEmplacement), 16)

    def test_emplacement_type(self):
        # Vérifie que chaque élément est bien un Emplacement
        for e in ville.ListeEmplacement:
            self.assertIsInstance(e, Emplacement)

    def test_routes_non_vides(self):
        # Vérifie qu'il y a au moins une route
        self.assertGreater(len(ville.ListeRoutes), 0)

    def test_routes_coherence(self):
        # Vérifie que chaque route relie deux emplacements de la liste
        for e1, e2, duree in ville.ListeRoutes:
            self.assertIn(e1, ville.ListeEmplacement)
            self.assertIn(e2, ville.ListeEmplacement)
            self.assertIsInstance(duree, int)

    def test_voisins_apres_init(self):
        # Chaque route doit être dans les voisins de chaque extrémité
        for e1, e2, duree in ville.ListeRoutes:
            self.assertIn(e2, e1.voisins)
            self.assertIn(e1, e2.voisins)


if __name__ == "__main__":
    unittest.main()
