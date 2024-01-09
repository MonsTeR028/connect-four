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

print(test_plateau())


# Essais sur les couleurs
print("\x1B[43m \x1B[0m : carré jaune ")
print("\x1B[41m \x1B[0m : carré rouge ")
print("\x1B[41mA\x1B[0m : A sur fond rouge")
