import os , sys
from os.path import dirname, join, abspath
sys.path.insert(0,abspath(join(dirname(__file__),'..')))

from Polyhash import Polyhash

from StrategieInterface import StrategieInterface
from Ballon import Ballon

class StrategieUnBallonParAltitude(StrategieInterface):
    def __init__(self):
        self.polyhash = None
    
    def initialisation(self, polyhash : Polyhash):
        self.polyhash = polyhash
    
    def donne_action(self, ballon: Ballon) -> int:
        if ballon.coord.z < ballon.id \
            and ballon.coord.z < self.polyhash.altitudes - 1 :
            return 1
        else : 
            return 0