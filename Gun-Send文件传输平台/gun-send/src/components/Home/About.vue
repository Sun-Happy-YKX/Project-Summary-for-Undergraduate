<template>
  <el-container id="background">
    <el-header>
      <goback-home id="gobackhome"></goback-home>
    </el-header>
    <el-main class="middle">
      <p id="name">Gun-Send</p>
      <div id="content">
        <p>{{ msg }}</p>
        <br>
        <p>本产品基于GunDB原理，具有去中心化的特点。</p>
        <p>为广大群众，提供了一个快捷方便的文件分享功能。</p>
        <br>
        <p>当前版本：1.0.0</p>
        <p>注意事项</p>
          <p>1. 功能未完善，Gun-Send-LAN还不支持测试。</p>
          <p>2. 文件上传大小仅限于50M以下。</p>
          <p>3. 本次设计暂时只支持全屏，不支持自由缩放。</p>
          <p>4. 关于产品、关于团队和帮助还未完善。</p>
          <p>5. 产品推荐使用Chrome浏览器，其他浏览器不影响功能使用，但影响显示效果。</p>
          <p>6. 跨浏览器使用不完全兼容（即IE上传的不推荐Chrome下载，但是部分浏览器可以这么处理）。</p>
          <p>7. 用户被限制的最大下载次数按点击下载按钮的次数算，而不是按照进入下载页面的次数算。</p>
          <p>8. 用户点击确认解析后才会报“超过下载次数”、“不在下载规定时间”等错。</p>
        <p>首页</p>
          <p>1. 用户点击关于产品，系统跳转至产品介绍页。</p>
          <p>2. 用户点击关于团队，系统跳转至团队介绍页。</p>
          <p>3. 用户点击帮助，系统跳转至帮助页面。</p>
          <p>4. 用户点击反馈，系统跳转至反馈页面。</p>
          <p>5. 用户点击上传文件，系统跳转至文件上传页面。</p>
          <p>6. 用户点击下载文件，系统跳转至文件下载页面。</p>
          <img src="../../assets/aboutScreen/1596000602218.png" width="100%">
          <img src="../../assets/aboutScreen/1596000640245.png" width="100%">
        <p>关于产品</p>
        <p>1. 用户点击返回首页，系统跳转至首页。</p>
        <img src="../../assets/aboutScreen/1596000577867.png" width="100%">
        <p>关于团队</p>
        <p>1. 用户点击返回首页，系统跳转至首页。</p>
        <img src="../../assets/aboutScreen/1596000672731.png" width="100%">
        <p>帮助</p>
        <p>1. 用户点击返回首页，系统跳转至首页。</p>
        <img src="../../assets/aboutScreen/1596000690143.png" width="100%">
        <p>反馈</p>
        <p>1. 用户点击返回首页，系统跳转至首页。</p>
        <p>2. 用户输入标题和内容后点击确认上传，选择确定后提示反馈成功，系统自动跳转至首页；
          若用户填写标题或内容为空，系统会提示标题/内容为空。</p>
        <img src="../../assets/aboutScreen/1596000712883.png" width="100%">

        <p>在输入标题与内容后，用户点击确认上传，系统弹出窗口</p>
        <img src="../../assets/aboutScreen/1596012077764.png" width="100%">

        <p>用户点击取消按钮，系统弹出</p>
        <img src="../../assets/aboutScreen/1596012269878.png" width="100%">

        <p>用户点击确认按钮，系统弹出并直接跳转回主页</p>
        <img src="../../assets/aboutScreen/1596012301021.png" width="100%">

        <p>用户未输入标题点提交</p>
        <img src="../../assets/aboutScreen/1596012118963.png" width="100%">

        <p>用户输入了标题，但未输入内容点提交</p>
        <img src="../../assets/aboutScreen/1596012152645.png" width="100%">

        <p>上传界面</p>
        <p>1. 用户点击文件选择，系统提供文件选择器进行多文件选择。</p>
        <p>2. 用户在“文件名称”后输入框内输入本次项目的文件名。</p>
        <p>3. 用户在“下载次数”后计数框内输入本次项目的最大下载次数。</p>
        <p>4. 用户点击“失效时间”和“生效时间”后的日期选择器，系统弹出只能时间选择弹框供用户进行选择。</p>
        <p>5. 用户点击“加密传输”后的开关，系统给出密码输入框以设置密码。</p>
        <p>6. 用户完成文件选择后，系统于右侧显示出文件列表。</p>
        <p>7. 用户在点击文件列表的某个文件后，系统进入预览界面。</p>
        <p>8. 用户点击文件列表某个文件的叉号，系统将在待上传文件列表中将其删除</p>
        <p>9. 用户点击确认上传并选择确认选项后，系统随后给出本次项目文件所对应的链接码，同时系统锁定所有的关于下载的设置输入，解锁“复制BT链接”按钮。</p>
        <p>10. 用户点击复制BT链接后，系统弹出复制成功提示，链接码成功复制到用户粘贴板上。</p>
        <p>11. 如果用户输入不合要求，用户点击“确认上传”按钮时就会报相应的错误。</p>
        <p>12. 用户点击返回首页，系统跳转至首页。</p>
        <p>总览</p>
        <img src="../../assets/aboutScreen/1596001597713.png" width="100%">

        <p>部分演示</p>
        <p>①文件选择</p>
        <img src="../../assets/aboutScreen/1596000831869.png" width="100%">

        <p>②时间选择</p>
        <img src="../../assets/aboutScreen/1596001629506.png" width="100%">

        <p>③加密传输</p>
        <img src="../../assets/aboutScreen/1596001660509.png" width="100%">

        <p>④确认上传</p>
        <p>用户点击确认上传</p>
        <img src="../../assets/aboutScreen/1596001697151.png" width="100%">

        <p>用户点击取消</p>
        <img src="../../assets/aboutScreen/1596012474217.png" width="100%">

        <p>用户点击确定</p>
        <img src="../../assets/aboutScreen/1596012517302.png" width="100%">

        <p>系统显示从这样的进度条</p>
        <img src="../../assets/aboutScreen/1596012598117.png" width="100%">

        <p>过渡到</p>
        <img src="../../assets/aboutScreen/1596001729707.png" width="100%">

        <p>可发现其他项均已禁用，用户不能再次点击</p>
        <p>⑤链接复制</p>
        <img src="../../assets/aboutScreen/1596001862883.png" width="100%">

        <p>系统弹出提示</p>
        <img src="../../assets/aboutScreen/1596001747061.png" width="100%">

        <p>下载界面</p>
        <p>1. 用户点击返回首页，系统跳转至首页。</p>
        <p>2. 用户输入解析链接，并点击确定后，系统根据是否上传时是否进行加密决定是否进行密码验证。</p>
        <p>3. 系统解析成功文件后，将文件列表呈现给用户，用户点击即可进行预览。</p>
        <p>4. 在文件解析成功后，系统提供“下载”按钮，用户点击下载按钮进行文件下载。文件名默认为“上传时项目命名.zip”。</p>
        <p>用户输入链接</p>
        <img src="../../assets/aboutScreen/1596002351056.png" width="100%">

        <p>用户点击确定，若不是正确的已存在的链接</p>
        <img src="../../assets/aboutScreen/1596012688128.png" width="100%">

        <p>是正确的已存在的链接时，系统提示输入密码</p>
        <img src="../../assets/aboutScreen/1596002405947.png" width="100%">

        <p>当用户密码输入错误</p>
        <img src="../../assets/aboutScreen/1596012812568.png" width="100%">

        <p>用户密码正确：系统显示文件列表（具有滚动轮）</p>
        <img src="../../assets/aboutScreen/1596002440303.png" width="100%">

        <p>用户点击文件可以进行预览</p>
        <img src="../../assets/aboutScreen/1596002630089.png" width="100%">

        <p>用户点击下载按钮下载文件</p>
        <img src="../../assets/aboutScreen/1596002717564.png" width="100%">

        <p>预览界面</p>
        <p>1.用户点击返回首页，系统跳转至首页。</p>
        <p>2.如果是PDF或视频预览，用户根据常识进行预览操作。</p>
        <p>3.对于某些文件格式暂不支持预览，如.doc，.pptx。</p>
        <p>4.txt文件格式文件中文乱码。</p>

        <img src="../../assets/aboutScreen/1596002767700.png" width="100%">
        <img src="../../assets/aboutScreen/1596003069117.png" width="100%">
        <img src="../../assets/aboutScreen/1596003083676.png" width="100%">

        <p>对一些暂时不支持预览的文件</p>
        <img src="../../assets/aboutScreen/1596016105148.png" width="100%">

        <p>txt类文件中文乱码问题</p>
        <img src="../../assets/aboutScreen/1596016375276.png" width="100%">

        <p>这个和用户电脑或浏览器配置相关，出现乱码需要用户自行在电脑或浏览器上进行语言包调整</p>
        <img src="../../assets/aboutScreen/image.png" width="100%">
      </div>
    </el-main>
  </el-container>
</template>

<script>
import GobackHome from '../GobackHome.vue'
export default {
  data () {
    return {
      msg: '关于产品'
    }
  },
  components: {
    GobackHome
  }
}
</script>

<style lang="scss" scoped>
.el-header {
  padding: 2px;
}
.middle {
  width: 60%;
  margin: 0 auto;
  margin-bottom: 50px;
  background: rgba(44,44,44,0.6);
}
#background {
  position: fixed;
  background-image: url("../../assets/production.jpg");
  height: 100%;
  width: 100%;
  background-size: 100% 100%;
  overflow:auto;
}
#gobackhome {
  margin: 0;
  width: 200px;
}
#name {
  font-size: 5rem;
  font-family: STKaiti,Metropolis,Inter,X-LocaleSpecific,sans-serif;
  color: white;
  text-align: center;
  margin: 0;
}
#content {
  margin: 10px auto 0;
  color: white;
  font-family: STKaiti,Metropolis,Inter,X-LocaleSpecific,sans-serif;
  font-size: 2rem;
}
</style>
