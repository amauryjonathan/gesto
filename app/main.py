from gui.main_window import MainWindow
from gestion.gestionnaire import GestionnaireAppareils

def main():
    gestionnaire = GestionnaireAppareils()
    app = MainWindow(gestionnaire)
    app.mainloop()

if __name__ == "__main__":
    main() 