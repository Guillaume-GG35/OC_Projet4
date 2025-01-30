#!/usr/bin/env python3

from Vue import message_erreur
from Modele import fonctions_modele

from datetime import datetime
import os


def choix_indisponible(choix_utilisateur, nombre_entrees):
    try:
        choix_utilisateur = int(choix_utilisateur)
        if choix_utilisateur > nombre_entrees:
            message_erreur.message_erreur_selection_menu(nombre_entrees)
            return True

        else:
            return False

    except ValueError:
        message_erreur.message_erreur_selection_menu(nombre_entrees)
        return True


def obtenir_choix_valide(menu):
    choix_utilisateur = menu.get_choix()
    while choix_indisponible(choix_utilisateur, menu.nombre_entrees):
        choix_utilisateur = menu.get_choix()

    return choix_utilisateur


def valider(saisie_utilisateur, type_donnee):
    match type_donnee:
        case "str":
            return not (saisie_utilisateur == "" or any(element.isdigit() for element in saisie_utilisateur))

        case "num":
            return not (saisie_utilisateur == "" or any(element.isalpha() for element in saisie_utilisateur))

        case "NumOrEmpty":
            return saisie_utilisateur == "" or saisie_utilisateur.isdigit()

        case "StrOrNum":
            saisie_utilisateur = saisie_utilisateur.replace(" ", "")
            return not (saisie_utilisateur == "" or saisie_utilisateur.isdigit() or saisie_utilisateur.isalpha())

        case "StrNumOrEmpty":
            return (
                saisie_utilisateur == ""
                or any(element.isalpha() for element in saisie_utilisateur)
                and any(element.isdigit() for element in saisie_utilisateur)
            )

        case "":
            return True


def valider_nombre_tours(nombre_tours):
    match nombre_tours:
        case "":
            nombre_tours = 4
    return nombre_tours


def verifier_date(date_str):
    if date_str == "Menu":
        return True

    else:
        try:
            datetime.strptime(date_str, "%d/%m/%Y")
            return True

        except ValueError:
            return False


def id_joueur_existe(nom_db, id_joueur):
    joueur = fonctions_modele.recherche_donnees_json(nom_db, "joueur", "identifiant", id_joueur)
    if joueur == []:
        return False
    else:
        return True


def nom_tournoi_existe(nom_db, nom_tournoi):
    tournoi = fonctions_modele.recherche_donnees_json(nom_db, "tournoi", "nom", nom_tournoi)
    if tournoi == []:
        return False
    else:
        return True


def fichier_donnees_existe(chemin_fichier):
    try:
        with open(chemin_fichier, "x"):
            pass
        os.remove(chemin_fichier)
        return False

    except FileExistsError:
        return True
