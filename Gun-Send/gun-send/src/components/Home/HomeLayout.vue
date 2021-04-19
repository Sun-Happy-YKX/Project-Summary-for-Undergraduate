<template>
  <div class="container">
    <el-row :gutter="40">
      <el-col :span="4"><span class="title grid-content bg-purple">Gun-Send</span></el-col>
      <el-col :span="3"><el-button @click.native="jumptoabout" type="text" class="grid-content bg-purple"><span>关于产品</span></el-button></el-col>
      <el-col :span="2.5"><el-button @click.native="jumptoteam" type="text" class="grid-content bg-purple"><span>关于团队</span></el-button></el-col>
      <el-col :span="2.5"><el-button @click.native="jumptohelp" type="text" class="grid-content bg-purple"><span>帮助</span></el-button></el-col>
      <el-col :span="3"><el-button @click.native="jumptofeedback" type="text" class="grid-content bg-purple"><span>反馈</span></el-button></el-col>
    </el-row>
  </div>
</template>

<script>
export default {
  name: 'HomeLayout',
  methods: {
    jumptoabout () {
      this.$router.push('/Home/About')
    },
    jumptoteam () {
      this.$router.push('/Home/TeamIntroduction')
    },
    jumptohelp () {
      this.$router.push('/Home/Help')
    },
    jumptofeedback () {
      this.$router.push('/Home/Feedback')
    }
  }
}
</script>

<style lang="scss" scoped>
.container {
  width: 1200px;
}
.el-row {
  margin-bottom: 20px;
  &:last-child {
    margin-bottom: 0;
  }
}
.el-col {
  border-radius: 4px;
}
.el-button:hover span {
  color: rgb(252, 235, 0);
}
.bg-purple {
  color: #ffffff;
  width: 100px;
}
.grid-content {
  margin-top: 20px;
  border-radius: 4px;
  min-height: 36px;
  font-size: 20px;
}
.title {
  background-color: #f16272;
  color: #fff;
  height: 30px;
  font-weight: bold;
  letter-spacing: 1.5px;
  border: 0;
  width: 150px;
  font-size: 18px;
  text-align: center;
  line-height: 35px;
  display: inline-block;
  margin-left: 30px;
}
</style>
