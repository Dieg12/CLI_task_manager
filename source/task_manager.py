import argparse
from textes import WELCOME_MESSAGE, ERROR_MESSAGE


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
    parser_remove = subparsers.add_parser(
        "remove", help="Supprime une tâche de la liste"
    )
    parser_remove.add_argument(
        "--id", required=True, help="Identifiant de la tâche à supprimer"
    )

    # Commande 'liste' : Affiche la liste des tâches
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

    # Traitement des commandes en fonction des arguments
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

    elif args.command == "remove":
        # À compléter : appel de la fonction de suppression de tâche
        print("Suppression de la tâche avec l'ID :", args.id)
    elif args.command == "list":
        # À compléter : appel de la fonction d'affichage de la liste des tâches
        print("Affichage de la liste des tâches")
        if args.sort:
            print(f"Tri par : {args.sort}")
    else:
        print(ERROR_MESSAGE)


if __name__ == "__main__":
    main()
