import random
import numpy as np
import time
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
from enum import Enum

# Approche 2
# Fait par gaël

# Type des cases du plateau
class TypeCase(Enum):
    VIDE = 0
    CROIX = 1
    ROND = 2

# Un plateau
class Plateau:
    def __init__(this):
        """<b>Constructeur</b>\n
        Initialise le plateau avec un numpy.array
        """
        this.taille = (9, 9) 
        this.plateau = np.zeros(this.taille, dtype=int)

        # les 2 variables vont accumuler tous les décalages du plateau
        this.décalageX = 0
        this.décalageY = 0

        # couleur pour l'affichage matplot (blanc = vide, bleu/rouge = pions)
        this.couleur = mcolors.ListedColormap(['white', 'blue', 'red'])

    def setCase(this, x : int, y : int, type : int):
        """<b>Modifie une case</b>\n
        Et agrandit le plateau si la case est en dehors
        Args:
            x (int): coordonnée en x
            y (int): coordonnée en y
            type (int): type de la nouvelle case
        """       
        # si coordonnées supérieures à la taille du plateau
        if (x > this.taille[0] - 1):
            this.setTaille(x + 1, this.taille[1], False)
        if (y > this.taille[1] - 1):
            this.setTaille(this.taille[0], y + 1, False)

        # si inférieures alors on doit agrandir et décaller tout le jeu puis mettre le pion qui était en négatif en 0
        if (x < 0):
            # on affecte le décalage
            this.décalageX += abs(x)
            this.setTaille(this.taille[0] + abs(x), this.taille[1], True)
            x = 0
        if (y < 0):
            this.décalageY += abs(y)
            this.setTaille(this.taille[0], this.taille[1] + abs(y), True)
            y = 0

        this.plateau[x, y] = type

    def getCase(this, x : int, y : int) -> int:
        """<b>Renvoie une case</b>
        Args:
            x (int): coordonnée en x
            y (int): coordonnée en y

        Returns:
            int: valeur du type de la case
        """
        # si case en dehors du plateau alors la case est vide
        if x < 0 or y < 0 or x >= this.taille[0] or y >= this.taille[1]:
            return TypeCase.VIDE.value
        
        return this.plateau[x, y]
        
    def setTaille(this, tailleX : int, tailleY : int, faireDécallage : bool):
        """<b>Redimensionne le plateau</b>
        Args:
            tailleX (int): nouvelle taille du plateau en X
            tailleY (int): nouvelle taille du plateau en Y
            faireDécallage (bool): Les valeurs doivent elles être décalées
        """
        # nouveau plateau remplit 0
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

    def décalerPlateau(this, stepX : int, stepY : int):
        """<b>décale les valeurs du plateau grâce à un pas<b>
        Args:
            stepX (int): taille du pas en X
            stepY (int): taille du pas en Y
        """
        # on commence à la fin du plateau vu que l'on doit décaler chaque pion de gauche vers droite / haut vers bas 
        for y in range(this.taille[1] - stepY - 1, -1, -1):
            for x in range(this.taille[0] - stepX - 1, -1, -1):
                # pas de get ou set pour éviter les appels récursifs
                case = this.plateau[x, y]
                this.plateau[x + stepX , y + stepY] = case
                this.plateau[x, y] = TypeCase.VIDE.value

class Jeu:
    def __init__(this, n : int):
        """<b>Constructeur<b>\n
        Initialise le plateau et les 2 joueurs

        Args:
            n (int): n symboles à aligné pour gagner
        """
        this.plateau = Plateau()

        this.joueur1 = TypeCase.ROND
        this.joueur2 = TypeCase.CROIX

        this.xmin = 0
        this.xmax = 0 
        this.ymin = 0
        this.ymax = 0    

        # le premier pion est en 0, 0
        this.plateau.setCase(int(this.plateau.taille[0] / 2), int(this.plateau.taille[1] / 2), this.joueur1.value)

        # distance maximale auquel le joueur peut jouer autour de chaque pion
        this.maxStep = 0

        this.gomoku = n

    def afficherMatPlot(this):
        """<b>Affiche dans avec matplotlib le morpion</b>
        """
        plt.imshow(this.plateau.plateau, cmap=this.plateau.couleur)
        plt.pause(0.01)
        plt.clf()

    def run(this):
        """<b>Boucle de jeu</b>
        Utiliser pour tester le code visuellement sans limite de coup (debug)
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

    def victoire(this) -> bool:
        """Détermine si un joueur a gagné

        Returns:
            bool: renvoie vrai si un joueur a gagné
        """
        for y in range(this.plateau.taille[1]):
            for x in range(this.plateau.taille[0]):
                # récupère le type de la case en x, y
                typeCase = this.plateau.getCase(x, y)

                # si la case ne contient pas de joueur alors on coupe la boucle pour faire le tour suivant
                if typeCase == TypeCase.VIDE.value:
                    continue

                # horizontale
                cpt = 0
                # temps que la case suivante est la même que la précédente on augmente le compteur
                while typeCase == this.plateau.getCase(cpt + x, y):
                    cpt += 1
                    if cpt == this.gomoku:                        
                        #print(f"{joueur.name}({joueur.value}) a gagné")
                        return True

                # verticale
                cpt = 1
                while typeCase == this.plateau.getCase(x, cpt + y):
                    cpt += 1      
                    if cpt == this.gomoku:
                        #print(f"{joueur.name}({joueur.value}) a gagné")
                        return True
                    
                # diagonale bas droite
                cpt = 1
                while typeCase == this.plateau.getCase(cpt + x, cpt + y):
                    cpt += 1      
                    if cpt == this.gomoku:
                        #print(f"{joueur.name}({joueur.value}) a gagné")
                        return True
                    
                # diagonale haut droite
                cpt = 1
                while typeCase == this.plateau.getCase(cpt + x, y - cpt):
                    cpt += 1      
                    if cpt == this.gomoku:
                        #print(f"{joueur.name}({joueur.value}) a gagné")
                        return True
                    
        return False

    def zoneJouable(this) -> tuple:
        """<b>Calcule la nouvelle position jouable pour un pion</b> \n
        Le but est de prendre le pion en x,y le plus éloigné en négatif et le pions en x,y le plus éloigné en positif \n
        Pour après appliquer le pas autour de cette zone de jeu (carré formé pas les 2 pions les plus éloignés)

        Returns:
            tuple: retourne les coordonnées x et y de la position à jouer
        """
        xmin = this.xmin - this.maxStep 
        xmax = this.xmax + this.maxStep
        ymin = this.ymin - this.maxStep
        ymax = this.ymax + this.maxStep

        while True:
            # position aléatoire dans la zone de jeu
            x = random.randint(xmin, xmax)
            y = random.randint(ymin, ymax)

            # x/y peuvent être négatives donc on applique le décallage du tableau 
            # par exemple un pion est joué en -3, il y a donc 3 en décallage de tableau et le pion est placé en 0 pour numpy (mais la position réelle est -3)
            nx = x + this.plateau.décalageX
            ny = y + this.plateau.décalageY
            if this.plateau.getCase(nx, ny) == TypeCase.VIDE.value:
                return (x, y)

    def jouerCoup(this, joueur : TypeCase, afficher : bool, p : int = 1) -> float:
        """<b>Joue un coup</b>
        Args:
            joueur (TypeCase): le joueur qui effectue le coup
            afficher (bool): s'il y a un affichage ou non
            p (int): paramètre de dispersion
        
        Returns:
            float: Temps d'exécution pour jouer un coup, ou -1 si le joueur a gagné
        """
        startTime = time.time()  

        this.maxStep = p

        # la vérification de la case n'est pas vide est faite dans la méthode zoneJouable
        x, y = this.zoneJouable()
        this.plateau.setCase(x + this.plateau.décalageX, y + this.plateau.décalageY, joueur.value)

        # on récupère les positions les plus éloignés si il y en a une nouvelle
        this.xmin = min(this.xmin, x)
        this.xmax = max(this.xmax, x)
        this.ymin = min(this.ymin, y)
        this.ymax = max(this.ymax, y)

        # affiche le jeu
        if (afficher):
            this.afficherMatPlot()

        # vérifie la victoire
        if (this.victoire()):
            return -1
        
        return (time.time() - startTime) * 1000
        
    
if __name__ == "__main__":
    jeu = Jeu(5)
    jeu.run()