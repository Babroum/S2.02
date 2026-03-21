import random
import time
import matplotlib.pyplot as plt

# Approche 1
# Fait par amadeus
DIRECTIONS = [(1, 0), (0, 1), (1, 1), (1, -1)]  # H, B, ↗, ↘

class App1_def :

    def __init__ (self, n):
        self.board = []   # liste de [(x, y, joueur...)]
        self.current_player = 1
        self.n = n # n symboles à aligné pour gagner

    def vide (self, x , y):
        """vérification de si les coordonnés sont prise ou non
        """
        for mx, my, _ in self.board :
            if mx == x and my == y :
                return False
        return True
    
    def placer (self, x, y):
        """placer le pion du joueur
        """
        if not self.vide(x,y) : #condition de placement (si c'est deja plein, on prend pas)
            return False
        self.board.append((x, y, self.current_player)) #on place dans la liste la position et le type du joueur (rond ou croix)
        win = self.verif_win(x, y) 
        if self.current_player == 1 :  #on effectue le changement de joueur a la fin d'un tour
            self.current_player = 2 
        else :
            self.current_player = 1
        
        return win #on renvoie la fonction de victoire

    def Addition_pion (self, x, y, dx, dy, pos_joueur):
        """
        compte le nombre de pion du joueur consécutif pour voir si il y a une victoire.
        on parcourt la liste et on regarde s'il y a un 4 fois le meme symbole dans la meme direction 

        """
        count = 0 
        cx = x + dx
        cy = y + dy
        while (cx, cy) in pos_joueur :
            count += 1
            cx += dx
            cy += dy
        return count

    def verif_win (self, x, y):
        """
        vérifie si le joueur gagne
        On fait l'ensemble des positions des joueurs depuis la liste
        """
        player = self.board[-1][2]
        pos_joueur = set() #set permet de ne pas pacourir toute la liste et donc d'aller plus vite dans la recherche, il va directement a la bonne case mémoireqqssssssssssssssssssssssssss ze<<<<<>>>>>>>>ZDQSDfd
        for mx, my, p in self.board:
            if p == player:
                pos_joueur.add((mx, my))
        for dx, dy in DIRECTIONS: #parcourt les 4 directions horizontales et les 2 diag repésenté par un veteur
            #combien de pions conséc du joueur sur trouve dans la direction lu
            total = (1 + self.Addition_pion(x, y, dx, dy, pos_joueur) #sens normal (le 1 pour le pions qui vient d'etre poser en (x,y))
                       + self.Addition_pion(x, y, -dx, -dy, pos_joueur)) #sens opposé    
            if total >= self.n:
                return True
        return False

    def recup_positions (self) : 
        """renvoie toute les positions des joueurs
        """
        return [(mx, my) for mx, my, _ in self.board]


    def reset (self):
        self.board = []
        self.current_player = 1
#=====BOT=====
def bot_mv(game, radius):
    """
    Choisit un coup aléatoire selon le paramètre de dispersion p.
    """
    # Récupère les cases déjà jouées (des deux joueurs)
    positions = game.recup_positions()
 
    # Premier coup
    if not positions:
        return 0, 0
 
    # Calcule les bornes actuelles du plateau (case la plus à gauche, droite, haut, bas)
    xs = [pos[0] for pos in positions]
    ys = [pos[1] for pos in positions]
    xmin, xmax = min(xs), max(xs)
    ymin, ymax = min(ys), max(ys)

 
    # On tente jusqu'à trouver une case libre au hasard
    while True:
        if radius == 0:
            # p = 0 : adjacence stricte
            # On choisit un pion déjà posé au hasard, puis un de ses 8 voisins
            ref = random.choice(positions)
            dx, dy = random.choice([(1,0),(-1,0),(0,1),(0,-1),(1,1),(-1,-1),(1,-1),(-1,1)])
            nx, ny = ref[0] + dx, ref[1] + dy
        else:
            # p > 0 : on tire une case au hasard dans la fenêtre
            # [xmin - radius, xmax + radius] × [ymin - radius, ymax + radius]
            # Plus p est grand, plus radius est élevé, plus la zone est grande
            nx = random.randint(int(xmin - radius), int(xmax + radius))
            ny = random.randint(int(ymin - radius), int(ymax + radius))
 
        # Si la case tirée est libre, on la retourne
        if game.vide(nx, ny):
            return nx, ny

def simulation (p=0.0, max_moves=500):
    """
    Simule une partie entre deux bots.
    winner = 0 si match nul (limite de coups atteinte).
    Utiliser pour tester le code
    """
    move_num = 0
    game = App1_def(5) #crée une nouvelle partie vide
    start = time.perf_counter() # démarre un chrono pour voir le temps qu'a duré la partie

    while True : #compteur de coups
        x, y = bot_mv(game, p) #bot choisi une case selon le paramètre p
        win = game.placer(x, y) #bot place un pion et renvoie True si victoire
        move_num +=1 
        if win:
            winner = 1 if game.current_player == 2 else 2 #Si victoire (if win) : Comme placer switche le joueur après avoir joué, current_player pointe déjà sur le joueur suivant.
            #                                             Donc si current_player == 2, c'est que le joueur 1 vient de gagner, et inversement.
            duration = time.perf_counter() - start
            return winner, move_num + 1, duration #qui a gagné, en combien de coups, et en combien de temps.

#main===============
if __name__ == "__main__":    
    game = App1_def(random.randint(2, 10))
    move_num = 0 #compteur du nombre de coups jouer
    while True:
        x, y = bot_mv(game, p=1)  #p pour le style de jeu, varie selon la valeur, plus p proche de 1 plus la partie est longue
        win = game.placer(x, y) 
        move_num += 1 #incrémentation du nombre de coups
        if win:
            winner = 1 if game.current_player == 2 else 2
            break
    print(f"Gagnant : Joueur {winner} en {move_num} coups")