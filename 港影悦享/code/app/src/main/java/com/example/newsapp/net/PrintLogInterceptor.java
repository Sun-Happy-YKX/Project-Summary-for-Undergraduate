package com.example.newsapp.net;


import android.util.Log;

import com.example.newsapp.tool.SharePerferenceUtils;
import com.google.gson.Gson;

import java.io.EOFException;
import java.io.IOException;
import java.nio.charset.Charset;

import okhttp3.Interceptor;
import okhttp3.MediaType;
import okhttp3.Request;
import okhttp3.RequestBody;
import okhttp3.Response;
import okhttp3.ResponseBody;
import okhttp3.internal.http.HttpHeaders;
import okio.Buffer;
import okio.BufferedSource;

/**
 * Created by 王玮 on 2016/9/8.
 */
public class PrintLogInterceptor implements Interceptor {
    private static final Charset UTF8 = Charset.forName("UTF-8");
    private String TAG = getClass().getSimpleName();
    private Gson gson = new Gson();

    public PrintLogInterceptor() {
    }

    @Override
    public Response intercept(Chain chain) throws IOException {
        Request request = chain.request();
//        request = request.newBuilder()
//                .addHeader("Authorization",
//                        SharePerferenceUtils.getString(MyApplication.getApp(), Config.TOKEN_KEY,""))
//                .build();
        printRequestLog(request);
        Response response;
        try {
            response = chain.proceed(request);
        } catch (Exception e) {
            Log.e(TAG, "[请求失败：] " + e);
            throw e;
        }
        printResponseLog(response);
        return response;
    }

    /**
     * 打印request日志
     *
     * @param request
     * @throws IOException
     */
    private void printRequestLog(Request request) throws IOException {
        RequestBody requestBody = request.body();
        boolean hasRequestBody = requestBody != null;
        String requestStartMessage = "[请求地址：] " + request.url();
        Log.i(TAG, "[请求header：]" + request.headers().toString());
        Log.i(TAG, requestStartMessage);
        if (hasRequestBody) {
            Buffer buffer = new Buffer();
            requestBody.writeTo(buffer);
            Charset charset = UTF8;
            MediaType contentType = requestBody.contentType();
            if (contentType != null) {
                charset = contentType.charset(UTF8);
            }
            if (isPlaintext(buffer)) {
                requestStartMessage = buffer.readString(charset);
            }
        }
        //打印请求log
        Log.i(TAG, requestStartMessage);
    }

    /**
     * 打印response日志
     *
     * @param response
     * @throws IOException
     */
    private void printResponseLog(Response response) throws IOException {
        ResponseBody responseBody = response.body();
        long contentLength = responseBody.contentLength();
        if (HttpHeaders.hasBody(response)) {//有返回数据
            Log.i(TAG, "[返回数据：]" + response.request());
            BufferedSource source = responseBody.source();
            source.request(Long.MAX_VALUE);
            Buffer buffer = source.buffer();
            if (contentLength != 0) {
                Log.i(TAG, "[返回地址：]" + response.request().url());
                Log.i(TAG, buffer.clone().readString(UTF8));
            }
        }
    }

    private boolean isPlaintext(Buffer buffer) {
        try {
            Buffer prefix = new Buffer();
            long byteCount = buffer.size() < 64 ? buffer.size() : 64;
            buffer.copyTo(prefix, 0, byteCount);
            for (int i = 0; i < 16; i++) {
                if (prefix.exhausted()) {
                    break;
                }
                int codePoint = prefix.readUtf8CodePoint();
                if (Character.isISOControl(codePoint) && !Character.isWhitespace(codePoint)) {
                    return false;
                }
            }
            return true;
        } catch (EOFException e) {
            Log.e(TAG, e.toString());
            return false;
        }
    }
}
