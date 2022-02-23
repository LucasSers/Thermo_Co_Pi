import java.net.*;
import java.io.*;

/**
 * @author JyB
 * @author LucasSers
 * Simule un client sur Android
 */

public class ClientAndroid {

	public static void main(String[] args) {

		int portServeur;
	    Socket socket;
	    InetAddress iPserveur;
	    BufferedReader in;
	    PrintWriter out;
	    String requete;
	    String reponse;
       	String ip = "192.168.0.100";

	    try {
	    	portServeur = 1111;
            iPserveur = InetAddress.getByName(ip);

	    	socket = new Socket(iPserveur, portServeur);
	    	in = new BufferedReader(new InputStreamReader(socket.getInputStream()));
	    	out = new PrintWriter(new OutputStreamWriter(socket.getOutputStream()), true);

			// traitement de la requête
	    	requete="select * from releve where instant > '2022-02-23 15:00:00'|50";
	    	out.println(requete);

			// traitement de la réponse reçu
			reponse = in.readLine();
			System.out.println(reponse);

	    } catch (ConnectException ce) {
			System.out.println("Erreur -> le serveur n'est pas lancé ou n'est pas trouvé");
		} catch (SocketException se) {
			System.out.println("Erreur -> le processus de votre connexion a été tué");
		} catch (Exception ex) {
			System.out.print("Erreur -> ");
			System.out.println(ex);
		}
	}

}
