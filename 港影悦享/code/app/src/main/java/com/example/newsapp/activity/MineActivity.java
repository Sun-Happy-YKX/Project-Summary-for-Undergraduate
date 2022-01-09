package com.example.newsapp.activity;

import android.widget.ImageView;
import android.widget.TextView;

import com.example.newsapp.Config;
import com.example.newsapp.R;
import com.example.newsapp.adapter.NewsAdapter;
import com.example.newsapp.base.BaseActivity;
import com.example.newsapp.bean.NewsBean;
import com.example.newsapp.bean.UserBean;
import com.example.newsapp.net.HttpManager;
import com.example.newsapp.tool.DialogTool;

import io.reactivex.Observable;
import io.reactivex.functions.Consumer;

/**
 * create by liubit on 2021/7/3
 */
public class MineActivity extends BaseActivity {
    TextView mTvName;
    TextView mTvAccount;
    ImageView mIvHead;

    @Override
    protected void onBindMainLayoutId() {
        setContentView(R.layout.activity_mine);
    }

    @Override
    protected void onInitView() {
        setTitle("个人中心");
        setBackBtn();

        mTvName = findViewById(R.id.mTvName);
        mTvAccount = findViewById(R.id.mTvAccount);
        mIvHead = findViewById(R.id.mIvHead);

//        if(Config.userBean==null){
//            getUserInfo();
//        }else {
//            mTvName.setText("用户名："+Config.userBean.getData().getName());
//            mTvAccount.setText("帐    号："+Config.userBean.getData().getPhone());
//        }
        getUserInfo();

        mIvHead.setBackgroundResource(Config.heads.get(Config.head_index));

    }

    private void getUserInfo(){
        DialogTool.showLoading(context);
        Observable observable = HttpManager.getInstance().getUserInfo(Config.ACCOUNT);
        send(observable, new Consumer() {
            @Override
            public void accept(Object o) throws Exception {
                DialogTool.dismissProgressDialog();
                UserBean userBean = (UserBean) o;
                Config.userBean = userBean;
                if(userBean.getCode()==0){
                    mTvName.setText("用户名："+userBean.getData().getName());
                    mTvAccount.setText("帐    号："+userBean.getData().getPhone());
                }else {
                    showToast(userBean.getMsg());
                    finish();
                }
            }

        });
    }
}
