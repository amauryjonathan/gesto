import json
import os
import shutil
import tkinter as tk
from tkinter import messagebox

def reset_database():
    """Réinitialise la base de données des appareils"""
    # Chemins des fichiers
    root_dir = os.path.dirname(__file__)
    old_json_path = os.path.join(root_dir, "appareils.json")
    new_json_path = os.path.join(root_dir, "app", "data", "appareils.json")
    
    # Créer le dossier data s'il n'existe pas
    os.makedirs(os.path.dirname(new_json_path), exist_ok=True)
    
    # Structure de base du fichier JSON
    base_structure = {
        "frigo": [],
        "four": [],
        "lave_linge": [],
        "lave_vaisselle": [],
        "lave_linge_sechant": []
    }
    
    # Créer une fenêtre temporaire pour les boîtes de dialogue
    root = tk.Tk()
    root.withdraw()  # Cacher la fenêtre principale
    
    # Demander confirmation
    if messagebox.askyesno("Confirmation", 
                          "Êtes-vous sûr de vouloir réinitialiser la base de données ?\n"
                          "Toutes les données seront supprimées."):
        try:
            # Si l'ancien fichier existe à la racine, le déplacer
            if os.path.exists(old_json_path):
                print("Déplacement de l'ancien fichier vers app/data/...")
                shutil.move(old_json_path, new_json_path)
                print("Fichier déplacé avec succès.")
            
            # Supprimer le fichier s'il existe (ancien ou nouveau emplacement)
            if os.path.exists(new_json_path):
                os.remove(new_json_path)
                print("Ancien fichier supprimé.")
            
            # Créer le nouveau fichier avec la structure de base
            with open(new_json_path, 'w', encoding='utf-8') as f:
                json.dump(base_structure, f, indent=4, ensure_ascii=False)
            
            print("Base de données réinitialisée avec succès!")
            messagebox.showinfo("Succès", "La base de données a été réinitialisée avec succès!")
            
        except Exception as e:
            print(f"Erreur lors de la réinitialisation: {e}")
            messagebox.showerror("Erreur", f"Une erreur est survenue: {e}")
    else:
        print("Opération annulée par l'utilisateur.")
        messagebox.showinfo("Annulation", "La réinitialisation a été annulée.")
    
    root.destroy()

if __name__ == "__main__":
    reset_database() 