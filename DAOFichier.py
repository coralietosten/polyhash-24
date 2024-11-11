from Polyhash import Polyhash
from Vecteur2 import Vecteur2
from CarteVent import CarteVent
from Balise import Balise

class DAOFichier:
    # TODO : documentation
    def donne_polyhash(nom_fichier: str)-> Polyhash:
        try :
            with open(nom_fichier, 'r') as input_file:
                contenu = input_file.read() # lecture du contenu du fichier,
                list_contenu = contenu.split("\n")
                try :
                    # Ligne 1
                    ligne_1 = list_contenu[0].split(" ")
                    lignes = int(ligne_1[0])
                    colonnes = int(ligne_1[1])
                    altitudes = int(ligne_1[2])

                    # Ligne 2
                    ligne_2 = list_contenu[1].split(" ")
                    nombre_cibles = int(ligne_2[0])
                    rayon_couverture = int(ligne_2[1])
                    ballons = int(ligne_2[2])
                    tours = int(ligne_2[3])

                    # Ligne 3
                    ligne_3 = list_contenu[2].split(" ")
                    depart = Vecteur2(ligne_3[0], ligne_3[1])

                    # A partir de la ligne 4
                    cibles = []
                    for i in range(3, 3 + nombre_cibles)  :
                        ligne_i = list_contenu[i].split(" ")
                        cibles.append(Balise(Vecteur2(ligne_i[0], ligne_i[1])))

                    # Vents 
                    carte_vent = []
                    for a in range(altitudes) :
                        vent_altitude_a = []
                        for l in range(3 + nombre_cibles + lignes*a, 3 + nombre_cibles + (a+1)*lignes) :
                            ligne_l = list_contenu[l].split(" ") 
                            vent_ligne_l = []
                            for c in range(0, colonnes*2, 2) :
                                vent_ligne_l.append(Vecteur2(int(ligne_l[c+1]), int(ligne_l[c])))
                            vent_altitude_a.append(vent_ligne_l)
                        carte_vent.append(vent_altitude_a)
                    
                    polyhash = Polyhash(lignes, colonnes, altitudes, nombre_cibles, rayon_couverture, ballons, tours, depart, cibles, CarteVent(carte_vent))
                    return polyhash
                except : 
                    print("Le contenu du fichier n'est pas à la forme valide !")
        except :
            print("Le fichier n'existe pas !")
