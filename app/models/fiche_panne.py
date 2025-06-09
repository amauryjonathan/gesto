class FichePanne:
    def __init__(self, appareil_id, date_creation=None):
        self.appareil_id = appareil_id
        self.date_creation = date_creation
        self.symptome = ""
        self.type_panne = ""
        self.cause_probable = ""
        self.notes_techniques = ""
        self.statut = "à réparer"  # à réparer, diagnostiquer, réparer
        self.date_resolution = None
        self.technicien = ""
        
    def to_dict(self):
        return {
            "appareil_id": self.appareil_id,
            "date_creation": self.date_creation,
            "symptome": self.symptome,
            "type_panne": self.type_panne,
            "cause_probable": self.cause_probable,
            "notes_techniques": self.notes_techniques,
            "statut": self.statut,
            "date_resolution": self.date_resolution,
            "technicien": self.technicien
        }
    
    @classmethod
    def from_dict(cls, data):
        fiche = cls(data["appareil_id"], data["date_creation"])
        fiche.symptome = data["symptome"]
        fiche.type_panne = data["type_panne"]
        fiche.cause_probable = data["cause_probable"]
        fiche.notes_techniques = data["notes_techniques"]
        fiche.statut = data["statut"]
        fiche.date_resolution = data["date_resolution"]
        fiche.technicien = data["technicien"]
        return fiche 