# 🕹️ Pac-Man Python 

Un clone du célèbre jeu **Pac-Man**, développé intégralement en Python avec la bibliothèque **Pygame**. 

## 🌟 Points Forts du Projet

* **Architecture Modulaire** : Code divisé en plusieurs fichiers (`main`, `pacman`, `ghost`, `constants`) pour une maintenance facilitée.
* **Système de Fruits Authentique** : Gestion dynamique de 8 types de bonus (Cerise, Fraise, Orange, Pomme, Melon, Galboss, Cloche, Clé) apparaissant selon le niveau.
* **UX & Game Design** :
    * Gestion d'états de jeu : `READY`, `PLAY`, `PAUSE`, `GAMEOVER`.
    * Double système de pause (touches **P** ou **Espace**).
    * Positionnement précis des entités au pixel près.
* **Graphismes Procéduraux** : Tous les designs (personnages et fruits) sont générés par code via les primitives de dessin de Pygame.

## 📂 Structure du Dépôt

Le projet est organisé comme suit pour garantir une lecture claire du code :

* **main.py** : Point d'entrée, gestion de la boucle de jeu et des états.
* **pacman.py** : Classe gérant les mouvements, l'animation et les collisions du joueur.
* **ghost.py** : Gestion des comportements et de la vulnérabilité des fantômes.
* **constants.py** : Configuration du labyrinthe, des couleurs et des variables globales.

## 🛠️ Installation et Lancement

### Prérequis
Vous devez disposer de **Python 3.x** installé sur votre machine.

### Installation de Pygame
Installez la bibliothèque nécessaire via le terminal :
```bash
pip install pygame
```

### Lancer le jeu

Exécutez simplement la commande suivante :

Bash

  

python main.py

## 📦 Distribution (Version .exe)

Le projet est prêt pour le déploiement. Pour générer une version installable sur Windows sans installation de Python requise :

1.  Installez PyInstaller : `pip install pyinstaller`
2.  Compilez : `pyinstaller --noconsole --onefile main.py`

L'exécutable se trouvera dans le dossier `/dist`.

## 🎮 Commandes du Jeu

-   **Flèches directionnelles** : Déplacer Pac-Man
-   **Touche Espace** : Mettre le jeu en pause / Reprendre
-   **Touche Espace** : Recommencer la partie (après un Game Over)
