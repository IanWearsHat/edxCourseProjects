import java.util.Scanner;

public class FractionCalculator {
    public static void main(String[] args) {
        Scanner input = new Scanner(System.in);

    }

    public static String getOperation(Scanner input){
        System.out.print("Please enter a valid operation (+, -, *, /, =, or Q/q to quit): ");
        boolean invalidInput = true;
        while (invalidInput) {
            String u_input = input.nextLine();
            u_input = u_input.strip();
            if (u_input.equalsIgnoreCase("+")
                    || u_input.equalsIgnoreCase("-")
                    || u_input.equalsIgnoreCase("*")
                    || u_input.equalsIgnoreCase("/")
                    || u_input.equalsIgnoreCase("=")) {
                invalidInput = false;
                return u_input;
            } else if (u_input.equalsIgnoreCase("q")) {
                invalidInput = false;
                System.exit(0);
            } else {
                System.out.print("Invalid input. (+, -, *, /, =, or Q/q to quit):");
            }
        }
        return null;
    }

    public static boolean isValidFraction(String input){
        if (input.indexOf("-") > 0) {
            System.out.println("Negative sign should be the first character.");
            return false;
        }
        else {
            String negativeTemp = input.replace("-", "");
            input.replace("-", "");
        }

        if (input.indexOf("/") == input.length() || input.indexOf("/") == 0) {
            System.out.println("Slash sign is in the wrong place, meaning there is no numerator or denominator.");
            return false;
        }
        else {
            int slashIndex = input.indexOf('/');
            input.replace("/", "");
        }

        for (int i = 0; i < input.length(); i++) {
            switch (input.indexOf(i)){
                case 0:
                case 1:
                case 2:
                case 3:
                case 4:
                case 5:
                case 6:
                case 7:
                case 8:
                case 9: break;
                default:
                    System.out.println("Non-integer found.");
                    return false;
            }
        }


        return true;
    }

}
