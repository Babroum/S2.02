DIRECTIONS = [(1, 0), (0, 1), (1, 1), (1, -1)]  # H, B, ↗, ↘
class App1_def :

    def __init__ (self):
        self.board = []   # liste de [(x, y, joueur...)]
        self.current_player = 1

    #vérification de si le les coordonnés sont prise ou non
    def vide (self, x , y):
        for mx, my in self.board :
            if mx == x and my == y :
                return False
        return True
        
    #placer le pion du joueur
    def placer (self, x, y):  
        if not self.vide(x,y) : #condition de placement (si c'est deja plein, on prend pas)
            return False
        self.board.append((x, y, self.current_player)) #on place dans la liste la position et le type du joueur (rond ou croix)
        win = self.verif_win(x, y) 
        if self.current_player == 1 :  #on effectue le changement de joueur a la fin d'un tour
            self.current_player = 2 
        else :
            self.current_player = 1
        
        return win #on renvoie la fonction de victoire
        
    #compte le nombre de pion du joueur consécutif pour voir si il y a une victoire
    def Addition_pion (self, x, y, dx, dy, pos_joueur): 
        #on parcourt la liste et on regarde s'il y a un 4 fois le meme symbole dans la meme direction 
        count = 0 
        cx = x + dx
        cy = y + dy
        while (cx, cy) in pos_joueur :
            count += 1
            cx += dx
            cy += dy
        return count

    def verif_win (self, x, y): #vérifie si le joueur gagne
        player = self.board[-1][2]
        #on fait l'ensemble des positions des joueur depuis la liste
        pos_joueur = set()
        for mx, my, p in self.board:
            if p == player:
                pos_joueur.add((mx, my))
        for dx, dy in DIRECTIONS:
            total = (1 + self.Addition_pion(pos_joueur, x, y, dx, dy)
                       + self.Addition_pion(pos_joueur, x, y, -dx, -dy))
            if total >= 5:
                return True
        return False

    def get_all_position (self) : #renvoie toute les positions des joueurs
        return [(mx, my) for mx, my, _ in self.moves]


    def reset (self): # reset la liste pour la prochaine partie
        self.moves = []
        self.current_player = 1