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

from Controleur.constantes import DB, STRING, RAPPORTS
import os


def case1(categorie):
    match categorie:

        case "joueur":
            # Créer un nouveau joueur

            infos_joueur = saisie_utilisateur.saisie_nouveau(categorie)
            if infos_joueur == "Menu":
                return

            else:
                infos_joueur["nombre_points"] = 0
                infos_joueur["nombre_exempte"] = 0
                fonctions_modele.ajout_donnees_json(DB, categorie, infos_joueur)
                message_succes.message_succes()

        case "tournoi":
            # Préparer un nouveau tournoi

            infos_nouveau_tournoi = saisie_utilisateur.saisie_nouveau(categorie)
            if infos_nouveau_tournoi == "Menu":
                return

            else:
                nom_tournoi = infos_nouveau_tournoi["nom"]
                if verifications.nom_tournoi_existe(DB, nom_tournoi):
                    message_erreur.tournoi_existant(nom_tournoi)

                else:
                    fonctions_modele.ajout_donnees_json(DB, categorie, infos_nouveau_tournoi)
                    message_succes.message_succes()

        case "rapport":
            # Afficher la liste des joueurs

            joueurs = interactions_controleur_modele.rechercher_tous_joueurs(DB)
            joueurs = sorted(joueurs)
            fichier_rapport = creer_rapport("case1")
            information_utilisateur.liste_elements("joueurs")
            for element in joueurs:
                information_utilisateur.afficher_element("joueur", element)
                with open(fichier_rapport, "a") as f:
                    f.write(f"- {element[0]} {element[1]}\n")

            information_utilisateur.rapport_exporte(fichier_rapport)


def case2(categorie):
    match categorie:

        case "joueur":
            # Afficher les infos d'un joueur

            chercher_saisie_utilisateur = saisie_utilisateur.saisie_utilisateur_recherche(categorie)
            if chercher_saisie_utilisateur == "Menu":
                return

            donnees = interactions_controleur_modele.donnees_a_rechercher(
                DB,
                categorie,
                "identifiant",
                chercher_saisie_utilisateur,
            )

            if not donnees:
                return

            interactions_controleur_modele.afficher_donnees(categorie, donnees)

        case "tournoi":
            # Afficher les infos d'un tournoi

            chercher_saisie_utilisateur = saisie_utilisateur.saisie_utilisateur_recherche(categorie)
            if chercher_saisie_utilisateur == "Menu":
                return

            donnees = interactions_controleur_modele.donnees_a_rechercher(
                DB, categorie, "nom", chercher_saisie_utilisateur
            )

            if not donnees:
                return

            elif donnees is not None or donnees != []:
                interactions_controleur_modele.afficher_donnees(categorie, donnees)

        case "rapport":
            # Afficher la liste des tournois

            tournois = interactions_controleur_modele.rechercher_tournois(DB)
            fichier_rapport = creer_rapport("case2")
            information_utilisateur.liste_elements("tournois")
            for element in tournois:
                information_utilisateur.afficher_element("tournoi", element)
                with open(fichier_rapport, "a") as f:
                    f.write(f"- {element}\n")

            information_utilisateur.rapport_exporte(fichier_rapport)


def case3(categorie):
    match categorie:

        case "tournoi":
            # Ajouter joueur à tournoi préparé

            liste_tournois = fonctions_controleur.afficher_tournois(DB, categorie, "date_debut", "", "pret")
            if liste_tournois != []:
                preparation.ajouter_joueur_dans_tournoi(categorie)

        case "rapport":
            # Afficher le nom et la date d'un tournoi

            chercher_saisie_utilisateur = saisie_utilisateur.saisie_utilisateur_recherche("tournoi")
            donnees = interactions_controleur_modele.donnees_a_rechercher(
                DB, "tournoi", "nom", chercher_saisie_utilisateur
            )
            if not donnees:
                return

            donnees = donnees[0]
            fichier_rapport = creer_rapport("case3")
            nom_du_tournoi = donnees["nom"]
            date_du_tournoi = donnees["date_debut"]

            with open(fichier_rapport, "a") as f:
                f.write(f"- {nom_du_tournoi} - {date_du_tournoi}\n")

            information_utilisateur.afficher_donnees_tournoi(nom_du_tournoi, date_du_tournoi)
            information_utilisateur.rapport_exporte(fichier_rapport)


def case4(categorie):
    match categorie:

        case "tournoi":
            # Démarrer tournoi préparé

            liste_tournois = fonctions_controleur.afficher_tournois(DB, categorie, "date_debut", "", "pret")
            if liste_tournois != [] and liste_tournois is not None:
                tournoi.demarrer_tournoi_prepare(categorie)

        case "rapport":
            # Afficher la liste des joueurs d'un tournoi

            chercher_saisie_utilisateur = saisie_utilisateur.saisie_utilisateur_recherche("tournoi")
            donnees = interactions_controleur_modele.donnees_a_rechercher(
                DB, "tournoi", "nom", chercher_saisie_utilisateur
            )
            if not donnees:
                return

            donnees = donnees[0]
            joueurs_du_tournoi = donnees["id_joueurs"]
            liste_joueurs = interactions_controleur_modele.rechercher_liste_joueurs(DB, joueurs_du_tournoi)
            information_utilisateur.liste_elements("joueurs")
            joueurs_enregistres = [[joueur["nom"], joueur["prenom"]] for joueur in liste_joueurs]
            joueurs_enregistres = sorted(joueurs_enregistres)
            fichier_rapport = creer_rapport("case4")
            for element in joueurs_enregistres:
                with open(fichier_rapport, "a") as f:
                    f.write(f"- {element[0]} {element[1]}\n")

                information_utilisateur.afficher_element("joueur", element)

            information_utilisateur.rapport_exporte(fichier_rapport)


def case5(categorie):
    match categorie:

        case "tournoi":
            # Afficher les tournois en cours

            fonctions_controleur.afficher_tournois(DB, categorie, "date_fin", "", "en_cours")

        case "rapport":
            # Afficher la liste des tours et des matchs d'un tournoi

            afficher_tournois_et_tours()


def case6(categorie):
    match categorie:

        case "tournoi":
            # Reprendre un tournoi en cours

            tournoi.reprendre_tournoi(categorie)


def afficher_tournois_et_tours():
    information_utilisateur.texte_liste_disponible("tournois")

    fichier_rapport = creer_rapport("case5")
    resultat = fonctions_modele.recherche_table(DB, "tournoi")
    noms_tournois = []
    tournoi_termine = []
    for element in resultat:
        noms_tournois.append(element["nom"])
        if element["date_fin"] != "":
            tournoi_termine.append(element["identifiant"])
            information_utilisateur.afficher_element("tournoi", element["nom"])

    if tournoi_termine == []:
        message_erreur.liste_vide_tournois()
        return

    saisie = saisie_utilisateur.saisie_utilisateur("nom du tournoi", STRING)
    if saisie == "Menu":
        return

    donnees = interactions_controleur_modele.donnees_a_rechercher(DB, "tournoi", "nom", saisie)
    if not donnees:
        return

    donnees = donnees[0]
    id_tournoi = donnees["identifiant"]
    chemin = fonctions_controleur.chemin_fichier(id_tournoi)
    fichier_existe = verifications.fichier_donnees_existe(chemin)
    if fichier_existe:
        tours = fonctions_modele.recherche_table(chemin, "tours")
        i = 1
        for element in tours:
            tour = []
            matchs = fonctions_modele.recherche_table(chemin, "matchs_termines_round_" + str(i))
            nom = element["nom"]
            date_debut = element["date_debut"]
            date_fin = element["date_fin"]
            tour.append(nom)
            tour.append(date_debut)
            tour.append(date_fin)
            information_utilisateur.afficher_element("rapport_tournoi", tour)
            with open(fichier_rapport, "a") as f:
                f.write(f"\n- {tour[0]} - {tour[1]} - {tour[2]}\n")

            for element in matchs:
                match = []
                no_match = element["no_match"]
                joueur1 = element["joueur1"]
                joueur2 = element["joueur2"]
                gagnant = element["gagnant"]
                donnees_j1 = fonctions_modele.recherche_donnees_json(chemin, "joueur", "identifiant", joueur1)[0]
                donnees_j2 = fonctions_modele.recherche_donnees_json(chemin, "joueur", "identifiant", joueur2)[0]
                donnees_gagnant = fonctions_modele.recherche_donnees_json(chemin, "joueur", "identifiant", gagnant)

                if donnees_gagnant != []:
                    donnees_gagnant = donnees_gagnant[0]
                match.append(no_match)
                match.append(f"{donnees_j1["prenom"]} {donnees_j1["nom"]}")
                match.append(f"{donnees_j2["prenom"]} {donnees_j2["nom"]}")

                if donnees_gagnant == []:
                    match.append("match nul")

                else:
                    match.append(f"{donnees_gagnant["prenom"]} {donnees_gagnant["nom"]}")
                information_utilisateur.afficher_element("matchs", match)

                with open(fichier_rapport, "a") as f:
                    f.write(
                        f"Match n°{match[0]} - Joueur 1 : {match[1]} - Joueur 2 : {match[2]} - Gagnant : {match[3]}\n"
                    )
            i += 1
        information_utilisateur.rapport_exporte(fichier_rapport)

    else:
        message_erreur.erreur_saisie()


def creer_rapport(type):
    maintenant = fonctions_controleur.date_nom_fichier()
    match type:
        case "case1":
            nom_fichier = f"liste_joueurs-{maintenant}.txt"

        case "case2":
            nom_fichier = f"liste_tournois-{maintenant}.txt"

        case "case3":
            nom_fichier = f"nom_date_tournoi-{maintenant}.txt"

        case "case4":
            nom_fichier = f"liste_joueurs_tournoi-{maintenant}.txt"

        case "case5":
            nom_fichier = f"liste_tours_matchs-{maintenant}.txt"

    os.makedirs(RAPPORTS, exist_ok=True)

    return RAPPORTS + nom_fichier
