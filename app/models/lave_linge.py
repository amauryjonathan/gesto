from .appareil import AppareilElectromenager

class LaveLinge(AppareilElectromenager):
    def __init__(self, identifiant: str, marque: str, reference: str, numero_serie: str, date_arrivee: str, statut: str, capacite: float):
        super().__init__(identifiant, marque, reference, numero_serie, date_arrivee, statut)
        self.capacite = capacite  # en kg

    def get_type(self) -> str:
        return "Lave-linge"

    def lancer_cycle(self, programme: str):
        print(f"Lancement du programme {programme}") 