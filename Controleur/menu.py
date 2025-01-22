#!/usr/bin/env python3


from Vue import message_erreur, message_succes, saisie_utilisateur
from Modele import fonctions_modele
from constantes import *
from Controleur import (
    verifications,
    interactions_controleur_modele,
    fonctions_controleur,
    preparation,
    tournoi,
)

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
                "1-Exporter la liste des joueurs",
                "2-Exporter la liste des tournois",
                "3-Exporter le nom et la date d'un tournoi",
                "4-Exporter la liste des joueurs d'un tournoi",
                "5-Exporter la liste des tours et des matchs d'un tournoi",
            ]

    return choix_disponibles


def run():
    # Demande à la vue l'afffichage du menu principal
    entrees_menu_principal = menus_disponibles("principal")
    menu_principal = saisie_utilisateur.Menu(entrees_menu_principal, "MENU PRINCIPAL")
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
                        fonctions_modele.ajout_donnees_json(DB, categorie, infos_joueur)
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
                    print("EN COURS DE PROGRAMMATION")
                    run()
        case "2":
            match categorie:
                case "joueur":
                    chercher_saisie_utilisateur = (
                        saisie_utilisateur.saisie_utilisateur_recherche(categorie)
                    )
                    donnees = interactions_controleur_modele.donnees_a_rechercher(
                        DB, categorie, "identifiant", chercher_saisie_utilisateur
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
                    print("EN COURS DE PROGRAMMATION")
                    run()
        case "3":
            match categorie:
                # ajouter joueur à tournoi préparé
                case "tournoi":
                    fonctions_controleur.afficher_tournois(
                        DB, categorie, "date_debut", "", "pret"
                    )
                    preparation.ajouter_joueur_dans_tournoi(categorie)

                case "rapport":
                    print("EN COURS DE PROGRAMMATION")
                    run()

        case "4":
            match categorie:
                # démarrer tournoi préparé
                case "tournoi":
                    fonctions_controleur.afficher_tournois(
                        DB, categorie, "date_debut", "", "pret"
                    )
                    tournoi.demarrer_tournoi_prepare(categorie)

                case "rapport":
                    print("EN COURS DE PROGRAMMATION")
                    run()
        case "5":
            match categorie:
                # Afficher les tournois en cours
                case "tournoi":
                    fonctions_controleur.afficher_tournois(
                        DB, categorie, "date_fin", "", "en_cours"
                    )
                    run()
                case "rapport":
                    print("EN COURS DE PROGRAMMATION")
                    run()
        case "6":
            match categorie:
                # Reprendre un tournoi en cours
                case "tournoi":
                    tournoi.reprendre_tournoi(categorie)
