package com.example.newsapp.bean;

/**
 * create by liubit on 2021/7/3
 */
public class UserBean {

    /**
     * msg : 操作成功
     * code : 0
     * data : {"id":3,"name":null,"pwd":"222","sex":null,"phone":"111","email":null,"birthday":null,"createTime":"2021-07-03 00:00:00"}
     */

    private String msg;
    private int code;
    /**
     * id : 3
     * name : null
     * pwd : 222
     * sex : null
     * phone : 111
     * email : null
     * birthday : null
     * createTime : 2021-07-03 00:00:00
     */

    private DataBean data;

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

    public DataBean getData() {
        return data;
    }

    public void setData(DataBean data) {
        this.data = data;
    }

    public static class DataBean {
        private int id;
        private String name;
        private String pwd;
        private Object sex;
        private String phone;
        private Object email;
        private Object birthday;
        private String createTime;

        public int getId() {
            return id;
        }

        public void setId(int id) {
            this.id = id;
        }

        public String getName() {
            return name;
        }

        public void setName(String name) {
            this.name = name;
        }

        public String getPwd() {
            return pwd;
        }

        public void setPwd(String pwd) {
            this.pwd = pwd;
        }

        public Object getSex() {
            return sex;
        }

        public void setSex(Object sex) {
            this.sex = sex;
        }

        public String getPhone() {
            return phone;
        }

        public void setPhone(String phone) {
            this.phone = phone;
        }

        public Object getEmail() {
            return email;
        }

        public void setEmail(Object email) {
            this.email = email;
        }

        public Object getBirthday() {
            return birthday;
        }

        public void setBirthday(Object birthday) {
            this.birthday = birthday;
        }

        public String getCreateTime() {
            return createTime;
        }

        public void setCreateTime(String createTime) {
            this.createTime = createTime;
        }
    }
}
