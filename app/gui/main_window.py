import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
from app.gui.windows.ajout_window import AjoutWindow
from app.gui.windows.technicien_detail_window import DetailWindow
from app.gui.windows.test_window import TestWindow

class MainWindow(tk.Tk):
    def __init__(self, gestionnaire):
        super().__init__()
        self.gestionnaire = gestionnaire
        self.geometry("1200x800")
        self.title("Gesto - Dashboard")
        self.selected_appareil_id = None
        self.create_widgets()

    def create_widgets(self):
        # Barre latérale
        sidebar = ttk.Frame(self)
        sidebar.pack(side="left", fill="y")
        self.section_var = tk.StringVar(value="Présentation")
        sections = ["Présentation", "Dépannage", "Tests", "Paramètres"]
        for section in sections:
            btn = ttk.Button(sidebar, text=section, width=20,
                            command=lambda s=section: self.show_section(s))
            btn.pack(pady=10, padx=10)

        # Barre supérieure
        topbar = ttk.Frame(self)
        topbar.pack(side="top", fill="x")
        ttk.Label(topbar, text="GESTO", font=("Arial", 18)).pack(side="left", padx=20, pady=10)
        ttk.Entry(topbar, width=40).pack(side="left", padx=20)
        ttk.Button(topbar, text="Ajouter un appareil", command=self.ouvrir_ajout).pack(side="right", padx=20)

        # Zone principale
        self.main = ttk.Frame(self)
        self.main.pack(side="left", fill="both", expand=True, padx=20, pady=20)
        self.show_section("Présentation")

    def show_section(self, section):
        for widget in self.main.winfo_children():
            widget.destroy()
        if section == "Présentation":
            ttk.Label(self.main, text="Liste des appareils", font=("Arial", 16)).pack(pady=10)
            columns = ("identifiant", "type", "marque", "reference", "numero_serie", "date_arrivee", "statut")
            self.tree = ttk.Treeview(self.main, columns=columns, show="headings", height=15)
            for col in columns:
                self.tree.heading(col, text=col.capitalize())
                self.tree.column(col, width=120)
            self.tree.pack(fill=tk.BOTH, expand=True)
            self.tree.bind("<<TreeviewSelect>>", self.on_tree_select)
            self.refresh_liste()
        elif section == "Dépannage":
            ttk.Label(self.main, text="Section Dépannage", font=("Arial", 16)).pack(pady=10)
            ttk.Button(self.main, text="Ouvrir Test pour l'appareil sélectionné", command=self.open_test).pack(pady=20)
        elif section == "Tests":
            ttk.Label(self.main, text="Section Tests", font=("Arial", 16)).pack(pady=20)
        elif section == "Paramètres":
            ttk.Label(self.main, text="Paramètres de l'application", font=("Arial", 16)).pack(pady=20)

    def refresh_liste(self):
        if hasattr(self, 'tree'):
            for item in self.tree.get_children():
                self.tree.delete(item)
            for type_app, appareils in self.gestionnaire.appareils.items():
                for appareil in appareils:
                    self.tree.insert("", tk.END, values=(
                        appareil.identifiant,
                        type_app.replace("_", " ").title(),
                        appareil.marque,
                        appareil.reference,
                        appareil.numero_serie,
                        appareil.date_arrivee,
                        appareil.statut
                    ))

    def on_tree_select(self, event):
        selection = self.tree.selection()
        if selection:
            item = self.tree.item(selection[0])
            self.selected_appareil_id = item['values'][0]

    def ouvrir_ajout(self):
        AjoutWindow(self, self.refresh_liste)

    def open_test(self):
        if self.selected_appareil_id:
            TestWindow(self, self.selected_appareil_id)
        else:
            messagebox.showwarning("Attention", "Veuillez sélectionner un appareil") 