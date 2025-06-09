from .appareil import Appareil

class LaveLingeSechant(Appareil):
    def __init__(self, identifiant: str, marque: str, reference: str, numero_serie: str, date_arrivee: str, statut: str, capacite: float, capacite_sechage: float):
        super().__init__(identifiant, marque, reference, numero_serie, date_arrivee, statut)
        self.capacite = capacite
        self.capacite_sechage = capacite_sechage

    def get_type(self) -> str:
        return "Lave-linge séchant"

    def __str__(self):
        return f"{super().__str__()} - Capacité lavage: {self.capacite}kg - Capacité séchage: {self.capacite_sechage}kg"

    def lancer_cycle(self, programme: str, sechage: bool = False):
        super().lancer_cycle(programme)
        if sechage:
            print(f"Lancement du séchage - Capacité de séchage : {self.capacite_sechage} kg") 