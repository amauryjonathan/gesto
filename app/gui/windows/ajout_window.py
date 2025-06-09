import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
from tkcalendar import DateEntry
from app.models.appareil import Appareil
from app.models.frigo import Frigo
from app.models.four import Four
from app.models.lave_linge import LaveLinge
from app.models.lave_vaisselle import LaveVaisselle
from app.models.lave_linge_sechant import LaveLingeSechant
from app.models.seche_linge import SecheLinge

class AjoutWindow(tk.Toplevel):
    def __init__(self, parent, callback):
        super().__init__(parent)
        self.title("Ajouter un appareil")
        self.geometry("400x600")
        self.callback = callback
        
        # Liste des marques disponibles
        self.marques = [
            "Samsung", "LG", "Bosch", "Whirlpool", "Electrolux",
            "Beko", "Haier", "Siemens", "Candy", "Indesit"
        ]
        
        # Liste des types d'appareils
        self.types = [
            "frigo",
            "four",
            "lave_linge",
            "lave_vaisselle",
            "lave_linge_sechant"
        ]
        
        # Liste des cellules disponibles (A à R)
        self.cellules = [chr(i) for i in range(65, 83)]  # A à R
        
        # Liste des positions disponibles
        self.positions = ["A", "B"]
        
        # Rendre la fenêtre modale
        self.transient(parent)
        self.grab_set()
        
        self.create_widgets()
        
    def create_widgets(self):
        # Frame principal
        main_frame = ttk.Frame(self, padding="10")
        main_frame.pack(fill="both", expand=True)
        
        # Type d'appareil
        ttk.Label(main_frame, text="Type d'appareil:").pack(fill="x", pady=5)
        self.type_var = tk.StringVar()
        self.type_combo = ttk.Combobox(main_frame, textvariable=self.type_var, values=self.types, state="readonly")
        self.type_combo.pack(fill="x", pady=5)
        self.type_combo.bind("<<ComboboxSelected>>", self.on_type_change)
        
        # Marque
        ttk.Label(main_frame, text="Marque:").pack(fill="x", pady=5)
        self.marque_var = tk.StringVar()
        self.marque_combo = ttk.Combobox(main_frame, textvariable=self.marque_var, values=self.marques, state="readonly")
        self.marque_combo.pack(fill="x", pady=5)
        
        # Référence
        ttk.Label(main_frame, text="Référence:").pack(fill="x", pady=5)
        self.reference_var = tk.StringVar()
        self.reference_entry = ttk.Entry(main_frame, textvariable=self.reference_var)
        self.reference_entry.pack(fill="x", pady=5)
        
        # Numéro de série
        ttk.Label(main_frame, text="Numéro de série:").pack(fill="x", pady=5)
        self.numero_serie_var = tk.StringVar()
        self.numero_serie_entry = ttk.Entry(main_frame, textvariable=self.numero_serie_var)
        self.numero_serie_entry.pack(fill="x", pady=5)
        
        # Date d'arrivée avec calendrier
        ttk.Label(main_frame, text="Date d'arrivée:").pack(fill="x", pady=5)
        self.date_arrivee_cal = DateEntry(main_frame, width=12, background='darkblue',
                                        foreground='white', borderwidth=2, date_pattern='dd/mm/yyyy')
        self.date_arrivee_cal.pack(fill="x", pady=5)
        
        # Statut
        ttk.Label(main_frame, text="Statut:").pack(fill="x", pady=5)
        self.statut_var = tk.StringVar(value="en stock")
        self.statut_combo = ttk.Combobox(main_frame, textvariable=self.statut_var, 
                                       values=["en stock", "en réparation", "réparé", "livré"], 
                                       state="readonly")
        self.statut_combo.pack(fill="x", pady=5)
        
        # Caractéristique spécifique
        ttk.Label(main_frame, text="Caractéristique spécifique:").pack(fill="x", pady=5)
        self.specifique_var = tk.StringVar()
        self.specifique_entry = ttk.Entry(main_frame, textvariable=self.specifique_var)
        self.specifique_entry.pack(fill="x", pady=5)
        
        # Capacité de séchage (initialement caché)
        self.capacite_sechage_frame = ttk.Frame(main_frame)
        ttk.Label(self.capacite_sechage_frame, text="Cap. séchage (kg):").pack(side="left")
        self.capacite_sechage_var = tk.StringVar()
        self.capacite_sechage_entry = ttk.Entry(self.capacite_sechage_frame, textvariable=self.capacite_sechage_var, width=10)
        self.capacite_sechage_entry.pack(side="left", padx=5)
        
        # Frame pour la localisation
        localisation_frame = ttk.LabelFrame(main_frame, text="Localisation", padding="5")
        localisation_frame.pack(fill="x", pady=10)
        
        # Cellule
        ttk.Label(localisation_frame, text="Cellule:").grid(row=0, column=0, sticky="w", padx=5, pady=5)
        self.cellule_var = tk.StringVar()
        self.cellule_combo = ttk.Combobox(localisation_frame, textvariable=self.cellule_var, 
                                        values=self.cellules, state="readonly", width=5)
        self.cellule_combo.grid(row=0, column=1, sticky="w", padx=5, pady=5)
        
        # Emplacement
        ttk.Label(localisation_frame, text="Emplacement:").grid(row=0, column=2, sticky="w", padx=5, pady=5)
        self.emplacement_var = tk.StringVar()
        self.emplacement_spinbox = ttk.Spinbox(localisation_frame, from_=1, to=9, 
                                             textvariable=self.emplacement_var, width=5)
        self.emplacement_spinbox.grid(row=0, column=3, sticky="w", padx=5, pady=5)
        
        # Position
        ttk.Label(localisation_frame, text="Position:").grid(row=0, column=4, sticky="w", padx=5, pady=5)
        self.position_var = tk.StringVar()
        self.position_combo = ttk.Combobox(localisation_frame, textvariable=self.position_var, 
                                         values=self.positions, state="readonly", width=5)
        self.position_combo.grid(row=0, column=5, sticky="w", padx=5, pady=5)
        
        # Boutons
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill="x", pady=20)
        
        ttk.Button(button_frame, text="Ajouter", command=self.ajouter_appareil).pack(side="left", padx=5)
        ttk.Button(button_frame, text="Annuler", command=self.destroy).pack(side="right", padx=5)
        
    def on_type_change(self, event=None):
        """Gère le changement de type d'appareil"""
        type_app = self.type_var.get()
        
        # Afficher/masquer le champ de capacité de séchage
        if type_app == "lave_linge_sechant":
            self.capacite_sechage_frame.pack(fill="x", pady=5)
        else:
            self.capacite_sechage_frame.pack_forget()
            
        # Mettre à jour le label de la caractéristique spécifique
        if type_app == "frigo":
            ttk.Label(self.specifique_entry.master, text="Température (°C):").pack(fill="x", pady=5)
        elif type_app in ["lave_linge", "lave_vaisselle"]:
            ttk.Label(self.specifique_entry.master, text="Capacité (kg):").pack(fill="x", pady=5)
        elif type_app == "four":
            ttk.Label(self.specifique_entry.master, text="Volume (L):").pack(fill="x", pady=5)
            
    def verifier_appareil_existant(self, type_app, marque, reference):
        """Vérifie si l'appareil existe déjà"""
        appareil_id = f"{type_app}_{marque}_{reference}"
        return appareil_id in self.master.appareils_dict
        
    def ajouter_appareil(self):
        """Ajoute un nouvel appareil"""
        # Récupération des valeurs
        type_app = self.type_var.get()
        marque = self.marque_var.get()
        reference = self.reference_var.get()
        numero_serie = self.numero_serie_var.get()
        date_arrivee = self.date_arrivee_cal.get_date().strftime("%d/%m/%Y")
        statut = self.statut_var.get()
        cellule = self.cellule_var.get()
        emplacement = self.emplacement_var.get()
        position = self.position_var.get()
        
        # Vérification des champs obligatoires
        if not all([type_app, marque, reference, numero_serie, date_arrivee]):
            messagebox.showerror("Erreur", "Tous les champs sont obligatoires!")
            return
            
        # Vérification si l'appareil existe déjà
        if self.verifier_appareil_existant(type_app, marque, reference):
            messagebox.showerror("Erreur", "Cet appareil existe déjà dans la base!")
            return
            
        try:
            # Création de l'appareil selon son type
            if type_app == "frigo":
                temperature = float(self.specifique_var.get())
                appareil = Frigo(f"F{len(self.master.gestionnaire.appareils['frigo'])+1:03d}", marque, reference, 
                               numero_serie, date_arrivee, statut, temperature)
            elif type_app == "four":
                volume = float(self.specifique_var.get())
                appareil = Four(f"O{len(self.master.gestionnaire.appareils['four'])+1:03d}", marque, reference, 
                              numero_serie, date_arrivee, statut, volume)
            elif type_app == "lave_linge":
                capacite = float(self.specifique_var.get())
                appareil = LaveLinge(f"L{len(self.master.gestionnaire.appareils['lave_linge'])+1:03d}", marque, reference, 
                                   numero_serie, date_arrivee, statut, capacite)
            elif type_app == "lave_vaisselle":
                capacite = float(self.specifique_var.get())
                appareil = LaveVaisselle(f"LV{len(self.master.gestionnaire.appareils['lave_vaisselle'])+1:03d}", marque, reference, 
                                       numero_serie, date_arrivee, statut, capacite)
            elif type_app == "lave_linge_sechant":
                capacite = float(self.specifique_var.get())
                capacite_sechage = float(self.capacite_sechage_var.get())
                appareil = LaveLingeSechant(f"LS{len(self.master.gestionnaire.appareils['lave_linge_sechant'])+1:03d}", marque, reference, 
                                          numero_serie, date_arrivee, statut, capacite, capacite_sechage)
            
            # Définir la localisation si elle est fournie
            if cellule and emplacement and position:
                try:
                    appareil.set_localisation(cellule, int(emplacement), position)
                except ValueError as e:
                    messagebox.showerror("Erreur", str(e))
                    return
            
            # Appel du gestionnaire pour ajouter l'appareil
            try:
                self.master.gestionnaire.ajouter_appareil(appareil)
            except ValueError as e:
                messagebox.showerror("Erreur", str(e))
                return
            self.master.refresh_liste()
            self.destroy()
            
        except ValueError:
            messagebox.showerror("Erreur", "Les valeurs numériques doivent être des nombres valides!") 