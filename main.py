import sys
from DAOFichier import DAOFichier
from Jeu import Jeu
from Strategies.StrategieAleatoire import StrategieAleatoire
from Strategies.GusStrategie import GusStrategie
from Strategies.StrategieProche import StrategieProche
from Polyhash import Polyhash

if __name__ == "__main__":
    DAO = DAOFichier
    polyhash: Polyhash = DAO.donne_polyhash("data/a_example.in")
    # polyhash: Polyhash = DAO.donne_polyhash(sys.argv[1])
    jeu = Jeu(polyhash)
    #Test avec la Stratégie Aléatoire
    max_game = (0,[])
    for i in range(1000):
        jeu.lancement_jeu(StrategieAleatoire())
        if jeu.score > max_game[0]:
            max_game = (jeu.score,jeu.actions)
    print("Aléatoire : ",max_game)

    #Test avec la Stratégie Augustin
    """max_game = (0,[])
    jeu.lancement_jeu(GusStrategie())
    if jeu.score > max_game[0]:
        max_game = (jeu.score,jeu.actions)
    print("Augustin : ",max_game)"""

    max_game = (0,[])
    jeu.lancement_jeu(StrategieProche())
    max_game = (jeu.score,jeu.actions)
    print("Proche : ",max_game)



    