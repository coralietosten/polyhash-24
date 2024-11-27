from Vecteur3 import *
from Balise import *


class Ballon:
    def __init__(self,coord:Vecteur3,id:int):
        self.id = id
        self.coord = coord
        self.estSortie = False

    def __str__(self):
        return f"Ballon (id : {self.id}, coord : {self.coord},estSortie : {self.estSortie})"

    def __repr__(self):
        return self.__str__()