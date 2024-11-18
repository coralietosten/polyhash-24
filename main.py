import sys
from DAOFichier import DAOFichier
from Jeu import Jeu
from Strategies.StrategieAleatoire import StrategieAleatoire
if __name__ == "__main__":
    DAO = DAOFichier
    polyhash = DAO.donne_polyhash("data/a_example.in")
    jeu = Jeu(polyhash)
    jeu.lancement_jeu(StrategieAleatoire())
    print(jeu.actions)
    print(jeu.score)