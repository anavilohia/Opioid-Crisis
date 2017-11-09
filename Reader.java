import java.io.File;
import java.io.FileNotFoundException;
import java.util.ArrayList;
import java.util.Iterator;
import java.util.Scanner;

public class Reader {

	private Scanner inDeath = null;
	private Scanner inUnemp = null;
	private File inUnempFile = new File("unemployment.txt");
	private File inDeathFile = new File("death.txt");
	private ArrayList<County> counties = new ArrayList<County>();

	/**
	 * @return an ArrayList of County objects, containing the opioid death rate and the unemployment rate for a specific county
	 */
	public ArrayList<County> getData() {

		openFiles();
		readUnemploymentData();
		readDeathData();
		deleteIncompleteCounties();
		
		return counties;

	}

	private void openFiles() {
		try {
			inDeath = new Scanner(inDeathFile);
		} catch (FileNotFoundException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}

		try {
			inUnemp = new Scanner(inUnempFile);
		} catch (FileNotFoundException e) {
			e.printStackTrace();
		}
	}

	/**
	 * Read the unemployment data and store the counties in the counties Array List.
	 */
	private void readUnemploymentData() {
		String line;

		inUnemp.nextLine();

		while (inUnemp.hasNextLine()) {
			line = inUnemp.nextLine();
			String[] entry = line.split("\t");
			entry[0] = entry[0].replaceAll("\"", "");

			County tempCounty = new County();
			tempCounty.setName(entry[0]);
			tempCounty.setUnemploymentRate(Double.parseDouble(entry[1]));

			counties.add(tempCounty);
		}

	}

	/**
	 * Read the death data, and if it is not "Unreliable" and we have the unemployment rate for that county in the ArrayList, then add the
	 * information to the counties ArrayList.
	 */
	private void readDeathData() {
		String line;

		inDeath.nextLine();

		while (inDeath.hasNextLine()) {
			line = inDeath.nextLine();
			String[] entry = line.split("\t");
			entry[0] = entry[0].replaceAll("\"", "");

			if (entry[4].equals("Unreliable") == false) {
				double rate = Double.parseDouble(entry[4]);

				for (int i = 0; i < counties.size(); i++) {
					String name = counties.get(i).getName();
					if (name.equalsIgnoreCase(entry[0])) {
						counties.get(i).setDeathRate(rate);
					}
				}
			}
		}
	}

	/**
	 * Delete counties for which there is no death rate information.
	 */
	private void deleteIncompleteCounties()
	{
		for (Iterator<County> iterator = counties.iterator(); iterator.hasNext();) {
		    County myCounty = iterator.next();
		    if (myCounty.getDeathRate() == -1) {
		        iterator.remove();
		    }
		}
	}

}
