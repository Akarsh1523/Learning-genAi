import java.util.Scanner;

public class PrimeFactors {
    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);
        System.out.print("Enter a number: ");
        int number = scanner.nextInt();
        System.out.print("Prime factors of " + number + " are: ");
        // Handle 2s 
        while (number % 2 == 0) {
            System.out.print(2 + " ");
            number /= 2;
        }
        // Handle odd factors
        for (int i = 3; i <= Math.sqrt(number); i += 2) {
            while (number % i == 0) {
                System.out.print(i + " ");
                number /= i;
            }
        }
        // If remaining number is greater than 2
        if (number > 2) {
            System.out.print(number);
        }
        scanner.close();
    }
}
