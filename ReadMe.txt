========= Comment exécuter le code : =========
- A la racine du projet (commande à exécuter):

>>> python -m venv .venv
>>> .Vent\Scripts\Activate
>>> pip install numpy
>>> pip install matplotlib
>>> pip install networkx
>>> python BOT.py

En lançant les paramètres de base sont : 
    - 100 coups max par partie
    - 10 parties
    - 5 symboles à devoir aligner
    - dispersion calculée à chaque coup

L'approche 2 et 4 peuvent être exécutées individuellement avec un affichage grâce à :

>>> python Approche2.py
>>> python Approche4.py

(Les 2 approches s'arrêtent quand il y a eu une victoire, sinon tournent à l'infini)
