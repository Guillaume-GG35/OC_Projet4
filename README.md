# OC-Projet4 : Développez un programme logiciel en Python.

Ce programme permet la gestion de tournois d'échecs.<br>
<br>
> [!NOTE]
> Testé sous Ubuntu 24.10 - Python 3.12.7

## Prérequis

Pour installer ce programme, vous aurez besoin d'une connexion internet. Le programme est ensuite exécuté en local et ne nécessite pas de connexion internet pour fonctionner.<br>
<br>
Python doit être installé sur votre ordinateur (version 3.12.7 ou supérieur).<br>
<br>
L'installateur **pip** doit également être disponible sur votre machine pour installer les dépendances.

## Installation et exécution du programme

<details>
<summary>Etape 1 - Installer git</summary><br>

Pour télécharger ce programme, vérifiez que git est bien installé sur votre poste.<br>
Vous pouvez l'installer en suivant les instructions fournies sur le site [git-scm.com](https://git-scm.com/book/fr/v2/D%C3%A9marrage-rapide-Installation-de-Git)

</details>

<details>
<summary>Etape 2 - Cloner le dépôt contenant le programme</summary><br>


Utilisez la commande suivante :

``git clone https://github.com/Guillaume-GG35/OC-Projet4.git``

</details>

<details>
<summary>Etape 3 - Créer et activer un evironnement virtuel</summary><br>

Placez vous dans le dossier **OC_Projet4** et créez un environnement virtuel avec la commande<br>
``python -m venv env``<br>

Activez cet environnement avec la commande<br>
``source env/bin/activate``

</details>

<details>
<summary>Etape 4 - Installer les dépendances</summary><br>

Pour que ce programme s'exécute, vous aurez besoin de plusieurs packages additionnels listés dans le fichier requirements.txt.<br>

Exécutez la commande <br>
``pip install -r requirements.txt``

</details>

<details>
<summary>Etape 5 - Exécuter le programme</summary><br>

Exécutez la commande <br>
``python main.py``

</details>

## Fontionnement du programme

Le programme comporte un menu principal suivi de plusieurs sous-menus :<br>
<br>
MENU PRINCIPAL<br>
1- Joueurs<br>
2- Tournois<br>
3- Rapports<br>
0- Quitter<br>
<br><br>
1- Le menu **Joueurs** permet de :
- Créer un nouveau joueur
- Afficher les informations d'un joueur
<br><br>

2- Le menu **Tournois** permet de :
- Préparer un nouveau tournoi
- Afficher les informations d'un tournoi
- Débuter un tournoi préparé
- Afficher les tournois en cours
- Reprendre un tournoi en cours
<br><br>

3- Le menu **Rapports** permet de :
- Afficher la liste des joueurs
- Afficher la liste des tournois
- Afficher le nom et la date d'un tournoi
- Afficher la liste des joueurs d'un tournoi
- Afficher la liste des tours et des matchs d'un tournoi
<br><br>

Les menus sont navigables en tapant le chiffre de l'action correspondante suivi de la touche entrée pour valider le choix.<br>
<br>
> [!NOTE]
> Lors de la première exécution du programme, un message indiquera que la base de données est vide. Ceci est un comportement normal.

## Générer un rapport avec flake8-html

Il est possible de générer des rapports avec flake8 au format HTML.<br>
Pour ceci, entrez les commandes suivante depuis le répertoire **OC_Projet4** :<br>

Activer l'environnement virtuel :<br>
``source env/bin/activate``

Lancer la commande pour générer le rapport :<br>
``flake8``

Un dossier **flake8_rapport** sera créé dans le dossier **OC_Projet4**.<br>
Pour afficher le rapport, ouvrir le fichier index.html
