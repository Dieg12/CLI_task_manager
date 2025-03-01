from ..source.tache import Tache

def main():
    # Test de la création d'une tâche avec uniquement le titre
    print("Création d'une tâche avec uniquement le titre...")
    tache1 = Tache("Faire les courses")
    print(tache1)
    assert tache1.get_titre() == "Faire les courses", "Erreur sur le titre"
    assert tache1.get_priorite() == 1, "La priorité par défaut devrait être 1"

    # Test des setters et getters
    print("\nModification des attributs de la tâche...")
    tache1.set_description("Acheter fruits, légumes et pain")
    tache1.set_priorite(3)
    tache1.set_date_limite("2025-03-05")
    
    assert tache1.get_description() == "Acheter fruits, légumes et pain", "Erreur sur la description"
    assert tache1.get_priorite() == 3, "Erreur sur la priorité"
    assert tache1.get_date_limite() == "2025-03-05", "Erreur sur la date limite"

    print("Titre :", tache1.get_titre())
    print("Description :", tache1.get_description())
    print("Priorité :", tache1.get_priorite())
    print("Date limite :", tache1.get_date_limite())

    # Test de la validation de la priorité (priorité minimale)
    print("\nTest de la priorité minimale (on tente de définir une valeur inférieure à 1)...")
    tache1.set_priorite(0)
    assert tache1.get_priorite() == 1, "La priorité ne doit pas être inférieure à 1"
    print("Priorité après tentative de définir 0 :", tache1.get_priorite())

    print("\nTous les tests ont été passés avec succès.")

if __name__ == "__main__":
    main()
