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
            # Chemin vers le fichier JSON dans app/data
            json_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "appareils.json")
            with open(json_path, "r", encoding="utf-8") as f:
                data = json.load(f)
                for type_app, liste in data.items():
                    for appareil in liste:
                        # Création de l'appareil avec les données de base
                        if type_app == "frigo":
                            new_appareil = Frigo(
                                appareil["identifiant"],
                                appareil["marque"],
                                appareil["reference"],
                                appareil["numero_serie"],
                                appareil["date_arrivee"],
                                appareil["statut"],
                                appareil["specifique"]
                            )
                        elif type_app == "four":
                            new_appareil = Four(
                                appareil["identifiant"],
                                appareil["marque"],
                                appareil["reference"],
                                appareil["numero_serie"],
                                appareil["date_arrivee"],
                                appareil["statut"],
                                appareil["specifique"]
                            )
                        elif type_app == "lave_linge":
                            new_appareil = LaveLinge(
                                appareil["identifiant"],
                                appareil["marque"],
                                appareil["reference"],
                                appareil["numero_serie"],
                                appareil["date_arrivee"],
                                appareil["statut"],
                                appareil["specifique"]
                            )
                        elif type_app == "lave_linge_sechant":
                            new_appareil = LaveLingeSechant(
                                appareil["identifiant"],
                                appareil["marque"],
                                appareil["reference"],
                                appareil["numero_serie"],
                                appareil["date_arrivee"],
                                appareil["statut"],
                                appareil["specifique"],
                                appareil["capacite_sechage"]
                            )
                        elif type_app == "lave_vaisselle":
                            new_appareil = LaveVaisselle(
                                appareil["identifiant"],
                                appareil["marque"],
                                appareil["reference"],
                                appareil["numero_serie"],
                                appareil["date_arrivee"],
                                appareil["statut"],
                                appareil["specifique"]
                            )
                        # Ajout de la localisation si elle existe
                        if "cellule" in appareil and "emplacement" in appareil and "position" in appareil:
                            new_appareil.set_localisation(
                                appareil["cellule"],
                                appareil["emplacement"],
                                appareil["position"]
                            )
                        self.appareils[type_app].append(new_appareil)
        except Exception as e:
            print(f"Erreur lors du chargement du fichier JSON: {str(e)}")

    def sauvegarder_json(self):
        data = {}
        for type_app, liste in self.appareils.items():
            data[type_app] = []
            for appareil in liste:
                appareil_dict = {
                    "identifiant": appareil.identifiant,
                    "marque": appareil.marque,
                    "reference": appareil.reference,
                    "numero_serie": appareil.numero_serie,
                    "date_arrivee": appareil.date_arrivee,
                    "statut": appareil.statut,
                    "cellule": appareil.cellule,
                    "emplacement": appareil.emplacement,
                    "position": appareil.position
                }
                # Ajout des spécificités selon le type d'appareil
                if type_app == "frigo":
                    appareil_dict["specifique"] = appareil.temperature
                elif type_app == "four":
                    appareil_dict["specifique"] = appareil.temperature
                elif type_app == "lave_linge":
                    appareil_dict["specifique"] = appareil.capacite
                elif type_app == "lave_linge_sechant":
                    appareil_dict["specifique"] = appareil.capacite
                    appareil_dict["capacite_sechage"] = appareil.capacite_sechage
                elif type_app == "lave_vaisselle":
                    appareil_dict["specifique"] = appareil.capacite
                data[type_app].append(appareil_dict)
        try:
            json_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "appareils.json")
            with open(json_path, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"Erreur lors de la sauvegarde du fichier JSON: {str(e)}")

    def ajouter_appareil(self, appareil):
        # Vérifier unicité de l'emplacement si localisation renseignée
        if appareil.cellule and appareil.emplacement and appareil.position:
            for type_app, liste in self.appareils.items():
                for a in liste:
                    if (a.cellule == appareil.cellule and
                        a.emplacement == appareil.emplacement and
                        a.position == appareil.position):
                        raise ValueError(f"L'emplacement {appareil.cellule}{appareil.emplacement}{appareil.position} est déjà occupé.")
        type_ = appareil.get_type().lower()
        if type_ == "lave-linge séchant":
            type_ = "lave_linge_sechant"
        elif type_ == "lave-linge":
            type_ = "lave_linge"
        elif type_ == "lave-vaisselle":
            type_ = "lave_vaisselle"
        self.appareils[type_].append(appareil)
        self.sauvegarder_json()

    def lister_appareils(self):
        return self.appareils

    def get_appareil_par_localisation(self, cellule: str, emplacement: int, position: str) -> AppareilElectromenager:
        for type_app, liste in self.appareils.items():
            for appareil in liste:
                if (appareil.cellule == cellule and 
                    appareil.emplacement == emplacement and 
                    appareil.position == position):
                    return appareil
        return None 