# Model/Pion.py

from Model.Constantes import *


#
# Ce fichier implémente les données/fonctions concernant le pion
# dans le jeu du Puissance 4
#
# Un pion est caractérisé par :
# - sa couleur (const.ROUGE ou const.JAUNE)
# - un identifiant de type int (pour l'interface graphique)
#
# L'identifiant sera initialisé par défaut à None
#

def type_pion(pion: dict) -> bool:
    """
    Détermine si le paramètre peut être ou non un Pion

    :param pion: Paramètre dont on veut savoir si c'est un Pion ou non
    :return: True si le paramètre correspond à un Pion, False sinon.
    """
    return type(pion) == dict and len(pion) == 2 and const.COULEUR in pion.keys() \
        and const.ID in pion.keys() \
        and pion[const.COULEUR] in const.COULEURS \
        and (pion[const.ID] is None or type(pion[const.ID]) == int)


def construirePion(couleur: int) -> dict:
    """
    Construit un pion avec la couleur choisit et un identifiant

    :param couleur: Constante de la liste const.COULEURS
    :return: Un dictionnaire constituée d'une couleur et d'un identifiant
    """
    if type(couleur) != int:
        raise TypeError("construirePion : Le paramètre n'est pas de type entier")
    if couleur not in const.COULEURS:
        raise ValueError(f"construirePion : la couleur {couleur} n’est pas correcte")

    pion = {const.COULEUR: couleur, const.ID: None}
    return pion


def getCouleurPion(pion: dict) -> int:
    """
    Retourne la couleur du pion passée en paramètre

    :param pion: Dictionnaire composée d'une couleur et d'un identifiant
    :return: Retourne la couleur du pion
    """
    if not type_pion(pion):
        raise TypeError("getCouleurPion : Le paramètre n’est pas un pion")

    return pion[const.COULEUR]
