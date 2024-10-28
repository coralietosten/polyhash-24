from Vecteur3 import *
from Balise import *


class Ballon:
    def __init__(self,coord:Vecteur3,objectif:Balise | None):
        self.coord = coord
        self.objectif = objectif
