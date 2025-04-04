#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Module task_manager.

Ce module fournit une interface en ligne de commande (CLI) pour la gestion d'une liste de tâches.
Il offre les fonctionnalités suivantes :

- Chargement et sauvegarde des tâches depuis/vers un fichier JSON.
- Ajout d'une nouvelle tâche, avec génération d'un identifiant unique.
- Suppression d'une tâche existante par son identifiant.
- Affichage de la liste des tâches, avec possibilité de tri par titre, priorité ou date d'échéance.
- Modification d'une tâche existante (édition).

Les tâches sont représentées par des instances de la classe Tache définie dans le module source.tache.
Les messages affichés à l'utilisateur sont centralisés dans le module source.textes.
"""

import argparse
import json
import random
from source.tache import Tache  # Importation de la classe Tache depuis tache.py
from source.textes import WELCOME_MESSAGE, ERROR_MESSAGE

DEFAULT_FILENAME = "tasks.json"  # Nom par défaut du fichier de sauvegarde des tâches


def load_tasks(filename):
    """
    Charge les tâches depuis un fichier JSON et retourne une liste d'objets Tache.

    Cette fonction tente d'ouvrir et de décoder le fichier JSON spécifié par `filename`.
    Si le fichier n'existe pas ou en cas d'erreur de décodage, elle retourne une liste vide.

    :param filename: Chemin du fichier JSON contenant les tâches, par défaut "tasks.json".
    :type filename: str
    :return: Liste des tâches chargées sous forme d'instances de Tache.
    :rtype: list[Tache]
    """
    try:
        with open(filename, "r", encoding="utf-8") as file:
            tasks_data = json.load(file)
        # Reconstruit les objets Tache à partir des dictionnaires
        tasks = [Tache.from_dict(item) for item in tasks_data]
        return tasks
    except FileNotFoundError:
        # Fichier non trouvé, on retourne une liste vide
        return []
    except json.JSONDecodeError:
        print("Erreur lors du décodage du fichier JSON.")
        return []


def save_tasks(tasks, filename="tasks.json"):
    """
    Sauvegarde une liste d'objets Tache dans un fichier JSON.

    Chaque objet Tache est converti en dictionnaire avant d'être sauvegardé.
    Le fichier est écrit avec l'encodage UTF-8 et une indentation pour améliorer la lisibilité.

    :param tasks: Liste des tâches à sauvegarder.
    :type tasks: list[Tache]
    :param filename: Chemin du fichier JSON dans lequel sauvegarder les tâches, par défaut "tasks.json".
    :type filename: str
    """
    tasks_data = [task.to_dict() for task in tasks]
    with open(filename, "w", encoding="utf-8") as file:
        json.dump(tasks_data, file, ensure_ascii=False, indent=4)


def generate_unique_id(tasks):
    """
    Génère un identifiant aléatoire à 6 chiffres qui n'est pas déjà utilisé parmi les tâches existantes.

    La fonction récupère les identifiants existants dans la liste `tasks` et continue à générer
    un nombre aléatoire entre 100000 et 999999 jusqu'à obtenir un identifiant unique.

    :param tasks: Liste des tâches existantes.
    :type tasks: list[Tache]
    :return: Un identifiant unique pour une nouvelle tâche.
    :rtype: int
    """
    existing_ids = {task.id for task in tasks if task.id is not None}
    while True:
        candidate = random.randint(100000, 999999)
        if candidate not in existing_ids:
            return candidate


def main():
    """
    Point d'entrée principal de l'application CLI de gestion de tâches.

    Cette fonction réalise les opérations suivantes :
      - Affiche un message de bienvenue.
      - Analyse les arguments de la ligne de commande à l'aide d'argparse.
      - En fonction de la commande spécifiée (add, remove, list, edit ou --version), exécute l'opération correspondante :
          - `add` : Ajoute une nouvelle tâche avec les attributs fournis et génère un identifiant unique.
          - `remove` : Supprime une tâche identifiée par son ID.
          - `list` : Affiche la liste des tâches, avec possibilité de tri par titre, priorité ou date d'échéance.
          - `edit` : Modifie une tâche existante en mettant à jour ses attributs.
          - `--version` : Affiche la version de l'application.
      - Charge les tâches existantes depuis un fichier JSON avant l'exécution et sauvegarde les modifications apportées.

    :return: None
    """
    print(WELCOME_MESSAGE)

    parser = argparse.ArgumentParser(
        description="Une application CLI simple.",
        formatter_class=argparse.RawTextHelpFormatter,
    )

    # Option globale pour afficher la version
    parser.add_argument(
        "--version", action="store_true", help="Affiche la version de l'application."
    )

    # Création des sous-commandes
    subparsers = parser.add_subparsers(
        dest="command",
        title="Commandes disponibles",
        help="Choisissez une commande à exécuter",
    )

    # Commande 'add' : Ajoute une tâche à la liste
    parser_add = subparsers.add_parser("add", help="Ajoute une tâche à la liste")
    parser_add.add_argument("--title", required=True, help="Titre de la tâche")
    parser_add.add_argument("--desc", help="Description de la tâche")
    parser_add.add_argument(
        "--priority", type=int, default=1, help="Priorité de la tâche (défaut: 1)"
    )
    parser_add.add_argument(
        "--due", help="Date d'échéance de la tâche (format YYYY-MM-DD)"
    )

    # Commande 'remove' : Supprime une tâche de la liste
    parser_remove = subparsers.add_parser(
        "remove", help="Supprime une tâche de la liste"
    )
    parser_remove.add_argument(
        "--id", required=True, help="Identifiant de la tâche à supprimer"
    )

    # Commande 'list' : Affiche la liste des tâches
    parser_list = subparsers.add_parser("list", help="Affiche la liste des tâches")
    parser_list.add_argument(
        "--sort",
        choices=["title", "priority", "due"],
        help=(
            "Trier la liste par :\n"
            "  title     Trier par titre\n"
            "  priority  Trier par priorité\n"
            "  due       Trier par date d'échéance"
        ),
    )

    # Commande 'edit' : Modifie une tâche existante
    parser_edit = subparsers.add_parser("edit", help="Modifie une tâche existante")
    parser_edit.add_argument(
        "--id", required=True, help="Identifiant de la tâche à modifier"
    )
    parser_edit.add_argument("--title", help="Nouveau titre de la tâche")
    parser_edit.add_argument("--desc", help="Nouvelle description de la tâche")
    parser_edit.add_argument(
        "--priority", type=int, help="Nouvelle priorité de la tâche"
    )
    parser_edit.add_argument(
        "--due", help="Nouvelle date d'échéance de la tâche (format YYYY-MM-DD)"
    )

    args = parser.parse_args()

    # Chargement des tâches existantes depuis le fichier JSON
    tasks = load_tasks(DEFAULT_FILENAME)

    if args.version:
        print("Version 1.0")
    elif args.command == "add":
        print("Ajout de la tâche :")
        print(f"  Titre       : {args.title}")
        if args.desc is not None:
            print(f"  Description : {args.desc}")
        print(f"  Priorité    : {args.priority}")
        if args.due is not None:
            print(f"  Date d'échéance : {args.due}")
        # Création de la nouvelle tâche sans ID initialement
        nouvelle_tache = Tache(args.title, args.desc, args.priority, args.due)
        # Génération d'un ID unique et affectation à la tâche
        nouvelle_tache.id = generate_unique_id(tasks)
        tasks.append(nouvelle_tache)
        save_tasks(tasks)
        print(
            f"Tâche ajoutée avec l'ID {nouvelle_tache.id} et sauvegardée dans tasks.json."
        )
    elif args.command == "remove":
        task_id = int(args.id)
        # Recherche de la tâche à supprimer par son ID
        task_to_remove = None
        for task in tasks:
            if task.id == task_id:
                task_to_remove = task
                break
        if task_to_remove:
            tasks.remove(task_to_remove)
            save_tasks(tasks)
            print(f"Tâche avec l'ID {task_id} supprimée.")
        else:
            print(f"Aucune tâche trouvée avec l'ID {task_id}.")
    elif args.command == "list":
        print("Affichage de la liste des tâches")
        if args.sort:
            print(f"Tri par : {args.sort}")
            if args.sort == "title":
                tasks.sort(key=lambda x: x.titre)
            elif args.sort == "priority":
                tasks.sort(key=lambda x: x.priorite)
            elif args.sort == "due":
                tasks.sort(key=lambda x: x.date_limite or "")
        # Affichage de toutes les tâches
        for task in tasks:
            print(task)
            print("-" * 40)
    elif args.command == "edit":
        task_id = int(args.id)
        # Recherche de la tâche à modifier par son ID
        task_to_edit = None
        for task in tasks:
            if task.id == task_id:
                task_to_edit = task
                break
        if task_to_edit:
            if args.title is not None:
                task_to_edit.set_titre(args.title)
            if args.desc is not None:
                task_to_edit.set_description(args.desc)
            if args.priority is not None:
                task_to_edit.set_priorite(args.priority)
            if args.due is not None:
                task_to_edit.set_date_limite(args.due)
            save_tasks(tasks)
            print(f"Tâche avec l'ID {task_id} mise à jour.")
        else:
            print(f"Aucune tâche trouvée avec l'ID {task_id}.")
    else:
        print(ERROR_MESSAGE)


if __name__ == "__main__":
    main()
