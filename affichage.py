import sys
import os
from DAOFichier import DAOFichier
from Jeu import Jeu
from Strategies.StrategieAleatoire import StrategieAleatoire
from Strategies.GusStrategie import GusStrategie
from Strategies.StrategieProche import StrategieProche
from Strategies.Strategie import Strategie
from Polyhash import Polyhash
import pickle
import time
from tabulate import tabulate
from pympler import asizeof
import tracemalloc
import gc

fichiers =["data/a_example.in","data/b_small.in","data/c_medium.in","data/d_final.in"]
nom_fichier = ["a_example","b_small","c_medium","d_final"]

if __name__ == "__main__":

    scores_proche=[]
    scores_aleatoire=[]
    scores_a =[]
    temps_proche = []
    temps_aleatoire =[]
    temps_a=[]
    for i in range(len(fichiers)):
        #demarage de la surveillance mémoire
        tracemalloc.start()
        gc.collect()

        #demarage de la surveillance du temps
        start = time.time()

        DAO = DAOFichier
        polyhash: Polyhash = DAO.donne_polyhash(fichiers[i])
        jeu = Jeu(polyhash)

        #strategie proche
        max_game_proche = (0,[])
        mem_proche = []
        mem_avant_proche = tracemalloc.get_tracemalloc_memory ( )
        jeu.lancement_jeu(StrategieProche())
        max_game_proche = (jeu.score,jeu.actions)
        scores_proche.append(max_game_proche[0])
        temps_proche.append(time.time() - start)
        taille_proche = asizeof.asizeof(StrategieProche())
        mem_apres_proche = tracemalloc.get_tracemalloc_memory ( )
        stat_proche = mem_apres_proche - mem_avant_proche
        mem_proche.append(stat_proche)
        print(mem_proche)

        # from pympler import classtracker
        # tr = classtracker.ClassTracker()
        # tr.track_class(StrategieProche)
        # tr.create_snapshot()
        # tr.create_snapshot()
        # tr.stats.print_summary()


        #strategie Aléatoire
        mem_alea =[]
        mem_avant_alea = tracemalloc.get_tracemalloc_memory ( )
        file_path = 'SauvegardeAleatoire/'+nom_fichier[i]
        if os.path.exists(file_path):
            with open('SauvegardeAleatoire/'+nom_fichier[i], 'rb') as f:
                max_game_alea = pickle.load(f)
            scores_aleatoire.append(max_game_alea[0])
        temps_aleatoire.append(time.time() - start)
        taille_aleatoire = asizeof.asizeof(StrategieAleatoire())
        mem_apres_alea = tracemalloc.get_tracemalloc_memory ( )
        stat_alea = mem_apres_alea - mem_avant_alea
        mem_alea.append(stat_alea)

        
        #strategie A*
        # mem_a =[]
        # mem_avant_a = tracemalloc.get_tracemalloc_memory ( )
        # max_game_a = (0,[])
        # jeu.lancement_jeu(Strategie())
        # max_game_a = (jeu.score,jeu.actions)
        # scores_a.append(max_game_a[0])
        # temps_a.append(time.time() - start)
        # mem_apres_a = tracemalloc.get_tracemalloc_memory ( )
        # stat_a = mem_apres_a - mem_avant_a
        # mem_a.append(stat_a)


    donnees_scores = [
        ["Proche", scores_proche[0], scores_proche[1], scores_proche[2], scores_proche[3]],
        ["Aléatoire",  scores_aleatoire[0],  scores_aleatoire[1], scores_aleatoire[2], scores_aleatoire[3]]]
        #["A*", scores_a[0], scores_a[1], scores_a[2], scores_a[3]]]

    donnees_temps =[
        ["Proche",temps_proche[0],temps_proche[1],temps_proche[2],temps_proche[3]],
        ["Aléatoire",temps_aleatoire[0],temps_aleatoire[1],temps_aleatoire[2],temps_aleatoire[3]]]
        #["A*",temps_a[0],temps_a[1],temps_a[2],temps_a[3]]]

    table_scores = tabulate(
        donnees_scores, 
        headers=["Stratégies", "a_example", "b_small","c_medium","d_final"], 
        tablefmt="grid"
    )

    table_temps = tabulate(
        donnees_temps, 
        headers=["Stratégies", "a_example", "b_small","c_medium","d_final"], 
        tablefmt="grid"
    )

    print(table_scores)
    print(table_temps)
    print(mem_proche)
    print(mem_alea)
    tracemalloc.stop()
    # for s in stat[:2]:
    #     print(s)
    # print(f'{taille_proche} octets')
    # print(f'{taille_aleatoire} octets')


    # print(f'Proche : Score : {scores_proche} Temps : {temps_proche}')
    # print(f'Aléatoire : Score : {scores_aleatoire} Temps : {temps_aleatoire}')
    # print(f'A* : Score: {scores_a} Temps : {temps_a}')
    

