package weka.data;

import java.io.BufferedReader;
import java.io.FileReader;
import java.io.PrintWriter;
import java.util.Random;

public class Data {

	public static void Augment() throws Exception {
		
		String srcFilename = "./generalized_data.arff";
		String destFilename = "./augmented_data.arff";
		
		PrintWriter writer = new PrintWriter(destFilename);
		// Print additional information needed by weka
		writer.println("@RELATION data_mining\n");
		writer.println("@ATTRIBUTE department REAL");
		writer.println("@ATTRIBUTE age REAL");
		writer.println("@ATTRIBUTE salary REAL");
		writer.println("@ATTRIBUTE class {senior, junior}\n");
		writer.println("@DATA\n");
		
		// Load generalized data
		try(BufferedReader br = new BufferedReader(new FileReader(srcFilename))){
			String line = null;
			while((line = br.readLine()) != null) {
				line = line.trim();
				// Drop comment line
				if(line.startsWith("%")) {
					continue;
				}
				String[] attrs = line.split(" ");
				String department = attrs[0];
				String age = attrs[1];
				String salary = attrs[2];
				String status = attrs[3];
				String count = attrs[4];
				for(int j = 0; j < Integer.parseInt(count); j++) {
					StringBuffer sb = new StringBuffer();
					// Append department: 1 - sales, 2 - systems, 3 - marketing, 4 - secretary
					if("sales".equals(department)) {
						sb.append(1 + " ");
					}else if("systems".equals(department)) {
						sb.append(2 + " ");
					}else if("marketing".equals(department)) {
						sb.append(3 + " ");
					}else if("secretary".equals(department)) {
						sb.append(4 + " ");
					}else {
						throw new Exception();
					}
					// Append age
					String[] bounds = age.split("\\.\\.\\.");
					int lowBound = Integer.parseInt(bounds[0]);
					int highBound = Integer.parseInt(bounds[1]);
					Random rand = new Random();
					int specifiedAge = rand.nextInt(highBound - lowBound + 1) + lowBound;
					sb.append(String.valueOf(specifiedAge) + " ");
					// Append salary
					bounds = salary.split("\\.\\.\\.");
					lowBound = Integer.parseInt(bounds[0].substring(0, bounds[0].length() - 1));
					highBound = Integer.parseInt(bounds[1].substring(0, bounds[1].length() - 1));
					int specifiedSalary = rand.nextInt(highBound - lowBound + 1) + lowBound;
					sb.append(String.valueOf(specifiedSalary) + " ");
					// Append status
					sb.append(status);
					writer.println(sb.toString());
				} 
			}
		}
		writer.close();
		
	}

}
