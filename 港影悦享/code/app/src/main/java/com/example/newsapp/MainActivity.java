package com.example.newsapp;

import android.view.View;
import android.view.animation.AnimationUtils;
import android.view.animation.LayoutAnimationController;

import androidx.recyclerview.widget.LinearLayoutManager;
import androidx.recyclerview.widget.RecyclerView;
import androidx.swiperefreshlayout.widget.SwipeRefreshLayout;

import com.example.newsapp.activity.MineActivity;
import com.example.newsapp.adapter.NewsAdapter;
import com.example.newsapp.base.BaseActivity;
import com.example.newsapp.bean.NewsBean;
import com.example.newsapp.bean.UserBean;
import com.example.newsapp.net.HttpManager;
import com.example.newsapp.tool.DialogTool;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.Random;

import io.reactivex.Observable;
import io.reactivex.functions.Consumer;

public class MainActivity extends BaseActivity {
    SwipeRefreshLayout mSwipeRefreshLayout;
    RecyclerView mRecyclerView;
    NewsAdapter adapter;
    List<NewsBean.DataBean> list = new ArrayList<>();

    @Override
    protected void onBindMainLayoutId() {
        setContentView(R.layout.activity_main);
    }

    @Override
    protected void onInitView() {
        setTitle("首页");
        setBackBtnVisibility(View.INVISIBLE);

        findViewById(R.id.mBtnInfo).setOnClickListener(view -> startAct(MineActivity.class));

        mSwipeRefreshLayout = findViewById(R.id.mSwipeRefreshLayout);
        mSwipeRefreshLayout.setOnRefreshListener(new SwipeRefreshLayout.OnRefreshListener() {
            @Override
            public void onRefresh() {
                getArticleList();
            }
        });
        mRecyclerView = findViewById(R.id.mRecyclerView);
        mRecyclerView.setLayoutManager(new LinearLayoutManager(context));
        LayoutAnimationController controller =
                AnimationUtils.loadLayoutAnimation(this, R.anim.item_anim);
        mRecyclerView.setLayoutAnimation(controller);

        getArticleList();

        Config.head_index = new Random().nextInt(Config.heads.size());
    }

    private void getArticleList(){
        DialogTool.showLoading(context);
        Observable observable = HttpManager.getInstance().getArticleList();
        send(observable, new Consumer() {
            @Override
            public void accept(Object o) throws Exception {
                mSwipeRefreshLayout.setRefreshing(false);
                DialogTool.dismissProgressDialog();
                NewsBean newsBean = (NewsBean) o;
                if(newsBean.getCode()==0){
                    list.clear();

                    List<NewsBean.DataBean> data = createRandomList(newsBean.getData());
                    if(data.size()>10){
                        for(int i=0;i<10;i++){
                            list.add(data.get(i));
                        }
                    }else {
                        list.addAll(data);
                    }
                    adapter = new NewsAdapter(context,list);
                    mRecyclerView.setAdapter(adapter);
                    mRecyclerView.scheduleLayoutAnimation();
                }else {
                    showToast(newsBean.getMsg());
                }
            }

        });
    }

    /**
     * 将list集合内容打散
     */
    private List<NewsBean.DataBean> createRandomList(List<NewsBean.DataBean> list) {
        Map<Integer, String> mmap = new HashMap<Integer, String>();
        List<NewsBean.DataBean> mlistNew = new ArrayList<NewsBean.DataBean>();
        while (mmap.size() < list.size()) {
            int random = (int) (Math.random() * list.size());
            if (!mmap.containsKey(random)) {
                mmap.put(random, "");
                mlistNew.add(list.get(random));
            }
        }
        return mlistNew;

    }

    @Override
    protected void onResume() {
        super.onResume();
        getUserInfo();
    }

    private void getUserInfo(){
        Observable observable = HttpManager.getInstance().getUserInfo(Config.ACCOUNT);
        send(observable, new Consumer() {
            @Override
            public void accept(Object o) throws Exception {
                UserBean userBean = (UserBean) o;
                Config.userBean = userBean;
            }

        });
    }

}