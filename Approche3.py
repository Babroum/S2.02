import numpy as np
import random
from enum import Enum

class TypeCase(Enum):
    VIDE = 0    # Case pas joué
    CROIX = 1   # Case joué par joueur1
    ROND = 2    # Case joué par joueur2

class Plateau:
    # Constructeur de Plateau
    def __init__(self):
        self.morpions = {} # Dictionnaire vide (va contenir les morpions utilisés pour jouer)

    # Méthodes de Plateau
    def coordsMorpion(self, x, y):
        # Calcul des coords du morpion
        mx = x // 3 # Position x du morpion
        my = y // 3 # Position y du morpion

        # Calcul des coords du contenu (Contiendra TypeCase)
        px = x % 3 # Position x dans le morpion
        py = y % 3 # Position y dans le morpion

        # Retourne tuple (clé dictionnaire) et les positions du contenu
        return (mx, my), px, py
    
    def setCase(self, x, y, type):
        # Assignation des variables (dans l'ordre du return)
        cle, px, py = self.coordsMorpion(x, y)

        # Création morpion si non existant
        if cle not in self.morpions:
            self.morpions[cle] = np.zeros((3, 3), dtype=int) # Tableau numpy rempli de 0 # On spécifie le type int (Défaut = float)

        # Rempli la case visée
        self.morpions[cle][py][px] = type.value # Sur numpy c'est posY puis posX
            
    def getCase(self, x, y):
        # Assignation des variables
        cle, px, py = self.coordsMorpion(x, y)

        # Retourne valeur vide si non existant
        if cle not in self.morpions:
            return TypeCase.VIDE.value
        
        # Retourne valeur de la case visée
        return self.morpions[cle][py][px]
    
    # Retourne vrai si valeur case 0 sinon faux
    def estVide(self, x, y):
        return self.getCase(x, y) == TypeCase.VIDE.value
    
class Jeu:
    # Constructeur de Jeu
    def __init__(self, n=5): # On met par défaut n=5 (alignement pour gagner)
        # Création du plateau
        self.plateau = Plateau()

        # Assignation typeCase pour chaque joueur
        self.joueur1 = TypeCase.CROIX
        self.joueur2 = TypeCase.ROND

        # Nb alignement pour gagner 
        self.n = n

        # Premier coup en (0,0)
        self.plateau.setCase(0, 0, self.joueur1)

        # Valeur par défaut dispersion
        self.dispersion = 1

    def afficher(self):
        # Boucle pour parcourir le dictionnaire morpions
        for cle in self.plateau.morpions:
            morpion = self.plateau.morpions[cle]
            print(f"Morpion {cle} :\n{morpion}") # Afficher le morpion

    def run(self):
        # méthode pour débug pas utilisé dans la version final
        limite = 1000 # Nb max de coups
        coups = 0 # Nb coups 

        while coups < limite:
            # Récupère le résultat du coup
            resultat = self.jouerCoup(self.joueur1)
            # Si joueur1 gagné
            if resultat:
                print("Le joueur1 (CROIX) a gagné !")
                return
            coups += 1

            # Récupère le résultat du coup
            resultat = self.jouerCoup(self.joueur2)
            # Si impossible de jouer
            # Si joueur2 gagné
            if resultat:
                print("Le joueur2 (ROND) a gagné !")
                return
            coups += 1
        
        print(f"Pas de gagnant après {coups} coups")

    def jouerCoup(self, joueur, p):
        # Assignation d'une dispersion pour le coup du joueur
        self.dispersion = p
        
        # Assignations des valeurs retournées par zoneJouable
        x, y = self.zoneJouable(joueur) 

        # Joueur joue
        self.plateau.setCase(x, y, joueur)

        # Vérificaton de la victoire après coup
        if self.victoire(x, y, joueur):
            return joueur # Retourne gagnant
        
        return False # Pas de gagnant

    def victoire(self, x, y, joueur):
        
        directions = [
            (1, 0), # Horizontale
            (0, 1), # Verticale
            (1, 1), # Diagonale descendante (\)
            (1, -1), # Diagonale montante (/)
            # Que 4 directions puisqu'on fera le sens opposé pour avoir les 8
        ]

        # Pour chaque direction
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
            
            # Gagné
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
        cx = [] # Liste des coords x de chaque coup joué
        cy = [] # Liste des coords y de chaque coup joué

        # Pour chaque morpion
        for cle in self.plateau.morpions:
            # On stocke le morpion
            morpion = self.plateau.morpions[cle]

            # On récupère les coordonnées
            mx = cle[0]
            my = cle[1]

            # Pour chaque position dans le morpion
            for py in range(3):
                for px in range(3):
                    
                    # Check si case utilisée
                    if morpion[py][px] != TypeCase.VIDE.value:
                        # Inverse de coordsMorpion
                        cx.append(mx * 3 + px)
                        cy.append(my * 3 + py)

        xmin = min(cx) - self.dispersion # Coup le plus à gauche
        xmax = max(cx) + self.dispersion # Coup le plus à droite
        ymin = min(cy) - self.dispersion # Coup le plus haut
        ymax = max(cy) + self.dispersion # Coup le plus bas
        # Étendu par dispersion pour jouer autour du coup

        # On teste 10067 fois
        for _ in range(10067):
            x = random.randint(xmin, xmax) # Valeur aléatoire dans la zone xmin xmax
            y = random.randint(ymin, ymax) # Valeur aléatoire dans la zone ymin ymax
            # Si case vide renvoie
            if self.plateau.estVide(x, y):
                return (x, y)

# Point d'entrée
if __name__ == "__main__":
    # Crée une partie avec N=5 (Gomoku)
    jeu = Jeu(n=5)

    # Assignation valeur p (dispersion)
    jeu.valeurDispersion(1)

    # Lance la boucle de jeu
    jeu.run()

    # Affichage final
    # jeu.afficher()
