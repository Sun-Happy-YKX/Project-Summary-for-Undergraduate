package com.example.newsapp;

import android.app.Application;

import com.example.newsapp.tool.CrashHandler;

/**
 * create by liubit on 2021/7/3
 */
public class App extends Application {
    private static App app;

    @Override
    public void onCreate() {
        super.onCreate();
        app = this;
        CrashHandler.getInstance().init(this);

    }

    public static App getApp(){
        return app;
    }
}
