<template>
  <el-container id="background">
    <el-header>
      <goback-home id="gobackhome"></goback-home>
    </el-header>
    <el-main class="middle">
      <p id="name">Gun-Send</p>
      <div id="content">
        {{ msg }}
        <p>获得帮助的渠道：</p>
        <p>如果您有任何使用上的问题，可以联系2488535755@qq.com</p>
        <p>该平台常见问题解答：</p>
        <p>Q:我可以管理我分享出去的文件吗？</p>
        <p>A:不可以，我们出于及传及分享，快捷轻便的目的，未设置账户，所以不能去管理自己的分享文件。</p>
      </div>
    </el-main>
  </el-container>
</template>

<script>
import GobackHome from '../GobackHome.vue'
export default {
  data () {
    return {
      msg: '帮助'
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
  background-image: url("../../assets/help.jpg");
  height: 100%;
  width: 100%;
  background-size: 100% 100%;
  overflow:auto;
}
#name {
  font-size: 5rem;
  font-family: STKaiti,Metropolis,Inter,X-LocaleSpecific,sans-serif;
  color: white;
  text-align: center;
  margin: 0;
}
#gobackhome {
  margin: 0;
  width: 200px;
}
#content {
  margin: 10px auto 0;
  color: white;
  font-family: STKaiti,Metropolis,Inter,X-LocaleSpecific,sans-serif;
  font-size: 2rem;
}
</style>
