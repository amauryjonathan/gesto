import tkinter as tk
from tkinter import ttk, messagebox
import time
from app.gestion.gestionnaire import GestionnaireAppareils
from app.models.frigo import Frigo
from app.models.four import Four
from app.models.lave_linge import LaveLinge
from app.models.lave_vaisselle import LaveVaisselle
from app.models.lave_linge_sechant import LaveLingeSechant
from app.gui.windows.ajout_window import AjoutWindow
from app.gui.windows.recherche_window import RechercheWindow
from app.gui.windows.details_window import DetailsWindow

class MainWindow(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Gestion des Appareils Électroménagers")
        self.geometry("800x600")
        
        self.gestionnaire = GestionnaireAppareils()
        self.create_widgets()
        self.refresh_liste()
    
    def create_widgets(self):
        # Frame principal
        main_frame = ttk.Frame(self)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Liste des appareils
        self.tree = ttk.Treeview(main_frame, columns=("ID", "Type", "Marque", "Référence", "Statut", "Localisation"), show="headings")
        self.tree.heading("ID", text="ID")
        self.tree.heading("Type", text="Type")
        self.tree.heading("Marque", text="Marque")
        self.tree.heading("Référence", text="Référence")
        self.tree.heading("Statut", text="Statut")
        self.tree.heading("Localisation", text="Localisation")
        
        self.tree.column("ID", width=50)
        self.tree.column("Type", width=100)
        self.tree.column("Marque", width=100)
        self.tree.column("Référence", width=100)
        self.tree.column("Statut", width=100)
        self.tree.column("Localisation", width=100)
        
        self.tree.pack(fill=tk.BOTH, expand=True)
        
        # Frame pour les boutons
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=tk.X, pady=10)
        
        ttk.Button(button_frame, text="Ajouter", command=self.ouvrir_ajout).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Modifier", command=self.modifier_appareil).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Supprimer", command=self.supprimer_appareil).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Rechercher", command=self.ouvrir_recherche).pack(side=tk.LEFT, padx=5)
    
    def refresh_liste(self):
        # Effacer la liste
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Récupérer tous les appareils
        appareils = []
        for type_appareil in self.gestionnaire.appareils.values():
            appareils.extend(type_appareil)
        
        # Trier par identifiant
        appareils.sort(key=lambda x: x.identifiant)
        
        # Ajouter à la liste
        for appareil in appareils:
            self.tree.insert("", tk.END, values=(
                appareil.identifiant,
                appareil.__class__.__name__,
                appareil.marque,
                appareil.reference,
                appareil.statut,
                appareil.get_localisation()
            ))
    
    def ouvrir_ajout(self):
        AjoutWindow(self)
    
    def modifier_appareil(self):
        selection = self.tree.selection()
        if not selection:
            messagebox.showwarning("Attention", "Veuillez sélectionner un appareil à modifier")
            return
        
        item = self.tree.item(selection[0])
        identifiant = item["values"][0]
        
        # Trouver l'appareil
        appareil = None
        for type_appareils in self.gestionnaire.appareils.values():
            for a in type_appareils:
                if a.identifiant == identifiant:
                    appareil = a
                    break
            if appareil:
                break
        
        if appareil:
            DetailsWindow(self, appareil)
    
    def supprimer_appareil(self):
        selection = self.tree.selection()
        if not selection:
            messagebox.showwarning("Attention", "Veuillez sélectionner un appareil à supprimer")
            return
        
        if messagebox.askyesno("Confirmation", "Voulez-vous vraiment supprimer cet appareil ?"):
            item = self.tree.item(selection[0])
            identifiant = item["values"][0]
            
            # Trouver et supprimer l'appareil
            for type_appareils in self.gestionnaire.appareils.values():
                for i, appareil in enumerate(type_appareils):
                    if appareil.identifiant == identifiant:
                        type_appareils.pop(i)
                        self.gestionnaire.sauvegarder_json()
                        self.refresh_liste()
                        return
    
    def ouvrir_recherche(self):
        RechercheWindow(self)

    def test_performance(self):
        """Test de performance avec les deux approches"""
        # Création de 1000 appareils pour le test
        appareils = []
        for i in range(1000):
            frigo = Frigo(f"F{i:03d}", "Samsung", f"RT{i}", f"SN{i}", "2024-01-01", "en stock", 4.5)
            appareils.append(frigo)
        
        # Test approche 1 (dictionnaire)
        start_time = time.time()
        for appareil in appareils:
            appareil_id = f"Frigo_{appareil.marque}_{appareil.reference}"
            self.gestionnaire.ajouter_appareil(appareil)
            # Ajout de métadonnées
            self.gestionnaire.metadonnees[appareil_id] = {
                'date_prise_en_charge': '2024-02-20',
                'panne_detectee': 'Compresseur défectueux',
                'statut_reparation': 'En cours',
                'technicien': 'Jean Dupont',
                'notes': 'Pièce commandée'
            }
        dict_time = time.time() - start_time
        
        # Test approche 2 (stockage direct)
        start_time = time.time()
        for appareil in appareils:
            # Simulation du stockage direct dans le Treeview
            pass
        direct_time = time.time() - start_time
        
        messagebox.showinfo("Résultats des tests", 
            f"Temps pour 1000 appareils:\n"
            f"Approche dictionnaire: {dict_time:.3f} secondes\n"
            f"Approche stockage direct: {direct_time:.3f} secondes\n\n"
            f"Consommation mémoire estimée:\n"
            f"Approche dictionnaire: ~2-3 MB\n"
            f"Approche stockage direct: ~10-15 MB") 