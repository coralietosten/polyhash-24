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
        for _ in range(self.polyhash.nombre_ballons):
            self.ballons.append(Ballon(Vecteur3(self.polyhash.depart.x,self.polyhash.depart.y,0)))
        #todo : Ajouter la carteIdBalise

    def calcul_score_tour(self):
        """calcul le score du tour pour tous les ballons""" 
        return 0

    def mise_a_jour(self):
        """Met à jour le score, la liste 'ballons', la liste 'action' et num_tour pour un tour et tous les ballons"""
        self.num_tour +=1
        action_tour = []
        carte_vent = self.polyhash.carte_vent
        for b in self.ballons :
            if not b.estSortie:
                #modifications des coordonnées des ballons
                action_b = self.strategie.donne_action(b) #récupère l'altitude où doit aller le ballon
                b.coord += Vecteur3(0,0,action_b) #modification de la coordonnée altitude
                vent = carte_vent[b.coord.z][b.coord.y][b.coord.x]
                b.coord += Vecteur3(vent.x,vent.y,0) #modification des coordonnées x et y
                b.coord.x %= self.polyhash.colonnes
                if b.coord.y < 0 or b.coord.y >= self.polyhash.lignes:
                    b.estSortie = True
            else:
                action_b=0
            action_tour.append(action_b) #ajout des actions de chaque ballons
        self.actions.append(action_tour)
        self.score += self.calcul_score_tour()
        

    def lancement_jeu(self,strategie:StrategieInterface):
        """Exécute tout le jeu en utilisant la stratégie."""
        self.strategie=strategie
        self.initialisation()
        strategie.initialisation(self.polyhash)
        for _ in range(self.polyhash.nombre_tours):
            self.mise_a_jour()


            
    
    