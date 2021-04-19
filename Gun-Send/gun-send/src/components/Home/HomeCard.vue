<template>
  <div class="box-card">
    <div class="box-inner">
      <h1 class="welcome">
        亲爱的朋友，欢迎来到文件共享平台
        <span class="name">Gun-Send</span>
        !
      </h1>
      <p class="body">
        听说你还在寻找文件分享捷径？
        <br>
      </p>
      <div class="upload">
        <span class="upload-text">尝试在Gun-Send上传你的第一个文件吧</span>
        <button class="upload-button" @click="jumptoupload">上传文件</button>
      </div>
      <div class="download">
        <button class="download-button" @click="jumptodownload">下载文件</button>
        <span class="download-text">使用好友分享的链接去下载文件</span>
        <span class="arrow"><i class="el-icon-right"></i></span>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  methods: {
    jumptoupload () {
      this.$router.push('/Upload')
    },
    jumptodownload () {
      this.$router.push('/Download')
    }
  }
}
</script>

<style scoped>
.box-card {
  width: 800px;
  height: 350px;
  padding-left: 50px;
  padding-top: 30px;
  background-color: #E0FFFF;
  box-shadow: #a1a1a1 0px 1px 5px;
}
.box-inner {
  display: flex;
  flex-direction: column;
  height: 297px;
}
.welcome {
  letter-spacing: 2px;
  font-size: 30px;
  margin-bottom: 30px;
}
.name {
  color: #ce25ce;
}
.upload {
  display: flex;
  background-color: #f16272;
  color: #fff;
  letter-spacing: 1px;
  height: 75px;
  width: 550px;
  align-items: center;
  justify-content: center;
}
.upload:hover {
  background-color: #000;
}
.download {
  margin-top: 50px;
}
.upload-button {
  background-color: transparent;
  border: 1px solid #def15c;
  color: #def15c;
  margin-left: 10px;
  height: 40px;
  font-weight: bold;
  font-size: 20px;
  letter-spacing: 1.5px;
}
.download-button {
  background-color: #f16272;
  color: #fff;
  margin-right: 10px;
  height: 30px;
  font-weight: bold;
  letter-spacing: 1.5px;
  border: 0;
  width: 100px;
}
.download-button:hover {
  background-color: #000;
}
.download-text {
  color: #000;
  letter-spacing: 1.5px;
  font-weight: bold;
}
.arrow {
  color: #000;
  margin-left: 10px;
}
.body {
  color: #656565;
  font-size: 18px;
  letter-spacing: 1.5px;
}
.upload-text {
  font-size: 18px;
  letter-spacing: 1.5px;
}
</style>
