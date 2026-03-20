import random
import time
from approche4 import placer, reinitialiser, nodes

N = 5
MAX_COUPS = 200

class Bot:
    def __init__(self, symbole, p):
        self.symbole = symbole
        self.p = p

    def dispersion(self):
        if self.p == 1:
            return 1000
        return round(self.p / (1 - self.p))

    def choisir_coup(self):
        if len(nodes) == 0:
            return (0, 0)

        xs = [pos[0] for pos in nodes]
        ys = [pos[1] for pos in nodes]
        xmin, xmax = min(xs), max(xs)
        ymin, ymax = min(ys), max(ys)

        if self.p == 0:
            cases = []
            directions = [(-1,-1),(-1,0),(-1,1),(0,-1),(0,1),(1,-1),(1,0),(1,1)]
            for (x, y) in list(nodes.keys()):
                for dx, dy in directions:
                    voisin = (x + dx, y + dy)
                    if voisin not in nodes:
                        cases.append(voisin)
            if cases:
                return random.choice(cases)
            return (xmin + random.randint(-1, 1), ymin + random.randint(-1, 1))

        rayon = self.dispersion()
        for _ in range(1000):
            x = random.randint(xmin - rayon, xmax + rayon)
            y = random.randint(ymin - rayon, ymax + rayon)
            if (x, y) not in nodes:
                return (x, y)

        return (xmax + 1, ymax + 1)


def jouer_partie(p, n=N):
    reinitialiser()
    bot1 = Bot("X", p)
    bot2 = Bot("O", p)
    joueurs = [bot1, bot2]
    tour = 0

    for coup in range(MAX_COUPS):
        bot = joueurs[tour % 2]
        x, y = bot.choisir_coup()
        if placer(x, y, bot.symbole, n):
            return bot.symbole, coup + 1
        tour += 1

    return None, MAX_COUPS


def simuler(nb_parties, p, n=N):
    resultats = {"X": 0, "O": 0, None: 0}
    temps_debut = time.time()

    for _ in range(nb_parties):
        gagnant, nb_coups = jouer_partie(p, n)
        resultats[gagnant] += 1

    temps_total = time.time() - temps_debut
    return resultats, temps_total


if __name__ == "__main__":
    for p in [0, 0.5, 1]:
        resultats, duree = simuler(100, p)
        print(f"p={p} | X gagne: {resultats['X']} | O gagne: {resultats['O']} | nul: {resultats[None]} | temps: {duree:.2f}s")
