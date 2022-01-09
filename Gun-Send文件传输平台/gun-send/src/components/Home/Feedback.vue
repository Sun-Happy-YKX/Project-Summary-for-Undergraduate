<template>
<el-container id="background">
  <el-header>
    <goback-home id="gobackhome"></goback-home>
  </el-header>
  <el-main class="middle">
    <p id="name">Gun-Send</p>
    <div id="feedbackmain">
      <div class="tips">输入标题：</div>
      <el-input class="feedinput" type="textarea" autosize placeholder="请输入标题"
      v-model="textarea1" @change="sendTitle"></el-input>
      <div style="margin: 20px 0;"></div>
      <div class="tips">输入内容：</div>
      <el-input class="feedinput" type="textarea" :autosize="{ minRows: 8, maxRows: 12}" placeholder="请输入内容"
      v-model="textarea2" @change="sendContent"></el-input><br>
      <confirm-upload id="conbtn"></confirm-upload>
    </div>
  </el-main>
</el-container>
</template>

<script>
import GobackHome from '../GobackHome.vue'
import ConfirmUpload from './ConfirmUpload'
export default {
  data () {
    return {
      textarea1: '',
      textarea2: ''
    }
  },
  components: {
    GobackHome,
    ConfirmUpload
  },
  methods: {
    sendTitle () {
      this.$bus.emit('sendTitle', this.textarea1)
    },
    sendContent () {
      this.$bus.emit('sendContent', this.textarea2)
    }
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
  background-image: url("../../assets/feedback.jpg");
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
#feedbackmain {
  margin: 0 auto;
  padding: 50px;
  width: 80%;
}
.tips {
  color: white;
}
.feedinput {
  width: 100%;
  margin: 2px auto;
}
#conbtn {
  margin-top: 6px;
}
</style>
