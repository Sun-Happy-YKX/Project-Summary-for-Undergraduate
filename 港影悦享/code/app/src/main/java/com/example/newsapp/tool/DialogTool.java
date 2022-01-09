package com.example.newsapp.tool;

import android.app.ProgressDialog;
import android.content.Context;

/**
 * create by liubit on 2021/4/26
 */
public class DialogTool {
    private static ProgressDialog progressDialog;

    public static void showLoading(Context context){
        progressDialog = new ProgressDialog(context);
        progressDialog.setTitle("温馨提示");
        progressDialog.setMessage("正在努力加载数据，请稍等~");
        progressDialog.show();
    }

    public static void dismissProgressDialog(){
        if(progressDialog!=null){
            progressDialog.dismiss();
        }
    }





}
