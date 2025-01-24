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

class Node:
    """A Node in a search tree."""
    def __init__(self, state, parent=None, action=None, path_cost=0):
        self.state = state
        self.parent = parent
        self.action = action
        self.path_cost = path_cost

    def __repr__(self): 
        return '<{}>'.format(self.state)
    
    def __len__(self): 
        return 0 if self.parent is None else (1 + len(self.parent))
    
    def __lt__(self, other): 
        return self.path_cost < other.path_cost
    
class PriorityQueue:
    """A queue in which the item with minimum f(item) is always popped first."""

    def __init__(self, items=(), key=lambda x: x): 
        self.key = key
        self.items = [] # a heap of (score, item) pairs
        for item in items:
            self.add(item)
         
    def add(self, item):
        """Add item to the queue."""
        pair = (self.key(item), item)
        heapq.heappush(self.items, pair)

    def pop(self):
        """Pop and return the item with min f(item) value."""
        return heapq.heappop(self.items)[1]
    
    def top(self): 
        return self.items[0][1]

    def __len__(self): 
        return len(self.items)

class Problem:
    """The abstract class for a formal problem. A new domain subclasses this,
    overriding `actions` and `results`, and perhaps other methods.
    The default action cost is 1 for all states.
    When you create an instance of a subclass, specify `initial`, and `goal` states 
    (or give an `is_goal` method) and perhaps other arguments for the subclass."""


    def __init__(self, initial: Vecteur3=None, goal: Vecteur3=None,polyhash:Polyhash=None): 
        """The constructor specifies the initial state, and possibly a goal
        state, if there is a unique goal. Your subclass's constructor can add
        other arguments."""
        self.initial = initial
        self.goal = goal
        self.polyhash = polyhash
        
    def actions(self, state: Vecteur3):     
        """Return the actions that can be executed in the given
        state. The result would typically be a list, but if there are
        many actions, consider yielding them one at a time in an
        iterator, rather than building them all at once.""" 
        actions = []  
        if state.z > 0: 
            new_state = self.result(state,-1)
            if new_state.x >=0 and new_state.y >=0 and new_state.x < self.polyhash.colonnes and new_state.y < self.polyhash.lignes : 
                actions.append(-1)
        if state.z < self.polyhash.altitudes-1: 
            new_state = self.result(state,1)
            if new_state.x >=0 and new_state.y >=0 and new_state.x < self.polyhash.colonnes and new_state.y < self.polyhash.lignes : 
                actions.append(1)
        if state.z>=0:
            new_state = self.result(state,0)
            if new_state.x >=0 and new_state.y >=0 and new_state.x < self.polyhash.colonnes and new_state.y < self.polyhash.lignes : 
                actions.append(0)
        return actions

    def result(self, state: Vecteur3, action:int): 
        """Return the state that results from executing the given
        action in the given state. The action must be one of
        self.actions(state)."""
        vent = self.polyhash.carte_vent[state.z+action][state.y][state.x]
        new_coord = Vecteur3(vent.x,vent.y,action)+state
        return new_coord
    
    def is_goal(self, state: Vecteur3):   
        """Return True if the state is a goal. The default method compares the
        state to self.goal or checks for state in self.goal if it is a
        list, as specified in the constructor."""     
        return distance(state,self.goal) ==0#<= self.polyhash.rayon_couverture+1
    
    def action_cost(self, s, a, s1): 
        """Return the cost of an action a from state s to state s1."""
        return 1
    
    def h(self, state:Vecteur3):  
        """Returns least possible cost to reach a goal for the state in given node."""             
        return distance(state,self.goal)
    
    def __str__(self):
        return '{}({!r}, {!r})'.format(
            type(self).__name__, self.initial, self.goal)
    

class Strategie(StrategieInterface):
    def __init__(self):
        self.polyhash = None
        self.map = []
        self.cibles = []
        self.tour = 0
        #2 c 4b 
    def initialisation(self,polyhash : Polyhash):
        self.polyhash = polyhash
        self.map = [[1]]*polyhash.nombre_ballons
        self.cibles = [None]*polyhash.nombre_ballons
        self.allCibles = []
        cibles = self.liste_objectifs()

        lsCibles = PriorityQueue(key=lambda x: (x[1]))
        for goal in cibles:
            score_chemin = self.eval_score_goal(Vecteur2(goal.x,goal.y))
            if score_chemin<=0 :
                continue
            lsCibles.add(((goal.x,goal.y),score_chemin))
        
        if len(lsCibles)!=0:
            cibles = []
        max = (False,0)
        while len(lsCibles)!=0:
            t = lsCibles.pop()
            if not max[0] and t[1]>10:
                max = (False,max[1]+1)
            else:
                max = (True,max[1])
            t = t[0]
            cibles.append(Vecteur2(t[0],t[1]))
        cibles.reverse()
        self.allCibles = cibles
        self.max = max[1]
        t = 0
        
        for i in range(0,polyhash.nombre_ballons):
            if i>=t*len(cibles):
                t+= 3            
            self.cibles[i] = (t,cibles[(i)%len(cibles)])

    
    def donne_action(self, ballon:Ballon) -> int:
        """entrée : un ballon et les données du polyhash
           sortie : l'action à effectuer pour un tour pour un ballon"""
        if ballon.id == 0:
            self.tour +=1

        if len(self.map[ballon.id])==0:
            n = self.a_star(ballon,self.cibles[ballon.id][1])
            if n == -2 : 
                self.map[ballon.id] = [0]
            else:
                self.map[ballon.id] = convertNodeToListActions(n)
        a=0
        if len(self.map[ballon.id])>0:
            a = self.map[ballon.id].pop(0)
        

        return a
    
    def a_star(self,ballon:Ballon,goal:Vecteur2,max_path_cost=4) :
        bgoal = Vecteur3(goal.x,goal.y,0)
        pb = Problem(ballon.coord,bgoal,self.polyhash)
        frontiere = PriorityQueue([Node(ballon.coord)],lambda x :  int(distance(x.state,bgoal)) + x.path_cost)

        ferme =  {(ballon.coord.x,ballon.coord.y,ballon.coord.z):Node(ballon.coord)}
        last = None
        while True:

            if len(frontiere) == 0:
                return Node(0)
            else:
                node = frontiere.pop()

                tupleState = (node.state.x,node.state.y,node.state.z)
                ferme[tupleState] = node
                # if pb.is_goal(node.state) :
                #     return node
                if node.path_cost >= min(max_path_cost,self.polyhash.nombre_tours):
                    return last
                else:
                    if last == None:
                        last = node
                    else:
                        if distance(last.state,bgoal)>distance(node.state,bgoal):
                            last = node
                    for action in pb.actions(node.state):
                        new_state = pb.result(node.state,action)
                        new_tupleState = (new_state.x,new_state.y,new_state.z)
                        nodeToAdd = Node(new_state,node,action,node.path_cost+1)
                        if new_tupleState not in ferme or nodeToAdd.path_cost < ferme[new_tupleState].path_cost :
                            try:
                                frontiere.add(nodeToAdd)
                            except:
                                print("ERREUR : ",frontiere.items,nodeToAdd)

    
    def eval_score_goal(self,goal:Vecteur2):
        """
        Renvoie le score du chemin optimal pour atteindre goal avec Astar"""
        ballon = Ballon(Vecteur3(self.polyhash.depart.x,self.polyhash.depart.y,-1),-5)
        score = 0
        actions = [1]
        for i in range(self.polyhash.nombre_tours):
            if not ballon.estSortie :
                if distance(ballon.coord,Vecteur3(goal.x,goal.y,ballon.coord.z))<= self.polyhash.rayon_couverture and i !=0:
                    score += 1

                if len(actions)==0:
                    n = self.a_star(ballon,goal)
                    if n == -2 : 
                        actions = [0]
                    else:
                        actions = convertNodeToListActions(n)
                a=0
                if len(actions)>0:
                    a = actions.pop(0)
                
                #Actualisation ballon 
                ballon.coord += Vecteur3(0,0,a) #modification de la coordonnée altitude
                if ballon.coord.z>=0 : #Si le ballon est lancé
                    vent = self.polyhash.carte_vent[ballon.coord.z][ballon.coord.y][ballon.coord.x]
                    ballon.coord += Vecteur3(vent.x,vent.y,0) #modification des coordonnées x et y
                    ballon.coord.x %= self.polyhash.colonnes
                    if ballon.coord.y < 0 or ballon.coord.y >= self.polyhash.lignes:
                        ballon.estSortie = True
        return score

    def liste_objectifs(self):
        """
        Retourne une liste des coordonées des centres des clusters dans un ordre décroissant du nombre 
        de balises présent dans le cluster
        Return : List<Vecteur2>
        """
        mapBalises = self.polyhash.carteIDBalises
        dicBalise = dict() # {IdBalise : (nbBaliseCLuster, CoordCluster)}
        
        for y in range(len(mapBalises)):
            listeLigneBalises = mapBalises[y]
            for x in range(len(listeLigneBalises)):
                listeBalises = listeLigneBalises[x]
                try:
                    listeBalises = self.verifyList(listeBalises,dicBalise)
                except RecursionError as err:
                    print("Erreur de récursion :", e)
                    print(listeLigneBalises[x],dicBalise)
                n = len(listeBalises)
                for e in listeBalises:
                    dicBalise[e] = (n,(x,y))
        queue = PriorityQueue(key=lambda tp : distanceV2(self.polyhash.depart,Vecteur2(tp[1][0],tp[1][1]))/tp[0])
        cluster = set()
        for tuple in dicBalise.values():
            if tuple[1] not in cluster :
                cluster.add(tuple[1])
                queue.add(tuple)
        listeObjectifs = []
        while len(queue)>0:
            clusterTuple = queue.pop()[1]
            listeObjectifs.append(Vecteur2(clusterTuple[0],clusterTuple[1]))
        return listeObjectifs
    
    def verifyList(self,ls,dico,i=0):
        """ 
        Retourne la liste actualisée avec les balises 
        étant actuellement dans leur plus grand cluster
        """
        
        while i < len(ls):
            if ls[i] in dico:
                #On vérifie si la liste actuelle est plus grande que le cluster actuel de ls[i]
                if len(ls)> dico[ls[i]][0] : 
                    i+=1
                else:
                    ls = ls[0:i] + ls[i+1:]
                    i=0
            else:
                i+=1
        return ls
    
        

    def baricentre(self, cluster) :
        xsum = 0
        ysum = 0
        n = len(cluster)
        for balise in cluster :
            xsum += balise.coord.x
            ysum += balise.coord.y
        centre = Vecteur2(int(round(xsum / n)), int(round(ysum / n)))
        return centre

    def longueur(self,v):
        return (v.x**2+v.y**2)**0.5
    
def distance(v1: Vecteur3, v2: Vecteur3):
    return sqrt((v1.x - v2.x)**2 + (v1.y - v2.y)**2 + (v1.z - v2.z)**2)

def distanceV2(v1: Vecteur2, v2: Vecteur2):
    return sqrt((v1.x - v2.x)**2 + (v1.y - v2.y)**2)

def convertNodeToListActions(node : Node) : 
    actions = []
    while node.parent != None:
        if node.action != None:
            actions.append(node.action)
        node = node.parent
    actions.reverse()
    return actions