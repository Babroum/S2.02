import matplotlib.pyplot as plt
import Approche2 as A2

# liste du temps d'exécution de chaque coup de chaque approche
a1 = []
a2 = []
a3 = []
a4 = []

App2 = A2.Jeu() # Initialise le jeu

def play(coup):
    cpt = 0
    # while pour l'approche 2
    while cpt < coup:
        cpt += 1
        t1 = App2.jouerCoup(App2.joueur1, False)
        # le joueur a gagné
        if t1 == -1:
            break
        a2.append(t1)

        cpt += 1
        t2 = App2.jouerCoup(App2.joueur2, False)
        if t2 == -1:
            break
        a2.append(t2)


coup = 10000

play(coup)

fig, ax = plt.subplots(figsize=(10, 6))

#ax.plot(coup, a1, marker='o', label='Approche 1')
ax.plot(range(len(a2)), a2, marker='s', label='Approche 2')
#ax.plot(coup, a3, marker='^', label='Approche 3')
#ax.plot(coup, a1, marker='D', label='Approche 4')

ax.set_xlabel('Nombre de coup jouer')
ax.set_ylabel('Temps d\'exécution (ms)')
ax.set_title('Temps d\'exécution d\'un coup en fonction du nombre de coup jouer')
ax.legend()
ax.grid(True, linestyle='--', alpha=0.5)

plt.tight_layout()
plt.show()