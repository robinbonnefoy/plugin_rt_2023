##############################

#####   Plugin RT 2023  ######

##############################
# Programme principal du plugin

### Importation des moules

# Bibliothèques générales
import os
import inspect
from PyQt5.QtWidgets import QAction, QFileDialog
from PyQt5.QtGui import QIcon
import os.path

# Ressources Qt designer depuis le fichier resources.py
from .ressources import *

# Classe de la boite de dialogue
from .interface_graphique_dialogue import CompilDialog

# Classe des fonctions processing
from .fonctions_processing import fct_pro

cmd_folder = os.path.split(inspect.getfile(inspect.currentframe()))[0]

class main:
        
    def __init__(self, iface):
    # Constructeur    : definition de la variable d'instance (iface) lorsque la classe maj_rt est apellée. 
        self.iface = iface
        # Vérifie si le plugin a été demarré une première fois dans l'interface QGIS.
        # Doit être initialisé dans initGui() pour survivre au rechargement du projet.
        self.first_start = None

        # Initialisez l'attribut pour stocker le chemin sélectionné
        self.selected_directory = ""

        self.dlg = CompilDialog() # Instanciation de la classe de dialogue
        self.fct = fct_pro(self.iface)  # Instanciation de la classe des fonctions processing

    def initGui(self):
    # Ajout des commandes du plugin (boutons, menus...) à l'interface de QGIS
        icon = os.path.join(os.path.join(cmd_folder, 'image/logo.png'))
        self.action = QAction(QIcon(icon), 'FREDON_RT', self.iface.mainWindow())
        self.action.triggered.connect(self.run)
        self.iface.addPluginToMenu('&FREDON_RT', self.action)
        self.iface.addToolBarIcon(self.action)

        # Va être mis à False au début du run()
        self.first_start = True

    def unload(self):
    # Suppression du menu, du bouton et du logo du plugin de l'interface QGIS
        self.iface.removeToolBarIcon(self.action)
        self.iface.removePluginMenu('&FREDON_RT', self.action)  
        del self.action

    def fermer (self):
        self.dlg.close()
    
    def open_dialog(self):
        """ Ouvre la fenêtre de dialogue pour sélectionner un dossier 
        et met à jour le chemin dans le conteneur ligne_chemin.        
        """
        # Créez une instance de QFileDialog
        dialog = QFileDialog()

        # Définissez le mode de sélection sur les dossiers seulement
        dialog.setFileMode(QFileDialog.Directory)

        # Ouvrez la boîte de dialogue et récupérez le chemin sélectionné
        self.selected_directory = dialog.getExistingDirectory(None, "Sélectionnez un dossier", "/")

        # Affichez le chemin sélectionné dans la console
        self.dlg.ligne_chemin.setText(self.selected_directory)
        dialog.accept() # fermer la fenêtre une fois le chemin sélectionné mis à jour
    
    def verif_import(self) :
        """
        Vérifie si un projet à bien été sélectionné et que le chemin du dossier est valide avant de lancer l'export.
        """
        chemin_dossier = self.dlg.ligne_chemin.text() # chemin saisi dans le QLineEdit
        nom_projet = self.dlg.choix_projet.currentText() # nom selectionné dans le QComboBox
        
        isExist = os.path.exists(chemin_dossier) # test si le chemin existe dans l'ordinateur.
        
        if nom_projet == "" : # si aucun projet projet n'est sélectionné --> affiche un message d'erreur
            self.dlg.ligne_info.setText("Aucun projet n'est sélectionné.")
            self.dlg.ligne_info.setStyleSheet("color: red;")

        elif not isExist : # si le chemin du dossier n'existe pas ou est vide --> affiche un message d'erreur
            self.dlg.ligne_info.setText('Le chemin du dossier est invalide.')
            self.dlg.ligne_info.setStyleSheet("color: red;")
        
        else : # si tout est ok --> lancement de l'export
            self.dlg.ligne_info.setText("Demande export validée.")
            self.dlg.ligne_info.setStyleSheet("color: green;")
            self.dlg.ligne_info.update()
            self.fct.preparation_export(nom_projet, chemin_dossier)

    def run(self):
        
        ### Boite de dialogue de la fenêtre principale
        self.dlg.setWindowTitle('FREDON OCCITANIE - RT') # Titre de la boite de dialogue
        
        self.dlg.ligne_chemin.setText(self.selected_directory)
        # Connecter les boutons
        self.dlg.bouton_fermer.clicked.connect(self.fermer) # fermer le plugin
        self.dlg.bouton_import.clicked.connect(self.verif_import) # lancement de la vérification lorsque l'export est demandé
        self.dlg.choix_chemin.clicked.connect(self.open_dialog) # ouverture de l'explorateur de fichiers
        
        self.dlg.show() # Afficher la boite de dialogue
        
        # Exécuter la boite de dialogue dans une boucle sans fin
        result = self.dlg.exec_()