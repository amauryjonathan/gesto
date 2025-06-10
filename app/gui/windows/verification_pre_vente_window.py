import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime

class VerificationPreVenteWindow(tk.Toplevel):
    def __init__(self, parent, appareil):
        super().__init__(parent)
        self.parent = parent
        self.appareil = appareil
        
        self.title(f"Vérification pré-vente - {appareil.identifiant}")
        self.geometry("800x600")
        
        # Créer ou récupérer la vérification existante
        self.verification = self.parent.gestionnaire.get_verification_pre_vente(appareil.identifiant)
        if not self.verification:
            self.verification = self.parent.gestionnaire.ajouter_verification_pre_vente(appareil.identifiant)
        
        self.create_widgets()
        
    def create_widgets(self):
        # Frame principal
        main_frame = ttk.Frame(self, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Vérifications visuelles
        visu_frame = ttk.LabelFrame(main_frame, text="Vérifications visuelles", padding="5")
        visu_frame.pack(fill=tk.X, pady=5)
        
        # Variables pour les cases à cocher
        self.commande_var = tk.BooleanVar(value=self.verification.commande_ok)
        self.verrou_var = tk.BooleanVar(value=self.verification.verrou_porte_ok)
        self.rotation_var = tk.BooleanVar(value=self.verification.rotation_tambour_ok)
        self.chauffe_var = tk.BooleanVar(value=self.verification.chauffe_ok)
        self.essorage_var = tk.BooleanVar(value=self.verification.essorage_ok)
        self.sechage_var = tk.BooleanVar(value=self.verification.sechage_ok)
        
        # Cases à cocher
        ttk.Checkbutton(visu_frame, text="Commande (bandeau)", variable=self.commande_var).pack(anchor=tk.W, pady=2)
        ttk.Checkbutton(visu_frame, text="Verrou de porte", variable=self.verrou_var).pack(anchor=tk.W, pady=2)
        ttk.Checkbutton(visu_frame, text="Rotation du tambour", variable=self.rotation_var).pack(anchor=tk.W, pady=2)
        ttk.Checkbutton(visu_frame, text="Chauffe", variable=self.chauffe_var).pack(anchor=tk.W, pady=2)
        ttk.Checkbutton(visu_frame, text="Essorage", variable=self.essorage_var).pack(anchor=tk.W, pady=2)
        ttk.Checkbutton(visu_frame, text="Séchage", variable=self.sechage_var).pack(anchor=tk.W, pady=2)
        
        # Programmes de test
        prog_frame = ttk.LabelFrame(main_frame, text="Programmes de test", padding="5")
        prog_frame.pack(fill=tk.X, pady=5)
        
        # Variables pour les programmes
        self.express_var = tk.StringVar(value=self.verification.programme_express)
        self.chauffe_var = tk.StringVar(value=self.verification.programme_chauffe)
        self.rotation_var = tk.StringVar(value=self.verification.programme_rotation)
        
        # Combobox pour les programmes
        ttk.Label(prog_frame, text="Programme Express:").pack(anchor=tk.W, pady=2)
        ttk.Combobox(prog_frame, textvariable=self.express_var, 
                    values=["non_testé", "en_cours", "réussi", "échoué"],
                    state="readonly").pack(anchor=tk.W, pady=2)
        
        ttk.Label(prog_frame, text="Programme Chauffe:").pack(anchor=tk.W, pady=2)
        ttk.Combobox(prog_frame, textvariable=self.chauffe_var,
                    values=["non_testé", "en_cours", "réussi", "échoué"],
                    state="readonly").pack(anchor=tk.W, pady=2)
        
        ttk.Label(prog_frame, text="Programme Rotation:").pack(anchor=tk.W, pady=2)
        ttk.Combobox(prog_frame, textvariable=self.rotation_var,
                    values=["non_testé", "en_cours", "réussi", "échoué"],
                    state="readonly").pack(anchor=tk.W, pady=2)
        
        # Observations
        obs_frame = ttk.LabelFrame(main_frame, text="Observations", padding="5")
        obs_frame.pack(fill=tk.BOTH, expand=True, pady=5)
        
        self.observations_text = tk.Text(obs_frame, height=10)
        self.observations_text.pack(fill=tk.BOTH, expand=True)
        self.observations_text.insert("1.0", "\n".join(f"{k}: {v}" for k, v in self.verification.observations.items()))
        
        # Boutons
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=tk.X, pady=10)
        
        ttk.Button(button_frame, text="Enregistrer", command=self.save_verification).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Valider", command=self.validate_verification).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Fermer", command=self.destroy).pack(side=tk.RIGHT, padx=5)
        
    def save_verification(self):
        # Mise à jour des vérifications visuelles
        self.verification.commande_ok = self.commande_var.get()
        self.verification.verrou_porte_ok = self.verrou_var.get()
        self.verification.rotation_tambour_ok = self.rotation_var.get()
        self.verification.chauffe_ok = self.chauffe_var.get()
        self.verification.essorage_ok = self.essorage_var.get()
        self.verification.sechage_ok = self.sechage_var.get()
        
        # Mise à jour des programmes
        self.verification.programme_express = self.express_var.get()
        self.verification.programme_chauffe = self.chauffe_var.get()
        self.verification.programme_rotation = self.rotation_var.get()
        
        # Mise à jour des observations
        observations_text = self.observations_text.get("1.0", tk.END).strip()
        for line in observations_text.split("\n"):
            if ":" in line:
                key, value = line.split(":", 1)
                key = key.strip()
                value = value.strip()
                if key in self.verification.observations:
                    self.verification.observations[key] = value
        
        # Sauvegarde
        self.parent.gestionnaire.mettre_a_jour_verification_pre_vente(
            self.appareil.identifiant,
            commande_ok=self.verification.commande_ok,
            verrou_porte_ok=self.verification.verrou_porte_ok,
            rotation_tambour_ok=self.verification.rotation_tambour_ok,
            chauffe_ok=self.verification.chauffe_ok,
            essorage_ok=self.verification.essorage_ok,
            sechage_ok=self.verification.sechage_ok,
            programme_express=self.verification.programme_express,
            programme_chauffe=self.verification.programme_chauffe,
            programme_rotation=self.verification.programme_rotation,
            observations=self.verification.observations
        )
        
        messagebox.showinfo("Succès", "Vérifications enregistrées avec succès!")
        
    def validate_verification(self):
        if not self.verification.est_complete():
            messagebox.showerror("Erreur", "Toutes les vérifications doivent être effectuées et réussies!")
            return
            
        self.verification.statut = "validé"
        self.parent.gestionnaire.mettre_a_jour_verification_pre_vente(
            self.appareil.identifiant,
            statut="validé"
        )
        
        messagebox.showinfo("Succès", "Vérifications validées avec succès!")
        self.destroy() 