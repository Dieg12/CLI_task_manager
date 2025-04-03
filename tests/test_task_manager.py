import unittest
from unittest.mock import patch
import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../source')))
import task_manager
from source.tache import Tache

class TestTaskManagerArgs(unittest.TestCase):
    def test_version_command_arguments(self):
        # Pour la commande --version, aucune sauvegarde ne doit être réalisée.
        test_argv = ["task_manager.py", "--version"]
        with patch.object(sys, "argv", test_argv):
            with patch("task_manager.load_tasks", return_value=[]) as mock_load:
                with patch("task_manager.save_tasks") as mock_save:
                    task_manager.main()
                    # Pour la version, save_tasks ne doit pas être appelée.
                    mock_save.assert_not_called()

    def test_add_command_arguments(self):
        # Simuler l'ajout d'une tâche avec des arguments précis.
        test_argv = [
            "task_manager.py", "add",
            "--title", "Test Title",
            "--desc", "Test description",
            "--priority", "2",
            "--due", "2025-03-05"
        ]
        with patch.object(sys, "argv", test_argv):
            # On simule une liste vide initialement.
            with patch("task_manager.load_tasks", return_value=[]) as mock_load:
                with patch("task_manager.save_tasks") as mock_save:
                    task_manager.main()
                    # Vérifier que save_tasks a été appelée avec une liste contenant une seule tâche
                    mock_save.assert_called_once()
                    tasks_list = mock_save.call_args[0][0]
                    self.assertEqual(len(tasks_list), 1)
                    task = tasks_list[0]
                    self.assertEqual(task.get_titre(), "Test Title")
                    self.assertEqual(task.get_description(), "Test description")
                    self.assertEqual(task.get_priorite(), 2)
                    self.assertEqual(task.get_date_limite(), "2025-03-05")
                    self.assertIsNotNone(task.id, "La tâche doit recevoir un ID unique")

    def test_remove_command_arguments(self):
        # Créer une tâche fictive avec un ID connu pour tester la suppression.
        task_to_remove = Tache("Task to remove", id=123456)
        test_argv = ["task_manager.py", "remove", "--id", "123456"]
        with patch.object(sys, "argv", test_argv):
            with patch("task_manager.load_tasks", return_value=[task_to_remove]) as mock_load:
                with patch("task_manager.save_tasks") as mock_save:
                    task_manager.main()
                    # Après suppression, la liste doit être vide.
                    mock_save.assert_called_once()
                    tasks_list = mock_save.call_args[0][0]
                    self.assertEqual(len(tasks_list), 0)

    def test_edit_command_arguments(self):
        # Créer une tâche fictive à modifier.
        task_to_edit = Tache("Old Title", "Old Description", 1, "2025-01-01", id=123456)
        test_argv = [
            "task_manager.py", "edit",
            "--id", "123456",
            "--title", "New Title",
            "--desc", "New Description",
            "--priority", "3",
            "--due", "2025-04-01"
        ]
        with patch.object(sys, "argv", test_argv):
            with patch("task_manager.load_tasks", return_value=[task_to_edit]) as mock_load:
                with patch("task_manager.save_tasks") as mock_save:
                    task_manager.main()
                    # Vérifier que les attributs de la tâche ont été mis à jour.
                    self.assertEqual(task_to_edit.get_titre(), "New Title")
                    self.assertEqual(task_to_edit.get_description(), "New Description")
                    self.assertEqual(task_to_edit.get_priorite(), 3)
                    self.assertEqual(task_to_edit.get_date_limite(), "2025-04-01")
                    mock_save.assert_called_once()

    def test_list_command_arguments(self):
        # Créer une liste fictive de tâches pour la commande "list".
        task1 = Tache("Task 1", "Desc 1", 1, "2025-01-01", id=111111)
        task2 = Tache("Task 2", "Desc 2", 2, "2025-02-02", id=222222)
        test_argv = ["task_manager.py", "list"]
        with patch.object(sys, "argv", test_argv):
            with patch("task_manager.load_tasks", return_value=[task1, task2]) as mock_load:
                # Pour "list", aucune sauvegarde ne doit être effectuée.
                with patch("task_manager.save_tasks") as mock_save:
                    task_manager.main()
                    mock_save.assert_not_called()

if __name__ == "__main__":
    unittest.main()
