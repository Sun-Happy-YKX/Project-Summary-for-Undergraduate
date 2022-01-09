// miniprogram/pages/upload_ready/upload_ready.js
import Notify from '@vant/weapp/notify/notify'

const db=wx.cloud.database()
const todos=db.collection('files')
var _this=null

Page({

  /**
   * 页面的初始数据
   */
  data: {
    fileSource:'',
    fileType:'',
    fileSize:0,
    shareNameValue:'', //分享的名称
    passwordValue:'',
    downloadNumLimit:-1, //-1代表没有次数限制
    showTimeLimit:false, //
    downloadDateLimit:7, //默认下载期限是7天
    showDateLimit:false,
    fileID:'' //云数据库里的文件id
  },

  /**
   * 生命周期函数--监听页面加载
   */
  onLoad: function (options) {
    _this=this
    this.setData({
      fileSource:options.filePath,
      fileType:options.fileType,
      fileSize:(options.fileSize/1024/1024).toFixed(2)
    })
    console.log('filesource'+this.fileSource)
  },

  setTimeLimit(e){
    this.setData({
      showTimeLimit:e.detail
    })
  },

  setPasswordShow(e){
    this.setData({
      showPasswordInput:e.detail
    })
  },

  setDateShow(e){
    this.setData({
      showDateLimit:e.detail
    })
  },

  doUploadToCloud(){
    if(_this.data.shareNameValue==''){
      Notify({ type: 'primary', message: '分享名称不能为空' })
      return
    }
    console.log('调用了上传的函数')
    wx.showLoading({
      title: '上传中',
    })
    const cloudPath = `my-images`+Date.now()+getApp().globalData.openid
    wx.cloud.uploadFile({
      cloudPath:cloudPath,
      filePath:_this.data.fileSource,
      success: res => {
        this.setData({
          fileID:res.fileID
        })
        todos.add({
          data:{
            fileID:res.fileID,
            shareName:_this.data.shareNameValue,
            fileSize:_this.data.fileSize,
            fileType:_this.data.fileType,
            uploadDate:Date.now(),
            downloadPassword:_this.data.passwordValue,
            downloadDateLimit:_this.data.downloadDateLimit,
            downloadNumLimit:_this.data.downloadNumLimit, 
            downloadNums:0 //默认下载次数是0
          },
          success: res => {
            console.log(_this.data.shareNameValue)
            wx.navigateTo({ //跳转至上传完成界面
              url: '../uploadFinishPage/uploadFinishPage?recordID='+res._id+"&shareName="+_this.data.shareNameValue+'&shareType=normal',
            })
            console.log(res)
          },
          fail: e => {
            console.log(e)
          }
        })
        console.log('[上传文件] 成功：', res)
        console.log('filepath'+fileSource)
        console.log('fileType'+fileType)
      },
      fail: e => {
        console.error('[上传文件] 失败：', e)
        wx.showToast({
          icon: 'none',
          title: '上传失败',
        })
      },
      complete: () => {
        wx.hideLoading()
      }
    })
  },

  onChangeNumLimit(e){
    this.setData({
      downloadNumLimit:e.detail
    })
  },

  onChangeDateLimit(e){
    this.setData({
      downloadDateLimit:e.detail
    })
  },

  previewImage() {
    wx.previewImage({
      urls: [this.data.fileSource],
      current: 'current',
      success: (res) => {},
      fail: (res) => {},
      complete: (res) => {},
    })
  },
  previewdoc(){
    
        // let filePath = res.tempFiles[0].path; //微信临时文件路径
        wx.openDocument({
          filePath: this.data.fileSource,
                showMenu: false,  //是否显示右上角菜单按钮  默认为false
          success: function (res) {
            console.log('打开本地文档成功')
          },
          fail: function(error){
            console.log("打开本地文件失败")
          }
        })
  }

})
