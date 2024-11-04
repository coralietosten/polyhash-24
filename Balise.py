from Vecteur2 import *

nb_balise = 0 # Nombre de balises total créé en tout

class Balise:
    def __init__(self,coord:Vecteur2):
        global nb_balise  # Indique que nb_balise est une variable globale
        self.id = nb_balise
        nb_balise += 1 # Incrémente de 1 la variable statique (commune à chaque instance)
        self.coord = coord

    def __str__(self):
        return f"Balise (id : {self.id}, coord : {self.coord})"

    def __repr__(self):
        return self.__str__()