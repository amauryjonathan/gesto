from datetime import datetime

class VerificationPreVente:
    def __init__(self, appareil_id, date_verification=None):
        self.appareil_id = appareil_id
        self.date_verification = date_verification or datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # Vérifications visuelles
        self.commande_ok = False
        self.verrou_porte_ok = False
        self.rotation_tambour_ok = False
        self.chauffe_ok = False
        self.essorage_ok = False
        self.sechage_ok = False
        
        # Programmes de test
        self.programme_express = "non_testé"  # non_testé, en_cours, réussi, échoué
        self.programme_chauffe = "non_testé"
        self.programme_rotation = "non_testé"
        
        # Observations
        self.observations = {
            "commande": "",
            "verrou_porte": "",
            "rotation_tambour": "",
            "chauffe": "",
            "essorage": "",
            "sechage": "",
            "programme_express": "",
            "programme_chauffe": "",
            "programme_rotation": ""
        }
        
        # Statut global
        self.statut = "en_cours"  # en_cours, validé, rejeté
        
    def to_dict(self):
        return {
            "appareil_id": self.appareil_id,
            "date_verification": self.date_verification,
            "commande_ok": self.commande_ok,
            "verrou_porte_ok": self.verrou_porte_ok,
            "rotation_tambour_ok": self.rotation_tambour_ok,
            "chauffe_ok": self.chauffe_ok,
            "essorage_ok": self.essorage_ok,
            "sechage_ok": self.sechage_ok,
            "programme_express": self.programme_express,
            "programme_chauffe": self.programme_chauffe,
            "programme_rotation": self.programme_rotation,
            "observations": self.observations,
            "statut": self.statut
        }
    
    @classmethod
    def from_dict(cls, data):
        verification = cls(data["appareil_id"], data["date_verification"])
        verification.commande_ok = data["commande_ok"]
        verification.verrou_porte_ok = data["verrou_porte_ok"]
        verification.rotation_tambour_ok = data["rotation_tambour_ok"]
        verification.chauffe_ok = data["chauffe_ok"]
        verification.essorage_ok = data["essorage_ok"]
        verification.sechage_ok = data["sechage_ok"]
        verification.programme_express = data["programme_express"]
        verification.programme_chauffe = data["programme_chauffe"]
        verification.programme_rotation = data["programme_rotation"]
        verification.observations = data["observations"]
        verification.statut = data["statut"]
        return verification
    
    def est_complete(self):
        """Vérifie si toutes les vérifications ont été effectuées"""
        verifications_ok = all([
            self.commande_ok,
            self.verrou_porte_ok,
            self.rotation_tambour_ok,
            self.chauffe_ok,
            self.essorage_ok,
            self.sechage_ok
        ])
        
        programmes_ok = all([
            self.programme_express == "réussi",
            self.programme_chauffe == "réussi",
            self.programme_rotation == "réussi"
        ])
        
        return verifications_ok and programmes_ok 