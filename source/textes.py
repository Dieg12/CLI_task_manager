# cli_texts.py

WELCOME_MESSAGE = "Bienvenue dans l'application CLI !"
HELP_TEXT = """
Usage : python task_manager.py [options]

Options :
  -h, --help    Affiche ce message d'aide

  add           Ajoute une tâche à la liste
    --title     Titre de la tâche
    --desc      Description de la tâche
    --priority  Priorité de la tâche
    --due       Date d'échéance de la tâche

  remove       Supprime une tâche de la liste
    --id        Identifiant de la tâche à supprimer

  liste        Affiche la liste des tâches
    --sort      Trier la liste par priorité ou date d'échéance
      title     Trier par titre
      priority  Trier par priorité
      due       Trier par date d'échéance
"""

ERROR_MESSAGE = "Une erreur est survenue. Veuillez réessayer."
