#!/usr/bin/env python3

from Modele import fonctions_modele
from Vue import message_erreur, information_utilisateur
from Controleur.constantes import DB


def donnees_a_rechercher(nom_db, categorie, nom_recherche, chercher_saisie_utilisateur):
    donnees = fonctions_modele.recherche_donnees_json(nom_db, categorie, nom_recherche, chercher_saisie_utilisateur)
    if categorie == "tournoi" and nom_recherche == "date_debut" and donnees == []:
        information_utilisateur.liste_simple_tournois(donnees)

    elif donnees == [] or donnees == "" or donnees is None:
        message_erreur.recherche_vide()
        return False

    else:
        return donnees


def afficher_donnees(categorie, donnees):
    for element in donnees:
        information_utilisateur.afficher_infos(categorie, element)


def rechercher_liste_joueurs(nom_db, id_joueurs):
    if len(id_joueurs) == 1:
        id_joueur = id_joueurs[0]
        return donnees_a_rechercher(nom_db, "joueur", "identifiant", id_joueur)[0]

    else:
        infos_joueurs = []
        for element in id_joueurs:
            infos_joueurs.append(*donnees_a_rechercher(nom_db, "joueur", "identifiant", element))

        return infos_joueurs


def rechercher_tous_joueurs(nom_db):
    resultat = fonctions_modele.recherche_table(nom_db, "joueur")
    noms_joueurs = []
    for element in resultat:
        noms_joueurs.append([element["nom"], element["prenom"]])

    return noms_joueurs


def rechercher_tournois(nom_db):
    resultat = fonctions_modele.recherche_table(nom_db, "tournoi")
    noms_tournois = []
    for element in resultat:
        noms_tournois.append(element["nom"])

    return noms_tournois


def injecter_joueurs_db_tournoi(db_tournoi, liste_joueurs):
    for element in liste_joueurs:
        donnees_joueur = donnees_a_rechercher(DB, "joueur", "identifiant", element)
        fonctions_modele.ajout_donnees_json(db_tournoi, "joueur", donnees_joueur[0])


def actualiser_points_joueur(nom_db, nombre_points, identifiant):
    fonctions_modele.actualisation_element_db(
        nom_db,
        "joueur",
        "nombre_points",
        nombre_points,
        "identifiant",
        identifiant,
    )


def affecter_point_joueur_exempte(db_tournoi, joueur_exempte):
    joueur_exempte.nombre_points += 1
    joueur_exempte.nombre_exempte += 1
    fonctions_modele.actualisation_element_db(
        db_tournoi,
        "joueur",
        "nombre_points",
        joueur_exempte.nombre_points,
        "identifiant",
        joueur_exempte.identifiant,
    )
    fonctions_modele.actualisation_element_db(
        db_tournoi,
        "joueur",
        "nombre_exempte",
        joueur_exempte.nombre_exempte,
        "identifiant",
        joueur_exempte.identifiant,
    )
