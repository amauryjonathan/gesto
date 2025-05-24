import tkinter as tk
from tkinter import ttk

class ListeFrame(ttk.Frame):
    def __init__(self, parent, callback_selection):
        super().__init__(parent)
        self.callback_selection = callback_selection
        self.create_widgets()
        
    def create_widgets(self):
        # Frame principal
        frame = ttk.LabelFrame(self, text="Liste des appareils")
        frame.pack(fill="both", expand=True, padx=10, pady=5)
        
        # Création du Treeview pour afficher les appareils
        self.tree = ttk.Treeview(frame, columns=("Type", "Marque", "Référence", "Spécifique"), show="headings")
        
        # Configuration des colonnes
        self.tree.heading("Type", text="Type")
        self.tree.heading("Marque", text="Marque")
        self.tree.heading("Référence", text="Référence")
        self.tree.heading("Spécifique", text="Spécifique")
        
        # Configuration de la largeur des colonnes
        self.tree.column("Type", width=100)
        self.tree.column("Marque", width=100)
        self.tree.column("Référence", width=100)
        self.tree.column("Spécifique", width=100)
        
        # Ajout d'une scrollbar
        scrollbar = ttk.Scrollbar(frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        # Placement des widgets
        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Bind du double-clic pour voir les détails
        self.tree.bind("<Double-1>", self.on_double_click)
        
    def refresh_liste(self, appareils):
        """Rafraîchit la liste des appareils"""
        # Effacer la liste actuelle
        for item in self.tree.get_children():
            self.tree.delete(item)
            
        # Ajouter les nouveaux appareils
        for type_app, liste in appareils.items():
            for appareil in liste:
                # Déterminer la valeur spécifique selon le type d'appareil
                spec = ""
                if hasattr(appareil, 'temperature'):
                    spec = f"{appareil.temperature}°C"
                elif hasattr(appareil, 'capacite'):
                    spec = f"{appareil.capacite}kg"
                elif hasattr(appareil, 'capacite_sechage'):
                    spec = f"{appareil.capacite_sechage}kg"
                    
                # Ajouter l'appareil à la liste
                self.tree.insert("", "end", values=(
                    type_app,
                    appareil.marque,
                    appareil.reference,
                    spec
                ), tags=(appareil,))
                
    def on_double_click(self, event):
        """Gère le double-clic sur un appareil"""
        item = self.tree.selection()[0]
        appareil = self.tree.item(item)["tags"][0]
        self.callback_selection(appareil) 