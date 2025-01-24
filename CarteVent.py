from typing import List
from Vecteur2 import *

class CarteVent:
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
    