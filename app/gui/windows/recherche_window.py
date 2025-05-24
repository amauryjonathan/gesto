import tkinter as tk
from tkinter import ttk, messagebox

class RechercheWindow(tk.Toplevel):
    def __init__(self, parent, gestionnaire):
        super().__init__(parent)
        self.title("Rechercher un appareil")
        self.geometry("400x300")
        self.gestionnaire = gestionnaire
        
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
        frame = ttk.Frame(self, padding="10")
        frame.pack(fill="both", expand=True)
        
        # Variables
        self.type_var = tk.StringVar(value="tous")
        self.marque_var = tk.StringVar()
        
        # Type d'appareil
        ttk.Label(frame, text="Type :").grid(row=0, column=0, sticky="w", pady=5)
        types = ["tous", "frigo", "four", "lave_linge", "lave_linge_sechant", "lave_vaisselle"]
        ttk.Combobox(frame, textvariable=self.type_var, values=types, width=15).grid(row=0, column=1, sticky="w", pady=5)
        
        # Marque
        ttk.Label(frame, text="Marque :").grid(row=1, column=0, sticky="w", pady=5)
        ttk.Entry(frame, textvariable=self.marque_var, width=20).grid(row=1, column=1, sticky="w", pady=5)
        
        # Boutons
        frame_boutons = ttk.Frame(frame)
        frame_boutons.grid(row=2, column=0, columnspan=2, pady=20)
        
        ttk.Button(frame_boutons, text="Rechercher", command=self.rechercher).pack(side="left", padx=5)
        ttk.Button(frame_boutons, text="Fermer", command=self.destroy).pack(side="left", padx=5)
        
    def rechercher(self):
        """Effectue la recherche selon les critères"""
        type_ = self.type_var.get()
        marque = self.marque_var.get().lower()
        
        # Récupérer tous les appareils
        appareils = self.gestionnaire.lister_appareils()
        
        # Filtrer selon les critères
        resultats = []
        for type_app, liste in appareils.items():
            if type_ == "tous" or type_app == type_:
                for appareil in liste:
                    if not marque or marque in appareil.marque.lower():
                        resultats.append((type_app, appareil))
        
        # Afficher les résultats
        if resultats:
            message = "Résultats de la recherche :\n\n"
            for type_app, appareil in resultats:
                message += f"{type_app} - {appareil.marque} {appareil.reference}\n"
            messagebox.showinfo("Résultats", message)
        else:
            messagebox.showinfo("Résultats", "Aucun appareil trouvé") 