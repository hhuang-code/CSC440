package weka.mlp;

import weka.classifiers.functions.MultilayerPerceptron;
import weka.core.Instance;
import weka.core.Instances;
import weka.core.converters.ConverterUtils.DataSource;

public class ClassifierMLNN {

	public static void Run() throws Exception{
		
		//Load training dataset
		DataSource source = new DataSource("./augmented_data.arff");
		
		Instances trainSet = source.getDataSet();	
				
		//Set class index to the last attribute
		trainSet.setClassIndex(trainSet.numAttributes() - 1);

		//Build a multi-layer neural network model
		MultilayerPerceptron mlp = new MultilayerPerceptron();
		mlp.setLearningRate(0.1);
		mlp.setMomentum(0.2);
		mlp.setTrainingTime(2000);
		mlp.setHiddenLayers("3");
		mlp.buildClassifier(trainSet);
		//Output model information
		System.out.println(mlp);

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
			double pred = mlp.classifyInstance(curIns);
			System.out.println(gt + " " + pred);
			
			if(gt == pred) {
				correctCnt++;
			}
		}
		double accuracyRate = (double)correctCnt / testSet.numInstances() * 100;
		System.out.println("Accuracy rate: " + String.format("%.0f%%", accuracyRate));
	}
}
