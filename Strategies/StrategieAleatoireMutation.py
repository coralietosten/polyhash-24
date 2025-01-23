import os , sys
from os.path import dirname, join, abspath
sys.path.insert(0,abspath(join(dirname(__file__),'..')))

from random import randint
import random 
from Polyhash import Polyhash

from StrategieInterface import StrategieInterface

class StrategieAleatoireMutation(StrategieInterface):
    """
    Stratégie basée sur des actions aléatoires avec mutations pour les ballons

    À partir d'une solution existante, cette stratégie introduit des mutations pour essayer d'obtenir un meilleur chemin

    Les mutations permettent d'explorer de nouveaux chemins en modifiant légèrement les actions des ballons à chaque tour
    """
    def __init__(self, max_game=[]):
        self.polyhash = None
        self.max_game = max_game
        self.tour = -1
        ##### PARAMETRES MUTATION

        self.newgame_p = 0 # 0.01 #Probabilité de chercher un tout nouveau max_game
        self.nbMaxNewChemin =  0 # Nombre maximum de tout nouveau chemin mutation
        self.nbMaxMutations = 10  # Nombre maximum de modification possible 

        self.mutation_p = 0#.1 # Probabilite d'un ballon à avoir un tout nouveau chemin
        self.mutation_chemin_p = 0.0001 # Probabilite d'un ballon à avoir des changements dans son chemin
        
        self.ballonsNew = set()
        self.ballonsNewChange = dict()

    def initialisation(self,polyhash : Polyhash):
        self.polyhash = polyhash
        self.tour = -1
        self.ballonsNew = set()
        self.ballonsNewChange = dict()
        if random.random() <= self.newgame_p:
            self.max_game = []


    def donne_action(self, ballon) -> int:
        # Incrémente le tour si c'est le premier ballon
        if ballon.id == 0:
            self.tour += 1 
        
        if ballon.coord.z <-1:
            print(ballon.coord.z)

        # Si aucune action maximale n'a été définie, retourne une action simple
        if len(self.max_game) == 0:
            return self.donne_action_simple(ballon)
        
        if (ballon.id in self.ballonsNew or random.random() <= self.mutation_p) and len(self.ballonsNew)<= self.nbMaxNewChemin:
            self.ballonsNew.add(ballon.id)
            return self.donne_action_simple(ballon)
        
        # Si le ballon doit avoir des changements dans son chemin
        if (ballon.id in self.ballonsNewChange.keys() or random.random() <= self.mutation_chemin_p) :
            if ballon.id not in self.ballonsNewChange:
                self.ballonsNewChange[ballon.id] = 0
            nbtour = self.polyhash.nombre_tours
            # Vérifie si une mutation est nécessaire et si le nombre de mutations n'a pas dépassé le maximum
            if random.random() <= (1/nbtour)*(nbtour/(nbtour-self.tour)) and self.ballonsNewChange[ballon.id] <= self.nbMaxMutations:
                self.ballonsNewChange[ballon.id] += 1
                return self.donne_action_simple(ballon)

        a = self.max_game[self.tour][ballon.id]
        if a in self.actions(ballon):
            return a
        return 0

    def donne_action_simple(self, ballon) -> int:
        """
        entrée : un ballon et les données du polyhash    
        sortie : l'action à effectuer pour un tour pour un ballon
        """
        if ballon.coord.z <= 0 :
            return randint(0,1) # Renvoie soit 0 (Rester) soit 1 (Monter)
        if ballon.coord.z == self.polyhash.altitudes-1 :
            return randint(0,1)-1 # Renvoie soit -1 (Descendre) soit 0 (Rester)
        return randint(0,2)-1 # Renvoie soit -1 (Descendre) soit 0 (Rester) soit 1 (Monter)

    def actions(self,ballon) -> int:
        """
        sortie : les actions possibles pour un ballon
        """
        if ballon.coord.z <= 0 :
            return [0,1] # Renvoie soit 0 (Rester) soit 1 (Monter)
        if ballon.coord.z == self.polyhash.altitudes-1 :
            return [-1,0] # Renvoie soit -1 (Descendre) soit 0 (Rester)
        return [-1,0,1] # Renvoie toute les actions possibles