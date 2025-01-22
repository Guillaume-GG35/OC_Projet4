#!/usr/bin/env python3

from constantes import CONSOLE, DB
from Vue import message_erreur
from Controleur import interactions_controleur_modele


def afficher_infos(categorie, donnees):
    match categorie:
        case "joueur":
            print()
            CONSOLE.print(
                f"{donnees['nom']} {donnees['prenom']} - {donnees['date_naissance']}",
                style="bold cyan",
            )
        case "tournoi":
            id_joueurs = donnees["id_joueurs"]
            liste_joueurs = interactions_controleur_modele.rechercher_liste_joueurs(
                DB, id_joueurs
            )
            print()
            CONSOLE.print(
                f"[bold yellow]Identifiant : [/bold yellow][bold white]{donnees['identifiant']}\n[/bold white]",
                f"[bold yellow]Nom du tournoi : [/bold yellow][bold white]{donnees['nom']}\n[/bold white]",
                f"[bold yellow]Lieu : [/bold yellow][bold white]{donnees['lieu']}\n[/bold white]",
                f"[bold yellow]Date de début : [/bold yellow][bold white]{donnees['date_debut']}\n[/bold white]",
                f"[bold yellow]Date de fin : [/bold yellow][bold white]{donnees['date_fin']}\n[/bold white]",
                f"[bold yellow]Nombre de tours : [/bold yellow][bold white]{donnees['nombre_tours']}\n[/bold white]",
                f"[bold yellow]Liste des participants : [/bold yellow]",
            )
            for joueur in liste_joueurs:
                CONSOLE.print(
                    f"[bold white]{joueur['identifiant']} - {joueur['nom']} {joueur['prenom']} - {joueur['date_naissance']}[/bold white]"
                )
            CONSOLE.print(
                f"[bold yellow]Description : [/bold yellow][bold white]{donnees['description']}[/bold white]\n\n"
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
        "SI VOUS CONTINUEZ, DES DONNEES PEUVENT ETRE PERDUES. \n Continuer ? [O/n] :"
    )
    while confirmation != "O" and confirmation != "n":
        message_erreur.message_erreur_yes_No()
        confirmation = input(
            "SI VOUS CONTINUEZ, DES DONNEES PEUVENT ETRE PERDUES. \n Continuer ? [O/n] :"
        )
    return confirmation


def afficher_nom_round(nom_round):
    print()
    CONSOLE.print(f"[bold yellow]{nom_round}[/bold yellow]")


def joueur_exempte(nom_joueur, prenom_joueur, id_joueur):
    CONSOLE.print(f"[white]Un nombre impair de joueurs a été trouvé.[/white]")
    CONSOLE.print(
        f"[white]{prenom_joueur} {nom_joueur} ({id_joueur}) est exempté pour ce tour.[/white]"
    )
    CONSOLE.print(
        "[white]1 point lui est attribué en compensation.[/white]", end="\n\n"
    )


def annonce_match(joueur1, joueur2, no_match):
    CONSOLE.print(
        f"[white]Le Match n°{no_match} oppose [bold]{joueur1.prenom} {joueur1.nom} ({joueur1.identifiant})[/bold][/white]",
        f"[white]et [bold]{joueur2.prenom} {joueur2.nom} ({joueur2.identifiant})[/bold][/white]",
    )


def fin_tour(nom):
    CONSOLE.print(f"Le {nom} est terminé !", style="bold green")


def tournoi_termine(id_tournoi, nom_tournoi):
    CONSOLE.print(
        f"[bold cyan]Le tournoi '{id_tournoi} - {nom_tournoi}' est terminé ![/bold cyan]",
        end="\n\n",
    )


def classement_tournoi(classement):
    CONSOLE.print("CLASSEMENT", style="bold yellow")
    for element in classement:
        CONSOLE.print(f"[bold cyan]{element}[/bold cyan]")
