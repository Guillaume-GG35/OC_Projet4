#!/usr/bin/env python3


from Vue import (
    message_erreur,
    message_succes,
    saisie_utilisateur,
    information_utilisateur,
)
from Modele import fonctions_modele
from Controleur import (
    verifications,
    interactions_controleur_modele,
    fonctions_controleur,
    preparation,
    tournoi,
)
from Controleur.constantes import DB

import os


def menus_disponibles(id_menu):
    match id_menu:
        case "principal":
            # Entrées du menu principal
            choix_disponibles = [
                "1-Joueurs",
                "2-Tournois",
                "3-Rapports",
                "0-Quitter",
            ]
        case "joueur":
            # Entrées du menu Joueurs
            choix_disponibles = [
                "1-Créer un nouveau joueur",
                "2-Afficher les infos d'un joueur",
                "0-Retour au menu principal",
            ]
        case "tournoi":
            # Entrées du menu Tournois
            choix_disponibles = [
                "1-Préparer un nouveau tournoi",
                "2-Afficher les infos d'un tournoi",
                "3-Ajouter un nouveau joueur à un tournoi préparé",
                "4-Débuter un tournoi préparé",
                "5-Afficher les tournois en cours",
                "6-Reprendre un tournoi en cours",
                "0-Retour au menu principal",
            ]
        case "rapport":
            # Entrées du menu Rapports
            choix_disponibles = [
                "1-Afficher la liste des joueurs",
                "2-Afficher la liste des tournois",
                "3-Afficher le nom et la date d'un tournoi",
                "4-Afficher la liste des joueurs d'un tournoi",
                "5-Afficher la liste des tours et des matchs d'un tournoi",
                "0-Retour au menu principal",
            ]

    return choix_disponibles


def run():
    # Demande à la vue l'afffichage du menu principal
    entrees_menu_principal = menus_disponibles("principal")
    menu_principal = saisie_utilisateur.Menu(
        entrees_menu_principal, "MENU PRINCIPAL"
    )
    try:
        if os.path.getsize(DB) == 0:
            message_erreur.json_vide(DB)
    except FileNotFoundError:
        message_erreur.json_introuvable(DB)
    choix_utilisateur_menu_principal = verifications.obtenir_choix_valide(
        menu_principal
    )

    match choix_utilisateur_menu_principal:
        case "0":
            message_succes.fin_programme()
        case "1":
            # Demande à la vue l'affichage du sous-menu "Joueur"
            categorie = "joueur"
            sous_menu(categorie)

        case "2":
            # Demande à la vue l'affichage du sous-menu "Tournoi"
            categorie = "tournoi"
            sous_menu(categorie)

        case "3":
            # Demande à la vue l'affichage du sous-menu "Rapport"
            categorie = "rapport"
            sous_menu(categorie)


def sous_menu(categorie):
    entrees_menu = menus_disponibles(categorie)
    menu = saisie_utilisateur.Menu(entrees_menu, categorie)
    choix_utilisateur_menu = verifications.obtenir_choix_valide(menu)

    match choix_utilisateur_menu:
        case "0":
            run()
        case "1":
            case1(categorie)

        case "2":
            case2(categorie)

        case "3":
            case3(categorie)

        case "4":
            case4(categorie)

        case "5":
            case5(categorie)

        case "6":
            case6(categorie)


def case1(categorie):
    match categorie:
        case "joueur":
            infos_joueur = saisie_utilisateur.saisie_nouveau(categorie)
            infos_joueur["nombre_points"] = 0
            infos_joueur["nombre_exempte"] = 0
            id_joueur = infos_joueur["identifiant"]
            if verifications.id_joueur_existe(DB, id_joueur):
                message_erreur.joueur_existant(id_joueur)
                run()
            else:
                fonctions_modele.ajout_donnees_json(
                    DB, categorie, infos_joueur
                )
                message_succes.message_succes()
        case "tournoi":
            infos_nouvel_element = saisie_utilisateur.saisie_nouveau(categorie)
            nom_tournoi = infos_nouvel_element["nom"]
            id_joueurs = infos_nouvel_element["id_joueurs"]
            if verifications.nom_tournoi_existe(DB, nom_tournoi):
                message_erreur.tournoi_existant(nom_tournoi)
                run()
            else:
                for element in id_joueurs:
                    if not verifications.id_joueur_existe(DB, element):
                        message_erreur.joueur_inexistant(element)
                        run()
                fonctions_modele.ajout_donnees_json(
                    DB, categorie, infos_nouvel_element
                )
                message_succes.message_succes()
        case "rapport":
            joueurs = interactions_controleur_modele.rechercher_tous_joueurs(
                DB
            )
            joueurs = sorted(joueurs)
            information_utilisateur.liste_elements("joueurs")
            for element in joueurs:
                information_utilisateur.afficher_element("joueur", element)


def case2(categorie):
    match categorie:
        case "joueur":
            chercher_saisie_utilisateur = (
                saisie_utilisateur.saisie_utilisateur_recherche(categorie)
            )
            donnees = interactions_controleur_modele.donnees_a_rechercher(
                DB,
                categorie,
                "identifiant",
                chercher_saisie_utilisateur,
            )
            interactions_controleur_modele.afficher_donnees(categorie, donnees)

        case "tournoi":
            chercher_saisie_utilisateur = (
                saisie_utilisateur.saisie_utilisateur_recherche(categorie)
            )
            donnees = interactions_controleur_modele.donnees_a_rechercher(
                DB, categorie, "nom", chercher_saisie_utilisateur
            )
            interactions_controleur_modele.afficher_donnees(categorie, donnees)

        case "rapport":
            tournois = interactions_controleur_modele.rechercher_tournois(DB)
            information_utilisateur.liste_elements("tournois")
            for element in tournois:
                information_utilisateur.afficher_element("tournoi", element)


def case3(categorie):
    match categorie:
        # ajouter joueur à tournoi préparé
        case "tournoi":
            fonctions_controleur.afficher_tournois(
                DB, categorie, "date_debut", "", "pret"
            )
            preparation.ajouter_joueur_dans_tournoi(categorie)

        case "rapport":
            chercher_saisie_utilisateur = (
                saisie_utilisateur.saisie_utilisateur_recherche("tournoi")
            )
            donnees = interactions_controleur_modele.donnees_a_rechercher(
                DB, "tournoi", "nom", chercher_saisie_utilisateur
            )[0]
            nom_du_tournoi = donnees["nom"]
            date_du_tournoi = donnees["date_debut"]
            information_utilisateur.afficher_donnees_tournoi(
                nom_du_tournoi, date_du_tournoi
            )


def case4(categorie):
    match categorie:
        # démarrer tournoi préparé
        case "tournoi":
            fonctions_controleur.afficher_tournois(
                DB, categorie, "date_debut", "", "pret"
            )
            tournoi.demarrer_tournoi_prepare(categorie)

        case "rapport":
            chercher_saisie_utilisateur = (
                saisie_utilisateur.saisie_utilisateur_recherche("tournoi")
            )
            donnees = interactions_controleur_modele.donnees_a_rechercher(
                DB, "tournoi", "nom", chercher_saisie_utilisateur
            )[0]
            joueurs_du_tournoi = donnees["id_joueurs"]
            liste_joueurs = (
                interactions_controleur_modele.rechercher_liste_joueurs(
                    DB, joueurs_du_tournoi
                )
            )
            information_utilisateur.liste_elements("joueurs")
            joueurs_enregistres = [
                [joueur["nom"], joueur["prenom"]] for joueur in liste_joueurs
            ]
            joueurs_enregistres = sorted(joueurs_enregistres)
            for element in joueurs_enregistres:
                information_utilisateur.afficher_element("joueur", element)


def case5(categorie):
    match categorie:
        # Afficher les tournois en cours
        case "tournoi":
            fonctions_controleur.afficher_tournois(
                DB, categorie, "date_fin", "", "en_cours"
            )
            run()
        case "rapport":
            fonctions_controleur.afficher_tournois(
                DB, "tournoi", "date_fin", "", "en_cours"
            )


def case6(categorie):
    match categorie:
        # Reprendre un tournoi en cours
        case "tournoi":
            tournoi.reprendre_tournoi(categorie)
