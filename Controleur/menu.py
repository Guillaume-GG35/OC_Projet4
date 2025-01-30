#!/usr/bin/env python3


from Vue import message_erreur, message_succes, saisie_utilisateur
from Controleur import verifications, execution_commandes
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
    menu_principal = saisie_utilisateur.Menu(entrees_menu_principal, "MENU PRINCIPAL")
    try:
        if os.path.getsize(DB) == 0:
            message_erreur.json_vide(DB)
    except FileNotFoundError:
        message_erreur.json_introuvable(DB)

    choix_utilisateur_menu_principal = verifications.obtenir_choix_valide(menu_principal)

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
            pass

        case "1":
            execution_commandes.case1(categorie)

        case "2":
            execution_commandes.case2(categorie)

        case "3":
            execution_commandes.case3(categorie)

        case "4":
            execution_commandes.case4(categorie)

        case "5":
            execution_commandes.case5(categorie)

        case "6":
            execution_commandes.case6(categorie)
