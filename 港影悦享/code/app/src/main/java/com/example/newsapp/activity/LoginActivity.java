package com.example.newsapp.activity;

import android.Manifest;
import android.content.pm.PackageManager;
import android.text.TextUtils;
import android.widget.EditText;

import androidx.core.app.ActivityCompat;

import com.example.newsapp.Config;
import com.example.newsapp.MainActivity;
import com.example.newsapp.R;
import com.example.newsapp.base.BaseActivity;
import com.example.newsapp.bean.CommonBean;
import com.example.newsapp.bean.LoginDTO;
import com.example.newsapp.net.HttpManager;

import io.reactivex.Observable;
import io.reactivex.functions.Consumer;

/**
 * create by liubit on 2021/7/3
 */
public class LoginActivity extends BaseActivity {
    EditText mEtPhone;
    EditText mEtPw;

    @Override
    protected void onBindMainLayoutId() {
        setContentView(R.layout.activity_login);
    }

    @Override
    protected void onInitView() {
        mEtPhone = findViewById(R.id.mEtPhone);
        mEtPw = findViewById(R.id.mEtPw);
        findViewById(R.id.mBtnLogin).setOnClickListener(view -> login());
        findViewById(R.id.mBtnReg).setOnClickListener(view -> reg());

        checkPermission();
    }

    private void login(){
        if(TextUtils.isEmpty(mEtPhone.getText().toString())){
            showToast("请输入帐号");
            return;
        }
        if(TextUtils.isEmpty(mEtPw.getText().toString())){
            showToast("请输入帐号");
            return;
        }
        LoginDTO loginDTO = new LoginDTO(mEtPhone.getText().toString(),mEtPw.getText().toString());
        Observable loginObservable = HttpManager.getInstance().login(loginDTO);
        send(loginObservable, new Consumer() {
            @Override
            public void accept(Object o) throws Exception {
                CommonBean commonBean = (CommonBean) o;
                if(commonBean.getCode()==0){
                    Config.ACCOUNT = mEtPhone.getText().toString();
                    startAct(MainActivity.class);
                }else {
                    showToast(commonBean.getMsg());
                }
            }
        });
    }

    private void reg(){
        startAct(RegActivity.class);
    }

    void checkPermission(){
        if(ActivityCompat.checkSelfPermission(this, Manifest.permission.WRITE_EXTERNAL_STORAGE) != PackageManager.PERMISSION_GRANTED){
            ActivityCompat.requestPermissions(this,new String[]{Manifest.permission.WRITE_EXTERNAL_STORAGE}, 10);
        }
    }


}
