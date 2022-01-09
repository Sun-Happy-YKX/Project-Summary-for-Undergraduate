package com.example.newsapp.adapter;

import android.content.Context;
import android.content.Intent;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.BaseAdapter;
import android.widget.ImageView;
import android.widget.LinearLayout;
import android.widget.TextView;
import android.widget.Toast;

import androidx.annotation.NonNull;
import androidx.constraintlayout.widget.ConstraintLayout;
import androidx.recyclerview.widget.RecyclerView;

import com.bumptech.glide.Glide;
import com.example.newsapp.R;
import com.example.newsapp.activity.DetailActivity;
import com.example.newsapp.bean.NewsBean;

import java.util.List;

/**
 * create by liubit on 2021/7/3
 */
public class NewsAdapter extends RecyclerView.Adapter<NewsAdapter.MyViewHolder> {
    private Context context;
    private List<NewsBean.DataBean> list;

    public NewsAdapter(Context context, List<NewsBean.DataBean> list) {
        this.context = context;
        this.list = list;
    }

    @NonNull
    @Override
    public MyViewHolder onCreateViewHolder(@NonNull ViewGroup parent, int viewType) {
        MyViewHolder holder = new MyViewHolder(LayoutInflater.from(context).inflate(R.layout.item_news,parent,false));
        return holder;
    }

    @Override
    public void onBindViewHolder(@NonNull MyViewHolder holder, int position) {
        holder.mTvTitle.setText(list.get(position).getName());
        holder.mTvTime.setText(list.get(position).getCreateTime());
        holder.mItem.setOnClickListener(view -> {
            if(list.get(position)==null){
                Toast.makeText(context,"数据不能为空",Toast.LENGTH_SHORT).show();
            }else {
                Intent intent = new Intent(context, DetailActivity.class);
                intent.putExtra("data", list.get(position));
                context.startActivity(intent);
            }
        });
        Glide.with(context).load(list.get(position).getImages()).into(holder.mIvImg);
    }

    @Override
    public int getItemCount() {
        return list.size();
    }

    class MyViewHolder extends RecyclerView.ViewHolder {
        TextView mTvTitle,mTvTime;
        ConstraintLayout mItem;
        ImageView mIvImg;

        MyViewHolder(View view) {
            super(view);
            mTvTitle = (TextView) view.findViewById(R.id.mTvTitle);
            mItem = (ConstraintLayout) view.findViewById(R.id.mItem);
            mTvTime = (TextView) view.findViewById(R.id.mTvTime);
            mIvImg = (ImageView) view.findViewById(R.id.mIvImg);
        }
    }
}
