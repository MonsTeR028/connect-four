from Model.Constantes import *
from Model.Pion import *
from Model.Plateau import *
from random import randint

#
# Ce fichier contient les fonctions gérant le joueur
#
# Un joueur sera un dictionnaire avec comme clé :
# - const.COULEUR : la couleur du joueur entre const.ROUGE et const.JAUNE
# - const.PLACER_PION : la fonction lui permettant de placer un pion, None par défaut,
#                       signifiant que le placement passe par l'interface graphique.
# - const.PLATEAU : référence sur le plateau de jeu, nécessaire pour l'IA, None par défaut
# - d'autres constantes nécessaires pour lui permettre de jouer à ajouter par la suite...
#

def type_joueur(joueur: dict) -> bool:
    """
    Détermine si le paramètre peut correspondre à un joueur.

    :param joueur: Paramètre à tester
    :return: True s'il peut correspondre à un joueur, False sinon.
    """
    if type(joueur) != dict:
        return False
    if const.COULEUR not in joueur or joueur[const.COULEUR] not in const.COULEURS:
        return False
    if const.PLACER_PION not in joueur or (joueur[const.PLACER_PION] is not None
                                           and not callable(joueur[const.PLACER_PION])):
        return False
    if const.PLATEAU not in joueur or (joueur[const.PLATEAU] is not None and
                                       not type_plateau(joueur[const.PLATEAU])):
        return False
    return True


def construireJoueur(couleur: int) -> dict:
    """
    Fonction qui permet de construire un joueur avec une couleur attribuer

    :param couleur: Constante parmi la liste const.COULEURS
    :return: Retourne un dictionnaire composée d'une couleur, d'un plateau et de placer pion
    """
    if type(couleur) != int:
        raise TypeError("construireJoueur : Le paramètre n’est pas un entier")
    if couleur not in const.COULEURS:
        raise ValueError(f"« construireJoueur : L’entier donné {couleur} n’est pas une couleur. ")

    joueur = {const.COULEUR: couleur, const.PLATEAU: None, const.PLACER_PION: None}
    return joueur


def getCouleurJoueur(joueur: dict) -> int:
    """
    Fonction qui permet de retourner la couleur d'un joueur

    :param joueur: Paramètre représenter par un dictionnaire composé d'une couleur, d'un plateau et de placer pion.
    :return: Retourne la couleur d'un joueur
    """
    if not type_joueur(joueur):
        raise TypeError("getCouleurJoueur : Le paramètre ne correspond pas à un joueur")

    return joueur[const.COULEUR]


def getPlateauJoueur(joueur: dict) -> list:
    """
    Fonction qui permet de retourner le plateau d'un joueur

    :param joueur: Paramètre représenter par un dictionnaire composé d'une couleur, d'un plateau et de placer pion.
    :return: Retourne le plateau d'un joueur
    """
    if not type_joueur(joueur):
        raise TypeError("getPlateauJoueur : Le paramètre ne correspond pas à un joueur")

    return joueur[const.PLATEAU]


def getPlacerPionJoueur(joueur: dict):
    """
    Fonction qui permet de retourner le placer pion d'un joueur

    :param joueur: Paramètre représenter par un dictionnaire composé d'une couleur, d'un plateau et de placer pion.
    :return: Retourne la fonction du dictionnaire de placer pion
    """
    if not type_joueur(joueur):
        raise TypeError("getPlacerPionJoueur : Le paramètre ne correspond pas à un joueur")

    return joueur[const.PLACER_PION]


def getPionJoueur(joueur: dict) -> dict:
    """
    Cette fonction construit un pion en fonction de la couleur du joueur et retourne ce pion.

    :param joueur: Paramètre représenter par un dictionnaire composé d'une couleur, d'un plateau et de placer pion.
    :return: Retourne le pion ainsi créé
    """
    if not type_joueur(joueur):
        raise TypeError("getPionJoueur : Le paramètre ne correspond pas à un joueur")

    pionJoueur = {const.COULEUR: joueur[const.COULEUR], const.ID: None}
    return pionJoueur


def setPlateauJoueur(joueur: dict, plateau: list) -> None:
    """
    Cette fonction « affecte » le plateau au joueur

    :param joueur: Paramètre représenter par un dictionnaire composé d'une couleur, d'un plateau et de placer pion.
    :param plateau: Tableau 2D (liste de listes), pouvant contenir des pions ou rien
    :return: Ne retourne rien
    """
    if not type_joueur(joueur):
        raise TypeError("setPlateauJoueur : Le premier paramètre ne correspond pas à un joueur")
    if not type_plateau(plateau):
        raise TypeError("setPlateauJoueur : Le second paramètre ne correspond pas à un plateau")

    joueur[const.PLATEAU] = plateau
    return None


def setPlacerPionJoueur(joueur: dict, fn) -> None:
    """
    Cette fonction « affecte » une fonction au joueur

    :param joueur: Paramètre représenté par un dictionnaire composé d'une couleur, d'un plateau et de placer pion.
    :param fn: Ce paramètre est une fonction que l'on veut affecter au joueur
    :return: Ne retourne rien
    """
    if not type_joueur(joueur):
        raise TypeError("setPlacerPionJoueur : Le premier paramètre ne correspond pas à un joueur")
    if not callable(fn):
        raise TypeError("setPlacerPionJoueur : le second paramètre n’est pas une fonction")

    joueur[const.PLACER_PION] = fn
    return None


def _placerPionJoueur(joueur: dict) -> int:
    """
    Cette fonction choisit un nombre aléatoire entre 0 et const.NB_COLUMNS – 1 tout en vérifiant que la colonne
    correspondante peut être jouée, qu’elle n’est pas remplie et le retourne.

    :param joueur: Paramètre représenté par un dictionnaire composé d'une couleur, d'un plateau et de placer pion.
    :return: Retourne un index de colonne aléatoire ou il possible de mettre un pion.
    """
    if not type_joueur(joueur):
        raise TypeError("_placerPionJoueur : Le paramètre n'est pas un joueur")

    if not isRempliPlateau(joueur[const.PLATEAU]):
        etat = True
        while etat:
            colonne = randint(0, const.NB_COLUMNS - 1)
            if joueur[const.PLATEAU][0][colonne] is None:
                return colonne


def initialiserIAJoueur(joueur: dict, booleen: bool) -> None:
    """
    Cette fonction affecte la fonction _placerPionJoueur à un joueur

    :param joueur: Paramètre représenté par un dictionnaire composé d'une couleur, d'un plateau et de placer pion.
    :param booleen: Booléen indiquant si le joueur joue en premier (True) ou en second (False).
    (sert dans une autre fonction)
    :return: Ne retourne rien
    """
    if not type_joueur(joueur):
        raise TypeError("initialiserIAJoueur : Le premier paramètre n'est pas un joueur")
    if type(booleen) != bool:
        raise TypeError("initialiserIAJoueur : Le second paramètre n'est pas un booléen")

    setPlacerPionJoueur(joueur, _placerPionJoueur)
    return None
