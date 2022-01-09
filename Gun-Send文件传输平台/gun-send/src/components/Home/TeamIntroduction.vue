<template>
  <el-container id="background">
    <el-header>
      <goback-home id="gobackhome"></goback-home>
    </el-header>
    <el-main class="middle">
      <p id="name">Gun-Send</p>
      <div id="content">
        {{ msg }}
        <p>团队名称：</p>
        <p>想转专业队</p>
        <p>成员组成：</p>
        <p>阳铠行--申峻宇--贾鑫---陈爽--曹亮</p>
        <p>经历概要：</p>
        <p>该小组成立于2020年7月，一起经历了难忘的企业实训，在共同的努力下，完成了这样一个基于GunDB的去中心化的文件分享平台。</p>
      </div>
    </el-main>
  </el-container>
</template>

<script>
import GobackHome from '../GobackHome.vue'
export default {
  data () {
    return {
      msg: '团队介绍'
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
  background-image: url("../../assets/team.jpg");
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
