#!/usr/bin/env python3

""" VUE """

import controleur
from constantes import *

# Constante permettant la mise en forme des instructions print()
# grâce au paramètre "style"


class Menu:
    def __init__(self, liste_entrees_menu, nom_menu):

        # Mise en forme des éléments du menu
        nom_menu = str.upper(nom_menu)
        CONSOLE.print(f"\n{nom_menu}", style="bold yellow")
        self.nombre_entrees = len(liste_entrees_menu) - 1
        for element in liste_entrees_menu:
            CONSOLE.print(element, style="bold green")

    def get_choix(self):
        self.choix_utilisateur = input("Votre choix : ")
        return self.choix_utilisateur


def json_introuvable(DB):
    CONSOLE.print(f"ATTENTION : le fichier {DB} est introuvable.", style="bold red")


def json_vide(DB):
    CONSOLE.print(f"ATTENTION : le fichier {DB} est vide.", style="bold red")


def saisie_nouveau(categorie):

    match categorie:
        case "joueur":
            identifiant = saisie_utilisateur("identifiant", STR_OR_NUM)
            nom = saisie_utilisateur("nom", STRING)
            prenom = saisie_utilisateur("prénom", STRING)

            date_correcte = ""
            while not date_correcte:
                date_naissance = input(
                    "Entrez la date de naissance du nouveau joueur (JJ/MM/AAAA) : "
                )
                controleur.retour_menu(date_naissance)
                date_correcte = controleur.verifier_date(date_naissance)
                if not date_correcte:
                    CONSOLE.print(
                        "SAISIE INCORRECTE : Veuillez entrer une date au format JJ/MM/AAAA",
                        style="bold red",
                    )

            infos_joueur = {
                "nom": nom.upper(),
                "prenom": prenom,
                "date_naissance": date_naissance,
                "identifiant": identifiant,
            }
            return infos_joueur

        case "tournoi":

            identifiant = controleur.generer_id()
            nom = saisie_utilisateur("nom", STRING)
            lieu = saisie_utilisateur("lieu", STRING)
            nombre_tours = saisie_utilisateur(
                "nombre de tours (valeur par défaut = 4)", NUM_OR_EMPTY
            )
            nombre_tours = controleur.valider_nombre_tours(nombre_tours)
            id_joueurs = saisie_utilisateur("identifiants des joueurs", STR_OR_NUM)
            liste_joueurs = controleur.concat_id_joueurs(id_joueurs)
            description = saisie_utilisateur("description", STRING)

            infos_tournoi = {
                "identifiant": identifiant,
                "nom": nom,
                "lieu": lieu,
                "date_debut": "",
                "date_fin": "",
                "nombre_tours": nombre_tours,
                "id_joueurs": liste_joueurs,
                "description": description,
            }
            return infos_tournoi


def saisie_utilisateur(type_nom, type_donnee):
    while True:
        saisie_utilisateur = input(
            f"(* = Menu principal) Entrez l'information suivante - {str.upper(type_nom)} : "
        )
        controleur.retour_menu(saisie_utilisateur)
        if controleur.valider(saisie_utilisateur, type_donnee):
            return saisie_utilisateur
        else:
            message_erreur(type_donnee)


def message_erreur(type_donnee):
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
                "SAISIE INCORRECTE : Veuillez entrer uniquement des chiffres ou laisser vide pour valider la valeur par défaut.",
                end="\n\n",
                style="bold red",
            )
        case "StrOrNum":
            CONSOLE.print(
                "SAISIE INCORRECTE : Veuillez entrer des chiffres et des lettres.",
                end="\n\n",
                style="bold red",
            )
        case "StrNumOrEmpty":
            CONSOLE.print(
                "SAISIE INCORRECTE : Veuillez entrer des chiffres et des lettres ou laisser vide.",
                end="\n\n",
                style="bold red",
            )


def message_erreur_selection_menu(nombre_entrees):
    CONSOLE.print(
        f"SAISIE INCORRECTE : Vous devez entrer un chiffre compris entre 0 et {nombre_entrees}",
        end="\n\n",
        style="bold red",
    )


def message_erreur_yes_No():
    CONSOLE.print("Veuillez entrer 'o' pour oui ou 'N' pour non.", style="bold red")


def message_erreur_Yes_no():
    CONSOLE.print("Veuillez entrer 'O' pour oui ou 'n' pour non.", style="bold red")


def saisie_utilisateur_recherche(categorie):
    match categorie:
        case "joueur":
            id_joueur = saisie_utilisateur("id du joueur", STR_OR_NUM)
            return id_joueur
        case "tournoi":
            print()
            CONSOLE.print("[bold cyan]Liste des tournois disponibles :[/bold cyan]")
            liste_tournois = controleur.rechercher_tournois(DB)
            for element in liste_tournois:
                print("- " + element)
            print()
            nom_tournoi = saisie_utilisateur("nom du tournoi", STRING)
            return nom_tournoi


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
            liste_joueurs = controleur.rechercher_liste_joueurs(DB, id_joueurs)
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


def fin_programme():
    print()
    CONSOLE.print("FIN DE PROGRAMME", style="bold yellow")
    print()
    exit()


def recherche_vide():
    CONSOLE.print(
        "Merci de vérifier votre saisie : Element introuvable.",
        style="bold red",
    )
    print()


def liste_simple_tournois(liste_tournois):
    print()
    CONSOLE.print("[bold cyan]Liste des tournois disponibles :[/bold cyan]")
    if liste_tournois == []:
        CONSOLE.print("Aucun tournoi à afficher", style="bold red")
    else:
        for element in liste_tournois:
            CONSOLE.print(f"- {element["nom"]}")
    print()


def liste_vide_tournois():
    print()
    CONSOLE.print("Aucun tournoi à afficher", style="bold red")


def joueur_inexistant(id_joueur):
    CONSOLE.print(
        f"L'identifiant '{id_joueur}' n'est associé à aucun joueur enregistré.",
        f"Merci d'ajouter ce nouveau joueur dans le menu 'JOUEURS' avant de l'associer à un tournoi",
        style="bold red",
    )


def joueur_existant(id_joueur):
    CONSOLE.print(f"L'identifiant '{id_joueur}' est déjà enregistré.", style="bold red")


def tournoi_existant(nom_tournoi):
    CONSOLE.print(f"Le nom '{nom_tournoi}' est déjà attribué.", style="bold red")


def message_succes():
    CONSOLE.print("Votre demande a bien été validée", style="bold green")


def lancer_tournoi():
    nom_tournoi = saisie_utilisateur("nom du tournoi", STRING)
    return nom_tournoi


def tournoi_deja_lance(id_tournoi):
    CONSOLE.print(
        f"[bold red]Le tournoi n°[yellow]{id_tournoi}[/yellow] est déjà commencé. Impossible d'ajouter un nouveau joueur.[/bold red]"
    )


def creation_fichier_db_tournoi(chemin_fichier):
    CONSOLE.print(
        f"Le fichier de données '{chemin_fichier}' a été créé avec succès.",
        style="bold green",
        end="\n\n",
    )


def demande_suppr_db_tournoi(chemin_fichier):
    CONSOLE.print(f"Le fichier de données '{chemin_fichier}' existe déjà.")
    confirmation = input(
        "SI VOUS CONTINUEZ, DES DONNEES PEUVENT ETRE PERDUES. \n Continuer ? [O/n] :"
    )
    while confirmation != "O" and confirmation != "n":
        message_erreur_yes_No()
        confirmation = input(
            "SI VOUS CONTINUEZ, DES DONNEES PEUVENT ETRE PERDUES. \n Continuer ? [O/n] :"
        )
    return confirmation


def fichier_ecrase(chemin_fichier):
    CONSOLE.print(
        f"Le fichier '{chemin_fichier}' contenant les données du tournoi a été vidé.",
        style="bold green",
        end="\n\n",
    )


def lancer_tournoi_impossible(nom_tournoi):
    CONSOLE.print(
        f"Impossible de débuter '{nom_tournoi}'.",
        "Vérifiez les données du fichier de données existant et utilisez le menu 'Chargement' pour reprendre le tournoi.",
        style="bold red",
    )


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


def liste_matchs(joueur1, joueur2, no_match):
    CONSOLE.print(
        f"[white]Le Match n°{no_match} oppose [bold]{joueur1.prenom} {joueur1.nom} ({joueur1.identifiant})[/bold][/white]",
        f"[white]et [bold]{joueur2.prenom} {joueur2.nom} ({joueur2.identifiant})[/bold][/white]",
    )


def saisie_id_gagnant():
    gagnant = saisie_utilisateur("id du gagnant (vide = match nul)", STRNUM_OR_EMPTY)
    return gagnant


def erreur_saisie():
    CONSOLE.print("Saisie incorrecte", style="bold red")


def sauvegarde(element):
    CONSOLE.print(
        f"Les données du {element} ont été sauvegardées.",
        style="bold green",
        end="\n\n",
    )


def fin_tour(nom):
    CONSOLE.print(f"Le {nom} est terminé !", style="bold green")


def tour_suivant():
    saisie_utilisateur = input("Souhaitez-vous lancer le tour suivant ? [o/N] : ")
    while saisie_utilisateur != "o" and saisie_utilisateur != "N":
        message_erreur_yes_No()
        saisie_utilisateur = input("Souhaitez-vous lancer le tour suivant ? [o/N] : ")
    return saisie_utilisateur


def tournoi_termine(id_tournoi, nom_tournoi):
    CONSOLE.print(
        f"[bold cyan]Le tournoi '{id_tournoi} - {nom_tournoi}' est terminé ![/bold cyan]",
        end="\n\n",
    )


def classement_tournoi(classement):
    CONSOLE.print("CLASSEMENT", style="bold yellow")
    for element in classement:
        CONSOLE.print(f"[bold cyan]{element}[/bold cyan]")
