from typing import List
from Balise import Balise

class CarteIDBalises:
    """
    Classe représentant une carte des IDs des balises couvertes par chaque cellule.

    Attributs :
    - carteBalise (List[List[List[int]]]): Un tableau de tableaux contenant les IDs des balises couvertes par chaque cellule.

    Méthodes :
    - __init__(self, balises: List[Balise], nb_lignes: int, nb_colonnes: int, rayon: int): Initialise la carte des balises.
    - coocercle(self, v: int) -> List[Tuple[int, int]]: Retourne les coordonnées proches d'une balise à une distance de v.
    - init_carte(self, nb_lignes: int, nb_colonnes: int, rayon: int, balises: List[Balise]) -> List[List[List[int]]]: Initialise la carte des IDs des balises.
    """
    def __init__(self, balises: list[Balise],nb_lignes: int, nb_colonnes: int, rayon: int) :
        self.carteBalise = self.init_carte(nb_lignes, nb_colonnes, rayon, balises)

    def coocercle(self, v:int) -> list[(int,int)] :
        """
        entrée: le rayon v , la balise , le nombre de ligne l , le nombre de colonne c
        sortie: la liste des coordonnées proche de la balise à une distance de v
        """
        liste_touche =[]
        for i in range (-v,v+1,1):
            for j in range(-v,v+1,1):
                if ((-i)**2 + (-j)**2) <= v**2:
                    liste_touche.append([i,j])
        return liste_touche

    def init_carte(self, nb_lignes: int, nb_colonnes: int, rayon: int, balises: list[Balise]) :
        """
        Initialise la carte des IDs des balises.

        Args:
            nb_lignes (int): Le nombre de lignes de la carte.
            nb_colonnes (int): Le nombre de colonnes de la carte.
            rayon (int): Le rayon de couverture des balises.
            balises (List[Balise]): La liste des balises.

        Returns:
            List[List[List[int]]]: La carte des IDs des balises couvertes par chaque cellule.
        """
        carteIDBalises = [[[] for i in range(nb_colonnes)] for j in range(nb_lignes)]
        cercle = self.coocercle(rayon)
        for balise in balises :
            for cord in cercle :
                if balise.coord.y + cord[1] >= 0 and balise.coord.y + cord[1] <  nb_lignes :
                    carteIDBalises[balise.coord.y + cord[1]][(balise.coord.x + cord[0])%nb_colonnes].append(balise.id)
        return carteIDBalises
