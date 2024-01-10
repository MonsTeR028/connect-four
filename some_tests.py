from Model import Plateau
from Model.Constantes import *
from Model.Plateau import *
from Model.Pion import *
from Model.Joueur import *
from random import randint, choice


def test_plateau() -> None:
    plateau = construirePlateau()
    print(plateau)
    pion = construirePion(const.JAUNE)
    ligne = placerPionPlateau(plateau, pion, 2)
    print("Placement d’un pion en colonne 2. Numéro de ligne :", ligne)
    print(plateau)
    return None


# test_plateau()


def test_toStringPlateau() -> None:
    plateau = construirePlateau()
    for i in range(20):
        placerPionPlateau(plateau, construirePion(choice(const.COULEURS)), randint(0, const.NB_COLUMNS - 1))
    print(toStringPlateau(plateau))
    return None


# test_toStringPlateau()


def test_detecter4horizontalPlateau() -> None:
    plateau = construirePlateau()
    for i in range(20):
        placerPionPlateau(plateau, construirePion(choice(const.COULEURS)), randint(0, const.NB_COLUMNS - 1))
    print(toStringPlateau(plateau))
    print(detecter4horizontalPlateau(plateau, const.ROUGE))
    return None


# test_detecter4horizontalPlateau()


def test_detecter4verticalPlateau() -> None:
    plateau = construirePlateau()
    for i in range(20):
        placerPionPlateau(plateau, construirePion(choice(const.COULEURS)), randint(0, const.NB_COLUMNS - 1))
    print(toStringPlateau(plateau))
    print(detecter4verticalPlateau(plateau, const.ROUGE))
    return None


# test_detecter4verticalPlateau()


def test_detecter4diagonaleDirectePlateau() -> None:
    plateau = construirePlateau()
    for i in range(100):
        placerPionPlateau(plateau, construirePion(choice(const.COULEURS)), randint(0, const.NB_COLUMNS - 1))
    print(toStringPlateau(plateau))
    print(detecter4diagonaleDirectePlateau(plateau, const.ROUGE))
    return None


# test_detecter4diagonaleDirectePlateau()


def test_detecter4diagonaleIndirectePlateau() -> None:
    plateau = construirePlateau()
    for i in range(100):
        placerPionPlateau(plateau, construirePion(choice(const.COULEURS)), randint(0, const.NB_COLUMNS - 1))
    print(toStringPlateau(plateau))
    print(detecter4diagonaleIndirectePlateau(plateau, const.ROUGE))
    return None


# test_detecter4diagonaleIndirectePlateau()


def test_getPionsGagnantsPlateau() -> None:
    plateau = construirePlateau()
    for i in range(15):
        placerPionPlateau(plateau, construirePion(choice(const.COULEURS)), randint(0, const.NB_COLUMNS - 1))
    print(toStringPlateau(plateau))
    print(getPionsGagnantsPlateau(plateau))
    return None


# test_getPionsGagnantsPlateau()


def test_isRempliTableau() -> None:
    plateau = construirePlateau()
    for i in range(60):
        placerPionPlateau(plateau, construirePion(choice(const.COULEURS)), randint(0, const.NB_COLUMNS - 1))
    print(toStringPlateau(plateau))
    print(isRempliPlateau(plateau))
    return None


# test_isRempliTableau()


# Joueur
def test_construireJoueur() -> None:
    joueur = construireJoueur(const.JAUNE)
    print(joueur)
    return None


# test_construireJoueur()


def test_getCouleurJoueur() -> None:
    joueur = construireJoueur(const.ROUGE)
    print(joueur)
    print(getCouleurJoueur(joueur))
    return None


# test_getCouleurJoueur()


def test_getPlateauJoueur() -> None:
    joueur = construireJoueur(const.JAUNE)
    print(joueur)
    print(getPlateauJoueur(joueur))
    return None


test_getPlateauJoueur()
