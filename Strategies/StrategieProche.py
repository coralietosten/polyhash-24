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

class StrategieProche(StrategieInterface):
    def __init__(self):
        self.polyhassh = None
        self.objectifs = {}
        self.ballons = []
    def initialisation(self,polyhash : Polyhash):
        self.polyhash = polyhash
        self.ballons = []
        self.objectifs = self.objectifs_ballons()
    
    def distance (self,vecteur1 : Vecteur3 , vecteur2 : Vecteur2):
        """
        renvoie la distance entre le vecteur1 et le vecteur2
        """
        return sqrt((vecteur1.x - vecteur2.x)**2 + (vecteur1.y - vecteur2.y)**2) 

    def distance_v2 (self,vecteur1 : Vecteur2, vecteur2 : Vecteur2):
        """
        renvoie la distance entre le vecteur1 et le vecteur2
        """
        return sqrt((vecteur1.x - vecteur2.x)**2 + (vecteur1.y - vecteur2.y)**2)

    def balise_proche(self,coords):
        """
        renvoie la balise la plus proche du ballon 
        """
        # coord_ballon = ballon.coord.x,ballon.coord.y
        bal_proche = Balise(Vecteur2(0,0))
        dist_min = self.polyhash.colonnes * self.polyhash.lignes
        for b in self.polyhash.cibles:
            if self.distance (coords , b.coord) < dist_min :
                dist_min = self.distance (coords , b.coord)
                bal_proche = b
        return bal_proche
    
    def balise_proche2(self,ballon):
        """
        renvoie la deuxieme balise la plus proche du ballon
        """
        coord_ballon = ballon.coord.x,ballon.coord.y
        bal_proche = Balise(Vecteur2(0,0))
        dist_min = self.polyhash.colonnes * self.polyhash.lignes
        for b in self.polyhash.cibles:
            if self.distance (coord_ballon , b.coord) < dist_min :
                if dist_min != self.balise_proche(ballon) :
                    dist_min = self.distance (coord_ballon , b.coord)
                    bal_proche = b
        return bal_proche

    def objectifs_ballons(self):
        """
        renvoie la cible objectif de chaque ballon sous forme de dictionnaire : clé : id_ballon, valeur :cible objectif du ballon
        """
        nb_ballons = self.polyhash.nombre_ballons
        objectifs ={}
        cibles = self.polyhash.cibles
        for i in range(nb_ballons):
            balise_i = self.balise_proche(self.polyhash.depart)
            if balise_i in cibles :
                cibles.remove(balise_i)
            objectifs[i] = balise_i
        return objectifs
    
    def donne_action(self, ballon) -> int:
        """entrée : un ballon et les données du polyhash
           sortie : l'action à effectuer pour un tour pour un ballon""" 
        if ballon.id not in self.ballons :
            self.ballons.append(ballon)
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
        #determination des coordonnées les plus pres de la cible objectif du ballon
        dist_min = self.polyhash.lignes * self.polyhash.colonnes
        altitude_a_prendre = 0
        for i in altitudes_disponibles :
            coord_v2_ballon = Vecteur2(coord_ballon.x, coord_ballon.y)
            coord_arrivee = coord_v2_ballon + carte_vent[coord_ballon.z + i][coord_ballon.y][coord_ballon.x]
            if coord_arrivee.x < self.polyhash.colonnes and coord_arrivee.x >= 0 and coord_arrivee.y < self.polyhash.lignes and coord_arrivee.y >= 0 :#si le ballon est dans la map
                dist = self.distance_v2(self.objectifs[ballon.id].coord, coord_arrivee)
                if dist < dist_min :
                    dist_min = dist 
                    altitude_a_prendre = i

        #recalcul de la cible objectif du ballon s'il est sur sa case
        if ballon.coord == self.objectifs[ballon.id].coord :
            balise2 = self.balise_proche2(ballon)
            if self.distance(ballon.coord , balise2.coord) < self.distance(ballon.coord,self.objectifs[ballon.id].coord ):
                self.objectifs[ballon.id] = balise2
        return altitude_a_prendre


        

