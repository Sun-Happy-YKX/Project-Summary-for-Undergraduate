package com.example.newsapp.dialog;

import android.app.Dialog;
import android.content.Context;
import android.os.Bundle;
import android.widget.EditText;
import android.widget.TextView;

import androidx.annotation.NonNull;

import com.example.newsapp.R;


/**
 * create by liubit on 2021/4/26
 */
public class InputDialog extends Dialog {
    private Context context;
    private EditText mEtName;
    private TextView mTvTitle;
    private DialogCallback callback;
    private String title;

    public InputDialog(@NonNull Context context) {
        super(context);
        this.context = context;
    }

    public InputDialog(@NonNull Context context, DialogCallback callback) {
        super(context);
        this.context = context;
        this.callback = callback;
    }

    public InputDialog(@NonNull Context context, String title, DialogCallback callback) {
        super(context);
        this.context = context;
        this.title = title;
        this.callback = callback;
    }

    public void setCallback(DialogCallback callback) {
        this.callback = callback;
    }

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.dialog_input);

        mEtName = findViewById(R.id.mEtName);
        mTvTitle = findViewById(R.id.mTvTitle);

        findViewById(R.id.mBtnClear).setOnClickListener(view -> mEtName.setText(""));
        findViewById(R.id.mBtnCancel).setOnClickListener(view -> dismiss());
        findViewById(R.id.mBtnSubmit).setOnClickListener(view -> submit());

        setCancelable(false);
        setCanceledOnTouchOutside(false);
    }

    public void setTitle(String title){
        mTvTitle.setText(title);
    }

    public void submit(){
        if(callback!=null){
            callback.submit(mEtName.getText().toString());
        }
        dismiss();
    }

    @Override
    public void show() {
        super.show();
    }

    public interface DialogCallback {
        void submit(String s);
    }

}
