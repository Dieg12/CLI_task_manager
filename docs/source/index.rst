CLI_TASK_MANAGER Documentation
==============================

Bienvenue dans la documentation de l'application CLI_TASK_MANAGER.
Cette documentation décrit en détail les modules suivants :

- **Module Tache** : Gestion de la classe Tache et de ses méthodes.
- **Module Task Manager** : Interface en ligne de commande pour la gestion des tâches.

.. toctree::
   :maxdepth: 2
   :caption: Sommaire :

   modules

Module Tache
============

Ce module définit la classe **Tache** qui représente une tâche avec ses attributs (titre, description, priorité, date d'échéance et identifiant) ainsi que ses méthodes associées (getters, setters, sérialisation et affichage).

.. automodule:: source.tache
    :members:
    :undoc-members:
    :show-inheritance:

Module Task Manager
===================

Ce module offre une interface en ligne de commande pour manipuler les tâches.  
Il propose notamment les fonctionnalités suivantes :

- Chargement et sauvegarde des tâches via un fichier JSON.
- Ajout d'une nouvelle tâche avec génération automatique d'un identifiant unique.
- Suppression d'une tâche existante.
- Affichage de la liste des tâches avec options de tri.
- Modification des tâches existantes.

.. automodule:: source.task_manager
    :members:
    :undoc-members:
    :show-inheritance:

Indices et tables
=================
* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
