from __future__ import annotations
import sys
from os.path import dirname, join, abspath
from Vecteur2 import Vecteur2
sys.path.insert(0,abspath(join(dirname(__file__),'..')))
from Polyhash import Polyhash
from Ballon import Ballon
from StrategieInterface import StrategieInterface
from copy import deepcopy

class StrategieArbre(StrategieInterface):
    """
    Stratégie basée sur un arbre de décision pour déterminer les actions des ballons.

    Attributs :
    - polyhash (Polyhash): L'objet Polyhash contenant les informations du jeu.
    - chemins (List[List[int]]): Liste des chemins pour chaque ballon.

    Méthodes :
    - initialisation(self, polyhash: Polyhash): Initialise la stratégie avec l'objet Polyhash.
    - donne_action(self, ballon: Ballon) -> int: Donne l'action suivante pour un ballon.
    """
    def __init__(self):
        self.polyhash = None
        self.chemins = None 
    
    def initialisation(self, polyhash : Polyhash):
        """
        Initialise la stratégie avec l'objet Polyhash.

        Args:
            polyhash (Polyhash): L'objet Polyhash contenant les informations du jeu.
        """
        self.polyhash = polyhash

        cord = self.polyhash.depart
        racine = Noeud(cord = cord, action= 1, score = 0, alittude= -1, profondeur=0)
        
        arbre = Arbre(racine, self.polyhash)
        self.chemins = arbre.chemin()
        for i in range(len(self.chemins)) :
            self.chemins[i].reverse()


    def donne_action(self, ballon: Ballon) -> int:
        """
        Donne l'action suivante pour un ballon.

        Args:
            ballon (Ballon): Le ballon pour lequel l'action est demandée.

        Returns:
            int: L'action suivante pour le ballon.
        """
        return self.chemins[ballon.id].pop()






class Noeud :
    """
    Classe représentant un noeud dans l'arbre de décision.

    Attributs :
    - racine (Noeud): Le noeud parent.
    - cord (Vecteur2): Les coordonnées du noeud.
    - action (int): L'action associée au noeud.
    - score (int): Le score du noeud.
    - alittude (int): L'altitude du noeud.
    - enfant_decendre (Noeud): L'enfant du noeud pour l'action "descendre".
    - enfant_reste (Noeud): L'enfant du noeud pour l'action "rester".
    - enfant_monte (Noeud): L'enfant du noeud pour l'action "monter".
    - profondeur (int): La profondeur du noeud dans l'arbre.
    """
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
    """
    Classe représentant un arbre de décision pour les ballons.

    Attributs :
    - racine (Noeud): Le noeud racine de l'arbre.
    - profendeur (int): La profondeur de l'arbre.
    - polyhash (Polyhash): L'objet Polyhash contenant les informations du jeu.
    - nombre_feuille_garder (int): Le nombre de feuilles à garder.
    - alittude (int): Le nombre d'altitudes.
    - carteIDBalises (List[List[List[int]]]): Une copie de la carte des IDs des balises.
    - carteIDBalises_originale (List[List[List[int]]]): Une copie originale de la carte des IDs des balises.
    - balises_couvertes (Dict[int, Set[int]]): Suivi des balises couvertes par tour.

    Méthodes :
    - __init__(self, racine: Noeud, polyhash: Polyhash): Initialise l'arbre.
    - construire_arbre(self): Construit l'arbre de décision.
    - chemin(self) -> List[List[int]]: Retourne les chemins pour chaque ballon.
    - mettre_à_jour(self, noeud: Noeud): Met à jour les scores des noeuds.
    - parcours(self, noeud_p: Noeud): Parcourt l'arbre pour mettre à jour les scores.
    """
    def __init__(self, racine: Noeud, polyhash: Polyhash):
        self.racine = racine
        self.profendeur = polyhash.nombre_tours
        self.polyhash = polyhash
        self.nombre_feuille_garder = polyhash.nombre_ballons
        self.alittude = polyhash.altitudes
        self.carteIDBalises = deepcopy(polyhash.carteIDBalises)
        self.carteIDBalises_originale = deepcopy(polyhash.carteIDBalises)
        self.balises_couvertes = {}  # Suivi des balises couvertes par tour

    def construire_arbre(self):
        """
        Construit l'arbre de décision.

        Returns:
            List[Noeud]: La liste des feuilles de l'arbre.
        """
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
                    if nouvel_alittude == -1 : 
                        nouvel_cord = noeud.cord
                    else :
                        nouvel_cord = noeud.cord + self.polyhash.carte_vent.vents[nouvel_alittude][noeud.cord.y][noeud.cord.x]

                    if nouvel_cord.y < self.polyhash.lignes and nouvel_cord.y >= 0 :
                        nouvel_cord.x %= self.polyhash.colonnes
                        nouvel_score = noeud.score + len(self.carteIDBalises[nouvel_cord.y][nouvel_cord.x])
                        
                        if noeud.alittude == -1 :
                            nouvel_score = 0

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
            feuilles = nouvelles_feuilles
        return feuilles
    
    def chemin(self):
        """
        Retourne les chemins pour chaque ballon.

        Returns:
            List[List[int]]: Les chemins pour chaque ballon.
        """
        feuilles = self.construire_arbre()
        resultat = []
        for i in range(self.polyhash.nombre_ballons):
            actions = []
            copie_feuille: Noeud = feuilles[i]

            while copie_feuille.racine is not None:
                actions.insert(0, copie_feuille.action)

                if copie_feuille.profondeur not in self.balises_couvertes:
                    self.balises_couvertes[copie_feuille.profondeur] = set()

                balises_couvertes = [
                    b for b in self.carteIDBalises[copie_feuille.cord.y][copie_feuille.cord.x]
                    if b not in self.balises_couvertes[copie_feuille.profondeur]
                ]

                self.balises_couvertes[copie_feuille.profondeur].update(balises_couvertes)

                copie_feuille = copie_feuille.racine

            feuilles = self.mettre_à_jour(feuilles[i])
            resultat.append(actions)
        return resultat


    def mettre_à_jour(self, noeud: Noeud):
        """
        Met à jour les scores des noeuds.

        Args:
            noeud (Noeud): Le noeud à partir duquel mettre à jour les scores.

        Returns:
            List[Noeud]: La liste des feuilles mises à jour.
        """
        feuilles = []
        
        def parcours(noeud_p: Noeud):
            if noeud_p.racine:
                balises = [balise for balise in self.carteIDBalises[noeud_p.cord.y][noeud_p.cord.x] if balise not in self.balises_couvertes[noeud_p.profondeur]]
                noeud_p.score = noeud_p.racine.score + len(balises)

            if noeud_p.enfant_decendre:
                parcours(noeud_p.enfant_decendre)
            if noeud_p.enfant_reste:
                parcours(noeud_p.enfant_reste)
            if noeud_p.enfant_monte:
                parcours(noeud_p.enfant_monte)

            if noeud_p.profondeur == self.profendeur:
                feuilles.append(noeud_p)

        parcours(self.racine)

        feuilles.sort(key=lambda n: n.score, reverse=True)
        return feuilles