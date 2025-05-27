class AppareilElectromenager:
    def __init__(self, identifiant: str, marque: str, reference: str, numero_serie: str, date_arrivee: str, statut: str, cellule: str = None, emplacement: int = None, position: str = None):
        self.identifiant = identifiant
        self.marque = marque
        self.reference = reference
        self.numero_serie = numero_serie
        self.date_arrivee = date_arrivee
        self.statut = statut
        self.cellule = cellule  # Lettre de A à R
        self.emplacement = emplacement  # Numéro de 1 à 9
        self.position = position  # 'A' pour devant, 'B' pour derrière

    def get_type(self) -> str:
        return "Appareil"

    def set_localisation(self, cellule: str, emplacement: int, position: str):
        if cellule not in [chr(i) for i in range(65, 83)]:  # A à R
            raise ValueError("La cellule doit être une lettre entre A et R")
        if not 1 <= emplacement <= 9:
            raise ValueError("L'emplacement doit être un nombre entre 1 et 9")
        if position not in ['A', 'B']:
            raise ValueError("La position doit être 'A' (devant) ou 'B' (derrière)")
        self.cellule = cellule
        self.emplacement = emplacement
        self.position = position

    def get_localisation(self) -> str:
        if not all([self.cellule, self.emplacement, self.position]):
            return "Non localisé"
        return f"{self.cellule}{self.emplacement}{self.position}"

    def __str__(self):
        localisation = self.get_localisation()
        return f"{self.get_type()} - {self.identifiant} - {self.marque} {self.reference} - {self.numero_serie} - {self.date_arrivee} - {self.statut} - {localisation}"

