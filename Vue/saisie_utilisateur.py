#!/usr/bin/env python3

from constantes import *
from Controleur import (
    fonctions_controleur,
    verifications,
    interactions_controleur_modele,
)
from Vue import message_erreur


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
                fonctions_controleur.retour_menu(date_naissance)
                date_correcte = verifications.verifier_date(date_naissance)
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

            identifiant = fonctions_controleur.generer_id()
            nom = saisie_utilisateur("nom", STRING)
            lieu = saisie_utilisateur("lieu", STRING)
            nombre_tours = saisie_utilisateur(
                "nombre de tours (valeur par défaut = 4)", NUM_OR_EMPTY
            )
            nombre_tours = verifications.valider_nombre_tours(nombre_tours)
            id_joueurs = saisie_utilisateur("identifiants des joueurs", STR_OR_NUM)
            liste_joueurs = fonctions_controleur.concat_id_joueurs(id_joueurs)
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
        fonctions_controleur.retour_menu(saisie_utilisateur)
        if verifications.valider(saisie_utilisateur, type_donnee):
            return saisie_utilisateur
        else:
            message_erreur.erreur(type_donnee)


def saisie_utilisateur_recherche(categorie):
    match categorie:
        case "joueur":
            id_joueur = saisie_utilisateur("id du joueur", STR_OR_NUM)
            return id_joueur
        case "tournoi":
            print()
            CONSOLE.print("[bold cyan]Liste des tournois disponibles :[/bold cyan]")
            liste_tournois = interactions_controleur_modele.rechercher_tournois(DB)
            for element in liste_tournois:
                print("- " + element)
            print()
            nom_tournoi = saisie_utilisateur("nom du tournoi", STRING)
            return nom_tournoi


def lancer_tournoi():
    nom_tournoi = saisie_utilisateur("nom du tournoi", STRING)
    return nom_tournoi


def saisie_id_gagnant():
    gagnant = saisie_utilisateur("id du gagnant (vide = match nul)", STRNUM_OR_EMPTY)
    return gagnant


def tour_suivant():
    saisie_utilisateur = input("Souhaitez-vous lancer le tour suivant ? [o/N] : ")
    while saisie_utilisateur != "o" and saisie_utilisateur != "N":
        message_erreur.message_erreur_yes_No()
        saisie_utilisateur = input("Souhaitez-vous lancer le tour suivant ? [o/N] : ")
    return saisie_utilisateur
