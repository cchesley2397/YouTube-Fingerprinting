package edu.rit;

import com.teamdev.jxbrowser.engine.Engine;
import com.teamdev.jxbrowser.view.javafx.BrowserView;
import javafx.application.Application;
import javafx.application.Platform;
import javafx.event.EventHandler;
import javafx.fxml.FXMLLoader;
import javafx.scene.Scene;
import javafx.scene.layout.BorderPane;
import javafx.stage.Stage;
import javafx.stage.StageStyle;
import javafx.stage.WindowEvent;

public class BrowserLauncher extends Application {

    private static Stage stage;

    private static BorderPane browser;

    private static BrowserView browserView;

    @Override
    public void start(Stage primaryStage){


        stage = primaryStage;
        stage.initStyle(StageStyle.UNDECORATED);
        //stage.getIcons().add(new Image(getClass().getResource("/images/splash.png").toExternalForm()));
        stage.setTitle("SplashBrowser™");

        primaryStage.setOnCloseRequest(new EventHandler<WindowEvent>() {
            @Override
            public void handle(WindowEvent event) {

                Platform.exit();

                Thread start = new Thread(new Runnable() {
                    @Override
                    public void run() {
                        Runtime.getRuntime().halt(0);
                    }
                });

                start.start();
            }
        });

        //TODO INDIVIDUAL STAGE LOADING
        try{
            browser = new BorderPane();
            browser.setCenter(browserView);
        }catch (Exception e){
            e.printStackTrace();
        }

        Scene baseScene = new Scene(browser, 1080, 660);
        baseScene.setFill(null);

        stage.setScene(baseScene);


        stage.show();
    }

    public static void setBrowserView(BrowserView browserView) {
        BrowserLauncher.browserView = browserView;
    }
}