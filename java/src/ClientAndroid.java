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
        byte[] ipServeur = new byte[] { 127, 0, 0, 1 };

	    try {
	    	portServeur = 1111;
            iPserveur = InetAddress.getByAddress("Localhost",ipServeur);

	    	socket = new Socket(iPserveur, portServeur);
	    	in = new BufferedReader(new InputStreamReader(socket.getInputStream()));
	    	out = new PrintWriter(new OutputStreamWriter(socket.getOutputStream()), true);

	    	requete="select * from releve";
	    	out.println(requete);

			do {
				reponse = in.readLine();
				System.out.println(reponse);
			} while(!reponse.equals(null) || !reponse.equals("FIN"));

	    } catch (Exception ex) {
	    	System.out.println("coucou"); //je passe dans l'exception wtf
	    }
	}

}
