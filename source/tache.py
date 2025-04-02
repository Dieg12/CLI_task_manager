#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Module tache.

Ce module définit la classe Tache qui représente une tâche avec les attributs suivants :
    - titre : str (obligatoire)
    - description : str ou None
    - priorite : int (au minimum 1)
    - date_limite : str ou None
    - id : int ou None

Les méthodes associées permettent la manipulation et la sérialisation des tâches.
"""

class Tache:
    """
    Classe représentant une tâche.

    :param titre: Le titre de la tâche (obligatoire).
    :type titre: str
    :param description: La description de la tâche, défaut None.
    :type description: str or None
    :param priorite: La priorité de la tâche (doit être au moins 1), défaut 1.
    :type priorite: int
    :param date_limite: La date limite de la tâche, par exemple au format YYYY-MM-DD.
    :type date_limite: str or None
    :param id: L'identifiant unique de la tâche, défaut None.
    :type id: int or None
    """

    def __init__(self, titre, description=None, priorite=1, date_limite=None, id=None):
        """
        Initialise une nouvelle instance de Tache.

        :param titre: Le titre de la tâche (obligatoire).
        :param description: La description de la tâche, défaut None.
        :param priorite: La priorité de la tâche, doit être au moins 1, défaut 1.
        :param date_limite: La date limite de la tâche, par exemple au format YYYY-MM-DD.
        :param id: L'identifiant unique de la tâche, défaut None.
        """
        self.titre = titre
        self.description = description
        # On vérifie que la priorité est au moins égale à 1 (si inférieure, on fixe à 1)
        self.priorite = priorite if priorite >= 1 else 1
        self.date_limite = date_limite
        self.id = id  # Attribut pour l'identifiant unique de la tâche

    def get_titre(self):
        """
        Retourne le titre de la tâche.

        :return: Le titre de la tâche.
        :rtype: str
        """
        return self.titre

    def set_titre(self, nouveau_titre):
        """
        Met à jour le titre de la tâche.

        :param nouveau_titre: Le nouveau titre.
        :type nouveau_titre: str
        """
        self.titre = nouveau_titre

    def get_description(self):
        """
        Retourne la description de la tâche.

        :return: La description de la tâche.
        :rtype: str or None
        """
        return self.description

    def set_description(self, nouvelle_description):
        """
        Met à jour la description de la tâche.

        :param nouvelle_description: La nouvelle description.
        :type nouvelle_description: str
        """
        self.description = nouvelle_description

    def get_priorite(self):
        """
        Retourne la priorité de la tâche.

        :return: La priorité de la tâche.
        :rtype: int
        """
        return self.priorite

    def set_priorite(self, nouvelle_priorite):
        """
        Met à jour la priorité de la tâche.
        Si la nouvelle priorité est inférieure à 1, elle est fixée à 1.

        :param nouvelle_priorite: La nouvelle priorité.
        :type nouvelle_priorite: int
        """
        if nouvelle_priorite < 1:
            self.priorite = 1
        else:
            self.priorite = nouvelle_priorite

    def get_date_limite(self):
        """
        Retourne la date limite de la tâche.

        :return: La date limite de la tâche.
        :rtype: str or None
        """
        return self.date_limite

    def set_date_limite(self, nouvelle_date_limite):
        """
        Met à jour la date limite de la tâche.

        :param nouvelle_date_limite: La nouvelle date limite, par exemple au format YYYY-MM-DD.
        :type nouvelle_date_limite: str
        """
        self.date_limite = nouvelle_date_limite

    def __str__(self):
        """
        Retourne une représentation en chaîne de caractères de la tâche.

        :return: Une chaîne de caractères décrivant la tâche.
        :rtype: str
        """
        return (
            f"Tâche ID: {self.id}\n"
            f"Titre: {self.titre}\n"
            f"Description: {self.description}\n"
            f"Priorité: {self.priorite}\n"
            f"Date limite: {self.date_limite}"
        )

    def to_dict(self):
        """
        Convertit la tâche en un dictionnaire, pratique pour la sérialisation en JSON.

        :return: Un dictionnaire représentant la tâche.
        :rtype: dict
        """
        return {
            "id": self.id,
            "titre": self.titre,
            "description": self.description,
            "priorite": self.priorite,
            "date_limite": self.date_limite,
        }

    @classmethod
    def from_dict(cls, tache_dict):
        """
        Reconstruit une instance de Tache à partir d'un dictionnaire.

        :param tache_dict: Dictionnaire contenant les attributs d'une tâche.
        :type tache_dict: dict
        :return: Une instance de Tache.
        :rtype: Tache
        """
        return cls(
            titre=tache_dict["titre"],
            description=tache_dict.get("description"),
            priorite=tache_dict.get("priorite", 1),
            date_limite=tache_dict.get("date_limite"),
            id=tache_dict.get("id"),
        )
