import java.util.ArrayList;
import java.util.Arrays;
import java.util.Scanner;
import java.util.Random;


public class Battleship {
    public static void main(String[] args) {
        int length = 10;
        int width = 10;
        String[][] pBoard = new String[length][width];
        String[][] cBoard = new String[length][width];

        boardInit(pBoard);
        playerPlaceShips(pBoard);

        boardInit(cBoard);
        computerPlaceShips(cBoard);

        showStatus(pBoard);

        String[][] pHitList = new String[length][width];
        String[][] cHitList = new String[length][width];
        initHitList(pHitList);
        initHitList(cHitList);

        String winner = "";
        boolean done = false;
        while (!done) {
            playerTurn(pHitList, cBoard);
            showStatus(pHitList);
            computerTurn(cHitList, pBoard);
            showStatus(pBoard);
            if (!shipsStillOnBoard(pBoard)) {
                done = true;
                winner = "Computer";
            }
            else if (!shipsStillOnBoard(cBoard)){
                done = true;
                winner = "Player";
            }
        }
        System.out.println(winner + " wins!");
    }

    // Fills the board with empty spaces according to the length and width of the board in main
    public static void boardInit(String[][] board) {
        for (int i = 0; i < board.length ; i++){
            for (int j = 0; j < board[i].length; j++) {
                board[i][j] = " ";
            }
        }
    }
    // show status of board (ex. the ships placed, the misses)
    public static void showStatus(String[][] board) {
        System.out.println("    0123456789    ");
        for (int i = 0; i < board.length ; i++){
            System.out.print(i + " | ");
            for (int j = 0; j < board[i].length; j++) {
                System.out.print(board[i][j]);
            }
            System.out.println(" | " + i);
        }
        System.out.println("    0123456789    ");
    }

//      if ship is on that coordinate, return true
    public static boolean shipPresent(int x, int y, String[][] board) {
        if (board[y][x] == "@") { return true; }
        return false;
    }

// has user enter coordinates for ship. if theres already a ship there, then tell use to reenter
    public static void playerPlaceShips(String[][] board){

        Scanner input = new Scanner(System.in);
        int i = 1;
        while (i < 7) {
            System.out.print("Enter X coordinate for Ship " + i + ": ");
            int x = input.nextInt();
            System.out.print("Enter Y coordinate for Ship " + i + ": ");
            int y = input.nextInt();
            if (shipPresent(x, y, board) == false) {
                board[y][x] = "@";
                i++;
            }
            else {
                System.out.println("INVALID LOCATION");
            }
        }
    }
// computer randomly generates where 6 ships will be for its board
    public static void computerPlaceShips(String[][] board) {
        Random rand = new Random();
        System.out.println("\nComputer placing ships...");
        int i = 1;
        while (i < 7) {
            int x = rand.nextInt(board.length - 1);
            int y = rand.nextInt(board.length - 1);
            if (shipPresent(x, y, board) == false) {
                board[y][x] = "@";
                i++;
            }
        }
        System.out.println("Computer finished placement.\n");
    }
    public static void initHitList(String[][] list) {
        for (int i = 0; i < list.length; i++) {
            for (int j = 0; j < list.length; j++) {
                list[i][j] = " ";
            }
        }
    }
// User enters a coordinate for a missile. If there is a ship there, print hit and place an x there
    // If a ship isn't there, place a -. If it's already been tried, reenter a coordinate
    // passes in a hit list as a parameter that will have entries of either true or false
    // false means no attempt at that coordinate, true means attempted
    public static void playerTurn(String[][] list, String[][] board) {
        Scanner turn = new Scanner(System.in);
        boolean over = false;
        while (!over) {
            System.out.print("Enter missile X coordinate: ");
            int x = turn.nextInt();
            System.out.print("Enter missile Y coordinates: ");
            int y = turn.nextInt();
            if (list[y][x] == " ") {
                if (shipPresent(x, y, board) == false) {
                    System.out.println("\nMiss");
                    list[y][x] = "-";
                }
                else {
                    System.out.println("\nHit");
                    list[y][x] = "X";
                }
                over = true;
            }
            else {System.out.println("\nAlready tried this coordinate.\n"); }
        }
    }

    public static void computerTurn(String[][] list, String[][] board) {
        Random rand = new Random();

        boolean over = false;
        while (!over) {
            int x = rand.nextInt(board.length - 1);
            int y = rand.nextInt(board.length - 1);
            if (list[y][x] == " ") {
                if (shipPresent(x, y, board) == false) {
                    System.out.println("\nComputer missed.");
                    board[y][x] = "-";
                    list[y][x] = "-";
                }
                else {
                    System.out.println("\nComputer hit.");
                    board[y][x] = "X";
                }
                over = true;
            }
        }
    }

    public static boolean shipsStillOnBoard(String[][] board) {
        for (int i = 0; i < board.length; i++){
            for (int j = 0; j < board.length; j++) {
                if (board[i][j] == "@") { return true; }
            }
        }
        return false;
    }

}
