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

from Controleur.constantes import DB, STRING, RAPPORTS, CHEMIN_DB_TOURNOIS, CHEMIN_BACKUP_TOURNOIS, CHEMIN_BACKUP_DB
import os
import shutil


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

        case "save/load":
            # Section de sauvegarde des données

            # Si le dossier de backup existe, on demande la confirmation d'écraser les données
            try:
                os.makedirs(CHEMIN_BACKUP_DB)
            except FileExistsError:
                message_erreur.fichier_existe()
                message_erreur.avertissement_perte_donnees()
                if saisie_utilisateur.continuer() == "N":
                    return

            fichiers_tournois = os.listdir(CHEMIN_DB_TOURNOIS)

            # Création du dossier de sauvegarde et copie des .json de chaque tournoi
            os.makedirs(CHEMIN_BACKUP_TOURNOIS, exist_ok=True)
            for element in fichiers_tournois:
                fichier_source = CHEMIN_DB_TOURNOIS + element
                fichier_destination = CHEMIN_BACKUP_TOURNOIS + element + ".bak"
                shutil.copyfile(fichier_source, fichier_destination)
                message_succes.fichier_copie(fichier_destination, "creation")

            # Copie du fichier data.json et enregistrelent de la date de sauvegarde
            fichier_source = DB
            fichier_destination = CHEMIN_BACKUP_DB + "data.json.bak"
            shutil.copyfile(fichier_source, fichier_destination)
            message_succes.fichier_copie(fichier_destination, "creation")
            fichier_txt_date = os.path.join(CHEMIN_BACKUP_DB, "date_derniere_sauvegarde.txt")
            with open(fichier_txt_date, "w") as f:
                f.write(f"{fonctions_controleur.date_maintenant()}\n")


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

        case "save/load":
            # Section de chargement des données sauvegardées

            # Vérification de l'existence du dossier de sauvegarde
            try:
                os.makedirs(CHEMIN_BACKUP_DB)
                os.rmdir(CHEMIN_BACKUP_DB)
                message_erreur.fichier_introuvable()
                return
            except FileExistsError:
                pass

            # Récupération de la date de dernière sauvegarde
            fichier_txt_date = os.path.join(CHEMIN_BACKUP_DB, "date_derniere_sauvegarde.txt")
            with open(fichier_txt_date, "r") as f:
                date_sauvegarde = f.readline()

            # Récupération de la liste des fichiers .bak de tournois
            # et du chemin complet de data.json.bak
            fichiers_bak_tournois = os.listdir(CHEMIN_BACKUP_TOURNOIS)
            fichier_bak_db = CHEMIN_BACKUP_DB + "data.json.bak"

            # Recherche de la liste des tournois enregistrés dans data.json.bak
            # Si un fichier est manquant, affichage d'un message d'erreur
            liste_tournois_bak_db = interactions_controleur_modele.rechercher_tournois(fichier_bak_db)
            if fichier_bak_db == "" or len(fichiers_bak_tournois) != len(liste_tournois_bak_db):
                message_erreur.erreur_fichiers_sauvegarde()
                return

            # Affichage de la liste des fichiers à restaurer et de la date de dernière sauvegarde
            information_utilisateur.texte_liste_disponible("fichiers de sauvegarde")
            for element in fichiers_bak_tournois:
                tournois = interactions_controleur_modele.donnees_a_rechercher(
                    fichier_bak_db, "tournoi", "identifiant", element[0:6]
                )
                tournoi = tournois[0]
                nom_tournoi = element + f" ({tournoi["nom"]})"
                information_utilisateur.afficher_element("tournoi", nom_tournoi)
            information_utilisateur.afficher_element("tournoi", "data.json.bak")
            information_utilisateur.date_sauvegarde(date_sauvegarde)

            # Demande confirmation utilisateur pour restaurer les fichiers
            information_utilisateur.information_restauration_fichiers()
            message_erreur.avertissement_perte_donnees()
            if saisie_utilisateur.continuer() == "N":
                return

            # Restauration des fichiers
            for element in fichiers_bak_tournois:
                chemin_fichier_bak = CHEMIN_BACKUP_TOURNOIS + element
                chemin_fichier_original = CHEMIN_DB_TOURNOIS + element[0:-4]
                if fonctions_controleur.taille_fichiers_differente(
                    chemin_fichier_bak, chemin_fichier_original
                ) or fonctions_controleur.taille_fichiers_differente(fichier_bak_db, DB):
                    if saisie_utilisateur.continuer() == "N":
                        return
                shutil.copyfile(chemin_fichier_bak, chemin_fichier_original)
                message_succes.fichier_copie(chemin_fichier_original, "restauration")
            shutil.copyfile(fichier_bak_db, DB)
            message_succes.fichier_copie(DB, "restauration")


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
    # Remplissage des listes noms_tournois et tournoi_termine
    # Affichage des tournois terminés
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

    # Si la base de données du tournoi demandé existe
    if fichier_existe:
        tours = fonctions_modele.recherche_table(chemin, "tours")
        i = 1

        # alors pour chaque tour on récupère dans une liste
        # le nom, la date_debut et la date_fin
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
            # puis on entre ces données dans le fichier texte
            with open(fichier_rapport, "a") as f:
                f.write(f"\n- {tour[0]} - {tour[1]} - {tour[2]}\n")

            # Pour chaque match, récupération du numéro et des informations du match et des joueurs
            for element in matchs:
                match = []
                no_match = element["no_match"]
                joueur1 = element["joueur1"]
                joueur2 = element["joueur2"]
                gagnant = element["gagnant"]
                donnees_j1 = fonctions_modele.recherche_donnees_json(chemin, "joueur", "identifiant", joueur1)[0]
                donnees_j2 = fonctions_modele.recherche_donnees_json(chemin, "joueur", "identifiant", joueur2)[0]
                donnees_gagnant = fonctions_modele.recherche_donnees_json(chemin, "joueur", "identifiant", gagnant)

                # Données gagnant contient une liste d'un seul dictionnaire
                # On modifie cette liste pour en extraire le dictionnaire.
                if donnees_gagnant != []:
                    donnees_gagnant = donnees_gagnant[0]

                # Ajout dans une liste des données à afficher
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
