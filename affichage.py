import sys
import os
from DAOFichier import DAOFichier
from Jeu import Jeu
from Strategies.StrategieAleatoire import StrategieAleatoire
from Strategies.StrategieProche import StrategieProche
from Strategies.Strategie import Strategie
from Strategies.StrategieTripleLigne import StrategieTripleLigne
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

    scores_proche = []
    scores_aleatoire = []
    scores_a = []
    scores_triple = []

    temps_proche = []
    temps_aleatoire = []
    temps_a = []
    temps_triple = []

    mem_proche = []
    mem_alea = []
    mem_a = []
    mem_triple = []

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
        gc.collect()  # Nettoyer la mémoire avant mesure
        mem_avant_proche = tracemalloc.get_tracemalloc_memory ( )
        jeu.lancement_jeu(StrategieProche())
        max_game_proche = (jeu.score,jeu.actions)
        scores_proche.append(max_game_proche[0])
        temps_proche.append(time.time() - start)
        taille_proche = asizeof.asizeof(StrategieProche())
        mem_apres_proche = tracemalloc.get_tracemalloc_memory ( )
        stat_proche = mem_apres_proche - mem_avant_proche
        mem_proche.append(stat_proche)

        # Strategie aléatoire
        gc.collect() 
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

        # Strategie A star
        gc.collect()  
        mem_avant_a = tracemalloc.get_tracemalloc_memory ( )
        max_game_a = (0,[])
        jeu.lancement_jeu(Strategie())
        max_game_a = (jeu.score,jeu.actions)
        scores_a.append(max_game_a[0])
        temps_a.append(time.time() - start)
        mem_apres_a = tracemalloc.get_tracemalloc_memory ( )
        stat_a = mem_apres_a - mem_avant_a
        mem_a.append(stat_a)

        # Stratégie Triple Ligne
        gc.collect()
        mem_avant_triple = tracemalloc.get_tracemalloc_memory()
        jeu.lancement_jeu(StrategieTripleLigne())
        scores_triple.append(jeu.score)
        temps_triple.append(time.time() - start)
        mem_apres_triple = tracemalloc.get_tracemalloc_memory()
        mem_triple.append(mem_apres_triple - mem_avant_triple)

    
    # Combiner les données en un seul tableau
    donnees_combinees = [
        ["Proche", nom_fichier[i], scores_proche[i], temps_proche[i], mem_proche[i] / (1024 * 1024)]
        for i in range(len(fichiers))
    ] + [
        ["Aléatoire", nom_fichier[i], scores_aleatoire[i], temps_aleatoire[i], mem_alea[i] / (1024 * 1024)]
        for i in range(len(fichiers))
    ] + [
        ["A star", nom_fichier[i], scores_a[i], temps_a[i], mem_a[i] / (1024 * 1024)]
        for i in range(len(fichiers))
    ] + [
        ["Triple Ligne", nom_fichier[i], scores_triple[i], temps_triple[i], mem_triple[i] / (1024 * 1024)]
        for i in range(len(fichiers))
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