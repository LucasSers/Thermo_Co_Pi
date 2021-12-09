# Récupère la température et la stocke dans un fichier .csv
# dans le format suivant :
# jj-mm-aaaa hh:mm:ss;temp(en°C)

from w1thermsensor import W1ThermSensor
import datetime, time, os


# Récupère la température renvoyée par la sonde
# et gère les erreurs de relevé
def getTemp() :
    tempCelsius = capteur.get_temperature()
    while ( tempInvalide(tempCelsius) ) : 
        print("Erreur! Température incohérente detectée lors du relevé")
        tempCelsius = capteur.get_temperature()

    tempCelsius = round(tempCelsius, 1) #Arrondi au dixième
    return tempCelsius


# Extremums du capteur (documentation dans le drive)
def tempInvalide(tempC) :
    return ((tempC < -55.0) | (tempC > 125.0))


# Récupère la date courante au moment du relevé de température
def getTime() :
    return datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S') 


# Met la température et sa date de relevé associée dans le fichier :
# "temperature.csv" 
# Ouverture du fichier en mode 'a' 
# Si le fichier n'existe pas, ce mode le créera. 
# Si le fichier existe déjà, 
# les nouvelles données seront ajoutées à la fin du fichier.
def writeDateTemp() :
    #obtenir les informations sur le système de fichiers monté contenant le chemin donné -> dossier courant
    st = os.statvfs(dossierCourant)   

    #obtenir l'espace libre disponible dans le répertoire st -> dossier courant
    #f_bavail : représente le nombre de blocs gratuits pour les utilisateurs non privilégiés
    #f_favail : représente le nombre d’inodes libres pour les utilisateurs non privilégiés
    free_space = st.f_bavail * st.f_frsize / 1024   

    dateActuelle = getTime()
    tempActuelle = getTemp()
    toWrite = str(dateActuelle) + ";" + str(tempActuelle) + "\n"
    if free_space >= len(toWrite.encode("utf-8")): #vérifie s'il reste de la place sur le disque
        with open("temperature.csv","a", encoding = 'utf-8') as fichier :
            fichier.write(toWrite)
            print ("Ecriture de => ", toWrite)
    else: 
        os.remove("temperature.csv")
        print ("Espace disque insuffisant, fichier des relevés supprimé")

# Lecture dans un fichier un nombre qui représente 
# l'intervalle de relevé en SECONDE
# choisit par l'utilisateur sur l'app Android et retourne ce nombre
# gère les caractères fin de ligne et les erreurs de saisie 
def intervalle() :
    with open("intervalle.txt", "r", encoding='utf-8') as fichier :
        ligne = fichier.readline().rstrip()
        number = intervDef
        try:
            ligneInt = int(ligne)
            if (ligneInt > 1):
                number = ligneInt
        except ValueError:
            pass
        return number


# --------------- Main ----------------------------
capteur = W1ThermSensor()
dossierCourant = os.getcwd()
intervDef = 60
while True:
    intervalleChoisi = intervalle()
    print ("Relevé de température en cours toutes les ",intervalleChoisi, " secondes ...")
    writeDateTemp()
    time.sleep(intervalleChoisi)