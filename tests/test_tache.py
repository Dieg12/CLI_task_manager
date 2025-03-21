import pytest
from source.tache import Tache

def test_creation_with_only_title():
    tache1 = Tache("Faire les courses")
    assert tache1.get_titre() == "Faire les courses", "Erreur sur le titre"
    assert tache1.get_priorite() == 1, "La priorité par défaut devrait être 1"

def test_setters_and_getters():
    tache1 = Tache("Faire les courses")
    tache1.set_description("Acheter fruits, légumes et pain")
    tache1.set_priorite(3)
    tache1.set_date_limite("2025-03-05")

    assert tache1.get_description() == "Acheter fruits, légumes et pain", "Erreur sur la description"
    assert tache1.get_priorite() == 3, "Erreur sur la priorité"
    assert tache1.get_date_limite() == "2025-03-05", "Erreur sur la date limite"

def test_priority_minimum():
    tache1 = Tache("Faire les courses")
    tache1.set_priorite(0)
    assert tache1.get_priorite() == 1, "La priorité ne doit pas être inférieure à 1"
