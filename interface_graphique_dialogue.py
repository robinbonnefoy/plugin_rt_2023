from msilib.schema import Dialog
import os

from qgis.PyQt import uic
from qgis.PyQt import QtWidgets

# Import de la classe graphique de dialogue définie dans "Interface_graphique.py"
from .Interface_graphique import Ui_Dialog

FORM_CLASS_1 = Ui_Dialog


# Compilation de la classe de "Interface_graphique.py" avec la classe parent QtWidgets contenant
# les fonctions de bases
class CompilDialog(QtWidgets.QDialog, FORM_CLASS_1):
    def __init__(self, parent=None):
        """Constructor."""
        super(CompilDialog, self).__init__(parent)
        # Set up the user interface from Designer through FORM_CLASS.
        # After self.setupUi() you can access any designer object by doing
        # self.<objectname>, and you can use autoconnect slots - see
        # http://qt-project.org/doc/qt-4.8/designer-using-a-ui-file.html
        # #widgets-and-dialogs-with-auto-connect
        self.setupUi(self)