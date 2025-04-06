# CLI_task_manager 📝

CLI_task_manager est une application en ligne de commande conçue pour vous aider à gérer facilement vos tâches quotidiennes. Grâce à une interface simple et intuitive, vous pouvez ajouter, supprimer, lister et modifier vos tâches directement depuis le terminal !

---

## 🚀 Fonctionnalités

- **Ajout de tâches** : Créez de nouvelles tâches avec un identifiant unique.
- **Suppression de tâches** : Supprimez une tâche existante en spécifiant son identifiant.
- **Liste des tâches** : Affichez la liste de toutes vos tâches avec des options de tri par titre, priorité ou date d'échéance.
- **Modification de tâches** : Éditez les détails d'une tâche existante.
- **Sauvegarde en JSON** : Toutes vos tâches sont sauvegardées dans un fichier JSON pour une persistance facile.

---

## ⚙️ Utilisation

Lancez l'application via la ligne de commande. Voici quelques exemples de commandes :

- **Ajouter une tâche** :
   ```bash
   python -m source.task_manager add --title "Acheter du pain" --desc "Acheter du pain à la boulangerie" --priority 2 --due "2025-04-10"
   ```

- **Lister les tâches** :
   ```bash
   python -m source.task_manager list --sort title
   ```

- **Supprimer une tâche** :
   ```bash
   python -m source.task_manager remove --id 123456
   ```

- **Modifier une tâche** :
   ```bash
   python -m source.task_manager edit --id 123456 --title "Acheter du pain complet" --priority 3
   ```

---

## 📚 Documentation

La documentation complète est générée avec **Sphinx**.

Elle est déployée automatiquement sur GitHub pages : https://dieg12.github.io/CLI_task_manager/ 

1. **Générer la documentation** :
   ```bash
   sphinx-build -M html ./docs/source ./build --fail-on-warning
   ```
2. **Consulter la documentation** :
   Ouvrez le fichier `build/html/index.html` dans votre navigateur.

---

## 🗂 Structure du Projet

- **`source.task_manager.py`** : Le module principal pour l'interface CLI.
- **`source.tache.py`** : Définit la classe `Tache` qui représente une tâche.
- **`source.textes.py`** : Contient les messages affichés à l'utilisateur.
- **`docs/`** : Contient la configuration et les sources de la documentation générée par Sphinx.

---

## 📄 Licence

Ce projet est entièrement libre de toute utilisation.

---

N'hésitez pas à ouvrir des issues si vous avez des questions ou des suggestions. Bonne utilisation et bonne gestion de vos tâches ! 🎉

## ✍️ Auteur

Projet réalisé dans le cadre du bachelor CSI

📅 Année : 2025  
👨‍🎓 Étudiant : Diego Iglesias 
🏫 Établissement : Campus XIIe Avenue