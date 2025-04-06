#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Module de tests pour le gestionnaire de tâches (task_manager).

Ce module contient des tests unitaires pour vérifier le bon fonctionnement
des commandes "add", "remove", "edit", "list" ainsi que des fonctions de
chargement et sauvegarde des tâches.

Chaque méthode de test est documentée avec une docstring au format Google.
"""

import unittest
import io
import sys
import os
import tempfile

sys.path.insert(
    0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../source"))
)
import task_manager
from unittest.mock import patch
from source.tache import Tache


class TestTaskManagerArgs(unittest.TestCase):
    """Tests unitaires pour les arguments des commandes de task_manager."""

    def test_add_command_arguments(self):
        """Test de la commande d'ajout de tâche avec arguments.

        Simule l'ajout d'une tâche avec des arguments précis et vérifie que :
          - La fonction save_tasks est appelée avec une liste contenant une tâche.
          - Les attributs de la tâche (titre, description, priorité, date limite)
            sont correctement définis.
          - Un ID unique est attribué à la tâche.
        """
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
            with patch("task_manager.load_tasks", return_value=[]) as mock_load:
                with patch("task_manager.save_tasks") as mock_save:
                    task_manager.main()
                    mock_save.assert_called_once()
                    tasks_list = mock_save.call_args[0][0]
                    self.assertEqual(len(tasks_list), 1)
                    task = tasks_list[0]
                    self.assertEqual(task.get_titre(), "Test Title")
                    self.assertEqual(task.get_description(), "Test description")
                    self.assertEqual(task.get_priorite(), 2)
                    self.assertEqual(task.get_date_limite(), "2025-03-05")
                    self.assertIsNotNone(
                        task.task_id, "La tâche doit recevoir un ID unique"
                    )

    def test_remove_command_arguments(self):
        """Test de la commande de suppression de tâche.

        Simule la suppression d'une tâche en utilisant un ID connu et vérifie
        que la tâche est retirée de la liste.
        """
        task_to_remove = Tache("Task to remove", task_id=123456)
        test_argv = ["task_manager.py", "remove", "--id", "123456"]
        with patch.object(sys, "argv", test_argv):
            with patch(
                "task_manager.load_tasks", return_value=[task_to_remove]
            ) as mock_load:
                with patch("task_manager.save_tasks") as mock_save:
                    task_manager.main()
                    mock_save.assert_called_once()
                    tasks_list = mock_save.call_args[0][0]
                    self.assertEqual(len(tasks_list), 0)

    def test_edit_command_arguments(self):
        """Test de la commande d'édition de tâche.

        Simule la modification d'une tâche à l'aide d'un ID et vérifie que les
        attributs de la tâche sont mis à jour en conséquence.
        """
        task_to_edit = Tache(
            "Old Title", "Old Description", 1, "2025-01-01", task_id=123456
        )
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
                    self.assertEqual(task_to_edit.get_titre(), "New Title")
                    self.assertEqual(task_to_edit.get_description(), "New Description")
                    self.assertEqual(task_to_edit.get_priorite(), 3)
                    self.assertEqual(task_to_edit.get_date_limite(), "2025-04-01")
                    mock_save.assert_called_once()

    def test_list_command_arguments(self):
        """Test de la commande de liste des tâches.

        Simule l'affichage d'une liste de tâches et vérifie que la fonction
        save_tasks n'est pas appelée lors de l'exécution de la commande list.
        """
        task1 = Tache("Task 1", "Desc 1", 1, "2025-01-01", task_id=111111)
        task2 = Tache("Task 2", "Desc 2", 2, "2025-02-02", task_id=222222)
        test_argv = ["task_manager.py", "list"]
        with patch.object(sys, "argv", test_argv):
            with patch(
                "task_manager.load_tasks", return_value=[task1, task2]
            ) as mock_load:
                with patch("task_manager.save_tasks") as mock_save:
                    task_manager.main()
                    mock_save.assert_not_called()

    def test_load_tasks_valid_file(self):
        """Test du chargement de tâches depuis un fichier JSON valide.

        Vérifie que :
          - Le nombre de tâches chargées est correct.
          - Les attributs des tâches (titre, description, priorité, date limite)
            correspondent aux valeurs attendues.
        """
        current_dir = os.path.dirname(__file__)
        json_file_path = os.path.join(current_dir, "test_tasks.json")
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
        """Test du chargement de tâches à partir d'un fichier inexistant.

        Vérifie que la fonction load_tasks retourne une liste vide si le fichier
        spécifié n'existe pas.
        """
        tasks = task_manager.load_tasks("nonexistent_file.json")
        self.assertEqual(tasks, [])

    def test_load_tasks_invalid_json(self):
        """Test du chargement de tâches depuis un fichier contenant un JSON invalide.

        Vérifie que la fonction load_tasks retourne une liste vide et affiche un
        message d'erreur en cas d'échec du décodage JSON.
        """
        with tempfile.NamedTemporaryFile("w", delete=False, encoding="utf-8") as tmp:
            tmp.write("ce n'est pas du JSON valide")
            tmp_filename = tmp.name
        try:
            with patch("builtins.print") as mock_print:
                tasks = task_manager.load_tasks(tmp_filename)
                self.assertEqual(tasks, [])
                mock_print.assert_called_with(
                    "Erreur lors du décodage du fichier JSON."
                )
        finally:
            os.remove(tmp_filename)

    def test_remove_nonexistent_id(self):
        """Test de la suppression d'une tâche avec un ID inexistant.

        Vérifie que lorsque l'on tente de supprimer une tâche dont l'ID n'existe pas,
        un message d'erreur est affiché et aucune sauvegarde n'est effectuée.
        """
        test_id = "999999"
        test_argv = ["task_manager.py", "remove", "--id", test_id]
        with patch.object(sys, "argv", test_argv):
            with patch("task_manager.load_tasks", return_value=[]):
                with patch("task_manager.save_tasks") as mock_save:
                    with patch("sys.stdout", new_callable=io.StringIO) as fake_out:
                        task_manager.main()
                        output = fake_out.getvalue()
                        self.assertIn(
                            f"Aucune tâche trouvée avec l'ID {test_id}", output
                        )
                        mock_save.assert_not_called()

    def test_edit_nonexistent_id(self):
        """Test de l'édition d'une tâche avec un ID inexistant.

        Vérifie que lorsque l'on tente d'éditer une tâche dont l'ID n'existe pas,
        un message d'erreur est affiché et aucune sauvegarde n'est effectuée.
        """
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
            with patch("task_manager.load_tasks", return_value=[]):
                with patch("task_manager.save_tasks") as mock_save:
                    with patch("sys.stdout", new_callable=io.StringIO) as fake_out:
                        task_manager.main()
                        output = fake_out.getvalue()
                        self.assertIn(
                            f"Aucune tâche trouvée avec l'ID {test_id}", output
                        )
                        mock_save.assert_not_called()


if __name__ == "__main__":
    unittest.main()
