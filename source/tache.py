class Tache:
    def __init__(self, titre, description=None, priorite=1, date_limite=None):
        # Le titre est obligatoire
        self.titre = titre
        self.description = description
        # On vérifie que la priorité est au moins égale à 1 (si inférieure, on fixe à 1)
        self.priorite = priorite if priorite >= 1 else 1
        self.date_limite = date_limite

    # Getter et setter pour le titre
    def get_titre(self):
        return self.titre

    def set_titre(self, nouveau_titre):
        self.titre = nouveau_titre

    # Getter et setter pour la description
    def get_description(self):
        return self.description

    def set_description(self, nouvelle_description):
        self.description = nouvelle_description

    # Getter et setter pour la priorité
    def get_priorite(self):
        return self.priorite

    def set_priorite(self, nouvelle_priorite):
        if nouvelle_priorite < 1:
            self.priorite = 1
        else:
            self.priorite = nouvelle_priorite

    # Getter et setter pour la date limite
    def get_date_limite(self):
        return self.date_limite

    def set_date_limite(self, nouvelle_date_limite):
        self.date_limite = nouvelle_date_limite

    # Méthode d'affichage pour faciliter la visualisation d'une tâche
    def __str__(self):
        return (f"Tâche: {self.titre}\n"
                f"Description: {self.description}\n"
                f"Priorité: {self.priorite}\n"
                f"Date limite: {self.date_limite}")

    # --- Méthodes d'aide pour la sérialisation JSON ---
    def to_dict(self):
        """
        Renvoie un dictionnaire représentant la tâche,
        pratique pour la sérialisation en JSON.
        """
        return {
            "titre": self.titre,
            "description": self.description,
            "priorite": self.priorite,
            "date_limite": self.date_limite
        }

    @classmethod
    def from_dict(cls, tache_dict):
        """
        Reconstruit un objet Tache à partir d'un dictionnaire.
        """
        return cls(
            titre=tache_dict["titre"],
            description=tache_dict.get("description"),
            priorite=tache_dict.get("priorite", 1),
            date_limite=tache_dict.get("date_limite")
        )