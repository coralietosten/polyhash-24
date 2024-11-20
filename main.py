import sys
from DAOFichier import DAOFichier
from Jeu import Jeu
from Strategies.StrategieAleatoire import StrategieAleatoire
from Strategies.GusStrategie import GusStrategie
from Polyhash import Polyhash

data_choix = 1
files = ["a_example","b_small","c_medium","d_final"]
if __name__ == "__main__":
    polyhash: Polyhash = DAOFichier.donne_polyhash("data/"+files[data_choix]+".in")
    # polyhash: Polyhash = DAO.donne_polyhash(sys.argv[1])
    jeu = Jeu(polyhash)
    #Test avec la Stratégie Aléatoire
    jeu.lancement_jeu(StrategieAleatoire())
    print("Aléatoire : ",jeu.score,jeu.actions)
    DAOFichier.cree_fichier(jeu.actions)

    #Test avec la Stratégie Augustin
    # jeu.lancement_jeu(GusStrategie())
    # print("Augustin : ",jeu.score,jeu.actions)



    