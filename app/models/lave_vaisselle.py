from .appareil import AppareilElectromenager

class LaveVaisselle(AppareilElectromenager):
    def __init__(self, identifiant: str, marque: str, reference: str, numero_serie: str, date_arrivee: str, statut: str, capacite: int):
        super().__init__(identifiant, marque, reference, numero_serie, date_arrivee, statut)
        self.capacite = capacite  # nombre de couverts

    def get_type(self) -> str:
        return "Lave-vaisselle"

    def lancer_cycle(self, programme: str):
        print(f"Lancement du programme {programme}") 