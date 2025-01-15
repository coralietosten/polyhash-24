import os , sys
from os.path import dirname, join, abspath
sys.path.insert(0,abspath(join(dirname(__file__),'..')))

from random import randint
from math import sqrt
from Polyhash import Polyhash
from Balise import Balise
from Ballon import Ballon
from Vecteur3 import Vecteur3
from Vecteur2 import Vecteur2

from StrategieInterface import StrategieInterface

class StrategieTripleLigne(StrategieInterface):
    def __init__(self):
        self.polyhassh = None
        self.objectifs = {}
        self.ballons = []
        self.yobjectif = 0
        self.tour = 0
        self.interval = 36
    def initialisation(self,polyhash : Polyhash):
        self.polyhash = polyhash
        self.yobjectif1Afrique = 10
        self.yobjectif2Afrique = 20
        self.yobjectif3Afrique = 30
        self.yobjectif1Australie = 10
        self.yobjectif2Australie = 20
        self.yobjectif3Australie = 30
        self.yobjectif1Amerique = 10
        self.yobjectif2Amerique = 20
        self.yobjectif3Amerique = 30
        self.debAfrique = 120
        self.debAustralie = 220

    def meilleury(self):
        liste = [0 for i in range(self.polyhash.lignes)]
        for balise in self.polyhash.cibles :
            liste[balise.coord.y] += 1
        maxi = liste[0]
        indicemaxi = 0
        for i in range(len(liste)):
            if liste[i] > maxi:
                maxi = liste[i]
                indicemaxi = i
        return indicemaxi

    def donne_action(self, ballon) -> int:
        """entrée : un ballon et les données du polyhash
           sortie : l'action à effectuer pour un tour pour un ballon"""
        if ballon.id not in self.ballons :
            self.ballons.append(ballon)
        self.tour += 1
        if (ballon.id - ballon.id%3) * self.interval >= self.tour :
            return 0
        #calcul des altitudes disponibles
        coord_ballon = ballon.coord
        altitudes_disponibles = []
        if coord_ballon.z > 0 and coord_ballon.z < self.polyhash.altitudes -1:
            altitudes_disponibles.append(1)
            altitudes_disponibles.append(-1)
            altitudes_disponibles.append(0)
        elif coord_ballon.z <= 0 :
            altitudes_disponibles.append(1)
        elif coord_ballon.z == self.polyhash.altitudes -1:
            altitudes_disponibles.append(-1)
            altitudes_disponibles.append(0)
        #récuperation des vents
        carte_vent = self.polyhash.carte_vent
        #determination des coordonnées les plus proche de la cible objectif du ballon
        dist_min = self.polyhash.lignes * self.polyhash.colonnes
        altitude_a_prendre = 0
        for i in altitudes_disponibles :
            coord_v2_ballon = Vecteur2(coord_ballon.x, coord_ballon.y)
            coord_arrivee = coord_v2_ballon + carte_vent[coord_ballon.z + i][coord_ballon.y][coord_ballon.x]
            if coord_arrivee.x < self.polyhash.colonnes and coord_arrivee.x >= 0 and coord_arrivee.y < self.polyhash.lignes and coord_arrivee.y >= 0 :
                if(ballon.id%3 == 0) :
                    if(ballon.coord.x > self.debAfrique and ballon.coord.x < self.debAustralie):
                        dist = abs(coord_arrivee.y - self.yobjectif1Afrique)
                    elif(ballon.coord.x > self.debAustralie):
                        dist = abs(coord_arrivee.y - self.yobjectif1Australie)
                    else :
                        dist = abs(coord_arrivee.y - self.yobjectif1Amerique)
                elif(ballon.id%3 == 1) :
                    if (ballon.coord.x > self.debAfrique and ballon.coord.x < self.debAustralie):
                        dist = abs(coord_arrivee.y - self.yobjectif2Afrique)
                    elif (ballon.coord.x > self.debAustralie):
                        dist = abs(coord_arrivee.y - self.yobjectif2Australie)
                    else:
                        dist = abs(coord_arrivee.y - self.yobjectif2Amerique)
                else :
                    if (ballon.coord.x > self.debAfrique and ballon.coord.x < self.debAustralie):
                        dist = abs(coord_arrivee.y - self.yobjectif3Afrique)
                    elif (ballon.coord.x > self.debAustralie):
                        dist = abs(coord_arrivee.y - self.yobjectif3Australie)
                    else:
                        dist = abs(coord_arrivee.y - self.yobjectif3Amerique)
                if dist < dist_min :
                    dist_min = dist 
                    altitude_a_prendre = i
        return altitude_a_prendre

        

