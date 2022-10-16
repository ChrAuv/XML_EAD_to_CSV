from xml.etree import ElementTree
from csv import writer
from time import time
# J'importe ici l''ensemble de "os"
import os
# https://docs.python.org/fr/3/library/pathlib.html
from pathlib import Path


# Script de transformation XML EAD vers CSV
# Christophe Auvray, Archives nationales du monde du travail, 2022


def main():
    """Cette fonction permet l'intégration du script dans
    eadtocsvmatrice.py"""
    # Décommenter main() tout en bas pour rendre le programme indépendant
    def create_column_value(parent, XPath):
        """Cette fonction crée une cellule à partir de la valeur d'un élément EAD.
        Si l'élément est trouvé (try), la cellule est créée avec sa valeur.
        Si l'élément n'est pas trouvé (except), la cellule est créée vide."""
        try:
            element = parent.find(XPath)
            element = ''.join(element.itertext())
            element = ' '.join(element.split())
        except:
            element = ''
        return element


    def create_column_attribute(parent, XPath):
        """Cette fonction crée une cellule à partir de la valeur d'un attribut EAD.
        Si l'attribut est trouvé (try), la cellule est créée avec sa valeur.
        Si l'attribut n'est pas trouvé (except), la cellule est créée vide."""
        try:
            valeur_attribut = parent.attrib[XPath]
        except:
            valeur_attribut = ''
        return valeur_attribut
            

    print("Ce script va transformer un ensemble de fichiers XML EAD "
          "en un tableau CSV avec une ligne par composant. "
          "Les fichiers doivent se trouver dans le répertoire 'EAD' situé "
          " au même niveau que le présent script.")

    # Sélectionner le répertoire (directory)
    xml_directory = './EAD'

    input("Appuyer sur Entrée pour continuer")

    # Créer le fichier CSV

    with open('output_EAD_multiple.csv', 'w', encoding="utf-8", newline="") as f:
        write_file = writer(f, delimiter=';')

        # Définir les en-têtes de colonnes
        headers = ["nom", "cote", "ark", "niveau", "altrender", "intitule", "date",
                   "presentation du contenu", "biographie du producteur", "métrage",
                   "conditonnement", "état de classement"]

        # Ecrire les en-têtes de colonne
        write_file.writerow(headers)

        # Dire que l'on veut travailler sur chaque fichier XML du répertoire
        # Si j'utilise print(xml_files_list) je constate que cette liste fonctionne
        xml_files_list = list(map(str,Path(xml_directory).glob('**/*.xml')))

        # Placer un compteur de composants
        # pour compter tous les <c>
        i = 1
        # pour compter tous les articles
        art = 1
        # Heure de début
        time_begin = time()

        # Parser chaque fichier XML
        for xml_file in xml_files_list:
            # Le nom de chaque fichier traité va s'afficher
            print(xml_file)
            # L'arbre XML est créé et parsé
            tree = ElementTree.parse(xml_file)
            # La première colonne comprendra le nom du fichier
            name = os.path.basename(xml_file)

            # Parser à l'intérieur de chaque fichier XML
            for composant in tree.findall(".//c"):
                # A chaque fois, appel de la fonction create_column_value() ou create_column_attribute()
                unitid = create_column_value(composant, './/did/unitid')
                # On affiche la cote traitée
                print(unitid)
                ark = create_column_attribute(composant, 'id')
                c_level = create_column_attribute(composant, 'level')
                altrender = create_column_attribute(composant, 'altrender')
                unittitle = create_column_value(composant, './/did/unittitle')
                unitdate = create_column_value(composant, './/did/unitdate')
                scopecontent = create_column_value(composant, './/scopecontent')
                bioghist = create_column_value(composant, './/bioghist')
                extent = create_column_value(composant, './/did/physdesc/extent') + " " + create_column_attribute(composant.find('.//did/physdesc/extent'), 'unit')
                # Pour remplacer le point par une virgule, méthode replace() :
                extent = extent.replace(".",",")
                container = create_column_value(composant, './/container')
                arrangement = create_column_value(composant, './/arrangement')
                # Augmenter le compteur de 1
                i += 1
                if c_level == "file":
                    art += 1
                # écriture de la ligne dans le CSV
                csv_line = [name, unitid, ark, c_level, altrender, unittitle, unitdate,
                        scopecontent, bioghist, extent, container, arrangement]
                # ajouter une nouvelle ligne au fichier CSV avec les données
                write_file.writerow(csv_line)

    # fermer le fichier CSV (pas indispensable avec "with")
    # f.close()

    # Heure de fin
    time_end = time()

    # Temps total
    total_time = time_end - time_begin

    print(f"Un total de {i} composants a été parsé (dont {art} articles), "
          f"dans {len(xml_files_list)} IR en {total_time} "
          f"secondes. Le fichier produit se trouve dans {os.getcwd()}. "
          f"Il comporte {len(headers)} colonnes.")

main()
