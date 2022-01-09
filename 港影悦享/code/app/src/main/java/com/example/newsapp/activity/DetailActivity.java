package com.example.newsapp.activity;

import android.content.Context;
import android.webkit.WebSettings;
import android.webkit.WebView;
import android.webkit.WebViewClient;
import android.widget.TextView;

import androidx.recyclerview.widget.LinearLayoutManager;
import androidx.recyclerview.widget.RecyclerView;

import com.example.newsapp.Config;
import com.example.newsapp.R;
import com.example.newsapp.adapter.CommentAdapter;
import com.example.newsapp.adapter.NewsAdapter;
import com.example.newsapp.base.BaseActivity;
import com.example.newsapp.bean.CommentBean;
import com.example.newsapp.bean.CommonBean;
import com.example.newsapp.bean.NewsBean;
import com.example.newsapp.bean.StatusBean;
import com.example.newsapp.dialog.InputDialog;
import com.example.newsapp.net.HttpManager;
import com.example.newsapp.tool.DialogTool;

import io.reactivex.Observable;
import io.reactivex.functions.Consumer;

/**
 * create by liubit on 2021/7/3
 */
public class DetailActivity extends BaseActivity {
    private NewsBean.DataBean dataBean;
    WebView mWebView;
    TextView mBtnGood;
    TextView mBtnComment;
    RecyclerView mRecyclerView;

    @Override
    protected void onBindMainLayoutId() {
        setContentView(R.layout.activity_detail);
    }

    @Override
    protected void onInitView() {
        setTitle("详情");
        setBackBtn();

        dataBean = (NewsBean.DataBean) getIntent().getSerializableExtra("data");

        mRecyclerView = findViewById(R.id.mRecyclerView);
        mRecyclerView.setLayoutManager(new LinearLayoutManager(context));

        mBtnGood = findViewById(R.id.mBtnGood);
        mBtnGood.setOnClickListener(view -> followme());
        mBtnComment = findViewById(R.id.mBtnComment);
        mBtnComment.setOnClickListener(view -> showCommentDialog());

        mWebView = findViewById(R.id.mWebView);
        initSetting(mWebView);

        mWebView.loadData(dataBean.getContent(),"text/html",  "utf-8");
        getComments();
        getStatus();
    }

    private void showCommentDialog(){
        InputDialog dialog = new InputDialog(context, new InputDialog.DialogCallback() {
            @Override
            public void submit(String s) {
                doComment(s);
            }
        });
        dialog.show();
    }

    @Override
    protected void onResume() {
        super.onResume();
    }

    /**
     * 配置 webview
     *
     * @param webView
     */
    public static void initSetting(WebView webView) {

        WebSettings settings = webView.getSettings();

        settings.setAllowFileAccess(true);
        settings.setAllowContentAccess(true);

        settings.setJavaScriptEnabled(true);

        //隐藏webview缩放按钮
        settings.setDisplayZoomControls(false);

        // 隐藏缩放按钮
        settings.setBuiltInZoomControls(true);

        settings.setUseWideViewPort(true);

        //设置WebView是否以概览模式加载页面，即按宽度缩小内容以适应屏幕。
        settings.setLoadWithOverviewMode(true);

        // 是否允许Cache，默认false。考虑需要存储缓存，应该为缓存指定存储路径setAppCachePath
        settings.setAppCacheEnabled(true);

        // 设置可以使用localStorage
        settings.setDomStorageEnabled(true);

        // 应用可以有数据库
        settings.setDatabaseEnabled(true);

        webView.setInitialScale(100);

        //字体放大
        settings.setTextZoom(100);

        webView.setWebViewClient(new WebViewClient(){
            @Override
            public boolean shouldOverrideUrlLoading(WebView view, String url) {
                view.loadUrl(url);
                return true;
            }
        });
    }

    private void doComment(String txt){
        Observable observable = HttpManager.getInstance().addComment(dataBean.getId(), txt, Config.userBean.getData().getId());
        send(observable, new Consumer() {
            @Override
            public void accept(Object o) throws Exception {
                CommonBean newsBean = (CommonBean) o;
                if(newsBean.getCode()==0){
                    showToast("评论成功");
                    getComments();
                }else {
                    showToast(newsBean.getMsg());
                }
            }

        });
    }

    private void getComments(){
        Observable observable = HttpManager.getInstance().getComments(dataBean.getId(), Config.userBean.getData().getId());
        send(observable, new Consumer() {
            @Override
            public void accept(Object o) throws Exception {
                CommentBean newsBean = (CommentBean) o;
                if(newsBean.getCode()==0){
                    CommentAdapter adapter = new CommentAdapter(context,newsBean.getData());
                    mRecyclerView.setAdapter(adapter);
                }else {
                    showToast(newsBean.getMsg());
                }
            }

        });
    }

    private void getStatus(){
        Observable observable = HttpManager.getInstance().getStatus(dataBean.getId(), Config.userBean.getData().getId());
        send(observable, new Consumer() {
            @Override
            public void accept(Object o) throws Exception {
                StatusBean newsBean = (StatusBean) o;
                if(newsBean.getCode()==0){
                    if(newsBean.isData()){
                        mBtnGood.setText("取消点赞");
                    }else {
                        mBtnGood.setText("点赞");
                    }
                }else {
                    showToast(newsBean.getMsg());
                }
            }

        });
    }

    private void followme(){
        if("点赞".equals(mBtnGood.getText().toString())){
            followmeAdd();
        }else {
            followmeRemove();
        }
    }

    private void followmeAdd(){
        Observable observable = HttpManager.getInstance().followmeAdd(dataBean.getId(), Config.userBean.getData().getId());
        send(observable, new Consumer() {
            @Override
            public void accept(Object o) throws Exception {
                CommonBean newsBean = (CommonBean) o;
                if(newsBean.getCode()==0){
                    showToast("点赞完成");
                    getStatus();
                }else {
                    showToast(newsBean.getMsg());
                }
            }

        });
    }

    private void followmeRemove(){
        Observable observable = HttpManager.getInstance().followmeRemove(dataBean.getId(), Config.userBean.getData().getId());
        send(observable, new Consumer() {
            @Override
            public void accept(Object o) throws Exception {
                CommonBean newsBean = (CommonBean) o;
                if(newsBean.getCode()==0){
                    showToast("取消点赞完成");
                    getStatus();
                }else {
                    showToast(newsBean.getMsg());
                }
            }

        });
    }


}
