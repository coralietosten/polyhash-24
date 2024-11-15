import os , sys
from os.path import dirname, join, abspath
sys.path.insert(0,abspath(join(dirname(__file__),'..')))

from StrategieInterface import StrategieInterface

class StrategieAleatoire(StrategieInterface):
    def initialisation(self):
        pass
    def donne_action(self, ballon , polyhash) -> int:
        """entrée : un ballon et les données du polyhash
           sortie : l'action à effectuer pour un tour pour un ballon"""
        pass

