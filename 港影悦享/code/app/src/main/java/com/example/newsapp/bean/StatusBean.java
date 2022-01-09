package com.example.newsapp.bean;

/**
 * create by liubit on 2021/7/3
 */
public class StatusBean {

    /**
     * msg : 未关注
     * code : 0
     * data : false
     */

    private String msg;
    private int code;
    private boolean data;

    public String getMsg() {
        return msg;
    }

    public void setMsg(String msg) {
        this.msg = msg;
    }

    public int getCode() {
        return code;
    }

    public void setCode(int code) {
        this.code = code;
    }

    public boolean isData() {
        return data;
    }

    public void setData(boolean data) {
        this.data = data;
    }
}
