from math import sqrt
from math import inf
from Polyhash import *
from Ballon import *
from CarteIDBalises import *

def distance(co1 : Vecteur2,co2 : Vecteur2): #caclul de l'heuristique (distance a vol d'oiseau) entre un ballon et son objectif
    if co1 == Vecteur3(-1,-1,-1) :
        return inf
    return sqrt((co1.x-co2.x)**2 + (co1.y-co2.y)**2)

def nextpos(coord : Vecteur3, cartevent : CarteVent):# co : (x,y,z) map : [z][y][x]
    """
    renvoit la prochaine position dans la carte, en prenant en argument une coordonnée et la carte vent,
    si la position sort de la carte vers le haut ou vers le bas, renvoit Vecteur3(-1,-1,-1)
    """
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

def prochainpoint(ballon : Ballon , goal : Vecteur2 , cartevent : CarteVent, prof : int, proba : bool) -> int:
    """
    calcul la prochaine en fonction des coordonnées du drone (co), de son objectif (goal) de la carte (map),
    de la profondeur(prof) et de l'utilisation ou non de système probabiliste(proba)
    """
    hauteur = len(cartevent.vents)
    def aux(co2 : Vecteur3,prof2 : int):
        if prof2 == 0 :
            return distance(Vecteur2(co2.x,co2.y),goal) #si la profondeur est nulle on renvoit l'heuristique (distance a vol d'oiseau)
        l = [aux(nextpos(co2 + Vecteur3(0,0,0),cartevent),prof2-1)]
        if co2.z < hauteur : #on vérifie si on peut aller au nord sans sortir de la map, si c'est le cas on calcul cette possibilité)
            l.append(aux(nextpos(co2 + Vecteur3(0,0,1),cartevent),prof2-1))
        if co2.z > 0 :
            l.append(aux(nextpos(co2 + Vecteur3(0,0,-1),cartevent),prof2-1))
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

def listeobjectifs(lbalises,dcouverture : int,carteidbalises : CarteIDBalises):
    """
    prend en argument la liste des balises et renvoit une liste des scores contenant une liste de coordonnée avec le score associé, trié par ordre d'importance
    """
    listescore = {} #listescore[IDbalise] = (score associé a la balise,balises adjacentes)
    for b1 in lbalises :
        balisesadjacentes = []
        for b2 in lbalises :
            if b1.id != b2.id and distance(b1.coord,b2.coord) < (dcouverture * 2) - 1 :
                balisesadjacentes.append(b2)
        bcentre = baricentre(balisesadjacentes)
        score = carteidbalises.cartesBalises[bcentre.x][bcentre.y]
        listescore[b1] = (bcentre,score,balisesadjacentes)
    for b in listescore.keys():
        #pour toute les balises adjacente a la balise b
        for badj in listescore[b][2] :
            #si une des balises adjacentes contient un score superieur a la balise b
            if listescore[badj][0] > listescore[b][0] :
                #supprimer la balise b de la liste des scores
                del listescore[b]
    return listescore
#O(nbBalise^2)

def baricentre(lbalises) :
    xsum = 0
    ysum = 0
    n = len(lbalises)
    for b in lbalises :
        xsum += b.coord.x
        ysum += b.coord.y
    centre = Vecteur2(xsum/n,ysum/n)
    return centre


class GusStrategie:
    def initialisation(self):
        pass

    def donne_action(self, ballon, polyhash: Polyhash) -> int:
        """entrée : un ballon et les données du polyhash
           sortie : l'action à effectuer pour un tour pour un ballon"""
        pass

