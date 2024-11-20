from Vecteur3 import *
from Balise import *


class Ballon:
    def __init__(self,coord:Vecteur3,id:int,objectif:Vecteur2 | None=None):
        self.id = id
        self.coord = coord
        self.objectif = objectif
        self.estSortie = False
