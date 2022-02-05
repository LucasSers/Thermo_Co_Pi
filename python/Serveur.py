# Serveur TCP multi-thread
# pour gérer plusieurs clients

import socket, threading, sqlite3


class Thread(threading.Thread):

    def __init__(self, info, clientSocket):
        threading.Thread.__init__(self)
        self.ip = info[0]
        self.port = info[1]
        self.socket = clientSocket
        print("[+] Nouveau thread pour %s %s" % (self.ip, self.port,))

    def run(self):
        while True:
            print("Connexion de %s sur le port %s" % (self.ip, self.port,))
            try:
                laConnexion = sqlite3.connect('releve.db')
                curseur = laConnexion.cursor()
            except sqlite3.Error as error:
                print("Erreur lors de la connexion à SQLite", error)

            requete = self.socket.recv(2048)
            sql = requete.decode()
            curseur.execute(sql)
            resultat = curseur.fetchall()
            for row in resultat:
                reponse = row[1] + ";" + str(row[2]) + "|"
                self.socket.send(reponse.encode())

            reponse="FIN".encode()
            self.socket.send(reponse)
            curseur.close()
            laConnexion.close()
            self.socket.close()

# ------------------------------------- MAIN -------------------------------

HOST = 'localhost'
PORT = 1111
serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # création du socket
try :
    serverSocket.bind((HOST, PORT)) # liaison du socket à une adresse précise
except socket.error:
    print ("La liaison du socket à l'adresse choisie a échoué.")


while True:
    serverSocket.listen()
    print("En écoute...")
    (clientSocket, info) = serverSocket.accept()
    newthread = Thread(info, clientSocket)
    newthread.start()