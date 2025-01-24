import os , sys
from os.path import dirname, join, abspath
sys.path.insert(0,abspath(join(dirname(__file__),'..')))

from random import randint
from math import sqrt
from Polyhash import Polyhash
from Balise import Balise
from Ballon import Ballon
from Vecteur3 import Vecteur3
from Vecteur2 import Vecteur2

from StrategieInterface import StrategieInterface

class StrategieProcheGus(StrategieInterface):
    def __init__(self):
        self.polyhassh = None
        self.objectifs = []
        self.ballons = []
    def initialisation(self,polyhash : Polyhash):
        self.polyhash = polyhash
        self.ballons = []
        self.dicobjectif = self.calcul_dicobjectifs()
        self.objectifs = self.dico_to_list(self.dicobjectif)

    
    def dico_to_list(self,dicobjectif) -> list[(int,Vecteur2)]:
        """
        prend le dictionnaire des objectifs (balise : score, coord) et renvoit une liste contenant des couples [(score,Vecteur2)] (score et coordonnée des points importants)
        triés par ordres croissants (on vise d'abord les points avec beaucoup de valeur)
        """
        listobjectif = []
        def aux(dico):
            maxi = -1
            keymax = -1
            for key in dico.keys():
                if dico[key][0] > maxi :
                    maxi = dico[key][0]
                    keymax = key
            return keymax
        while len(dicobjectif) != 0 :
            b = aux(dicobjectif)
            listobjectif.append((dicobjectif[b][0],dicobjectif[b][1]))
        return listobjectif
    
    def calcul_dicobjectifs(self):
        """
        prend en argument la liste des balises et renvoit une liste des scores contenant une liste de coordonnée avec le score associé, trié par ordre d'importance
        """
        lbalises = self.polyhash.cibles
        dcouverture = self.polyhash.rayon_couverture
        carteidbalises = self.polyhash.carteIDBalises
        dicobjectif = {} #listescore[IDbalise] = (score associé a la balise,balises adjacentes)
        for b1 in lbalises :
            balisesadjacentes = []
            for b2 in lbalises :
                if b1.id != b2.id and self.distance(b1.coord,b2.coord) < (dcouverture * 2) - 1 :
                    balisesadjacentes.append(b2)
            bcentre = self.baricentre(balisesadjacentes + [b1])
            score = len(carteidbalises[bcentre.x][bcentre.y])
            dicobjectif[b1] = (score,bcentre,balisesadjacentes)
        for b in dicobjectif.keys():
            #pour toute les balises adjacente a la balise b
            for badj in dicobjectif[b][2] :
                #si une des balises adjacentes contient un score superieur a la balise b
                if dicobjectif[badj][0] > dicobjectif[b][0] :
                    #supprimer la balise b du dicobjectif
                    del dicobjectif[b]
        return dicobjectif
    #O(nbBalise^2)

    def baricentre(self,balises) :
        xsum = 0
        ysum = 0
        n = len(balises)
        for b in balises :
            xsum += b.coord.x
            ysum += b.coord.y
        centre = Vecteur2(xsum/n,ysum/n)
        return centre
    
    def distance (self,vecteur1 : Vecteur3 , vecteur2 : Vecteur2):
        """
        renvoie la distance entre le vecteur1 et le vecteur2
        """
        return sqrt((vecteur1.x - vecteur2.x)**2 + (vecteur1.y - vecteur2.y)**2) 

    def distance_v2 (self,vecteur1 : Vecteur2, vecteur2 : Vecteur2):
        """
        renvoie la distance entre le vecteur1 et le vecteur2
        """
        return sqrt((vecteur1.x - vecteur2.x)**2 + (vecteur1.y - vecteur2.y)**2)

    def balise_proche(self):
        """
        renvoie la balise la plus proche du ballon
        """
        coord_depart = self.polyhash.depart
        bal_proche = Balise(Vecteur2(0,0))
        dist_min = self.polyhash.colonnes * self.polyhash.lignes
        for b in self.polyhash.cibles:
            if self.distance (coord_depart , b.coord) < dist_min :
                dist_min = self.distance (coord_depart , b.coord)
                bal_proche = b
        return bal_proche

    
    def donne_action(self, ballon) -> int:
        """entrée : un ballon et les données du polyhash
           sortie : l'action à effectuer pour un tour pour un ballon"""
        if ballon.id not in self.ballons :
            self.ballons.append(ballon)
        #calcul des altitudes disponibles
        coord_ballon = ballon.coord
        altitudes_disponibles = []
        if coord_ballon.z > 0 and coord_ballon.z < self.polyhash.altitudes -1:
            altitudes_disponibles.append(1)
            altitudes_disponibles.append(-1)
            altitudes_disponibles.append(0)
        elif coord_ballon.z <= 0 :
            altitudes_disponibles.append(1)
        elif coord_ballon.z == self.polyhash.altitudes -1:
            altitudes_disponibles.append(-1)
            altitudes_disponibles.append(0)
        #récuperation des vents
        carte_vent = self.polyhash.carte_vent
        #determination des coordonnées les plus pres de la cible objectif du ballon
        dist_min = self.polyhash.lignes * self.polyhash.colonnes
        altitude_a_prendre = 0
        for i in altitudes_disponibles :
            coord_v2_ballon = Vecteur2(coord_ballon.x, coord_ballon.y)
            coord_arrivee = coord_v2_ballon + carte_vent[coord_ballon.z + i][coord_ballon.y][coord_ballon.x]
            if coord_arrivee.x < self.polyhash.colonnes and coord_arrivee.x > 0 and coord_arrivee.y < self.polyhash.lignes and coord_arrivee.y > 0 :#si le ballon est dans la map
                dist = self.distance_v2(self.objectifs[ballon.id].coord, coord_arrivee)
                if dist < dist_min :
                    dist_min = dist 
                    altitude_a_prendre = i 
        return altitude_a_prendre


        

