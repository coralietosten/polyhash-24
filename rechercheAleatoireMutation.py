import os
from DAOFichier import DAOFichier
from Jeu import Jeu
from Strategies.StrategieAleatoireMutation import StrategieAleatoireMutation
from Polyhash import Polyhash
# import simpleaudio as sa
import pickle
import time
# define an object to play
# wave_object = sa.WaveObject.from_wave_file('son2.wav')



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
        time.sleep(2)
    else:
        max_game = (0,[])

    enregistrer_solution(max_game)
    strat = StrategieAleatoireMutation(max_game[1])
    if data_choix == 0:
        strat.newgame_p = 0
        strat.nbMaxNewChemin =  0
        strat.nbMaxMutations = 10 
        strat.mutation_chemin_p = 0.0001 
    elif data_choix == 1:
        strat.newgame_p = 0
        strat.nbMaxNewChemin =  0
        strat.nbMaxMutations = 10 
        strat.mutation_chemin_p = 0.0001 
    elif data_choix == 2:
        strat.newgame_p = 0
        strat.nbMaxNewChemin =  0
        strat.nbMaxMutations = 2
        strat.mutation_chemin_p = 0.1 
    elif data_choix == 3:
        strat.newgame_p = 0
        strat.nbMaxNewChemin =  0
        strat.nbMaxMutations = 10 
        strat.mutation_chemin_p = 0.0001 

    import multiprocessing
    import threading

    max_game_value = multiprocessing.Value('d', max_game[0]) 
    max_game_actions = multiprocessing.Manager().list(max_game[1])

    lock = threading.Lock()

    def travail(task_id):
        global max_game_value, max_game_actions
        while True:
            try:
                strat.max_game = list(max_game_actions)
                jeu.lancement_jeu(strat)

                if jeu.score > max_game_value.value:
                    with lock:
                        if jeu.score > max_game_value.value:
                            max_game_value.value = jeu.score
                            max_game_actions[:] = jeu.actions 
                            enregistrer_solution((max_game_value.value, list(max_game_actions)))
                            print(f"Une meilleure solution a été trouvée par le cœur {task_id} : {jeu.score}")

            except Exception as e:
                print(f"Une erreur est survenue dans le cœur {task_id} : {str(e)}")
                break

    num_cores = multiprocessing.cpu_count() - 0
    print(f"Lancement avec {num_cores} cœurs")

    with multiprocessing.Pool(num_cores) as pool:
        pool.map(travail, range(num_cores))