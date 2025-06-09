from typing import List, Dict
import json
import os
from app.models.appareil import Appareil
from app.models.frigo import Frigo
from app.models.four import Four
from app.models.lave_linge import LaveLinge
from app.models.lave_vaisselle import LaveVaisselle
from app.models.lave_linge_sechant import LaveLingeSechant
from app.models.fiche_panne import FichePanne
from datetime import datetime

class GestionnaireAppareils:
    def __init__(self):
        self.appareils = {
            "frigo": [],
            "four": [],
            "lave_linge": [],
            "lave_linge_sechant": [],
            "lave_vaisselle": []
        }
        self.fiches_panne = {}  # Dictionnaire des fiches de panne par appareil_id
        self.charger_json()
        self.charger_fiches_panne()

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

    def get_appareil_par_localisation(self, cellule: str, emplacement: int, position: str) -> Appareil:
        for type_app, liste in self.appareils.items():
            for appareil in liste:
                if (appareil.cellule == cellule and 
                    appareil.emplacement == emplacement and 
                    appareil.position == position):
                    return appareil
        return None 

    def charger_fiches_panne(self):
        try:
            with open("app/data/fiches_panne.json", "r", encoding="utf-8") as f:
                data = json.load(f)
                for appareil_id, fiche_data in data.items():
                    self.fiches_panne[appareil_id] = FichePanne.from_dict(fiche_data)
        except FileNotFoundError:
            pass

    def sauvegarder_fiches_panne(self):
        data = {appareil_id: fiche.to_dict() for appareil_id, fiche in self.fiches_panne.items()}
        with open("app/data/fiches_panne.json", "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)

    def ajouter_fiche_panne(self, appareil_id, symptome, type_panne, cause_probable, notes_techniques, technicien):
        fiche = FichePanne(appareil_id, datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        fiche.symptome = symptome
        fiche.type_panne = type_panne
        fiche.cause_probable = cause_probable
        fiche.notes_techniques = notes_techniques
        fiche.technicien = technicien
        self.fiches_panne[appareil_id] = fiche
        self.sauvegarder_fiches_panne()

    def get_fiche_panne(self, appareil_id):
        return self.fiches_panne.get(appareil_id)

    def mettre_a_jour_fiche_panne(self, appareil_id, **kwargs):
        if appareil_id in self.fiches_panne:
            fiche = self.fiches_panne[appareil_id]
            for key, value in kwargs.items():
                if hasattr(fiche, key):
                    setattr(fiche, key, value)
            self.sauvegarder_fiches_panne()

    def get_appareil_by_id(self, appareil_id):
        for type_app, appareils in self.appareils.items():
            for appareil in appareils:
                if appareil.identifiant == appareil_id:
                    return appareil
        return None 