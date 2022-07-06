import java.util.Scanner;

public class EntreeUtilisateur {
    public static String readInput(String message, String letters, String optionsMessage)
    {
        String input;
        boolean isNotVerified;
        do {
            System.out.print(message);
            input = scanner.nextLine();
            isNotVerified = !letters.contains(input) && !input.equals("?");
            if(isNotVerified)
            {
                System.out.println("le input n'est pas valide entrer autre valeur \n");
                System.out.print(message);
                input = scanner.nextLine();
            }
            else if(input.equals("?")){
                System.out.println(optionsMessage);
            }
        }while (isNotVerified);
        return input;
    }
    private static final Scanner scanner = new Scanner(System.in);

    public static String getValue(String message)
    {
        System.out.print(message);
        return scanner.nextLine();
    }
}
