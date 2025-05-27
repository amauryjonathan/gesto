import tkinter as tk
from tkinter import ttk

class DetailsWindow(tk.Toplevel):
    def __init__(self, parent, appareil, metadonnees=None):
        super().__init__(parent)
        self.title("Détails de l'appareil")
        self.geometry("400x600")
        self.appareil = appareil
        self.metadonnees = metadonnees or {}
        
        # Rendre la fenêtre modale
        self.transient(parent)
        self.grab_set()
        
        self.create_widgets()
        
    def create_widgets(self):
        # Frame principal
        main_frame = ttk.Frame(self, padding="10")
        main_frame.pack(fill="both", expand=True)
        
        # Informations de base
        base_frame = ttk.LabelFrame(main_frame, text="Informations de base", padding="5")
        base_frame.pack(fill="x", pady=5)
        
        # Type
        ttk.Label(base_frame, text="Type:").grid(row=0, column=0, sticky="w", pady=2)
        ttk.Label(base_frame, text=self.appareil.get_type()).grid(row=0, column=1, sticky="w", pady=2)
        
        # Marque
        ttk.Label(base_frame, text="Marque:").grid(row=1, column=0, sticky="w", pady=2)
        ttk.Label(base_frame, text=self.appareil.marque).grid(row=1, column=1, sticky="w", pady=2)
        
        # Référence
        ttk.Label(base_frame, text="Référence:").grid(row=2, column=0, sticky="w", pady=2)
        ttk.Label(base_frame, text=self.appareil.reference).grid(row=2, column=1, sticky="w", pady=2)
        
        # Numéro de série
        ttk.Label(base_frame, text="Numéro de série:").grid(row=3, column=0, sticky="w", pady=2)
        ttk.Label(base_frame, text=self.appareil.numero_serie).grid(row=3, column=1, sticky="w", pady=2)
        
        # Date d'arrivée
        ttk.Label(base_frame, text="Date d'arrivée:").grid(row=4, column=0, sticky="w", pady=2)
        ttk.Label(base_frame, text=self.appareil.date_arrivee).grid(row=4, column=1, sticky="w", pady=2)
        
        # Statut
        ttk.Label(base_frame, text="Statut:").grid(row=5, column=0, sticky="w", pady=2)
        ttk.Label(base_frame, text=self.appareil.statut).grid(row=5, column=1, sticky="w", pady=2)
        
        # Caractéristiques spécifiques
        spec_frame = ttk.LabelFrame(main_frame, text="Caractéristiques spécifiques", padding="5")
        spec_frame.pack(fill="x", pady=5)
        
        if hasattr(self.appareil, 'temperature'):
            ttk.Label(spec_frame, text="Température:").grid(row=0, column=0, sticky="w", pady=2)
            ttk.Label(spec_frame, text=f"{self.appareil.temperature}°C").grid(row=0, column=1, sticky="w", pady=2)
        elif hasattr(self.appareil, 'capacite'):
            ttk.Label(spec_frame, text="Capacité:").grid(row=0, column=0, sticky="w", pady=2)
            ttk.Label(spec_frame, text=f"{self.appareil.capacite}kg").grid(row=0, column=1, sticky="w", pady=2)
        elif hasattr(self.appareil, 'capacite_sechage'):
            ttk.Label(spec_frame, text="Capacité de séchage:").grid(row=0, column=0, sticky="w", pady=2)
            ttk.Label(spec_frame, text=f"{self.appareil.capacite_sechage}kg").grid(row=0, column=1, sticky="w", pady=2)
        
        # Localisation
        loc_frame = ttk.LabelFrame(main_frame, text="Localisation", padding="5")
        loc_frame.pack(fill="x", pady=5)
        
        localisation = self.appareil.get_localisation()
        ttk.Label(loc_frame, text="Position:").grid(row=0, column=0, sticky="w", pady=2)
        ttk.Label(loc_frame, text=localisation).grid(row=0, column=1, sticky="w", pady=2)
        
        # Métadonnées
        if self.metadonnees:
            meta_frame = ttk.LabelFrame(main_frame, text="Métadonnées", padding="5")
            meta_frame.pack(fill="x", pady=5)
            
            row = 0
            for key, value in self.metadonnees.items():
                if value is not None:
                    ttk.Label(meta_frame, text=f"{key}:").grid(row=row, column=0, sticky="w", pady=2)
                    ttk.Label(meta_frame, text=str(value)).grid(row=row, column=1, sticky="w", pady=2)
                    row += 1
        
        # Informations de réparation
        if self.metadonnees:
            rep_frame = ttk.LabelFrame(main_frame, text="Informations de réparation", padding="5")
            rep_frame.pack(fill="x", pady=5)
            
            # Date de prise en charge
            if self.metadonnees.get('date_prise_en_charge'):
                ttk.Label(rep_frame, text="Date de prise en charge:").grid(row=0, column=0, sticky="w", pady=2)
                ttk.Label(rep_frame, text=self.metadonnees['date_prise_en_charge']).grid(row=0, column=1, sticky="w", pady=2)
            
            # Panne détectée
            if self.metadonnees.get('panne_detectee'):
                ttk.Label(rep_frame, text="Panne détectée:").grid(row=1, column=0, sticky="w", pady=2)
                ttk.Label(rep_frame, text=self.metadonnees['panne_detectee']).grid(row=1, column=1, sticky="w", pady=2)
            
            # Statut de réparation
            if self.metadonnees.get('statut_reparation'):
                ttk.Label(rep_frame, text="Statut de réparation:").grid(row=2, column=0, sticky="w", pady=2)
                ttk.Label(rep_frame, text=self.metadonnees['statut_reparation']).grid(row=2, column=1, sticky="w", pady=2)
            
            # Technicien
            if self.metadonnees.get('technicien'):
                ttk.Label(rep_frame, text="Technicien:").grid(row=3, column=0, sticky="w", pady=2)
                ttk.Label(rep_frame, text=self.metadonnees['technicien']).grid(row=3, column=1, sticky="w", pady=2)
            
            # Notes
            if self.metadonnees.get('notes'):
                ttk.Label(rep_frame, text="Notes:").grid(row=4, column=0, sticky="w", pady=2)
                ttk.Label(rep_frame, text=self.metadonnees['notes']).grid(row=4, column=1, sticky="w", pady=2)
        
        # Bouton Fermer
        ttk.Button(main_frame, text="Fermer", command=self.destroy).pack(pady=20)
        
        # Centrer la fenêtre
        self.update_idletasks()
        width = self.winfo_width()
        height = self.winfo_height()
        x = (self.winfo_screenwidth() // 2) - (width // 2)
        y = (self.winfo_screenheight() // 2) - (height // 2)
        self.geometry(f'{width}x{height}+{x}+{y}') 