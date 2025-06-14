import unittest
from compagnie_taxi.reseau_taxi import Emplacement, Reseau


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
        routes = [(self.a, self.b, 5), (self.b, self.c, 3)]
        chemin, distance = self.a.TrajetOpti(self.c, routes)
        self.assertEqual([e.numero for e in chemin], [1, 2, 3])
        self.assertEqual(distance, 8)

    def test_trajet_opti_no_path(self):
        # Aucun chemin entre a et c
        routes = [(self.a, self.b, 5)]
        chemin, distance = self.a.TrajetOpti(self.c, routes)
        self.assertEqual(chemin, [])
        self.assertEqual(distance, float("inf"))

    def test_str_repr_eq_ne_lt_hash(self):
        a = Emplacement(1)
        b = Emplacement(2)
        a2 = Emplacement(1)
        self.assertEqual(str(a), "1")
        self.assertEqual(repr(a), "Emplacement(numero=1, voisins=[])")
        self.assertEqual(a, a2)
        self.assertNotEqual(a, b)
        self.assertTrue((a < b))
        self.assertEqual(hash(a), hash(a2))

    def test_reseau_methods(self):
        r = Reseau()
        a = Emplacement(1)
        b = Emplacement(2)
        r.ajouter_emplacement(a)
        r.ajouter_emplacement(b)
        r.ajouter_routes((a, b, 5))
        r.initialiser_voisins()
        self.assertIn(a, r.ListeEmplacement)
        self.assertIn(b, r.ListeEmplacement)
        self.assertIn((a, b, 5), r.ListeRoutes)
        self.assertIn(b, a.voisins)
        self.assertIn(a, b.voisins)
        r2 = Reseau()
        r2.ajouter_emplacement(Emplacement(1))
        r2.ajouter_emplacement(Emplacement(2))
        r2.ajouter_routes((r2.ListeEmplacement[0], r2.ListeEmplacement[1], 5))
        r2.initialiser_voisins()
        self.assertEqual(r, r2)
        self.assertTrue(not (r != r2))

    def test_trajet_opti_fluctuations(self):
        a = Emplacement(1)
        b = Emplacement(2)
        a.voisins = [b]
        b.voisins = [a]
        routes = [(a, b, 10)]
        chemin, distance = a.TrajetOpti(
            b, routes, fluctuations={(1, 2): 2.0}, fluctuation=True
        )
        self.assertEqual(chemin, [a, b])
        self.assertEqual(distance, 20)


if __name__ == "__main__":
    unittest.main()
