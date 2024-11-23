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
        #self.ballons = {}
        self.ballons = []
    def initialisation(self,polyhash : Polyhash):
        self.polyhash = polyhash
    
    def distance (self,vecteur1 : Vecteur3 , vecteur2 : Vecteur2):
        """
        renvoie la distance entre le vecteur1 et le vecteur2
        """
        vecteur = vecteur2
        return sqrt((vecteur1.x - vecteur2.x)**2 + (vecteur1.y - vecteur2.y)**2) 

    def distance_v2 (self,vecteur1 : Vecteur2, vecteur2 : Vecteur2):
        """
        renvoie la distance entre le vecteur1 et le vecteur2
        """
        vecteur = vecteur2
        return sqrt((vecteur1.x - vecteur2.x)**2 + (vecteur1.y - vecteur2.y)**2)

    def balise_proche(self, ballon : Ballon):
        """
        renvoie la balise la plus proche du ballon
        """
        bal_proche = Balise(Vecteur2(0,0))
        dist_min = self.polyhash.colonnes * self.polyhash.lignes
        for b in self.polyhash.cibles:
            if self.distance (ballon.coord , b.coord) < dist_min :
                dist_min = self.distance (ballon.coord , b.coord)
                bal_proche = b
        return bal_proche

    def objecttifs_ballons(self, ballons):
        """
        renvoie la cible objectif de chaque ballon sous forme de dictionnaire : clé : ballon, valeur :cible objectif du ballon
         """
        objectifs ={}
        cibles = self.polyhash.cibles
        for i in range(len(ballons)):
            balise_i = self.balise_proche(ballons[i])
            if balise_i in cibles :
                cibles.remove(balise_i)
            objectifs[ballons[i]] = balise_i
        return objectifs
    
    def donne_action(self, ballon) -> int:
        """entrée : un ballon et les données du polyhash
           sortie : l'action à effectuer pour un tour pour un ballon"""
        if ballon.id not in self.ballons :
            self.ballons.append(ballon)
        objectifs = self.objecttifs_ballons(self.ballons)
        #calcul des altitudes disponibles
        coord_ballon = ballon.coord
        altitudes_disponibles = [0]
        if coord_ballon.z == 0 :
            altitudes_disponibles.append(1)
        elif coord_ballon.z == self.polyhash.altitudes -1 :
            altitudes_disponibles.append(-1)
        else :
            altitudes_disponibles.append(1)
            altitudes_disponibles.append(-1)
        #récuperation des vents
        carte_vent = self.polyhash.carte_vent
        #determination des coordonnées les plus pres de la cible objectif du ballon
        dist_min = self.polyhash.lignes * self.polyhash.colonnes
        altitude_a_prendre = 0
        for i in altitudes_disponibles :
            coord_v2_ballon = Vecteur2(coord_ballon.x, coord_ballon.y)
            coord_arrivee = coord_v2_ballon + carte_vent[coord_ballon.z + i][coord_ballon.y][coord_ballon.x]
            dist = self.distance_v2(objectifs[ballon].coord, coord_arrivee)
            if dist < dist_min :
                dist_min = dist 
                altitude_a_prendre = i 
        return altitude_a_prendre


        



        if ballon.coord.z == 0 :
            return randint(0,1) #Renvoie soit 0 (Rester) soit 1 (Monter)
        if ballon.coord.z == self.polyhash.altitudes-1 :
            return randint(0,1)-1 #Renvoie soit -1 (Descendre) soit 0 (Rester)
        return randint(0,2)-1 #Renvoie soit -1 (Descendre) soit 0 (Rester) soit 1 (Monter)

