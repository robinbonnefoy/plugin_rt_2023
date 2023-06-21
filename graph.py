
##############################

#####   Plugin RT 2023  ######

##############################
# Fonction pour tracer les graphiques

### Import des bibliothèques

from .variables_globales import *
from datetime import date
from qgis.core import QgsVectorLayer
import matplotlib.pyplot as plt


# Définition de la classe pour tracer le graphique
class graph :    

    def graph_pie_chart (self, chemin_prelevement, nom) :
        """
        Trace deux diagrammes en cammembert de la répartition des prélèvements et des végétaux prélevés par espèce végétale. Les données sont issues d'une couche de prélèvements Xylella.
        """

        ### Chargement de la couche de prélèvement

        layer_prelevement = QgsVectorLayer(chemin_prelevement, "prelevement", "ogr")

        # Récupération des index des champs d'intérêts

        index_prel_espece = layer_prelevement.dataProvider().fieldNameIndex("espece")
        index_prel_genre = layer_prelevement.dataProvider().fieldNameIndex("genre")
        index_prel_nb = layer_prelevement.dataProvider().fieldNameIndex("nb")
        index_prel_prel_fauch = layer_prelevement.dataProvider().fieldNameIndex("prel_fauch")
        index_prel_hote_spe = layer_prelevement.dataProvider().fieldNameIndex("hote_spe")
        index_prel_sympto = layer_prelevement.dataProvider().fieldNameIndex("sympto")

        ### Construction du jeu de données brut 

        D_prelevement = {} # Dictionnaire des données : {"genre espece" : [nb_prelevemment, nb_vegetaux_preleves]}

        for feature_prel in layer_prelevement.getFeatures() : # pour l'ensemble des prélèvements
            attrs_prel = feature_prel.attributes() # récupération des attributs du prélèvement

            if attrs_prel[index_prel_prel_fauch] == 'Prélèvement végétal' : # si le prélèvement est bien un prélèvement

                # construction du nom du végétal
                nom_vegetal = attrs_prel[index_prel_genre].strip() + ' ' + attrs_prel[index_prel_espece].strip() # concaténation du genre et de l'espèce en supprimant les espaces
                nom_vegetal = nom_vegetal.lower() # mise en minuscule --> insensible à la casse

                if nom_vegetal in D_prelevement : # si l'espèce est déjà dans le dictionnaire

                    nb_prel = D_prelevement[nom_vegetal][0] # récupération du nb de prélèvement avant MAJ
                    nb_veg = D_prelevement[nom_vegetal][1] # récupération du nb de végétaux prélevés avant MAJ

                    nb_prel_ac = nb_prel + 1 # MAJ du nombre de prelevement
                    nb_veg_ac = nb_veg + attrs_prel[index_prel_nb] # MAJ du nombre de végétaux prélevés

                    D_prelevement[nom_vegetal] = [nb_prel_ac, nb_veg_ac] # mise à jour des valeurs dans le dictionnaire
        
                else : # sinon l'espèce n'est pas dans le dictionnaire

                    D_prelevement[nom_vegetal] = [1, attrs_prel[index_prel_nb]] # ajout de l'espece dans le dictionnaire avec les valeurs


        ### Construction du jeu de données pour plt

        ## Liste brutes
        L_espece = [] # liste des espèces 
        L_nb_prelevement = [] # liste des nombres de prélèvements
        L_nb_vegetaux_prel = [] # liste des nombres de vegétaux prélevés ..

        for cle, valeur in D_prelevement.items() : # pour l'ensemble des éléments du dictionnaire
            L_espece.append(cle.capitalize()) 
            L_nb_prelevement.append(valeur[0])
            L_nb_vegetaux_prel.append(valeur[1])

        ## Listes simplifiés : les espèces avec une proportion <10% sont rassemblés dans une catégorie 'Autres'

        nb_espece = len(L_espece) # nombre d'espèces dans le dictionnaire
        nb_vegetaux_total = sum(L_nb_vegetaux_prel) # nombre de vegétaux total prélevés
        nb_prelevement_total = sum(L_nb_prelevement) # nombre total de prélèvements

        nb_prel_autres = 0
        nb_veg_autres = 0

        L_espece_prel_f = []
        L_espece_veg_f = []
        L_nb_prelevement_f = []
        L_nb_vegetaux_prel_f = []

        # Jeu de données du nombre de végétaux prélevés et nombre de prélèvement
        for k in range(nb_espece) :
    
            nb_veg = L_nb_vegetaux_prel[k]
            nb_prel = L_nb_prelevement[k]

            if nb_prel / nb_prelevement_total < 0.1 : # critère de proportion uniquement pris sur les prélèvements
                nb_veg_autres += nb_veg
                nb_prel_autres += nb_prel
            else : 
                L_espece_veg_f.append(L_espece[k])
                L_nb_vegetaux_prel_f.append(L_nb_vegetaux_prel[k])
                L_espece_prel_f.append(L_espece[k])
                L_nb_prelevement_f.append(L_nb_prelevement[k])

        L_espece_veg_f.append('Autres espèces')
        L_nb_vegetaux_prel_f.append(nb_veg_autres)
        L_espece_prel_f.append('Autres espèces')
        L_nb_prelevement_f.append(nb_prel_autres)

        today = date.today()
        date_au = today.strftime("%Y-%m-%d")

        output_dir_veg = folder_graph + nom + '_veg_' + date_au +'.png'
        output_dir_prel = folder_graph + nom + '_prel_' + date_au +'.png'

        
        plt.pie(L_nb_vegetaux_prel_f, labels=L_espece_veg_f, autopct=lambda pct: f"{pct:.1f}%\n({int(round(pct/100*nb_vegetaux_total))} végétaux)", textprops={'fontsize': 11})
        plt.savefig(output_dir_veg, dpi=300, bbox_inches='tight')
        plt.close()
        plt.pie(L_nb_prelevement_f, labels=L_espece_prel_f, autopct=lambda pct: f"{pct:.1f}%\n({int(round(pct/100*nb_prelevement_total))} prélèvements)", textprops={'fontsize': 11})
        plt.savefig(output_dir_prel, dpi=300, bbox_inches='tight')
        plt.close()

    def graph_pie_chart_filter (self, chemin_prelevement, nom, field_filter, expression) :
        """
        Trace deux diagrammes en cammembert de la répartition des prélèvements et des végétaux prélevés par espèce végétale. Les données sont issues d'une couche de prélèvements Xylella et sont flitrées sur le champ "field_filter" et le critère choisi (expression).
        """

        ### Chargement de la couche de prélèvement

        layer_prelevement = QgsVectorLayer(chemin_prelevement, "prelevement", "ogr")

        # Récupération des index des champs d'intérêts

        index_prel_espece = layer_prelevement.dataProvider().fieldNameIndex("espece")
        index_prel_genre = layer_prelevement.dataProvider().fieldNameIndex("genre")
        index_prel_nb = layer_prelevement.dataProvider().fieldNameIndex("nb")
        index_prel_prel_fauch = layer_prelevement.dataProvider().fieldNameIndex("prel_fauch")
        index_prel_field_filter = layer_prelevement.dataProvider().fieldNameIndex(field_filter)

        ### Construction du jeu de données brut 

        D_prelevement = {} # Dictionnaire des données : {"genre espece" : [nb_prelevemment, nb_vegetaux_preleves]}

        for feature_prel in layer_prelevement.getFeatures() : # pour l'ensemble des prélèvements
            attrs_prel = feature_prel.attributes() # récupération des attributs du prélèvement

            if attrs_prel[index_prel_prel_fauch] == 'Prélèvement végétal' and attrs_prel[index_prel_field_filter] == expression : # si le prélèvement est bien un prélèvement

                # construction du nom du végétal
                nom_vegetal = attrs_prel[index_prel_genre].strip() + ' ' + attrs_prel[index_prel_espece].strip() # concaténation du genre et de l'espèce en supprimant les espaces
                nom_vegetal = nom_vegetal.lower() # mise en minuscule --> insensible à la casse

                if nom_vegetal in D_prelevement : # si l'espèce est déjà dans le dictionnaire

                    nb_prel = D_prelevement[nom_vegetal][0] # récupération du nb de prélèvement avant MAJ
                    nb_veg = D_prelevement[nom_vegetal][1] # récupération du nb de végétaux prélevés avant MAJ

                    nb_prel_ac = nb_prel + 1 # MAJ du nombre de prelevement
                    nb_veg_ac = nb_veg + attrs_prel[index_prel_nb] # MAJ du nombre de végétaux prélevés

                    D_prelevement[nom_vegetal] = [nb_prel_ac, nb_veg_ac] # mise à jour des valeurs dans le dictionnaire
        
                else : # sinon l'espèce n'est pas dans le dictionnaire

                    D_prelevement[nom_vegetal] = [1, attrs_prel[index_prel_nb]] # ajout de l'espece dans le dictionnaire avec les valeurs


        ### Construction du jeu de données pour plt

        ## Liste brutes
        L_espece = [] # liste des espèces 
        L_nb_prelevement = [] # liste des nombres de prélèvements
        L_nb_vegetaux_prel = [] # liste des nombres de vegétaux prélevés ..

        for cle, valeur in D_prelevement.items() : # pour l'ensemble des éléments du dictionnaire
            L_espece.append(cle.capitalize()) 
            L_nb_prelevement.append(valeur[0])
            L_nb_vegetaux_prel.append(valeur[1])

        ## Listes simplifiés : les espèces avec une proportion <10% sont rassemblés dans une catégorie 'Autres'

        nb_espece = len(L_espece) # nombre d'espèces dans le dictionnaire
        nb_vegetaux_total = sum(L_nb_vegetaux_prel) # nombre de vegétaux total prélevés
        nb_prelevement_total = sum(L_nb_prelevement) # nombre total de prélèvements

        nb_prel_autres = 0
        nb_veg_autres = 0

        L_espece_prel_f = []
        L_espece_veg_f = []
        L_nb_prelevement_f = []
        L_nb_vegetaux_prel_f = []

        # Jeu de données du nombre de végétaux prélevés et nombre de prélèvement
        for k in range(nb_espece) :
    
            nb_veg = L_nb_vegetaux_prel[k]
            nb_prel = L_nb_prelevement[k]

            if nb_prel / nb_prelevement_total < 0.1 : # critère de proportion uniquement pris sur les prélèvements
                nb_veg_autres += nb_veg
                nb_prel_autres += nb_prel
            else : 
                L_espece_veg_f.append(L_espece[k])
                L_nb_vegetaux_prel_f.append(L_nb_vegetaux_prel[k])
                L_espece_prel_f.append(L_espece[k])
                L_nb_prelevement_f.append(L_nb_prelevement[k])

        L_espece_veg_f.append('Autres espèces')
        L_nb_vegetaux_prel_f.append(nb_veg_autres)
        L_espece_prel_f.append('Autres espèces')
        L_nb_prelevement_f.append(nb_prel_autres)

        today = date.today()
        date_au = today.strftime("%Y-%m-%d")

        output_dir_veg = folder_graph + nom + '_veg_' + date_au +'.png'
        output_dir_prel = folder_graph + nom + '_prel_' + date_au +'.png'

        
        plt.pie(L_nb_vegetaux_prel_f, labels=L_espece_veg_f, autopct=lambda pct: f"{pct:.1f}%\n({int(round(pct/100*nb_vegetaux_total))} végétaux)", textprops={'fontsize': 11})
        plt.savefig(output_dir_veg, dpi=300, bbox_inches='tight')
        plt.close()
        plt.pie(L_nb_prelevement_f, labels=L_espece_prel_f, autopct=lambda pct: f"{pct:.1f}%\n({int(round(pct/100*nb_prelevement_total))} prélèvements)", textprops={'fontsize': 11})
        plt.savefig(output_dir_prel, dpi=300, bbox_inches='tight')
        plt.close()
    
    ## Fin fct graph_pie_chart

##Fin classe graph