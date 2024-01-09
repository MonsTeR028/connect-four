from Model.Constantes import *
from Model.Pion import *


#
# Le plateau représente la grille où sont placés les pions.
# Il constitue le coeur du jeu car c'est dans ce fichier
# où vont être programmées toutes les règles du jeu.
#
# Un plateau sera simplement une liste de liste.
# Ce sera en fait une liste de lignes.
# Les cases du plateau ne pourront contenir que None ou un pion
#
# Pour améliorer la "rapidité" du programme, il n'y aura aucun test sur les paramètres.
# (mais c'est peut-être déjà trop tard car les tests sont fait en amont, ce qui ralentit le programme...)
#

def type_plateau(plateau: list) -> bool:
    """
    Permet de vérifier que le paramètre correspond à un plateau.
    Renvoie True si c'est le cas, False sinon.

    :param plateau: Objet qu'on veut tester
    :return: True s'il correspond à un plateau, False sinon
    """
    if type(plateau) != list:
        return False
    if len(plateau) != const.NB_LINES:
        return False
    wrong = "Erreur !"
    if next((wrong for line in plateau if type(line) != list or len(line) != const.NB_COLUMNS), True) == wrong:
        return False
    if next((wrong for line in plateau for c in line if not(c is None) and not type_pion(c)), True) == wrong:
        return False
    return True


def construirePlateau() -> list:
    """
    Crée un plateau (tableau 2D) vide
    :return: Retourne une liste de liste vide représentant le plateau
    """
    plateau = []
    for lignes in range(const.NB_LINES):
        plateau.append([])
        for colonnes in range(const.NB_COLUMNS):
            plateau[lignes].append(None)
    return plateau


def placerPionPlateau(plateau: list, pion: dict, colonne: int) -> int:
    """
    Place un pion dans une colonne donnée et retourne la ligne ou le pion retombe

    :param plateau: Tableau 2D (liste de listes), pouvant contenir des pions ou rien
    :param pion: Dictionnaire composée d'une couleur et d'un identifiant
    :param colonne: Numéro de colonne choisit entre 0 et const.NB_COLUMNS-1
    :return: retourne la ligne ou le pion tombe
    """
    if not type_plateau(plateau):
        raise TypeError("placerPionPlateau : Le premier paramètre ne correspond pas à un plateau")
    if not type_pion(pion):
        raise TypeError("placerPionPlateau : Le second paramètre n'est pas un pion")
    if type(colonne) is not int:
        raise TypeError("placerPionPlateau : Le troisième paramètre n'est pas un entier")
    if colonne < 0 or colonne > const.NB_COLUMNS-1:
        raise ValueError(f"placerPionPlateau : La valeur de la colonne {colonne} n’est pas correcte")

    rep = 0
    if plateau[0][colonne] is None:
        plateau[0][colonne] = pion
    else:
        rep = -1
    for lignes in range(1, len(plateau)):
        if plateau[lignes][colonne] is None:
            plateau[lignes][colonne] = pion
            plateau[lignes - 1][colonne] = None
            rep = lignes
    return rep
