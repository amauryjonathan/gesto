from .appareil import Appareil

class Four(Appareil):
    def __init__(self, identifiant: str, marque: str, reference: str, numero_serie: str, date_arrivee: str, statut: str, volume: float):
        super().__init__(identifiant, marque, reference, numero_serie, date_arrivee, statut)
        self.volume = volume

    def get_type(self) -> str:
        return "Four"

    def __str__(self):
        return f"{super().__str__()} - Volume: {self.volume}L" 