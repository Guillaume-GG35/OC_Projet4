#!/usr/bin/env python3

from tinydb import TinyDB, where
from Controleur.constantes import DB

DB = TinyDB(DB)


def selection_bdd(nom_fichier_db):
    db = TinyDB(nom_fichier_db)
    return db


def table(db, categorie):
    table = db.table(categorie)
    return table


def ajout_donnees_json(nom_fichier_db, categorie, donnees):
    db = selection_bdd(nom_fichier_db)
    table(db, categorie).insert(donnees)


def recherche_donnees_json(nom_fichier_db, categorie, nom_recherche, chercher_saisie_utilisateur):
    db = selection_bdd(nom_fichier_db)
    recherche = table(db, categorie).search(where(nom_recherche) == chercher_saisie_utilisateur)
    return recherche


def recherche_table(nom_fichier_db, categorie):
    db = selection_bdd(nom_fichier_db)
    recherche = table(db, categorie).all()
    return recherche


def actualisation_element_db(nom_fichier_db, categorie, cle, valeur, element, nom_element):
    db = selection_bdd(nom_fichier_db)
    table(db, categorie).update({cle: valeur}, where(element) == nom_element)
