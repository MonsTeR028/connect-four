from Model.Constantes import *
from Model.Plateau import *
from Model.Pion import *
from random import randint, choice


def test_plateau() -> None:
    plateau = construirePlateau()
    print(plateau)
    pion = construirePion(const.JAUNE)
    ligne = placerPionPlateau(plateau, pion, 2)
    print("Placement d’un pion en colonne 2. Numéro de ligne :", ligne)
    print(plateau)
    return None

#test_plateau()


def test_toStringPlateau() -> None:
    plateau = construirePlateau()
    for i in range(20):
        placerPionPlateau(plateau, construirePion(choice(const.COULEURS)), randint(0, const.NB_COLUMNS - 1))
    print(toStringPlateau(plateau))
    return None

test_toStringPlateau()
