#!/usr/bin/env python3

from Vue import (
    saisie_utilisateur,
    information_utilisateur,
    message_erreur,
    message_succes,
)
from Modele import classes, fonctions_modele
from Controleur import (
    interactions_controleur_modele,
    fonctions_controleur,
    preparation,
)

from Controleur.constantes import DB


def demarrer_tournoi_prepare(categorie):
    nom_tournoi = saisie_utilisateur.lancer_tournoi()
    if nom_tournoi == "Menu":
        return
    liste_donnees_tournoi = interactions_controleur_modele.donnees_a_rechercher(DB, categorie, "nom", nom_tournoi)
    if not liste_donnees_tournoi:
        return
    elif liste_donnees_tournoi != [] and liste_donnees_tournoi is not None:
        donnees_tournoi = liste_donnees_tournoi[0]
        tournoi = classes.Tournoi(**donnees_tournoi)
        fonctions_modele.actualisation_element_db(
            DB,
            "tournoi",
            "date_debut",
            tournoi.date_debut,
            "identifiant",
            tournoi.identifiant,
        )
        db_tournoi = fonctions_controleur.fichier_donnees_tournoi(tournoi.identifiant, tournoi.nom)
        interactions_controleur_modele.injecter_joueurs_db_tournoi(db_tournoi, tournoi.liste_joueurs)
        lancer_tours(tournoi, db_tournoi, "", "tournoi", "new", "", "")


def lancer_tours(
    tournoi,
    db_tournoi,
    combinaisons_matchs_possibles,
    categorie,
    type_lancement,
    liste_matchs,
    no_match,
):
    premier_tour = tournoi.tour_actuel

    for tournoi.tour_actuel in range(premier_tour, int(tournoi.nombre_tours) + 1):
        tour = classes.Tour(tournoi.tour_actuel, tournoi.nom)
        information_utilisateur.afficher_nom_round(tour.nom)

        if tournoi.tour_actuel == 1:
            liste_id_triee = preparation.ordre_joueurs_aleatoire(tournoi.liste_joueurs)
            matchs_possibles = fonctions_modele.recherche_donnees_json(
                db_tournoi, "liste_matchs_possibles", "nom", "matchs_possibles"
            )

            if matchs_possibles == []:
                combinaisons_matchs_possibles = fonctions_controleur.combinaisons_possibles(liste_id_triee)
                matchs_possibles = {
                    "nom": "matchs_possibles",
                    "matchs_jouables": combinaisons_matchs_possibles,
                }
                fonctions_modele.ajout_donnees_json(
                    db_tournoi,
                    "liste_matchs_possibles",
                    matchs_possibles,
                )

            liste_joueurs_triee = interactions_controleur_modele.rechercher_liste_joueurs(db_tournoi, liste_id_triee)

        else:
            liste_joueurs_triee = preparation.trier_joueurs_par_points(db_tournoi, tournoi.liste_joueurs)
            liste_id_triee = [joueur["identifiant"] for joueur in liste_joueurs_triee]

        if type_lancement == "load" and liste_matchs != []:
            donnees_joueur_exempte = ""
            type_lancement = ""
            tour.matchs = liste_matchs

        else:
            no_match = 1
            appariements = preparation.generer_appariements(
                db_tournoi,
                liste_id_triee,
                liste_joueurs_triee,
                tournoi.tour_actuel,
                combinaisons_matchs_possibles,
            )
            donnees_joueur_exempte = appariements[0]

            if donnees_joueur_exempte != "":
                preparation.afficher_joueur_exempte(donnees_joueur_exempte)
                joueur_exempte = classes.Joueur(**donnees_joueur_exempte)
                interactions_controleur_modele.affecter_point_joueur_exempte(db_tournoi, joueur_exempte)

            liste_matchs = appariements[1]
            tour.matchs = liste_matchs

            i = 1
            for element in liste_matchs:
                donnees_match = {"nom": "match " + str(i), "donnees": element}
                fonctions_modele.ajout_donnees_json(
                    db_tournoi,
                    "liste_matchs_round_" + str(tournoi.tour_actuel),
                    donnees_match,
                )
                i += 1
        for element in liste_matchs:
            id1, _ = element[0]
            id2, _ = element[1]
            match_a_tester = (id1, id2)
            match_a_tester_ordonne = tuple(sorted(match_a_tester))

            try:
                combinaisons_matchs_possibles.remove(match_a_tester_ordonne)
                fonctions_modele.actualisation_element_db(
                    db_tournoi,
                    "liste_matchs_possibles",
                    "matchs_jouables",
                    combinaisons_matchs_possibles,
                    "nom",
                    "matchs_possibles",
                )

            except ValueError:
                pass

        for match_tournoi in liste_matchs:
            liste_joueurs = [
                classes.Joueur(**interactions_controleur_modele.rechercher_liste_joueurs(db_tournoi, [joueur[0]]))
                for joueur in match_tournoi
            ]
            joueur1 = liste_joueurs[0]
            joueur2 = liste_joueurs[1]
            match_x = classes.Match(
                tournoi.nom,
                tour.nom,
                no_match,
                joueur1.identifiant,
                joueur2.identifiant,
            )
            information_utilisateur.annonce_match(joueur1, joueur2, no_match)
            id_gagnant = saisie_utilisateur.saisie_id_gagnant()
            if id_gagnant == "Menu":
                return
            while id_gagnant != joueur1.identifiant and id_gagnant != joueur2.identifiant and id_gagnant != "":
                message_erreur.erreur_saisie()
                id_gagnant = saisie_utilisateur.saisie_id_gagnant()
                if id_gagnant == "Menu":
                    return
            match_x.fin()
            match id_gagnant:
                case joueur1.identifiant:
                    joueur1.gagnant()
                    match_x.joueur_gagnant(joueur1.identifiant)
                    interactions_controleur_modele.actualiser_points_joueur(
                        db_tournoi, joueur1.nombre_points, joueur1.identifiant
                    )
                case joueur2.identifiant:
                    joueur2.gagnant()
                    match_x.joueur_gagnant(joueur2.identifiant)
                    interactions_controleur_modele.actualiser_points_joueur(
                        db_tournoi, joueur2.nombre_points, joueur2.identifiant
                    )
                case "":
                    joueur1.match_nul()
                    joueur2.match_nul()
                    interactions_controleur_modele.actualiser_points_joueur(
                        db_tournoi, joueur1.nombre_points, joueur1.identifiant
                    )
                    interactions_controleur_modele.actualiser_points_joueur(
                        db_tournoi, joueur2.nombre_points, joueur2.identifiant
                    )
            fonctions_modele.ajout_donnees_json(
                db_tournoi,
                "matchs_termines_round_" + str(tournoi.tour_actuel),
                match_x.__dict__,
            )
            message_succes.sauvegarde("match")
            no_match += 1

        tour.fin()
        information_utilisateur.fin_tour(tour.nom)
        fonctions_modele.ajout_donnees_json(db_tournoi, "tours", tour.__dict__)
        message_succes.sauvegarde("tour")

        if tournoi.tour_actuel < int(tournoi.nombre_tours):
            tour_suivant_accord_utilisateur = saisie_utilisateur.tour_suivant()
            if tour_suivant_accord_utilisateur == "N":
                return

    tournoi.fin()
    fonctions_modele.actualisation_element_db(
        DB,
        "tournoi",
        "date_fin",
        tournoi.date_fin,
        "identifiant",
        tournoi.identifiant,
    )
    fonctions_modele.ajout_donnees_json(db_tournoi, categorie, tournoi.__dict__)
    information_utilisateur.tournoi_termine(tournoi.identifiant, tournoi.nom)
    classement = classement_tournoi(db_tournoi, tournoi.liste_joueurs)
    information_utilisateur.classement_tournoi(classement)


def reprendre_tournoi(categorie):
    liste_tournois_en_cours = fonctions_controleur.afficher_tournois(DB, categorie, "date_fin", "", "en_cours")
    if liste_tournois_en_cours == []:
        pass
    else:
        noms_tournois_en_cours = [tournoi["nom"] for tournoi in liste_tournois_en_cours]

        nom_tournoi = saisie_utilisateur.lancer_tournoi()
        if nom_tournoi == "Menu":
            return
        while nom_tournoi not in noms_tournois_en_cours:
            message_erreur.erreur_saisie()
            nom_tournoi = saisie_utilisateur.lancer_tournoi()
            if nom_tournoi == "Menu":
                return

        liste_donnees_tournoi = interactions_controleur_modele.donnees_a_rechercher(DB, categorie, "nom", nom_tournoi)
        donnees_tournoi = liste_donnees_tournoi[0]
        tournoi = classes.Tournoi(**donnees_tournoi)

        db_tournoi = fonctions_controleur.chemin_fichier(tournoi.identifiant)
        nombre_matchs_par_tour = tournoi.calculer_nombre_match_par_tour()

        for i in range(1, int(tournoi.nombre_tours) + 1):
            donnees = fonctions_modele.recherche_donnees_json(db_tournoi, "tours", "nom", "Round " + str(i))
            if donnees == []:
                tournoi.tour_actuel = i
                break
        matchs_possibles = fonctions_modele.recherche_donnees_json(
            db_tournoi, "liste_matchs_possibles", "nom", "matchs_possibles"
        )[0]
        data_matchs_possibles = matchs_possibles["matchs_jouables"]
        combinaisons_matchs_possibles = [tuple(element) for element in data_matchs_possibles]

        donnees_matchs = []
        for j in range(1, int(nombre_matchs_par_tour) + 1):
            try:
                donnees_matchs.append(
                    fonctions_modele.recherche_donnees_json(
                        db_tournoi,
                        "liste_matchs_round_" + str(tournoi.tour_actuel),
                        "nom",
                        "match " + str(j),
                    )[0]["donnees"]
                )
            except IndexError:
                pass

        for element in donnees_matchs:
            element[0] = tuple(element[0])
            element[1] = tuple(element[1])

        for i in range(1, int(nombre_matchs_par_tour) + 1):
            donnees = fonctions_modele.recherche_donnees_json(
                db_tournoi,
                "matchs_termines_round_" + str(tournoi.tour_actuel),
                "no_match",
                i,
            )
            if donnees == []:
                no_match = i
                break
            else:
                donnees_matchs.pop(i - 1)

        lancer_tours(
            tournoi,
            db_tournoi,
            combinaisons_matchs_possibles,
            categorie,
            "load",
            donnees_matchs,
            no_match,
        )


def classement_tournoi(db_tournoi, liste_joueurs):
    donnees_classement = preparation.trier_joueurs_par_points(db_tournoi, liste_joueurs)
    classement = []
    for joueur in donnees_classement:
        id = joueur["identifiant"]
        nom = joueur["nom"]
        prenom = joueur["prenom"]
        nb_points = joueur["nombre_points"]
        classement.append(f"{id} - {nom} {prenom} : {nb_points} points")
    return classement
