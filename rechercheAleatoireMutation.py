import os,sys
from DAOFichier import DAOFichier
from Jeu import Jeu
from Strategies.StrategieAleatoireMutation import StrategieAleatoireMutation
from Polyhash import Polyhash
import pickle
import time



files = ["a_example","b_small","c_medium","d_final"]

def enregistrer_solution(game,sortie):
    global files
    global data_choix
    with open(sortie, 'wb') as f:
            pickle.dump(game, f)

if __name__ == "__main__":
    if len(sys.argv) - 1 > 2 or len(sys.argv) - 1  == 0 :
        print("Attention : Il manque des paramètres !")
        print("""Construction de la commande : 
                py rechercheAleatoireMutation.py chemin/fichier_entree.txt chemin/fichier_sortie.txt
               
              OU

                py rechercheAleatoireMutation.py chemin/fichier_sortie.txt
              """)
    else:
        if len(sys.argv) - 1 == 1 :
            print("Un seul parametre à été sortie, il prend en compte le chemin de sortie")
            for i,file_name in enumerate(os.listdir("data/")):
                print(f"{i} - {file_name}")
            a = input("Entrer le numéro du fichier de donnée que vous souhaitez utiliser :")
            try:
                a = int(a)
                chemin_entree = "data/"+os.listdir("data/")[a]
                data_choix = a
                 
            except:
                long = len(os.listdir("data/"))-1
                print(f"Attention, la réponse attendu est un nombre entier compris entre 0 et {long}")
            chemin_sortie = sys.argv[1]

        else:  
            chemin_entree = sys.argv[1]
            chemin_sortie = sys.argv[2]

        DAO = DAOFichier
        polyhash: Polyhash = DAO.donne_polyhash(chemin_entree)

        jeu = Jeu(polyhash)
        
        #Récupération des sauvegardes des chemins / score
        file_path = 'SauvegardeAleatoire/'+files[data_choix]
        if os.path.exists(file_path):
            with open('SauvegardeAleatoire/'+files[data_choix], 'rb') as f:
                max_game = pickle.load(f)
                DAOFichier.cree_fichier(max_game[1],chemin_sortie)

            print("Jeu : ",max_game[0])
            time.sleep(2)
        else:
            max_game = (0,[])

        enregistrer_solution(max_game,'SauvegardeAleatoire/'+files[data_choix])
        maxs = [(0,[])]*5
        maxs[0] = max_game
        
        #Utilisation la Stratégie Aléatoire Mutation
        strats = [StrategieAleatoireMutation(maxs[i][1]) for i in range(len(maxs))]
        while True:
            for i,strat in enumerate(strats):
                if data_choix == 0:
                    strat.newgame_p = 0
                    strat.nbMaxNewChemin =  0
                    strat.nbMaxMutations = 10 
                    strat.mutation_chemin_p = 0.0001 
                elif data_choix == 1:
                    strat.newgame_p = 0.01
                    strat.nbMaxNewChemin =  1
                    strat.nbMaxMutations = 1 
                    strat.mutation_chemin_p = 0.1 
                    strat.nb_max_enfant_mutation = 3 #Nombre maximum d'enfant généré par une mutation

                elif data_choix == 2:
                    strat.newgame_p = 0.001
                    strat.nbMaxNewChemin =  1
                    strat.nbMaxMutations = 3
                    strat.mutation_chemin_p = 0.01 
                    strat.nb_max_enfant_mutation = 2
                elif data_choix == 3:
                    strat.newgame_p = 0.2
                    strat.nbMaxNewChemin =  10
                    strat.nbMaxMutations = 10
                    strat.mutation_chemin_p = 0.0001 

                try:
                    strat.max_game = maxs[i][1]
                    jeu.lancement_jeu(strat)
                    
                    if jeu.score > maxs[i][0]:
                        maxs[i] = (jeu.score,jeu.actions)
                    if jeu.score > max_game[0]:
                        max_game = (jeu.score,jeu.actions)
                        print(max_game[0])
                        print(ls)
                        enregistrer_solution((jeu.score,jeu.actions),'SauvegardeAleatoire/'+files[data_choix])
                        print(f"Une meilleure solution a été trouvée : {jeu.score}")
                    if jeu.score>300_000:
                        maxs.sort(key=lambda x:x[0])
                        ls = [maxs[i][0] for i in range(len(maxs))]
                        # print(ls)
                        strats[9].mutation(maxs[i][1])
                        jeu.lancement_jeu(strat)

                        if jeu.score > maxs[i][0]:
                            print(ls)
                            maxs[i] = (jeu.score,jeu.actions)
                        if jeu.score > max_game[0]:
                            print(ls)
                            
                            max_game = (jeu.score,jeu.actions)
                            enregistrer_solution((jeu.score,jeu.actions),'SauvegardeAleatoire/'+files[data_choix])
                            print(f"Une meilleure solution a été trouvée : {jeu.score}")

                except Exception as e:
                    # print(f"Une erreur est survenue : {str(e)}")
                    break
