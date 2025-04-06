import unittest, io, sys, os, tempfile

sys.path.insert(
    0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../source"))
)
import task_manager
from unittest.mock import patch
from source.tache import Tache


class TestTaskManagerArgs(unittest.TestCase):

    def test_add_command_arguments(self):
        # Simuler l'ajout d'une tâche avec des arguments précis.
        test_argv = [
            "task_manager.py",
            "add",
            "--title",
            "Test Title",
            "--desc",
            "Test description",
            "--priority",
            "2",
            "--due",
            "2025-03-05",
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
                    self.assertIsNotNone(task.task_id, "La tâche doit recevoir un ID unique")

    def test_remove_command_arguments(self):
        # Créer une tâche fictive avec un ID connu pour tester la suppression.
        task_to_remove = Tache("Task to remove", task_id=123456)
        test_argv = ["task_manager.py", "remove", "--id", "123456"]
        with patch.object(sys, "argv", test_argv):
            with patch(
                "task_manager.load_tasks", return_value=[task_to_remove]
            ) as mock_load:
                with patch("task_manager.save_tasks") as mock_save:
                    task_manager.main()
                    # Après suppression, la liste doit être vide.
                    mock_save.assert_called_once()
                    tasks_list = mock_save.call_args[0][0]
                    self.assertEqual(len(tasks_list), 0)

    def test_edit_command_arguments(self):
        # Créer une tâche fictive à modifier.
        task_to_edit = Tache("Old Title", "Old Description", 1, "2025-01-01", task_id=123456)
        test_argv = [
            "task_manager.py",
            "edit",
            "--id",
            "123456",
            "--title",
            "New Title",
            "--desc",
            "New Description",
            "--priority",
            "3",
            "--due",
            "2025-04-01",
        ]
        with patch.object(sys, "argv", test_argv):
            with patch(
                "task_manager.load_tasks", return_value=[task_to_edit]
            ) as mock_load:
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
        task1 = Tache("Task 1", "Desc 1", 1, "2025-01-01", task_id=111111)
        task2 = Tache("Task 2", "Desc 2", 2, "2025-02-02", task_id=222222)
        test_argv = ["task_manager.py", "list"]
        with patch.object(sys, "argv", test_argv):
            with patch(
                "task_manager.load_tasks", return_value=[task1, task2]
            ) as mock_load:
                # Pour "list", aucune sauvegarde ne doit être effectuée.
                with patch("task_manager.save_tasks") as mock_save:
                    task_manager.main()
                    mock_save.assert_not_called()

    def test_load_tasks_valid_file(self):
        # Construction du chemin absolu vers le fichier de test
        current_dir = os.path.dirname(__file__)
        json_file_path = os.path.join(current_dir, "test_tasks.json")
        # Chargement des tâches à partir du fichier de test
        tasks = task_manager.load_tasks(json_file_path)
        self.assertEqual(len(tasks), 3)

        # Vérification de la première tâche
        self.assertEqual(tasks[0].get_titre(), "Tache de test")
        self.assertIsNone(tasks[0].get_description())
        self.assertEqual(tasks[0].get_priorite(), 1)
        self.assertIsNone(tasks[0].get_date_limite())

        # Vérification de la deuxième tâche
        self.assertEqual(tasks[1].get_titre(), "Tache de test 2")
        self.assertIsNone(tasks[1].get_description())
        self.assertEqual(tasks[1].get_priorite(), 1)
        self.assertEqual(tasks[1].get_date_limite(), "2025-04-06")

        # Vérification de la troisième tâche
        self.assertEqual(tasks[2].get_titre(), "Tache de test 3")
        self.assertEqual(tasks[2].get_description(), "La description")
        self.assertEqual(tasks[2].get_priorite(), 1)
        self.assertEqual(tasks[2].get_date_limite(), "2025-04-20")

    def test_load_tasks_file_not_found(self):
        # Si le fichier n'existe pas, load_tasks doit retourner une liste vide.
        tasks = task_manager.load_tasks("nonexistent_file.json")
        self.assertEqual(tasks, [])

    def test_load_tasks_invalid_json(self):
        # Création d'un fichier temporaire contenant un contenu invalide (non JSON)
        with tempfile.NamedTemporaryFile("w", delete=False, encoding="utf-8") as tmp:
            tmp.write("ce n'est pas du JSON valide")
            tmp_filename = tmp.name
        try:
            # Capturer l'affichage du message d'erreur
            with patch("builtins.print") as mock_print:
                tasks = task_manager.load_tasks(tmp_filename)
                self.assertEqual(tasks, [])
                mock_print.assert_called_with(
                    "Erreur lors du décodage du fichier JSON."
                )
        finally:
            os.remove(tmp_filename)

    def test_remove_nonexistent_id(self):
        # Tester la suppression d'une tâche avec un ID inexistant
        test_id = "999999"
        test_argv = ["task_manager.py", "remove", "--id", test_id]
        with patch.object(sys, "argv", test_argv):
            # Simuler l'absence de tâches (liste vide)
            with patch("task_manager.load_tasks", return_value=[]):
                with patch("task_manager.save_tasks") as mock_save:
                    # Capturer la sortie standard pour vérifier le message affiché
                    with patch("sys.stdout", new_callable=io.StringIO) as fake_out:
                        task_manager.main()
                        output = fake_out.getvalue()
                        # Vérifier que le message d'erreur attendu est affiché
                        self.assertIn(
                            f"Aucune tâche trouvée avec l'ID {test_id}", output
                        )
                        # Vérifier qu'aucune sauvegarde n'est effectuée
                        mock_save.assert_not_called()

    def test_edit_nonexistent_id(self):
        # Tester l'édition d'une tâche avec un ID inexistant
        test_id = "999999"
        test_argv = [
            "task_manager.py",
            "edit",
            "--id",
            test_id,
            "--title",
            "New Title",
            "--desc",
            "New Description",
            "--priority",
            "3",
            "--due",
            "2025-04-01",
        ]
        with patch.object(sys, "argv", test_argv):
            # Simuler l'absence de tâches (liste vide)
            with patch("task_manager.load_tasks", return_value=[]):
                with patch("task_manager.save_tasks") as mock_save:
                    # Capturer la sortie standard pour vérifier le message affiché
                    with patch("sys.stdout", new_callable=io.StringIO) as fake_out:
                        task_manager.main()
                        output = fake_out.getvalue()
                        # Vérifier que le message d'erreur attendu est affiché
                        self.assertIn(
                            f"Aucune tâche trouvée avec l'ID {test_id}", output
                        )
                        # Vérifier qu'aucune sauvegarde n'est effectuée
                        mock_save.assert_not_called()


if __name__ == "__main__":
    unittest.main()
