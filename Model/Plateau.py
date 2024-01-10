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
    if next((wrong for line in plateau for c in line if not (c is None) and not type_pion(c)), True) == wrong:
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
    if colonne < 0 or colonne > const.NB_COLUMNS - 1:
        raise ValueError(f"placerPionPlateau : La valeur de la colonne {colonne} n’est pas correcte")

    rep = 0
    if plateau[0][colonne] is None:
        plateau[0][colonne] = pion
    else:
        rep = -1
    for lignes in range(1, const.NB_LINES):
        if plateau[lignes][colonne] is None:
            plateau[lignes][colonne] = pion
            plateau[lignes - 1][colonne] = None
            rep = lignes
    return rep


def toStringPlateau(plateau: list) -> str:
    """
    Transforme un plateau en texte ordonnée et lisible
    :param plateau: Tableau 2D (liste de listes), pouvant contenir des pions ou rien
    :return: Retourne une chaîne de caractère représentant le plateau
    """
    if not type_plateau(plateau):
        raise TypeError("toStringPlateau : Le paramètre n'est pas un plateau")

    resultat = ""
    for lignes in range(const.NB_LINES):
        for colonnes in range(const.NB_COLUMNS):
            if plateau[lignes][colonnes] is None:
                resultat += "| "
            else:
                if plateau[lignes][colonnes][const.COULEUR] == const.JAUNE:
                    resultat += "|\x1B[43m \x1B[0m"
                else:
                    resultat += "|\x1B[41m \x1B[0m"
        resultat += f"| {lignes}\n"
    resultat += " 0 1 2 3 4 5 6"
    return resultat


def detecter4horizontalPlateau(plateau: list, couleur: int) -> list:
    """
    Retourne toutes les séries de 4 pions alignés horizontalement à la suite

    :param plateau: Tableau 2D (liste de listes), pouvant contenir des pions ou rien
    :param couleur: Constante parmi la liste const.COULEURS
    :return: Retourne une liste de listes de toutes les séries de 4 pions alignés horizontalement,
    si aucune série de 4 pions retourne une liste vide
    """
    if not type_plateau(plateau):
        raise TypeError("detecter4horizontalPlateau : Le premier paramètre ne correspond pas à un plateau")
    if type(couleur) != int:
        raise TypeError("detecter4horizontalPlateau : le second paramètre n’est pas un entier")
    if couleur not in const.COULEURS:
        raise ValueError(f"detecter4horizontalPlateau : La valeur de la couleur {couleur} n’est pas correcte")

    pions = 0
    liste = []
    listeFinale = []
    for lignes in range(const.NB_LINES):
        for colonnes in range(const.NB_COLUMNS):
            if plateau[lignes][colonnes] is None:
                pions = 0
                liste = []
            elif plateau[lignes][colonnes][const.COULEUR] == couleur:
                pions += 1
                liste.append(plateau[lignes][colonnes])
            else:
                pions = 0
                liste = []
            if pions == 4:
                listeFinale.extend(liste)
                pions = 0
                liste = []
        pions = 0
        liste = []
    return listeFinale


def detecter4verticalPlateau(plateau: list, couleur: int) -> list:
    """
    Retourne toutes les séries de 4 pions alignés verticalement à la suite

    :param plateau: Tableau 2D (liste de listes), pouvant contenir des pions ou rien
    :param couleur: Constante parmi la liste const.COULEURS
    :return: Retourne une liste de listes de toutes les séries de 4 pions alignés verticalement,
    si aucune série de 4 pions retourne une liste vide
    """
    if not type_plateau(plateau):
        raise TypeError("detecter4verticalPlateau : Le premier paramètre ne correspond pas à un plateau")
    if type(couleur) != int:
        raise TypeError("detecter4verticalPlateau : le second paramètre n’est pas un entier")
    if couleur not in const.COULEURS:
        raise ValueError(f"detecter4verticalPlateau : La valeur de la couleur {couleur} n’est pas correcte")

    pions = 0
    liste = []
    listeFinale = []

    for colonnes in range(const.NB_COLUMNS):
        for lignes in range(const.NB_LINES):
            if plateau[lignes][colonnes] is None:
                pions = 0
                liste = []
            elif plateau[lignes][colonnes][const.COULEUR] == couleur:
                pions += 1
                liste.append(plateau[lignes][colonnes])
            else:
                pions = 0
                liste.append(plateau[lignes][colonnes])
            if pions == 4:
                listeFinale.extend(liste)
                pions = 0
                liste = []
        pions = 0
        liste = []
    return listeFinale


def detecter4diagonaleDirectePlateau(plateau: list, couleur: int) -> list:
    """
        Retourne toutes les séries de 4 pions alignés en diagonales directes à la suite

        :param plateau: Tableau 2D (liste de listes), pouvant contenir des pions ou rien
        :param couleur: Constante parmi la liste const.COULEURS
        :return: Retourne une liste de listes de toutes les séries de 4 pions alignés en diagonales directes,
        si aucune série de 4 pions retourne une liste vide
        """
    if not type_plateau(plateau):
        raise TypeError("detecter4diagonaleDirectePlateau : Le premier paramètre ne correspond pas à un plateau")
    if type(couleur) != int:
        raise TypeError("detecter4diagonaleDirectePlateau : le second paramètre n’est pas un entier")
    if couleur not in const.COULEURS:
        raise ValueError(f"detecter4diagonaleDirectePlateau : La valeur de la couleur {couleur} n’est pas correcte")

    liste = []
    listeFinale = []
    listeBloquer = []

    for lignes in range(const.NB_LINES-3):
        for colonnes in range(const.NB_COLUMNS-3):
            if plateau[lignes][colonnes] is not None and plateau[lignes][colonnes][const.COULEUR] == couleur \
                    and (lignes, colonnes) not in listeBloquer:
                liste.append(plateau[lignes][colonnes])
                for i in range(3):
                    if plateau[lignes+i+1][colonnes+i+1] is not None \
                            and plateau[lignes+i+1][colonnes+i+1][const.COULEUR] == couleur:
                        liste.append(plateau[lignes+i+1][colonnes+i+1])
                        listeBloquer.append((lignes+i+1, colonnes+i+1))
                if len(liste) == 4:
                    listeFinale.extend(liste)
            liste = []
    return listeFinale

def detecter4diagonaleIndirectePlateau(plateau: list, couleur: int) -> list:
    """
        Retourne toutes les séries de 4 pions alignés en diagonales indirectes à la suite

        :param plateau: Tableau 2D (liste de listes), pouvant contenir des pions ou rien
        :param couleur: Constante parmi la liste const.COULEURS
        :return: Retourne une liste de listes de toutes les séries de 4 pions alignés en diagonales indirectes,
        si aucune série de 4 pions retourne une liste vide
        """
    if not type_plateau(plateau):
        raise TypeError("detecter4diagonaleindirectePlateau : Le premier paramètre ne correspond pas à un plateau")
    if type(couleur) != int:
        raise TypeError("detecter4diagonaleindirectePlateau : le second paramètre n’est pas un entier")
    if couleur not in const.COULEURS:
        raise ValueError(f"detecter4diagonaleindirectePlateau : La valeur de la couleur {couleur} n’est pas correcte")

    liste = []
    listeFinale = []
    listeBloquer = []

    for lignes in range(const.NB_LINES-1, const.NB_LINES-4, -1):
        for colonnes in range(const.NB_COLUMNS-3):
            if plateau[lignes][colonnes] is not None and plateau[lignes][colonnes][const.COULEUR] == couleur \
                    and (lignes, colonnes) not in listeBloquer:
                liste.append(plateau[lignes][colonnes])
                for i in range(3):
                    if plateau[lignes-i-1][colonnes+i+1] is not None \
                            and plateau[lignes-i-1][colonnes+i+1][const.COULEUR] == couleur:
                        liste.append(plateau[lignes-i-1][colonnes+i+1])
                        listeBloquer.append((lignes-i-1, colonnes+i+1))
                if len(liste) == 4:
                    listeFinale.extend(liste)
            liste = []
    return listeFinale


def getPionsGagnantsPlateau(plateau: list) -> list:
    """
    Fonction qui retourne toutes les suites de 4 possibles (verticales, horizontales et les deux diagonales)
    pour les deux couleurs de pion

    :param plateau: Tableau 2D (liste de listes), pouvant contenir des pions ou rien
    :return: Retourne une liste de listes de toutes les séries de 4 pions alignés que ce soit horizontalement,
    verticalement, ou diagonalement pour les deux couleurs
    et si aucune série de 4 pions n'existe retourne une liste vide.
    """
    if not type_plateau(plateau):
        raise TypeError("getPionsGagnantsPlateau : Le paramètre n’est pas un plateau")

    liste = []
    liste.extend(detecter4horizontalPlateau(plateau, const.ROUGE))
    liste.extend(detecter4horizontalPlateau(plateau, const.JAUNE))
    liste.extend(detecter4horizontalPlateau(plateau, const.ROUGE))
    liste.extend(detecter4verticalPlateau(plateau, const.JAUNE))
    liste.extend(detecter4verticalPlateau(plateau, const.ROUGE))
    liste.extend(detecter4diagonaleDirectePlateau(plateau, const.JAUNE))
    liste.extend(detecter4diagonaleDirectePlateau(plateau, const.ROUGE))
    liste.extend(detecter4diagonaleIndirectePlateau(plateau, const.JAUNE))
    liste.extend(detecter4diagonaleIndirectePlateau(plateau, const.ROUGE))
    return liste


def isRempliPlateau(plateau: list) -> bool:
    """
    La fonction reçoit en paramètre un plateau et qui retourne True si le plateau est complètement rempli de pions,
     False sinon.

    :param plateau: Tableau 2D (liste de listes), pouvant contenir des pions ou rien
    :return: Retourne True si le plateau est complètement rempli de pions,
     False sinon.
    """
    if not type_plateau(plateau):
        raise TypeError("isRempliTableau : Le paramètre n’est pas un plateau")

    res = True
    for i in range(const.NB_COLUMNS):
        if plateau[0][i] is None:
            res = False
    return res
