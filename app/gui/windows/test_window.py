import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
import time

class TestWindow(tk.Toplevel):
    def __init__(self, parent, appareil):
        super().__init__(parent)
        self.parent = parent
        self.appareil = appareil
        
        print(f"Initialisation de la fenêtre de test pour {appareil.identifiant}")
        
        self.title(f"Test - {appareil.identifiant}")
        # Définir une taille minimale pour la fenêtre
        self.minsize(800, 600)
        # Définir la taille par défaut
        self.geometry("1000x800")
        
        # Variables pour les timers
        self.timer_running = False
        self.start_time = None
        self.current_program = None
        
        # Créer ou récupérer le test existant
        self.test = self.parent.gestionnaire.get_test(appareil.identifiant)
        print(f"Test récupéré : {self.test}")
        if not self.test:
            print("Création d'un nouveau test")
            self.test = self.parent.gestionnaire.ajouter_test(appareil.identifiant)
        
        # Charger le nombre de tentatives sauvegardé (si existant)
        self.tentatives = self.test.observations.get("tentatives", {
            "Express": 0,
            "Chauffe": 0,
            "Rotation": 0
        })
        # S'assurer que toutes les clés existent
        for prog in ["Express", "Chauffe", "Rotation"]:
            if prog not in self.tentatives:
                self.tentatives[prog] = 0
        
        print("Création des widgets")
        self.create_widgets()
        print("Widgets créés")
        
    def create_widgets(self):
        # Frame principal avec scrollbar
        main_container = ttk.Frame(self)
        main_container.pack(fill=tk.BOTH, expand=True)
        
        # Canvas pour le scroll
        canvas = tk.Canvas(main_container)
        scrollbar = ttk.Scrollbar(main_container, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw", width=canvas.winfo_width())
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Pack des éléments de scroll
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Frame principal avec padding
        main_frame = ttk.Frame(scrollable_frame, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Vérifications visuelles
        visu_frame = ttk.LabelFrame(main_frame, text="Vérifications visuelles", padding="5")
        visu_frame.pack(fill=tk.X, pady=5)
        
        # Fonction pour convertir les valeurs en booléens
        def to_bool(value):
            if isinstance(value, bool):
                return value
            if isinstance(value, str):
                return value.lower() in ['true', 'vrai', 'ok']
            return False
        
        # Variables pour les cases à cocher
        self.commande_var = tk.BooleanVar(value=to_bool(self.test.commande_ok))
        self.verrou_var = tk.BooleanVar(value=to_bool(self.test.verrou_porte_ok))
        self.rotation_check_var = tk.BooleanVar(value=to_bool(self.test.rotation_tambour_ok))
        self.chauffe_check_var = tk.BooleanVar(value=to_bool(self.test.chauffe_ok))
        self.essorage_var = tk.BooleanVar(value=to_bool(self.test.essorage_ok))
        self.sechage_var = tk.BooleanVar(value=to_bool(self.test.sechage_ok))
        
        # Cases à cocher
        ttk.Checkbutton(visu_frame, text="Commande (bandeau)", variable=self.commande_var).pack(anchor=tk.W, pady=2)
        ttk.Checkbutton(visu_frame, text="Verrou de porte", variable=self.verrou_var).pack(anchor=tk.W, pady=2)
        ttk.Checkbutton(visu_frame, text="Rotation du tambour", variable=self.rotation_check_var).pack(anchor=tk.W, pady=2)
        ttk.Checkbutton(visu_frame, text="Chauffe", variable=self.chauffe_check_var).pack(anchor=tk.W, pady=2)
        ttk.Checkbutton(visu_frame, text="Essorage", variable=self.essorage_var).pack(anchor=tk.W, pady=2)
        ttk.Checkbutton(visu_frame, text="Séchage", variable=self.sechage_var).pack(anchor=tk.W, pady=2)
        
        # Programmes de test
        prog_frame = ttk.LabelFrame(main_frame, text="Programmes de test", padding="5")
        prog_frame.pack(fill=tk.X, pady=5)
        
        # Timer frame
        timer_frame = ttk.Frame(prog_frame)
        timer_frame.pack(fill=tk.X, pady=5)
        
        self.timer_label = ttk.Label(timer_frame, text="Timer: 00:00:00")
        self.timer_label.pack(side=tk.LEFT, padx=5)
        
        self.timer_button = ttk.Button(timer_frame, text="Démarrer Timer", command=self.toggle_timer)
        self.timer_button.pack(side=tk.LEFT, padx=5)
        
        # Variables pour les programmes
        self.express_prog_var = tk.StringVar(value=self.test.programme_express or "non_testé")
        self.chauffe_prog_var = tk.StringVar(value=self.test.programme_chauffe or "non_testé")
        self.rotation_prog_var = tk.StringVar(value=self.test.programme_rotation or "non_testé")
        
        # Frame pour chaque programme
        self._prev_status = {
            "Express": self.test.programme_express or "non_testé",
            "Chauffe": self.test.programme_chauffe or "non_testé",
            "Rotation": self.test.programme_rotation or "non_testé"
        }
        
        for prog_name, prog_var in [("Express", self.express_prog_var), 
                                  ("Chauffe", self.chauffe_prog_var),
                                  ("Rotation", self.rotation_prog_var)]:
            prog_subframe = ttk.Frame(prog_frame)
            prog_subframe.pack(fill=tk.X, pady=5)
            
            ttk.Label(prog_subframe, text=f"Programme {prog_name}:").pack(side=tk.LEFT, padx=5)
            combo = ttk.Combobox(prog_subframe, textvariable=prog_var,
                               values=["non_testé", "en_cours", "réussi", "échoué"],
                               state="readonly", width=15)
            combo.pack(side=tk.LEFT, padx=5)
            combo.bind("<Button-1>", lambda e, p=prog_name: self.store_prev_status(p))
            combo.bind("<<ComboboxSelected>>", lambda e, p=prog_name: self.on_program_status_change(p))
            
            ttk.Button(prog_subframe, text="Ajouter problème",
                      command=lambda p=prog_name: self.add_problem(p)).pack(side=tk.LEFT, padx=5)
        
        # Journal des problèmes
        journal_frame = ttk.LabelFrame(main_frame, text="Journal des problèmes", padding="5")
        journal_frame.pack(fill=tk.BOTH, expand=True, pady=5)
        
        # Ajouter une scrollbar pour le journal
        journal_scroll = ttk.Scrollbar(journal_frame)
        journal_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.journal_text = tk.Text(journal_frame, height=10, yscrollcommand=journal_scroll.set)
        self.journal_text.pack(fill=tk.BOTH, expand=True)
        journal_scroll.config(command=self.journal_text.yview)
        
        # Charger le journal sauvegardé
        journal_saved = self.test.observations.get("journal_problemes", "")
        self.journal_text.delete("1.0", tk.END)
        self.journal_text.insert("1.0", journal_saved)
        
        # Observations
        obs_frame = ttk.LabelFrame(main_frame, text="Observations", padding="5")
        obs_frame.pack(fill=tk.BOTH, expand=True, pady=5)
        
        # Ajouter une scrollbar pour les observations
        obs_scroll = ttk.Scrollbar(obs_frame)
        obs_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.observations_text = tk.Text(obs_frame, height=10, yscrollcommand=obs_scroll.set)
        self.observations_text.pack(fill=tk.BOTH, expand=True)
        obs_scroll.config(command=self.observations_text.yview)
        
        # Charger les observations en excluant journal_problemes et tentatives
        observations = {k: v for k, v in self.test.observations.items() 
                       if k not in ["journal_problemes", "tentatives"] and v}
        self.observations_text.delete("1.0", tk.END)
        if observations:
            self.observations_text.insert("1.0", "\n".join(f"{k}: {v}" for k, v in observations.items()))
        
        # Frame pour les boutons (toujours visible en bas)
        button_frame = ttk.Frame(self)
        button_frame.pack(side=tk.BOTTOM, fill=tk.X, padx=10, pady=10)
        
        ttk.Button(button_frame, text="Enregistrer", command=self.save_verification).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Valider", command=self.validate_verification).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Fermer", command=self.destroy).pack(side=tk.RIGHT, padx=5)
        
        # Configurer le canvas pour qu'il s'adapte à la taille de la fenêtre
        def configure_canvas(event):
            canvas.configure(width=event.width)
            canvas.itemconfig(canvas.find_withtag("all")[0], width=event.width)
        
        canvas.bind("<Configure>", configure_canvas)
        
    def toggle_timer(self):
        if not self.timer_running:
            self.start_time = time.time()
            self.timer_running = True
            self.timer_button.configure(text="Arrêter Timer")
            self.update_timer()
        else:
            self.timer_running = False
            self.timer_button.configure(text="Démarrer Timer")
            self.start_time = None
            
    def update_timer(self):
        if self.timer_running:
            elapsed = time.time() - self.start_time
            hours = int(elapsed // 3600)
            minutes = int((elapsed % 3600) // 60)
            seconds = int(elapsed % 60)
            self.timer_label.configure(text=f"Timer: {hours:02d}:{minutes:02d}:{seconds:02d}")
            self.after(1000, self.update_timer)
            
    def store_prev_status(self, program_name):
        self._prev_status[program_name] = self.get_program_var(program_name).get()
            
    def on_program_status_change(self, program_name):
        new_status = self.get_program_var(program_name).get()
        prev_status = self._prev_status[program_name]
        # Incrémenter la tentative si on passe de non_testé à en_cours
        if prev_status == "non_testé" and new_status == "en_cours":
            self.tentatives[program_name] += 1
            self.journal_text.insert(tk.END, 
                f"Tentative {self.tentatives[program_name]} du programme {program_name}\n")
        # Arrêter le programme précédent s'il existe
        if new_status == "en_cours":
            if self.current_program and self.current_program != program_name:
                self.get_program_var(self.current_program).set("non_testé")
                self.journal_text.insert(tk.END, 
                    f"Programme {self.current_program} arrêté car {program_name} a été démarré\n")
            self.current_program = program_name
            if not self.timer_running:
                self.toggle_timer()  # Démarrer le timer si pas déjà en cours
        # Si on arrête le programme en cours
        elif self.current_program == program_name and new_status != "en_cours":
            self.current_program = None
            if self.timer_running:
                self.toggle_timer()  # Arrêter le timer
            
    def get_program_var(self, program_name):
        if program_name == "Express":
            return self.express_prog_var
        elif program_name == "Chauffe":
            return self.chauffe_prog_var
        elif program_name == "Rotation":
            return self.rotation_prog_var
            
    def add_problem(self, program_name):
        if not self.timer_running:
            messagebox.showwarning("Attention", "Veuillez démarrer le timer avant d'ajouter un problème")
            return
            
        # Créer une fenêtre de dialogue pour saisir le problème
        dialog = tk.Toplevel(self)
        dialog.title(f"Ajouter un problème - Programme {program_name}")
        dialog.geometry("400x300")
        
        ttk.Label(dialog, text=f"Description du problème (Tentative {self.tentatives[program_name]}):").pack(pady=5)
        problem_text = tk.Text(dialog, height=5)
        problem_text.pack(pady=5, padx=5, fill=tk.X)
        
        def save_problem():
            problem = problem_text.get("1.0", tk.END).strip()
            if problem:
                elapsed = time.time() - self.start_time
                hours = int(elapsed // 3600)
                minutes = int((elapsed % 3600) // 60)
                seconds = int(elapsed % 60)
                timestamp = f"{hours:02d}:{minutes:02d}:{seconds:02d}"
                
                # Ajouter le problème au journal avec le numéro de tentative
                self.journal_text.insert(tk.END, 
                    f"[{timestamp}] Programme {program_name} (Tentative {self.tentatives[program_name]}): {problem}\n")
                
                # Mettre à jour le statut du programme
                self.get_program_var(program_name).set("échoué")
                
                dialog.destroy()
        
        ttk.Button(dialog, text="Enregistrer", command=save_problem).pack(pady=10)
        
    def save_verification(self):
        # Mise à jour des vérifications visuelles
        self.test.commande_ok = self.commande_var.get()
        self.test.verrou_porte_ok = self.verrou_var.get()
        self.test.rotation_tambour_ok = self.rotation_check_var.get()
        self.test.chauffe_ok = self.chauffe_check_var.get()
        self.test.essorage_ok = self.essorage_var.get()
        self.test.sechage_ok = self.sechage_var.get()
        
        # Mise à jour des programmes
        self.test.programme_express = self.express_prog_var.get()
        self.test.programme_chauffe = self.chauffe_prog_var.get()
        self.test.programme_rotation = self.rotation_prog_var.get()
        
        # Mise à jour des observations
        observations_text = self.observations_text.get("1.0", tk.END).strip()
        for line in observations_text.split("\n"):
            if ":" in line:
                key, value = line.split(":", 1)
                key = key.strip()
                value = value.strip()
                if key in self.test.observations:
                    self.test.observations[key] = value
        
        # Ajouter le journal des problèmes et les tentatives aux observations
        self.test.observations["journal_problemes"] = self.journal_text.get("1.0", tk.END).strip()
        self.test.observations["tentatives"] = self.tentatives
        
        # Sauvegarde
        self.parent.gestionnaire.mettre_a_jour_test(
            self.appareil.identifiant,
            commande_ok=self.test.commande_ok,
            verrou_porte_ok=self.test.verrou_porte_ok,
            rotation_tambour_ok=self.test.rotation_tambour_ok,
            chauffe_ok=self.test.chauffe_ok,
            essorage_ok=self.test.essorage_ok,
            sechage_ok=self.test.sechage_ok,
            programme_express=self.test.programme_express,
            programme_chauffe=self.test.programme_chauffe,
            programme_rotation=self.test.programme_rotation,
            observations=self.test.observations
        )
        
        messagebox.showinfo("Succès", "Tests enregistrés avec succès!")
        
    def validate_verification(self):
        if not self.test.est_complete():
            messagebox.showerror("Erreur", "Toutes les vérifications doivent être effectuées et réussies!")
            return
            
        self.test.statut = "validé"
        self.parent.gestionnaire.mettre_a_jour_test(
            self.appareil.identifiant,
            statut="validé"
        )
        
        messagebox.showinfo("Succès", "Tests validés avec succès!")
        self.destroy()

    def destroy(self):
        # Appeler la méthode de fermeture de la fenêtre principale
        if hasattr(self.parent, 'fermer_fenetre_test'):
            self.parent.fermer_fenetre_test(self.appareil.identifiant)
        super().destroy() 