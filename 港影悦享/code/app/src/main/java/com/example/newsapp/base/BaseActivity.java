package com.example.newsapp.base;

import android.app.ProgressDialog;
import android.content.ClipData;
import android.content.ClipboardManager;
import android.content.Context;
import android.content.Intent;
import android.os.Bundle;
import android.text.TextUtils;
import android.util.Log;
import android.view.View;
import android.widget.ImageView;
import android.widget.TextView;
import android.widget.Toast;

import androidx.annotation.Nullable;

import com.example.newsapp.R;
import com.trello.rxlifecycle3.android.ActivityEvent;
import com.trello.rxlifecycle3.components.support.RxAppCompatActivity;

import org.greenrobot.eventbus.EventBus;

import java.io.File;

import io.reactivex.Observable;
import io.reactivex.Observer;
import io.reactivex.android.schedulers.AndroidSchedulers;
import io.reactivex.functions.Consumer;
import io.reactivex.schedulers.Schedulers;

import static com.trello.rxlifecycle3.internal.Preconditions.checkNotNull;


/**
 * create by liubit on 2021/4/26
 */
public abstract class BaseActivity extends RxAppCompatActivity {
    protected Context context;
    protected String TAG = getClass().getSimpleName();
    /**
     * 绑定布局
     */
    protected abstract void onBindMainLayoutId();

    /**
     * 初始化你的页面，这里做完后，界面就优先显示布局了-【主线程
     */
    protected abstract void onInitView();


    @Override
    protected void onCreate(@Nullable Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        context = this;
        onBindMainLayoutId();
        onInitView();

    }

    public void setTitle(String title){
        TextView textView = findViewById(R.id.mMenuTitle);
        if(textView!=null){
            textView.setText(title);
        }
    }

    public void setBackBtn(){
        ImageView mBtnBack = findViewById(R.id.mBtnBack);
        if(mBtnBack!=null){
            mBtnBack.setOnClickListener(view -> finish());
        }
    }

    public void setBackBtnVisibility(int visibility){
        ImageView mBtnBack = findViewById(R.id.mBtnBack);
        if(mBtnBack!=null){
            mBtnBack.setVisibility(visibility);
        }
    }

    @Override
    protected void onDestroy() {
        context = null;
        super.onDestroy();
    }

    public void startAct(Class s){
        startActivity(new Intent(this,s));
    }

    public void send(Observable observable, Consumer consumer) {
        checkNotNull(observable, "observable is null");
        try {
            observable.compose(bindUntilEvent(ActivityEvent.DESTROY)).subscribeOn(Schedulers.io()).observeOn(AndroidSchedulers.mainThread()).subscribe(consumer);
        }catch (Exception e){
            e.printStackTrace();
        }
    }

    public void send(Observable observable, Observer observer) {
        checkNotNull(observable, "observable is null");
        try {
            observable.compose(bindUntilEvent(ActivityEvent.DESTROY)).subscribeOn(Schedulers.io()).observeOn(AndroidSchedulers.mainThread()).subscribe(observer);
        }catch (Exception e){
            e.printStackTrace();

        }
    }

    public void showToast(String txt){
        Toast.makeText(context,txt,Toast.LENGTH_SHORT).show();
    }

}
