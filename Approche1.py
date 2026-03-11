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
        #on parcours la liste et on regarde si il y a un 3 fois le meme symbole dans la meme direction 
        count = 0 
        cx = x + dx
        cy = y + dy
        while (cx, cy) in pos_joueur :
            count += 1
            cx += dx
            cy += dy
        return count

    #def verif_win (self): #vérifie si le joueur gagne


    # def get_all_position (self) : #renvoie toute les positions des joueurs


    # def reset (self): # reset le dico pour une nouvelle partie