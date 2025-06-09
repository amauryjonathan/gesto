import sys
import os
import traceback
sys.path.append(os.path.abspath(os.path.dirname(__file__)))

from app.gestion.gestionnaire import GestionnaireAppareils
from app.gui.main_window import MainWindow

if __name__ == "__main__":
    try:
        gestionnaire = GestionnaireAppareils()
        app = MainWindow(gestionnaire)
        app.mainloop()
    except Exception as e:
        print('Erreur attrapée :')
        traceback.print_exc() 