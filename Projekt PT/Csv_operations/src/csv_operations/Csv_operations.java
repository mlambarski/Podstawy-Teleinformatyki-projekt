package csv_operations;

import java.io.File;
import java.io.FileNotFoundException;
import java.util.Scanner;
import java.util.logging.Level;
import java.util.logging.Logger;


public class Csv_operations {

    public static void main(String[] args) throws FileNotFoundException {
        String filename =  "osoby.csv";
        File file = new File(filename);
        Scanner inputStream = new Scanner(file);
        while(inputStream.hasNext()){
                String data = inputStream.next();
                System.out.println(data + "***");
            }
        inputStream.close();
        
        
    }    
}
