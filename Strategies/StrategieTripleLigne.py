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
        self.interval = 36 #intervalle auquel les ballons sont relachés 
    def initialisation(self,polyhash : Polyhash):
        self.polyhash = polyhash
        #décalage par rapport aux positions 10 20 30 pour chaque continent
        decalageAf = 1
        decalageAu = 0
        decalageAm = -1
        self.yobjectif1Afrique = 10 + decalageAf
        self.yobjectif2Afrique = 20+ decalageAf
        self.yobjectif3Afrique = 30+ decalageAf
        self.yobjectif1Australie = 10+ decalageAu
        self.yobjectif2Australie = 20+ decalageAu
        self.yobjectif3Australie = 30+ decalageAu
        self.yobjectif1Amerique = 10+ decalageAm
        self.yobjectif2Amerique = 20+ decalageAm
        self.yobjectif3Amerique = 30+ decalageAm
        #coordonnée x pour lesquels les ballons changent d'objectif y (pour l'Afrique et pour l'Australie)
        self.debAfrique = 120
        self.debAustralie = 220

    def meilleury(self):
        """
        fonction non utilisée mais qui pourrait être utile pour un début d'automatisation
        renvoit la coordonnée y qui rencontre le plus de balise.
        """
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
        """
        entrée : un ballon et les données du polyhash
        sortie : l'action à effectuer pour un tour pour un ballon

        calcul avec le même principe que la stratégie proche, l'action a prendre pour s'aligner au plus proche de la coordonnée y
        désirée, la coordonnée y est choisit via les variables données au debut.

        On divise les ballons en 3 groupes avec leur ID.
        Avec les groupes et les continents ils ont une coordonnée y spécifique a choisir.
        """
        if ballon.id not in self.ballons :
            self.ballons.append(ballon)
        self.tour += 1
        if ballon.id * self.interval >= self.tour :
            return 0
        if (ballon.id%3 == 0):
            self.tour -= 1
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