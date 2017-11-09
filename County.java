/**
 * 
 * A class to represent a county, which has a name, death rate (per 100,000 persons)and 
 * 
 * @author Nicoale Lari
 *
 */
public class County {

	public County() {
		name = "";
		deathRate = -1;
		unemploymentRate = -1;
	}

	private String name;
	private double deathRate;
	private double unemploymentRate;

	public String getName() {
		return name;
	}

	public void setName(String name) {
		this.name = name;
	}

	public double getDeathRate() {
		return deathRate;
	}

	public void setDeathRate(double deathRate) {
		this.deathRate = deathRate;
	}

	public double getUnemploymentRate() {
		return unemploymentRate;
	}

	public void setUnemploymentRate(double unemploymentRate) {
		this.unemploymentRate = unemploymentRate;
	}

	public void println() {
		System.out.println(this.unemploymentRate + "\t" + this.deathRate + "\t" + this.name);
	}

}
