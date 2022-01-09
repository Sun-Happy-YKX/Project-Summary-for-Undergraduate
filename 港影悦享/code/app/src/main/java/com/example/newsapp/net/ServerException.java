package com.example.newsapp.net;


/**
 * Created by 王玮 on 2016/9/12.
 */
public class ServerException extends Exception {
    private String code;

    public ServerException(String code, String msg) {
        super(msg);
        this.code = code;
    }

    public ServerException(String msg) {
        super(msg);
    }

    public String getCode() {
        return code;
    }

    public void setCode(String code) {
        this.code = code;
    }
}
