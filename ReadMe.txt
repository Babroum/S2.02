========= Comment executé le code : =========
- A la racine du projet (commande à exécuté):

>>> python -m venv .venv
>>> .venv\Scripts\Activate
>>> pip install numpy
>>> pip install matplotlib
>>> pip install networkx
>>> python BOT.py

En lançant les paramètres de base sont : 
    - 100 coup max par partie
    - 10 parties
    - 5 symboles à devoir aligné
    - dispersion calculée à chaque coup

L'approche 2 et 4 peuvent être exécuté individuellement avec un affichage grâce à :

>>> python Approche2.py
>>> python Approche4.py

(Les 2 approches s'arrête quand il y a eu une victoire, sinon tourne à l'infini)