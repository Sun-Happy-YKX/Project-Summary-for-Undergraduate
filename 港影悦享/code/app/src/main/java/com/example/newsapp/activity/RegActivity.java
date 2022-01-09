package com.example.newsapp.activity;

import android.Manifest;
import android.content.pm.PackageManager;
import android.text.TextUtils;
import android.widget.EditText;

import androidx.core.app.ActivityCompat;

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
public class RegActivity extends BaseActivity {
    EditText mEtPhone;
    EditText mEtPw;
    EditText mEtName;

    @Override
    protected void onBindMainLayoutId() {
        setContentView(R.layout.activity_reg);
    }

    @Override
    protected void onInitView() {
        setTitle("注册");
        setBackBtn();

        mEtPhone = findViewById(R.id.mEtPhone);
        mEtPw = findViewById(R.id.mEtPw);
        mEtName = findViewById(R.id.mEtName);
        findViewById(R.id.mBtnReg).setOnClickListener(view -> reg());

    }

    private void reg(){
        if(TextUtils.isEmpty(mEtPhone.getText().toString())){
            showToast("请输入帐号");
            return;
        }
        if(TextUtils.isEmpty(mEtPw.getText().toString())){
            showToast("请输入帐号");
            return;
        }
        if(TextUtils.isEmpty(mEtName.getText().toString())){
            showToast("请输入用户名");
            return;
        }
        LoginDTO loginDTO = new LoginDTO(mEtPhone.getText().toString(),mEtPw.getText().toString());
        loginDTO.setName(mEtName.getText().toString());
        Observable loginObservable = HttpManager.getInstance().register(loginDTO);
        send(loginObservable, new Consumer() {
            @Override
            public void accept(Object o) throws Exception {
                CommonBean commonBean = (CommonBean) o;
                if(commonBean.getCode()==0){
                    showToast("注册成功");
                    finish();
                }else {
                    showToast(commonBean.getMsg());
                }
            }
        });
    }

}
