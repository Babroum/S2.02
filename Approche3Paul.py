import numpy as np
import random
import enum

class TypeCase(enum):
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
        py = x % 3 # Position y dans le morpion

        # Tuple(mx, my) = clé du dictionnaire
        return (mx, my), px, py
    
    def setCase(self, x, y, type):
        # Dépaquetage de tuple / Assignation des variables dans l'ordre du return
        cle, px, py = self.coordsMorpion(x, y)

        # Création du morpion s'il n'existait pas
        if cle not in self.morpions:
            self.morpions[cle] = np.zeros((3, 3), dtype=int) # On spécifie le type int (Défaut = float)

            self.morpions[cle][py][px] = type.value # À NOTER : sur numpy c'est posY puis posX
            
    def getCase(self, x, y):
        cle, px, py = self.coordsMorpion(x, y)

        if cle not in self.morpions:
            return TypeCase.VIDE.value
        
        return int(self.morpions[cle][py][px])
