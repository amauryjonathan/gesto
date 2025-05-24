from typing import List, Dict
import json
import os
from app.models.appareil import AppareilElectromenager
from app.models.frigo import Frigo
from app.models.four import Four
from app.models.lave_linge import LaveLinge
from app.models.lave_vaisselle import LaveVaisselle
from app.models.lave_linge_sechant import LaveLingeSechant

class GestionnaireAppareils:
    def __init__(self):
        self.appareils = {
            "frigo": [],
            "four": [],
            "lave_linge": [],
            "lave_linge_sechant": [],
            "lave_vaisselle": []
        }
        self.charger_json()

    def charger_json(self):
        try:
            with open("appareils.json", "r") as f:
                data = json.load(f)
                for appareil in data:
                    type_ = appareil["type"]
                    if type_ == "frigo":
                        self.appareils["frigo"].append(Frigo(
                            appareil["identifiant"],
                            appareil["marque"],
                            appareil["reference"],
                            appareil["numero_serie"],
                            appareil["date_arrivee"],
                            appareil["statut"],
                            appareil["specifique"]
                        ))
                    elif type_ == "four":
                        self.appareils["four"].append(Four(
                            appareil["identifiant"],
                            appareil["marque"],
                            appareil["reference"],
                            appareil["numero_serie"],
                            appareil["date_arrivee"],
                            appareil["statut"],
                            appareil["specifique"]
                        ))
                    elif type_ == "lave_linge":
                        self.appareils["lave_linge"].append(LaveLinge(
                            appareil["identifiant"],
                            appareil["marque"],
                            appareil["reference"],
                            appareil["numero_serie"],
                            appareil["date_arrivee"],
                            appareil["statut"],
                            appareil["specifique"]
                        ))
                    elif type_ == "lave_linge_sechant":
                        self.appareils["lave_linge_sechant"].append(LaveLingeSechant(
                            appareil["identifiant"],
                            appareil["marque"],
                            appareil["reference"],
                            appareil["numero_serie"],
                            appareil["date_arrivee"],
                            appareil["statut"],
                            appareil["specifique"],
                            appareil["capacite_sechage"]
                        ))
                    elif type_ == "lave_vaisselle":
                        self.appareils["lave_vaisselle"].append(LaveVaisselle(
                            appareil["identifiant"],
                            appareil["marque"],
                            appareil["reference"],
                            appareil["numero_serie"],
                            appareil["date_arrivee"],
                            appareil["statut"],
                            appareil["specifique"]
                        ))
        except Exception as e:
            print(f"Erreur lors du chargement du fichier JSON: {str(e)}")

    def ajouter_appareil(self, appareil):
        type_ = appareil.get_type().lower()
        if type_ == "lave-linge séchant":
            type_ = "lave_linge_sechant"
        elif type_ == "lave-linge":
            type_ = "lave_linge"
        elif type_ == "lave-vaisselle":
            type_ = "lave_vaisselle"
        self.appareils[type_].append(appareil)

    def lister_appareils(self):
        return self.appareils 