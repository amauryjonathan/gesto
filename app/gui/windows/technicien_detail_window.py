import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime

class DetailWindow(tk.Toplevel):
    def __init__(self, master, appareil):
        super().__init__(master)
        self.master = master
        self.appareil = appareil
        
        self.title(f"Détails de l'appareil {appareil.identifiant}")
        self.geometry("600x800")
        
        # Création des variables
        self.marque_var = tk.StringVar(value=appareil.marque)
        self.reference_var = tk.StringVar(value=appareil.reference)
        self.numero_serie_var = tk.StringVar(value=appareil.numero_serie)
        self.date_arrivee_var = tk.StringVar(value=appareil.date_arrivee)
        self.statut_var = tk.StringVar(value=appareil.statut)
        self.cellule_var = tk.StringVar(value=appareil.cellule if appareil.cellule else "")
        self.emplacement_var = tk.StringVar(value=str(appareil.emplacement) if appareil.emplacement else "")
        self.position_var = tk.StringVar(value=appareil.position if appareil.position else "")
        
        # Création des widgets
        self.create_widgets()
        
    def create_widgets(self):
        # Frame principal
        main_frame = ttk.Frame(self, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Informations de base
        ttk.Label(main_frame, text="Informations de base", font=('Helvetica', 12, 'bold')).grid(row=0, column=0, columnspan=2, pady=10)
        
        # Identifiant (non modifiable)
        ttk.Label(main_frame, text="Identifiant:").grid(row=1, column=0, sticky=tk.W, pady=5)
        ttk.Label(main_frame, text=self.appareil.identifiant).grid(row=1, column=1, sticky=tk.W, pady=5)
        
        # Marque
        ttk.Label(main_frame, text="Marque:").grid(row=2, column=0, sticky=tk.W, pady=5)
        ttk.Entry(main_frame, textvariable=self.marque_var).grid(row=2, column=1, sticky=tk.W, pady=5)
        
        # Référence
        ttk.Label(main_frame, text="Référence:").grid(row=3, column=0, sticky=tk.W, pady=5)
        ttk.Entry(main_frame, textvariable=self.reference_var).grid(row=3, column=1, sticky=tk.W, pady=5)
        
        # Numéro de série
        ttk.Label(main_frame, text="Numéro de série:").grid(row=4, column=0, sticky=tk.W, pady=5)
        ttk.Entry(main_frame, textvariable=self.numero_serie_var).grid(row=4, column=1, sticky=tk.W, pady=5)
        
        # Date d'arrivée
        ttk.Label(main_frame, text="Date d'arrivée:").grid(row=5, column=0, sticky=tk.W, pady=5)
        ttk.Entry(main_frame, textvariable=self.date_arrivee_var).grid(row=5, column=1, sticky=tk.W, pady=5)
        
        # Statut
        ttk.Label(main_frame, text="Statut:").grid(row=6, column=0, sticky=tk.W, pady=5)
        statuts = ["à réparer", "diagnostiquer", "réparer"]
        ttk.Combobox(main_frame, textvariable=self.statut_var, values=statuts).grid(row=6, column=1, sticky=tk.W, pady=5)
        
        # Localisation
        ttk.Label(main_frame, text="Localisation", font=('Helvetica', 12, 'bold')).grid(row=7, column=0, columnspan=2, pady=10)
        
        # Cellule
        ttk.Label(main_frame, text="Cellule:").grid(row=8, column=0, sticky=tk.W, pady=5)
        cellules = [chr(i) for i in range(65, 83)]  # A à R
        ttk.Combobox(main_frame, textvariable=self.cellule_var, values=cellules).grid(row=8, column=1, sticky=tk.W, pady=5)
        
        # Emplacement
        ttk.Label(main_frame, text="Emplacement:").grid(row=9, column=0, sticky=tk.W, pady=5)
        emplacements = list(range(1, 10))  # 1 à 9
        ttk.Combobox(main_frame, textvariable=self.emplacement_var, values=emplacements).grid(row=9, column=1, sticky=tk.W, pady=5)
        
        # Position
        ttk.Label(main_frame, text="Position:").grid(row=10, column=0, sticky=tk.W, pady=5)
        positions = ["A", "B"]
        ttk.Combobox(main_frame, textvariable=self.position_var, values=positions).grid(row=10, column=1, sticky=tk.W, pady=5)
        
        # Caractéristiques spécifiques
        ttk.Label(main_frame, text="Caractéristiques spécifiques", font=('Helvetica', 12, 'bold')).grid(row=11, column=0, columnspan=2, pady=10)
        
        # Ajouter les caractéristiques spécifiques selon le type d'appareil
        row = 12
        if hasattr(self.appareil, 'temperature'):
            self.temperature_var = tk.StringVar(value=str(self.appareil.temperature))
            ttk.Label(main_frame, text="Température (°C):").grid(row=row, column=0, sticky=tk.W, pady=5)
            ttk.Entry(main_frame, textvariable=self.temperature_var).grid(row=row, column=1, sticky=tk.W, pady=5)
            row += 1
        elif hasattr(self.appareil, 'volume'):
            self.volume_var = tk.StringVar(value=str(self.appareil.volume))
            ttk.Label(main_frame, text="Volume (L):").grid(row=row, column=0, sticky=tk.W, pady=5)
            ttk.Entry(main_frame, textvariable=self.volume_var).grid(row=row, column=1, sticky=tk.W, pady=5)
            row += 1
        elif hasattr(self.appareil, 'capacite'):
            self.capacite_var = tk.StringVar(value=str(self.appareil.capacite))
            ttk.Label(main_frame, text="Capacité (kg):").grid(row=row, column=0, sticky=tk.W, pady=5)
            ttk.Entry(main_frame, textvariable=self.capacite_var).grid(row=row, column=1, sticky=tk.W, pady=5)
            row += 1
            if hasattr(self.appareil, 'capacite_sechage'):
                self.capacite_sechage_var = tk.StringVar(value=str(self.appareil.capacite_sechage))
                ttk.Label(main_frame, text="Capacité séchage (kg):").grid(row=row, column=0, sticky=tk.W, pady=5)
                ttk.Entry(main_frame, textvariable=self.capacite_sechage_var).grid(row=row, column=1, sticky=tk.W, pady=5)
                row += 1
        
        # Boutons
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=row, column=0, columnspan=2, pady=20)
        
        ttk.Button(button_frame, text="Enregistrer", command=self.save_changes).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Annuler", command=self.destroy).pack(side=tk.LEFT, padx=5)
        
    def save_changes(self):
        try:
            # Mise à jour des informations de base
            self.appareil.marque = self.marque_var.get()
            self.appareil.reference = self.reference_var.get()
            self.appareil.numero_serie = self.numero_serie_var.get()
            self.appareil.date_arrivee = self.date_arrivee_var.get()
            self.appareil.statut = self.statut_var.get()
            
            # Mise à jour de la localisation
            cellule = self.cellule_var.get()
            emplacement = self.emplacement_var.get()
            position = self.position_var.get()
            
            if cellule and emplacement and position:
                try:
                    self.appareil.set_localisation(cellule, int(emplacement), position)
                except ValueError as e:
                    messagebox.showerror("Erreur", str(e))
                    return
            
            # Mise à jour des caractéristiques spécifiques
            if hasattr(self.appareil, 'temperature'):
                self.appareil.temperature = float(self.temperature_var.get())
            elif hasattr(self.appareil, 'volume'):
                self.appareil.volume = float(self.volume_var.get())
            elif hasattr(self.appareil, 'capacite'):
                self.appareil.capacite = float(self.capacite_var.get())
                if hasattr(self.appareil, 'capacite_sechage'):
                    self.appareil.capacite_sechage = float(self.capacite_sechage_var.get())
            
            # Sauvegarder les modifications
            self.master.gestionnaire.sauvegarder_appareils()
            self.master.refresh_liste()
            messagebox.showinfo("Succès", "Les modifications ont été enregistrées avec succès!")
            self.destroy()
            
        except ValueError as e:
            messagebox.showerror("Erreur", "Veuillez vérifier les valeurs numériques!") 