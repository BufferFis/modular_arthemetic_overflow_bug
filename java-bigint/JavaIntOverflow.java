import java.io.FileWriter;
import java.io.IOException;
import java.math.BigInteger;
import java.util.Random;

public class JavaIntOverflow {
  static Random rand = new Random();

  public static void main(String[] args) throws IOException {
    FileWriter writer = new FileWriter("results.csv");

    writer.append("input_size,method,time_ns,success,overflow_detected\n");

    int[] sizes = { 1000, 10000, 50000, 100000, 500000, 1000000 };

    for (int size : sizes) {
      for (int i = 0; i < 50; i++) {

        int items = size;
        int price = 5000;
        int balance = 1_000_000_000;

        // -------------------------
        // Attack 2: int overflow
        // -------------------------
        long start = System.nanoTime();

        int total = items * price;
        boolean success = (total <= balance);
        boolean overflow = (items != 0 && total / items != price);

        long end = System.nanoTime();

        writer.append(size + ",attack_int," + (end - start) + "," + success + "," + overflow + "\n");

        // -------------------------
        // Attack 3: BigInteger misuse
        // -------------------------
        start = System.nanoTime();

        BigInteger totalBI = BigInteger.valueOf(items)
            .multiply(BigInteger.valueOf(price));

        int totalCast = totalBI.intValue(); // vulnerability
        boolean successBI = (totalCast <= balance);

        end = System.nanoTime();

        writer.append(size + ",attack_bigint_cast," + (end - start) + "," + successBI + ",false\n");

        // -------------------------
        // Prevention 1: Safe BigInteger
        // -------------------------
        start = System.nanoTime();

        boolean safe1 = totalBI.compareTo(BigInteger.valueOf(balance)) <= 0;

        end = System.nanoTime();

        writer.append(size + ",safe_bigint," + (end - start) + "," + safe1 + ",false\n");

        // -------------------------
        // Prevention 2: Bounds check
        // -------------------------
        start = System.nanoTime();

        boolean overflowDetected = false;
        boolean safe2 = false;

        if (items > Integer.MAX_VALUE / price) {
          overflowDetected = true;
          safe2 = false;
        } else {
          int safeTotal = items * price;
          safe2 = safeTotal <= balance;
        }

        end = System.nanoTime();

        writer.append(size + ",safe_bounds," + (end - start) + "," + safe2 + "," + overflowDetected + "\n");

        // -------------------------
        // Prevention 3: Safe multiplyExact
        // -------------------------
        start = System.nanoTime();

        boolean safe3;
        boolean overflow3 = false;

        try {
          int safeTotal = Math.multiplyExact(items, price);
          safe3 = safeTotal <= balance;
        } catch (ArithmeticException e) {
          overflow3 = true;
          safe3 = false;
        }

        end = System.nanoTime();

        writer.append(size + ",safe_multiplyExact," + (end - start) + "," + safe3 + "," + overflow3 + "\n");
      }
    }

    writer.close();
    System.out.println("✅ results.csv generated");
  }
}
