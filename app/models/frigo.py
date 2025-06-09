from .appareil import Appareil

class Frigo(Appareil):
    def __init__(self, identifiant: str, marque: str, reference: str, numero_serie: str, date_arrivee: str, statut: str, temperature: float):
        super().__init__(identifiant, marque, reference, numero_serie, date_arrivee, statut)
        self.temperature = temperature

    def get_type(self) -> str:
        return "Frigo"

    def __str__(self):
        return f"{super().__str__()} - Température: {self.temperature}°C"

    def regler_temperature(self, temperature: float):
        self.temperature = temperature
        print(f"Température réglée à {temperature}°C") 