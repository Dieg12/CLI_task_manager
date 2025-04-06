#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Module tache.

Ce module définit la classe Tache qui représente une tâche avec les attributs suivants :

    titre (str): Le titre de la tâche (obligatoire).
    description (str or None): La description de la tâche.
    priorite (int): La priorité de la tâche (doit être au moins 1).
    date_limite (str or None): La date limite de la tâche (par exemple au format YYYY-MM-DD).
    id (int or None): L'identifiant unique de la tâche.

Les méthodes associées permettent la manipulation et la sérialisation des tâches.
"""
from dataclasses import dataclass, field


@dataclass
class Tache:
    """Représente une tâche avec ses attributs.

    Attributes:
        titre (str): Le titre de la tâche.
        description (str, optional): La description de la tâche. Defaults to None.
        priorite (int): La priorité de la tâche. Defaults to 1.
        date_limite (str, optional): La date limite de la tâche (format YYYY-MM-DD).\
              Defaults to None.
        task_id (int, optional): L'identifiant unique de la tâche. Defaults to None.
    """

    titre: str
    description: str = None
    priorite: int = field(default=1)
    date_limite: str = None
    task_id: int = None

    def __post_init__(self):
        """Assure la validité des données après l'initialisation.

        Vérifie que la priorité n'est pas inférieure à 1 et la corrige si nécessaire.
        """
        self.priorite = max(self.priorite, 1)

    def get_titre(self):
        """
        Retourne le titre de la tâche.

        Returns:
            str: Le titre de la tâche.
        """
        return self.titre

    def set_titre(self, nouveau_titre):
        """
        Met à jour le titre de la tâche.

        Args:
            nouveau_titre (str): Le nouveau titre.
        """
        self.titre = nouveau_titre

    def get_description(self):
        """
        Retourne la description de la tâche.

        Returns:
            str or None: La description de la tâche.
        """
        return self.description

    def set_description(self, nouvelle_description):
        """
        Met à jour la description de la tâche.

        Args:
            nouvelle_description (str): La nouvelle description.
        """
        self.description = nouvelle_description

    def get_priorite(self):
        """
        Retourne la priorité de la tâche.

        Returns:
            int: La priorité de la tâche.
        """
        return self.priorite

    def set_priorite(self, nouvelle_priorite):
        """
        Met à jour la priorité de la tâche.
        Si la nouvelle priorité est inférieure à 1, elle est fixée à 1.

        Args:
            nouvelle_priorite (int): La nouvelle priorité.
        """
        if nouvelle_priorite < 1:
            self.priorite = 1
        else:
            self.priorite = nouvelle_priorite

    def get_date_limite(self):
        """
        Retourne la date limite de la tâche.

        Returns:
            str or None: La date limite de la tâche.
        """
        return self.date_limite

    def set_date_limite(self, nouvelle_date_limite):
        """
        Met à jour la date limite de la tâche.

        Args:
            nouvelle_date_limite (str): La nouvelle date limite, par exemple au format YYYY-MM-DD.
        """
        self.date_limite = nouvelle_date_limite

    def __str__(self):
        """
        Retourne une représentation en chaîne de caractères de la tâche.

        Returns:
            str: Une chaîne de caractères décrivant la tâche.
        """
        return (
            f"Tâche ID: {self.task_id}\n"
            f"Titre: {self.titre}\n"
            f"Description: {self.description}\n"
            f"Priorité: {self.priorite}\n"
            f"Date limite: {self.date_limite}"
        )

    def to_dict(self):
        """
        Convertit la tâche en un dictionnaire, pratique pour la sérialisation en JSON.

        Returns:
            dict: Un dictionnaire représentant la tâche.
        """
        return {
            "task_id": self.task_id,
            "titre": self.titre,
            "description": self.description,
            "priorite": self.priorite,
            "date_limite": self.date_limite,
        }

    @classmethod
    def from_dict(cls, tache_dict):
        """
        Reconstruit une instance de Tache à partir d'un dictionnaire.

        Args:
            tache_dict (dict): Dictionnaire contenant les attributs d'une tâche.

        Returns:
            Tache: Une instance de Tache.
        """
        return cls(
            titre=tache_dict["titre"],
            description=tache_dict.get("description"),
            priorite=tache_dict.get("priorite", 1),
            date_limite=tache_dict.get("date_limite"),
            task_id=tache_dict.get("task_id"),
        )
