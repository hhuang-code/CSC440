package weka.test;

import java.util.Scanner;

import weka.bayes.ClassifierBayesNetwork;
import weka.data.Data;
import weka.mlp.ClassifierMLNN;
import weka.svm.ClassifierSVM;

public class Test {

	public static void main(String[] args) throws Exception{
		
		// Augment generalized dataset
		Data.Augment();
		
		System.out.println("Input classifier type (1-SVM, 2-MLNN, 3-Bayes, 0-Exit): ");
		Scanner scan = new Scanner(System.in);
		int type = scan.nextInt();
		
		while(true) {
			switch(type) {
				case 0:
					scan.close();
					System.exit(0);
				case 1:
					// Run SVM classifier
					ClassifierSVM.Run();	
					System.out.println("Input classifier type (1-SVM, 2-MLNN, 3-Bayes, 0-Exit): ");
					break;
				case 2:
					// Run Multi-layer neural network classifier
					ClassifierMLNN.Run();	
					System.out.println("Input classifier type (1-SVM, 2-MLNN, 3-Bayes, 0-Exit): ");
					break;
				case 3:
					// Run Bayes network classifier
					ClassifierBayesNetwork.Run();	
					System.out.println("Input classifier type (1-SVM, 2-MLNN, 3-Bayes, 0-Exit): ");
					break;
				default:
					System.out.println("Invalid input! Please input again: ");
			}
			scan = new Scanner(System.in);
			type = scan.nextInt();
		}	
	}

}
