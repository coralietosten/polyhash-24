import sys
from DAOFichier import DAOFichier
from Jeu import Jeu
from Strategies.StrategieAleatoire import StrategieAleatoire
from Polyhash import Polyhash

if __name__ == "__main__":
    DAO = DAOFichier
    polyhash: Polyhash = DAO.donne_polyhash("data/a_example.in")
    # polyhash: Polyhash = DAO.donne_polyhash(sys.argv[1])
    jeu = Jeu(polyhash)
    jeu.lancement_jeu(StrategieAleatoire())
    print(jeu.actions)
    print(jeu.score)