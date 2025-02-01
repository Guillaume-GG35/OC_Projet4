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
    # Récupération des données de saisie utilisateur
    nom_tournoi = saisie_utilisateur.saisie_utilisateur("nom du tournoi", STRING)
    if nom_tournoi == "Menu":
        return

    id_nouveau_joueur = saisie_utilisateur.saisie_utilisateur("id du nouveau joueur", STR_OR_NUM)
    if id_nouveau_joueur == "Menu":
        return
    joueur_existant = verifications.id_joueur_existe(DB, id_nouveau_joueur)
    if not joueur_existant:
        message_erreur.joueur_inexistant(id_nouveau_joueur)
        return

    # Récupération des données du tournoi dans la base de données principale
    donnees = interactions_controleur_modele.donnees_a_rechercher(DB, categorie, "nom", nom_tournoi)
    if not donnees:
        return
    donnees = donnees[0]

    # Si le fichier json du tournoi n'existe pas,
    # on ajoute les id_joueur dans le tournoi
    # enregistré dans base de données principale
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
    # Si un nombre impair de joueurs est trouvé
    # alors on exempte un joueur
    if len(liste_id_joueurs) % 2 != 0:
        if no_tour == 1:
            # Pour le premier tour, le dernier joueur de la liste est exempté
            joueur_exempte = interactions_controleur_modele.rechercher_liste_joueurs(nom_db, [liste_id_joueurs[-1]])
            liste_id_joueurs_finale = liste_id_joueurs[:-1]

        else:
            liste_joueurs_a_exempter = []
            # Mise en place d'une liste des joueurs qui n'ont jamais été exemptés
            for element in liste_joueurs_triee:
                if element["nombre_exempte"] == 0:
                    liste_joueurs_a_exempter.append(element)
            # Si la liste n'a qu'un seul élément, alors c'est ce joueur qui doit être exempté
            if len(liste_joueurs_a_exempter) == 1:
                joueur_exempte = liste_joueurs_a_exempter[0]

            else:
                # Sinon le joueur qui a le moins de points et qui n'a jamais
                # été exempté sera exempté pour ce tour
                for joueur in reversed(liste_joueurs_triee):
                    if joueur["nombre_exempte"] == 0:
                        joueur_exempte = joueur
                        break

            # On dresse la liste finale des joueurs en supprimant le joueur exempté
            liste_id_joueurs_finale = [id for id in liste_id_joueurs if id != joueur_exempte["identifiant"]]
    else:
        # Si le nombre de joueurs est pair, aucun joueur n'est exempté
        liste_id_joueurs_finale = list(liste_id_joueurs)
        joueur_exempte = ""

    while len(liste_id_joueurs_finale) > 0:
        i = 0
        for j in range(-1, 2):
            # On prend le premier et le dernier joueur de la liste et on
            # les associe pour tester si ce match est une combinaison possible
            match_a_tester = tuple(sorted((liste_id_joueurs_finale[i], liste_id_joueurs_finale[j])))
            match_valide = False

            for element in combinaisons_possibles:
                if match_a_tester == element:
                    match_valide = True
                    break

            if match_valide:
                break

        while not match_valide:
            # Tentative d'appairer le joueur[i] avec les joueurs suivants dans la liste
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
            # Après avoir essayé plusieurs tentative d'appariements
            # on valide le match si aucune meilleure solution n'est trouvée
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

        # Suppression des joueurs sélectionnées pour le match
        # de la liste des joueurs à placer
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
    # Si le nombre de points de chaque joueur est identique
    # alors on mélange la liste pour préparer le travail
    # de l'algorithme d'appariement
    for i in range(0, len(points) - 2):
        if points[i] != points[i + 1]:
            shuffle = False
            break

    if shuffle:
        liste_joueurs_triee = ordre_joueurs_aleatoire(liste_joueurs_a_trier)

    else:
        # Sinon on trie la liste en fonction du nombre de points de chaque joueur
        liste_joueurs_triee = sorted(
            liste_joueurs_a_trier,
            key=lambda d: float(d["nombre_points"]),
            reverse=True,
        )

    return liste_joueurs_triee
