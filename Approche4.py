import time
import random
import networkx as nx
import matplotlib . pyplot as plt
from enum import Enum

# Approche 2
# Fait par gaël

class Type(Enum):
    CROIX = 0
    ROND = 1

class Noeud:    

    def __init__(this, x : int , y : int, type : Type):
        """<b>Constructeur</b>
        Initialise le noeud de type Type en position x, y

        Args:
            x (int): coordonnées en X
            y (int): coordonnées en Y
            type (Type): type de noeud (pour différencier les 2 joueurs)
        """
        # Les 8 directions voisines au noeud
        Noeud.DIRECTIONS = [(x-1, y-1), (x, y-1), (x+1, y-1),
                            (x-1, y  ),           (x+1, y  ),
                            (x-1, y+1), (x, y+1), (x+1, y+1)]

        this.pos = (x, y)
        this.type = type

    # pour networkx, il va appelé str quand il va lire la liste d'adjacence qui contient des types Noeud
    def __str__(this):
        return f"({this.type.value})"
    
class GestionNoeud:
    positions = {} # on fait une copie du dictionnaire qui contient les Noeud pour évité de devoir boucle sur tout le dict quand on doit getNoeud

    def ajouterNoeud(noeuds : dict, noeud : Noeud):
        """<b>Ajoute un noeud à la liste d'adjacence</b>

        Args:
            noeuds (dict): liste d'adjacence
            noeud (Noeud): noeud
        """
        # ajoute le noeud sans arrêtes
        noeuds[noeud] = []
        GestionNoeud.positions[noeud.pos] = noeud
        for n in noeuds.keys():
            # si le noeud n'est pas déjà présent, même si cela n'est pas censé arrivé
            if n.pos[0] != noeud.pos[0] and n.pos[1] != noeud.pos[1]:
                # cherche tous les voisins du noeud et ajoute au noeud si il y en a
                GestionNoeud.ajouterArrete(noeuds, noeud)                
    
    def ajouterArrete(noeuds : dict, noeud : Noeud):
        """<b>Cherche les voisins autour du noeud</b> 
        Si il y a un voisin à une distance de 1, alors on créer l'arrête

        Args:
            noeuds (dict): liste d'adjacence
        """
        voisins = []
        # pour toutes les directions, donc tous les voisins adjacents
        for dir in noeud.DIRECTIONS:
            voisin = GestionNoeud.getNoeud(GestionNoeud.positions, dir)
            # si le voisin existe on l'ajoute en arrête
            if voisin != None:
                voisins.append(GestionNoeud.getNoeud(GestionNoeud.positions, dir))

        # puis ajoute le noeud en clé et ses voisins en valeur dans la liste d'adjacence
        noeuds[noeud] = voisins
    
    def getNoeud(positions : dict, pos : tuple) -> Noeud:
        """Retourne le noeud à la position (x, y) donné

        Args:
            positions (dict): liste d'ajacence mais avec des tuples et non pas des Noeud
            pos (tuple): position (x, y)

        Returns:
            Noeud: noeud à la position (x, y), sinon None si le noeud n'existe pas
        """
        # le fait de ne plus faire de for on passe de O(n) à O(1) donc pour les get dans victoire, ... on passe de O(n²) à O(n)
        # le get retourne la valeur de la clé fourni en premier paramètre sinon None
        # le get hash la clé en O(1) et donc le hash donne directement l'emplacement mémoire de la valeur sans parcourir le dictionnaire
        return positions.get(pos, None)

class Jeu:

    def __init__(this, n : int, afficher : bool = False):
        """<b>Constructeur</b>
        Initialise le plateau et les 2 joueurs

        Args:
            n (int): n symboles à aligné pour gagner
            afficher (bool): si le jeu doit être afficher
        """
        # liste d'adjacence des noeuds
        # les clés sont de type Noeud
        # les valeurs sont des listes de Noeud
        this.noeuds = {}
        GestionNoeud.positions = {}

        this.joueur1 = Type.ROND
        this.joueur2 = Type.CROIX

        # le premier pion est en (0, 0)
        this.xmin = 0
        this.xmax = 0  
        this.ymin = 0
        this.ymax = 0

        # le dictionnaire sera modifié car c'est une référence qui est passée en paramètre 
        # donc les modifications sont visible sans besoin de return le dictionnaire modifié
        GestionNoeud.ajouterNoeud(this.noeuds, Noeud(0, 0, this.joueur1)) # le premier pion est en 0, 0

        this.maxStep = 0

        this.gomoku = n 

        this.afficher = afficher

        if this.afficher:
            # pour l'affichage
            this.fig = plt.figure(figsize=(10, 10))

    def afficherNetWorkX(this):
        G = nx.Graph(this.noeuds)
        plt.figure(this.fig.number)                
        # créer un dictionnaire mais avec les coordonnées x et y de chaque noeud pour que networkx positionne avec les bonnes coordonnées
        pos = {noeud: (noeud.pos[0], noeud.pos[1]) for noeud in this.noeuds}
        nx.draw(G,pos=pos, with_labels=True, node_size=800, font_weight='bold', edge_color='gray')
        plt.title("Approche 4")
        plt.pause(0.3)
        plt.clf()

    def zoneJouable(this) -> tuple:
        """<b>Calcule la nouvelle position jouable pour un pion</b> \n
        Le but est de prendre le pion en x,y le plus éloigné en négatif et le pions en x,y le plus éloigné en positif \n
        Pour après appliquer le pas autour de cette zone de jeu (carré formé pas les 2 pions les plus éloignés)
        Returns:
            tuple: _description_
        """
        xmin = this.xmin - this.maxStep
        xmax = this.xmax + this.maxStep
        ymin = this.ymin - this.maxStep
        ymax = this.ymax + this.maxStep

        while True:
            x = random.randint(xmin, xmax)
            y = random.randint(ymin, ymax)
            if GestionNoeud.getNoeud(GestionNoeud.positions, (x, y)) == None:
                return (x, y)

    def victoire(this) -> bool:
        """Détermine si un joueur a gagné

        Returns:
            bool: renvoie vrai si un joueur a gagné
        """
        for n in this.noeuds:
            x = n.pos[0]
            y = n.pos[1]

            # pas besoin de regardr toutes les directions vu que chaque noeud va regardé
            # par exemple si on vérifie la diagonale pour le Noeud1 : x+1 et y+1
            # pas besoin de vérifié pour le Noeud2: x-1 et y-1 car le noeud qui sera à cette (Noeud2) position lui va regarder en x+1 et y+1 (Noeud1)

            # horizontale
            cpt = 1
            # temps que le noeud suivant existe et qu'il est le même que le précédenton augmente le compteur
            while (GestionNoeud.getNoeud(GestionNoeud.positions, (x + cpt, y)) != None) and \
                  (n.type == GestionNoeud.getNoeud(GestionNoeud.positions, (x + cpt, y)).type):
                cpt += 1
                if cpt == this.gomoku:                        
                    #print(f"{n.type.name}({n.type.value}) a gagné, Horiz")
                    return True
                
            # verticale
            cpt = 1
            while (GestionNoeud.getNoeud(GestionNoeud.positions, (x, y + cpt)) != None) and \
                  (n.type == GestionNoeud.getNoeud(GestionNoeud.positions, (x, y + cpt)).type):
                cpt += 1      
                if cpt == this.gomoku:
                    #print(f"{n.type.name}({n.type.value}) a gagné, vert")
                    return True
                
            # diagonale bas droite
            cpt = 1
            while (GestionNoeud.getNoeud(GestionNoeud.positions, (x + cpt, y - cpt)) != None) and \
                  (n.type == GestionNoeud.getNoeud(GestionNoeud.positions, (x + cpt, y - cpt)).type):
                cpt += 1      
                if cpt == this.gomoku:
                    #print(f"{n.type.name}({n.type.value}) a gagné, diag bas droite")
                    return True
                
            # diagonale haut droite
            cpt = 1
            while (GestionNoeud.getNoeud(GestionNoeud.positions, (x + cpt, y + cpt)) != None) and \
                  (n.type == GestionNoeud.getNoeud(GestionNoeud.positions, (x + cpt, y + cpt)).type):
                cpt += 1      
                if cpt == this.gomoku:
                    #print(f"{n.type.name}({n.type.value}) a gagné, diag haut droite")
                    return True

            

    def jouerCoup(this, joueur : Type, p : int = 1) -> float:
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

        x, y = this.zoneJouable()
        GestionNoeud.ajouterNoeud(this.noeuds, Noeud(x, y, joueur))

        # on récupère les positions les plus éloignés si il y en a une nouvelle
        this.xmin = min(this.xmin, x)
        this.xmax = max(this.xmax, x)
        this.ymin = min(this.ymin, y)
        this.ymax = max(this.ymax, y)

        # affiche le jeu
        if (this.afficher):
            this.afficherNetWorkX()

        # vérifie la victoire
        if (this.victoire()):
            return -1

        return (time.time() - startTime) * 1000

        
if __name__ == "__main__":
    affichage = True
    jeu = Jeu(3, affichage)  
    while True:
        t1 = jeu.jouerCoup(jeu.joueur1, 4)
        if t1 == -1:
            break

        t2 = jeu.jouerCoup(jeu.joueur2, 4)
        if t2 == -1:
            break
    
    if affichage:
        G = nx.Graph()
        for noeud, voisins in jeu.noeuds.items():
            G.add_node(noeud)
            for voisin in voisins:
                G.add_edge(noeud, voisin)
        pos = {noeud: (noeud.pos[0], noeud.pos[1]) for noeud in jeu.noeuds}
        nx.draw(G, pos=pos, with_labels=True, node_size=800, font_weight='bold', edge_color='gray')
        plt.title("Approche 4")
        plt.show()