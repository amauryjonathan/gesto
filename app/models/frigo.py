from .appareil import AppareilElectromenager

class Frigo(AppareilElectromenager):
    def __init__(self, identifiant: str, marque: str, reference: str, numero_serie: str, date_arrivee: str, statut: str, temperature: float = 4.0):
        super().__init__(identifiant, marque, reference, numero_serie, date_arrivee, statut)
        self.temperature = temperature

    def get_type(self) -> str:
        return "Réfrigérateur"

    def regler_temperature(self, temperature: float):
        self.temperature = temperature
        print(f"Température réglée à {temperature}°C") 