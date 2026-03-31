import java.math.BigInteger;

public class JavaIntOverflow {
    public static void main(String[] args) {
        System.out.println("=== Java Integer Overflow Attacks ===\n");
        
        int items = 500000;
        int price = 5000;
        int userBalance = 1000; // User only has 1000 credits
        
        System.out.println("Items to buy: " + items);
        System.out.println("Price per item: " + price);
        System.out.println("User Balance: " + userBalance);
        
        // --- Attack 2: Classic Java int Overflow ---
        System.out.println("\n[!] Attack 2: Classic Java int Overflow");
        int totalCostInt = items * price;
        System.out.println("Calculated Total Cost (int): " + totalCostInt);
        if (totalCostInt <= userBalance) {
            System.out.println("VULNERABLE: Transaction approved! User got 500k items for 'free' because cost wrapped to negative.");
        } else {
            System.out.println("SECURE: Transaction denied.");
        }
        
        // --- Attack 3: BigInteger Improper Migration Attack ---
        System.out.println("\n[!] Attack 3: BigInteger Improper Migration Attack");
        // Math is done with BigInteger
        BigInteger bigItems = BigInteger.valueOf(items);
        BigInteger bigPrice = BigInteger.valueOf(price);
        BigInteger trueTotal = bigItems.multiply(bigPrice);
        System.out.println("True Total (BigInteger): " + trueTotal);
        
        // Vulnerability: developer casts back to int for the check
        int castedTotal = trueTotal.intValue();
        System.out.println("Casted back to int for balance check: " + castedTotal);
        
        if (castedTotal <= userBalance) {
            System.out.println("VULNERABLE: Transaction approved! Developer thought BigInteger fixed it, but .intValue() brought the bug back!");
        } else {
            System.out.println("SECURE: Transaction denied.");
        }
        
        // --- Prevention: Proper BigInteger usage ---
        System.out.println("\n[*] Prevention: Full BigInteger Usage without Casting");
        BigInteger bigBalance = BigInteger.valueOf(userBalance);
        // Compare using BigInteger.compareTo
        if (trueTotal.compareTo(bigBalance) <= 0) {
            System.out.println("VULNERABLE (Should not happen)");
        } else {
            System.out.println("SECURE: Transaction denied! Proper check using BigInteger.compareTo blocked the attack.");
        }
    }
}
