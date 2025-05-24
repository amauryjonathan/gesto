import tkinter as tk
from tkinter import ttk, messagebox
from app.models.frigo import Frigo
from app.models.four import Four
from app.models.lave_linge import LaveLinge
from app.models.lave_vaisselle import LaveVaisselle
from app.models.lave_linge_sechant import LaveLingeSechant

class AjoutWindow(tk.Toplevel):
    def __init__(self, parent, callback_ajout):
        super().__init__(parent)
        self.title("Ajouter un appareil")
        self.geometry("400x300")
        self.callback_ajout = callback_ajout
        
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
        self.type_var = tk.StringVar(value="frigo")
        self.marque_var = tk.StringVar()
        self.ref_var = tk.StringVar()
        self.spec_var = tk.StringVar()
        self.spec2_var = tk.StringVar()
        
        # Type d'appareil
        ttk.Label(frame, text="Type :").grid(row=0, column=0, sticky="w", pady=5)
        types = ["frigo", "four", "lave_linge", "lave_linge_sechant", "lave_vaisselle"]
        ttk.Combobox(frame, textvariable=self.type_var, values=types, width=15).grid(row=0, column=1, sticky="w", pady=5)
        
        # Marque
        ttk.Label(frame, text="Marque :").grid(row=1, column=0, sticky="w", pady=5)
        ttk.Entry(frame, textvariable=self.marque_var, width=20).grid(row=1, column=1, sticky="w", pady=5)
        
        # Référence
        ttk.Label(frame, text="Référence :").grid(row=2, column=0, sticky="w", pady=5)
        ttk.Entry(frame, textvariable=self.ref_var, width=20).grid(row=2, column=1, sticky="w", pady=5)
        
        # Spécifique
        ttk.Label(frame, text="Spécifique :").grid(row=3, column=0, sticky="w", pady=5)
        ttk.Entry(frame, textvariable=self.spec_var, width=20).grid(row=3, column=1, sticky="w", pady=5)
        
        # Capacité de séchage (initialement caché)
        self.spec2_label = ttk.Label(frame, text="Cap. séchage :")
        self.spec2_entry = ttk.Entry(frame, textvariable=self.spec2_var, width=20)
        
        # Boutons
        frame_boutons = ttk.Frame(frame)
        frame_boutons.grid(row=5, column=0, columnspan=2, pady=20)
        
        ttk.Button(frame_boutons, text="Ajouter", command=self.ajouter_appareil).pack(side="left", padx=5)
        ttk.Button(frame_boutons, text="Annuler", command=self.destroy).pack(side="left", padx=5)
        
        # Bind event pour afficher/masquer le champ de capacité de séchage
        self.type_var.trace_add("write", self.on_type_change)
        
    def on_type_change(self, *args):
        """Affiche ou masque le champ de capacité de séchage selon le type d'appareil"""
        if self.type_var.get() == "lave_linge_sechant":
            self.spec2_label.grid(row=4, column=0, sticky="w", pady=5)
            self.spec2_entry.grid(row=4, column=1, sticky="w", pady=5)
        else:
            self.spec2_label.grid_remove()
            self.spec2_entry.grid_remove()
            
    def ajouter_appareil(self):
        """Crée et ajoute un nouvel appareil"""
        type_ = self.type_var.get()
        marque = self.marque_var.get()
        ref = self.ref_var.get()
        spec = self.spec_var.get()
        spec2 = self.spec2_var.get()
        
        if not marque or not ref:
            messagebox.showerror("Erreur", "Marque et référence obligatoires")
            return
            
        try:
            if type_ == "frigo":
                temp = float(spec) if spec else 4.0
                appareil = Frigo(marque, ref, temp)
            elif type_ == "four":
                temp = float(spec) if spec else 0.0
                appareil = Four(marque, ref, temp)
            elif type_ == "lave_linge":
                cap = float(spec) if spec else 7.0
                appareil = LaveLinge(marque, ref, cap)
            elif type_ == "lave_linge_sechant":
                cap = float(spec) if spec else 8.0
                cap_sechage = float(spec2) if spec2 else 5.0
                appareil = LaveLingeSechant(marque, ref, cap, cap_sechage)
            elif type_ == "lave_vaisselle":
                cap = int(spec) if spec else 12
                appareil = LaveVaisselle(marque, ref, cap)
            else:
                messagebox.showerror("Erreur", "Type inconnu")
                return
                
            # Appel du callback pour informer la fenêtre principale
            self.callback_ajout(appareil)
            
            # Fermer la fenêtre
            self.destroy()
            
        except ValueError as e:
            messagebox.showerror("Erreur", str(e)) 