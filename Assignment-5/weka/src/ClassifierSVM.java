package weka.svm;

import weka.core.Instance;
import weka.core.Instances;
import weka.core.converters.ConverterUtils.DataSource;
import weka.classifiers.functions.SMO;

public class ClassifierSVM{
	
	public static void Run() throws Exception{
		
		//Load training dataset
		DataSource source = new DataSource("./augmented_data.arff");
		
		Instances trainSet = source.getDataSet();	
				
		//Set class index to the last attribute
		trainSet.setClassIndex(trainSet.numAttributes() - 1);

		//Build a SVM model
		SMO smo = new SMO();
		smo.buildClassifier(trainSet);
		//Output model information
		System.out.println(smo);

		//Load new dataset
		DataSource source1 = new DataSource("./augmented_data.arff");
		Instances testSet = source1.getDataSet();	
		//Set class index to the last attribute
		testSet.setClassIndex(testSet.numAttributes() - 1);

		//Make predictions for each instance in test set
		System.out.println("Ground truth Class, Predicted Class");
		int correctCnt = 0;
		for (int i = 0; i < testSet.numInstances(); i++) {
			//Get ground truth class for current instance
			double gt = testSet.instance(i).classValue();
			//Get current instance
			Instance curIns = testSet.instance(i);
			//Make prediction
			double pred = smo.classifyInstance(curIns);
			System.out.println(gt + " " + pred);
			
			if(gt == pred) {
				correctCnt++;
			}
		}
		double accuracyRate = (double)correctCnt / testSet.numInstances() * 100;
		System.out.println("Accuracy rate: " + String.format("%.0f%%", accuracyRate));
	}
}
