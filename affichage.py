import sys
import os
from DAOFichier import DAOFichier
from Jeu import Jeu
from Strategies.StrategieAleatoire import StrategieAleatoire
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

    mem_proche = []
    mem_alea =[]
    mem_a=[]

    for i in range(len(fichiers)):
        # Demarage de la surveillance mémoire
        tracemalloc.start()
        gc.collect()

        # Demarage de la surveillance du temps
        start = time.time()

        DAO = DAOFichier
        polyhash: Polyhash = DAO.donne_polyhash(fichiers[i])
        jeu = Jeu(polyhash)

        # Strategie proche
        max_game_proche = (0,[])
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

        # Strategie A*
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


    # Combiner les données en un seul tableau
    donnees_combinees = [
        ["Proche", "a_example", scores_proche[0], temps_proche[0], mem_proche[0]],
        ["Proche", "b_small", scores_proche[1], temps_proche[1], mem_proche[1]],
        ["Proche", "c_medium", scores_proche[2], temps_proche[2], mem_proche[2]],
        ["Proche", "d_final", scores_proche[3], temps_proche[3], mem_proche[3]],
        ["Aléatoire", "a_example", scores_aleatoire[0], temps_aleatoire[0], mem_alea[0]],
        ["Aléatoire", "b_small", scores_aleatoire[1], temps_aleatoire[1], mem_alea[1]],
        ["Aléatoire", "c_medium", scores_aleatoire[2], temps_aleatoire[2], mem_alea[2]],
        ["Aléatoire", "d_final", scores_aleatoire[3], temps_aleatoire[3], mem_alea[3]]
    ]

    # Créer le tableau combiné
    table_combinee = tabulate(
        donnees_combinees,
        headers=["Stratégies", "Scénario", "Scores (points)", "Temps (s)", "Mémoire (MB)"],
        tablefmt="grid"
    )

    # Afficher le tableau combiné
    print(table_combinee)

    tracemalloc.stop()