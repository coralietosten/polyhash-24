from __future__ import annotations
import os, sys
from os.path import dirname, join, abspath
from Vecteur3 import Vecteur3
from Vecteur2 import Vecteur2

sys.path.insert(0, abspath(join(dirname(__file__), '..')))
from Polyhash import Polyhash
from Ballon import Ballon
from StrategieInterface import StrategieInterface
from copy import deepcopy


class StrategieArbre(StrategieInterface):
    def __init__(self):
        self.polyhash = None
        self.appel = 0
        self.chemins = None
    
    def initialisation(self, polyhash: Polyhash):
        self.polyhash = polyhash
        cord = self.polyhash.depart + self.polyhash.carte_vent.vents[0][self.polyhash.depart.y][self.polyhash.depart.x]
        racine = Noeud(cord=cord, action=1, score=0, alittude=-1, profondeur=0)
        arbre = Arbre(racine, self.polyhash)
        self.chemins = arbre.chemin()

    def donne_action(self, ballon: Ballon) -> int:
        chemin = self.chemins[ballon.id]
        index_action = self.appel % len(chemin)
        action = chemin[index_action]
        self.appel += 1
        return action


class Noeud:
    def __init__(self, cord: Vecteur2, action: int, score: int, alittude: int, profondeur: int, 
                 racine: Noeud = None, enfant_decendre: Noeud = None, enfant_reste: Noeud = None, enfant_monte: Noeud = None):
        self.racine = racine
        self.cord = cord
        self.action = action
        self.score = score
        self.alittude = alittude
        self.enfant_decendre = enfant_decendre
        self.enfant_reste = enfant_reste
        self.enfant_monte = enfant_monte
        self.profondeur = profondeur

    def __str__(self):
        return f"cord: {self.cord}, action: {self.action}, score: {self.score}"


class Arbre:
    def __init__(self, racine: Noeud, polyhash: Polyhash):
        self.racine = racine
        self.profendeur = polyhash.nombre_tours - 1
        self.polyhash = polyhash
        self.nombre_feuille_garder = polyhash.nombre_ballons
        self.alittude = polyhash.altitudes
        self.carteIDBalises = deepcopy(polyhash.carteIDBalises)
        self.balises_couvertes = {}

    def construire_arbre(self):
        feuilles = [self.racine]
        self.balises_couvertes = {0: set()}

        for i in range(self.profendeur):
            nouvelles_feuilles = []
            self.balises_couvertes[i + 1] = set()

            for noeud in feuilles:
                actions_possibles = [0]
                if noeud.alittude > 0:
                    actions_possibles.append(-1)
                if noeud.alittude < self.alittude - 1:
                    actions_possibles.append(1)

                for action in actions_possibles:
                    nouvel_alittude = noeud.alittude + action
                    nouvel_cord = noeud.cord + self.polyhash.carte_vent.vents[nouvel_alittude][noeud.cord.y][noeud.cord.x]

                    if nouvel_cord.y < self.polyhash.lignes:
                        nouvel_cord.x %= self.polyhash.colonnes
                        balises = self.carteIDBalises[nouvel_cord.y][nouvel_cord.x]
                        balises_non_couvertes = [b for b in balises if b not in self.balises_couvertes[i]]
                        nouvel_score = noeud.score + len(balises_non_couvertes)

                        nouvel_enfant = Noeud(
                            cord=nouvel_cord,
                            action=action,
                            score=nouvel_score,
                            alittude=nouvel_alittude,
                            racine=noeud,
                            profondeur=noeud.profondeur + 1
                        )

                        self.balises_couvertes[i + 1].update(balises_non_couvertes)

                        if action == -1:
                            noeud.enfant_decendre = nouvel_enfant
                        elif action == 0:
                            noeud.enfant_reste = nouvel_enfant
                        elif action == 1:
                            noeud.enfant_monte = nouvel_enfant

                        nouvelles_feuilles.append(nouvel_enfant)

            nouvelles_feuilles.sort(key=lambda n: n.score, reverse=True)
            feuilles = nouvelles_feuilles[:self.nombre_feuille_garder]

        return feuilles

    def chemin(self):
        feuilles = self.construire_arbre()
        resultat = []
        for i in range(self.nombre_feuille_garder):
            actions = []
            copie_feuille: Noeud = feuilles[i]

            while copie_feuille.racine is not None:
                actions.insert(0, copie_feuille.action)
                self.balises_couvertes[copie_feuille.profondeur] = self.carteIDBalises[copie_feuille.cord.y][copie_feuille.cord.x]
                copie_feuille = copie_feuille.racine

            resultat.append(actions)
            print(f"Chemin {i}: {actions}")
        return resultat
