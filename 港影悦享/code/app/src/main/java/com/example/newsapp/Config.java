package com.example.newsapp;

import com.example.newsapp.bean.UserBean;

import java.util.ArrayList;
import java.util.List;

/**
 * create by liubit on 2021/7/3
 */
public class Config {

    public static final String BASE_URL = "http://121.5.67.175:8181";
    public static String ACCOUNT = "";
    public static UserBean userBean;
    public static int head_index = 0;

    public static List<Integer> heads = new ArrayList<Integer>(){{
        add(R.mipmap.head);
        add(R.mipmap.head2);
        add(R.mipmap.head3);
        add(R.mipmap.head4);
        add(R.mipmap.head5);
        add(R.mipmap.head6);
        add(R.mipmap.head7);
    }};

}
