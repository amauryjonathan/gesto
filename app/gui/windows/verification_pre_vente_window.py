import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
import time

class VerificationPreVenteWindow(tk.Toplevel):
    def __init__(self, parent, appareil):
        super().__init__(parent)
        self.parent = parent
        self.appareil = appareil
        
        self.title(f"Vérification pré-vente - {appareil.identifiant}")
        self.geometry("1000x800")
        
        # Variables pour les timers
        self.timer_running = False
        self.start_time = None
        self.current_program = None
        
        # Créer ou récupérer la vérification existante
        self.verification = self.parent.gestionnaire.get_verification_pre_vente(appareil.identifiant)
        if not self.verification:
            self.verification = self.parent.gestionnaire.ajouter_verification_pre_vente(appareil.identifiant)
        
        self.create_widgets()
        
    def create_widgets(self):
        # Frame principal
        main_frame = ttk.Frame(self, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Vérifications visuelles
        visu_frame = ttk.LabelFrame(main_frame, text="Vérifications visuelles", padding="5")
        visu_frame.pack(fill=tk.X, pady=5)
        
        # Variables pour les cases à cocher
        self.commande_var = tk.BooleanVar(value=self.verification.commande_ok)
        self.verrou_var = tk.BooleanVar(value=self.verification.verrou_porte_ok)
        self.rotation_var = tk.BooleanVar(value=self.verification.rotation_tambour_ok)
        self.chauffe_var = tk.BooleanVar(value=self.verification.chauffe_ok)
        self.essorage_var = tk.BooleanVar(value=self.verification.essorage_ok)
        self.sechage_var = tk.BooleanVar(value=self.verification.sechage_ok)
        
        # Cases à cocher
        ttk.Checkbutton(visu_frame, text="Commande (bandeau)", variable=self.commande_var).pack(anchor=tk.W, pady=2)
        ttk.Checkbutton(visu_frame, text="Verrou de porte", variable=self.verrou_var).pack(anchor=tk.W, pady=2)
        ttk.Checkbutton(visu_frame, text="Rotation du tambour", variable=self.rotation_var).pack(anchor=tk.W, pady=2)
        ttk.Checkbutton(visu_frame, text="Chauffe", variable=self.chauffe_var).pack(anchor=tk.W, pady=2)
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
        self.express_var = tk.StringVar(value=self.verification.programme_express)
        self.chauffe_var = tk.StringVar(value=self.verification.programme_chauffe)
        self.rotation_var = tk.StringVar(value=self.verification.programme_rotation)
        
        # Frame pour chaque programme
        for prog_name, prog_var in [("Express", self.express_var), 
                                  ("Chauffe", self.chauffe_var),
                                  ("Rotation", self.rotation_var)]:
            prog_subframe = ttk.Frame(prog_frame)
            prog_subframe.pack(fill=tk.X, pady=5)
            
            ttk.Label(prog_subframe, text=f"Programme {prog_name}:").pack(side=tk.LEFT, padx=5)
            combo = ttk.Combobox(prog_subframe, textvariable=prog_var,
                               values=["non_testé", "en_cours", "réussi", "échoué"],
                               state="readonly", width=15)
            combo.pack(side=tk.LEFT, padx=5)
            combo.bind("<<ComboboxSelected>>", lambda e, p=prog_name: self.on_program_status_change(p))
            
            # Bouton pour ajouter un problème
            ttk.Button(prog_subframe, text="Ajouter problème",
                      command=lambda p=prog_name: self.add_problem(p)).pack(side=tk.LEFT, padx=5)
        
        # Journal des problèmes
        journal_frame = ttk.LabelFrame(main_frame, text="Journal des problèmes", padding="5")
        journal_frame.pack(fill=tk.BOTH, expand=True, pady=5)
        
        self.journal_text = tk.Text(journal_frame, height=10)
        self.journal_text.pack(fill=tk.BOTH, expand=True)
        
        # Observations
        obs_frame = ttk.LabelFrame(main_frame, text="Observations", padding="5")
        obs_frame.pack(fill=tk.BOTH, expand=True, pady=5)
        
        self.observations_text = tk.Text(obs_frame, height=10)
        self.observations_text.pack(fill=tk.BOTH, expand=True)
        self.observations_text.insert("1.0", "\n".join(f"{k}: {v}" for k, v in self.verification.observations.items()))
        
        # Boutons
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=tk.X, pady=10)
        
        ttk.Button(button_frame, text="Enregistrer", command=self.save_verification).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Valider", command=self.validate_verification).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Fermer", command=self.destroy).pack(side=tk.RIGHT, padx=5)
        
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
            
    def on_program_status_change(self, program_name):
        new_status = self.get_program_var(program_name).get()
        
        # Si on met un programme en cours
        if new_status == "en_cours":
            # Arrêter le programme précédent s'il existe
            if self.current_program and self.current_program != program_name:
                self.get_program_var(self.current_program).set("non_testé")
                # Ajouter une note dans le journal
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
            return self.express_var
        elif program_name == "Chauffe":
            return self.chauffe_var
        elif program_name == "Rotation":
            return self.rotation_var
            
    def add_problem(self, program_name):
        if not self.timer_running:
            messagebox.showwarning("Attention", "Veuillez démarrer le timer avant d'ajouter un problème")
            return
            
        # Créer une fenêtre de dialogue pour saisir le problème
        dialog = tk.Toplevel(self)
        dialog.title(f"Ajouter un problème - Programme {program_name}")
        dialog.geometry("400x300")
        
        ttk.Label(dialog, text="Description du problème:").pack(pady=5)
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
                
                # Ajouter le problème au journal
                self.journal_text.insert(tk.END, 
                    f"[{timestamp}] Programme {program_name}: {problem}\n")
                
                # Mettre à jour le statut du programme
                self.get_program_var(program_name).set("échoué")
                
                dialog.destroy()
        
        ttk.Button(dialog, text="Enregistrer", command=save_problem).pack(pady=10)
        
    def save_verification(self):
        # Mise à jour des vérifications visuelles
        self.verification.commande_ok = self.commande_var.get()
        self.verification.verrou_porte_ok = self.verrou_var.get()
        self.verification.rotation_tambour_ok = self.rotation_var.get()
        self.verification.chauffe_ok = self.chauffe_var.get()
        self.verification.essorage_ok = self.essorage_var.get()
        self.verification.sechage_ok = self.sechage_var.get()
        
        # Mise à jour des programmes
        self.verification.programme_express = self.express_var.get()
        self.verification.programme_chauffe = self.chauffe_var.get()
        self.verification.programme_rotation = self.rotation_var.get()
        
        # Mise à jour des observations
        observations_text = self.observations_text.get("1.0", tk.END).strip()
        for line in observations_text.split("\n"):
            if ":" in line:
                key, value = line.split(":", 1)
                key = key.strip()
                value = value.strip()
                if key in self.verification.observations:
                    self.verification.observations[key] = value
        
        # Ajouter le journal des problèmes aux observations
        self.verification.observations["journal_problemes"] = self.journal_text.get("1.0", tk.END).strip()
        
        # Sauvegarde
        self.parent.gestionnaire.mettre_a_jour_verification_pre_vente(
            self.appareil.identifiant,
            commande_ok=self.verification.commande_ok,
            verrou_porte_ok=self.verification.verrou_porte_ok,
            rotation_tambour_ok=self.verification.rotation_tambour_ok,
            chauffe_ok=self.verification.chauffe_ok,
            essorage_ok=self.verification.essorage_ok,
            sechage_ok=self.verification.sechage_ok,
            programme_express=self.verification.programme_express,
            programme_chauffe=self.verification.programme_chauffe,
            programme_rotation=self.verification.programme_rotation,
            observations=self.verification.observations
        )
        
        messagebox.showinfo("Succès", "Vérifications enregistrées avec succès!")
        
    def validate_verification(self):
        if not self.verification.est_complete():
            messagebox.showerror("Erreur", "Toutes les vérifications doivent être effectuées et réussies!")
            return
            
        self.verification.statut = "validé"
        self.parent.gestionnaire.mettre_a_jour_verification_pre_vente(
            self.appareil.identifiant,
            statut="validé"
        )
        
        messagebox.showinfo("Succès", "Vérifications validées avec succès!")
        self.destroy() 