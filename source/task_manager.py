#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Module task_manager.

Ce module fournit une interface en ligne de commande (CLI) pour la gestion d'une liste de tâches.

Fonctionnalités:
    - Chargement et sauvegarde des tâches depuis/vers un fichier JSON.
    - Ajout d'une nouvelle tâche, avec génération d'un identifiant unique.
    - Suppression d'une tâche existante par son identifiant.
    - Affichage de la liste des tâches, avec possibilité de tri par titre,\
          priorité ou date d'échéance.
    - Modification d'une tâche existante (édition).

Les tâches sont représentées par des instances de la classe Tache,\
      définie dans le module source.tache.
Les messages affichés à l'utilisateur sont centralisés dans le module source.textes.
"""

import argparse
import json
import random
from source.tache import Tache  # Importation de la classe Tache depuis tache.py
from source.textes import WELCOME_MESSAGE, ERROR_MESSAGE

DEFAULT_FILENAME = "tasks.json"  # Nom par défaut du fichier de sauvegarde des tâches


def load_tasks(filename):
    """Charge les tâches depuis un fichier JSON et retourne une liste d'objets Tache.

    Si le fichier n'existe pas ou en cas d'erreur de décodage, une liste vide est retournée.

    Args:
        filename (str): Chemin du fichier JSON contenant les tâches.

    Returns:
        list[Tache]: Liste d'instances de Tache.
    """
    try:
        with open(filename, "r", encoding="utf-8") as file:
            tasks_data = json.load(file)
        # Reconstruction des objets Tache à partir des dictionnaires
        return [Tache.from_dict(item) for item in tasks_data]
    except FileNotFoundError:
        return []
    except json.JSONDecodeError:
        print("Erreur lors du décodage du fichier JSON.")
        return []


def save_tasks(tasks, filename=DEFAULT_FILENAME):
    """Sauvegarde une liste d'objets Tache dans un fichier JSON.

    Chaque objet Tache est converti en dictionnaire avant d'être sauvegardé.

    Args:
        tasks (list[Tache]): Liste des tâches à sauvegarder.
        filename (str, optional): Chemin du fichier JSON de sauvegarde.\
              Defaults to DEFAULT_FILENAME.
    """
    tasks_data = [task.to_dict() for task in tasks]
    with open(filename, "w", encoding="utf-8") as file:
        json.dump(tasks_data, file, ensure_ascii=False, indent=4)


def generate_unique_id(tasks):
    """Génère un identifiant unique à 6 chiffres non utilisé parmi les tâches existantes.

    Args:
        tasks (list[Tache]): Liste des tâches existantes.

    Returns:
        int: Un identifiant unique.
    """
    existing_ids = {task.id for task in tasks if task.id is not None}
    while True:
        candidate = random.randint(100000, 999999)
        if candidate not in existing_ids:
            return candidate


def handle_add(args, tasks):
    """Ajoute une nouvelle tâche.

    Affiche les informations de la tâche à ajouter,\
          crée une instance de Tache avec un identifiant unique,
    ajoute la tâche à la liste et sauvegarde la liste dans le fichier JSON par défaut.

    Args:
        args: Arguments de la ligne de commande contenant les détails de la tâche.
        tasks (list[Tache]): Liste des tâches existantes.
    """
    print("Ajout de la tâche :")
    print(f"  Titre       : {args.title}")
    if args.desc is not None:
        print(f"  Description : {args.desc}")
    print(f"  Priorité    : {args.priority}")
    if args.due is not None:
        print(f"  Date d'échéance : {args.due}")
    nouvelle_tache = Tache(args.title, args.desc, args.priority, args.due)
    nouvelle_tache.id = generate_unique_id(tasks)
    tasks.append(nouvelle_tache)
    save_tasks(tasks)
    print(
        f"Tâche ajoutée avec l'ID {nouvelle_tache.id} et sauvegardée dans {DEFAULT_FILENAME}."
    )


def handle_remove(args, tasks):
    """Supprime une tâche en recherchant par identifiant.

    Args:
        args: Arguments de la ligne de commande contenant l'identifiant de la tâche à supprimer.
        tasks (list[Tache]): Liste des tâches existantes.
    """
    task_id = int(args.id)
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


def handle_list(args, tasks):
    """Affiche la liste des tâches, avec un tri optionnel.

    Args:
        args: Arguments de la ligne de commande pouvant inclure l'option de tri.
        tasks (list[Tache]): Liste des tâches existantes.
    """
    print("Affichage de la liste des tâches")
    if args.sort:
        print(f"Tri par : {args.sort}")
        if args.sort == "title":
            tasks.sort(key=lambda x: x.titre)
        elif args.sort == "priority":
            tasks.sort(key=lambda x: x.priorite)
        elif args.sort == "due":
            tasks.sort(key=lambda x: x.date_limite or "")
    for task in tasks:
        print(task)
        print("-" * 40)


def handle_edit(args, tasks):
    """Modifie une tâche existante en recherchant par identifiant.

    Args:
        args: Arguments de la ligne de commande contenant les modifications à apporter à la tâche.
        tasks (list[Tache]): Liste des tâches existantes.
    """
    task_id = int(args.id)
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


def main():
    """Point d'entrée principal de l'application CLI.

    Configure l'analyse des arguments de la ligne de commande et délègue l'exécution
    de la commande à la fonction correspondante.
    """
    print(WELCOME_MESSAGE)

    parser = argparse.ArgumentParser(
        description="Une application CLI simple.",
        formatter_class=argparse.RawTextHelpFormatter,
    )

    subparsers = parser.add_subparsers(
        dest="command",
        title="Commandes disponibles",
        help="Choisissez une commande à exécuter",
    )

    # Configuration de la commande "add"
    parser_add = subparsers.add_parser("add", help="Ajoute une tâche à la liste")
    parser_add.add_argument("--title", required=True, help="Titre de la tâche")
    parser_add.add_argument("--desc", help="Description de la tâche")
    parser_add.add_argument(
        "--priority", type=int, default=1, help="Priorité de la tâche (défaut: 1)"
    )
    parser_add.add_argument(
        "--due", help="Date d'échéance de la tâche (format YYYY-MM-DD)"
    )
    parser_add.set_defaults(func=handle_add)

    # Configuration de la commande "remove"
    parser_remove = subparsers.add_parser(
        "remove", help="Supprime une tâche de la liste"
    )
    parser_remove.add_argument(
        "--id", required=True, help="Identifiant de la tâche à supprimer"
    )
    parser_remove.set_defaults(func=handle_remove)

    # Configuration de la commande "list"
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
    parser_list.set_defaults(func=handle_list)

    # Configuration de la commande "edit"
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
    parser_edit.set_defaults(func=handle_edit)

    args = parser.parse_args()

    # Chargement des tâches depuis le fichier JSON
    tasks = load_tasks(DEFAULT_FILENAME)

    if hasattr(args, "func"):
        args.func(args, tasks)
    else:
        print(ERROR_MESSAGE)


if __name__ == "__main__":
    main()
