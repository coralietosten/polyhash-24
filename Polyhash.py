from dataclasses import dataclass
from Balise import Balise
from Vecteur2 import Vecteur2
from CarteVent import CarteVent
from CarteIDBalises import CarteIDBalises

@dataclass
class Polyhash:
    # TODO : documentation
    lignes: int
    colonnes: int
    altitudes: int
    nombre_cibles: int
    rayon_couverture: int
    nombre_ballons: int
    nombre_tours: int
    depart: Vecteur2
    cibles: list[Balise]
    carte_vent: CarteVent
    carteIDBalises: list = None  # Initialisée dans __post_init__

    def __post_init__(self):
        # Initialisation de `carteIDBalises`
        carteID = CarteIDBalises(self.cibles, self.lignes, self.colonnes, self.rayon_couverture)
        self.carteIDBalises = carteID.carteBalise

    def __str__(self):
        return (
            f"Polyhash(\n"
            f"    lignes = {self.lignes}, colonnes = {self.colonnes}, altitudes = {self.altitudes},\n"
            f"    nombre_cibles = {self.nombre_cibles}, rayon_couverture = {self.rayon_couverture}, ballons = {self.nombre_ballons}, tours = {self.nombre_tours},\n"
            f"    depart = {self.depart},\n"
            f"    cibles = {self.cibles},\n"
            f"    carte_vent = {self.carte_vent}\n"
            f")"
        )

    def __repr__(self):
        return self.__str__()


