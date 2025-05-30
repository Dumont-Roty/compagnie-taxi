import unittest
from compagnie_taxi.analyse_frequentation import AnalyseFrequentation

class TestAnalyseFrequentation(unittest.TestCase):
    def test_frequentation_emplacements(self):
        analyseur = AnalyseFrequentation(fluctuations={(9, 13): 2.0}, etats_emplacements={3: "travaux"})
        trajets = analyseur.calculer_tous_trajets()
        emp_freq = analyseur.frequentation_emplacements(trajets)
        self.assertEqual(len(emp_freq), 16)
        self.assertTrue(all(isinstance(v, int) for v in emp_freq.values()))
        self.assertIn(3, emp_freq)
        self.assertTrue(any(v > 0 for v in emp_freq.values()))

    def test_top_emplacements(self):
        analyseur = AnalyseFrequentation()
        trajets = analyseur.calculer_tous_trajets()
        emp_freq = analyseur.frequentation_emplacements(trajets)
        top3 = analyseur.top_emplacements(emp_freq, n=3)
        self.assertEqual(len(top3), 3)
        self.assertTrue(all(top3[i][1] >= top3[i+1][1] for i in range(2)))

if __name__ == "__main__":
    unittest.main()