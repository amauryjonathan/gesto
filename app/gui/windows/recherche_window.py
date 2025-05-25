import tkinter as tk
from tkinter import ttk, messagebox

class RechercheWindow(tk.Toplevel):
    def __init__(self, parent, gestionnaire):
        super().__init__(parent)
        self.title("Rechercher un appareil")
        self.geometry("400x300")
        self.gestionnaire = gestionnaire
        
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
        
        # Rendre la fenêtre modale
        self.transient(parent)
        self.grab_set()
        
        self.create_widgets()
        
        # Centrer la fenêtre
        self.update_idletasks()
        width = self.winfo_width()
        height = self.winfo_height()
        x = (self.winfo_screenwidth() // 2) - (width // 2)
        y = (self.winfo_screenheight() // 2) - (height // 2)
        self.geometry(f'{width}x{height}+{x}+{y}')
        
    def create_widgets(self):
        # Frame principal
        main_frame = ttk.Frame(self, padding="10")
        main_frame.pack(fill="both", expand=True)
        
        # Type d'appareil
        ttk.Label(main_frame, text="Type d'appareil:").pack(fill="x", pady=5)
        self.type_var = tk.StringVar()
        self.type_combo = ttk.Combobox(main_frame, textvariable=self.type_var, values=self.types, state="readonly")
        self.type_combo.pack(fill="x", pady=5)
        
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
        
        # Boutons
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill="x", pady=20)
        
        ttk.Button(button_frame, text="Rechercher", command=self.rechercher).pack(side="left", padx=5)
        ttk.Button(button_frame, text="Fermer", command=self.destroy).pack(side="right", padx=5)
        
    def rechercher(self):
        """Effectue la recherche d'appareils"""
        type_app = self.type_var.get()
        marque = self.marque_var.get()
        reference = self.reference_var.get()
        
        # Récupérer tous les appareils
        appareils = self.gestionnaire.lister_appareils()
        
        # Filtrer les résultats
        resultats = []
        for type_, liste in appareils.items():
            if type_app and type_ != type_app:
                continue
                
            for appareil in liste:
                if marque and appareil.marque != marque:
                    continue
                if reference and appareil.reference != reference:
                    continue
                    
                resultats.append(appareil)
        
        # Afficher les résultats
        if resultats:
            message = "Appareils trouvés:\n\n"
            for appareil in resultats:
                message += f"Type: {appareil.get_type()}\n"
                message += f"Marque: {appareil.marque}\n"
                message += f"Référence: {appareil.reference}\n"
                message += f"Numéro de série: {appareil.numero_serie}\n"
                message += f"Date d'arrivée: {appareil.date_arrivee}\n"
                message += f"Statut: {appareil.statut}\n"
                if hasattr(appareil, 'temperature'):
                    message += f"Température: {appareil.temperature}°C\n"
                elif hasattr(appareil, 'capacite'):
                    message += f"Capacité: {appareil.capacite}kg\n"
                elif hasattr(appareil, 'capacite_sechage'):
                    message += f"Capacité séchage: {appareil.capacite_sechage}kg\n"
                message += "\n"
            
            messagebox.showinfo("Résultats", message)
        else:
            messagebox.showinfo("Résultats", "Aucun appareil trouvé.") 