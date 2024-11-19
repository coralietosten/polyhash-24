from Polyhash import Polyhash
class StrategieInterface:
    def initialisation(self,polyhash : Polyhash):
        pass
    def donne_action(self, ballon) -> int:
        """entrée : un ballon et les données du polyhash
           sortie : l'action à effectuer pour un tour pour un ballon"""
        pass
    