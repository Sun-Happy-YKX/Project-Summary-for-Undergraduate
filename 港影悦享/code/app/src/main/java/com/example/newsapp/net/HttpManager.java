package com.example.newsapp.net;

import com.example.newsapp.Config;
import com.example.newsapp.bean.LoginDTO;

import java.util.concurrent.TimeUnit;

import io.reactivex.Observable;
import io.reactivex.functions.Function;
import io.reactivex.schedulers.Schedulers;
import okhttp3.OkHttpClient;
import retrofit2.Retrofit;
import retrofit2.adapter.rxjava2.RxJava2CallAdapterFactory;
import retrofit2.converter.gson.GsonConverterFactory;
import retrofit2.converter.scalars.ScalarsConverterFactory;

public class HttpManager {
    /**
     * retrofit框架
     */
    private Retrofit retrofit;
    private OkHttpClient httpClientBuilder, downloadHttpClientBuilder;
    /**
     * 服务器请求接口
     */
    private MobileService apiService;


    public HttpManager() {
        //创建一个Http并且设置超时时间
        //初始化OkHttp
        httpClientBuilder = new OkHttpClient.Builder()
                .readTimeout(15, TimeUnit.SECONDS)
                .writeTimeout(15, TimeUnit.SECONDS)
                //设置超时时间，这里以秒为单位
                .connectTimeout(15, TimeUnit.SECONDS)
                .retryOnConnectionFailure(true)
//                .cache(setCache())//设置磁盘缓存
                //添加打印拦截
//                .addInterceptor(new InterceptorSign())
                .addInterceptor(new PrintLogInterceptor())
                .build();
        //初始化下载用OkHttp
        downloadHttpClientBuilder = new OkHttpClient.Builder()
                .readTimeout(15, TimeUnit.SECONDS)
                .writeTimeout(15, TimeUnit.SECONDS)
                //设置超时时间，这里以秒为单位
                .connectTimeout(15, TimeUnit.SECONDS)
                .retryOnConnectionFailure(true)
                .build();
        retrofit = new Retrofit.Builder()
                .baseUrl(Config.BASE_URL)
                .addConverterFactory(ScalarsConverterFactory.create())//添加String 转还器
                .addConverterFactory(GsonConverterFactory.create())
                .addCallAdapterFactory(RxJava2CallAdapterFactory.create())
                .client(httpClientBuilder)
                .build();

        //创建http接口事件
        apiService = retrofit.create(MobileService.class);
    }

    private static synchronized void init() {
        if (SingleHolder.INSTANCE == null) {
            SingleHolder.INSTANCE = new HttpManager();
        }
    }

    //延迟实例化
    public static HttpManager getInstance() {
        if (SingleHolder.INSTANCE == null) {
            init();
        }
        return SingleHolder.INSTANCE;
    }

    public static void release() {
        SingleHolder.INSTANCE = null;
    }

    public OkHttpClient getDownloadHttpClientBuilder() {
        return downloadHttpClientBuilder;
    }

    public OkHttpClient get() {
        return httpClientBuilder;
    }

    private Observable parseResponse(Observable resultOb) {
        return resultOb.subscribeOn(Schedulers.io()).flatMap((Function<Object, Observable<?>>) httpResponse -> {
                    if (httpResponse == null)
                        return Observable.error(new ServerException("-999", "接口请求失败"));
                    else
                        return Observable.just(httpResponse);

                }
        );
    }

    public Observable login(LoginDTO loginDTO) {
        return apiService.login(loginDTO.getPhone(), loginDTO.getPwd()).subscribeOn(Schedulers.io());
    }

    public Observable register(LoginDTO loginDTO) {
        return apiService.register(loginDTO.getPhone(), loginDTO.getPwd(), loginDTO.getName()).subscribeOn(Schedulers.io());
    }

    public Observable getArticleList() {
        return apiService.getArticleList().subscribeOn(Schedulers.io());
    }

    public Observable getUserInfo(String account) {
        return apiService.getUserInfo(account).subscribeOn(Schedulers.io());
    }

    public Observable getComments(int articleId,int userId) {
        return apiService.getComments(articleId).subscribeOn(Schedulers.io());
    }

    public Observable getStatus(int followId,int userId) {
        return apiService.getStatus(followId,userId).subscribeOn(Schedulers.io());
    }

    public Observable addComment(int articleId,String txt,int userId) {
        return apiService.addComment(articleId,txt,userId).subscribeOn(Schedulers.io());
    }

    public Observable followmeAdd(int articleId,int userId) {
        return apiService.followmeAdd(articleId,userId).subscribeOn(Schedulers.io());
    }

    public Observable followmeRemove(int followId,int userId) {
        return apiService.followmeRemove(followId,userId).subscribeOn(Schedulers.io());
    }

    /**
     * 在访问HttpManager时创建单例
     */
    private static class SingleHolder {
        private static HttpManager INSTANCE = null;
    }

}
