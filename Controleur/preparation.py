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
    menu,
)

from constantes import *

import random


def ajouter_joueur_dans_tournoi(categorie):
    nom_tournoi = saisie_utilisateur.saisie_utilisateur("nom du tournoi", STRING)
    id_nouveau_joueur = saisie_utilisateur.saisie_utilisateur(
        "id du nouveau joueur", STR_OR_NUM
    )

    donnees = interactions_controleur_modele.donnees_a_rechercher(
        DB, categorie, "nom", nom_tournoi
    )
    donnees = donnees[0]
    fichier = fonctions_controleur.chemin_fichier(donnees["identifiant"])
    if not verifications.fichier_donnees_existe(fichier):
        for element in donnees["id_joueurs"]:
            if element == id_nouveau_joueur:
                message_erreur.joueur_existant(id_nouveau_joueur)
                menu.run()
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
        menu.run()

    joueur_existant = verifications.id_joueur_existe(DB, id_nouveau_joueur)
    if not joueur_existant:
        message_erreur.joueur_inexistant(id_nouveau_joueur)
        menu.run()


def generer_appariements(
    nom_db, liste_id_joueurs, liste_joueurs_triee, no_tour, combinaisons_possibles
):
    matchs = []
    if len(liste_id_joueurs) % 2 != 0:
        if no_tour == 1:
            joueur_exempte = interactions_controleur_modele.rechercher_liste_joueurs(
                nom_db, [liste_id_joueurs[-1]]
            )
            liste_id_joueurs_finale = liste_id_joueurs[:-1]
        else:
            dernier_joueur = liste_joueurs_triee[-1]
            valeur_min_nombre_points = float(dernier_joueur["nombre_points"])
            valeur_min_exemption = float("inf")
            for joueur in reversed(liste_joueurs_triee):
                if (
                    joueur["nombre_exempte"] < valeur_min_exemption
                    and float(joueur["nombre_points"]) == valeur_min_nombre_points
                ):
                    joueur_exempte = joueur
                    valeur_min_exemption = joueur["nombre_exempte"]

            liste_id_joueurs_finale = [
                id for id in liste_id_joueurs if id != joueur_exempte["identifiant"]
            ]
    else:
        liste_id_joueurs_finale = list(liste_id_joueurs)
        joueur_exempte = ""

    while len(liste_id_joueurs_finale) > 0:
        i = 0
        j = 1
        match_a_tester = tuple(
            sorted((liste_id_joueurs_finale[i], liste_id_joueurs_finale[j]))
        )
        match_valide = False
        while not match_valide:
            if (
                j < len(liste_id_joueurs_finale) - 1
                and match_a_tester not in combinaisons_possibles
            ):
                j += 1
                match_a_tester = (
                    liste_id_joueurs_finale[i],
                    liste_id_joueurs_finale[j],
                )
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
    liste_joueurs_a_trier = interactions_controleur_modele.rechercher_liste_joueurs(
        db_tournoi, liste_joueurs
    )
    liste_joueurs_triee = sorted(
        liste_joueurs_a_trier, key=lambda d: float(d["nombre_points"]), reverse=True
    )
    return liste_joueurs_triee
