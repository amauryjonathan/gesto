from datetime import datetime

class Test:
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
        """Crée un test à partir d'un dictionnaire"""
        test = cls(data["appareil_id"], data.get("date_verification"))
        
        # Gérer les valeurs booléennes et non_testé
        def to_bool(value):
            if isinstance(value, bool):
                return value
            if isinstance(value, str):
                return value.lower() in ['true', 'vrai', 'ok']
            return False
        
        # Mettre à jour les vérifications visuelles
        test.commande_ok = data.get("commande_ok", False)
        test.verrou_porte_ok = data.get("verrou_porte_ok", False)
        test.rotation_tambour_ok = data.get("rotation_tambour_ok", False)
        test.chauffe_ok = data.get("chauffe_ok", False)
        test.essorage_ok = data.get("essorage_ok", False)
        test.sechage_ok = data.get("sechage_ok", False)
        
        # Mettre à jour les programmes
        test.programme_express = data.get("programme_express", "non_testé")
        test.programme_chauffe = data.get("programme_chauffe", "non_testé")
        test.programme_rotation = data.get("programme_rotation", "non_testé")
        
        # Mettre à jour les observations
        test.observations = data.get("observations", {})
        
        # Mettre à jour le statut
        test.statut = data.get("statut", "en_cours")
        
        return test
    
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