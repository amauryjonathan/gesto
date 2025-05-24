class AppareilElectromenager:
    def __init__(self, identifiant: str, marque: str, reference: str, numero_serie: str, date_arrivee: str, statut: str):
        self.identifiant = identifiant
        self.marque = marque
        self.reference = reference
        self.numero_serie = numero_serie
        self.date_arrivee = date_arrivee
        self.statut = statut

    def get_type(self) -> str:
        return "Appareil"

    def __str__(self):
        return f"{self.get_type()} - {self.identifiant} - {self.marque} {self.reference} - {self.numero_serie} - {self.date_arrivee} - {self.statut}"

