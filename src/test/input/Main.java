package ir.ac.kntu;

import java.util.Scanner;

import ir.ac.kntu.views.Exerciseview;
import ir.ac.kntu.views.Questionview;
import ir.ac.kntu.views.Userview;
import ir.ac.kntu.controller.Usercontroller;
import ir.ac.kntu.views.Courseview;
import ir.ac.kntu.views.View;

public class Main {
    public static Scanner sc = new Scanner(System.in);

    public static void main(String[] args) {
        Usercontroller.register("ali", "ali", "ali@gmail.com", "123", 123, 123);
        Usercontroller.register("mmd", "mmd", "mmd@gmail.com", "123", 456, 456);
        Usercontroller.register("meti", "meti", "meti@gmail.com", "123", 456, 456);
        while (true) {
            mainFunc();
        }
    }

    public static void mainFunc() {
        View.showStatus();
        int choice = Menu.shoMenuHandler();
        choiceHandler(choice);
    }

    public static void choiceHandler(int choice) {
        if (choice > 0 && choice < 10) {
            mainChoiceHandler(choice);
        } else if (choice > 10 && choice < 20) {
            userChoiceHandler(choice);
        } else if (choice > 20 && choice < 30) {
            courseChoiceHandler(choice);
        } else if (choice > 30 && choice < 40) {
            exerciseChoiceHandler(choice);
        } else if (choice > 40 && choice < 50) {
            questionChoiceHandler(choice);
        } else if (choice == 10 || choice == 0 || choice == 20 || choice == 30 || choice == 40) {
            View.back();
        } else {
            View.showResult("Please choose a valid task");
        }
    }

    private static void mainChoiceHandler(int choice) {
        switch (choice) {
            case 2:
                View.searchCourse();
                break;
            case 3:
                View.searchUser();
                break;
            case 4:
                View.addQuestionToBank();
                break;
            case 5:
                View.showQuestionbank();
                break;
            default:
                View.showResult("Please choose a valid task");
                break;
        }
    }

    private static void userChoiceHandler(int choice) {
        switch (choice) {
            case 11:
                Userview.register();
                break;
            case 12:
                Userview.login();
                break;
            default:
                View.showResult("Please choose a valid task");
                break;
        }
    }

    private static void courseChoiceHandler(int choice) {
        switch (choice) {
            case 21:
                Courseview.addCourse();
                break;
            case 22:
                Courseview.deleteCourse();
                break;
            case 23:
                Courseview.modifyCourse();
                break;
            case 24:
                Courseview.addUser();
                break;
            case 25:
                Courseview.closeCourse();
                break;
            case 26:
                Courseview.opeanCourse();
                break;
            case 27:
                Courseview.chooseCourse();
                break;
            default:
                View.showResult("Please choose a valid task");
                break;
        }
    }

    private static void exerciseChoiceHandler(int choice) {
        switch (choice) {
            case 31:
                Exerciseview.createExercise();
                break;
            case 32:
                Exerciseview.deleteExercise();
                break;
            case 33:
                Exerciseview.modifyExercise();
                break;
            case 34:
                Exerciseview.chooseExercise();
                break;
            case 35:
                Exerciseview.getScoreTable();
                break;
            default:
                View.showResult("Please choose a valid task");
                break;
        }
    }

    private static void questionChoiceHandler(int choice) {
        switch (choice) {
            case 41:
                Questionview.addQuestion();
                break;
            case 42:
                Questionview.deleteQuestion();
                break;
            case 43:
                Questionview.modifyQuestion();
                break;
            case 44:
                Questionview.getSubmitsOfUser();
                break;
            case 45:
                Questionview.gradeQuestion();
                break;            
            case 46:
                Questionview.getSubmitsAndPoints();
                break;
            case 47:
                Questionview.answerQuestion();
                break;
            case 48:
                Questionview.setFinalSubmit();
                break;
            default:
                View.showResult("Please choose a valid task");
                break;
        }

    }

}