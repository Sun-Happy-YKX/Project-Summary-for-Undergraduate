// miniprogram/pages/shareOpenPage/shareOpenPage.js
const db = wx.cloud.database()
const todos = db.collection('files')
var _this = null
const app = getApp()
const oneDay = 24 * 60 * 60 * 1000

Page({

  /**
   * 页面的初始数据
   */
  data: {
    isButtonForbidden: false, //按钮是否被禁用
    showPreviewButton: false, //预览按钮是否显示
    res: '',
    recordID: '',
    shareName: '',
    fileSize: 0,
    fileType: '',
    buttonText: '下载文件', //要是不符合条件就会变成其他文字 todo 最好按钮颜色也一并变化
    fileID: '',
    filePath: '',
    downloadNumLimit: -1,
    downloadDateLimit: '',
    downloadPassword: '',
    downloadNums: 0,
    showPasswordPop: false,
    is_password_false: false,
    enter_password: '',
    surplus_enter_num: 5, //输入密码容许五次输入错误
    actionSheetShow: false,
    actions: [{
      name: '保存到手机'
    }]
  },

  /**
   * 生命周期函数--监听页面加载
   */
  onLoad: function (options) {
    _this = this
    this.onGetOpenid()
    this.setData({
      recordID: options.recordID
    })
    console.log("recordID=" + options.recordID)
    todos.doc(this.data.recordID).get({ //云数据库里获取文件数据
      success: (res) => {
        this.setData({
          res: res.data,
          fileID: res.data.fileID
        })
        //开始给页面元素赋值
        var oneDay = 24 * 60 * 60 * 1000
        var res = this.data.res
        this.setData({
          shareName: res.shareName,
          fileSize: res.fileSize,
          fileType: res.fileType,
          downloadDateLimit: res.uploadDate + res.downloadDateLimit * oneDay,
          downloadNumLimit: res.downloadNumLimit,
          downloadNums: res.downloadNums,
          downloadPassword: res.downloadPassword
        })

        //开始判断文件附加条件
        //判断下载次数
        if (res.downloadNumLimit != -1) { //等于-1说明没有设置限制
          if (res.downloadNumLimit <= res.downloadNums) { //限制次数等于实际下载次数
            this.setData({
              buttonText: '超过下载次数限制',
              isButtonForbidden: true
            })
            return
          }
        }
        //判断日期
        if (res.downloadDateLimit * 24 * 60 * 60 * 1000 + res.uploadDate < Date.now()) { //超时了的话
          this.setData({
            buttonText: '超过下载期限',
            isButtonForbidden: true
          })
          return
        }
      },
      fail: (res) => {
        console.log('失败了')
        console.log(res)
      }
    })
  },
  downloadSharedFile() { //点击下载按钮之后
    if (this.data.isButtonForbidden == true) {
      return
    }
    if (this.data.downloadPassword == '') {
      this.downloadFile()
      this.setData({
        isButtonForbidden: true
      })
      if (_this.data.fileType == 'file') {
        _this.setData({
          showPreviewButton: true
        })
      }
    } else {
      this.setData({
        showPasswordPop: true
      })
    }
  },
  downloadFile: function () {
    _this = this
    wx.showLoading({
      title: '正在下载',
    })
    wx.cloud.downloadFile({
      fileID: this.data.fileID,
      success: res => {
        wx.hideLoading()
        this.setData({
          filePath: res.tempFilePath
        })
        //还应当增加文件的下载次数
        wx.cloud.callFunction({
          name: 'reduceDownloadTimes',
          data: {
            recordID: _this.data.recordID
          },
          complete: (res) => {
            console.log('增加了下载次数')
            console.log(res)
          }
        })
      },
      fail(res) {
        wx.showToast({
          title: '下载文件失败了',
          duration: 5000,
        })
      }
    })
  },
  enterPasswordChange: function (event) {
    this.setData({
      enter_password: event.detail
    })
  },
  confirmEnterPassword: function (event) {
    if (this.data.enter_password == this.data.downloadPassword) {
      this.closePasswordPop()
      this.downloadFile()
      this.setData({
        isButtonForbidden: true
      })
    } else {
      this.setData({
        is_password_false: true,
        enter_password: '',
        surplus_enter_num: this.data.surplus_enter_num - 1
      })
    }
    if (this.data.surplus_enter_num <= 0) {
      wx.switchTab({
        url: '../index/index'
      })
    }
  },
  closePasswordPop: function () {
    this.setData({
      showPasswordPop: false,
      enter_password: ''
    })
  },
  onGetOpenid: function () {
    // 调用云函数
    wx.cloud.callFunction({
      name: 'login',
      data: {},
      success: res => {
        console.log('[云函数] [login] user openid: ', res.result.openid)
        app.globalData.openid = res.result.openid
      },
      fail: err => {
        console.error('[云函数] [login] 调用失败', err)
      }
    })
  },

  previewImage() {
    wx.previewImage({
      urls: [this.data.filePath],
      current: 'current',
      success: (res) => {},
      fail: (res) => {},
      complete: (res) => {},
    })
  },

  previewdoc() {

    // let filePath = res.tempFiles[0].path; //微信临时文件路径
    wx.openDocument({
      filePath: this.data.filePath,
      showMenu: true, //是否显示右上角菜单按钮  默认为false
      success: function (res) {
        console.log('打开本地文档成功')
      },
      fail: function (error) {
        console.log("打开本地文件失败")
      }
    })
  }
})