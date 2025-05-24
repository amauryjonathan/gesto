import tkinter as tk
from tkinter import ttk

class DetailsWindow(tk.Toplevel):
    def __init__(self, parent, appareil):
        super().__init__(parent)
        self.title(f"Détails - {appareil.marque} {appareil.reference}")
        self.geometry("400x300")
        self.appareil = appareil
        
        # Rendre la fenêtre modale
        self.transient(parent)
        self.grab_set()
        
        self.create_widgets()
        
    def create_widgets(self):
        # Frame principal
        frame = ttk.Frame(self, padding="10")
        frame.pack(fill="both", expand=True)
        
        # Informations générales
        ttk.Label(frame, text="Informations générales", font=("", 12, "bold")).pack(pady=(0, 10))
        
        # Type d'appareil
        ttk.Label(frame, text=f"Type: {self.appareil.get_type()}").pack(anchor="w", pady=2)
        
        # Marque
        ttk.Label(frame, text=f"Marque: {self.appareil.marque}").pack(anchor="w", pady=2)
        
        # Référence
        ttk.Label(frame, text=f"Référence: {self.appareil.reference}").pack(anchor="w", pady=2)
        
        # Caractéristiques spécifiques
        ttk.Label(frame, text="Caractéristiques spécifiques", font=("", 12, "bold")).pack(pady=(20, 10))
        
        # Afficher les caractéristiques selon le type d'appareil
        if hasattr(self.appareil, 'temperature'):
            ttk.Label(frame, text=f"Température: {self.appareil.temperature}°C").pack(anchor="w", pady=2)
        if hasattr(self.appareil, 'capacite'):
            ttk.Label(frame, text=f"Capacité: {self.appareil.capacite}kg").pack(anchor="w", pady=2)
        if hasattr(self.appareil, 'capacite_sechage'):
            ttk.Label(frame, text=f"Capacité de séchage: {self.appareil.capacite_sechage}kg").pack(anchor="w", pady=2)
            
        # Bouton de fermeture
        ttk.Button(frame, text="Fermer", command=self.destroy).pack(pady=(20, 0))
        
        # Centrer la fenêtre
        self.update_idletasks()
        width = self.winfo_width()
        height = self.winfo_height()
        x = (self.winfo_screenwidth() // 2) - (width // 2)
        y = (self.winfo_screenheight() // 2) - (height // 2)
        self.geometry(f'{width}x{height}+{x}+{y}') 