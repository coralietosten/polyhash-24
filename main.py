import sys,os
from DAOFichier import DAOFichier
from Jeu import Jeu
from Strategies.StrategieAleatoire import StrategieAleatoire
from Strategies.StrategieProche import StrategieProche
from Strategies.Strategie import Strategie
from Strategies.StrategieArbre import StrategieArbre
from Polyhash import Polyhash
from Strategies.StrategieTripleLigne import StrategieTripleLigne
import pickle
data_choix = 3
files = ["a_example","b_small","c_medium","d_final"]

def enregistrer_solution(game):
    global files
    global data_choix
    with open('C:/Users/brali/Documents/PolytechDoc/ProjetAlgo/Vizualiser/polyhash-24/SauvegardeAleatoire/'+files[data_choix], 'wb') as f:
            pickle.dump(game, f)

if __name__ == "__main__": 
    
    if len(sys.argv) - 1 > 2 or len(sys.argv) - 1  == 0 :
        print("Attention : Il manque des paramètres !")
        print("""Construction de la commande : 
                py fichier.py chemin/fichier_entree.txt chemin/fichier_sortie.txt
               
              OU

                py fichier.py chemin/fichier_sortie.txt
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
        max_game = (0,[])

        #Test avec la Stratégie Proche
        jeu.lancement_jeu(StrategieProche())
        game = (jeu.score,jeu.actions)
        max_game = game
        print("Proche : ",game[0])
        
        #Test avec la Stratégie A*
        jeu.lancement_jeu(Strategie())
        game = (jeu.score,jeu.actions)
        if game[0]>max_game[0] :
            max_game = game
        print("A_star : ",game[0])

        #  Test avec la Stratégie triple Ligne
        jeu.lancement_jeu(StrategieTripleLigne())
        game = (jeu.score,jeu.actions)
        if game[0]>max_game[0] :
            max_game = game
        print("Triple Ligne : ",game[0])

        #Enregistrement de la stratégie ayant fait le meilleur score : 
        DAO.cree_fichier(max_game[1],chemin_sortie)


    
    