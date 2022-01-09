// miniprogram/pages/login/login.js

const db = wx.cloud.database();
const userInfo = db.collection('userInfo');
const _ = db.command;
const app = getApp();
var _this

Page({
  data: {
    logged: true,
    userInfo: '',
    userID: ''
  },

  onLoad() {
    this.Login()
    console.log('获取数据')
    _this = this
  },

  getUserProfile() {
    console.log('臊皮罢了')
    // 推荐使用wx.getUserProfile获取用户信息，开发者每次通过该接口获取用户个人信息均需用户确认，开发者妥善保管用户快速填写的头像昵称，避免重复弹窗
    wx.getUserProfile({
      desc: '展示用户信息', // 声明获取用户个人信息后的用途，后续会展示在弹窗中，请谨慎填写
      success: (res) => {
        this.setData({
          userInfo: res.userInfo,
          hasUserInfo: true,
          logged:true
        })
        app.globalData.logged = true
        userInfo.add({ //未登录用户添加进云数据库
          data: {
            _userInfo: res.userInfo
          },
          success: function (res) {
            console.log(res)
          }
        })
      }
    })
  },
  Login: function () {
    // 调用云函数
    const _this = this
    wx.cloud.callFunction({
      name: 'login',
      data: {},
      success: res => {
        _this.data.userID = res.result.openid
        app.globalData.openid = res.result.openid
        db.collection('userInfo').where({
          _openid: res.result.openid,
        }).get({
          success: function (res2) {
            if (res2.data.length == 0) { //要是没有登录过
              console.log('没有登陆过')
              _this.setData({
                logged:false
              })
              return false
            } else {
              console.log('登陆过')
              console.log(res2)
              app.globalData.logged = true
              console.log(_this.data)
              _this.setData({
                logged: true,
                userInfo:res2.data[0]._userInfo
              })
              return true
            }
          }
        })
      },
      fail: err => {
        console.error('[云函数] [login] 调用失败', err)
        wx.navigateTo({
          url: '../deployFunctions/deployFunctions',
        })
      }
    })
  },

  switchToSharedFile(e){
    wx.navigateTo({
      url: '../UserSharedFile/sharedFile?userID='+this.data.userID,
    })
  }
})