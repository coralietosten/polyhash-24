import sys
from DAOFichier import DAOFichier

if __name__ == "__main__":
    DAO = DAOFichier
    polyshash = DAO.donne_polyhash(sys.argv[1])
    print(polyshash)