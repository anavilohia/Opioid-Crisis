import java.io.FileNotFoundException;
import java.io.PrintWriter;
import java.util.ArrayList;
import java.util.Comparator;

public class Runner {

	static ArrayList<County> counties;

	public static void main(String[] args) {

		double[] intervalDeathSum = new double[13];
		double[] intervalOccurences = new double[13];
		Reader myReader = new Reader();
		counties = myReader.getData();
		
		PrintWriter out = null;
		try {
			out = new PrintWriter("Final.txt");
		} catch (FileNotFoundException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}

		counties.sort(Comparator.comparing(County::getUnemploymentRate));

		for (County myCounty : counties) {
			int i = 3;

			while (myCounty.getUnemploymentRate() > i)
				i++;

			if (i < 13) {
				intervalDeathSum[i] += myCounty.getDeathRate();
				intervalOccurences[i]++;
			}

		}

		
		out.println("Unemployment,Death");

		System.out.println("Unemployment\tDeaths(per 100,000)\n");

		for (int i = 3; i < 13; i++) {
			double rate = intervalDeathSum[i] / intervalOccurences[i];

			System.out.print(i - 1 + "-" + i + " %\t\t");
			System.out.printf("%.2f\n", rate);
			
			out.printf("%.2f,%.2f", (double)i - 0.5, rate);
			out.println();
		}
		
		out.close();

	}
}