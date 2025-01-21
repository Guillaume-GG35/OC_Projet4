#!/usr/bin/env python3

""" CONTROLEUR """

import modele
import vue
from constantes import *
from datetime import datetime
import shortuuid
import os
import random
import itertools


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


def choix_indisponible(choix_utilisateur, nombre_entrees):
    try:
        choix_utilisateur = int(choix_utilisateur)
        if choix_utilisateur > nombre_entrees:
            vue.message_erreur_selection_menu(nombre_entrees)
            return True
        else:
            return False
    except ValueError:
        vue.message_erreur_selection_menu(nombre_entrees)
        return True


def obtenir_choix_valide(menu):
    choix_utilisateur = menu.get_choix()
    while choix_indisponible(choix_utilisateur, menu.nombre_entrees):
        choix_utilisateur = menu.get_choix()
    return choix_utilisateur


def valider(saisie_utilisateur, type_donnee):
    match type_donnee:
        case "str":
            return not (
                saisie_utilisateur == ""
                or any(element.isdigit() for element in saisie_utilisateur)
            )

        case "num":
            return not (
                saisie_utilisateur == ""
                or any(element.isalpha() for element in saisie_utilisateur)
            )

        case "NumOrEmpty":
            return saisie_utilisateur == "" or saisie_utilisateur.isdigit()

        case "StrOrNum":
            saisie_utilisateur = saisie_utilisateur.replace(" ", "")
            return not (
                saisie_utilisateur == ""
                or saisie_utilisateur.isdigit()
                or saisie_utilisateur.isalpha()
            )
        case "StrNumOrEmpty":
            return (
                saisie_utilisateur == ""
                or any(element.isalpha() for element in saisie_utilisateur)
                and any(element.isdigit() for element in saisie_utilisateur)
            )


def valider_nombre_tours(nombre_tours):
    match nombre_tours:
        case "":
            nombre_tours = 4
    return nombre_tours


def verifier_date(date_str):
    try:
        datetime.strptime(date_str, "%d/%m/%Y")
        return True
    except ValueError:
        return False


def date_maintenant():
    date = datetime.now()
    maintenant = date.strftime("%d/%m/%Y - %H:%M")
    return maintenant


def generer_id():
    identifiant = shortuuid.ShortUUID().random(length=6)
    return identifiant


def donnees_a_rechercher(nom_db, categorie, nom_recherche, chercher_saisie_utilisateur):
    donnees = modele.recherche_donnees_json(
        nom_db, categorie, nom_recherche, chercher_saisie_utilisateur
    )
    if donnees == [] or donnees == "" or donnees is None:
        vue.recherche_vide()
        run()
    else:
        return donnees


def afficher_donnees(categorie, donnees):
    for element in donnees:
        vue.afficher_infos(categorie, element)


def rechercher_liste_joueurs(nom_db, id_joueurs):
    if len(id_joueurs) == 1:
        id_joueur = id_joueurs[0]
        return donnees_a_rechercher(nom_db, "joueur", "identifiant", id_joueur)[0]
    else:
        infos_joueurs = []
        for element in id_joueurs:
            infos_joueurs.append(
                *donnees_a_rechercher(nom_db, "joueur", "identifiant", element)
            )
        return infos_joueurs


def concat_id_joueurs(id_joueurs):
    liste_joueurs = id_joueurs.split()
    return liste_joueurs


def retour_menu(element):
    if element == "*":
        run()


def rechercher_tournois(nom_db):
    resultat = modele.recherche_table(nom_db, "tournoi")
    noms_tournois = []
    for element in resultat:
        noms_tournois.append(element["nom"])
    return noms_tournois


def id_joueur_existe(nom_db, id_joueur):
    joueur = modele.recherche_donnees_json(nom_db, "joueur", "identifiant", id_joueur)
    if joueur == []:
        return False
    else:
        return True


def nom_tournoi_existe(nom_db, nom_tournoi):
    tournoi = modele.recherche_donnees_json(nom_db, "tournoi", "nom", nom_tournoi)
    if tournoi == []:
        return False
    else:
        return True


def afficher_tournois(nom_db, categorie, cle, valeur, mode):
    os.makedirs("historique", exist_ok=True)
    liste_tournois = donnees_a_rechercher(nom_db, categorie, cle, valeur)
    if liste_tournois:
        i = 0
        for element in liste_tournois:
            id_tournoi = element["identifiant"]
            chemin_fichier = os.path.join("historique", id_tournoi + ".json")
            if fichier_donnees_existe(chemin_fichier):
                match mode:
                    case "pret":
                        liste_tournois.pop(i)
            else:
                match mode:
                    case "en_cours":
                        liste_tournois.pop(i)

            i += 1
        vue.liste_simple_tournois(liste_tournois)


def ajouter_joueur_dans_tournoi(categorie):
    nom_tournoi = vue.saisie_utilisateur("nom du tournoi", STRING)
    id_nouveau_joueur = vue.saisie_utilisateur("id du nouveau joueur", STR_OR_NUM)

    donnees = donnees_a_rechercher(DB, categorie, "nom", nom_tournoi)
    donnees = donnees[0]
    fichier = chemin_fichier(donnees["identifiant"])
    if not fichier_donnees_existe(fichier):
        for element in donnees["id_joueurs"]:
            if element == id_nouveau_joueur:
                vue.joueur_existant(id_nouveau_joueur)
                run()
        donnees["id_joueurs"].append(id_nouveau_joueur)
        modele.actualisation_element_db(
            DB,
            categorie,
            "id_joueurs",
            donnees["id_joueurs"],
            "nom",
            nom_tournoi,
        )
        vue.message_succes()
    else:
        vue.tournoi_deja_lance(donnees["identifiant"])
        run()

    joueur_existant = id_joueur_existe(DB, id_nouveau_joueur)
    if not joueur_existant:
        vue.joueur_inexistant(id_nouveau_joueur)
        run()


def chemin_fichier(id_tournoi):
    fichier = os.path.join("historique", id_tournoi + ".json")
    return fichier


def fichier_donnees_existe(chemin_fichier):
    try:
        with open(chemin_fichier, "x") as fichier:
            pass
        os.remove(chemin_fichier)
        return False
    except FileExistsError:
        return True


def generer_appariements(
    nom_db, liste_id_joueurs, liste_joueurs_triee, no_tour, combinaisons_possibles
):
    matchs = []
    if len(liste_id_joueurs) % 2 != 0:
        if no_tour == 1:
            joueur_exempte = rechercher_liste_joueurs(nom_db, [liste_id_joueurs[-1]])
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
                joueur1 = donnees_a_rechercher(
                    DB, "joueur", "identifiant", liste_id_joueurs_finale[i]
                )[0]
                joueur2 = donnees_a_rechercher(
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
    vue.joueur_exempte(
        nom_joueur_exempte,
        prenom_joueur_exempte,
        id_joueur_exempte,
    )


def affecter_point_joueur_exempte(db_tournoi, joueur_exempte):
    joueur_exempte.nombre_points += 1
    joueur_exempte.nombre_exempte += 1
    modele.actualisation_element_db(
        db_tournoi,
        "joueur",
        "nombre_points",
        joueur_exempte.nombre_points,
        "identifiant",
        joueur_exempte.identifiant,
    )
    modele.actualisation_element_db(
        db_tournoi,
        "joueur",
        "nombre_exempte",
        joueur_exempte.nombre_exempte,
        "identifiant",
        joueur_exempte.identifiant,
    )


def creer_db_tournoi(db_tournoi):
    with open(db_tournoi, "x") as f:
        pass


def fichier_donnees_tournoi(id_tournoi, nom_tournoi):
    db_tournoi = chemin_fichier(id_tournoi)
    os.makedirs("historique", exist_ok=True)
    if not fichier_donnees_existe(db_tournoi):
        creer_db_tournoi(db_tournoi)
        vue.creation_fichier_db_tournoi(db_tournoi)
    else:
        confirmation = vue.demande_suppr_db_tournoi(db_tournoi)
        match confirmation:
            case "O":
                os.remove(db_tournoi)
                creer_db_tournoi(db_tournoi)
                vue.fichier_ecrase(db_tournoi)
            case "n":
                vue.lancer_tournoi_impossible(nom_tournoi)
                run()
    return db_tournoi


def injecter_joueurs_db_tournoi(db_tournoi, liste_joueurs):
    for element in liste_joueurs:
        donnees_joueur = donnees_a_rechercher(DB, "joueur", "identifiant", element)
        modele.ajout_donnees_json(db_tournoi, "joueur", donnees_joueur[0])


def ordre_joueurs_aleatoire(liste_joueurs):
    random.shuffle(liste_joueurs)
    return liste_joueurs


def trier_joueurs_par_points(db_tournoi, liste_joueurs):
    liste_joueurs_a_trier = rechercher_liste_joueurs(db_tournoi, liste_joueurs)
    liste_joueurs_triee = sorted(
        liste_joueurs_a_trier, key=lambda d: float(d["nombre_points"]), reverse=True
    )
    return liste_joueurs_triee


def actualiser_points_joueur(nom_db, nombre_points, identifiant):
    modele.actualisation_element_db(
        nom_db,
        "joueur",
        "nombre_points",
        nombre_points,
        "identifiant",
        identifiant,
    )


def classement_tournoi(db_tournoi, liste_joueurs):
    donnees_classement = trier_joueurs_par_points(db_tournoi, liste_joueurs)
    classement = [
        f"{joueur['identifiant']} - {joueur['nom']} {joueur['prenom']} : {joueur['nombre_points']} points"
        for joueur in donnees_classement
    ]
    return classement


def combinaisons_possibles(liste_id_triee):
    combinaisons_possibles = []
    for combinaison in itertools.combinations(liste_id_triee, 2):
        combinaisons_possibles.append(tuple(sorted(combinaison)))

    return combinaisons_possibles


def demarrer_tournoi_prepare(categorie):
    nom_tournoi = vue.lancer_tournoi()
    liste_donnees_tournoi = donnees_a_rechercher(DB, categorie, "nom", nom_tournoi)
    donnees_tournoi = liste_donnees_tournoi[0]
    tournoi = modele.Tournoi(**donnees_tournoi)
    modele.actualisation_element_db(
        DB,
        "tournoi",
        "date_debut",
        tournoi.date_debut,
        "identifiant",
        tournoi.identifiant,
    )
    db_tournoi = fichier_donnees_tournoi(tournoi.identifiant, tournoi.nom)
    injecter_joueurs_db_tournoi(db_tournoi, tournoi.liste_joueurs)
    lancer_tours(tournoi, db_tournoi, "", "tournoi")


def lancer_tours(tournoi, db_tournoi, combinaisons_matchs_possibles, categorie):
    premier_tour = tournoi.tour_actuel
    for tournoi.tour_actuel in range(premier_tour, int(tournoi.nombre_tours) + 1):
        tour = modele.Tour(tournoi.tour_actuel, tournoi.nom)
        vue.afficher_nom_round(tour.nom)
        if tournoi.tour_actuel == 1:
            liste_id_triee = ordre_joueurs_aleatoire(tournoi.liste_joueurs)

            combinaisons_matchs_possibles = combinaisons_possibles(liste_id_triee)
            matchs_possibles = {
                "nom": "matchs_possibles",
                "matchs_jouables": combinaisons_matchs_possibles,
            }
            modele.ajout_donnees_json(
                db_tournoi,
                "liste_matchs_possibles",
                matchs_possibles,
            )

            liste_joueurs_triee = rechercher_liste_joueurs(db_tournoi, liste_id_triee)
        else:
            liste_joueurs_triee = trier_joueurs_par_points(
                db_tournoi, tournoi.liste_joueurs
            )
            liste_id_triee = [joueur["identifiant"] for joueur in liste_joueurs_triee]
        appariements = generer_appariements(
            db_tournoi,
            liste_id_triee,
            liste_joueurs_triee,
            tournoi.tour_actuel,
            combinaisons_matchs_possibles,
        )
        donnees_joueur_exempte = appariements[0]
        if donnees_joueur_exempte != "":
            afficher_joueur_exempte(donnees_joueur_exempte)
            joueur_exempte = modele.Joueur(**donnees_joueur_exempte)

        liste_matchs = appariements[1]
        for element in liste_matchs:
            id1, _ = element[0]
            id2, _ = element[1]
            match_a_tester = (id1, id2)
            match_a_tester_ordonne = tuple(sorted(match_a_tester))
            try:
                combinaisons_matchs_possibles.remove(match_a_tester_ordonne)
                modele.actualisation_element_db(
                    db_tournoi,
                    "liste_matchs_possibles",
                    "matchs_jouables",
                    combinaisons_matchs_possibles,
                    "nom",
                    "matchs_possibles",
                )
            except ValueError:
                pass
        no_match = 1
        for round in liste_matchs:
            liste_joueurs = [
                modele.Joueur(**rechercher_liste_joueurs(db_tournoi, [joueur[0]]))
                for joueur in round
            ]
            joueur1 = liste_joueurs[0]
            joueur2 = liste_joueurs[1]
            match_x = modele.Match(
                tournoi.nom,
                tour.nom,
                no_match,
                joueur1.identifiant,
                joueur2.identifiant,
            )
            vue.liste_matchs(joueur1, joueur2, no_match)
            id_gagnant = vue.saisie_id_gagnant()
            while (
                id_gagnant != joueur1.identifiant
                and id_gagnant != joueur2.identifiant
                and id_gagnant != ""
            ):
                vue.erreur_saisie()
                id_gagnant = vue.saisie_id_gagnant()
            match_x.fin()
            match id_gagnant:
                case joueur1.identifiant:
                    joueur1.gagnant()
                    match_x.joueur_gagnant(joueur1.identifiant)
                    actualiser_points_joueur(
                        db_tournoi, joueur1.nombre_points, joueur1.identifiant
                    )
                case joueur2.identifiant:
                    joueur2.gagnant()
                    match_x.joueur_gagnant(joueur2.identifiant)
                    actualiser_points_joueur(
                        db_tournoi, joueur2.nombre_points, joueur2.identifiant
                    )
                case "":
                    joueur1.match_nul()
                    joueur2.match_nul()
                    actualiser_points_joueur(
                        db_tournoi, joueur1.nombre_points, joueur1.identifiant
                    )
                    actualiser_points_joueur(
                        db_tournoi, joueur2.nombre_points, joueur2.identifiant
                    )
            modele.ajout_donnees_json(db_tournoi, "matchs", match_x.__dict__)
            vue.sauvegarde("match")
            no_match += 1
        if donnees_joueur_exempte != "":
            affecter_point_joueur_exempte(db_tournoi, joueur_exempte)
        tour.fin()
        vue.fin_tour(tour.nom)
        modele.ajout_donnees_json(db_tournoi, "tours", tour.__dict__)
        vue.sauvegarde("tour")
        if tournoi.tour_actuel < int(tournoi.nombre_tours):
            tour_suivant_accord_utilisateur = vue.tour_suivant()
            if tour_suivant_accord_utilisateur == "N":
                run()
    tournoi.fin()
    modele.actualisation_element_db(
        DB,
        "tournoi",
        "date_fin",
        tournoi.date_fin,
        "identifiant",
        tournoi.identifiant,
    )
    modele.ajout_donnees_json(db_tournoi, categorie, tournoi.__dict__)
    vue.tournoi_termine(tournoi.identifiant, tournoi.nom)
    classement = classement_tournoi(db_tournoi, tournoi.liste_joueurs)
    vue.classement_tournoi(classement)
    run()


# Fonction qui génère les données du sous-menu et qui en demande l'affichage
def sous_menu(categorie):
    entrees_menu = menus_disponibles(categorie)
    menu = vue.Menu(entrees_menu, categorie)
    choix_utilisateur_menu = obtenir_choix_valide(menu)

    match choix_utilisateur_menu:
        case "0":
            run()
        case "1":
            match categorie:
                case "joueur":
                    infos_joueur = vue.saisie_nouveau(categorie)
                    infos_joueur["nombre_points"] = 0
                    infos_joueur["nombre_exempte"] = 0
                    id_joueur = infos_joueur["identifiant"]
                    if id_joueur_existe(DB, id_joueur):
                        vue.joueur_existant(id_joueur)
                        run()
                    else:
                        modele.ajout_donnees_json(DB, categorie, infos_joueur)
                        vue.message_succes()
                case "tournoi":
                    infos_nouvel_element = vue.saisie_nouveau(categorie)
                    nom_tournoi = infos_nouvel_element["nom"]
                    id_joueurs = infos_nouvel_element["id_joueurs"]
                    if nom_tournoi_existe(DB, nom_tournoi):
                        vue.tournoi_existant(nom_tournoi)
                        run()
                    else:
                        for element in id_joueurs:
                            if not id_joueur_existe(DB, element):
                                vue.joueur_inexistant(element)
                                run()
                        modele.ajout_donnees_json(DB, categorie, infos_nouvel_element)
                        vue.message_succes()
                case "rapport":
                    print("EN COURS DE PROGRAMMATION")
                    run()
        case "2":
            match categorie:
                case "joueur":
                    chercher_saisie_utilisateur = vue.saisie_utilisateur_recherche(
                        categorie
                    )
                    donnees = donnees_a_rechercher(
                        DB, categorie, "identifiant", chercher_saisie_utilisateur
                    )
                    afficher_donnees(categorie, donnees)
                case "tournoi":
                    chercher_saisie_utilisateur = vue.saisie_utilisateur_recherche(
                        categorie
                    )
                    donnees = donnees_a_rechercher(
                        DB, categorie, "nom", chercher_saisie_utilisateur
                    )
                    afficher_donnees(categorie, donnees)
                case "rapport":
                    print("EN COURS DE PROGRAMMATION")
                    run()
        case "3":
            match categorie:
                # ajouter joueur à tournoi préparé
                case "tournoi":
                    afficher_tournois(DB, categorie, "date_debut", "", "pret")
                    ajouter_joueur_dans_tournoi(categorie)

                case "rapport":
                    print("EN COURS DE PROGRAMMATION")
                    run()

        case "4":
            match categorie:
                # démarrer tournoi préparé
                case "tournoi":
                    afficher_tournois(DB, categorie, "date_debut", "", "pret")
                    demarrer_tournoi_prepare(categorie)

                case "rapport":
                    print("EN COURS DE PROGRAMMATION")
                    run()
        case "5":
            match categorie:
                # Afficher les tournois en cours
                case "tournoi":
                    afficher_tournois(DB, categorie, "date_fin", "", "en_cours")
                    run()
                case "rapport":
                    print("EN COURS DE PROGRAMMATION")
                    run()
        case "6":
            match categorie:
                # Reprendre un tournoi en cours
                case "tournoi":
                    nom_tournoi = vue.lancer_tournoi()
                    liste_donnees_tournoi = donnees_a_rechercher(
                        DB, categorie, "nom", nom_tournoi
                    )
                    donnees_tournoi = liste_donnees_tournoi[0]
                    tournoi = modele.Tournoi(**donnees_tournoi)

                    db_tournoi = chemin_fichier(tournoi.identifiant)
                    # nombre_matchs_par_tour = tournoi.calculer_nombre_match_par_tour()

                    for i in range(1, int(tournoi.nombre_tours) + 1):
                        donnees = modele.recherche_donnees_json(
                            db_tournoi, "tours", "nom", "Round " + str(i)
                        )
                        if donnees == []:
                            tournoi.tour_actuel = i
                            break
                    matchs_possibles = modele.recherche_donnees_json(
                        db_tournoi, "liste_matchs_possibles", "nom", "matchs_possibles"
                    )[0]
                    data_matchs_possibles = matchs_possibles["matchs_jouables"]
                    combinaisons_matchs_possibles = [
                        tuple(element) for element in data_matchs_possibles
                    ]

                    lancer_tours(
                        tournoi, db_tournoi, combinaisons_matchs_possibles, categorie
                    )


def run():
    # Demande à la vue l'afffichage du menu principal
    entrees_menu_principal = menus_disponibles("principal")
    menu_principal = vue.Menu(entrees_menu_principal, "MENU PRINCIPAL")
    try:
        if os.path.getsize(DB) == 0:
            vue.json_vide(DB)
    except FileNotFoundError:
        vue.json_introuvable(DB)
    choix_utilisateur_menu_principal = obtenir_choix_valide(menu_principal)

    match choix_utilisateur_menu_principal:
        case "0":
            vue.fin_programme()
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
