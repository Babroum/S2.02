import matplotlib.pyplot as plt
import random
import time

import Approche1 as A1
import Approche2 as A2
import Approche3 as A3

# liste du temps d'exécution de chaque coup de chaque approche
a1 = []
a2 = []
a3 = []
a4 = []

def dispersion():
    """<b>Calcule la dispersion</b>
    """
    # random.random est compris entre 0(inclus) et 1(exclus) donc uniform permet d'avoir le 1 inclus
    p = random.uniform(0,1)
    if p == 0:
        return 1
    elif p == 1:
        return 1000
    else:
        # min pour évité de dépassé 1000 en distance max
        return min(int(1 / (1 - p)), 1000)

def play(coup):
    """<b>Exécute une partie</b>
    Alterne les coups de chaque approches qui utilise le même paramètre de dispersion pour chaque coup

    Args:
        coup (_int_): nombre de coup max avant de stopper l'exécution
    """
    # N symboles à aligné, commence à 2 pour évité de gagné a 1 symbole et limite à 10 pour que ce soit réalisable
    gomoku = random.randint(2, 10)
    print(f"Gomoku : {gomoku}")

    # Initialise le jeu des 4 approches
    App1 = A1.App1_def(gomoku)
    App2 = A2.Jeu(gomoku) 
    App3 = A3.Jeu(gomoku)

    # variables booléens de victoire
    app1Win = True
    app2Win = False
    app3Win = False
    app4Win = False   

    cpt = 0
    # while pour les approches
    while cpt < coup:
        p = dispersion()        

        # APPROCHE 1
        if not app1Win:
            cpt += 1 # incrémentation du nombre de coups
            startTime = time.time()
            x, y = A1.bot_mv(App1, p)  #p pour le style de jeu, varie selon la valeur, plus p proche de 1 plus la partie est longue
            win = App1.placer(x, y)             
            if win:
                app1Win = True
                print(f"app1 gagne au coup nb : {coup}")
            else:
                a1.append((time.time() - startTime) * 1000)
        
        # APPROCHE 2
        if not app2Win:
            cpt += 1
            t1 = App2.jouerCoup(App2.joueur1, False, p) # True False : pour l'affichage du coup avec matplotlib
            # le joueur a gagné (-1 si gagnant, sinon le temps d'un coup est retourné)
            if t1 == -1:
                app2Win = True
                print(f"app2 gagne au coup nb : {coup}")
            else:
                a2.append(t1)

            cpt += 1
            t2 = App2.jouerCoup(App2.joueur2, False, p)
            if t2 == -1:
                app2Win = True
                print(f"app1 gagne au coup nb : {coup}")
            else:
                a2.append(t2)

        # APPROCHE 3
        if not app3Win:
            cpt += 1
            startTime = time.time()
            t1 = App3.jouerCoup(App3.joueur1, p)
            if t1:
                app3Win = True
                print(f"app3 gagne au coup nb : {coup}")
            else:
                a3.append((time.time() - startTime) * 1000)

            startTime = time.time()
            t2 = App3.jouerCoup(App3.joueur2, p)
            if t2:
                app3Win = True
                print(f"app3 gagne au coup nb : {coup}")
            else:
                a3.append((time.time() - startTime) * 1000)
        # APPROCHE 4

    cpt = 0
    # while pour l'approche 3

    cpt = 0
    # while pour l'approche 4


# ============================== Exécution ==============================

coup = 100

play(coup)

fig, ax = plt.subplots(figsize=(10, 6))

ax.plot(range(len(a1)), a1, marker='o', label='Approche 1')
ax.plot(range(len(a2)), a2, marker='s', label='Approche 2')
ax.plot(range(len(a3)), a3, marker='^', label='Approche 3')
#ax.plot(coup, a1, marker='D', label='Approche 4')

ax.set_xlabel('Nombre de coup jouer')
ax.set_ylabel('Temps d\'exécution (ms)')
ax.set_title('Temps d\'exécution d\'un coup en fonction du nombre de coup jouer')
ax.legend()
ax.grid(True, linestyle='--', alpha=0.5)

plt.tight_layout()
plt.show()