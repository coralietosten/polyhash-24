from math import sqrt
from math import inf
from Polyhash import *
from Ballon import *
from CarteIDBalises import *


class GusStrategie:
    def __init__(self):
        self.polyhash = None
        self.probabiliste = False
        self.dicobjectif = {}
        self.listobjectif = []
    def initialisation(self,polyhash : Polyhash):
        self.polyhash = polyhash
        self.dicobjectif = self.calcul_dicobjectifs()
        self.listobjectif = self.dico_to_list(self.dicobjectif)

    def donne_action(self, ballon, polyhash: Polyhash) -> int:
        """entrée : un ballon et les données du polyhash
           sortie : l'action à effectuer pour un tour pour un ballon"""
        pass

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

    def distance(self,co1 : Vecteur2,co2 : Vecteur2): #caclul de l'heuristique (distance a vol d'oiseau) entre un ballon et son objectif
        if co1 == Vecteur3(-1,-1,-1) :
            return inf
        return sqrt((co1.x-co2.x)**2 + (co1.y-co2.y)**2)

    def nextpos(self,coord : Vecteur3):# co : (x,y,z) map : [z][y][x]
        """
        renvoit la prochaine position dans la carte, en prenant en argument une coordonnée et la carte vent,
        si la position sort de la carte vers le haut ou vers le bas, renvoit Vecteur3(-1,-1,-1)
        """
        cartevent = self.polyhash.carte_vent
        if coord == Vecteur3(-1,-1,-1) :
            return Vecteur3(-1,-1,-1)
        longueur = len(cartevent.vents[0])
        largeur = len(cartevent.vents[0][0])
        vent = cartevent.vents[coord.z][coord.x][coord.y]
        newpos = Vecteur3((coord.x + vent.x)%longueur,(coord.y + vent.y),coord.z)
        if newpos.y >= 0 and newpos.y < largeur : #si la position est toujours dans la carte on la renvoit
            return newpos
        else : #sinon on renvoit -1,-1,-1 qui renvoit infinie dans la fonction distance
            return Vecteur3(-1,-1,-1)

    def prochainpoint(self,ballon : Ballon , goal : Vecteur2, prof : int, proba : bool) -> int:
        """
        calcul la prochaine en fonction des coordonnées du drone (co), de son objectif (goal) de la carte (map),
        de la profondeur(prof) et de l'utilisation ou non de système probabiliste(proba)
        """
        cartevent = self.polyhash.carte_vent
        hauteur = len(cartevent.vents)
        def aux(co2 : Vecteur3,prof2 : int):
            if prof2 == 0 :
                return self.distance(Vecteur2(co2.x,co2.y),goal) #si la profondeur est nulle on renvoit l'heuristique (distance a vol d'oiseau)
            l = [aux(self.nextpos(co2 + Vecteur3(0,0,0)),prof2-1)]
            if co2.z < hauteur : #on vérifie si on peut aller au nord sans sortir de la map, si c'est le cas on calcul cette possibilité)
                l.append(aux(self.nextpos(co2 + Vecteur3(0,0,1)),prof2-1))
            if co2.z > 0 :
                l.append(aux(self.nextpos(co2 + Vecteur3(0,0,-1)),prof2-1))
            if proba :
                return #à coder, renvoit la prochaine coordonnée de manière probabiliste (plus l'heuristique est petite, plus elle a de chance d'être choisie)
            else :
                return min(l) #renvoit la prochaine coordonnée
        positions = {aux(ballon.coord,prof) : 0,}
        if ballon.coord.z > 0 :
            positions[aux(ballon.coord + Vecteur3(0,0,-1),prof)] = -1
        if ballon.coord.z < hauteur :
            positions[aux(ballon.coord + Vecteur3(0,0,1),prof)] = 1
        return positions[min(positions.keys())] #on renvoit l'action associée a la distance minimale

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
            bcentre = self.baricentre(balisesadjacentes)
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
