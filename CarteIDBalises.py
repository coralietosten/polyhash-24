from typing import List

class CarteIDBalises:
    def __init__(self,listBalises :  List[List[List[int]]]):
        self.cartesBalises = listBalises

    def coocercle(v:int) -> list[(int,int)] :
        """
        entrée: le rayon v , la balise , le nombre de ligne l , le nombre de colonne c
        sortie: la liste des coordonnées proche de la balise à une distance de v
        """
        liste_touche =[]
        for i in range (-v,v+1,1):
            for j in range(-v,v+1,1):
                if ((-i)**2 + (-j)**2) <= v**2:
                    liste_touche.append((i,j))
        return liste_touche
