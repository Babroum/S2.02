import random
import numpy as np
import time
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
from enum import Enum

# Approche 2
# Fait par gaêl

# Type des cases du plateau
class TypeCase(Enum):
    VIDE = 0
    CROIX = 1
    ROND = 2
    TEST = 3

# Un plateau
class Plateau:
    def __init__(this):
        """<b>Constructeur</b>\n
        Initialise le plateau avec un tableau numpy.array
        """
        this.taille = (9, 9)
        this.plateau = np.zeros(this.taille, dtype=int)
        this.couleur = mcolors.ListedColormap(['white', 'blue', 'red'])

    def setCase(this, x, y, type):
        """<b>Modifie une case</b>\n
        Et aggrandit le plateau si la case est endehors
        Args:
            x (_int_): coordonnée en x
            y (_int_): coordonnée en y
            type (_int_): type de la nouvelle case
        """       
        # si coordonnées supérieur à la taille de grille
        if (x > this.taille[0] - 1):
            this.setTaille(x + 1, this.taille[1], False)
        if (y > this.taille[1] - 1):
            this.setTaille(this.taille[0], y + 1, False)

        # si inférieur alors on doit aggrandir et décallé tout le jeu puis mettre le pion qui était en négatif en 0
        if (x < 0):
            this.setTaille(this.taille[0] + abs(x), this.taille[1], True)
            x = 0
        if (y < 0):
            this.setTaille(this.taille[0], this.taille[1] + abs(y), True)
            y = 0

        this.plateau[x, y] = type

    def getCase(this, x, y):
        """<b>Renvoie une case</b>
        Args:
            x (_int_): coordonnée en x
            y (_int_): coordonnée en y

        Returns:
            _int_: valeur du type de la case
        """
        # si case en dehors du plateau alors la case est vide
        if x < 0 or y < 0 or x >= this.taille[0] or y >= this.taille[1]:
            return TypeCase.VIDE.value
        
        return this.plateau[x, y]
        
    def setTaille(this, tailleX, tailleY, faireDécallage):
        """<b>Redimensionne le plateau</b>
        Args:
            tailleX (_int_): nouvelle taille du plateau en X
            tailleY (_int_): nouvelle taille du plateau en Y
            faireDécallage (_bool_): Les valeurs doivent elles être décallé
        """
        # nouveau plateau de 0
        nvlPlateau = np.zeros((tailleX, tailleY), dtype=int)
        # on colle l'ancien plateau dans le nouveau plus grand
        nvlPlateau[:this.taille[0], :this.taille[1]] = this.plateau
        # on assigne le plateau actuel au nouveau
        this.plateau = nvlPlateau
        # récupère la taille avant de modifier 
        oldTaille = (this.taille[0], this.taille[1])
        # on assigne la taille à la nouvelle taille
        this.taille = (tailleX, tailleY)
        
        # si pas de décallage a faire on en fait pas
        if not faireDécallage: return

        # décale toutes les cases
        this.décalerPlateau(tailleX - oldTaille[0], tailleY - oldTaille[1])

    def décalerPlateau(this, stepX, stepY):
        """<b>décale les valeurs du tableau grâce à un pas<b>
        Args:
            stepX (_int_): taille du pas en X
            stepY (_int_): taille du pas en Y
        """
        # on commence à la fin du tableau vu que l'on doit décallé chaque pion de gauche à droite / haut à bas 
        for y in range(this.taille[1] - stepY - 1, -1, -1):
            for x in range(this.taille[0] - stepX - 1, -1, -1):
                # pas de get ou set pour évité les appels récursifs
                case = this.plateau[x, y]
                this.plateau[x + stepX , y + stepY] = case
                this.plateau[x, y] = TypeCase.VIDE.value

class Jeu:
    def __init__(this):
        """<b>Constructeur<b>\n
        Initialise le plateau et les 2 joueurs
        """
        this.plateau = Plateau()

        this.joueur1 = TypeCase.ROND
        this.joueur2 = TypeCase.CROIX

        #le premier pion est en 0, 0
        this.plateau.setCase(int(this.plateau.taille[0] / 2), int(this.plateau.taille[1] / 2), this.joueur1.value)

        # distance maximal auquel le joueur peux jouer
        this.maxStep = 0

        # minimum de 2 pour évité de gagné avec juste une case
        this.gomoku = random.randint(2, 10);
        print(f"Gomoku : {this.gomoku}")

    def afficherMatPlot(this):
        """<b>Affiche dans avec matplotlib le morpion</b>
        """
        plt.imshow(this.plateau.plateau, cmap=this.plateau.couleur)
        plt.pause(0.01)
        plt.clf()

    def run(this):
        """<b>Boucle de jeu</b>
        Utiliser pour tester le code visuellement sans limite de coup
        """
        while True:                    
            t1 = this.jouerCoup(this.joueur1, True)
            if t1 == -1:
                break
            t2 = this.jouerCoup(this.joueur2, True)
            if t2 == -1:
                break

        plt.imshow(this.plateau.plateau, cmap=this.plateau.couleur)
        plt.show()

    def victoire(this):
        """_Determine si un joueur à gagné_

        Returns:
            _bool_: renvoie vrai si un joueur à gagné
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
                    if cpt == this.gomoku:                        
                        print(f"{joueur.name}({joueur.value}) à gagné")
                        return True

                # verticale
                cpt = 0
                while typeCase == this.plateau.getCase(x, cpt + y):
                    cpt += 1      
                    if cpt == this.gomoku:
                        print(f"{joueur.name}({joueur.value}) à gagné")
                        return True
                    
                # diagonale bas droite
                cpt = 0
                while typeCase == this.plateau.getCase(cpt + x, cpt + y):
                    cpt += 1      
                    if cpt == this.gomoku:
                        print(f"{joueur.name}({joueur.value}) à gagné")
                        return True
                    
                # diagonale haut droite
                cpt = 0
                while typeCase == this.plateau.getCase(cpt + x, y - cpt):
                    cpt += 1      
                    if cpt == this.gomoku:
                        print(f"{joueur.name}({joueur.value}) à gagné")
                        return True
                    
        return False
        
    def dispersion(this):
        """<b>Calcule la dispersion</b>
        """
        # random.random est compris entre 0(inclus) et 1(exclus) donc uniform permet d'avoir le 1 inclus
        p = random.uniform(0,1)
        if p == 0:
            this.maxStep = 1
        elif p == 1:
            this.maxStep = 1000
        else:
            this.maxStep = min(int(1 / (1 - p)), 1000)

    def zoneJouable(this):
        """<b>Calcule la nouvelle position jouable pour un pion</b> \n
        La méthode récupère une position (x, y) autour de chaque pion sur le plateau\n
        Et l'ajoute dans une liste, et sélectionne après parmit cette liste une position\n
        que le prochain pion va recevoir

        Returns:
            _tuple_: retourne les coordonnées x et y de la position à joué
        """
        positionJouable = []
        # parcours le plateau 
        for y in range(this.plateau.taille[1]):
            for x in range(this.plateau.taille[0]):
                # si il y a une case qui comporte un pion
                if this.plateau.getCase(x, y) in (TypeCase.CROIX.value, TypeCase.ROND.value):
                    # on selection aléatoirement une case jouable autour du pion 
                    # par exemple pour 10 pions sur le plateau il y aura 10 positions jouables pour le prochain pion
                    casesLibres = []
                   
                    # pour chaque case jouable autour de la case x, y
                    for ty in range(y - this.maxStep, y + this.maxStep + 1):
                        for tx in range(x - this.maxStep, x + this.maxStep + 1):
                            # getcase va récupéré la case et si elle n'existe pas alors il va aggrandir le tableau en conséquence
                            if this.plateau.getCase(tx, ty) == TypeCase.VIDE.value:                                
                                casesLibres.append((tx, ty))
                    
                    # cet valeur est stocké dans la list e de positionJouable
                    if len(casesLibres) > 0:
                        positionJouable.append(random.choice(casesLibres))
        
        
        # retourne une position jouable pour le prochain pion depuis la liste de positions jouables
        return (random.choice(positionJouable))

    def jouerCoup(this, joueur, afficher):
        """<b>Joue un coup</b>
        Args:
            joueur (_TypeCase_): le joueur qui effectue le coup
            afficher (_bool_): si il y a un affichage ou non
        
        Returns:
            _float_: Temps d'exécution pour jouer un coup, ou -1 si le joueur a gagné
        """
        startTime = time.time()  
        this.dispersion()
        # la vérification de la case n'est pas vide est faite dans la méthode zoneJouable
        x, y = this.zoneJouable()
        this.plateau.setCase(x, y,joueur.value)

        # affiche le jeu
        if (afficher):
            this.afficherMatPlot()

        # vérifie la victoire
        if (this.victoire()):
            return -1
        
        return (time.time() - startTime) *1000
        
    
if __name__ == "__main__":
    jeu = Jeu()
    jeu.run()