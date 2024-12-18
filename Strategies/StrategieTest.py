import os , sys
from os.path import dirname, join, abspath
sys.path.insert(0,abspath(join(dirname(__file__),'..')))

from random import randint
from Polyhash import Polyhash

from StrategieInterface import StrategieInterface

class StrategieTest(StrategieInterface):
    def __init__(self,coups : list):
        self.polyhassh = None
        self.tour = 0
        self.coups = coups
    def initialisation(self,polyhash : Polyhash):
        self.polyhash = polyhash
    
    def donne_action(self, ballon) -> int:
        if ballon.id == 0 :
            self.tour +=1
        return self.coups[self.tour-1]
        
