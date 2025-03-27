import argparse
import json
import datetime
from tache import Tache
from textes import WELCOME_MESSAGE, ERROR_MESSAGE

def load_tasks(filename="tasks.json"):
    """
    Charge les tâches depuis un fichier JSON et retourne une liste d'objets Tache.
    Si le fichier n'existe pas ou en cas d'erreur de lecture, retourne une liste vide.
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
    """
    # Conversion de chaque objet Tache en dictionnaire
    tasks_data = [task.to_dict() for task in tasks]
    with open(filename, "w", encoding="utf-8") as file:
        json.dump(tasks_data, file, ensure_ascii=False, indent=4)

def main():
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
    parser_remove = subparsers.add_parser("remove", help="Supprime une tâche de la liste")
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

    args = parser.parse_args()

    # Exemple d'intégration : on charge d'abord les tâches existantes
    tasks = load_tasks()

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
        # Création et ajout de la nouvelle tâche
        nouvelle_tache = Tache(args.title, args.desc, args.priority, args.due)
        tasks.append(nouvelle_tache)
        save_tasks(tasks)
        print("Tâche ajoutée et sauvegardée dans tasks.json.")
    elif args.command == "remove":
        # Ici, vous devriez rechercher la tâche par son identifiant et la supprimer.
        print("Suppression de la tâche avec l'ID :", args.id)
        # Par exemple, en se basant sur une position dans la liste ou un attribut spécifique.
        # Puis sauvegarder la liste mise à jour :
        save_tasks(tasks)
    elif args.command == "list":
        print("Affichage de la liste des tâches")
        if args.sort:
            print(f"Tri par : {args.sort}")
            # Implémentez ici le tri en fonction de args.sort
        # Affichage de toutes les tâches
        for index, task in enumerate(tasks):
            print(f"ID: {index} -> {task}")
    else:
        print(ERROR_MESSAGE)


if __name__ == "__main__":
    # Chargement initial
    tasks = load_tasks()
    print("Tâches chargées :")
    for t in tasks:
        print(t)

    # Ajout d'une nouvelle tâche d'exemple
    print("\nAjout d'une nouvelle tâche d'exemple...")
    nouvelle_tache = Tache("Exemple 3", "Ceci est une tâche d'exemple", priorite=-4, date_limite=str(datetime.datetime(2025, 3, 29)))
    tasks.append(nouvelle_tache)

    # Sauvegarde des tâches mises à jour
    save_tasks(tasks)
    print("La nouvelle tâche a été ajoutée et sauvegardée.")
