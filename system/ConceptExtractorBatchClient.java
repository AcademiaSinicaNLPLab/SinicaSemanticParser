//import semanticrolelabeling.*;
import java.io.*;
import edu.stanford.nlp.trees.Tree;
import java.util.*;
import java.io.File;
import java.io.FileReader;
import opennlp.maxent.DataStream;
import opennlp.maxent.PlainTextByLineDataStream;

//package bdn;
/*  The java.net package contains the basics needed for network operations. */
import java.net.*;
/* The java.io package contains the basics needed for IO operations. */
import java.io.*;

public class ConceptExtractorBatchClient
{
    
    
    public static void main(String[] args)
    {
        String host = "localhost";
        int port = 29999;

        System.err.println("# SocketClient initialized");
        
        try
        {   
            // read sentence from file
            BufferedReader inputReader = new BufferedReader(new FileReader("../input/input.txt"));
            
            PrintWriter outputFileWriter = new PrintWriter("../output/output.txt", "UTF-8");
            outputFileWriter.println("<rdf:RDF xmlns:rdf=\"http://www.w3.org/1999/02/22-rdf-syntax-ns#\">");
            outputFileWriter.println("<rdf:Description rdf:about=\"http://sentic.net/challenge/sentence\">");
            outputFileWriter.close();
            String sent;
            System.err.println("# Processing....");

            while ((sent = inputReader.readLine()) != null)
            {
                String sentence = sent + (char) 13;
                
                // Establish a socket connetion
                InetAddress address = InetAddress.getByName(host);
                Socket connection = new Socket(address, port);

                // send sentence to server via socket
                BufferedOutputStream bos = new BufferedOutputStream(connection.getOutputStream());
                OutputStreamWriter osw = new OutputStreamWriter(bos, "US-ASCII");
                System.err.println("# send sentence: "+sentence);
                osw.write(sentence);
                osw.flush();

                //System.out.println("Concept Extraction....");
                BufferedReader fromServer = new BufferedReader(new InputStreamReader(connection.getInputStream()));

                // MaxisKao @ 20140822
                // In this version, the serverResponse would be only "Concepts:\r"
                String serverResponse = fromServer.readLine();
                

                // MaxisKao @ 20140822
                // Just pass the sentence as parameter to the python program
                //
                //----VVVV--- Andy Lee add 20140522 for transfering sentence to python program.
                // File wfile2 = new File("../temp/sent-output.txt");
                // BufferedWriter wr2 = new BufferedWriter(new OutputStreamWriter(new FileOutputStream(wfile2),"UTF-8"));
                // String toFileString = sent;
                // wr2.write(toFileString);
                // wr2.flush();
                // wr2.close();
                //----^^^^--- Andy Lee add 20140522 for transfering sentence to python program.

                // Pass the sentence to conceptFormulator2
                Runtime rlabeler = Runtime.getRuntime();
                String srlClassifier = "python conceptFormulator2.py " + '"'+sent+'"' ;
                //String srlClassifier = "python conceptFormulator.py " + '"'+sent+'"' ;
                Process p = rlabeler.exec(srlClassifier);
                BufferedReader br = new BufferedReader(new InputStreamReader(p.getInputStream()));
                p.waitFor();

                String line2;
                while((line2 = br.readLine()) != null) 
                {
                    System.out.println(line2);
                }
        } 
        
        FileWriter fstream = new FileWriter("../output/output.txt", true); //true tells to append data.
        BufferedWriter outFileWriter;
        outFileWriter = new BufferedWriter(fstream);
        outFileWriter.write("</rdf:Description>");
        outFileWriter.write("\n</rdf:RDF>");
        outFileWriter.close();
        System.out.println("Done!");

        }
        catch (Exception e)
        {
            String cause = e.getMessage();
            if (cause.equals("python: not found"))
                System.out.println("No python interpreter found.");
            else
                System.out.println("Error: "+cause); //Andy add 20140522 for error handling.
        }
    }
}