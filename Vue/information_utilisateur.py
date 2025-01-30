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
            liste_joueurs = interactions_controleur_modele.rechercher_liste_joueurs(DB, id_joueurs)
            print()
            CONSOLE.print(
                "[bold yellow]Identifiant : [/bold yellow]",
                f"[bold white]{donnees['identifiant']}\n[/bold white]",
                "[bold yellow]Nom du tournoi :[/bold yellow]",
                f"[bold white]{donnees['nom']}\n[/bold white]",
                "[bold yellow]Lieu :[/bold yellow]",
                f"[bold white]{donnees['lieu']}\n[/bold white]",
                "[bold yellow]Date de début :[/bold yellow]",
                f"[bold white]{donnees['date_debut']}\n[/bold white]",
                "[bold yellow]Date de fin :[/bold yellow]",
                f"[bold white]{donnees['date_fin']}\n[/bold white]",
                "[bold yellow]Nombre de tours :[/bold yellow]",
                f"[bold white]{donnees['nombre_tours']}\n[/bold white]",
                "[bold yellow]Liste des participants :[/bold yellow]",
            )

            for joueur in liste_joueurs:
                CONSOLE.print(
                    f"[bold white]{joueur['identifiant']} [/bold white]",
                    f"[bold white]- {joueur['nom']} [/bold white]",
                    f"[bold white]{joueur['prenom']} [/bold white]",
                    f"[bold white]- {joueur['date_naissance']}[/bold white]",
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
        f"[white]{prenom_joueur} {nom_joueur} [/white]",
        f"[white]({id_joueur}) est exempté pour ce tour.[/white]",
    )
    CONSOLE.print("[white]1 point lui est attribué en compensation.[/white]", end="\n\n")


def annonce_match(joueur1, joueur2, no_match):
    CONSOLE.print(
        f"[white]Le Match n°{no_match} oppose [/white]",
        f"[white bold]{joueur1.prenom} {joueur1.nom} [/white bold]",
        f"[white bold]({joueur1.identifiant})[/white bold]",
        f"[white]et [bold]{joueur2.prenom} [/white][/bold]",
        f"[white bold]{joueur2.nom} ({joueur2.identifiant})[/white bold]",
    )


def fin_tour(nom):
    CONSOLE.print(f"Le {nom} est terminé !", style="bold green")


def tournoi_termine(id_tournoi, nom_tournoi):
    CONSOLE.print(
        f"[bold cyan]Le tournoi '{id_tournoi} [/bold cyan]",
        f"[bold cyan]- {nom_tournoi}' est terminé ![/bold cyan]",
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

        case "rapport_tournoi":
            print()
            CONSOLE.print(
                f"[bold green]- {element[0]} - [/bold green]",
                f"[bold green]début : {element[1]} - [/bold green]",
                f"[bold green]fin : {element[2]}[/bold green]",
            )

        case "matchs":
            CONSOLE.print(
                f"  [bold yellow]- Match n°{element[0]} - [/bold yellow]",
                "[bold cyan]Joueur 1 : [/bold cyan]",
                f"[bold white]{element[1]}[/bold white] - ",
                "[bold cyan]Joueur 2 : [/bold cyan]",
                f"[bold white]{element[2]}[/bold white] - ",
                "[bold cyan]Gagnant : [/bold cyan]",
                f"[bold white]{element[3]}[/bold white]",
            )


def afficher_donnees_tournoi(nom_tournoi, date_tournoi):
    if date_tournoi == "":
        date_tournoi = "Ce tournoi n'a pas commencé."

    CONSOLE.print(f"[bold white]- {nom_tournoi} : {date_tournoi}[/bold white]")


def texte_liste_disponible(element):
    print()
    CONSOLE.print(f"[bold cyan]Liste des {element} disponibles :[/bold cyan]")


def afficher_nombre_matchs(nb_matchs):
    CONSOLE.print(
        f"{nb_matchs} matchs seront nécessaires pour que tout les joueurs s'affrontent une fois.", style="bold yellow"
    )


def afficher_nombre_tours(nb_tours):
    CONSOLE.print(f"Le nombre de tours conseillés est de {nb_tours} tours.", style="bold yellow")
    CONSOLE.print("ATTENTION :", style="bold yellow")
    CONSOLE.print(
        "L'algorithme d'appariements peut afficher des résultats inattendus si une valeur différente est entrée.",
        style="bold yellow",
    )


def rapport_exporte(nom_fichier):
    CONSOLE.print(f"\nLe rapport [bold cyan]{nom_fichier}[/bold cyan] a été créé.", style="bold green")
