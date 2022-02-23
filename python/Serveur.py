# Serveur TCP multi-thread
# pour gérer plusieurs clients
# et 1 thread pour enregistrer les
# températures dans la BD
# JyB
# LucasSers

from w1thermsensor import W1ThermSensor
import datetime, time, socket, threading, sqlite3, re


##################################################################
# PARTIE SERVEUR
##################################################################
class ThreadServer(threading.Thread):

    def __init__(self, info, clientSocket):
        threading.Thread.__init__(self)
        self.ip = info[0]
        self.port = info[1]
        self.socket = clientSocket
        print("[+] Nouveau thread pour %s %s" % (self.ip, self.port,))

    def run(self,):
        print("Connexion de %s sur le port %s" % (self.ip, self.port,))
        try:
            laConnexion = sqlite3.connect('releve.db')
            curseur = laConnexion.cursor()
        except sqlite3.Error as error:
            print("Erreur lors de la connexion à SQLite", error)
            curseur.close()
            laConnexion.close()

        try:
            # réception de la requête
            requete = self.socket.recv(2048)

            # traitement de la requête
            msg = requete.decode()

            #analyse de la requete et scinde en 2 parties
            tbMsg = msg.split("|")

            # Une pour la requete sql
            sql = tbMsg[0]
            # Et l'autre pour l'intervalle de relevé (facultatif)
            try:
                time = tbMsg[1]
                setIntervalle(time)
            except IndexError: # le tableau n'existe pas car le client n'a pas spécifié l'intervalle de relevé
                pass

            curseur.execute(sql)
            resultat = curseur.fetchall()
            reponse = ""

            # construction de la réponse
            for row in resultat:
                reponse += row[1] + ";" + str(row[2]) + "|"

            reponse += str(intervalle())
            reponse += "/FIN"
            print(reponse)

            # envoi de la réponse
            self.socket.send(reponse.encode())

            # fermeture des connexions et du thread
            print("Fermeture de %s sur le port %s" % (self.ip, self.port,))
            curseur.close()
            laConnexion.close()
            self.socket.close() # =! shutdown

        except Exception as e:
            print(e)
            # fermeture de la connexion
            self.socket.close()



##################################################################
# PARTIE ENREGISTREMENT BD
##################################################################
class ThreadDB(threading.Thread):

    # Récupère la température renvoyée par la sonde
    # et gère les erreurs de relevé
    def getTemp(self):
        tempCelsius = self.capteur.get_temperature()
        while (tempInvalide(tempCelsius)):
            print("Erreur! Température incohérente detectée lors du relevé")
            tempCelsius = self.capteur.get_temperature()

        tempCelsius = round(tempCelsius, 1)  # Arrondi au dixième
        return tempCelsius


    # Inscrit la température et son instant de relevé dans la base de donnée
    def writeDateTemp(self):
        date = getTime()
        temp = ThreadDB.getTemp(self)
        data = {"dateActuelle": date, "tempActuelle": temp}
        toWrite = str(date) + " " + str(temp) + "\n"
        print("Relevé de température en cours toutes les ", self.intervalleChoisi, " secondes ...")
        print("Inscription dans la base de donée => ", toWrite)
        try:
            self.curseur.execute(""" 
                        INSERT INTO releve(instant, temperature)
                        VALUES(:dateActuelle, :tempActuelle)
                        """, data)
            self.bd.commit()
        except Exception as erreur:
            print("Erreur lors de l'inscription du relevé dans la table !")
            self.bd.rollback()
            erreur.getMessage()


    def __init__(self):
        threading.Thread.__init__(self)
        self.capteur = W1ThermSensor()
        self.intervalleChoisi = 60
        self.bd = sqlite3.connect('releve.db',
                                  check_same_thread=False)  # Ouverture de de la connexion à la base de donnée
        self.curseur = self.bd.cursor()  # Création d'un objet cursor pour executer des instructions SQLite

    def run(self):
        try:
            self.curseur.execute(""" CREATE TABLE IF NOT EXISTS releve(
                            id INTEGER PRIMARY KEY AUTOINCREMENT, 
                            instant DATETIME NOT NULL, 
                            temperature NUMERIC NOT NULL); """)
            self.bd.commit()
        except Exception as e:
            print("Erreur lors de l'initialisation de la Base de Donnée")
            self.bd.rollback()
            e.getMessage()
            self.bd.close()

        while True:
            self.intervalleChoisi = intervalle()
            ThreadDB.writeDateTemp(self)
            time.sleep(self.intervalleChoisi-1) # 1sec est le temps d'exécution du programme


##################################################################
# METHODES OUTILS
##################################################################
# Extremums du capteur (documentation dans le drive)
def tempInvalide(tempC):
    return ((tempC < -55.0) | (tempC > 125.0))



# Récupère la date courante au moment du relevé de température
def getTime():
    return datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')


# Lecture dans un fichier d'une ip en str
# retourne cette str
# gère les caractères fin de ligne et les erreurs de saisie
def ip():
    with open("ip.txt", "r", encoding='utf-8') as fichier:
        ligne = fichier.readline().rstrip()
        addr = "127.0.0.1" # ip par défaut si erreur
        ip = addr
        ok = re.search("^(?:[0-9]{1,3}\.){3}[0-9]{1,3}$", ligne)
        if (ok): # si la ligne matche à la regex IPv4
            ip = ligne
        else:
            setIp(ip)

        return ip


# Ecriture dans un fichier d'une ip en str
# gère les caractères fin de ligne et les erreurs de saisie
def setIp(chaine):
    with open("ip.txt", "w", encoding='utf-8') as fichier:
        addr = "127.0.0.1" # ip par défaut si erreur
        ip = addr
        ok = re.search("^(?:[0-9]{1,3}\.){3}[0-9]{1,3}$", chaine)
        if (ok): # si la chaine matche à la regex IPv4
            ip = chaine

        fichier.write(str(ip))



# Lecture dans un fichier d'un nombre qui représente
# l'intervalle de relevé en SECONDE
# retourne ce nombre
# gère les caractères fin de ligne et les erreurs de saisie
def intervalle():
    with open("intervalle.txt", "r", encoding='utf-8') as fichier:
        ligne = fichier.readline().rstrip()
        number = 60 # intervalle par défaut si erreur
        try:
            ligneInt = int(ligne)
            if (ligneInt >= 10): # 10 sec minimum
                number = ligneInt
        except ValueError:
            setIntervalle(number) # ecriture de la valeur par défaut pour lever l'erreur le prochain appel
        return number



# Ecriture dans un fichier d'un nombre qui représente
# l'intervalle de relevé en SECONDE
# choisit par l'utilisateur sur l'app Android
# gère les erreurs de saisie
def setIntervalle(entier):
    with open("intervalle.txt", "w", encoding='utf-8') as fichier:
        number = 60 # intervalle par défaut si erreur
        try:
            ligneInt = int(entier)
            if (ligneInt >= 10): # 10 sec minimum
                number = ligneInt
        except ValueError:
            pass
        fichier.write(str(number))



# ------------------------------------- MAIN -------------------------------

HOST = ip()
PORT = 1111
serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # création du socket
try:
    serverSocket.bind((HOST, PORT))  # liaison du socket à une adresse précise
except socket.error:
    print("La liaison du socket à l'adresse choisie a échouée.")
    exit()

try:
    serverSocket.listen()
    print("En écoute...\n")
except socket.error:
    print("Impossible d'écouter sur le socket choisi")
    exit()


# thread permettant l'enregistrement des BD
thread1DB = ThreadDB()
thread1DB.start()


while True:
    (clientSocket, info) = serverSocket.accept()
    newthread = ThreadServer(info, clientSocket)
    newthread.start()
