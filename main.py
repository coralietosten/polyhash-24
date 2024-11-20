import sys
from DAOFichier import DAOFichier
from Jeu import Jeu
from Strategies.StrategieAleatoire import StrategieAleatoire
from Polyhash import Polyhash

if __name__ == "__main__":
    DAO = DAOFichier
    polyhash: Polyhash = DAO.donne_polyhash("data/b_small.in")
    # polyhash: Polyhash = DAO.donne_polyhash(sys.argv[1])
    jeu = Jeu(polyhash)
    max_game = (0,[])
    #Test avec la Stratégie Aléatoire
    for i in range(100000):
        jeu.lancement_jeu(StrategieAleatoire())
        if jeu.score > max_game[0]:
            max_game = (jeu.score,jeu.actions)
    print(max_game)