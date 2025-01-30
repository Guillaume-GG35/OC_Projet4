#!/usr/bin/env python3

from Controleur import fonctions_controleur


class Joueur:
    def __init__(self, **kwargs):
        self.nom = kwargs.get("nom")
        self.prenom = kwargs.get("prenom")
        self.date_naissance = kwargs.get("date_naissance")
        self.identifiant = kwargs.get("identifiant")
        self.nombre_points = float(kwargs.get("nombre_points", 0))
        self.nombre_exempte = kwargs.get("nombre_exempte", 0)

    def gagnant(self):
        self.nombre_points += 1

    def match_nul(self):
        self.nombre_points += 0.5


class Tournoi:
    tour_actuel = 1

    def __init__(self, **kwargs):
        self.identifiant = kwargs.get("identifiant")
        self.nom = kwargs.get("nom")
        self.lieu = kwargs.get("lieu")
        self.date_debut = fonctions_controleur.date_maintenant()
        self.date_fin = kwargs.get("date_fin")
        self.nombre_tours = kwargs.get("nombre_tours", 4)
        self.liste_joueurs = kwargs.get("id_joueurs")
        self.description = kwargs.get("description")

    def calculer_nombre_joueurs(self):
        nombre_joueurs = len(self.liste_joueurs)
        return nombre_joueurs

    def calculer_nombre_match_par_tour(self):
        nombre_joueurs = self.calculer_nombre_joueurs()
        if nombre_joueurs % 2 != 0:
            nombre_matchs_par_tour = (nombre_joueurs - 1) / 2
        else:
            nombre_matchs_par_tour = nombre_joueurs / 2
        return nombre_matchs_par_tour

    def fin(self):
        self.date_fin = fonctions_controleur.date_maintenant()


class Tour:
    def __init__(self, numero_tour, tournoi_associe):
        self.nom = "Round " + str(numero_tour)
        self.tournoi_associe = tournoi_associe
        self.date_debut = fonctions_controleur.date_maintenant()
        self.matchs = []

    def fin(self):
        self.date_fin = fonctions_controleur.date_maintenant()


class Match:

    def __init__(self, nom_tournoi, nom_tour, no_match, joueur1, joueur2):
        self.nom_tournoi = nom_tournoi
        self.nom_tour = nom_tour
        self.no_match = no_match
        self.date_debut = fonctions_controleur.date_maintenant()
        self.date_fin = ""
        self.joueur1 = joueur1
        self.joueur2 = joueur2
        self.gagnant = ""

    def joueur_gagnant(self, id_gagnant):
        self.gagnant = id_gagnant

    def fin(self):
        self.date_fin = fonctions_controleur.date_maintenant()
