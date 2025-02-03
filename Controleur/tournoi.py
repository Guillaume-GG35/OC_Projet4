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
    # Récupération de la saisie utilisateur (nom du tournoi à lancer)
    nom_tournoi = saisie_utilisateur.lancer_tournoi()
    if nom_tournoi == "Menu":
        return

    # Recherche des données du tournoi demandées par l'utilisateur
    # (une liste est retournée par la fonction donnees_a_rechercher)
    liste_donnees_tournoi = interactions_controleur_modele.donnees_a_rechercher(DB, categorie, "nom", nom_tournoi)
    if not liste_donnees_tournoi:
        return

    elif liste_donnees_tournoi != [] and liste_donnees_tournoi is not None:
        # Création d'un objet Tournoi et actualisation du fichier data.json
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
        # - Création de la base de données spécifique au tournoi
        # - Injection des participants dans cette nouvelle base de données
        # - Lancement du tournoi
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
    # Dans le cas d'une "Reprise d'un tournoi en cours", le premier tour à jouer
    # ne sera pas nécessairement le premier tour du tournoi
    premier_tour = tournoi.tour_actuel

    # Boucle sur le nombre de tours du tournoi
    # Pour chaque tour du tournoi, création d'un objet tour et affichage du numéro de tour
    for tournoi.tour_actuel in range(premier_tour, int(tournoi.nombre_tours) + 1):
        tour = classes.Tour(tournoi.tour_actuel, tournoi.nom)
        information_utilisateur.afficher_nom_round(tour.nom)

        # Au premier tour, mélange des joueurs
        # et vérification de l'existence dans la base de données du tournoi
        # de la liste des matchs possibles
        if tournoi.tour_actuel == 1:
            liste_id_triee = preparation.ordre_joueurs_aleatoire(tournoi.liste_joueurs)
            matchs_possibles = fonctions_modele.recherche_donnees_json(
                db_tournoi, "liste_matchs_possibles", "nom", "matchs_possibles"
            )

            # Si la base de données du tournoi ne contient pas de liste matchs_possibles
            # alors création de cette liste et ajout dans la base de données du tournoi
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

            # liste_joueurs_triee contient une liste de dictionnaires rassemblant
            # l'ensemble des données de chaque joueur du tournoi
            liste_joueurs_triee = interactions_controleur_modele.rechercher_liste_joueurs(db_tournoi, liste_id_triee)

        else:
            # Tri des joueurs en fonction de leur nombre de points dans le tournoi
            # Mise à jour de la liste_id_triee en fonction du nombre de points des joueurs
            liste_joueurs_triee = preparation.trier_joueurs_par_points(db_tournoi, tournoi.liste_joueurs)
            liste_id_triee = [joueur["identifiant"] for joueur in liste_joueurs_triee]

        # Si le lancement du tour est demandé par le menu "Reprendre un tournoi en cours"
        if type_lancement == "load" and liste_matchs != []:
            donnees_joueur_exempte = ""
            type_lancement = ""
            tour.matchs = liste_matchs

        else:
            # Génération des appariements

            # La variable donnees_joueur_exempte contient un dictionnaire rassemblant
            # toutes les informations du joueur exempté

            # La fonction generer_appariements renvoie un tuple contenant dans l'ordre :
            # 1- les informations du joueur exempté
            # 2- la liste des matchs du tour contenant les 2 identifiants des joueurs pour chaque match
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

            # liste_matchs contient une liste de 2 tuples contenant chacun : (identifiant_joueur, nombre_points)
            liste_matchs = appariements[1]
            tour.matchs = liste_matchs

            # Pour chaque match, on ajoute dans la base de données du tournoi dans la catégorie liste_matchs_round_x
            # un dictionnaire contenant le nom du match et les données associées
            i = 1
            for element in liste_matchs:
                donnees_match = {"nom": "match " + str(i), "donnees": element}
                fonctions_modele.ajout_donnees_json(
                    db_tournoi,
                    "liste_matchs_round_" + str(tournoi.tour_actuel),
                    donnees_match,
                )
                i += 1

        # Pour chaque tuple de la variable element, on extrait l'identifiant des joueurs pour créer match_a_tester
        # La variable _ (underscore) prend pour valeur le nombre de points. Elle n'est pas utilisée
        count = no_match
        for element in liste_matchs:
            id1, _ = element[0]
            id2, _ = element[1]
            match_a_tester = (id1, id2)
            match_a_tester_ordonne = tuple(sorted(match_a_tester))

            # Suppression du match_a_tester des combinaisons_matchs_possibles
            # Actualisation de la liste des matchs_jouables présente dans la base de données du tournoi
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
            # Récupération du nom des joueurs pour affichage des matchs du tour en cours
            infos_joueurs = interactions_controleur_modele.rechercher_liste_joueurs(db_tournoi, [id1, id2])
            joueurs = []
            for element in infos_joueurs:
                joueurs.append(f"{element["nom"]} {element["prenom"]}")

            information_utilisateur.annonce_matchs_debut_round(joueurs[0], id1, joueurs[1], id2, count)
            count += 1

        for match_tournoi in liste_matchs:
            # liste_joueurs contient chaque instance de la classe Joueur
            # La variable joueur contient le tuple (id_joueur, nombre_points)
            liste_joueurs = [
                classes.Joueur(**interactions_controleur_modele.rechercher_liste_joueurs(db_tournoi, [joueur[0]]))
                for joueur in match_tournoi
            ]
            # Les variables joueur1 et joueur2 contiennent l'instance de classe de chaque Joueur
            joueur1 = liste_joueurs[0]
            joueur2 = liste_joueurs[1]
            match_x = classes.Match(
                tournoi.nom,
                tour.nom,
                no_match,
                joueur1.identifiant,
                joueur2.identifiant,
            )

            # On demande à l'utilisateur de saisir l'identifiant du gagnant
            id_gagnant = saisie_utilisateur.saisie_id_gagnant(no_match)
            if id_gagnant == "Menu":
                return
            while id_gagnant != joueur1.identifiant and id_gagnant != joueur2.identifiant and id_gagnant != "":
                message_erreur.erreur_saisie()
                message_erreur.choix_possibles(joueur1.identifiant, joueur2.identifiant)
                id_gagnant = saisie_utilisateur.saisie_id_gagnant(no_match)
                if id_gagnant == "Menu":
                    return

            # On déclare la fin du match et on met à jour les points des joueurs dans la base de données du tournoi
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

            # Ajout des données du match terminé dans la base de données du tournoi
            # Affichage d'un message de succès de la sauvegarde
            # On passe au match suivant
            fonctions_modele.ajout_donnees_json(
                db_tournoi,
                "matchs_termines_round_" + str(tournoi.tour_actuel),
                match_x.__dict__,
            )
            message_succes.sauvegarde("match")
            no_match += 1

        # A la fin de tout les matchs, on déclare la fin du tour
        # Ajout des données du tour dans la base de données du tournoi
        tour.fin()
        information_utilisateur.fin_tour(tour.nom)
        fonctions_modele.ajout_donnees_json(db_tournoi, "tours", tour.__dict__)
        message_succes.sauvegarde("tour")

    # A la fin de tout les tours, on déclare la fin du tournoi
    # Actualisation de la base de données principale
    # Actualisation de la base de données du tournoi
    # Création du classement
    # Affichage du classement
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
    # La variable liste_tournois_en_cours contient les dictionnaires de tout les tournois en cours
    liste_tournois_en_cours = fonctions_controleur.afficher_tournois(DB, categorie, "date_fin", "", "en_cours")
    if liste_tournois_en_cours == []:
        # Le message d'erreur est généré dans la fonction afficher_tournois
        pass
    else:
        # Récupération du nom des tournois en cours
        # Saisie utilisateur du nom du tournoi à reprendre
        # Boucle while si la saisie utilisateur n'est pas un tournoi en cours
        noms_tournois_en_cours = [tournoi["nom"] for tournoi in liste_tournois_en_cours]

        nom_tournoi = saisie_utilisateur.lancer_tournoi()
        if nom_tournoi == "Menu":
            return
        while nom_tournoi not in noms_tournois_en_cours:
            message_erreur.erreur_saisie()
            nom_tournoi = saisie_utilisateur.lancer_tournoi()
            if nom_tournoi == "Menu":
                return

        # Récupération de données du tournoi enregistrées dans la base de données principale
        # Création d'une instance de classe Tournoi
        liste_donnees_tournoi = interactions_controleur_modele.donnees_a_rechercher(DB, categorie, "nom", nom_tournoi)
        donnees_tournoi = liste_donnees_tournoi[0]
        tournoi = classes.Tournoi(**donnees_tournoi)

        # Récupération du chemin de fichier de la base de données du tournoi
        db_tournoi = fonctions_controleur.chemin_fichier(tournoi.identifiant)
        nombre_matchs_par_tour = tournoi.calculer_nombre_match_par_tour()

        # Pour chaque tour du tournoi, on cherche dans la base de données du tournoi
        # si le tour a déjà été commencé. On sort de la boucle en gardant le tournoi.tour_actuel
        for i in range(1, int(tournoi.nombre_tours) + 1):
            donnees = fonctions_modele.recherche_donnees_json(db_tournoi, "tours", "nom", "Round " + str(i))
            if donnees == []:
                tournoi.tour_actuel = i
                break

        # Récupération de la liste des matchs_possibles enregistrée dans la base de données tournoi
        # La variable data_matchs_possibles contient une liste de tout les matchs possibles
        # qui sont enregistrés sous forme de liste de 2 éléments
        # La compréhension de liste transforme chaque "match_possible" en un tuple
        matchs_possibles = fonctions_modele.recherche_donnees_json(
            db_tournoi, "liste_matchs_possibles", "nom", "matchs_possibles"
        )[0]
        data_matchs_possibles = matchs_possibles["matchs_jouables"]
        combinaisons_matchs_possibles = [tuple(element) for element in data_matchs_possibles]

        # Récupération des données des matchs du dernier tour enregistré
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

        # Création des tuples contenant les données des joueurs
        # element[0] : tuple contenant l'identifiant et le nombre de points du joueur 1
        # element[1] : tuple contenant l'identifiant et le nombre de points du joueur 2
        for element in donnees_matchs:
            element[0] = tuple(element[0])
            element[1] = tuple(element[1])

        # Récupération du numéro du dernier match joué dans le tour_actuel
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

        # Lancement du tour avec les informations passées en paramètre
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
