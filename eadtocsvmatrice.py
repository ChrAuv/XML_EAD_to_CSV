import eadfiletocsv
import eaddirectorytocsv


# Script de transformation XML EAD vers CSV
# Christophe Auvray, Archives nationales du monde du travail, 2022


prog_launch = True

while prog_launch == True:
    choice = input("Souhaitez-vous parser un ou plusieurs fichiers XML ?\n"
               "A) un seul fichier\n"
               "B) plusieurs fichiers\n"
               "C) quitter le programme\n")
    if choice == "A":
        eadfiletocsv.main()
        prog_launch = False
    elif choice == "B":
        eaddirectorytocsv.main()
        prog_launch = False
    elif choice == "C":
        exit()
    else:
        print("Entrer 'A', 'B' ou 'C'")

input("Appuyer sur Entrée pour quitter.")
exit()

# Autre méthode, moins pratique :
##    if choice == "A":
##        exec(open("./EAD_file_to_CSV_try.py").read())
##        prog_launch = False
##    elif choice == "B":
##        exec(open("./EAD_file_to_CSV_try_multiple.py").read())
##        prog_launch = False
##    else:
##        print("Entrer 'A' ou 'B'")
