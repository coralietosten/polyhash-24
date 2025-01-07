import sys
import os
from DAOFichier import DAOFichier
from Jeu import Jeu
from Strategies.StrategieAleatoire import StrategieAleatoire
from Strategies.GusStrategie import GusStrategie
from Strategies.StrategieProche import StrategieProche
from Polyhash import Polyhash
import pickle

fichiers =["data/a_example.in","data/b_small.in","data/c_medium.in","data/d_final.in"]
nom_fichier = ["a_example","b_small","c_medium","d_final"]

if __name__ == "__main__":

    scores_proche=[]
    scores_aleatoire=[]
    for i in range(len(fichiers)):
        DAO = DAOFichier
        polyhash: Polyhash = DAO.donne_polyhash(fichiers[i])
        jeu = Jeu(polyhash)

        #strategie proche
        max_game = (0,[])
        jeu.lancement_jeu(StrategieProche())
        max_game_proche = (jeu.score,jeu.actions)
        scores_proche.append(max_game_proche[0])
    
        #strategie Aléatoire
        file_path = 'SauvegardeAleatoire/'+nom_fichier[i]
        if os.path.exists(file_path):
            with open('SauvegardeAleatoire/'+nom_fichier[i], 'rb') as f:
                max_game_alea = pickle.load(f)
            scores_aleatoire.append(max_game_alea[0])

    print(f'Proche : {scores_proche}')
    print(f'Aléatoire : {scores_aleatoire}')
    
