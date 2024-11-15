from Polyhash import *
from Ballon import Ballon

from StrategieInterface import StrategieInterface
from Strategies.StrategieAleatoire import StrategieAleatoire 
from Vecteur3 import Vecteur3
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

    def calcul_score_tour(self):
        """calcul le score du tour pour tous les ballons""" 
        pass

    def mise_a_jour(self):
        """Met à jour le score, la liste 'ballons', la liste 'action' et num_tour pour un tour et tous les ballons"""
        self.num_tour +=1
        action_tour = []
        carte_vent = self.polyhash.carte_vent
        for b in self.ballons :
            #modifications des coordonnées des ballons
            action_b = self.strategie(b, self.polyhash) #récupère l'altitude où doit aller le ballon
            b.coord += Vecteur3(0,0,action_b) #modification de la coordonnée altitude
            b.coord += carte_vent[b.coord.z][b.coord.x][b.coord.y] #modification des coordonnées x et y
            action_tour.append(self.strategie(b,self.polyhash)) #ajout des actions de chaque ballons
        self.actions.append(action_tour)
        self.score += calcul_score_tour()
        

    def lancement_jeu(self,strategie:StrategieInterface):
        """Exécute tout le jeu en utilisant la stratégie."""
        self.strategie=strategie
        self.initialisation()
        for i in range(self.polyhash.nombre_tour):
            self.mise_a_jour()


            
    
    