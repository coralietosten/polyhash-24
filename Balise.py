from Vecteur2 import *

class Balise:
    nb_balise = 0 #Nombre de balises total créé en tout
    def __init__(self,coord:Vecteur2):
        self.id = self.nb_balise
        self.coord = coord

        self.nb_balise +=1 #Incrémente de 1 la variable statique (commune à chaque instance)
