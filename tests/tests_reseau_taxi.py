import unittest
from compagnie_taxi.reseau_taxi import Emplacement

class TestEmplacement(unittest.TestCase):
    def setUp(self):
        # Création de 3 emplacements pour les tests
        self.a = Emplacement(1)
        self.b = Emplacement(2)
        self.c = Emplacement(3)
        # Définition des voisins
        self.a.voisins = [self.b]
        self.b.voisins = [self.a, self.c]
        self.c.voisins = [self.b]

    def test_est_voisin(self):
        self.assertTrue(self.a.EstVoisin(self.b))
        self.assertFalse(self.a.EstVoisin(self.c))
        self.assertTrue(self.b.EstVoisin(self.c))

    def test_equality(self):
        a2 = Emplacement(1)
        self.assertEqual(self.a, a2)
        self.assertNotEqual(self.a, self.b)

    def test_hash(self):
        a2 = Emplacement(1)
        self.assertEqual(hash(self.a), hash(a2))

    def test_trajet_opti_simple(self):
        
        routes = [
            (self.a, self.b, 5),
            (self.b, self.c, 3)
        ]
        chemin, distance = self.a.TrajetOpti(self.c, routes)
        self.assertEqual([e.numero for e in chemin], [1, 2, 3])
        self.assertEqual(distance, 8)

    def test_trajet_opti_no_path(self):
        # Aucun chemin entre a et c
        routes = [
            (self.a, self.b, 5)
        ]
        chemin, distance = self.a.TrajetOpti(self.c, routes)
        self.assertEqual(chemin, [])
        self.assertEqual(distance, float('inf'))

if __name__ == "__main__":
    unittest.main()

