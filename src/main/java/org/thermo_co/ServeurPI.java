package org.thermo_co;

import java.net.*;
import java.io.*;

/**
 * @author JyB
 * Sur le Raspberry PI, Serveur TCP multi-thread
 * pour gérer plusieurs clients android
 */


public class ServeurPI {

	public static void main(String[] args) {
		Socket serviceSocket;
        int port = 432;
        try {
            ServerSocket ecoute = new ServerSocket(port);
            System.out.println("Serveur lancé !");
            while(true) {
                serviceSocket = ecoute.accept();
                ServicePI thread  = new ServicePI(serviceSocket);
                thread.start();
            }
        } catch (IOException err) {
            new IOException(err.getMessage());
        }
	}

}
