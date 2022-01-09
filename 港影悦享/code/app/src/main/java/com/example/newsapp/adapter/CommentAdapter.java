package com.example.newsapp.adapter;

import android.content.Context;
import android.content.Intent;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.ImageView;
import android.widget.TextView;

import androidx.annotation.NonNull;
import androidx.constraintlayout.widget.ConstraintLayout;
import androidx.recyclerview.widget.RecyclerView;

import com.bumptech.glide.Glide;
import com.example.newsapp.Config;
import com.example.newsapp.R;
import com.example.newsapp.activity.DetailActivity;
import com.example.newsapp.bean.CommentBean;
import com.example.newsapp.bean.NewsBean;

import java.util.List;
import java.util.Random;

/**
 * create by liubit on 2021/7/3
 */
public class CommentAdapter extends RecyclerView.Adapter<CommentAdapter.MyViewHolder> {
    private Context context;
    private List<CommentBean.DataBean> list;

    public CommentAdapter(Context context, List<CommentBean.DataBean> list) {
        this.context = context;
        this.list = list;
    }

    @NonNull
    @Override
    public MyViewHolder onCreateViewHolder(@NonNull ViewGroup parent, int viewType) {
        MyViewHolder holder = new MyViewHolder(LayoutInflater.from(context).inflate(R.layout.item_comment,parent,false));
        return holder;
    }

    @Override
    public void onBindViewHolder(@NonNull MyViewHolder holder, int position) {
        holder.mTvName.setText(list.get(position).getName());
        holder.mTvContent.setText(list.get(position).getContent());
        holder.mIvHead.setBackgroundResource(Config.heads.get(new Random().nextInt(Config.heads.size())));
    }

    @Override
    public int getItemCount() {
        return list.size();
    }

    class MyViewHolder extends RecyclerView.ViewHolder {
        TextView mTvName,mTvContent;
        ImageView mIvHead;

        MyViewHolder(View view) {
            super(view);
            mTvName = (TextView) view.findViewById(R.id.mTvName);
            mTvContent = (TextView) view.findViewById(R.id.mTvContent);
            mIvHead = (ImageView) view.findViewById(R.id.mIvHead);

        }
    }
}
