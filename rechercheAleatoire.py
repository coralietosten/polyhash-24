import os
from DAOFichier import DAOFichier
from Jeu import Jeu
from Strategies.StrategieAleatoire import StrategieAleatoire
from Polyhash import Polyhash

import pickle

data_choix = 3
files = ["a_example","b_small","c_medium","d_final"]

def enregistrer_solution(game):
    global files
    global data_choix
    with open('SauvegardeAleatoire/'+files[data_choix], 'wb') as f:
            pickle.dump(game, f)
if __name__ == "__main__":
    DAO = DAOFichier
    polyhash: Polyhash = DAO.donne_polyhash("data/"+files[data_choix]+".in")
    jeu = Jeu(polyhash)
    #Utilisation la Stratégie Aléatoire

    file_path = 'SauvegardeAleatoire/'+files[data_choix]
    if os.path.exists(file_path):
        with open('SauvegardeAleatoire/'+files[data_choix], 'rb') as f:
            max_game = pickle.load(f)
            DAOFichier.cree_fichier(max_game[1],"PropositionSolution/StrategieAleatoire/sortie_"+files[data_choix]+".txt")

        print("Jeu : ",max_game[0])
    else:
        max_game = (0,[])
    for i in range(10):
        jeu.lancement_jeu(StrategieAleatoire())
        if jeu.score > max_game[0]:
            max_game = (jeu.score,jeu.actions)
    enregistrer_solution(max_game)
    print("Save !")
    while True:
        jeu.lancement_jeu(StrategieAleatoire())
        if jeu.score > max_game[0]:
            max_game = (jeu.score,jeu.actions)
            enregistrer_solution(max_game)
            print("Une meilleure solution a été trouvé !")







    