from Vecteur2 import *


class Balise:
    nb_balise = 0 # Nombre de balises total créé en tout
    def __init__(self,coord:Vecteur2):
        self.id = self.nb_balise
        self.coord = coord

        Balise.nb_balise += 1 # Incrémente de 1 la variable statique (commune à chaque instance)

    def __str__(self):
        return f"Balise (id : {self.id}, coord : {self.coord})"

    def __repr__(self):
        return self.__str__()