import Toast from '@vant/weapp/toast/toast'
var _this = null
Page({

  /**
   * 页面的初始数据
   */
  data: {
    totalQuestionsNum:5,
    needQuestionsNum:3,
    questionList:[],
    fileSource:'',
    fileType:'',
    fileSize:'',
    downloadDateLimit:7, //默认下载期限是7天
    fileID:'', //云数据库里的文件id
    shareName:''
  },

  /**
   * 生命周期函数--监听页面加载
   */
  onLoad: function (options) {
    wx.showLoading({
      title: '加载问题中',
    })
    this.setData({
      fileSource:options.filePath,
      fileType:options.fileType,
      fileSize:options.fileSize,
      totalQuestionsNum:parseInt(options.totalQuestionsNum),
      needQuestionsNum:parseInt(options.needQuestionsNum),
      shareName:options.shareName,
      downloadDateLimit:options.downloadDateLimit
    })
    // 这里开始构建questionList，从数据库里面获取，有两个属性：问题+答案（数组）
    var temp_question = []
    wx.cloud.callFunction({ //用云函数测试
      name:'getQuestionFromCloud',
      data:{
        question_num:this.data.totalQuestionsNum
      },
      complete:(res)=>{
        temp_question = res.result.list
        for(var i=0;i<temp_question.length;i++){
          temp_question[i].radio = 0 
        }
        this.setData({
          questionList:temp_question,
        })
        wx.hideLoading({
          success: (res) => {},
        })
      },
    })

  },
  
  confirmSubmit: function(){
    _this = this
    var temp_questionList = _this.data.questionList;
    for(var i=0;i<temp_questionList.length;i++){
      if(temp_questionList[i].radio==0){
        Toast.fail('问题'+(i+1)+'非空');
        return
      }
    }
    wx.requestSubscribeMessage({
      tmplIds: ['Al5lWrv7uFR1hQf1BBlNGOSmHivCeKkTUTCegisgn_k'],
      success(res) {
        console.log(res)
        if(res.Al5lWrv7uFR1hQf1BBlNGOSmHivCeKkTUTCegisgn_k == 'accept'){
          _this.comfirmSubmitDetail()
        }
        else{
          wx.switchTab({
            url: '../index/index',
          })
          wx.showToast({
            title: '不同意就爬',
            duration: 5000,
          })
        }     
      },
      fail(err) {
        console.log(err);
      }
    })
   
  },
  comfirmSubmitDetail: function(){
    _this = this
    wx.showLoading({
      title:'正在上传'
    })
    const cloudPath = `my-images`+Date.now()+getApp().globalData.openid
    console.log(_this.data.fileSource)
    wx.cloud.uploadFile({
      cloudPath: cloudPath,
      filePath: _this.data.fileSource,
      success: res => {
        _this.setData({
          fileID:res.fileID
        })
        const db=wx.cloud.database()
        const todos=db.collection('question_files')
        todos.add({
          data:{
            shareName:_this.data.shareName,
            fileID:res.fileID,
            uploadDate:Date.now(),
            downloadDateLimit:_this.data.downloadDateLimit, 
            downloadNums:0, 
            fileType:_this.data.fileType,
            fileSize:_this.data.fileSize,
            needQuestionsNum:_this.data.needQuestionsNum,
            questionList: _this.data.questionList,
            accessUsersList: []
          },
          success: res => {
            wx.navigateTo({ //跳转至上传完成界面
              url: '../uploadFinishPage/uploadFinishPage?recordID='+res._id+'&shareType=question'+'&shareName='+_this.data.shareName,
            })
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
  onChange: function(event){
    var idx = parseInt(event.target.dataset.idx)
    var temp_questionList = this.data.questionList
    temp_questionList[idx].radio = parseInt(event.detail)
    temp_questionList[idx].chooseAnswer = 0
    this.setData({
      questionList: temp_questionList
    })
  },

  setDateShow(e){
    this.setData({
      showDateLimit:e.detail
    })
  },
})