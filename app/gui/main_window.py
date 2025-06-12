import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
from app.gui.windows.ajout_window import AjoutWindow
from app.gui.windows.technicien_detail_window import DetailWindow
from app.gui.windows.test_window import TestWindow
import os

class MainWindow(tk.Tk):
    def __init__(self, gestionnaire):
        super().__init__()
        
        self.title("GESTO - Gestion des Tests")
        self.geometry("1200x800")
        
        # Dictionnaire pour suivre les fenêtres de test ouvertes
        self.test_windows = {}
        
        # Initialisation du gestionnaire
        self.gestionnaire = gestionnaire
        
        # Création des widgets
        self.create_menu()
        self.create_widgets()
        
        # Démarrer la sauvegarde automatique (toutes les 5 minutes)
        self.after(300000, self.sauvegarde_automatique)
        
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
        # Frame pour la recherche
        search_frame = ttk.Frame(self.presentation_frame)
        search_frame.pack(fill="x", padx=5, pady=5)
        
        ttk.Label(search_frame, text="Rechercher:").pack(side="left", padx=5)
        self.search_var = tk.StringVar()
        self.search_var.trace("w", self.filter_tree)
        search_entry = ttk.Entry(search_frame, textvariable=self.search_var, width=40)
        search_entry.pack(side="left", padx=5)
        
        # Bouton pour effacer la recherche
        ttk.Button(search_frame, text="Effacer", command=self.clear_search).pack(side="left", padx=5)
        
        # Frame pour la liste des appareils
        list_frame = ttk.Frame(self.presentation_frame)
        list_frame.pack(fill="both", expand=True, padx=5, pady=5)
        
        # Liste des appareils
        self.tree = ttk.Treeview(list_frame, columns=("identifiant", "type", "marque", "reference", "numero_serie", "date_arrivee", "statut", "localisation"), show="headings")
        
        # Configuration des colonnes
        columns = {
            "identifiant": "Identifiant",
            "type": "Type",
            "marque": "Marque",
            "reference": "Référence",
            "numero_serie": "Numéro de série",
            "date_arrivee": "Date d'arrivée",
            "statut": "Statut",
            "localisation": "Localisation"
        }
        
        for col, text in columns.items():
            self.tree.heading(col, text=text, command=lambda c=col: self.sort_tree(c))
            self.tree.column(col, width=100)
        
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
        
        self.tree.bind("<Double-1>", self.afficher_synthese_machine)
        # Zone de synthèse
        self.synthese_frame = ttk.LabelFrame(self.presentation_frame, text="Synthèse de la machine", padding=10)
        self.synthese_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        self.synthese_text = tk.Text(self.synthese_frame, height=15)
        self.synthese_text.pack(fill=tk.BOTH, expand=True)
        
        # Variable pour suivre l'état du tri
        self.sort_column = None
        self.sort_reverse = False

    def create_depannage_tab(self):
        # Frame principal
        frame = ttk.Frame(self.depannage_frame)
        frame.pack(fill=tk.BOTH, expand=True)
        
        # Bouton pour ouvrir la vérification pré-vente
        ttk.Button(frame, text="Test", 
                   command=self.open_test).pack(pady=10)
        
        # Frame pour la sélection de l'appareil
        select_frame = ttk.LabelFrame(frame, text="Sélection de l'appareil", padding=10)
        select_frame.pack(fill=tk.X, padx=5, pady=5)
        
        # Liste déroulante pour sélectionner l'appareil
        self.appareil_var = tk.StringVar()
        self.appareil_combo = ttk.Combobox(select_frame, textvariable=self.appareil_var)
        self.appareil_combo.pack(fill=tk.X, pady=5)
        self.appareil_combo.bind("<<ComboboxSelected>>", self.on_appareil_selected)
        
        # Frame pour les deux sections côte à côte
        sections_frame = ttk.Frame(frame)
        sections_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Frame pour le formulaire de panne (à gauche)
        form_frame = ttk.LabelFrame(sections_frame, text="Fiche de panne", padding=10)
        form_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 5))
        
        # Symptôme
        ttk.Label(form_frame, text="Symptôme:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.symptome_text = tk.Text(form_frame, height=3, width=40)
        self.symptome_text.grid(row=0, column=1, sticky=tk.W, pady=5)
        
        # Cause probable
        ttk.Label(form_frame, text="Cause probable:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.cause_probable_text = tk.Text(form_frame, height=3, width=40)
        self.cause_probable_text.grid(row=1, column=1, sticky=tk.W, pady=5)
        
        # Notes techniques
        ttk.Label(form_frame, text="Notes techniques:").grid(row=2, column=0, sticky=tk.W, pady=5)
        self.notes_text = tk.Text(form_frame, height=5, width=40)
        self.notes_text.grid(row=2, column=1, sticky=tk.W, pady=5)
        
        # Technicien
        ttk.Label(form_frame, text="Technicien:").grid(row=3, column=0, sticky=tk.W, pady=5)
        self.technicien_var = tk.StringVar()
        ttk.Entry(form_frame, textvariable=self.technicien_var).grid(row=3, column=1, sticky=tk.W, pady=5)
        
        # Statut
        ttk.Label(form_frame, text="Statut:").grid(row=4, column=0, sticky=tk.W, pady=5)
        self.statut_var = tk.StringVar(value="à réparer")
        statuts = ["à réparer", "diagnostiquer", "réparer"]
        ttk.Combobox(form_frame, textvariable=self.statut_var, values=statuts).grid(row=4, column=1, sticky=tk.W, pady=5)
        
        # Boutons de la fiche de panne
        button_frame = ttk.Frame(form_frame)
        button_frame.grid(row=5, column=0, columnspan=2, pady=20)
        
        ttk.Button(button_frame, text="Enregistrer", command=self.save_fiche_panne).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Effacer", command=self.clear_fiche_panne).pack(side=tk.LEFT, padx=5)
        
        # Frame pour le résumé des tests (à droite)
        test_frame = ttk.LabelFrame(sections_frame, text="Résumé des tests", padding=10)
        test_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(5, 0))
        
        # Zone de texte pour le résumé des tests
        self.test_summary_text = tk.Text(test_frame, height=20, width=40)
        self.test_summary_text.pack(fill=tk.BOTH, expand=True)
        
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
            self.symptome_text.delete(1.0, tk.END)
            self.symptome_text.insert(1.0, fiche.symptome)
            self.cause_probable_text.delete(1.0, tk.END)
            self.cause_probable_text.insert(1.0, fiche.cause_probable)
            self.notes_text.delete(1.0, tk.END)
            self.notes_text.insert(1.0, fiche.notes_techniques)
            self.technicien_var.set(fiche.technicien)
            self.statut_var.set(fiche.statut)
        else:
            self.clear_fiche_panne()
            
        # Mettre à jour le résumé des tests
        self.update_test_summary(appareil_id)
        
    def update_test_summary(self, appareil_id):
        """Met à jour le résumé des tests pour l'appareil sélectionné"""
        test = self.gestionnaire.get_test(appareil_id)
        self.test_summary_text.delete(1.0, tk.END)
        
        if not test:
            self.test_summary_text.insert(1.0, "Aucun test effectué")
            return
            
        summary = "Vérifications visuelles:\n"
        summary += f"✓ Commande: {'OK' if test.commande_ok else 'Non testé'}\n"
        summary += f"✓ Verrou porte: {'OK' if test.verrou_porte_ok else 'Non testé'}\n"
        summary += f"✓ Rotation tambour: {'OK' if test.rotation_tambour_ok else 'Non testé'}\n"
        summary += f"✓ Chauffe: {'OK' if test.chauffe_ok else 'Non testé'}\n"
        summary += f"✓ Essorage: {'OK' if test.essorage_ok else 'Non testé'}\n"
        summary += f"✓ Séchage: {'OK' if test.sechage_ok else 'Non testé'}\n\n"
        
        summary += "Programmes testés:\n"
        summary += f"• Express: {test.programme_express or 'Non testé'}\n"
        summary += f"• Chauffe: {test.programme_chauffe or 'Non testé'}\n"
        summary += f"• Rotation: {test.programme_rotation or 'Non testé'}\n\n"
        
        if test.observations.get('journal_problemes'):
            summary += "Derniers problèmes:\n"
            # Prendre les 3 dernières lignes du journal
            problems = test.observations['journal_problemes'].split('\n')[-3:]
            summary += '\n'.join(problems) + '\n\n'
            
        if test.statut:
            summary += f"Statut du test: {test.statut}"
            
        self.test_summary_text.insert(1.0, summary)
        
    def save_fiche_panne(self):
        if not self.appareil_var.get():
            messagebox.showerror("Erreur", "Veuillez sélectionner un appareil")
            return
            
        appareil_id = self.appareil_var.get().split(" - ")[0]
        
        self.gestionnaire.ajouter_fiche_panne(
            appareil_id=appareil_id,
            symptome=self.symptome_text.get(1.0, tk.END).strip(),
            cause_probable=self.cause_probable_text.get(1.0, tk.END).strip(),
            notes_techniques=self.notes_text.get(1.0, tk.END).strip(),
            technicien=self.technicien_var.get()
        )
        
        # Mettre à jour le statut
        self.gestionnaire.mettre_a_jour_fiche_panne(
            appareil_id,
            statut=self.statut_var.get()
        )
        
        messagebox.showinfo("Succès", "Fiche de panne enregistrée avec succès!")
        
    def clear_fiche_panne(self):
        self.symptome_text.delete(1.0, tk.END)
        self.cause_probable_text.delete(1.0, tk.END)
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
                item = self.tree.insert("", tk.END, values=(
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

    def open_test(self):
        if not self.appareil_var.get():
            messagebox.showerror("Erreur", "Veuillez sélectionner un appareil dans la liste déroulante")
            return
            
        appareil_id = self.appareil_var.get().split(" - ")[0]
        appareil = self.gestionnaire.get_appareil_by_id(appareil_id)
        if not appareil:
            messagebox.showerror("Erreur", "Appareil non trouvé")
            return
            
        self.ouvrir_fenetre_test(appareil)

    def ouvrir_fenetre_test(self, appareil):
        # Vérifier si une fenêtre de test est déjà ouverte pour cet appareil
        if appareil.identifiant in self.test_windows:
            # Si la fenêtre existe mais a été fermée, la retirer du dictionnaire
            if not self.test_windows[appareil.identifiant].winfo_exists():
                del self.test_windows[appareil.identifiant]
            else:
                # Si la fenêtre existe toujours, afficher un message et proposer des options
                reponse = messagebox.askyesnocancel(
                    "Fenêtre de test déjà ouverte",
                    f"Une fenêtre de test est déjà ouverte pour l'appareil {appareil.identifiant}.\n\n"
                    "Voulez-vous :\n"
                    "- 'Oui' : Basculer vers la fenêtre existante\n"
                    "- 'Non' : Ouvrir une nouvelle fenêtre\n"
                    "- 'Annuler' : Ne rien faire"
                )
                
                if reponse is None:  # Annuler
                    return
                elif reponse:  # Oui - basculer vers la fenêtre existante
                    self.test_windows[appareil.identifiant].lift()
                    self.test_windows[appareil.identifiant].focus_force()
                    return
                else:  # Non - fermer l'ancienne fenêtre et en ouvrir une nouvelle
                    self.test_windows[appareil.identifiant].destroy()
        
        # Créer une nouvelle fenêtre de test
        test_window = TestWindow(self, appareil)
        # Stocker la référence de la fenêtre
        self.test_windows[appareil.identifiant] = test_window
        # Configurer la fenêtre pour qu'elle se retire du dictionnaire quand elle est fermée
        test_window.protocol("WM_DELETE_WINDOW", lambda: self.fermer_fenetre_test(appareil.identifiant))

    def fermer_fenetre_test(self, appareil_id):
        # Retirer la fenêtre du dictionnaire
        if appareil_id in self.test_windows:
            del self.test_windows[appareil_id]

    def afficher_synthese_machine(self, event):
        selection = self.tree.selection()
        if not selection:
            return
        appareil_id = self.tree.item(selection[0])['values'][0]
        appareil = self.gestionnaire.get_appareil_by_id(appareil_id)
        fiche = self.gestionnaire.get_fiche_panne(appareil_id)
        test = self.gestionnaire.get_test(appareil_id)
        synthese = f"Identifiant : {appareil.identifiant}\nType : {type(appareil).__name__}\nMarque : {appareil.marque}\nRéférence : {appareil.reference}\nNuméro de série : {appareil.numero_serie}\nDate arrivée : {appareil.date_arrivee}\nStatut : {appareil.statut}\n"
        if fiche:
            synthese += f"\n--- Fiche de panne ---\nSymptôme : {fiche.symptome}\nCause probable : {fiche.cause_probable}\nNotes techniques : {fiche.notes_techniques}\nTechnicien : {fiche.technicien}\nStatut : {fiche.statut}\n"
        if test:
            synthese += f"\n--- Test ---\nVérifications visuelles :\n  Commande : {test.commande_ok}\n  Verrou porte : {test.verrou_porte_ok}\n  Rotation tambour : {test.rotation_tambour_ok}\n  Chauffe : {test.chauffe_ok}\n  Essorage : {test.essorage_ok}\n  Séchage : {test.sechage_ok}\nProgrammes :\n  Express : {test.programme_express}\n  Chauffe : {test.programme_chauffe}\n  Rotation : {test.programme_rotation}\nJournal des problèmes :\n{test.observations.get('journal_problemes', '')}\nObservations :\n"
            for k, v in test.observations.items():
                if k != 'journal_problemes' and k != 'tentatives':
                    synthese += f"  {k} : {v}\n"
        self.synthese_text.delete("1.0", tk.END)
        self.synthese_text.insert("1.0", synthese)

    def create_menu(self):
        menubar = tk.Menu(self)
        self.config(menu=menubar)
        
        # Menu Fichier
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Fichier", menu=file_menu)
        file_menu.add_command(label="Quitter", command=self.quit)
        
        # Menu Fenêtres
        windows_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Fenêtres", menu=windows_menu)
        windows_menu.add_command(label="Fenêtres de test ouvertes", command=self.afficher_fenetres_test)
        
        # Menu Sauvegardes
        backup_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Sauvegardes", menu=backup_menu)
        backup_menu.add_command(label="Liste des sauvegardes", command=self.afficher_sauvegardes)
        backup_menu.add_command(label="Sauvegarder maintenant", command=self.sauvegarder_maintenant)
        
    def afficher_sauvegardes(self):
        """Affiche la fenêtre de gestion des sauvegardes"""
        backup_window = tk.Toplevel(self)
        backup_window.title("Gestion des sauvegardes")
        backup_window.geometry("600x400")
        
        # Liste des sauvegardes
        frame = ttk.Frame(backup_window, padding="10")
        frame.pack(fill=tk.BOTH, expand=True)
        
        ttk.Label(frame, text="Sauvegardes disponibles:").pack(anchor=tk.W)
        
        # Créer un Treeview pour afficher les sauvegardes
        columns = ("Date", "Heure", "Fichier")
        tree = ttk.Treeview(frame, columns=columns, show="headings")
        
        # Définir les en-têtes
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=150)
        
        # Ajouter les sauvegardes
        for backup_file in self.gestionnaire.get_liste_backups():
            filename = os.path.basename(backup_file)
            # Extraire la date et l'heure du nom de fichier
            date_str = filename[6:14]  # YYYYMMDD
            time_str = filename[15:21]  # HHMMSS
            date = f"{date_str[:4]}-{date_str[4:6]}-{date_str[6:]}"
            time = f"{time_str[:2]}:{time_str[2:4]}:{time_str[4:]}"
            
            tree.insert("", tk.END, values=(date, time, filename))
        
        tree.pack(fill=tk.BOTH, expand=True, pady=5)
        
        # Boutons
        button_frame = ttk.Frame(frame)
        button_frame.pack(fill=tk.X, pady=10)
        
        def restaurer_selection():
            selection = tree.selection()
            if not selection:
                messagebox.showwarning("Attention", "Veuillez sélectionner une sauvegarde à restaurer")
                return
                
            if messagebox.askyesno("Confirmation", 
                "Êtes-vous sûr de vouloir restaurer cette sauvegarde ?\nLes données actuelles seront remplacées."):
                backup_file = os.path.join("app", "data", "backups", tree.item(selection[0])["values"][2])
                if self.gestionnaire.restaurer_backup(backup_file):
                    messagebox.showinfo("Succès", "Sauvegarde restaurée avec succès")
                    self.refresh_liste()  # Rafraîchir l'affichage
                    backup_window.destroy()
                else:
                    messagebox.showerror("Erreur", "Erreur lors de la restauration")
        
        ttk.Button(button_frame, text="Restaurer", command=restaurer_selection).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Fermer", command=backup_window.destroy).pack(side=tk.RIGHT, padx=5)
        
    def sauvegarder_maintenant(self):
        """Force une sauvegarde immédiate"""
        self.gestionnaire.sauvegarder_tests()
        messagebox.showinfo("Succès", "Sauvegarde effectuée avec succès")

    def sauvegarde_automatique(self):
        """Effectue une sauvegarde automatique et programme la prochaine"""
        self.gestionnaire.sauvegarder_tests()
        # Programmer la prochaine sauvegarde
        self.after(300000, self.sauvegarde_automatique)

    def afficher_fenetres_test(self):
        """Affiche une fenêtre listant toutes les fenêtres de test ouvertes"""
        if not self.test_windows:
            messagebox.showinfo("Information", "Aucune fenêtre de test ouverte")
            return
            
        # Créer une nouvelle fenêtre
        window = tk.Toplevel(self)
        window.title("Fenêtres de test ouvertes")
        window.geometry("400x300")
        
        # Frame principal
        frame = ttk.Frame(window, padding="10")
        frame.pack(fill=tk.BOTH, expand=True)
        
        # Liste des fenêtres
        ttk.Label(frame, text="Fenêtres de test actuellement ouvertes :").pack(anchor=tk.W)
        
        # Créer un Treeview
        columns = ("Appareil", "Statut")
        tree = ttk.Treeview(frame, columns=columns, show="headings")
        
        # Définir les en-têtes
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=150)
        
        # Ajouter les fenêtres
        for appareil_id, test_window in self.test_windows.items():
            if test_window.winfo_exists():
                # Récupérer le statut du test
                test = self.gestionnaire.get_test(appareil_id)
                statut = test.statut if test else "en_cours"
                tree.insert("", tk.END, values=(appareil_id, statut))
        
        tree.pack(fill=tk.BOTH, expand=True, pady=5)
        
        # Boutons
        button_frame = ttk.Frame(frame)
        button_frame.pack(fill=tk.X, pady=10)
        
        def basculer_vers_fenetre():
            selection = tree.selection()
            if not selection:
                messagebox.showwarning("Attention", "Veuillez sélectionner une fenêtre")
                return
                
            appareil_id = tree.item(selection[0])["values"][0]
            if appareil_id in self.test_windows:
                self.test_windows[appareil_id].lift()
                self.test_windows[appareil_id].focus_force()
                window.destroy()
        
        ttk.Button(button_frame, text="Basculer vers la fenêtre", command=basculer_vers_fenetre).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Fermer", command=window.destroy).pack(side=tk.RIGHT, padx=5)

    def sort_tree(self, col):
        """Trie les éléments de la Treeview selon la colonne sélectionnée"""
        # Récupérer tous les éléments
        items = [(self.tree.set(item, col), item) for item in self.tree.get_children("")]
        
        # Déterminer si c'est la même colonne que précédemment
        if self.sort_column == col:
            self.sort_reverse = not self.sort_reverse
        else:
            self.sort_column = col
            self.sort_reverse = False
        
        # Trier les éléments
        items.sort(reverse=self.sort_reverse)
        
        # Réorganiser les éléments dans la Treeview
        for index, (_, item) in enumerate(items):
            self.tree.move(item, "", index)
        
        # Mettre à jour l'en-tête de la colonne pour indiquer le sens du tri
        for column in self.tree["columns"]:
            if column == col:
                self.tree.heading(column, text=f"{self.tree.heading(column)['text']} {'↓' if self.sort_reverse else '↑'}")
            else:
                self.tree.heading(column, text=self.tree.heading(column)['text'].replace(' ↓', '').replace(' ↑', ''))

    def clear_search(self):
        """Efface le texte de recherche et réinitialise l'affichage"""
        self.search_var.set("")
        self.refresh_liste()  # Réinitialiser la liste complète

    def filter_tree(self, *args):
        """Filtre les éléments de la Treeview selon le texte de recherche"""
        search_text = self.search_var.get().lower()
        
        # Si la recherche est vide, réinitialiser la liste
        if not search_text:
            self.refresh_liste()
            return
            
        # Sauvegarder tous les éléments actuels avec leurs valeurs
        all_items = []
        for item in self.tree.get_children():
            values = [str(self.tree.set(item, col)).lower() for col in self.tree["columns"]]
            original_values = [self.tree.set(item, col) for col in self.tree["columns"]]
            all_items.append((values, original_values))
        
        # Effacer le treeview
        self.tree.delete(*self.tree.get_children())
        
        # Réinsérer les éléments qui correspondent à la recherche
        for values, original_values in all_items:
            if any(search_text in value for value in values):
                self.tree.insert("", tk.END, values=original_values) 