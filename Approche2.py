import random
import numpy as np
from enum import Enum

# Type des cases du plateau
class TypeCase(Enum):
    VIDE = 0
    CROIX = 1
    CARRE = 2

# Un plateau
class Plateau:
    def __init__(this):
        """_Constructeur_\n
        Initialise le plateau avec un tableau numpy.array
        """
        this.taille = (10, 10)
        this.plateau = np.zeros(this.taille, dtype=int)

    def setCase(this, x, y, type):
        """_Modifie une case_
        Args:
            x (_int_): _coordonnée en x_
            y (_int_): _coordonnée en y_
            type (_TypeCase_): _type de la nouvelle case_
        """       
        this.plateau[x, y] = type.value

    def getCase(this, x, y):
        """_Renvoie une case_
        Et redimensionne la case si le plateau est trop petit
        Args:
            x (_int_): _coordonnée en x_
            y (_int_): _coordonnée en y_

        Returns:
            _int_: _valeur du type de la case_
        """
        if (x > this.taille[0] - 1):
            this.setTaille(x + 1, this.taille[1])
        if (y > this.taille[1] - 1):
            this.setTaille(this.taille[0], y + 1)

        return this.plateau[x, y]
        
    def setTaille(this, tailleX, tailleY):
        """_Redimensionne le plateay_
        Args:
            tailleX (_int_): _nouvelle taille du plateau en X_
            tailleY (_int_): _nouvelle taille du plateau en Y_
        """
        # nouvelle plateau de 0
        nvlPlateau = np.zeros((tailleX, tailleY), dtype=int)
        # on colle l'ancienne plateau dans la nouvelle plus grande
        nvlPlateau[:this.taille[0], :this.taille[1]] = this.plateau
        # on assigne la plateau actuelle à la nouvelle
        this.plateau = nvlPlateau  
        # on assigne la taille à la nouvelle taille
        this.taille = (tailleX, tailleY)

class Jeu:
    def __init__(this):
        """_Constructeur_\n
        Initialise le plateau et les 2 joueurs
        """
        this.plateau = Plateau()
        this.joueur1 = TypeCase.CARRE if int(input("Croix = 1 ou Carre = 2 : ")) == 2 else TypeCase.CROIX
        this.joueur2 = TypeCase.CARRE if this.joueur1 == TypeCase.CROIX else TypeCase.CROIX

    def afficher(this):
        """_Affiche dans la console le morpion_
        """
        for j in range(this.plateau.taille[1]):
            for i in range(this.plateau.taille[0]):
                print(this.plateau.getCase(i, j), end=" , ")
            print("\n")

    def run(this):
        """_Boucle de jeu_
        """
        while True:           

            # JOUEUR 1
            x1, y1 = map(int, input("J1 : pos (x y) : ").split())
            while this.plateau.getCase(x1, y1) != TypeCase.VIDE.value:
                print("J1 : case pleine rejouer")
                x1, y1 = map(int, input("J1 : pos (x y) : ").split())
            this.plateau.setCase(x1, y1, this.joueur1)

            # JOUEUR 2
            x2, y2 = map(int, input("J2 : pos (x y) : ").split())
            while this.plateau.getCase(x2, y2) != TypeCase.VIDE.value:
                print("J2 : case pleine rejouer")
                x2, y2 = map(int, input("J2 : pos (x y) : ").split())
            this.plateau.setCase(x2, y2, this.joueur2)

            this.afficher()

if __name__ == "__main__":
    jeu = Jeu()
    jeu.run()