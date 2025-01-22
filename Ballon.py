from Vecteur3 import Vecteur3

class Ballon:
    """
    Classe représentant un ballon.

    Attributs :
    - id (int) : Identifiant unique du ballon.
    - coord (Vecteur3) : Coordonnées du ballon.
    - estSortie (bool) : Indique si le ballon est sorti.
    """
    def __init__(self,coord:Vecteur3,id:int):
        self.id = id
        self.coord = coord
        self.estSortie = False

    def __str__(self):
        return f"Ballon (id : {self.id}, coord : {self.coord},estSortie : {self.estSortie})"

    def __repr__(self):
        return self.__str__()