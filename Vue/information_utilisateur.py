#!/usr/bin/env python3

from Controleur.constantes import CONSOLE, DB
from Vue import message_erreur
from Controleur import interactions_controleur_modele


def afficher_infos(categorie, donnees):
    match categorie:
        case "joueur":
            print()
            CONSOLE.print(
                f"{donnees['nom']} {donnees['prenom']} ",
                f"- {donnees['date_naissance']}",
                style="bold cyan",
            )
        case "tournoi":
            id_joueurs = donnees["id_joueurs"]
            liste_joueurs = (
                interactions_controleur_modele.rechercher_liste_joueurs(
                    DB, id_joueurs
                )
            )
            print()
            CONSOLE.print(
                "[bold yellow]Identifiant : [/bold yellow]",
                f"[bold white]{donnees['identifiant']}\n[/bold white]",
                "[bold yellow]Nom du tournoi : [/bold yellow]",
                f"[bold white]{donnees['nom']}\n[/bold white]",
                "[bold yellow]Lieu : [/bold yellow]",
                f"[bold white]{donnees['lieu']}\n[/bold white]",
                "[bold yellow]Date de début : [/bold yellow]",
                f"[bold white]{donnees['date_debut']}\n[/bold white]",
                "[bold yellow]Date de fin : [/bold yellow]",
                f"[bold white]{donnees['date_fin']}\n[/bold white]",
                "[bold yellow]Nombre de tours : [/bold yellow]",
                f"[bold white]{donnees['nombre_tours']}\n[/bold white]",
                "[bold yellow]Liste des participants : [/bold yellow]",
            )
            for joueur in liste_joueurs:
                CONSOLE.print(
                    f"[bold white]{joueur['identifiant']} ",
                    f"- {joueur['nom']} {joueur['prenom']} ",
                    f"- {joueur['date_naissance']}[/bold white]",
                )
            CONSOLE.print(
                "[bold yellow]Description : [/bold yellow]",
                f"[bold white]{donnees['description']}[/bold white]\n\n",
            )


def liste_simple_tournois(liste_tournois):
    print()
    CONSOLE.print("[bold cyan]Liste des tournois disponibles :[/bold cyan]")
    if liste_tournois == []:
        message_erreur.liste_vide_tournois()
    else:
        for element in liste_tournois:
            CONSOLE.print(f"- {element["nom"]}")
    print()


def demande_suppr_db_tournoi(chemin_fichier):
    CONSOLE.print(f"Le fichier de données '{chemin_fichier}' existe déjà.")
    confirmation = input(
        "SI VOUS CONTINUEZ, DES DONNEES PEUVENT ETRE PERDUES.",
        " \n Continuer ? [O/n] :",
    )
    while confirmation != "O" and confirmation != "n":
        message_erreur.message_erreur_yes_No()
        confirmation = input(
            "SI VOUS CONTINUEZ, DES DONNEES PEUVENT ETRE PERDUES.",
            " \n Continuer ? [O/n] :",
        )
    return confirmation


def afficher_nom_round(nom_round):
    print()
    CONSOLE.print(f"[bold yellow]{nom_round}[/bold yellow]")


def joueur_exempte(nom_joueur, prenom_joueur, id_joueur):
    CONSOLE.print("[white]Un nombre impair de joueurs a été trouvé.[/white]")
    CONSOLE.print(
        f"[white]{prenom_joueur} {nom_joueur} ",
        f"({id_joueur}) est exempté pour ce tour.[/white]",
    )
    CONSOLE.print(
        "[white]1 point lui est attribué en compensation.[/white]", end="\n\n"
    )


def annonce_match(joueur1, joueur2, no_match):
    CONSOLE.print(
        f"[white]Le Match n°{no_match} oppose ",
        f"[bold]{joueur1.prenom} {joueur1.nom} ",
        f"({joueur1.identifiant})[/bold][/white]",
        f"[white]et [bold]{joueur2.prenom} ",
        f"{joueur2.nom} ({joueur2.identifiant})[/bold][/white]",
    )


def fin_tour(nom):
    CONSOLE.print(f"Le {nom} est terminé !", style="bold green")


def tournoi_termine(id_tournoi, nom_tournoi):
    CONSOLE.print(
        f"[bold cyan]Le tournoi '{id_tournoi} ",
        f"- {nom_tournoi}' est terminé ![/bold cyan]",
        end="\n\n",
    )


def classement_tournoi(classement):
    CONSOLE.print("CLASSEMENT", style="bold yellow")
    for element in classement:
        CONSOLE.print(f"[bold cyan]{element}[/bold cyan]")


def liste_elements(categorie):
    print()
    CONSOLE.print(f"Liste des {categorie} enregistrés :", style="bold cyan")


def afficher_element(categorie, element):
    match categorie:
        case "joueur":
            CONSOLE.print(f"- {element[0]} {element[1]}", style="bold")
        case "tournoi":
            CONSOLE.print(f"- {element}", style="bold")


def afficher_donnees_tournoi(nom_tournoi, date_tournoi):
    CONSOLE.print(f"[bold white]- {nom_tournoi} : {date_tournoi}[/bold white]")
