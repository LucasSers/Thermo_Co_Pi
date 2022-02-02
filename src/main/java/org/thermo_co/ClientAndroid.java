package org.thermo_co;

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
	    
	    try {
	    	portServeur = 432;
	    	iPserveur = InetAddress.getLocalHost();  //127.0.0.1

	    	socket = new Socket(iPserveur, portServeur);
	    	in = new BufferedReader(new InputStreamReader(socket.getInputStream()));
	    	out = new PrintWriter(new OutputStreamWriter(socket.getOutputStream()), true);

	    	requete="select * from releve";
	    	out.println(requete);

			do {
				reponse = in.readLine();
				System.out.println(reponse);
			} while(!reponse.equals("FIN"));

	    } catch (Exception ex) {
	    	System.out.println(ex.getMessage());
	    }


	}

}
