package org.thermo_co;

import java.net.*;
import java.io.*;
import java.sql.*; //jdbc

/**
 * @author JyB
 * @author LucasSers
 * Attend une requête du client
 * l'exécute sur sa BD SQLite et renvoie les lignes qu'il obtient
 * après execution
 */

public class ServicePI extends Thread {

	private Socket socket;
	private String requete;
	private String cheminBD = "C:\\Users\\Utilisateur\\releve.db";
	private StringBuilder buffer = new StringBuilder();
	private final int TAILLE_PAQUET = 65535-24; // Max paquet TCP - nbr de caractères max d'une ligne de la table
	private boolean ligneSuivante; // le curseur ne trouve plus de ligne
	Connection laConnexion;
	Statement stmt;
	ResultSet resultat; //objet de retour d'une requête SQL
	

	ServicePI(Socket socket) {
		this.socket = socket;
	}

	public void run() {
		System.out.println("Nouveau thread du serveur exécuté");
		while(true) {
			try {
				BufferedReader in = new BufferedReader(new InputStreamReader(socket.getInputStream()));
				PrintWriter out = new PrintWriter(socket.getOutputStream(),true);
				requete = "";
				try {
					requete = in.readLine();
					laConnexion = DriverManager.getConnection("jdbc:sqlite:" + cheminBD);
					stmt = laConnexion.createStatement();
					resultat = stmt.executeQuery(requete);

					ligneSuivante = resultat.next(); // au moins une ligne est disponible et donc entrer dans le while
					while (ligneSuivante) {
						if (buffer.length() < TAILLE_PAQUET) { // pour ne pas dépasser la taille max d'un paquet TCP
							/* ajoute la ligne au buffer */
							buffer.append(resultat.getString("instant") + ";" + resultat.getString("temperature"));
							if (ligneSuivante = resultat.next()) { // on regarde si la ligne suivante est vide
								buffer.append("|"); // met un délimiteur uniquement s'il y a une ligne suivante
							}
						} else { // envoi prématuré car supérieur à la taille d'un paquet TCP
							out.println(buffer); // envoi la requête
							buffer.delete(0,buffer.length()); // vide le buffer
						}
					}
					/* il n'y a pas d'autres lignes après donc on envoi tout */
					if (!ligneSuivante) {
						out.println(buffer); // envoi la requête
						buffer.delete(0,buffer.length()); // vide le buffer
					}
					/* on ferme la connexion */
					out.println("FIN");
					laConnexion.close();
					stmt.close();

				} catch (SQLException sqlException) {
					sqlException.printStackTrace();
					System.out.println("Erreur de connexion : " + sqlException.getMessage());
				}


				out.close();
				in.close();
				socket.close();

			} catch (IOException err) {
				new IOException(err.getMessage());
			} 
		}

	}

}
