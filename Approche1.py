class App1_def :

    def __init__ (self):
        self.board = {}   # {(x, y): 1 ou 2}
        self.current_player = 1

    def vide (self, x , y):
        return(x, y) not in self.board    
    
    def placer (self, x, y):  #placer le pion du joueur
        if not self.vide(x,y) :
            return False
        self.board[(x,y)] = self.current_player

        if self.current_player == 1 :
            self.current_player = 2

        return self.verif_win
        
    def Addition_pion (self, x, y, dx, dy, joueur): #compte le nombre de pion du joueur consécutif 
        count = 0
        cx = x + dx
        cy = y + dy
        while self.board((cx, cy)) == joueur :
            count += 1
            cx += dx
            cy += dy
        return count

    # def verif_win (self): #vérifie si le joueur gagne


    # def get_all_position (self) : #renvoie toute les positions des joueurs


    # def reset (self): # reset le dico pour une nouvelle partie