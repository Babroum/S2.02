import random

DIRECTIONS = [(1, 0), (0, 1), (1, 1), (1, -1)]  # H, B, ↗, ↘

class App1_def :

    def __init__ (self):
        self.board = []   # liste de [(x, y, joueur...)]
        self.current_player = 1

    def vide (self, x , y):
        """vérification de si les coordonnés sont prise ou non
        """
        for mx, my in self.board :
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
        pos_joueur = set()
        for mx, my, p in self.board:
            if p == player:
                pos_joueur.add((mx, my))
        for dx, dy in DIRECTIONS: #parcourt les 4 directions horizontales et les 2 diag repésenté par un veteur
            #combien de pions conséc du joueur sur trouve dans la direction lu
            total = (1 + self.Addition_pion(pos_joueur, x, y, dx, dy) #sens normal (le 1 pour le pions qui vient d'etre poser en (x,y))
                       + self.Addition_pion(pos_joueur, x, y, -dx, -dy)) #sens opposé
            if total >= 5:
                return True
        return False

    def get_all_position (self) : 
        """renvoie toute les positions des joueurs
        """
        return [(mx, my) for mx, my, _ in self.moves]


    def reset (self):
        self.moves = []
        self.current_player = 1
#=====BOT=====

def dispersion_radius(p): # p rayon
    """
    p se rapproche de 1, plus (1 - p) petit, plus 1 / (1 - p) explose. Le min(..., 1000) empêche le rayon de dépasser 1000,
    correspond à [xmin - 1000, xmax + 1000].
    """
    if p >= 1.0: #car 1/0 impossible
        return 1000
    return min(1.0 / (1.0 - p), 1000) #formule sur le projet f(p) = 1 / (1 - p)

def bot_mv(game,p):
    """
    Choisit un coup aléatoire selon le paramètre de dispersion p.
    """
    # Récupère les cases déjà jouées (des deux joueurs)
    positions = game.get_all_podition()
 
    # Premier coup
    if not positions:
        return 0, 0
 
    # Calcule les bornes actuelles du plateau (case la plus à gauche, droite, haut, bas)
    xs = [pos[0] for pos in positions]
    ys = [pos[1] for pos in positions]
    xmin, xmax = min(xs), max(xs)
    ymin, ymax = min(ys), max(ys)
 
    # Calcule le rayon de dispersion selon p : p grand, zone large
    radius = dispersion_radius(p)
 
    # On tente jusqu'à 10 000 fois de trouver une case libre au hasard
    for _ in range(10000):
        if p == 0:
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
        if game.is_empty(nx, ny):
            return nx, ny