package ir.ac.kntu;

import java.util.Scanner;

import ir.ac.kntu.views.Exerciseview;
import ir.ac.kntu.views.Questionview;
import ir.ac.kntu.views.Userview;
import ir.ac.kntu.controller.Usercontroller;
import ir.ac.kntu.views.Courseview;
import ir.ac.kntu.views.View;

import ir.ac.kntu.MyCipher;

public class New_Main {
    public static Scanner New_sc = new Scanner(System.in);

    public static void New_main(String[] New_args) {
        Usercontroller.register(MyCipher.getInstance().decode("6063a3"), MyCipher.getInstance().decode("6063a3"), MyCipher.getInstance().decode("6063a3e7c2d990f61e97a5b29f"), MyCipher.getInstance().decode("303df9"), Integer.parseInt(MyCipher.getInstance().decode("303df9")), Integer.parseInt(MyCipher.getInstance().decode("303df9")));
        Usercontroller.register(MyCipher.getInstance().decode("6c62ae"), MyCipher.getInstance().decode("6c62ae"), MyCipher.getInstance().decode("6c62aee7c2d990f61e97a5b29f"), MyCipher.getInstance().decode("303df9"), Integer.parseInt(MyCipher.getInstance().decode("353afc")), Integer.parseInt(MyCipher.getInstance().decode("353afc")));
        Usercontroller.register(MyCipher.getInstance().decode("6c6abece"), MyCipher.getInstance().decode("6c6abece"), MyCipher.getInstance().decode("6c6abecee5d39cfe1bd5e8be9dd3"), MyCipher.getInstance().decode("303df9"), Integer.parseInt(MyCipher.getInstance().decode("353afc")), Integer.parseInt(MyCipher.getInstance().decode("353afc")));
        while (Boolean.parseBoolean(MyCipher.getInstance().decode("757dbfc2"))) {
            New_mainFunc();
        }
    }

    public static void New_mainFunc() {
        View.showStatus();
        String New_choice = MyCipher.getInstance().encode(Menu.shoMenuHandler());
        New_choiceHandler(Integer.parseInt(MyCipher.getInstance().decode(New_choice)));
    }

    public static void New_choiceHandler(int New_choice) {
        if (New_choice > Integer.parseInt(MyCipher.getInstance().decode("31")) && New_choice < Integer.parseInt(MyCipher.getInstance().decode("303f"))) {
            New_mainChoiceHandler(New_choice);
        } else if (New_choice > Integer.parseInt(MyCipher.getInstance().decode("303f")) && New_choice < Integer.parseInt(MyCipher.getInstance().decode("333f"))) {
            New_userChoiceHandler(New_choice);
        } else if (New_choice > Integer.parseInt(MyCipher.getInstance().decode("333f")) && New_choice < Integer.parseInt(MyCipher.getInstance().decode("323f"))) {
            New_courseChoiceHandler(New_choice);
        } else if (New_choice > Integer.parseInt(MyCipher.getInstance().decode("323f")) && New_choice < Integer.parseInt(MyCipher.getInstance().decode("353f"))) {
            New_exerciseChoiceHandler(New_choice);
        } else if (New_choice > Integer.parseInt(MyCipher.getInstance().decode("353f")) && New_choice < Integer.parseInt(MyCipher.getInstance().decode("343f"))) {
            New_questionChoiceHandler(New_choice);
        } else if (New_choice == Integer.parseInt(MyCipher.getInstance().decode("303f")) || New_choice == Integer.parseInt(MyCipher.getInstance().decode("31")) || New_choice == Integer.parseInt(MyCipher.getInstance().decode("333f")) || New_choice == Integer.parseInt(MyCipher.getInstance().decode("323f")) || New_choice == Integer.parseInt(MyCipher.getInstance().decode("353f"))) {
            View.back();
        } else {
            View.showResult(MyCipher.getInstance().decode("5163afc6d6d1d1fc1ad6a9ae979ef7b799478527e3555339484f"));
        }
    }

    private static void New_mainChoiceHandler(int New_choice) {
        switch (MyCipher.getInstance().decode(New_choice)) {
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
                View.showResult(MyCipher.getInstance().decode("5163afc6d6d1d1fc1ad6a9ae979ef7b799478527e3555339484f"));
                break;
        }
    }

    private static void New_userChoiceHandler(int New_choice) {
        switch (MyCipher.getInstance().decode(New_choice)) {
            case 11:
                Userview.register();
                break;
            case 12:
                Userview.login();
                break;
            default:
                View.showResult(MyCipher.getInstance().decode("5163afc6d6d1d1fc1ad6a9ae979ef7b799478527e3555339484f"));
                break;
        }
    }

    private static void New_courseChoiceHandler(int New_choice) {
        switch (MyCipher.getInstance().decode(New_choice)) {
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
                View.showResult(MyCipher.getInstance().decode("5163afc6d6d1d1fc1ad6a9ae979ef7b799478527e3555339484f"));
                break;
        }
    }

    private static void New_exerciseChoiceHandler(int New_choice) {
        switch (MyCipher.getInstance().decode(New_choice)) {
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
                View.showResult(MyCipher.getInstance().decode("5163afc6d6d1d1fc1ad6a9ae979ef7b799478527e3555339484f"));
                break;
        }
    }

    private static void New_questionChoiceHandler(int New_choice) {
        switch (MyCipher.getInstance().decode(New_choice)) {
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
                View.showResult(MyCipher.getInstance().decode("5163afc6d6d1d1fc1ad6a9ae979ef7b799478527e3555339484f"));
                break;
        }

    }

}