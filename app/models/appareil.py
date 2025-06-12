class Appareil:
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
        # Création de l'identifiant unique caché
        self.identifiant_unique = f"{marque}-{reference}-{numero_serie}"

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

    def to_dict(self):
        return {
            "identifiant": self.identifiant,
            "identifiant_unique": self.identifiant_unique,
            "marque": self.marque,
            "reference": self.reference,
            "numero_serie": self.numero_serie,
            "date_arrivee": self.date_arrivee,
            "statut": self.statut,
            "cellule": self.cellule,
            "emplacement": self.emplacement,
            "position": self.position
        }

    @classmethod
    def from_dict(cls, data):
        """Crée un appareil à partir d'un dictionnaire"""
        appareil = cls(
            identifiant=data["identifiant"],
            marque=data["marque"],
            reference=data["reference"],
            numero_serie=data["numero_serie"],
            date_arrivee=data["date_arrivee"],
            statut=data["statut"],
        )
        
        # Gérer la localisation si elle existe
        if "cellule" in data and "emplacement" in data and "position" in data:
            appareil.set_localisation(data["cellule"], data["emplacement"], data["position"])
            
        # Si l'identifiant unique n'existe pas dans les données, le créer
        if "identifiant_unique" not in data:
            appareil.identifiant_unique = f"{appareil.marque}-{appareil.reference}-{appareil.numero_serie}"
        else:
            appareil.identifiant_unique = data["identifiant_unique"]
            
        return appareil

