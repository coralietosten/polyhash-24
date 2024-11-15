from Polyhash import *
from StrategieInterface import StrategieInterface
from Strategies.StrategieAleatoire import StrategieAleatoire 

class Jeu:

    def __init__(self,polyhash):
        self.polyhash = polyhash
        self.ballons = []
        self.carteIdBalises = []
        self.score = 0
        self.actions = []
        self.strategie = None
        self.num_tour = 0

    def initialisation(self):
        pass

    def mise_a_jour(self):
        """Met à jour le score, la liste 'ballons', la liste 'action' et num_tour """
        
        pass

    def lancement_jeu(self,strategie:StrategieInterface):
        """Exécute tout le jeu en utilisant la stratégie."""
        pass
    
    