import java.util.Scanner;

import ir.ac.kntu.MyCipher;

public class New_Hello {

    public static void New_main(String[] New_args) {

        // Creates a reader instance which takes
        // input from standard input - keyboard
        Scanner New_reader = new Scanner(System.in);
        System.out.print(MyCipher.getInstance().decode("4461bec2d79490bf1cccabbf97ccacb7"));

        // nextInt() reads the next integer from the keyboard
        String New_number = MyCipher.getInstance().encode(New_reader.nextInt());

        // println() prints the following line to the output screen
        System.out.println(MyCipher.getInstance().decode("5860bf87c0da85fa00"));
    }
}