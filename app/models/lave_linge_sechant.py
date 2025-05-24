from .lave_linge import LaveLinge

class LaveLingeSechant(LaveLinge):
    def __init__(self, identifiant: str, marque: str, reference: str, numero_serie: str, date_arrivee: str, statut: str, capacite: float, capacite_sechage: float):
        super().__init__(identifiant, marque, reference, numero_serie, date_arrivee, statut, capacite)
        self.capacite_sechage = capacite_sechage  # en kg

    def get_type(self) -> str:
        return "Lave-linge séchant"

    def lancer_cycle(self, programme: str, sechage: bool = False):
        super().lancer_cycle(programme)
        if sechage:
            print(f"Lancement du séchage - Capacité de séchage : {self.capacite_sechage} kg") 