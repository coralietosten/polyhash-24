import os
from DAOFichier import DAOFichier
from Jeu import Jeu
from Strategies.StrategieAleatoire import StrategieAleatoire
from Polyhash import Polyhash

import pickle

data_choix = 0
files = ["a_example","b_small","c_medium","d_final"]

def enregistrer_solution(game):
    global files
    global data_choix
    with open('SolutionsAleatoire/'+files[data_choix], 'wb') as f:
            pickle.dump(game, f)
if __name__ == "__main__":
    DAO = DAOFichier
    polyhash: Polyhash = DAO.donne_polyhash("data/"+files[data_choix]+".in")
    jeu = Jeu(polyhash)
    #Utilisation la Stratégie Aléatoire

    file_path = 'SolutionsAleatoire/'+files[data_choix]
    if os.path.exists(file_path):
        with open('SolutionsAleatoire/'+files[data_choix], 'rb') as f:
            max_game = pickle.load(f)
        print("Jeu : ",max_game)
    else:
        max_game = (0,[])
    for i in range(1000):
        jeu.lancement_jeu(StrategieAleatoire())
        if jeu.score > max_game[0]:
            max_game = (jeu.score,jeu.actions)
    enregistrer_solution(max_game)
    while True:
        jeu.lancement_jeu(StrategieAleatoire())
        if jeu.score > max_game[0]:
            max_game = (jeu.score,jeu.actions)
            enregistrer_solution(max_game)






    