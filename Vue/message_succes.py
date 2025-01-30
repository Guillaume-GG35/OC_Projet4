#!/usr/bin/env python3

from Controleur.constantes import CONSOLE


def fin_programme():
    print()
    CONSOLE.print("FIN DE PROGRAMME", style="bold yellow")
    print()
    exit()


def message_succes():
    CONSOLE.print("Votre demande a bien été validée", style="bold green")


def creation_fichier_db_tournoi(chemin_fichier):
    CONSOLE.print(
        f"Le fichier de données '{chemin_fichier}' a été créé avec succès.",
        style="bold green",
        end="\n\n",
    )


def fichier_ecrase(chemin_fichier):
    CONSOLE.print(
        f"Le fichier '{chemin_fichier}' ",
        "contenant les données du tournoi a été vidé.",
        style="bold green",
        end="\n\n",
    )


def sauvegarde(element):
    CONSOLE.print(
        f"Les données du {element} ont été sauvegardées.",
        style="bold green",
        end="\n\n",
    )
