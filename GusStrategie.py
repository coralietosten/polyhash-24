from maths import sqrt
def fichier():
    return

Class ballon:
    def __init__ (self,co = (0,0),h = 0,goal = (0,0)):
        self.co : (int,int)
        self.h



def h(co1,co2): #caclul de l'heuristique (distance a vol d'oiseau) entre un ballon et son objectif
    return sqrt((co1[0]-co2[0])**2 + (co1[1]-co2[1])**2)


def nextpos(co,map): #co : (x,y,z) map : [z][y][x]
    vent = map[co[2]][co[1]][co[0]] #récupération du vecteur vent sur la case donnée
    return (co[0] + vent[0],co[1] + vent[1],co[2]) #ajout du vecteur vent aux coordonnées de base

def prochainpoint(co,goal,map,prof,proba): #calcul le prochain point a prendre en fonction des coordonnées du drone (co), de son objectif (goal) de la carte (map), de la profondeur(prof) et de l'utilisation ou non de système probabiliste(proba)
    def aux(co2,prof2,movement):
        if prof2 == 0 :
            return h(co2,goal)
        haut = nextpos(co2 + (0,0,1))
        rien = nextpos(co2 + (0,0,0))
        bas  = nextpos(co2 + (0,0,-1))
        if proba :
            return #à coder, renvoit la prochaine coordonnée de manière probabiliste (plus l'heuristique est petite, plus elle a de chance d'être choisie)
        else :
            return min(aux(haut,prof2-1),aux(rien,prof2-1),aux(bas,prof2-1)) #renvoit la prochaine coordonnée



def calculmapbalise(distance,lbalise,l,L):
    """
    prend en argument la distance de couverture, la liste des balises a couvrir, la longueur l et la largeur L de la carte et
    renvoit une carte avec dans chaque case la liste des ID de balise qui sont affectés par la zone de couverture du ballon
    """
    tab = [[[] for i in range(l)] for j in range(L)]
    lcercle = cercle(distance)
    for balise in lbalisee :
        for coord in lcercle :
            if inbounds(balise.x + coord.x, balise.y + coord.y):
                tab[balise.y + coord.y][balise.x + coord.x].append(balise.id)
    return tab




def calculmapgoal(mapbalise,l,L):
    """
    prend en argument la carte des ID de balise et avec, fait une carte de score avec le nombre dans la case correspondant au nombre de balise
    affectée par la zone
    """
    return tab = [[len(mapbalise[j][i]) for i in range(l)] for j in range(L)]
    


def cercle(distance : int) -> List[vecteur2]:




[
    [
        [(1,2),(1,2),(1,2),(1,2),(1,2),(1,2)],
        [(1,2),(1,2),(1,2),(1,2),(1,2),(1,2)],
        [(1,2),(1,2),(1,2),(1,2),(1,2),(1,2)]
    ],
    [
        [(1,2),(1,2),(1,2),(1,2),(1,2),(1,2)],
        [(1,2),(1,2),(1,2),(1,2),(1,2),(1,2)],
        [(1,2),(1,2),(1,2),(1,2),(1,2),(1,2)]
    ],
    [
        [(1,2),(1,2),(1,2),(1,2),(1,2),(1,2)],
        [(1,2),(1,2),(1,2),(1,2),(1,2),(1,2)],
        [(1,2),(1,2),(1,2),(1,2),(1,2),(1,2)]
    ]
]

[
    [[ ],[1],[ ],[ ],[ ],[3],[3],[3]],
    [[1],[1],[1],[ ],[ ],[ ],[2,3],[ ]],
    [[ ],[1],[ ],[ ],[ ],[2],[2],[2]],
    [[ ],[ ],[ ],[ ],[ ],[ ],[2],[ ]],
]






def heuristique():



#la grille a droite se relie a gauche






#Classes :
#vecteur2 : x : int, y : int

#vecteur3 : x : int, y : int, z : int

#ballons-drone : position : vecteur3, goal : vecteur2

#CarteVent : List.List.List[vecteur2]

#CarteGoal : List.List.List[int] <- id balises

#DAO file : nbballons : int, nb balise : int ...................

