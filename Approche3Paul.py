import numpy as np
import random
from enum import Enum

class TypeCase(Enum):
    VIDE = 0    # Case pas joué
    CROIX = 1   # symbole joueur 1
    ROND = 2    # symbole joueur 2

class Plateau:
    # Constructeur
    def __init__(self):
        self.morpions = {} # Dictionnaire vide (va contenir les morpions utilisés pour jouer)

    # Méthodes
    def coordsMorpion(self, x, y):
        # Morpion
        mx = x // 3 # Position x du morpion
        my = y // 3 # Position y du morpion

        # Contenu du morpion
        px = x % 3 # Position x dans le morpion
        py = y % 3 # Position y dans le morpion

        # Tuple(mx, my) = clé du dictionnaire
        return (mx, my), px, py
    
    def setCase(self, x, y, type):
        # Assignation des variables dans l'ordre du return
        cle, px, py = self.coordsMorpion(x, y)

        # Création du morpion s'il n'existait pas
        if cle not in self.morpions:
            self.morpions[cle] = np.zeros((3, 3), dtype=int) # On spécifie le type int (Défaut = float)

        self.morpions[cle][py][px] = type.value # À NOTER : sur numpy c'est posY puis posX
            
    def getCase(self, x, y):
        cle, px, py = self.coordsMorpion(x, y)

        if cle not in self.morpions:
            return TypeCase.VIDE.value
        
        return self.morpions[cle][py][px]
    
    # Utiliser plus tard pour la liste casesLibres
    def estVide(self, x, y):
        return self.getCase(x, y) == TypeCase.VIDE.value
    
class Jeu:
    # Constructeur
    def __init__(self, n=5): # Mettre par défaut n=5 (alignement pour gagner)
        # Création du plateau
        self.plateau = Plateau()

        # Assignation des types de case pour chaque joueur
        self.joueur1 = TypeCase.CROIX
        self.joueur2 = TypeCase.ROND

        # Nb alignement pour gagner 
        self.n = n

        # Premier coup (forcemment en (0, 0))
        self.plateau.setCase(0, 0, self.joueur1)

        self.dispersion = 1

    def afficher(self):
        # Boucle pour parcourir le dictionnaire morpions
        for cle in self.plateau.morpions:
            morpion = self.plateau.morpions[cle]
            print(f"Morpion {cle} :\n{morpion}") # Afficher le morpion

    def run(self):
        limite = 9999 # nb max de coups
        coups = 0 # nb coups (à 1 car le premier coup est en (0,0) par le joueur1)

        while coups < limite:
            # Vérification position jouable            
            pos = self.zoneJouable(self.joueur2)

            if pos is None:
                print("Aucune case jouable pour le joueur 1.")
                break

            x, y = pos 

            # Commence avec le joueur2 puisque le premier coup a été fait par le joueur1 en (0, 0)
            self.plateau.setCase(x, y, self.joueur2)

            # Vérificaton de la victoire après coup
            if self.victoire(x, y, self.joueur2):
                print(f"Joueur2 (ROND) a gagné en ({x}, {y}) !")
                return # fin
            
            coups += 1
            
            # Même chose avec le joueur1
            pos = self.zoneJouable(self.joueur1)

            if pos is None:
                print("Aucune case jouable pour le joueur 1.")
                break

            x, y = pos 

            self.plateau.setCase(x, y, self.joueur1)

            if self.victoire(x, y, self.joueur1):
                print(f"Joueur1 (CROIX) a gagné en ({x}, {y}) !")
                return
            
            coups += 1

        print(f"Pas de gagnant après {coups} coups.")

    def victoire(self, x, y, joueur):
        
        directions = [
            (1, 0), # Horizontale
            (0, 1), # Verticale
            (1, 1), # Diagonale descendante (\)
            (1, -1), # Diagonale montante (/)
            # Que 4 directions puisqu'on fera le sens opposé pour avoir les 8
        ]

        # Dépaqutage du tuple dans directions 
        for dx, dy in directions:
            # 1 celui sur lequel on est positionné compte
            compte = 1

            # Avance en positif
            for cpt in range(1, self.n):
                if self.plateau.getCase(x + cpt*dx, y + cpt*dy) == joueur.value:
                    compte += 1
                else :
                    break

            # Avance en négatif 
            for cpt in range(1, self.n):
                if self.plateau.getCase(x - cpt*dx, y - cpt*dy) == joueur.value:
                    compte += 1
                else :
                    break

            if compte >= self.n:
                return True
            
        return False
    
    def valeurDispersion(self, p):
        if p == 0 :
            self.dispersion = 1
        elif p >= 1:
            self.dispersion = 1000
        else:
            self.dispersion = int(1/(1-p))

    def zoneJouable(self, joueur):
    
        sx = []
        sy = []

        # On Parcourt tous les morpions 
        for cle in self.plateau.morpions:
            # On stocke le morpion
            morpion = self.plateau.morpions[cle]
            # On récupère les coordonnées
            mx = cle[0]
            my = cle[1]

            # On parcourt le morpion
            for py in range(3):
                for px in range(3):
                    
                    # On check si la case est utilisée
                    if morpion[py][px] != TypeCase.VIDE.value:
                        # Inverse de coordsMorpion
                        sx.append(mx * 3 + px)
                        sy.append(my * 3 + py)

        xmin = min(sx) - self.dispersion
        xmax = max(sx) + self.dispersion
        ymin = min(sy) - self.dispersion
        ymax = max(sy) + self.dispersion

        for _ in range(10000):
            x = random.randint(xmin, xmax)
            y = random.randint(ymin, ymax)
            if self.plateau.estVide(x, y):
                return (x, y)

# Point d'entrée
if __name__ == "__main__":
    # Crée une partie avec N=5 (Gomoku)
    jeu = Jeu(n=5)

    jeu.valeurDispersion(1)

    # Lance la boucle de jeu
    jeu.run()

    # Affichage final
    # jeu.afficher()