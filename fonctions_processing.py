##############################

#####   Plugin RT 2023  ######

##############################
# Fonctions processing

#### IMPORT DES BIBLIOTHEQUES

import datetime as dt
from qgis.PyQt.QtXml import QDomDocument
from qgis.core import Qgis, QgsProject, QgsPrintLayout, QgsLayoutExporter, QgsReadWriteContext
from qgis.PyQt.QtXml import QDomDocument
from qgis.PyQt.QtCore import *
from qgis.utils import iface

# Variables globales
from .variables_globales import *
# Classe grap pour les diagrammes en camembert
from .graph import graph

# Classe de la boite de dialogue
from .interface_graphique_dialogue import CompilDialog

class fct_pro : 

    def __init__ (self, iface) :
    # Constructeur	: definition de la variable d'instance (iface) lorsque la classe fct_pro est apellée.
        self.iface = iface

        self.fct_graph = graph()

        self.dlg = CompilDialog()

    def export (self, c_qgz_rendu, c_qgz_RT, c_qpt, c_pdf,texte_info) :
    # Export d'un bilan en pdf --> ancienne version utilisant le qgz + le qpt.

        projet = QgsProject.instance() # Création d'une instance QgsProject
        projet.read(c_qgz_rendu) # Lecture du projet de rendu et ajout à l'instance QgsProject
        composition = QgsPrintLayout(projet) # Ajout du projet au rendu (la composition) -> necessaire pour le fond de carte et pour les données géo-référencées permettant de calculer les aggregats des tableaux

        document = QDomDocument() # création d'un document XML qui va contenir la mise en page qpt
        template_file = open(c_qpt) # ouverture de la mise en page qpt
        template_content = template_file.read() # lecture de la mise en page
        template_file.close()
        document.setContent(template_content) # ajout de la mise en page au document XML

        composition.loadFromTemplate(document, QgsReadWriteContext()) # ajout du document XML au rendu

        exporter = QgsLayoutExporter(composition) # préparation à l'export
        
        c_pdf_complet = c_pdf + dt.datetime.today().strftime('%Y_%m_%d') + ".pdf" # construction du chemin d'export pdf en ajoutant la date

        exporter.exportToPdf(c_pdf_complet, QgsLayoutExporter.PdfExportSettings()) # export du pdf

        projet.clear() # fermeture du projet rendu

        projet_bis = QgsProject.instance() # réouverture du projet suivi RT
        
        if projet_bis.read(c_qgz_RT) :
            self.iface.messageBar().pushMessage("EXPORT PDF", texte_info, level=Qgis.Success) # Affichage du message de succès
    
    
    def export_V2 (self, c_qgz_rendu, c_qgz_RT, nom_layout, nom_export, c_dossier, texte_info) :
        """Export un bilan au format PDF à partir d'un QGZ seul """

        projet = QgsProject.instance() # Création d'une instance QgsProject
        # projet.read(c_qgz_rendu) # Lecture du projet de rendu et ajout à l'instance QgsProject

        iface.addProject(c_qgz_rendu) # ouverture du projet de rendu --> affiche les décoration par rapport à la méthode .read()
        
        layout = projet.layoutManager().layoutByName(nom_layout) # Récupération de la mise en page
        
        exporter = QgsLayoutExporter(layout) # préparation à l'export
        
        c_pdf_complet = c_dossier + '/' + nom_export + '_' + dt.datetime.today().strftime('%Y_%m_%d') + ".pdf" # construction du chemin d'export pdf en ajoutant la date

        exporter.exportToPdf(c_pdf_complet, QgsLayoutExporter.PdfExportSettings()) # export du pdf

        c_pdf_complet_sauv = c_dossier_sauv + '/' + nom_export + '_' + dt.datetime.today().strftime('%Y_%m_%d') + ".pdf" # construction du chemin d'export pdf en ajoutant la date

        exporter.exportToPdf(c_pdf_complet_sauv, QgsLayoutExporter.PdfExportSettings()) # export du pdf
        # projet.clear() # fermeture du projet rendu

        # projet_bis = QgsProject.instance() # réouverture du projet suivi RT
        
        #if projet_bis.read(c_qgz_RT) :
        if iface.addProject(c_qgz_RT) :
            self.iface.messageBar().pushMessage("EXPORT PDF", texte_info, level=Qgis.Success) # Affichage du message de succès
        else :
            self.iface.messageBar().pushMessage("ERREUR EXPORT", 'Contacter cartographie@fredon-occitanie.fr', level=Qgis.Critical) # Affichage du message de succès

    def preparation_export (self, nom_projet, chemin_dossier) :
        """ Lance l'export du projet choisi par l'utilisateur """
        if nom_projet == 'Xylella_ENR' :
            self.fct_graph.graph_pie_chart_filter(c_xyl_enr_prelevement,'xylella_ENR_ZT', "zone", 'ZT_15-20km') # édition des graphiques en zone ZT
            self.fct_graph.graph_pie_chart_filter(c_xyl_enr_prelevement,'xylella_ENR_ZI', "zone", 'ZI_10-15km') # édition des graphiques en zone ZI
            self.export_V2 (c_xyl_ENR_ZT_rendu_qgz, c_xyl_RT_qgz, 'rendu ENR', 'bilan_xylella_ENR_ZT', chemin_dossier, 'Le bilan Xylella_ENR a bien été exporté !') # Export PDF

        elif nom_projet == 'Xylella_11F' :
            self.fct_graph.graph_pie_chart(c_xyl_11f_prelevement,'xylella_11F')
            self.export_V2 (c_xyl_11F_rendu_qgz, c_xyl_RT_qgz, 'rendu_11F', 'bilan_xylella_11F', chemin_dossier, 'Le bilan Xylella_11F a bien été exporté !')

        elif nom_projet == 'Xylella_30A' :
            self.fct_graph.graph_pie_chart(c_xyl_30a_prelevement,'xylella_30A')
            self.export_V2 (c_xyl_30A_rendu_qgz, c_xyl_RT_qgz, 'rendu_30A', 'bilan_xylella_30A', chemin_dossier, 'Le bilan Xylella_30A a bien été exporté !')

        elif nom_projet == 'Xylella_31A' :
            self.fct_graph.graph_pie_chart(c_xyl_31a_prelevement,'xylella_31A')
            self.export_V2 (c_xyl_31A_rendu_qgz, c_xyl_RT_qgz, 'rendu_31A', 'bilan_xylella_31A', chemin_dossier, 'Le bilan Xylella_31A a bien été exporté !')

        elif nom_projet == 'Xylella_81A' :
            self.fct_graph.graph_pie_chart(c_xyl_81a_prelevement,'xylella_81A')
            self.export_V2 (c_xyl_81A_rendu_qgz, c_xyl_RT_qgz, 'rendu_81A', 'bilan_xylella_81A', chemin_dossier, 'Le bilan Xylella_81A a bien été exporté !')