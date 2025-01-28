#!/usr/bin/env python3

from Controleur import (
    fonctions_controleur,
    verifications,
    interactions_controleur_modele,
)
from Vue import message_erreur, information_utilisateur

from Controleur.constantes import (
    CONSOLE,
    DB,
    STRING,
    NUM_OR_EMPTY,
    STR_OR_NUM,
    STRNUM_OR_EMPTY,
)


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
            nom_champs = [
                "identifiant",
                "nom",
                "prénom",
                "date de naissance (jj/mm/aaaa)",
            ]
            type_champs = [STR_OR_NUM, STRING, STRING, ""]
            i = 0
            infos_joueur = {}
            for champ in nom_champs:

                if champ == "nom":
                    saisie = saisie_utilisateur(champ, type_champs[i])
                    saisie = saisie.upper()
                    infos_joueur[champ] = saisie

                elif champ == "prénom":
                    saisie = saisie_utilisateur(champ, type_champs[i])
                    champ = "prenom"

                elif champ == "date de naissance (jj/mm/aaaa)":
                    saisie = saisie_utilisateur(champ, type_champs[i])
                    date_correcte = verifications.verifier_date(saisie)
                    while not date_correcte:
                        CONSOLE.print(
                            "SAISIE INCORRECTE : Veuillez entrer une date ",
                            "au format JJ/MM/AAAA",
                            style="bold red",
                        )
                        saisie = saisie_utilisateur(champ, type_champs[i])
                        date_correcte = verifications.verifier_date(saisie)
                    champ = "date_naissance"
                    infos_joueur[champ] = saisie

                else:
                    saisie = saisie_utilisateur(champ, type_champs[i])

                if saisie == "*":
                    return "Menu"
                else:
                    infos_joueur[champ] = saisie
                i += 1
            return infos_joueur

        case "tournoi":

            nom_champs = [
                "identifiant",
                "nom",
                "lieu",
                "nombre de tours (valeur par défaut = 4)",
                "identifiants des joueurs",
                "description",
            ]
            type_champs = [
                "",
                STRING,
                STRING,
                NUM_OR_EMPTY,
                STR_OR_NUM,
                STRING,
            ]

            i = 0
            infos_tournoi = {}
            for champ in nom_champs:

                if champ == "identifiant":
                    saisie = fonctions_controleur.generer_id()
                    infos_tournoi[champ] = saisie
                    i += 1
                    continue

                elif champ == "nombre de tours (valeur par défaut = 4)":
                    saisie = saisie_utilisateur(champ, type_champs[i])
                    cle = "nombre_tours"
                    nombre_tours = verifications.valider_nombre_tours(saisie)
                    infos_tournoi[cle] = nombre_tours

                elif champ == "identifiants des joueurs":
                    saisie = saisie_utilisateur(champ, type_champs[i])
                    liste_joueurs = fonctions_controleur.concat_id_joueurs(
                        saisie
                    )
                    liste_joueurs.sort()
                    cle = "id_joueurs"
                    infos_tournoi[cle] = liste_joueurs

                else:
                    saisie = saisie_utilisateur(champ, type_champs[i])
                    infos_tournoi[champ] = saisie

                if saisie == "*":
                    return "Menu"
                i += 1

            infos_tournoi["date_debut"] = ""
            infos_tournoi["date_fin"] = ""
            return infos_tournoi


def saisie_utilisateur(type_nom, type_donnee):
    while True:
        print()
        message = "(* = Menu principal) Entrez l'information suivante"
        saisie_utilisateur = input(f"{message} - {str.upper(type_nom)} : ")
        if saisie_utilisateur == "*":
            return "Menu"
        elif verifications.valider(saisie_utilisateur, type_donnee):
            return saisie_utilisateur
        else:
            message_erreur.erreur(type_donnee)


def saisie_utilisateur_recherche(categorie):
    match categorie:
        case "joueur":
            id_joueur = saisie_utilisateur("id du joueur", STR_OR_NUM)
            if id_joueur == "*":
                return "Menu"
            else:
                return id_joueur
        case "tournoi":
            print()
            information_utilisateur.texte_liste_disponible("tournois")
            liste_tournois = (
                interactions_controleur_modele.rechercher_tournois(DB)
            )
            for element in liste_tournois:
                print("- " + element)
            print()
            nom_tournoi = saisie_utilisateur("nom du tournoi", STRING)
            if nom_tournoi == "*":
                return "Menu"
            else:
                return nom_tournoi


def lancer_tournoi():
    nom_tournoi = saisie_utilisateur("nom du tournoi", STRING)
    if nom_tournoi == "*":
        return "Menu"
    else:
        return nom_tournoi


def saisie_id_gagnant():
    gagnant = saisie_utilisateur(
        "id du gagnant (vide = match nul)", STRNUM_OR_EMPTY
    )
    if gagnant == "*":
        return "Menu"
    else:
        return gagnant


def tour_suivant():
    saisie_utilisateur = input(
        "Souhaitez-vous lancer le tour suivant ? [o/N] : "
    )
    while saisie_utilisateur != "o" and saisie_utilisateur != "N":
        message_erreur.message_erreur_yes_No()
        saisie_utilisateur = input(
            "Souhaitez-vous lancer le tour suivant ? [o/N] : "
        )
    return saisie_utilisateur
