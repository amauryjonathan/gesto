import tkinter as tk
from tkinter import ttk, messagebox
from app.models.frigo import Frigo
from app.models.four import Four
from app.models.lave_linge import LaveLinge
from app.models.lave_vaisselle import LaveVaisselle
from app.models.lave_linge_sechant import LaveLingeSechant

class AjoutFrame(ttk.Frame):
    def __init__(self, parent, callback_ajout):
        super().__init__(parent)
        self.callback_ajout = callback_ajout
        self.create_widgets()
        
    def create_widgets(self):
        # Variables
        self.type_var = tk.StringVar(value="frigo")
        self.marque_var = tk.StringVar()
        self.ref_var = tk.StringVar()
        self.spec_var = tk.StringVar()
        self.spec2_var = tk.StringVar()
        
        # Frame principal
        frame = ttk.LabelFrame(self, text="Ajouter un appareil")
        frame.pack(fill="x", padx=10, pady=5)
        
        # Type d'appareil
        ttk.Label(frame, text="Type :").pack(side="left", padx=5)
        types = ["frigo", "four", "lave_linge", "lave_linge_sechant", "lave_vaisselle"]
        ttk.Combobox(frame, textvariable=self.type_var, values=types, width=15).pack(side="left")
        
        # Marque
        ttk.Label(frame, text="Marque :").pack(side="left", padx=5)
        ttk.Entry(frame, textvariable=self.marque_var, width=12).pack(side="left")
        
        # Référence
        ttk.Label(frame, text="Référence :").pack(side="left", padx=5)
        ttk.Entry(frame, textvariable=self.ref_var, width=12).pack(side="left")
        
        # Spécifique
        ttk.Label(frame, text="Spécifique :").pack(side="left", padx=5)
        ttk.Entry(frame, textvariable=self.spec_var, width=10).pack(side="left")
        
        # Capacité de séchage (initialement caché)
        ttk.Label(frame, text="Cap. séchage :").pack(side="left", padx=5)
        self.spec2_entry = ttk.Entry(frame, textvariable=self.spec2_var, width=10)
        self.spec2_entry.pack(side="left")
        
        # Bouton d'ajout
        ttk.Button(frame, text="Ajouter", command=self.ajouter_appareil).pack(side="left", padx=5)
        
        # Bind event pour afficher/masquer le champ de capacité de séchage
        self.type_var.trace_add("write", self.on_type_change)
        
    def on_type_change(self, *args):
        """Affiche ou masque le champ de capacité de séchage selon le type d'appareil"""
        if self.type_var.get() == "lave_linge_sechant":
            self.spec2_entry.pack(side="left")
        else:
            self.spec2_entry.pack_forget()
            
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
            
            # Réinitialisation des champs
            self.marque_var.set("")
            self.ref_var.set("")
            self.spec_var.set("")
            self.spec2_var.set("")
            
        except ValueError as e:
            messagebox.showerror("Erreur", str(e)) 