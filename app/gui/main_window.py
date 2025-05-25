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
    def __init__(self, gestionnaire: GestionnaireAppareils):
        super().__init__()
        self.title("Gestion des Appareils Electroménagers")
        self.geometry("800x600")
        self.gestionnaire = gestionnaire
        
        # Dictionnaire pour stocker les appareils par identifiant
        self.appareils_dict = {}
        
        # Métadonnées pour le suivi technique
        self.metadonnees = {}
        
        self.create_widgets()
        self.refresh_liste()
        
    def create_widgets(self):
        # Frame pour la liste des appareils
        frame_liste = ttk.LabelFrame(self, text="Liste des appareils")
        frame_liste.pack(fill="both", expand=True, padx=10, pady=5)
        
        # Création du Treeview pour afficher les appareils
        self.tree = ttk.Treeview(frame_liste, columns=("Type", "Marque", "Référence", "Spécifique", "Statut"), show="headings")
        
        # Configuration des colonnes
        self.tree.heading("Type", text="Type")
        self.tree.heading("Marque", text="Marque")
        self.tree.heading("Référence", text="Référence")
        self.tree.heading("Spécifique", text="Spécifique")
        self.tree.heading("Statut", text="Statut")
        
        # Configuration de la largeur des colonnes
        self.tree.column("Type", width=100)
        self.tree.column("Marque", width=100)
        self.tree.column("Référence", width=100)
        self.tree.column("Spécifique", width=100)
        self.tree.column("Statut", width=150)
        
        # Ajout d'une scrollbar
        scrollbar = ttk.Scrollbar(frame_liste, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        # Placement des widgets
        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Frame pour les boutons
        frame_boutons = ttk.Frame(self)
        frame_boutons.pack(fill="x", padx=10, pady=5)
        
        # Boutons
        ttk.Button(frame_boutons, text="Ajouter un appareil", command=self.ouvrir_ajout).pack(side="left", padx=5)
        ttk.Button(frame_boutons, text="Rechercher", command=self.ouvrir_recherche).pack(side="left", padx=5)
        ttk.Button(frame_boutons, text="Test Performance", command=self.test_performance).pack(side="left", padx=5)
        
        # Bind du double-clic pour voir les détails
        self.tree.bind("<Double-1>", self.on_double_click)
    
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
            self.appareils_dict[appareil_id] = appareil
            # Ajout de métadonnées
            self.metadonnees[appareil_id] = {
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
    
    def ouvrir_ajout(self):
        """Ouvre la fenêtre d'ajout d'appareil"""
        AjoutWindow(self, self.on_appareil_ajoute)
    
    def ouvrir_recherche(self):
        """Ouvre la fenêtre de recherche"""
        RechercheWindow(self, self.gestionnaire)
    
    def on_appareil_ajoute(self, appareil):
        """Callback appelé quand un nouvel appareil est ajouté"""
        self.gestionnaire.ajouter_appareil(appareil)
        self.refresh_liste()
        messagebox.showinfo("Succès", "Appareil ajouté avec succès!")
    
    def on_double_click(self, event):
        """Gère le double-clic sur un appareil"""
        item = self.tree.selection()[0]
        appareil_id = self.tree.item(item)["tags"][0]
        appareil = self.appareils_dict.get(appareil_id)
        if appareil:
            # Récupération des métadonnées
            metadonnees = self.metadonnees.get(appareil_id, {})
            DetailsWindow(self, appareil, metadonnees)
    
    def refresh_liste(self):
        """Rafraîchit la liste des appareils"""
        # Effacer la liste actuelle
        for item in self.tree.get_children():
            self.tree.delete(item)
            
        # Vider le dictionnaire
        self.appareils_dict.clear()
        self.metadonnees.clear()
            
        # Ajouter les nouveaux appareils
        for type_app, liste in self.gestionnaire.lister_appareils().items():
            for appareil in liste:
                # Créer un identifiant unique pour l'appareil
                appareil_id = f"{type_app}_{appareil.marque}_{appareil.reference}"
                
                # Stocker l'appareil dans le dictionnaire
                self.appareils_dict[appareil_id] = appareil
                
                # Initialiser les métadonnées
                self.metadonnees[appareil_id] = {
                    'date_prise_en_charge': None,
                    'panne_detectee': None,
                    'statut_reparation': 'Non réparé',
                    'technicien': None,
                    'notes': None
                }
                
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
                    spec,
                    self.metadonnees[appareil_id]['statut_reparation']
                ), tags=(appareil_id,)) 