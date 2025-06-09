import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
from app.gui.windows.ajout_window import AjoutWindow
from app.gui.windows.technicien_detail_window import DetailWindow

class MainWindow(tk.Tk):
    def __init__(self, gestionnaire):
        super().__init__()
        self.gestionnaire = gestionnaire
        
        self.title("Gestion des appareils")
        self.geometry("1200x800")
        
        self.create_widgets()
        
    def create_widgets(self):
        # Création du notebook (onglets)
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # Onglet Présentation
        self.presentation_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.presentation_frame, text="Présentation")
        self.create_presentation_tab()
        
        # Onglet Dépannage
        self.depannage_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.depannage_frame, text="Dépannage")
        self.create_depannage_tab()
        
    def create_presentation_tab(self):
        # Frame pour la liste des appareils
        list_frame = ttk.Frame(self.presentation_frame)
        list_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Liste des appareils
        self.tree = ttk.Treeview(list_frame, columns=("identifiant", "type", "marque", "reference", "numero_serie", "date_arrivee", "statut", "localisation"), show="headings")
        
        # Configuration des colonnes
        self.tree.heading("identifiant", text="Identifiant")
        self.tree.heading("type", text="Type")
        self.tree.heading("marque", text="Marque")
        self.tree.heading("reference", text="Référence")
        self.tree.heading("numero_serie", text="Numéro de série")
        self.tree.heading("date_arrivee", text="Date d'arrivée")
        self.tree.heading("statut", text="Statut")
        self.tree.heading("localisation", text="Localisation")
        
        self.tree.column("identifiant", width=100)
        self.tree.column("type", width=100)
        self.tree.column("marque", width=100)
        self.tree.column("reference", width=100)
        self.tree.column("numero_serie", width=150)
        self.tree.column("date_arrivee", width=100)
        self.tree.column("statut", width=100)
        self.tree.column("localisation", width=100)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        # Placement des widgets
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Bouton d'ajout
        ttk.Button(self.presentation_frame, text="Ajouter un appareil", command=self.ouvrir_ajout).pack(pady=5)
        
        # Remplir la liste
        self.refresh_liste()
        
    def create_depannage_tab(self):
        # Frame pour la sélection de l'appareil
        select_frame = ttk.LabelFrame(self.depannage_frame, text="Sélection de l'appareil", padding=10)
        select_frame.pack(fill=tk.X, padx=5, pady=5)
        
        # Liste déroulante pour sélectionner l'appareil
        self.appareil_var = tk.StringVar()
        self.appareil_combo = ttk.Combobox(select_frame, textvariable=self.appareil_var)
        self.appareil_combo.pack(fill=tk.X, pady=5)
        self.appareil_combo.bind("<<ComboboxSelected>>", self.on_appareil_selected)
        
        # Frame pour le formulaire de panne
        form_frame = ttk.LabelFrame(self.depannage_frame, text="Fiche de panne", padding=10)
        form_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Type de panne
        ttk.Label(form_frame, text="Type de panne:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.type_panne_var = tk.StringVar()
        types_panne = ["Électrique", "Mécanique", "Électronique", "Hydraulique", "Autre"]
        ttk.Combobox(form_frame, textvariable=self.type_panne_var, values=types_panne).grid(row=0, column=1, sticky=tk.W, pady=5)
        
        # Notes techniques
        ttk.Label(form_frame, text="Notes techniques:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.notes_text = tk.Text(form_frame, height=5, width=40)
        self.notes_text.grid(row=1, column=1, sticky=tk.W, pady=5)
        
        # Technicien
        ttk.Label(form_frame, text="Technicien:").grid(row=2, column=0, sticky=tk.W, pady=5)
        self.technicien_var = tk.StringVar()
        ttk.Entry(form_frame, textvariable=self.technicien_var).grid(row=2, column=1, sticky=tk.W, pady=5)
        
        # Statut
        ttk.Label(form_frame, text="Statut:").grid(row=3, column=0, sticky=tk.W, pady=5)
        self.statut_var = tk.StringVar(value="à réparer")
        statuts = ["à réparer", "diagnostiquer", "réparer"]
        ttk.Combobox(form_frame, textvariable=self.statut_var, values=statuts).grid(row=3, column=1, sticky=tk.W, pady=5)
        
        # Boutons
        button_frame = ttk.Frame(form_frame)
        button_frame.grid(row=4, column=0, columnspan=2, pady=20)
        
        ttk.Button(button_frame, text="Enregistrer", command=self.save_fiche_panne).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Effacer", command=self.clear_fiche_panne).pack(side=tk.LEFT, padx=5)
        
        # Mettre à jour la liste des appareils
        self.update_appareil_list()
        
    def update_appareil_list(self):
        appareils = []
        for type_app, liste in self.gestionnaire.appareils.items():
            for appareil in liste:
                appareils.append(f"{appareil.identifiant} - {appareil.marque} {appareil.reference}")
        self.appareil_combo['values'] = appareils
        
    def on_appareil_selected(self, event):
        # Récupérer l'identifiant de l'appareil sélectionné
        selection = self.appareil_var.get()
        appareil_id = selection.split(" - ")[0]
        
        # Charger la fiche de panne existante ou créer une nouvelle
        fiche = self.gestionnaire.get_fiche_panne(appareil_id)
        if fiche:
            self.type_panne_var.set(fiche.type_panne)
            self.notes_text.delete(1.0, tk.END)
            self.notes_text.insert(1.0, fiche.notes_techniques)
            self.technicien_var.set(fiche.technicien)
            self.statut_var.set(fiche.statut)
        else:
            self.clear_fiche_panne()
            
    def save_fiche_panne(self):
        if not self.appareil_var.get():
            messagebox.showerror("Erreur", "Veuillez sélectionner un appareil")
            return
            
        appareil_id = self.appareil_var.get().split(" - ")[0]
        
        self.gestionnaire.ajouter_fiche_panne(
            appareil_id,
            self.type_panne_var.get(),
            self.notes_text.get(1.0, tk.END).strip(),
            self.technicien_var.get()
        )
        
        # Mettre à jour le statut
        self.gestionnaire.mettre_a_jour_fiche_panne(
            appareil_id,
            statut=self.statut_var.get()
        )
        
        messagebox.showinfo("Succès", "Fiche de panne enregistrée avec succès!")
        
    def clear_fiche_panne(self):
        self.type_panne_var.set("")
        self.notes_text.delete(1.0, tk.END)
        self.technicien_var.set("")
        self.statut_var.set("à réparer")
        
    def refresh_liste(self):
        # Effacer la liste
        for item in self.tree.get_children():
            self.tree.delete(item)
            
        # Remplir la liste
        for type_app, appareils in self.gestionnaire.appareils.items():
            for appareil in appareils:
                localisation = f"{appareil.cellule}{appareil.emplacement}{appareil.position}" if appareil.cellule and appareil.emplacement and appareil.position else ""
                self.tree.insert("", tk.END, values=(
                    appareil.identifiant,
                    type_app.replace("_", " ").title(),
                    appareil.marque,
                    appareil.reference,
                    appareil.numero_serie,
                    appareil.date_arrivee,
                    appareil.statut,
                    localisation
                ))
                
    def ouvrir_ajout(self):
        AjoutWindow(self, self.refresh_liste) 