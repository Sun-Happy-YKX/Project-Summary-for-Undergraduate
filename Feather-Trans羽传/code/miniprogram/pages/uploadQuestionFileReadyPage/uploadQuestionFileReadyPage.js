// miniprogram/pages/uploadQuestionFileReadyPage/uploadQuestionFileReadyPage.js
import Notify from '@vant/weapp/notify/notify'

Page({

  /**
   * 页面的初始数据
   */
  data: {
    fileSource:'', //文件路径
    fileType:'',  //文件类型
    fileSize:2,
    shareNameValue:'', //分享的名称
    totalQuestionsNum:5, //问题总数
    needQuestionsNum:3, //需要答对的问题数
    showDateLimit:false,
    downloadDateLimit:7
  },

  /**
   * 生命周期函数--监听页面加载
   */
  onLoad: function (options) {
    this.setData({
      fileSource:options.filePath,
      fileType:options.fileType
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

  onDragTotalQuestionsNum(e){ //拖拽进度条   
    this.setData({
      totalQuestionsNum:e.detail.value,
    })
  },

  onChangeTotalQuestionsNum(e){ //直接点进度条   
    this.setData({
      totalQuestionsNum:e.detail,
      needQuestionsNum:e.detail
    })
  },

  onDragEndTotalQuestion(){
    this.setData({
      needQuestionsNum:this.data.totalQuestionsNum
    })
  },

  onDragNeedQuestionsNum(e){
    this.setData({
      needQuestionsNum:e.detail.value
    })
  },

  onChangeNeedQuestionsNum(e){
    this.setData({
      needQuestionsNum:e.detail
    })
  },

  startSelectQuestion(){ //开始选择问题,跳转界面
    if(this.data.shareNameValue==''){
      Notify({ type: 'primary', message: '分享名称不能为空' })
      return
    }
    wx.navigateTo({
      url: '../selectQuestionsPage/selectQuestionsPage?filePath='+this.data.fileSource+
      '&fileType='+this.data.fileType+'&shareName='+this.data.shareNameValue+'&downloadDateLimit='+this.data.downloadDateLimit+'&totalQuestionsNum='+this.data.totalQuestionsNum+
      '&needQuestionsNum='+this.data.needQuestionsNum+'&fileSize='+this.data.fileSize
    })
  },

  setDateShow(e){
    this.setData({
      showDateLimit:e.detail
    })
  },

  onChangeDateLimit(e){
    this.setData({
      downloadDateLimit:e.detail
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