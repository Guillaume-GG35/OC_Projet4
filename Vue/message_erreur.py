#!/usr/bin/env python3

from Controleur.constantes import CONSOLE


def json_introuvable(DB):
    CONSOLE.print(f"ATTENTION : le fichier '{DB}' est introuvable.", style="bold red")


def json_vide(DB):
    CONSOLE.print(f"ATTENTION : le fichier '{DB}' est vide.", style="bold red")


def erreur(type_donnee):
    match type_donnee:
        case "str":
            CONSOLE.print(
                "SAISIE INCORRECTE : Veuillez entrer uniquement des lettres.",
                end="\n\n",
                style="bold red",
            )
        case "num":
            CONSOLE.print(
                "SAISIE INCORRECTE : Veuillez entrer uniquement des chiffres.",
                end="\n\n",
                style="bold red",
            )
        case "NumOrEmpty":
            CONSOLE.print(
                "SAISIE INCORRECTE : Veuillez entrer uniquement des chiffres",
                "ou laisser vide pour valider la valeur par défaut.",
                end="\n\n",
                style="bold red",
            )
        case "StrOrNum":
            CONSOLE.print(
                "SAISIE INCORRECTE : Veuillez entrer des",
                "chiffres et des lettres.",
                end="\n\n",
                style="bold red",
            )
        case "StrNumOrEmpty":
            CONSOLE.print(
                "SAISIE INCORRECTE : Veuillez entrer des",
                "chiffres et des lettres ou laisser vide.",
                end="\n\n",
                style="bold red",
            )


def message_erreur_selection_menu(nombre_entrees):
    CONSOLE.print(
        "SAISIE INCORRECTE : Vous devez entrer un",
        f"chiffre compris entre 0 et {nombre_entrees}",
        end="\n\n",
        style="bold red",
    )


def message_erreur_date():
    CONSOLE.print("SAISIE INCORRECTE : Veuillez entrer une date au format JJ/MM/AAAA", style="bold red")


def message_erreur_yes_No():
    CONSOLE.print("Veuillez entrer 'o' pour oui ou 'N' pour non.", style="bold red")


def message_erreur_Yes_no():
    CONSOLE.print("Veuillez entrer 'O' pour oui ou 'n' pour non.", style="bold red")


def recherche_vide():
    CONSOLE.print(
        "Merci de vérifier votre saisie : Element introuvable.",
        style="bold red",
    )
    print()


def liste_vide_tournois():
    print()
    CONSOLE.print("Aucun tournoi à afficher", style="bold red")


def joueur_inexistant(id_joueur):
    CONSOLE.print(
        f"L'identifiant '{id_joueur}'",
        "n'est associé à aucun joueur enregistré.",
        style="bold red",
    )


def joueur_existant(id_joueur):
    CONSOLE.print(f"L'identifiant '{id_joueur}' est déjà enregistré.", style="bold red")


def tournoi_existant(nom_tournoi):
    CONSOLE.print(f"Le nom '{nom_tournoi}' est déjà attribué.", style="bold red")


def tournoi_deja_lance(id_tournoi):
    CONSOLE.print(
        f"[bold red]Le tournoi n°[yellow]{id_tournoi}[/yellow]",
        " est déjà commencé. Impossible d'ajouter un ",
        "nouveau joueur.[/bold red]",
    )


def lancer_tournoi_impossible(nom_tournoi):
    CONSOLE.print(
        f"Impossible de débuter '{nom_tournoi}'.",
        "Vérifiez les données du fichier de données existant ",
        "et utilisez le menu 'Chargement' pour reprendre le tournoi.",
        style="bold red",
    )


def erreur_saisie():
    CONSOLE.print("Saisie incorrecte", style="bold red")


def erreur_match():
    CONSOLE.print("Une erreur s'est produite durant l'appariement des joueurs.", style="bold red")
    CONSOLE.print("Le tournoi ne peut pas continuer.", style="bold red")


def choix_possibles(id_joueur1, id_joueur2):
    CONSOLE.print(f"Les choix possibles sont '{id_joueur1}' ou '{id_joueur2}'", style="bold red")


def fichier_existe():
    print()
    CONSOLE.print("Des fichiers de sauvegarde existent déjà.", style="bold red")


def fichiers_differents(fichier1, fichier2):
    print()
    CONSOLE.print(f"Les fichiers '{fichier1}' et '{fichier2}' sont différents.", style="bold red")


def avertissement_perte_donnees():
    CONSOLE.print("ATTENTION : SI VOUS CONTINUEZ, DES DONNEES IMPORTANTES PEUVENT ETRE PERDUES !", style="bold red")


def fichier_introuvable():
    CONSOLE.print("Il n'existe aucun fichier de sauvegarde à restaurer.", style="bold red")


def erreur_fichiers_sauvegarde():
    print()
    CONSOLE.print("Une erreur est survenue dans la lecture des fichiers de sauvegarde.", style="bold red")
    CONSOLE.print("Certains fichiers de données sont peut-être manquants.", style="bold red")
    CONSOLE.print("La sauvegarde du fichier 'data.json' est peut-être corrompue.", style="bold red")
