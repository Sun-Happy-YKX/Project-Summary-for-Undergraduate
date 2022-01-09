package com.example.newsapp.bean;

import java.util.List;

/**
 * create by liubit on 2021/7/3
 */
public class CommentBean {

    /**
     * msg : 操作成功
     * code : 0
     * data : [{"id":1,"userId":5,"articleId":3,"content":"123456","createTime":"2021-07-03 00:00:00"}]
     */

    private String msg;
    private int code;
    /**
     * id : 1
     * userId : 5
     * articleId : 3
     * content : 123456
     * createTime : 2021-07-03 00:00:00
     */

    private List<DataBean> data;

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

    public List<DataBean> getData() {
        return data;
    }

    public void setData(List<DataBean> data) {
        this.data = data;
    }

    public static class DataBean {
        private int id;
        private int userId;
        private int articleId;
        private String content;
        private String createTime;
        private String name;

        public String getName() {
            return name;
        }

        public void setName(String name) {
            this.name = name;
        }

        public int getId() {
            return id;
        }

        public void setId(int id) {
            this.id = id;
        }

        public int getUserId() {
            return userId;
        }

        public void setUserId(int userId) {
            this.userId = userId;
        }

        public int getArticleId() {
            return articleId;
        }

        public void setArticleId(int articleId) {
            this.articleId = articleId;
        }

        public String getContent() {
            return content;
        }

        public void setContent(String content) {
            this.content = content;
        }

        public String getCreateTime() {
            return createTime;
        }

        public void setCreateTime(String createTime) {
            this.createTime = createTime;
        }
    }
}
