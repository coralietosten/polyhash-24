from typing import List
from Balise import Balise

class CarteIDBalises:
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
        init carteIDBalises 
        """
        carteIDBalises = [[[] for i in range(nb_colonnes)] for j in range(nb_lignes)]
        cercle = self.coocercle(2)
        for balise in balises :
            for cord in cercle :
                if int(balise.coord.y) + cord[1] >= 0 and int(balise.coord.y) + cord[1] <  nb_lignes :
                    carteIDBalises[int(balise.coord.y) + cord[1]][(int(balise.coord.x) + cord[0])%nb_colonnes].append(balise.id)
        return carteIDBalises
