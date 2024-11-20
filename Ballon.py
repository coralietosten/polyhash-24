from Vecteur3 import *
from Balise import *


class Ballon:
    def __init__(self,coord:Vecteur3,id:int):
        self.id = id
        self.coord = coord
        self.estSortie = False
