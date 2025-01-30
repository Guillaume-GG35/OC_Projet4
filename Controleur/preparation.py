#!/usr/bin/env python3

from Vue import (
    saisie_utilisateur,
    information_utilisateur,
    message_erreur,
    message_succes,
)
from Modele import fonctions_modele
from Controleur import (
    interactions_controleur_modele,
    verifications,
    fonctions_controleur,
)

from Controleur.constantes import DB, STRING, STR_OR_NUM

import random


def ajouter_joueur_dans_tournoi(categorie):
    nom_tournoi = saisie_utilisateur.saisie_utilisateur("nom du tournoi", STRING)
    if nom_tournoi == "Menu":
        return

    donnees = interactions_controleur_modele.donnees_a_rechercher(DB, categorie, "nom", nom_tournoi)
    if not donnees:
        return

    id_nouveau_joueur = saisie_utilisateur.saisie_utilisateur("id du nouveau joueur", STR_OR_NUM)
    if id_nouveau_joueur == "Menu":
        return

    joueur_existant = verifications.id_joueur_existe(DB, id_nouveau_joueur)
    if not joueur_existant:
        message_erreur.joueur_inexistant(id_nouveau_joueur)
        return

    donnees = donnees[0]
    fichier = fonctions_controleur.chemin_fichier(donnees["identifiant"])
    if not verifications.fichier_donnees_existe(fichier):
        for element in donnees["id_joueurs"]:
            if element == id_nouveau_joueur:
                message_erreur.joueur_existant(id_nouveau_joueur)
                return

        donnees["id_joueurs"].append(id_nouveau_joueur)
        fonctions_modele.actualisation_element_db(
            DB,
            categorie,
            "id_joueurs",
            donnees["id_joueurs"],
            "nom",
            nom_tournoi,
        )
        message_succes.message_succes()

    else:
        message_erreur.tournoi_deja_lance(donnees["identifiant"])


def generer_appariements(
    nom_db,
    liste_id_joueurs,
    liste_joueurs_triee,
    no_tour,
    combinaisons_possibles,
):
    matchs = []
    if len(liste_id_joueurs) % 2 != 0:
        if no_tour == 1:
            joueur_exempte = interactions_controleur_modele.rechercher_liste_joueurs(nom_db, [liste_id_joueurs[-1]])
            liste_id_joueurs_finale = liste_id_joueurs[:-1]

        else:
            liste_joueurs_a_exempter = []
            for element in liste_joueurs_triee:
                if element["nombre_exempte"] == 0:
                    liste_joueurs_a_exempter.append(element)

            if len(liste_joueurs_a_exempter) == 1:
                joueur_exempte = liste_joueurs_a_exempter[0]

            else:
                for joueur in reversed(liste_joueurs_triee):
                    if joueur["nombre_exempte"] == 0:
                        joueur_exempte = joueur
                        break

            liste_id_joueurs_finale = [id for id in liste_id_joueurs if id != joueur_exempte["identifiant"]]
    else:
        liste_id_joueurs_finale = list(liste_id_joueurs)
        joueur_exempte = ""

    while len(liste_id_joueurs_finale) > 0:
        i = 0
        for j in range(-1, 2):
            match_a_tester = tuple(sorted((liste_id_joueurs_finale[i], liste_id_joueurs_finale[j])))
            match_valide = False

            for element in combinaisons_possibles:
                if match_a_tester == element:
                    match_valide = True
                    break

            if match_valide:
                break

        while not match_valide:
            for j in range(2, len(liste_id_joueurs_finale)):
                match_a_tester = tuple(sorted((liste_id_joueurs_finale[i], liste_id_joueurs_finale[j])))
                for element in combinaisons_possibles:
                    if match_a_tester == element:
                        match_valide = True
                        break

                if match_valide:
                    break

            if not match_valide:
                if joueur_exempte:
                    joueur_exempte_copie = joueur_exempte
                    joueur_exempte = interactions_controleur_modele.rechercher_liste_joueurs(
                        nom_db, [liste_id_joueurs_finale[1]]
                    )
                    liste_id_joueurs_finale[1] = joueur_exempte_copie["identifiant"]
                    match_valide = True

                else:
                    match_valide = True

        joueur1 = interactions_controleur_modele.donnees_a_rechercher(
            DB, "joueur", "identifiant", liste_id_joueurs_finale[i]
        )[0]
        joueur2 = interactions_controleur_modele.donnees_a_rechercher(
            DB, "joueur", "identifiant", liste_id_joueurs_finale[j]
        )[0]
        matchs.append(
            [
                (joueur1["identifiant"], joueur1["nombre_points"]),
                (joueur2["identifiant"], joueur2["nombre_points"]),
            ]
        )

        liste_id_joueurs_finale.remove(joueur1["identifiant"])
        liste_id_joueurs_finale.remove(joueur2["identifiant"])

    return joueur_exempte, matchs


def afficher_joueur_exempte(joueur_exempte):
    nom_joueur_exempte = joueur_exempte["nom"]
    prenom_joueur_exempte = joueur_exempte["prenom"]
    id_joueur_exempte = joueur_exempte["identifiant"]
    information_utilisateur.joueur_exempte(
        nom_joueur_exempte,
        prenom_joueur_exempte,
        id_joueur_exempte,
    )


def ordre_joueurs_aleatoire(liste_joueurs):
    random.shuffle(liste_joueurs)
    return liste_joueurs


def trier_joueurs_par_points(db_tournoi, liste_joueurs):
    liste_joueurs_a_trier = interactions_controleur_modele.rechercher_liste_joueurs(db_tournoi, liste_joueurs)
    points = [joueur["nombre_points"] for joueur in liste_joueurs_a_trier]
    shuffle = True
    for i in range(0, len(points) - 2):
        if points[i] != points[i + 1]:
            shuffle = False
            break

    if shuffle:
        liste_joueurs_triee = ordre_joueurs_aleatoire(liste_joueurs_a_trier)

    else:
        liste_joueurs_triee = sorted(
            liste_joueurs_a_trier,
            key=lambda d: float(d["nombre_points"]),
            reverse=True,
        )

    return liste_joueurs_triee
