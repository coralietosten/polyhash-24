from Polyhash import Polyhash
from Vecteur2 import Vecteur2
from CarteVent import CarteVent
from Balise import Balise

class DAOFichier:
    """
    Classe pour lire un fichier de configuration et créer un objet `Polyhash`,
    ainsi que pour écrire les déplacements des ballons dans un fichier de sortie.

    Méthodes :
    - `donne_polyhash(chemin_fichier: str) -> Polyhash` :
        Lit un fichier de configuration et retourne un objet `Polyhash` initialisé à partir des données du fichier.
    - `cree_fichier(list_deplacement: list[list[int]], chemin_sortie: str = "sortie.txt") -> None` :
        Écrit les déplacements des ballons dans un fichier de sortie.
    """

    @staticmethod
    def donne_polyhash(chemin_fichier: str) -> Polyhash:
        """
        Lit un fichier de configuration et initialise un objet `Polyhash`.
        """
        try:
            with open(chemin_fichier, 'r') as input_file:
                contenu = input_file.read()  # Lecture du contenu du fichier
                list_contenu = contenu.split("\n")

                # Ligne 1
                ligne_1 = list_contenu[0].split(" ")
                lignes = int(ligne_1[0])
                colonnes = int(ligne_1[1])
                altitudes = int(ligne_1[2])

                # Ligne 2
                ligne_2 = list_contenu[1].split(" ")
                nombre_cibles = int(ligne_2[0])
                rayon_couverture = int(ligne_2[1])
                nombre_ballons = int(ligne_2[2])
                tours = int(ligne_2[3])

                # Ligne 3
                ligne_3 = list_contenu[2].split(" ")
                depart = Vecteur2(int(ligne_3[1]), int(ligne_3[0]))

                # À partir de la ligne 4
                cibles = []
                for i in range(3, 3 + nombre_cibles):
                    ligne_i = list_contenu[i].split(" ")
                    cibles.append(Balise(Vecteur2(int(ligne_i[1]), int(ligne_i[0]))))

                # Initialisation de la carte des vents
                carte_vent = []
                # Boucle sur chaque altitude
                for a in range(altitudes):
                    # Initialisation de la liste des vents pour l'altitude courante
                    vent_altitude_a = []

                    # Boucle sur les lignes correspondant à l'altitude courante
                    for l in range(3 + nombre_cibles + lignes * a, 3 + nombre_cibles + (a + 1) * lignes):
                        ligne_l = list_contenu[l].split(" ")
                        vent_ligne_l = []

                        # Boucle sur les colonnes de la ligne courante (chaque paire de valeurs représente un vecteur de vent)
                        for c in range(0, colonnes * 2, 2):
                            vent_ligne_l.append(Vecteur2(int(ligne_l[c + 1]), int(ligne_l[c])))
                        vent_altitude_a.append(vent_ligne_l)
                    carte_vent.append(vent_altitude_a)

                # Création de l'objet Polyhash
                polyhash = Polyhash(
                    lignes, colonnes, altitudes, nombre_cibles,
                    rayon_couverture, tours, nombre_ballons,
                    depart, cibles, CarteVent(carte_vent)
                )
                return polyhash

        except FileNotFoundError:
            raise FileNotFoundError(f"Le fichier spécifié '{chemin_fichier}' est introuvable.")
        except (ValueError, IndexError) as e:
            raise ValueError(f"Le fichier '{chemin_fichier}' contient des données invalides ou mal formatées. Détails : {e}")

    @staticmethod
    def cree_fichier(list_deplacement: list[list[int]], chemin_sortie="sortie.txt") -> None:
        """
        Écrit les déplacements des ballons dans un fichier de sortie.
        """
        contenu = ""
        for dep in list_deplacement :
            ligne = ""
            for val in dep :
                ligne += str(val) + " "
            ligne += "\n"
            contenu += ligne
        
        with open(chemin_sortie, 'w') as fichier:
            fichier.write(contenu)