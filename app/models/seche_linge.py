from .appareil import Appareil

class SecheLinge(Appareil):
    def __init__(self, identifiant: str, marque: str, reference: str, numero_serie: str, date_arrivee: str, statut: str, capacite: float):
        super().__init__(identifiant, marque, reference, numero_serie, date_arrivee, statut)
        self.capacite = capacite

    def get_type(self) -> str:
        return "Sèche-linge"

    def __str__(self):
        return f"{super().__str__()} - Capacité: {self.capacite}kg" 