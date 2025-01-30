#!/usr/bin/env python3

from Modele import fonctions_modele
from Vue import message_erreur, message_succes, information_utilisateur
from Controleur import verifications

import shortuuid
import os
import itertools
from datetime import datetime


def date_maintenant():
    date = datetime.now()
    maintenant = date.strftime("%d/%m/%Y - %H:%M")

    return maintenant


def date_nom_fichier():
    date = datetime.now()
    maintenant = date.strftime("%d-%m-%Y-%H-%M-%S")

    return maintenant


def generer_id():
    identifiant = shortuuid.ShortUUID().random(length=6)

    return identifiant


def concat_id_joueurs(id_joueurs):
    liste_joueurs = set(id_joueurs.split())
    liste_joueurs_finale = [joueur for joueur in liste_joueurs]

    return liste_joueurs_finale


def retour_menu(element):
    if element == "*":
        return True


def creer_db_tournoi(db_tournoi):
    with open(db_tournoi, "x"):
        pass


def chemin_fichier(id_tournoi):
    fichier = os.path.join("data", "tournaments", "historique", id_tournoi + ".json")

    return fichier


def chemin_dossier():
    dossier = os.path.join("data", "tournaments", "historique")

    return dossier


def fichier_donnees_tournoi(id_tournoi, nom_tournoi):
    db_tournoi = chemin_fichier(id_tournoi)
    dossier = chemin_dossier()
    os.makedirs(dossier, exist_ok=True)
    if not verifications.fichier_donnees_existe(db_tournoi):
        creer_db_tournoi(db_tournoi)
        message_succes.creation_fichier_db_tournoi(db_tournoi)

    else:
        confirmation = information_utilisateur.demande_suppr_db_tournoi(db_tournoi)
        match confirmation:
            case "O":
                os.remove(db_tournoi)
                creer_db_tournoi(db_tournoi)
                message_succes.fichier_ecrase(db_tournoi)

            case "n":
                message_erreur.lancer_tournoi_impossible(nom_tournoi)

    return db_tournoi


def afficher_tournois(nom_db, categorie, cle, valeur, mode):
    os.makedirs(chemin_dossier(), exist_ok=True)
    liste_tournois = fonctions_modele.recherche_donnees_json(nom_db, categorie, cle, valeur)
    liste_tournois_finale = [element for element in liste_tournois]
    if liste_tournois:
        i = 0
        for element in liste_tournois:
            id_tournoi = element["identifiant"]
            fichier = chemin_fichier(id_tournoi)
            if verifications.fichier_donnees_existe(fichier):
                match mode:
                    case "pret":
                        liste_tournois_finale.pop(i)
                        i -= 1
            else:
                match mode:
                    case "en_cours":
                        liste_tournois_finale.pop(i)
                        i -= 1

            i += 1

    information_utilisateur.liste_simple_tournois(liste_tournois_finale)

    return liste_tournois_finale


def combinaisons_possibles(liste_id_triee):
    combinaisons_possibles = []
    for combinaison in itertools.combinations(liste_id_triee, 2):
        combinaisons_possibles.append(tuple(sorted(combinaison)))

    return combinaisons_possibles


def calculer_nombre_joueurs(liste_joueurs):
    nb_joueurs = len(liste_joueurs)

    return nb_joueurs


def calculer_nombre_matchs(nb_joueurs):
    nb_matchs = nb_joueurs * (nb_joueurs - 1) / 2

    return int(nb_matchs)


def calculer_nombre_tours(nb_joueurs):
    if nb_joueurs % 2 == 0:
        nb_tours = nb_joueurs - 1

    else:
        nb_tours = nb_joueurs

    return nb_tours
