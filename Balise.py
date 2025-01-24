from Vecteur2 import Vecteur2

class Balise:
    """
    Classe représentant une balise.

    Attributs :
    - id (int) : Identifiant unique de la balise.
    - coord (Vecteur2) : Coordonnées de la balise.
    """
    nb_balise = 0 # Nombre de balises total créé en tout
    def __init__(self,coord:Vecteur2):
        """
        Initialise une nouvelle balise avec les coordonnées spécifiées.

        Args:
            coord (Vecteur2): Les coordonnées de la balise.
        """
        self.id = self.nb_balise
        self.coord = coord

        Balise.nb_balise += 1 # Incrémente de 1 la variable statique (commune à chaque instance)

    def __str__(self):
        return f"Balise (id : {self.id}, coord : {self.coord})"

    def __repr__(self):
        return self.__str__()