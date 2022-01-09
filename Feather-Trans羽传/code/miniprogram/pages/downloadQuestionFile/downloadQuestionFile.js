// miniprogram/pages/shareOpenPage/shareOpenPage.js
const db = wx.cloud.database()
const todos = db.collection('question_files')
var _this = null
const app = getApp()
const oneDay = 24 * 60 * 60 * 1000

Page({

  /**
   * 页面的初始数据
   */
  data: {
    isButtonForbidden: false, //按钮是否被禁用
    showPreviewButton: false,
    res: '',
    recordID: '',
    shareName: '',
    fileSize: 0,
    fileType: '',
    buttonText: '下载文件', //要是不符合条件就会变成其他文字 todo 最好按钮颜色也一并变化
    fileID: '',
    filePath: '',
    openid: '',
    userInfo: '',
    ownerOpenID: '',
    downloadDateLimit: '',
    actionSheetShow: false,
    showPasswordPop: false,
    is_password_false: false,
    enter_password: '',
    surplus_enter_num: 5, //输入密码容许五次输入错误
    questionList: [],
    accessUsersList: [],
    showQuestionPop: false,
    questionErrorTip: false,
    questionErrorText: '',
    needQuestionsNum: 0,
    actions: [{
      name: '保存到手机'
    }]
  },

  /**
   * 生命周期函数--监听页面加载
   */
  onLoad: function (options) {
    _this = this
    this.setData({
      recordID: options.recordID //先随便给个测试数据跑通
      // recordID: '79550af260abd10019d95a431c1d2451'
    })
    wx.showLoading({
      title: '加载中',
    })
    console.log('调用login之前')
    wx.cloud.callFunction({
      name: 'login',
      data: {},
      success: res => {
        _this.setData({
          openid: res.result.openid
        })
        app.globalData.openid = res.result.openid
        _this.InitalConditionCheck()
      },
      fail: err => {
        console.error('[云函数] [login] 调用失败', err)
      }
    })
  },
  InitalConditionCheck() {
    todos.doc(this.data.recordID).get({ //云数据库里获取文件数据
      success: (res) => {
        this.setData({
          res: res.data,
          fileID: res.data.fileID
        })
        wx.cloud.callFunction({
          name: "getUserInfo",
          data: {
            userID: _this.data.openid
          },
          success: res => {
            _this.setData({
              userInfo: res.result.data[0]._userInfo
            })
          },
          fail: err => {
            reject(err)
          }
        })
        //开始给页面元素赋值
        var oneDay = 24 * 60 * 60 * 1000
        var res = this.data.res
        this.setData({
          shareName: res.shareName,
          fileSize: res.fileSize,
          fileType: res.fileType,
          downloadDateLimit: res.uploadDate + res.downloadDateLimit * oneDay,
          questionList: res.questionList,
          needQuestionsNum: res.needQuestionsNum,
          accessUsersList: res.accessUsersList,
          ownerOpenID: res._openid
        })
        // 先判断这人之前有没有访问过
        var access_list = this.data.accessUsersList
        var this_user_openID = app.globalData.openid
        var is_contained = false
        for (var i = 0; i < access_list.length; i++) {
          if (this_user_openID == access_list[i].userID) {
            is_contained = true
          }
        }
        // for循环可能要遍历一下，我怕还没遍历完就直接判断容易gg
        if (is_contained == true) {
          wx.switchTab({
            url: '../index/index',
          })
          wx.showToast({
            title: '已经回答过了',
            icon: 'error',
            duration: 5000,
          })
          wx.hideLoading({
            success: (res) => {},
          })
          return
        }
        wx.hideLoading({
          success: (res) => {},
        })
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
            buttonText: '超过下载期限'
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
  closePasswordPop: function () {
    this.setData({
      showPasswordPop: false,
      is_password_false: false,
      enter_password: ''
    })
  },
  downloadSharedFile() { //点击下载按钮之后
    if (this.data.isButtonForbidden == true) {
      return
    }
    this.setData({
      showQuestionPop: true
    })
  },
  updateAccessUsersData: function (right_num, total_num) {
    var access_item = {
      userID: app.globalData.openid,
      userRightNum: right_num,
      userTotalNum: total_num
    }
    this.data.accessUsersList.push(access_item)
    db.collection('question_files').doc(this.data.recordID).update({
      data: {
        accessUsersList: this.data.accessUsersList
      },
      success: function (res) {

      }
    })
  },
  downloadFile: function () {
    _this = this
    wx.showLoading({
      title: '正在下载',
    })
    wx.cloud.downloadFile({
      fileID: this.data.fileID,
      success: res => {
        this.setData({
          filePath: res.tempFilePath
        })
        if (this.data.fileType == 'file') {
          this.setData({
            showPreviewButton: true
          })
        }
        wx.hideLoading({
          success: (res) => {},
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
  closeQuestionPop: function () {
    this.setData({
      showQuestionPop: false
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
        console.log(app.globalData)
      },
      fail: err => {
        console.error('[云函数] [login] 调用失败', err)
      }
    })
  },
  onQuestionChange: function (event) {
    var idx = parseInt(event.target.dataset.idx)
    var temp_questionList = this.data.questionList
    temp_questionList[idx].chooseAnswer = parseInt(event.detail)
    this.setData({
      questionList: temp_questionList
    })
  },
  confirmQuestion: function () {
    for (var i = 0; i < this.data.questionList.length; i++) {
      if (this.data.questionList[i].chooseAnswer == 0) {
        this.setData({
          questionErrorTip: true,
          questionErrorText: '问题' + (i + 1) + '非空'
        })
        return
      }
    }
    var right_count = 0
    for (var i = 0; i < this.data.questionList.length; i++) {
      if (this.data.questionList[i].radio == this.data.questionList[i].chooseAnswer) {
        right_count++
      }
    }
    if (right_count >= this.data.needQuestionsNum) {
      this.downloadFile()
      this.setData({
        isButtonForbidden: true,
        showQuestionPop: false
      })
      // 这里密码输入正确说明这人去答题了，我们提示一下文件主
      wx.cloud.callFunction({
        name: 'sendMessage',
        data: {
          'accepterID': _this.data.ownerOpenID,
          'messageContent': '有人参与了答题，快来看看他的答题情况吧！',
          'senderName': _this.data.userInfo.nickName,
          'sendTime': _this.getNowTimeParse(),
          'fileID': _this.data.recordID
        },
        success: res => {
          console.log('发送订阅消息 调用成功')
        },
        fail: err => {
          console.error('[云函数] 调用失败', err)
        }
      })
      _this.updateAccessUsersData(right_count, _this.data.questionList.length)
    } else {
      wx.switchTab({
        url: '../index/index'
      })
      wx.showToast({
        title: '题目错太多',
        duration: 5000,
      })
    }
  },
  getNowTimeParse() {
    const time = new Date();
    const YYYY = time.getFullYear();
    const MM = time.getMonth() < 9 ? '0' + (time.getMonth() + 1) : (time.getMonth() + 1);
    const DD = time.getDate() < 10 ? '0' + time.getDate() : time.getDate();
    const hh = time.getHours() < 10 ? '0' + time.getHours() : time.getHours();
    const mm = time.getMinutes() < 10 ? '0' + time.getMinutes() : time.getMinutes();
    const ss = time.getSeconds() < 10 ? '0' + time.getSeconds() : time.getSeconds();
    const ms = time.getMilliseconds()
    return `${YYYY}-${MM}-${DD} ${hh}:${mm}:${ss}`;
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