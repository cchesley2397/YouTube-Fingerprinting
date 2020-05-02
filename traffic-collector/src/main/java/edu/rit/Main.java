package edu.rit;

import com.google.gson.*;
import com.sun.jna.Platform;
import com.teamdev.jxbrowser.browser.Browser;
import com.teamdev.jxbrowser.dom.Element;
import com.teamdev.jxbrowser.engine.*;
import com.teamdev.jxbrowser.frame.Frame;
import com.teamdev.jxbrowser.net.*;
import com.teamdev.jxbrowser.net.callback.InterceptRequestCallback;
import com.teamdev.jxbrowser.time.Timestamp;
import com.teamdev.jxbrowser.ui.KeyCode;
import com.teamdev.jxbrowser.ui.event.KeyTyped;
import com.teamdev.jxbrowser.view.javafx.BrowserView;
import javafx.application.Application;
import javafx.stage.Stage;
import org.apache.commons.io.IOUtils;
import org.pcap4j.core.*;
import org.pcap4j.packet.Packet;
import org.pcap4j.util.NifSelector;

import java.io.*;
import java.io.File;
import java.nio.file.Paths;
import java.util.ArrayList;
import java.util.function.Consumer;

import static java.nio.charset.StandardCharsets.UTF_8;

public class Main {

    static PcapHandle handle;
    static PcapDumper dumper;

    static boolean vidStarted = false;

    static Gson gson = new GsonBuilder().setPrettyPrinting().create();
    static JsonObject videosObject;

    static BrowserView browserView;

    static boolean pageLoaded = false;

    static PcapNetworkInterface getNetworkDevice() {
        PcapNetworkInterface device = null;
        try {
            device = new NifSelector().selectNetworkInterface();
        } catch (IOException e) {
            e.printStackTrace();
        }
        return device;
    }

    public static Engine createEngine(String directory){

        final Engine browserEngine;


        browserEngine = Engine.newInstance(
                EngineOptions.newBuilder(RenderingMode.HARDWARE_ACCELERATED)
                        // The language used on the default error pages and GUI.
                        .language(Language.ENGLISH_US)
                        //.userAgent(Utils.DESKTOP_USER_AGENT)
                        .addSwitch("disable-web-security")
                        .licenseKey("1BNDIEOFAYW62JIXIHD4GS3F0PFMQKK4QC2VNWJK2JUS82ZXJHSUPBVHQ7ORY84AHJPH0O")
                        .userDataDir(Paths.get(directory))
                        //.userAgent(Utils.DESKTOP_USER_AGENT)
                        .enableProprietaryFeature(ProprietaryFeature.H_264)
                        .build());

        Network network = browserEngine.network();
        network.set(InterceptRequestCallback.class, params -> {
            UrlRequest urlRequest = params.urlRequest();

            //System.out.println(urlRequest.url());

            UrlRequestJob.Options options = UrlRequestJob.Options
                    .newBuilder(urlRequest.id(), HttpStatus.OK)
                    .addHttpHeader(HttpHeader.of("Content-Type", "text/html"))
                    .build();
            UrlRequestJob urlRequestJob = network.newUrlRequestJob(options);

            String html = "";

            //System.out.println(urlRequest.url());

            if(urlRequest.url().contains("www.youtube.com/generate")){
                //System.out.println("LOADED PAGE!");
                pageLoaded = true;
            }

            if (urlRequest.url().contains("https://www.youtube.com/api/stats/watchtime") && urlRequest.url().contains("state=paused") && vidStarted) {
                System.out.println("VID DONE!");

                try {
                    handle.breakLoop();
                }catch (Exception e){
                    e.printStackTrace();
                }
            }else{
                return InterceptRequestCallback.Response.proceed();
            }


            return InterceptRequestCallback.Response.proceed();
        });

        return browserEngine;
    }

    public static BrowserView createBrowserView(Engine browserEngine){
        Browser browser = browserEngine.newBrowser();

        BrowserView browserView = BrowserView.newInstance(browser);
        browserView.getProperties().put("Engine",browserEngine);

        return browserView;
    }

    public static void main(String[] args) throws PcapNativeException, NotOpenException {
        // The code we had before
        PcapNetworkInterface device = getNetworkDevice();
        System.out.println("You chose: " + device);

        // New code below here
        if (device == null) {
            System.out.println("No device chosen.");
            System.exit(1);
        }

        try {
            File initialFile = new File("videos.json");
            InputStream in = new FileInputStream(initialFile);
            BufferedReader reader = new BufferedReader(new InputStreamReader(in));
            String content = IOUtils.toString(reader);  // or any other encoding
            JsonObject jsonObject = gson.fromJson(content, JsonObject.class);
            //videosObject = jsonObject.get("videos").getAsJsonObject();
            videosObject = jsonObject;
        }catch (Exception e){
            e.printStackTrace();
            System.exit(1);
        }



        Engine browserEngine = createEngine("chrome/default");
        //System.out.println(SettingsLoader.getSettings().getBrowserProxy());
        //setProxy(defaultBrowserEngine, getProxy(defaultBrowserEngine));

        browserView = createBrowserView(browserEngine);

        BrowserLauncher.setBrowserView(browserView);
        new Thread(() -> Application.launch(BrowserLauncher.class)).start();

        /*
        (new Thread() {
            public void run() {
                while(true) {
                    try {
                        Element documentElement = browserView.getBrowser().mainFrame().get().document().get().documentElement().get();
                        while (documentElement.findElementByClassName("ytp-ad-skip-button").isPresent()) {
                            documentElement.findElementByClassName("ytp-ad-skip-button").get().click();
                            try {
                                Thread.sleep(500);
                            } catch (Exception e) {
                                e.printStackTrace();
                            }
                        }

                        Thread.sleep(1000);
                    } catch (Exception e) {
                        e.printStackTrace();
                    }
                }
            }
        }).start();
         */


        // Open the device and get a handle
        int snapshotLength = 65536; // in bytes
        int readTimeout = 50; // in milliseconds

        boolean needToSkip = false;
        String lastSkipped = "";

        for(String videoId : videosObject.keySet()) {
            if (new File(videoId + ".pcap").exists()) {
                needToSkip = true;
                lastSkipped = videoId;
            }
        }

        if(needToSkip && new File(lastSkipped + ".pcap").exists()){
            new File(lastSkipped + ".pcap").delete();
        }

        for(String videoId : videosObject.keySet()) {
            if(new File(videoId + ".pcap").exists()){
                System.out.println("VIDEO "+videoId+" ALREADY CAPTURED, SKIPPING...");
                continue;
            }


            pageLoaded = false;
            vidStarted = false;

            handle = device.openLive(snapshotLength, PcapNetworkInterface.PromiscuousMode.NONPROMISCUOUS, readTimeout);
            dumper = handle.dumpOpen(videoId + ".pcap");

            // Set a filter to only listen for tcp packets on port 80 (HTTP)
            String filter = "tcp port 443";
            handle.setFilter(filter, BpfProgram.BpfCompileMode.OPTIMIZE);

            // Create a listener that defines what to do with the received packets
            PacketListener listener = new PacketListener() {
                @Override
                public void gotPacket(Packet packet) {
                    // Print packet information to screen
                    //System.out.println(handle.getTimestamp());
                    //System.out.println(packet);

                    // Dump packets to file
                    try {
                        dumper.dump(packet, handle.getTimestamp());
                    } catch (NotOpenException e) {
                        e.printStackTrace();
                    }
                }
            };

            // Tell the handle to loop using the listener we created
            try {
                int maxPackets = 50000;


                try {
                    Thread.sleep(1000);
                    System.out.println("LOADING "+videoId);
                    browserView.getBrowser().navigation().loadUrl("https://www.youtube.com/watch?v=" + videoId);


                    int retryCount = 0;
                    while (true) {
                        if (pageLoaded = true) {
                            (new Thread() {
                                public void run() {
                                    try {
                                        Thread.sleep(500);
                                    } catch (Exception e) {
                                        e.printStackTrace();
                                    }
                                    System.out.println("STARTING VIDEO!");
                                    browserView.getBrowser().dispatch(KeyTyped.newBuilder(KeyCode.KEY_CODE_SPACE).build());
                                    try {
                                        Thread.sleep(500);
                                    } catch (Exception e) {
                                        e.printStackTrace();
                                    }
                                    vidStarted = true;
                                }
                            }).start();

                            break;
                        } else if (retryCount >= 20) {
                            continue;
                        }
                    }
                } catch (Exception e) {
                    e.printStackTrace();
                }

                System.out.println("STARTING CAPTURE!");
                handle.loop(maxPackets, listener);
            }catch (java.lang.InterruptedException interruptedE){
                //DO NOTHING WHEN INTERRUPTED, FUNCTIONALITY IS EXPECTED
            }catch (Exception e) {
                e.printStackTrace();
            }

            // Print out handle statistics
            PcapStat stats = handle.getStats();
            System.out.println("Packets received: " + stats.getNumPacketsReceived());
            System.out.println("Packets dropped: " + stats.getNumPacketsDropped());
            System.out.println("Packets dropped by interface: " + stats.getNumPacketsDroppedByIf());
            // Supported by WinPcap only
            if (Platform.isWindows()) {
                System.out.println("Packets captured: " +stats.getNumPacketsCaptured());
            }


            // Cleanup when complete
            if(dumper.isOpen()){
                dumper.close();
            }
            if(handle.isOpen()){
                handle.close();
            }
        }
    }
}
