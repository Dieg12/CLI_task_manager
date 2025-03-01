import unittest
from source.tache import Tache

class TestTache(unittest.TestCase):

    def test_creation_with_only_title(self):
        """Test de la création d'une tâche avec uniquement le titre."""
        tache1 = Tache("Faire les courses")
        self.assertEqual(tache1.get_titre(), "Faire les courses", "Erreur sur le titre")
        self.assertEqual(tache1.get_priorite(), 1, "La priorité par défaut devrait être 1")

    def test_setters_and_getters(self):
        """Test des setters et getters de la tâche."""
        tache1 = Tache("Faire les courses")
        tache1.set_description("Acheter fruits, légumes et pain")
        tache1.set_priorite(3)
        tache1.set_date_limite("2025-03-05")

        self.assertEqual(tache1.get_description(), "Acheter fruits, légumes et pain", "Erreur sur la description")
        self.assertEqual(tache1.get_priorite(), 3, "Erreur sur la priorité")
        self.assertEqual(tache1.get_date_limite(), "2025-03-05", "Erreur sur la date limite")

    def test_priority_minimum(self):
        """Test de la validation de la priorité minimale."""
        tache1 = Tache("Faire les courses")
        tache1.set_priorite(0)
        self.assertEqual(tache1.get_priorite(), 1, "La priorité ne doit pas être inférieure à 1")

if __name__ == "__main__":
    unittest.main()
