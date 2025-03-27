import pytest
from source.tache import Tache
from source.task_manager import generate_unique_id


def test_creation_with_only_title():
    tache1 = Tache("Faire les courses")
    assert tache1.get_titre() == "Faire les courses", "Erreur sur le titre"
    assert tache1.get_priorite() == 1, "La priorité par défaut devrait être 1"
    assert tache1.description is None, "La description par défaut devrait être None"
    assert tache1.date_limite is None, "La date limite par défaut devrait être None"
    assert tache1.id is None, "L'id par défaut devrait être None"


def test_setters_and_getters():
    tache1 = Tache("Faire les courses")
    tache1.set_description("Acheter fruits, légumes et pain")
    tache1.set_priorite(3)
    tache1.set_date_limite("2025-03-05")
    assert (
        tache1.get_description() == "Acheter fruits, légumes et pain"
    ), "Erreur sur la description"
    assert tache1.get_priorite() == 3, "Erreur sur la priorité"
    assert tache1.get_date_limite() == "2025-03-05", "Erreur sur la date limite"


def test_priority_minimum():
    tache1 = Tache("Faire les courses")
    tache1.set_priorite(0)
    assert tache1.get_priorite() == 1, "La priorité ne doit pas être inférieure à 1"


def test_to_dict_from_dict():
    # Création d'une tâche avec un id défini
    tache1 = Tache("Test", "Test description", 5, "2025-01-01", id=123456)
    d = tache1.to_dict()
    expected = {
        "id": 123456,
        "titre": "Test",
        "description": "Test description",
        "priorite": 5,
        "date_limite": "2025-01-01",
    }
    assert d == expected, "La conversion en dictionnaire ne fonctionne pas comme prévu"

    # Reconstruction de la tâche à partir du dictionnaire
    tache2 = Tache.from_dict(d)
    assert tache2.get_titre() == "Test", "Erreur sur le titre reconstruit"
    assert (
        tache2.get_description() == "Test description"
    ), "Erreur sur la description reconstruit"
    assert tache2.get_priorite() == 5, "Erreur sur la priorité reconstruit"
    assert (
        tache2.get_date_limite() == "2025-01-01"
    ), "Erreur sur la date limite reconstruit"
    assert tache2.id == 123456, "L'id n'a pas été correctement reconstruit"


def test_str_representation():
    tache1 = Tache("Faire les courses", "Acheter du lait", 2, "2025-03-05", id=654321)
    rep = str(tache1)
    assert "Tâche ID: 654321" in rep, "La représentation en chaîne ne contient pas l'ID"
    assert (
        "Titre: Faire les courses" in rep
    ), "La représentation en chaîne ne contient pas le titre"


def test_generate_unique_id():
    # Créer une liste de tâches avec des IDs connus
    tache1 = Tache("Tâche 1", id=111111)
    tache2 = Tache("Tâche 2", id=222222)
    tasks = [tache1, tache2]
    new_id = generate_unique_id(tasks)
    assert new_id not in {
        111111,
        222222,
    }, "L'ID généré doit être unique par rapport aux tâches existantes"
    assert 100000 <= new_id <= 999999, "L'ID doit être un nombre à 6 chiffres"

    # Test de génération avec une liste vide
    tasks = []
    new_id = generate_unique_id(tasks)
    assert (
        100000 <= new_id <= 999999
    ), "L'ID doit être un nombre à 6 chiffres pour une liste vide"
