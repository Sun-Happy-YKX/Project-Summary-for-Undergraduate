package com.example.newsapp.net;

import com.example.newsapp.bean.CommentBean;
import com.example.newsapp.bean.CommonBean;
import com.example.newsapp.bean.LoginDTO;
import com.example.newsapp.bean.NewsBean;
import com.example.newsapp.bean.StatusBean;
import com.example.newsapp.bean.UserBean;

import io.reactivex.Observable;
import retrofit2.http.Body;
import retrofit2.http.GET;
import retrofit2.http.POST;
import retrofit2.http.Query;


public interface MobileService {

    @GET(value = "/api/login")
    Observable<CommonBean> login(@Query("phone") String phone, @Query("pwd") String pwd);

    @GET(value = "/api/register")
    Observable<CommonBean> register(@Query("phone") String phone, @Query("pwd") String pwd, @Query("name") String name);

    @GET(value = "/api/articleList")
    Observable<NewsBean> getArticleList();

    @GET(value = "/api/getUserInfo")
    Observable<UserBean> getUserInfo(@Query("phone") String phone);

    @GET(value = "/api/comment/list")
    Observable<CommentBean> getComments(@Query("articleId") int articleId);

    @GET(value = "/api/followme/status")
    Observable<StatusBean> getStatus(@Query("followId") int followId, @Query("userId") int userId);

    @GET(value = "/api/comment/add")
    Observable<CommonBean> addComment(@Query("articleId") int articleId,@Query("content") String content, @Query("userId") int userId);

    @GET(value = "/api/followme/add")
    Observable<CommonBean> followmeAdd(@Query("followId") int articleId,@Query("userId") int userId);

    @GET(value = "/api/followme/remove")
    Observable<CommonBean> followmeRemove(@Query("followId") int followId,@Query("userId") int userId);

}
