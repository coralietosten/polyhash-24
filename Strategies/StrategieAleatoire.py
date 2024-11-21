import os , sys
from os.path import dirname, join, abspath
sys.path.insert(0,abspath(join(dirname(__file__),'..')))

from random import randint
from Polyhash import Polyhash

from StrategieInterface import StrategieInterface

class StrategieAleatoire(StrategieInterface):
    def __init__(self):
        self.polyhassh = None
    def initialisation(self,polyhash : Polyhash):
        self.polyhash = polyhash
    
    def donne_action(self, ballon) -> int:
        """entrée : un ballon et les données du polyhash
           sortie : l'action à effectuer pour un tour pour un ballon"""
        if ballon.coord.z <= 0 :
            return randint(0,1) #Renvoie soit 0 (Rester) soit 1 (Monter)
        if ballon.coord.z == self.polyhash.altitudes-1 :
            return randint(0,1)-1 #Renvoie soit -1 (Descendre) soit 0 (Rester)
        return randint(0,2)-1 #Renvoie soit -1 (Descendre) soit 0 (Rester) soit 1 (Monter)

