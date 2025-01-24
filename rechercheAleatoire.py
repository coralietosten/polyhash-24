import os,sys
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
    if len(sys.argv) - 1 > 2 or len(sys.argv) - 1  == 0 :
        print("Attention : Il manque des paramètres !")
        print("""Construction de la commande : 
                py rechercheAleatoire.py chemin/fichier_entree.txt chemin/fichier_sortie.txt
               
              OU

                py rechercheAleatoire.py chemin/fichier_sortie.txt
              """)
    else:
        if len(sys.argv) - 1 == 1 :
            print("Un seul paramètre à été sortie, il prend en compte le chemin de sortie")
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

if __name__ == "__main__":
    DAO = DAOFichier
    polyhash: Polyhash = DAO.donne_polyhash(chemin_entree)
    jeu = Jeu(polyhash)
    #Utilisation la Stratégie Aléatoire

    file_path = 'SauvegardeAleatoire/'+files[data_choix]
    if os.path.exists(file_path):
        with open('SauvegardeAleatoire/'+files[data_choix], 'rb') as f:
            max_game = pickle.load(f)
            DAOFichier.cree_fichier(max_game[1],chemin_sortie)

        print("Jeu : ",max_game[0])
    else:
        max_game = (0,[])
        
    enregistrer_solution(max_game)
    print("Sauvegardé !")
    while True:
        jeu.lancement_jeu(StrategieAleatoire())
        if jeu.score > max_game[0]:
            max_game = (jeu.score,jeu.actions)
            enregistrer_solution(max_game)
            print(f"Une meilleure solution a été trouvé ! ({jeu.score})")







    