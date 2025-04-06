import unittest
from source.tache import Tache
from source.task_manager import generate_unique_id


class TestTache(unittest.TestCase):

    def test_creation_with_only_title(self):
        tache1 = Tache("Faire les courses")
        self.assertEqual(tache1.get_titre(), "Faire les courses", "Erreur sur le titre")
        self.assertEqual(
            tache1.get_priorite(), 1, "La priorité par défaut devrait être 1"
        )
        self.assertIsNone(
            tache1.description, "La description par défaut devrait être None"
        )
        self.assertIsNone(
            tache1.date_limite, "La date limite par défaut devrait être None"
        )
        self.assertIsNone(tache1.task_id, "L'id par défaut devrait être None")

    def test_setters_and_getters(self):
        tache1 = Tache("Faire les courses")
        tache1.set_description("Acheter fruits, légumes et pain")
        tache1.set_priorite(3)
        tache1.set_date_limite("2025-03-05")
        self.assertEqual(
            tache1.get_description(),
            "Acheter fruits, légumes et pain",
            "Erreur sur la description",
        )
        self.assertEqual(tache1.get_priorite(), 3, "Erreur sur la priorité")
        self.assertEqual(
            tache1.get_date_limite(), "2025-03-05", "Erreur sur la date limite"
        )

    def test_priority_minimum(self):
        tache1 = Tache("Faire les courses")
        tache1.set_priorite(0)
        self.assertEqual(
            tache1.get_priorite(), 1, "La priorité ne doit pas être inférieure à 1"
        )

    def test_to_dict_from_dict(self):
        # Création d'une tâche avec un id défini
        tache1 = Tache("Test", "Test description", 5, "2025-01-01", task_id=123456)
        d = tache1.to_dict()
        expected = {
            "task_id": 123456,
            "titre": "Test",
            "description": "Test description",
            "priorite": 5,
            "date_limite": "2025-01-01",
        }
        self.assertEqual(
            d, expected, "La conversion en dictionnaire ne fonctionne pas comme prévu"
        )

        # Reconstruction de la tâche à partir du dictionnaire
        tache2 = Tache.from_dict(d)
        self.assertEqual(tache2.get_titre(), "Test", "Erreur sur le titre reconstruit")
        self.assertEqual(
            tache2.get_description(),
            "Test description",
            "Erreur sur la description reconstruit",
        )
        self.assertEqual(tache2.get_priorite(), 5, "Erreur sur la priorité reconstruit")
        self.assertEqual(
            tache2.get_date_limite(),
            "2025-01-01",
            "Erreur sur la date limite reconstruit",
        )
        self.assertEqual(tache2.task_id, 123456, "L'id n'a pas été correctement reconstruit")

    def test_str_representation(self):
        tache1 = Tache(
            "Faire les courses", "Acheter du lait", 2, "2025-03-05", task_id=654321
        )
        rep = str(tache1)
        self.assertIn(
            "Tâche ID: 654321", rep, "La représentation en chaîne ne contient pas l'ID"
        )
        self.assertIn(
            "Titre: Faire les courses",
            rep,
            "La représentation en chaîne ne contient pas le titre",
        )

    def test_generate_unique_id(self):
        # Créer une liste de tâches avec des IDs connus
        tache1 = Tache("Tâche 1", task_id=111111)
        tache2 = Tache("Tâche 2", task_id=222222)
        tasks = [tache1, tache2]
        new_id = generate_unique_id(tasks)
        self.assertNotIn(
            new_id,
            {111111, 222222},
            "L'ID généré doit être unique par rapport aux tâches existantes",
        )
        self.assertTrue(
            100000 <= new_id <= 999999, "L'ID doit être un nombre à 6 chiffres"
        )

        # Test de génération avec une liste vide
        tasks = []
        new_id = generate_unique_id(tasks)
        self.assertTrue(
            100000 <= new_id <= 999999,
            "L'ID doit être un nombre à 6 chiffres pour une liste vide",
        )


if __name__ == "__main__":
    unittest.main()
