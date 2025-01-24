from typing import List
from Vecteur2 import Vecteur2

class CarteVent:
    """
    Classe représentant la carte des vents sous la forme d'un tableau de tableaux.

    Attributs :
    - vents (List[List[List[Vecteur2]]]): La liste des directions des vents selon les coordonnées sous la forme de Vecteur2.
    """
    def __init__(self,listVents :  List[List[List[Vecteur2]]]):
        self.vents = listVents
    
    def __str__(self):
        resultat = "CarteVent(\n    vents = [\n"
        
        for altitude in self.vents:
            resultat += "        [\n"
            for ligne in altitude:
                resultat += "            " + str(ligne) + ",\n"
            resultat += "        ],\n"
        
        resultat += "    ]\n)"
        return resultat

    def __repr__(self):
        return self.__str__()
    
    def __getitem__(self,index):
        return self.vents[index]