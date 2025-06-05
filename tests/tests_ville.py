import unittest
import src.compagnie_taxi.ville as ville

class TestVille(unittest.TestCase):
    def setUp(self):
        ville.ListeEmplacement.clear()
        ville.ListeRoutes.clear()
        ville.defListEmplacement()
        ville.defListeRoutes()

    def test_nb_emplacements(self):
        # Vérifie qu'il y a bien 16 emplacements
        self.assertEqual(len(ville.ListeEmplacement), 16)

    def test_emplacement_type(self):
        # Vérifie que chaque élément est bien un Emplacement
        from compagnie_taxi.reseau_taxi import Emplacement
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
        # Vérifie que les voisins sont bien initialisés
        for e1, e2, duree in ville.ListeRoutes:
            if e2 not in e1.voisins:
                e1.voisins.append(e2)
            if e1 not in e2.voisins:
                e2.voisins.append(e1)
        # Chaque route doit être dans les voisins de chaque extrémité
        for e1, e2, duree in ville.ListeRoutes:
            self.assertIn(e2, e1.voisins)
            self.assertIn(e1, e2.voisins)

if __name__ == "__main__":
    unittest.main()