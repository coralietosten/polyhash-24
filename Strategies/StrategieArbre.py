from __future__ import annotations
import os , sys
from os.path import dirname, join, abspath
from Vecteur3 import Vecteur3
from Vecteur2 import Vecteur2
sys.path.insert(0,abspath(join(dirname(__file__),'..')))
from math import sqrt
from random import randint
from Polyhash import Polyhash
from Ballon import Ballon

from StrategieInterface import StrategieInterface
import heapq
from copy import deepcopy


class StrategieArbre(StrategieInterface):
    def __init__(self):
        self.polyhash = None
        self.appel = 0
        self.chemins = None 
    
    def initialisation(self, polyhash : Polyhash):
        self.polyhash = polyhash

        cord = self.polyhash.depart + self.polyhash.carte_vent.vents[0][self.polyhash.depart.y][self.polyhash.depart.x]
        racine = Noeud(cord = cord, action= 1, score = 0, alittude= -1, profondeur=0)
        
        arbre = Arbre(racine, self.polyhash)
        self.chemins = arbre.chemin()


    def donne_action(self, ballon: Ballon) -> int:
        chemin = self.chemins[ballon.id]
        index_action = self.appel % len(chemin)
        action = chemin[index_action]
        self.appel += 1
        return action


class Noeud :
    def __init__(self, cord: Vecteur2, action: int, score: int, alittude: int, profondeur: int, racine: Noeud = None, enfant_decendre: Noeud = None, enfant_reste: Noeud = None, enfant_monte: Noeud = None):
        self.racine = racine
        self.cord = cord
        self.action = action # poid de l'arrete
        self.score = score # valeur du noeud
        self.alittude = alittude
        self.enfant_decendre = enfant_decendre
        self.enfant_reste = enfant_reste
        self.enfant_monte = enfant_monte
        self.profondeur = profondeur

    def __str__(self):
        return "cord : "+  str(self.cord) + " action : " + str(self.action) + " score : " + str(self.score)
    
    def __eq__(self, value: Noeud):
        if value is not None :
            return self.cord == value.cord and self.alittude == value.alittude and self.action == value.action and self.score == value.score
        else : return False

class Arbre:
    def __init__(self, racine: Noeud, polyhash: Polyhash):
        self.racine = racine
        self.profendeur = polyhash.nombre_tours - 1
        self.polyhash = polyhash
        self.nombre_feuille_garder = polyhash.nombre_ballons
        self.alittude = polyhash.altitudes
        self.carteIDBalises = deepcopy(polyhash.carteIDBalises)
        self.carteIDBalises_originale = deepcopy(polyhash.carteIDBalises)
        self.balises_couvertes = {}  # Suivi des balises couvertes par tour

    def construire_arbre(self):
        feuilles = [self.racine]
        self.balises_couvertes = {0: set()}  # Initialisation pour le tour 0

        for i in range(self.profendeur):
            nouvelles_feuilles = []
            self.balises_couvertes[i + 1] = set()  # Préparer l'ensemble des balises couvertes pour le tour suivant

            for noeud in feuilles:
                actions_possibles = [0]  # Peut rester
                if noeud.alittude > 0:
                    actions_possibles.append(-1)  # Peut descendre
                if noeud.alittude < self.alittude - 1:
                    actions_possibles.append(1)  # Peut monter

                for action in actions_possibles:
                    nouvel_alittude = noeud.alittude + action
                    nouvel_cord = noeud.cord + self.polyhash.carte_vent.vents[nouvel_alittude][noeud.cord.y][noeud.cord.x]

                    if nouvel_cord.y < self.polyhash.lignes:
                        nouvel_cord.x %= self.polyhash.colonnes
                        nouvel_score = noeud.score + len(self.carteIDBalises[nouvel_cord.y][nouvel_cord.x])

                        nouvel_enfant = Noeud(
                            cord=nouvel_cord,
                            action=action,
                            score=nouvel_score,
                            alittude=nouvel_alittude,
                            racine=noeud,
                            profondeur=noeud.profondeur + 1,
                        )

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

    def mettre_à_jour(self, noeud: Noeud, profondeur: int):
        feuilles = []

        def parcours(noeud_p: Noeud):
            if noeud_p.profondeur == profondeur:
                balises = [balise for balise in self.carteIDBalises[noeud_p.cord.y][noeud_p.cord.x] if balise not in self.balises_couvertes[profondeur]]
                noeud_p.score = noeud_p.racine.score + len(balises)
            elif noeud_p.profondeur > profondeur:
                noeud_p.score = noeud_p.racine.score + len(self.carteIDBalises[noeud_p.cord.y][noeud_p.cord.x])

            if noeud_p.enfant_decendre:
                parcours(noeud_p.enfant_decendre)
            if noeud_p.enfant_reste:
                parcours(noeud_p.enfant_reste)
            if noeud_p.enfant_monte:
                parcours(noeud_p.enfant_monte)

            if (
                not noeud_p.enfant_decendre
                and not noeud_p.enfant_reste
                and not noeud_p.enfant_monte
            ):
                feuilles.append(noeud_p)

        parcours(self.racine)

        feuilles.sort(key=lambda n: n.score, reverse=True)
        return feuilles[:self.nombre_feuille_garder]

    def chemin(self):
        feuilles = self.construire_arbre()
        resultat = []
        for i in range(self.nombre_feuille_garder):
            actions = []
            copie_feuille: Noeud = deepcopy(feuilles[i])

            while copie_feuille.racine is not None:
                actions.insert(0, copie_feuille.action)
                feuilles = self.mettre_à_jour(copie_feuille, copie_feuille.profondeur)
                copie_feuille = deepcopy(copie_feuille.racine)

            resultat.append(actions)
            print("chemin :", i, ':', actions)
        return resultat
