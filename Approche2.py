import random
import numpy as np
import time
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
from enum import Enum
import math

# Type des cases du plateau
class TypeCase(Enum):
    VIDE = 0
    CROIX = 1
    ROND = 2

# Un plateau
class Plateau:
    def __init__(this):
        """_Constructeur_\n
        Initialise le plateau avec un tableau numpy.array
        """
        this.taille = (10, 10)
        this.plateau = np.zeros(this.taille, dtype=int)
        this.couleur = mcolors.ListedColormap(['white', 'blue', 'red'])

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

        this.joueur1 = TypeCase.ROND
        this.joueur2 = TypeCase.CROIX

        #le premier pion est en 0, 0
        this.plateau.setCase(0, 0, this.joueur1)

        # distance maximal auquel le joueur peux jouer
        this.maxStep = 0

    def afficher(this):
        """_Affiche dans la console le morpion_
        """
        for j in range(this.plateau.taille[1]):
            for i in range(this.plateau.taille[0]):
                print(this.plateau.getCase(i, j), end=" , ")
            print("\n")
        print("==========================================")

    def afficherMatPlot(this):
        """_Affiche dans avec matplotlib le morpion_
        """
        plt.imshow(this.plateau.plateau, cmap=this.plateau.couleur)
        for j in range(this.plateau.taille[1]):
            for i in range(this.plateau.taille[0]):
                val = this.plateau.getCase(i, j)
                if val != 0:
                    plt.text(j, i, '0' if val == this.joueur1.value else 'X',
                             ha='center', va='center',
                            fontsize=12, fontweight='bold', color='white')
        plt.pause(1)
        plt.clf()

    def run(this):
        """_Boucle de jeu_
        """

        while True:             
            #====================================================         
            this.dispersion()

            # JOUEUR 1 ROND
            # la vérification de la case n'est pas vide est faite dans la méthode zoneJouable
            x, y = this.zoneJouable(this.joueur1)
            this.plateau.setCase(x, y, this.joueur1)

            # affiche le jeu
            this.afficherMatPlot()
            # vérifie la victoire
            if (this.victoire()):
                return
            
            #====================================================
            this.dispersion()

            # JOUEUR 2 CROIX
            x, y = this.zoneJouable(this.joueur2)
            this.plateau.setCase(x, y, this.joueur2)

            # affiche le jeu 
            this.afficherMatPlot()
            # vérifie la victoire
            if (this.victoire()): 
                return

            # il faut vérifié la victoire entre chaque joueur car si le joueur 1 gagne mais que le joueur 2 gagne aussi et que sont pion est plus proche du centre
            # alors la méthode va détecté que le joueur 2 à gagné en premier alors que non 
            # car la méthode this.victoire() commence en 0 0 puis augmente en x avant d'augmenter en y

    def victoire(this):
        """_Determine si un joueur à gagné_

        Returns:
            _bool_: _renvoie vrai si un joueur à gagné_
        """
        for y in range(this.plateau.taille[1]):
            for x in range(this.plateau.taille[0]):
                # récupère le type de la case en x, y
                typeCase = this.plateau.getCase(x, y)

                # si la case ne contient pas de joueur alors on coupe la boucle pour faire le tour suivant
                if typeCase == TypeCase.VIDE.value:
                    continue

                joueur = this.joueur1 if typeCase == this.joueur1.value else this.joueur2

                # horizontale
                cpt = 0
                # temps que la case suivante est la même que la précédente on augmente le compteur
                while typeCase == this.plateau.getCase(cpt + x, y):
                    cpt += 1
                    if cpt == 3:                        
                        print(f"{joueur.name}({joueur.value}) à gagné, x:{x}, y:{y}")
                        return True

                # verticale
                cpt = 0
                while typeCase == this.plateau.getCase(x, cpt + y):
                    cpt += 1      
                    if cpt == 3:
                        print(f"{joueur.name}({joueur.value}) à gagné, x:{x}, y:{y}")
                        return True
                    
                # diagonale
                cpt = 0
                while typeCase == this.plateau.getCase(cpt + x, cpt + y):
                    cpt += 1      
                    if cpt == 3:
                        print(f"{joueur.name}({joueur.value}) à gagné, x:{x}, y:{y}")
                        return True
                    
        return False
        
    def dispersion(this):
        # random.random est compris entre 0(inclus) et 1(exclus) donc uniform permet d'avoir le 1 inclus
        p = random.randrange(0, 1000, 1) / 1000
        if p == 0:
            this.maxStep = 1
        elif p == 1:
            this.maxStep = 1000
        else:
            this.maxStep = int(1 / (1 - p))

    def zoneJouable(this, j):
        """_Calcule la nouvelle position jouable pour un pion_ \n
        La méthode récupère une position (x, y) autour de chaque pion sur le plateau\n
        Et l'ajoute dans une liste, et sélectionne après parmit cette liste une position\n
        que le prochain pion va recevoir

        Returns:
            _tuple_: _retourne les coordonnées x et y de la position à joué_
        """
        positionJouable = []
        print(f"step : {this.maxStep}")
        # parcours le plateau 
        for y in range(this.plateau.taille[1]):
            for x in range(this.plateau.taille[0]):
                # si il y a une case qui comporte un pion
                if this.plateau.getCase(x, y) in (TypeCase.CROIX.value, TypeCase.ROND.value):
                    # on selection aléatoirement une case jouable autour du pion 
                    # par exemple pour 10 pions sur le plateau il y aura 10 positions jouables pour le prochain pion
                    casesLibres = []
                    for ty in range(max(0, y - this.maxStep), y + this.maxStep + 1):
                        for tx in range(max(0, x - this.maxStep), x + this.maxStep + 1):
                            if this.plateau.getCase(tx, ty) == TypeCase.VIDE.value:                                
                                casesLibres.append((tx, ty))
                    
                    # cet valeur est stocké dans la list e de positionJouable
                    if len(casesLibres) > 0:
                        positionJouable.append(random.choice(casesLibres))
        
        
        # retourne une position jouable pour le prochain pion depuis la liste de positions jouables
        return (random.choice(positionJouable))
                    

if __name__ == "__main__":
    jeu = Jeu()
    jeu.run()