//index.js 测试git
const app = getApp()
var _this
let that = this;

Page({
  data: {
    height:0,
    clientHeight:0,
    activeTab:0,
    avatarUrl: './user-unlogin.png',
    userInfo: {},
    hasUserInfo: false,
    logged: false,
    takeSession: false,
    requestResult: '',
    canIUseGetUserProfile: false,
    canIUseOpenData: wx.canIUse('open-data.type.userAvatarUrl'), // 如需尝试获取用户信息可改为false,
    isQuestionFile:false,
    pop_show:false, //弹窗的显示控制
    textValue:"",
    jpg_source:"",
    actionSheetShow: false,
    questionActionSheetShow:false, //问答文件的选择菜单
    actions: [
      {
        name: '从手机相册选择',
      },
      {
        name: '从聊天记录选择',
      },
    ],
  },

  onLoad: function() {
    _this = this
    _this.onGetOpenid()
    wx.getSystemInfo({
      success: function (res) {
        // 获取可使用窗口宽度
        let clientHeight = res.windowHeight;
        // 获取可使用窗口高度
        let clientWidth = res.windowWidth;
        // 算出比例
        let ratio = 750 / clientWidth;
        // 算出高度(单位rpx)
        let height = clientHeight * ratio;
        // 设置高度
        _this.setData({
          height: height,
          clientHeight:clientHeight
        });
      }
    });
  },

  getUserProfile() {
    // 推荐使用wx.getUserProfile获取用户信息，开发者每次通过该接口获取用户个人信息均需用户确认，开发者妥善保管用户快速填写的头像昵称，避免重复弹窗
    wx.getUserProfile({
      desc: '展示用户信息', // 声明获取用户个人信息后的用途，后续会展示在弹窗中，请谨慎填写
      success: (res) => {
        this.setData({
          avatarUrl: res.userInfo.avatarUrl,
          userInfo: res.userInfo,
          hasUserInfo: true,
        })
      }
    })
  },

  onGetUserInfo: function(e) {
    if (!this.data.logged && e.detail.userInfo) {
      this.setData({
        logged: true,
        avatarUrl: e.detail.userInfo.avatarUrl,
        userInfo: e.detail.userInfo,
        hasUserInfo: true,
      })
    }
  },

  onGetOpenid: function() {
    // 调用云函数
    wx.cloud.callFunction({
      name: 'login',
      data: {},
      success: res => {
        app.globalData.openid = res.result.openid
      },
      fail: err => {
        console.error('[云函数] [login] 调用失败', err)
      }
    })
  },

  doUpload(filePath,fileType,fileSize){ //上传普通文件
    wx.navigateTo({
      url: '../upload_ready/upload_ready?filePath='+filePath+'&fileType='+fileType+'&fileSize='+fileSize
    })
    wx.hideLoading({
      success: (res) => {},
    })
  },

  doUploadQuestionFile(filePath,fileType,fileSize){ //上传问答文件
    wx.navigateTo({
      url: '../uploadQuestionFileReadyPage/uploadQuestionFileReadyPage?filePath='+filePath+'&fileType='+fileType+'&fileSize='+fileSize
    })
    wx.hideLoading({
      success: (res) => {},
    })
  },

  // 上传图片
  chooseByAlbum: function () { //从手机相册选择
    // 选择图片
    wx.chooseImage({
      count: 1,
      sizeType: ['compressed'],
      sourceType: ['album', 'camera'],
      success: function (res) {
        
        wx.showLoading({
          title: '上传中',
        }
        )
        const filePath = res.tempFilePaths[0]
        const fileSize = res.tempFiles[0].size
        if(_this.data.isQuestionFile==false){
          _this.doUpload(filePath,"image",fileSize)
        }else{
          _this.doUploadQuestionFile(filePath,"image",fileSize)
        }
        // 上传图片
        
      },
      fail: e => {
        console.error(e)
      }
    })
  },
  
  tapUploadButton(){
    this.setData({
      actionSheetShow:true,
      isQuestionFile:false
    })
  },

  tapUploadQuestionFileButton(){
    this.setData({
      questionActionSheetShow:true,
      isQuestionFile:true
    })
  },

  onChange_text(event){
    this.setData({
      textValue:event.detail
    }),
    console.log(this.data.textValue)
  },
  
  onClose(){
    console.log('close')
  },

  onCloseActionSheet() {
    this.setData({ 
      actionSheetShow: false
    });
  },

  onCloseQuestionActionSheet() {
    this.setData({ 
      questionActionSheetShow: false
    });
  },

  onSelectActionSheet(event) {
    var resultFromActionSheet=event.detail;
    if(resultFromActionSheet.name=="从手机相册选择"){
      this.chooseByAlbum()
      return 
    }
    if(resultFromActionSheet.name="从聊天记录选择"){
      wx.chooseMessageFile({
        count: 10,
        type: 'all',
        success (res) {
          // tempFilePath可以作为img标签的src属性显示图片
          const tempFile = res.tempFiles[0]
          if(_this.data.isQuestionFile==false){
            _this.doUpload(tempFile.path,tempFile.type,tempFile.size)
          }else{
            _this.doUploadQuestionFile(tempFile.path,tempFile.type,tempFile.size)
          }
        }
      })
    }
  },

  tabOnChange(e){
    this.setData({
      activeTab:e.detail
    })
    console.log(this.activeTab)
    if(this.data.activeTab==1){
      wx.reLaunch({
        url: '../MyPage/MyPage',
      })
    }
  },

  swithToSharedFile(e){
    wx.navigateTo({
      url: '../sharedFile/sharedFile',
    })
  }

})
