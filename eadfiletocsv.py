# linter : http://pep8online.com/
# permet de parser le fichier XML :
# https://docs.python.org/3/library/xml.etree.elementtree.html
from xml.etree import ElementTree
# permet de créer le fichier CSV :
# https://docs.python.org/fr/3/library/csv.html?highlight=csv
from csv import writer
# permet de mesurer le temps :
# https://docs.python.org/fr/3/library/time.html?highlight=time#module-time
from time import time
# permet de communiquer avec le système de fichiers de l'ordinateur :
# https://docs.python.org/fr/3/library/os.html
from os import getcwd


# Script de transformation XML EAD vers CSV
# Christophe Auvray, Archives nationales du monde du travail, 2022


def main():
    """Cette fonction permet l'intégration du script dans
    eadtocsvmatrice.py"""
    # Décommenter main() tout en bas pour rendre le programme indépendant
    def create_column_value(parent, XPath):
        # Une indentation = 4 espaces
        """Cette fonction crée une cellule à partir de la valeur d'un élément EAD.
        Si l'élément est trouvé (try), la cellule est créée avec sa valeur.
        Si l'élément n'est pas trouvé (except), la cellule est créée vide."""
        try:
            element = parent.find(XPath)
            # Permet de prendre en compte les balises <p>, <emph>, <list>, etc. :
            element = ''.join(element.itertext())
            # Supprimer les espaces en trop avec les méthodes split() et join() :
            element = ' '.join(element.split())
        except:
            element = ''
        # La variable va retourner la valeur de l'élément :
        return element
        # Sauter deux espaces après avoir défini une fonction


    def create_column_attribute(parent, XPath):
        """Cette fonction crée une cellule à partir de la valeur d'un attribut EAD.
        Si l'attribut est trouvé (try), la cellule est créée avec sa valeur.
        Si l'attribut n'est pas trouvé (except), la cellule est créée vide."""
        try:
            valeur_attribut = parent.attrib[XPath]
        except:
            valeur_attribut = ''
        # La variable va retourner la valeur de l'attribut :
        return valeur_attribut


    print("Ce script va transformer un fichier XML EAD en un tableau CSV avec "
          "une ligne par composant.\n"
          "Ce fichier doit se trouver dans un répertoire 'EAD' situé au même "
          "niveau que le présent script.")

    # Sélectionner le fichier XML (input)
    fichier_xml = input("entrer le nom du fichier XML EAD à parser, avec son extension.\n")
    # Le premier élément indique le sous-dossier. Coder "./" en premier élément
    # s'il n'y a pas de sous-dossier.
    fichier_xml = "./EAD/" + fichier_xml
    
    input("Appuyer sur Entrée pour continuer")

    # Créer le fichier CSV (output), dire qu'on veut l'écrire de A à Z ("w"),
    # encodé en UTF-8. fichier sera dans la variable "f"
    with open('output_EAD_file.csv', 'w', encoding="utf-8", newline="") as f:
        # séparateur point-virgule
        write_file = writer(f, delimiter=';')

        # Parser le fichier XML
        tree = ElementTree.parse(fichier_xml)

        # Définir les en-têtes de colonnes
        headers = ["cote", "ark", "niveau", "altrender", "intitule", "date",
                   "presentation du contenu", "biographie du producteur", "métrage",
                   "conditonnement", "état de classement"]

        # Ecrire les en-têtes de colonne
        write_file.writerow(headers)

        # Placer un compteur de composants
        i = 1
        # Heure de début
        time_begin = time()

        # contrairement à la majorité des autres langages, en Python,
        # une boucle for va forcément itérer via une collection
        # (liste, dictionnaire, string, etc.) - équivalent d'un for-each.

        # Pour une boucle "for" classique :
        # for i in range(0, 5, 1):
        #     print(i) # -> affiche de 0 à 4 par pas de 1 (fin - 1)

        # "composant" est une variable qui se déclare (se crée) et s'initie
        # (reçoit une valeur) en même temps.
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
            # ici, je concaténe la valeur de l'élément et la
            # valeur de l'attribut pour avoir l'unité indiquée
            extent = create_column_value(composant, './/did/physdesc/extent') + " " + create_column_attribute(composant.find('.//did/physdesc/extent'), 'unit')
            # Pour remplacer le point par une virgule, méthode replace() :
            extent = extent.replace(".",",")
            container = create_column_value(composant, './/container')
            arrangement = create_column_value(composant, './/arrangement')
            # Augmenter le compteur de 1
            i += 1
            # écriture de la ligne dans le CSV
            csv_line = [unitid, ark, c_level, altrender, unittitle, unitdate,
                        scopecontent, bioghist, extent, container, arrangement]
            # ajouter une nouvelle ligne au fichier CSV avec les données
            write_file.writerow(csv_line)

    # fermer le fichier CSV (pas indispensable ici), "with" le fait lui-même
    # f.close()

    # Heure de fin
    time_end = time()

    # Temps total
    total_time = time_end - time_begin

    # Conclusion :
    print(f"Un total de {i} composants a été parsé en {total_time} "
          f"secondes. Le fichier produit se trouve dans {getcwd()}. "
          f"Il comporte {len(headers)} colonnes.")


##main()
