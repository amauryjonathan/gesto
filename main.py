import sys
import os
sys.path.append(os.path.abspath(os.path.dirname(__file__)))

from app.gestion.gestionnaire import GestionnaireAppareils
from app.gui.main_window import MainWindow

if __name__ == "__main__":
    gestionnaire = GestionnaireAppareils()
    app = MainWindow(gestionnaire)
    app.mainloop() 