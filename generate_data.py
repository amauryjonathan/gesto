import json
import os
import random
from datetime import datetime, timedelta
from itertools import product

def generate_appareils():
    # Liste des marques disponibles
    marques = [
        "Samsung", "LG", "Bosch", "Whirlpool", "Electrolux",
        "Beko", "Haier", "Siemens", "Candy", "Indesit"
    ]
    
    # Types d'appareils et leurs caractéristiques
    types_appareils = {
        "frigo": {
            "prefix_id": "F",
            "ref_prefix": "RT",
            "temp_range": (2, 8)
        },
        "four": {
            "prefix_id": "O",
            "ref_prefix": "OV",
            "temp_range": (100, 250)
        },
        "lave_linge": {
            "prefix_id": "L",
            "ref_prefix": "WL",
            "cap_range": (5, 12)
        },
        "lave_vaisselle": {
            "prefix_id": "LV",
            "ref_prefix": "DW",
            "cap_range": (8, 16)
        },
        "lave_linge_sechant": {
            "prefix_id": "LS",
            "ref_prefix": "WD",
            "cap_range": (7, 10),
            "sechage_range": (4, 8)
        }
    }
    
    # Statuts possibles
    statuts = ["A Nettoyer", "En attente", "En réparation", "Réparé", "En test", "Prêt à livrer"]
    
    # Générer la date d'arrivée (entre 1 et 30 jours dans le passé)
    def random_date():
        days_ago = random.randint(1, 30)
        return (datetime.now() - timedelta(days=days_ago)).strftime("%Y-%m-%d")
    
    # Structure de base
    appareils = {
        "frigo": [],
        "four": [],
        "lave_linge": [],
        "lave_vaisselle": [],
        "lave_linge_sechant": []
    }
    
    # Générer toutes les combinaisons possibles de racks
    cellules = [chr(i) for i in range(65, 83)]  # A à R
    emplacements = list(range(1, 10))  # 1 à 9
    positions = ["A", "B"]
    all_racks = list(product(cellules, emplacements, positions))
    random.shuffle(all_racks)
    rack_index = 0
    
    # Générer 200 appareils (40 de chaque type)
    for type_app, specs in types_appareils.items():
        for i in range(40):
            # Générer un identifiant unique
            identifiant = f"{specs['prefix_id']}{i+1:03d}"
            
            # Générer une référence
            reference = f"{specs['ref_prefix']}{random.randint(100, 999)}"
            
            # Créer l'appareil
            appareil = {
                "identifiant": identifiant,
                "marque": random.choice(marques),
                "reference": reference,
                "numero_serie": f"SN{random.randint(10000, 99999)}",
                "date_arrivee": random_date(),
                "statut": random.choice(statuts)
            }
            
            # Ajouter les caractéristiques spécifiques selon le type
            if type_app == "frigo":
                appareil["specifique"] = round(random.uniform(*specs["temp_range"]), 1)
            elif type_app == "four":
                appareil["specifique"] = round(random.uniform(*specs["temp_range"]))
            elif type_app == "lave_linge":
                appareil["specifique"] = round(random.uniform(*specs["cap_range"]), 1)
            elif type_app == "lave_vaisselle":
                appareil["specifique"] = round(random.uniform(*specs["cap_range"]))
            elif type_app == "lave_linge_sechant":
                appareil["specifique"] = round(random.uniform(*specs["cap_range"]), 1)
                appareil["capacite_sechage"] = round(random.uniform(*specs["sechage_range"]), 1)
            
            # Attribuer un rack unique
            if rack_index < len(all_racks):
                cellule, emplacement, position = all_racks[rack_index]
                appareil["cellule"] = cellule
                appareil["emplacement"] = emplacement
                appareil["position"] = position
                rack_index += 1
            
            appareils[type_app].append(appareil)
    
    return appareils

def save_to_json(appareils):
    # Chemin vers le fichier JSON
    json_path = os.path.join("app", "data", "appareils.json")
    
    # S'assurer que le dossier existe
    os.makedirs(os.path.dirname(json_path), exist_ok=True)
    
    # Sauvegarder dans le fichier JSON
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(appareils, f, indent=4, ensure_ascii=False)
    
    print(f"200 appareils ont été générés et sauvegardés dans {json_path}")

if __name__ == "__main__":
    appareils = generate_appareils()
    save_to_json(appareils) 