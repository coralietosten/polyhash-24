import sys
from DAOFichier import DAOFichier
from CarteIDBalises import CarteIDBalises
from Polyhash import Polyhash

if __name__ == "__main__":
    DAO = DAOFichier
    polyhash: Polyhash = DAO.donne_polyhash(sys.argv[1])
    carteIDBalises = CarteIDBalises(polyhash.cibles, polyhash.lignes, polyhash.colonnes, polyhash.ballons)