from Model.Constantes import *
from Model.Joueur import *
from random import randint
from Model.Plateau import toStringPlateau


def initialiserColonnes() -> dict:
    coups = {}
    for colonne in range(const.NB_COLUMNS):
        coups[colonne] = 0
    return coups


def isColonneValide(joueur: dict, colonne: int) -> bool:
    if type(colonne) != int:
        raise TypeError("isColonneValide : Le second paramètre n'est pas un entier")
    if colonne < 0 or colonne > const.NB_COLUMNS - 1:
        raise ValueError(f"isColonneValide : La valeur de la colonne '{colonne}' est en dehors du plateau")

    estValide = False
    if joueur[const.PLATEAU][0][colonne] is None:
        estValide = True
    return estValide


def verifierColonnesPossibles(joueur: dict, listeColonnes: dict) -> dict:
    listeDeletion = []
    for colonne in listeColonnes.keys():
        if not isColonneValide(joueur, colonne):
            listeDeletion.append(colonne)
    while len(listeDeletion) > 0:
        del listeColonnes[listeDeletion[0]]
        del listeDeletion[0]
    return listeColonnes


def couleurAdverse(joueur: dict) -> object:
    couleur = const.JAUNE
    if joueur[const.COULEUR] == const.JAUNE:
        couleur = const.ROUGE
    return couleur


def detecter3horizontaleAdversaire(joueur: dict) -> list:
    pions = 0
    liste = []
    listeFinale = []
    for lignes in range(const.NB_LINES):
        for colonnes in range(const.NB_COLUMNS):
            if joueur[const.PLATEAU][lignes][colonnes] is None:
                pions = 0
                liste = []
            elif joueur[const.PLATEAU][lignes][colonnes][const.COULEUR] == couleurAdverse(joueur):
                pions += 1
                liste.append((lignes, colonnes))
            else:
                pions = 0
                liste = []
            if pions == 3:
                listeFinale.append(liste)
                pions = 0
                liste = []
        pions = 0
        liste = []
    return listeFinale


def valeurAjouterHorizontaleAdversaire(joueur: dict, listeColonnes: dict) -> dict:
    # Ajout du poids pour la colonne sur le point de faire un puissance 4 horizontale
    listeP3 = detecter3horizontaleAdversaire(joueur)
    if len(listeP3) > 0:
        for P3 in range(len(listeP3)):
            if listeP3[P3][0][1] > 0:
                if joueur[const.PLATEAU][listeP3[P3][0][0]][listeP3[P3][0][1]-1] is None:
                    listeColonnes[listeP3[P3][0][1]-1] += 100
                if listeP3[P3][0][0] < const.NB_LINES - 1:
                    if joueur[const.PLATEAU][listeP3[P3][0][0]+1][listeP3[P3][0][1]-1] is None:
                        listeColonnes[listeP3[P3][0][1] - 1] -= 100
            if listeP3[P3][-1][1] < const.NB_COLUMNS - 1:
                if joueur[const.PLATEAU][listeP3[P3][-1][0]][listeP3[P3][-1][1]+1] is None:
                    listeColonnes[listeP3[P3][-1][1]+1] += 95
                if listeP3[P3][-1][0] < const.NB_LINES - 1:
                    if joueur[const.PLATEAU][listeP3[P3][-1][0]+1][listeP3[P3][-1][1]+1] is None:
                        listeColonnes[listeP3[P3][-1][1] + 1] -= 95
                if listeP3[P3][-1][1] < const.NB_LINES - 2:
                    if couleurAdverse(joueur) == \
                            joueur[const.PLATEAU][listeP3[P3][-1][0]][listeP3[P3][-1][1] + 2][const.COULEUR]:
                        listeColonnes[listeP3[P3][-1][1] + 1] += 95

    return listeColonnes


def detecter3verticalAdversaire(joueur: dict) -> list:
    pions = 0
    liste = []
    listeFinale = []


    for colonnes in range(const.NB_COLUMNS):
        for lignes in range(const.NB_LINES):
            if joueur[const.PLATEAU][lignes][colonnes] is None:
                pions = 0
                liste = []
            elif joueur[const.PLATEAU][lignes][colonnes][const.COULEUR] == couleurAdverse(joueur):
                pions += 1
                liste.append((lignes, colonnes))
            else:
                pions = 0
                liste = []
            if pions == 3:
                listeFinale.append(liste)
                pions = 0
                liste = []
        pions = 0
        liste = []
    return listeFinale


def valeurAjouterVerticalAdversaire(joueur: dict, listeColonnes: dict) -> dict:
    listeP3 = detecter3verticalAdversaire(joueur)
    if len(listeP3) > 0:
        for P3 in range(len(listeP3)):
            if joueur[const.PLATEAU][listeP3[P3][0][0]-1][listeP3[P3][0][1]] is None:
                listeColonnes[listeP3[P3][0][1]] += 80
    return listeColonnes


def detecter3diagonaleDirecteAdversaire(joueur: dict) -> list:
    liste = []
    listeFinale = []
    listeBloquer = []

    for lignes in range(const.NB_LINES - 2):
        for colonnes in range(const.NB_COLUMNS - 2):
            if joueur[const.PLATEAU][lignes][colonnes] is not None \
                    and joueur[const.PLATEAU][lignes][colonnes][const.COULEUR] == couleurAdverse(joueur) \
                    and (lignes, colonnes) not in listeBloquer:
                liste.append((lignes, colonnes))
                for i in range(2):
                    if joueur[const.PLATEAU][lignes + i + 1][colonnes + i + 1] is not None \
                            and joueur[const.PLATEAU][lignes+i+1][colonnes+i+1][const.COULEUR]==couleurAdverse(joueur):
                        liste.append((lignes + i + 1, colonnes + i + 1))
                        listeBloquer.append((lignes + i + 1, colonnes + i + 1))
                if len(liste) == 3:
                    listeFinale.append(liste)
            liste = []
    return listeFinale


def valeurAjouterDiagonaleDirecteAdversaire(joueur: dict, listeColonnes: dict) -> dict:
    listeP3 = detecter3diagonaleDirecteAdversaire(joueur)
    if len(listeP3) > 0:
        for P3 in range(len(listeP3)):
            if listeP3[P3][0][0]-1 > 0 and listeP3[P3][0][1] > 0:
                if joueur[const.PLATEAU][listeP3[P3][0][0]-1][listeP3[P3][0][1]-1] is None:
                    listeColonnes[listeP3[P3][0][1]-1] += 90
                if joueur[const.PLATEAU][listeP3[P3][0][0]][listeP3[P3][0][1]-1] is None:
                    listeColonnes[listeP3[P3][0][1]-1] -= 900
            if listeP3[P3][-1][0] < const.NB_LINES - 1 and listeP3[P3][-1][1] < const.NB_COLUMNS - 1:
                if joueur[const.PLATEAU][listeP3[P3][-1][0]+1][listeP3[P3][-1][1]+1] is None:
                    listeColonnes[listeP3[P3][-1][1]+1] += 85
                if listeP3[P3][-1][0] > const.NB_LINES - 2:
                    if joueur[const.PLATEAU][listeP3[P3][-1][0]+2][listeP3[P3][-1][1]+1] is None:
                        listeColonnes[listeP3[P3][-1][1]+1] -= 850

    return listeColonnes


def detecter3diagonaleIndirecteAdversaire(joueur: dict) -> list:
    liste = []
    listeFinale = []
    listeBloquer = []

    for lignes in range(const.NB_LINES-1, const.NB_LINES-5, -1):
        for colonnes in range(const.NB_COLUMNS-2):
            if joueur[const.PLATEAU][lignes][colonnes] is not None \
                    and joueur[const.PLATEAU][lignes][colonnes][const.COULEUR] == couleurAdverse(joueur) \
                    and (lignes, colonnes) not in listeBloquer:
                liste.append((lignes, colonnes))
                for i in range(2):
                    if joueur[const.PLATEAU][lignes-i-1][colonnes+i+1] is not None \
                            and joueur[const.PLATEAU][lignes-i-1][colonnes+i+1][const.COULEUR]==couleurAdverse(joueur):
                        liste.append((lignes-i-1, colonnes+i+1))
                        listeBloquer.append((lignes-i-1, colonnes+i+1))
                if len(liste) == 3:
                    listeFinale.append(liste)
            liste = []
    return listeFinale


def valeurAjouterDiagonaleIndirecteAdversaire(joueur: dict, listeColonnes: dict) -> dict:
    listeP3 = detecter3diagonaleIndirecteAdversaire(joueur)
    if len(listeP3) > 0:
        for P3 in range(len(listeP3)):
            if listeP3[P3][0][0] < const.NB_LINES - 1 and listeP3[P3][0][0] > 0:
                if joueur[const.PLATEAU][listeP3[P3][0][0]+1][listeP3[P3][0][1]-1] is None:
                    listeColonnes[listeP3[P3][0][1]-1] += 92
                if listeP3[P3][0][0] < const.NB_LINES - 2:
                    if joueur[const.PLATEAU][listeP3[P3][0][0]+2][listeP3[P3][0][1]-1] is None:
                        listeColonnes[listeP3[P3][0][0]-2] -= 920
            if listeP3[P3][-1][0] > 1 and listeP3[P3][-1][1] < const.NB_COLUMNS - 1:
                if joueur[const.PLATEAU][listeP3[P3][-1][0]-1][listeP3[P3][-1][1]+1] is None:
                    listeColonnes[listeP3[P3][-1][1]+1] += 91
                if joueur[const.PLATEAU][listeP3[P3][-1][0]][listeP3[P3][-1][1]+1] is None:
                    listeColonnes[listeP3[P3][-1][1]+1] -= 910

    return listeColonnes


def detecter3horizontale(joueur: dict) -> list:
    pions = 0
    liste = []
    listeFinale = []
    for lignes in range(const.NB_LINES):
        for colonnes in range(const.NB_COLUMNS):
            if joueur[const.PLATEAU][lignes][colonnes] is None:
                pions = 0
                liste = []
            elif joueur[const.PLATEAU][lignes][colonnes][const.COULEUR] == joueur[const.COULEUR]:
                pions += 1
                liste.append((lignes, colonnes))
            else:
                pions = 0
                liste = []
            if pions == 3:
                listeFinale.append(liste)
                pions = 0
                liste = []
        pions = 0
        liste = []
    return listeFinale


def valeurAjouterHorizontale(joueur: dict, listeColonnes: dict) -> dict:
    # Ajout du poids pour la colonne sur le point de faire un puissance 4 horizontale
    listeP3 = detecter3horizontale(joueur)
    if len(listeP3) > 0:
        for P3 in range(len(listeP3)):
            if listeP3[P3][0][1] > 0:
                if joueur[const.PLATEAU][listeP3[P3][0][0]][listeP3[P3][0][1]-1] is None:
                    listeColonnes[listeP3[P3][0][1]-1] += 1000
                if listeP3[P3][0][0] < const.NB_LINES - 1:
                    if joueur[const.PLATEAU][listeP3[P3][0][0]+1][listeP3[P3][0][1]-1] is None:
                        listeColonnes[listeP3[P3][0][1] - 1] -= 1000
            if listeP3[P3][-1][1] < const.NB_COLUMNS - 1:
                if joueur[const.PLATEAU][listeP3[P3][-1][0]][listeP3[P3][-1][1]+1] is None:
                    listeColonnes[listeP3[P3][-1][1]+1] += 950
                if listeP3[P3][-1][0] < const.NB_LINES - 1:
                    if joueur[const.PLATEAU][listeP3[P3][-1][0]+1][listeP3[P3][-1][1]+1] is None:
                        listeColonnes[listeP3[P3][-1][1] + 1] -= 950

    return listeColonnes


def detecter3vertical(joueur: dict) -> list:
    pions = 0
    liste = []
    listeFinale = []


    for colonnes in range(const.NB_COLUMNS):
        for lignes in range(const.NB_LINES):
            if joueur[const.PLATEAU][lignes][colonnes] is None:
                pions = 0
                liste = []
            elif joueur[const.PLATEAU][lignes][colonnes][const.COULEUR] == joueur[const.COULEUR]:
                pions += 1
                liste.append((lignes, colonnes))
            else:
                pions = 0
                liste = []
            if pions == 3:
                listeFinale.append(liste)
                pions = 0
                liste = []
        pions = 0
        liste = []
    return listeFinale


def valeurAjouterVertical(joueur: dict, listeColonnes: dict) -> dict:
    listeP3 = detecter3vertical(joueur)
    if len(listeP3) > 0:
        for P3 in range(len(listeP3)):
            if joueur[const.PLATEAU][listeP3[P3][0][0]-1][listeP3[P3][0][1]] is None:
                listeColonnes[listeP3[P3][0][1]] += 800
    return listeColonnes


def placerPionAleatoire(joueur: dict) -> int:
    if not isRempliPlateau(joueur[const.PLATEAU]):
        etat = True
        while etat:
            colonne = randint(0, const.NB_COLUMNS - 1)
            if joueur[const.PLATEAU][0][colonne] is None:
                return colonne


def detecter3diagonaleDirecte(joueur: dict) -> list:
    liste = []
    listeFinale = []
    listeBloquer = []

    for lignes in range(const.NB_LINES - 2):
        for colonnes in range(const.NB_COLUMNS - 2):
            if joueur[const.PLATEAU][lignes][colonnes] is not None \
                    and joueur[const.PLATEAU][lignes][colonnes][const.COULEUR] == joueur[const.COULEUR] \
                    and (lignes, colonnes) not in listeBloquer:
                liste.append((lignes, colonnes))
                for i in range(2):
                    if joueur[const.PLATEAU][lignes + i + 1][colonnes + i + 1] is not None \
                            and joueur[const.PLATEAU][lignes+i+1][colonnes+i+1][const.COULEUR] == joueur[const.COULEUR]:
                        liste.append((lignes + i + 1, colonnes + i + 1))
                        listeBloquer.append((lignes + i + 1, colonnes + i + 1))
                if len(liste) == 3:
                    listeFinale.append(liste)
            liste = []
    return listeFinale


def valeurAjouterDiagonaleDirecte(joueur: dict, listeColonnes: dict) -> dict:
    listeP3 = detecter3diagonaleDirecte(joueur)
    if len(listeP3) > 0:
        for P3 in range(len(listeP3)):
            if listeP3[P3][0][0]-1 > 0 and listeP3[P3][0][1] > 0:
                if joueur[const.PLATEAU][listeP3[P3][0][0]-1][listeP3[P3][0][1]-1] is None:
                    listeColonnes[listeP3[P3][0][1]-1] += 900
                if joueur[const.PLATEAU][listeP3[P3][0][0]][listeP3[P3][0][1]-1] is None:
                    listeColonnes[listeP3[P3][0][1]-1] -= 900
            if listeP3[P3][-1][0] < const.NB_LINES - 1 and listeP3[P3][-1][1] < const.NB_COLUMNS - 1:
                if joueur[const.PLATEAU][listeP3[P3][-1][0]+1][listeP3[P3][-1][1]+1] is None:
                    listeColonnes[listeP3[P3][-1][1]+1] += 850
                if listeP3[P3][-1][0] > const.NB_LINES - 2:
                    if joueur[const.PLATEAU][listeP3[P3][-1][0]+2][listeP3[P3][-1][1]+1] is None:
                        listeColonnes[listeP3[P3][-1][1]+1] -= 850

    return listeColonnes


def detecter3diagonaleIndirecte(joueur: dict) -> list:
    liste = []
    listeFinale = []
    listeBloquer = []

    for lignes in range(const.NB_LINES-1, const.NB_LINES-5, -1):
        for colonnes in range(const.NB_COLUMNS-2):
            if joueur[const.PLATEAU][lignes][colonnes] is not None \
                    and joueur[const.PLATEAU][lignes][colonnes][const.COULEUR] == joueur[const.COULEUR] \
                    and (lignes, colonnes) not in listeBloquer:
                liste.append((lignes, colonnes))
                for i in range(2):
                    if joueur[const.PLATEAU][lignes-i-1][colonnes+i+1] is not None \
                            and joueur[const.PLATEAU][lignes-i-1][colonnes+i+1][const.COULEUR] == joueur[const.COULEUR]:
                        liste.append((lignes-i-1, colonnes+i+1))
                        listeBloquer.append((lignes-i-1, colonnes+i+1))
                if len(liste) == 3:
                    listeFinale.append(liste)
            liste = []
    return listeFinale


def valeurAjouterDiagonaleIndirecte(joueur: dict, listeColonnes: dict) -> dict:
    listeP3 = detecter3diagonaleIndirecte(joueur)
    if len(listeP3) > 0:
        for P3 in range(len(listeP3)):
            if listeP3[P3][0][0] < const.NB_LINES - 1 and listeP3[P3][0][0] > 0:
                if joueur[const.PLATEAU][listeP3[P3][0][0]+1][listeP3[P3][0][1]-1] is None:
                    listeColonnes[listeP3[P3][0][1]-1] += 920
                if listeP3[P3][0][0] < const.NB_LINES - 2:
                    if joueur[const.PLATEAU][listeP3[P3][0][0]+2][listeP3[P3][0][1]-1] is None:
                        listeColonnes[listeP3[P3][0][0]-2] -= 920
            if listeP3[P3][-1][0] > 1 and listeP3[P3][-1][1] < const.NB_COLUMNS - 1:
                if joueur[const.PLATEAU][listeP3[P3][-1][0]-1][listeP3[P3][-1][1]+1] is None:
                    listeColonnes[listeP3[P3][-1][1]+1] += 910
                if joueur[const.PLATEAU][listeP3[P3][-1][0]][listeP3[P3][-1][1]+1] is None:
                    listeColonnes[listeP3[P3][-1][1]+1] -= 910

    return listeColonnes


def detecter2horizontaleAdversaire(joueur: dict) -> list:
    pions = 0
    liste = []
    listeFinale = []
    for lignes in range(const.NB_LINES):
        for colonnes in range(const.NB_COLUMNS):
            if joueur[const.PLATEAU][lignes][colonnes] is None:
                pions = 0
                liste = []
            elif joueur[const.PLATEAU][lignes][colonnes][const.COULEUR] == couleurAdverse(joueur):
                pions += 1
                liste.append((lignes, colonnes))
            else:
                pions = 0
                liste = []
            if pions == 2:
                listeFinale.append(liste)
                pions = 0
                liste = []
        pions = 0
        liste = []
    return listeFinale


def valeurAjouter2HorizontaleAdversaire(joueur: dict, listeColonnes: dict) -> dict:
    listeP3 = detecter2horizontaleAdversaire(joueur)
    if len(listeP3) > 0:
        for P3 in range(len(listeP3)):
            if listeP3[P3][0][1] > 0:
                if joueur[const.PLATEAU][listeP3[P3][0][0]][listeP3[P3][0][1]-1] is None:
                    listeColonnes[listeP3[P3][0][1]-1] += 20
                if listeP3[P3][0][0] < const.NB_LINES - 1:
                    if joueur[const.PLATEAU][listeP3[P3][0][0]+1][listeP3[P3][0][1]-1] is None:
                        listeColonnes[listeP3[P3][0][1] - 1] -= 20
            if listeP3[P3][-1][1] < const.NB_COLUMNS - 1:
                if joueur[const.PLATEAU][listeP3[P3][-1][0]][listeP3[P3][-1][1]+1] is None:
                    listeColonnes[listeP3[P3][-1][1]+1] += 18
                if listeP3[P3][-1][0] < const.NB_LINES - 1:
                    if joueur[const.PLATEAU][listeP3[P3][-1][0]+1][listeP3[P3][-1][1]+1] is None:
                        listeColonnes[listeP3[P3][-1][1] + 1] -= 18

    return listeColonnes


def detecter2verticalAdversaire(joueur: dict) -> list:
    pions = 0
    liste = []
    listeFinale = []


    for colonnes in range(const.NB_COLUMNS):
        for lignes in range(const.NB_LINES):
            if joueur[const.PLATEAU][lignes][colonnes] is None:
                pions = 0
                liste = []
            elif joueur[const.PLATEAU][lignes][colonnes][const.COULEUR] == couleurAdverse(joueur):
                pions += 1
                liste.append((lignes, colonnes))
            else:
                pions = 0
                liste = []
            if pions == 2:
                listeFinale.append(liste)
                pions = 0
                liste = []
        pions = 0
        liste = []
    return listeFinale


def valeurAjouter2VerticalAdversaire(joueur: dict, listeColonnes: dict) -> dict:
    listeP3 = detecter2verticalAdversaire(joueur)
    if len(listeP3) > 0:
        for P3 in range(len(listeP3)):
            if joueur[const.PLATEAU][listeP3[P3][0][0]-1][listeP3[P3][0][1]] is None:
                listeColonnes[listeP3[P3][0][1]] += 10
    return listeColonnes


def colonneFinale(joueur: dict) -> int:
    colonnesPossibles = verifierColonnesPossibles(joueur, initialiserColonnes())
    colonnesPossibles = valeurAjouterHorizontaleAdversaire(joueur, colonnesPossibles)
    colonnesPossibles = valeurAjouterVerticalAdversaire(joueur, colonnesPossibles)
    colonnesPossibles = valeurAjouterDiagonaleDirecteAdversaire(joueur, colonnesPossibles)
    colonnesPossibles = valeurAjouterDiagonaleIndirecteAdversaire(joueur, colonnesPossibles)
    colonnesPossibles = valeurAjouterHorizontale(joueur, colonnesPossibles)
    colonnesPossibles = valeurAjouterVertical(joueur, colonnesPossibles)
    colonnesPossibles = valeurAjouterDiagonaleDirecte(joueur, colonnesPossibles)
    colonnesPossibles = valeurAjouter2HorizontaleAdversaire(joueur, colonnesPossibles)
    colonnesPossibles = valeurAjouter2VerticalAdversaire(joueur, colonnesPossibles)

    poidsMaxi = 0
    coupsFinal = 0

    for colonne in colonnesPossibles.items():
        if colonne[1] > poidsMaxi:
            poidsMaxi = colonne[1]
            coupsFinal = colonne[0]

    colonnesPossibles[coupsFinal] = 0
    if poidsMaxi == 0:
        return placerPionAleatoire(joueur)
    return coupsFinal
