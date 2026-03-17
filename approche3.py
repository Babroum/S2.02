import numpy as np

class Approche3 :
    def __init__(self, N=5):
        self.blocs = {}
        self.N = N

    def _cle_bloc(self, x, y):
        return (x // 3, y // 3)

    def _position_locale(self, x, y):
        return (x % 3, y % 3)

    def get_symbole(self, x, y):
        cle = self._cle_bloc(x, y)
        if cle not in self.blocs:
            return 0
        lx, ly = self._position_locale(x, y)
        return self.blocs[cle][lx][ly]

    def placer(self, x, y, joueur):
        cle = self._cle_bloc(x, y)
        if cle not in self.blocs:
            self.blocs[cle] = np.zeros((3, 3), dtype=int)
        lx, ly = self._position_locale(x, y)
        self.blocs[cle][lx][ly] = joueur

    def verifier_victoire(self, x, y, joueur):
        directions = [(1, 0), (0, 1), (1, 1), (1, -1)]
        for dx, dy in directions:
            count = 1
            for i in range(1, self.N):
                if self.get_symbole(x + i * dx, y + i * dy) == joueur:
                    count += 1
                else:
                    break
            for i in range(1, self.N):
                if self.get_symbole(x - i * dx, y - i * dy) == joueur:
                    count += 1
                else:
                    break
            if count >= self.N:
                return True
        return False

