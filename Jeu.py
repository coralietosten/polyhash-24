from Polyhash import *
from Ballon import Ballon

from StrategieInterface import StrategieInterface
from Strategies.StrategieAleatoire import StrategieAleatoire 

class Jeu:

    def __init__(self,polyhash):
        self.polyhash : Polyhash = polyhash
        self.ballons = []
        self.carteIdBalises = []
        self.score = 0
        self.actions = []
        self.strategie = None
        self.num_tour = 0

    def initialisation(self):
        for _ in range(self.polyhash.ballons):
            self.ballons.append(Ballon(self.polyhash.depart))
        #todo : Ajouter la carteIdBalise

    def mise_a_jour(self):
        """Met à jour le score, la liste 'ballons', la liste 'action' et num_tour """
        
        pass

    def lancement_jeu(self,strategie:StrategieInterface):
        """Exécute tout le jeu en utilisant la stratégie."""
        pass
    
    