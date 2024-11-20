import os , sys
from os.path import dirname, join, abspath
sys.path.insert(0,abspath(join(dirname(__file__),'..')))

from random import randint
from math import sqrt
from Polyhash import Polyhash
from Balise import Balise
from Ballon import Ballon

from StrategieInterface import StrategieInterface

class StrategieProche(StrategieInterface):
    def __init__(self):
        self.polyhassh = None
    def initialisation(self,polyhash : Polyhash):
        self.polyhash = polyhash
    
    def distance (self,ballon : Ballon , balise : Balise):
        """
        renvoie la distance entre le ballon et la cible
        """
        return sqrt((ballon.coor.x - balise.coord.x)**2 + (ballon.coor.y - balise.coord.y))

    def balise_proche(self,ballon):
        """
        renvoie la balise la plus proche du ballon
        """
        id_bal_proche = -1
        dist_min = self.polyhash.colonnes * self.polyhash.lignes
        for b in self.polyhash.cibles:
            if self.distance (ballon , b) < dist_min :
                dist_min = self.distance (ballon , b)
                id_bal_proche = b.id
        return id_bal_proche





    def donne_action(self, ballon) -> int:
        """entrée : un ballon et les données du polyhash
           sortie : l'action à effectuer pour un tour pour un ballon"""
        if ballon.coord.z == 0 :
            return randint(0,1) #Renvoie soit 0 (Rester) soit 1 (Monter)
        if ballon.coord.z == self.polyhash.altitudes-1 :
            return randint(0,1)-1 #Renvoie soit -1 (Descendre) soit 0 (Rester)
        return randint(0,2)-1 #Renvoie soit -1 (Descendre) soit 0 (Rester) soit 1 (Monter)

